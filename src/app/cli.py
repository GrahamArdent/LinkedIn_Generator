from __future__ import annotations
from datetime import date
from pathlib import Path
import argparse
import os

from dotenv import load_dotenv
load_dotenv()

from .scheduler import load_schedule, resolve_persona_for_date
from .prompt_builder import build_prompt_blocks
from .research import pick_quote, pick_stat
from .composer import compose_post, build_carousel_from_text
from .validators import validate_post, enforce_no_links_in_body
from .renderer import render_to_files
from .citations import load_citations, pick_citations, load_whitelist, filter_to_whitelist
from .topics_loader import load_topics, select_topic_for
from .persona_logic import enrich_with_persona_rules
from .image_brief import make_carousel_brief
from .generation import generate_post_via_llm, to_text
from . import logger

BASE = Path(__file__).resolve().parents[2]
CONFIG = BASE / "config"
DATA = BASE / "data"
OUT = BASE / "out"

def _load_topics_local_then_env() -> tuple[list[dict], list[dict]]:
    g1 = DATA / "Graham_120Day_Final.csv"
    a1 = DATA / "Ardent_12Week_Filled_2025-09-23.csv"
    topics_graham = load_topics(g1) if g1.exists() else []
    topics_ardent = load_topics(a1) if a1.exists() else []
    g_env = os.getenv("GRAHAM_TOPICS_CSV")
    a_env = os.getenv("ARDENT_TOPICS_CSV")
    if not topics_graham and g_env:
        topics_graham = load_topics(Path(g_env))
    if not topics_ardent and a_env:
        topics_ardent = load_topics(Path(a_env))
    return topics_graham, topics_ardent

def _allowed_source_titles(cites: list[dict]) -> list[str]:
    titles = []
    for c in cites:
        t = c.get("title")
        if t:
            titles.append(t)
    return titles[:5]

def main() -> None:
    parser = argparse.ArgumentParser(description="Dual-persona LinkedIn post generator")
    parser.add_argument("command", choices=["post"], help="generate content")
    parser.add_argument("--date", help="YYYY-MM-DD (default: today)")
    parser.add_argument("--persona", help="override persona key")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--llm", action="store_true", help="Use LLM pipeline")
    parser.add_argument("--post-type", choices=["text", "doc_carousel"], default="text")
    args = parser.parse_args()

    if args.command != "post":
        raise SystemExit("Unknown command")

    the_date = date.fromisoformat(args.date) if args.date else date.today()

    schedule = load_schedule(CONFIG / "schedule.yaml")
    persona_key = args.persona or resolve_persona_for_date(schedule, the_date)
    if not persona_key:
        print("No persona scheduled for this date.")
        return

    blocks = build_prompt_blocks(CONFIG)
    quote = pick_quote(DATA)
    stat = pick_stat(DATA)
    all_cites = load_citations(DATA)
    whitelist = load_whitelist(CONFIG)

    topics_graham, topics_ardent = _load_topics_local_then_env()
    chosen = select_topic_for(the_date, persona_key, topics_graham, topics_ardent)

    topic_hint = stat.get("metric") if stat else None
    cites = pick_citations(all_cites, topic=topic_hint, max_items=2)
    cites = filter_to_whitelist(cites, whitelist)

    payload = compose_post(persona_key, blocks, quote, stat, citations=cites)
    if chosen and chosen.get("topic"):
        payload["metadata"]["selected_topic"] = chosen["topic"]
        payload = enrich_with_persona_rules(payload, persona_key, chosen["topic"])

    if args.llm:
        ctx = {
            "persona_key": persona_key,
            "objective": "Educate (Graham) or convert (Ardent) depending on persona.",
            "topic": payload["metadata"].get("selected_topic", payload["metadata"].get("topic_key", "identity")),
            "pillar": payload["metadata"].get("inferred_pillar", "trend_decode"),
            "services": payload["metadata"].get("service_map", []),
            "cta_allow": blocks["personas"][persona_key].get("cta_patterns", []),
            "hashtags": blocks["hashtags"][blocks["personas"][persona_key]["hashtag_set"]],
            "allowed_sources": _allowed_source_titles(cites),
        }
        post_json = generate_post_via_llm(CONFIG, ctx)
        payload["body"] = to_text(post_json)

    # house rules
    payload["body"] = enforce_no_links_in_body(payload["body"])
    links = [c.get("url") for c in cites if c.get("url")]
    q1 = "Which control is most brittle in practice: identity, endpoints, or SaaS trust?"
    q2 = "Want the checklist? Say 'checklist' and I’ll DM it."
    first_comment = "\n".join(["[Q] " + q1, "[Q] " + q2, "", "Links:"] + links).strip()

    brief = make_carousel_brief(payload)
    payload["metadata"]["image_brief"] = brief

    post_type = args.post_type
    carousel = None
    if post_type == "doc_carousel":
        carousel = build_carousel_from_text(payload["body"])

    basename = f"{the_date.isoformat()}_{persona_key}_{post_type}"
    paths = render_to_files(
        {
            "persona": persona_key,
            "post_type": post_type,
            "body": payload["body"],
            "first_comment": first_comment,
            "citations": cites,
            "carousel": carousel,
            "metadata": payload["metadata"],
        },
        OUT,
        basename,
    )

    if args.dry_run:
        print(payload["body"])
        print("\n[First comment]\n" + first_comment)
        if carousel:
            print("\n[Carousel slides]")
            for i, s in enumerate(carousel, 1):
                print(f"{i}. {s['title']}")
    else:
        # append analytics log
        info = {
            "date": the_date.isoformat(),
            "persona": persona_key,
            "post_type": post_type,
            "body": payload["body"],
            "hashtags": payload["metadata"].get("hashtags", []),
            "citations": cites,
            "paths": paths,
        }
        log_path = logger.append_log(OUT, info)
        print(f"Saved: {paths['md']}\nMeta: {paths['meta']}\nLogged: {log_path}")

if __name__ == "__main__":
    main()
