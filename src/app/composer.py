from __future__ import annotations

from typing import Any


def compose_post(
    persona_key: str,
    prompt_blocks: dict[str, Any],
    quote: dict[str, str],
    stat: dict[str, str],
    citations: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    pconf = prompt_blocks["personas"][persona_key]
    skeleton = prompt_blocks["prompts"]["skeleton"]["sections"]
    hashtags_pool = prompt_blocks["hashtags"][pconf["hashtag_set"]]

    sections: list[str] = []
    for sec in skeleton:
        if sec == "hook":
            sections.append(
                "Leaders lose more to silent identity drift than to loud malware headlines."
            )
        elif sec == "exec_pov":
            sections.append(
                "Executives don’t buy controls — they buy continuity. The risk isn’t the exploit; it’s the downstream cash burn, disclosure clocks, and stalled roadmap."
            )
        elif sec == "proof_point":
            if stat:
                sections.append(
                    f"Data point: {stat.get('metric')} ≈ {stat.get('value')}{stat.get('unit','')} ({stat.get('source')}, {stat.get('date')})."
                )
        elif sec == "micro_plays":
            sections.append(
                "\n".join(
                    [
                        "Do now: enforce live-callback approvals for high-risk changes.",
                        "Do next: inventory high-trust SaaS integrations and rotate tokens.",
                        "Never: rely on annual point-in-time tests for assurance.",
                    ]
                )
            )
        elif sec == "quote":
            if quote:
                sections.append(
                    f"\"{quote.get('quote')}\" — {quote.get('author')} ({quote.get('source')})"
                )
        elif sec == "cta":
            sections.append(pconf["cta_patterns"][0])
        elif sec == "hashtags":
            sections.append(" ".join(hashtags_pool[:5]))

    body = "\n\n".join(sections)
    if citations:
        cites_lines = [
            f"Source: {c.get('title')} ({c.get('publisher')}, {c.get('pub_date')}) - {c.get('url')}"
            for c in citations
        ]
        body += "\n\n" + "\n".join(cites_lines)

    return {
        "persona": persona_key,
        "body": body,
        "metadata": {
            "quote": quote,
            "stat": stat,
            "hashtags": hashtags_pool[:5],
        },
    }


def _split_paras(text: str) -> list[str]:
    return [p.strip() for p in text.replace("\r", "").split("\n\n") if p.strip()]


def _extract_micro(text: str) -> dict:
    """Return dict with do_now, do_next, never if present."""
    do_now = do_next = never = ""
    for line in text.splitlines():
        s = line.strip()
        if s.lower().startswith("do now:"):
            do_now = s
        elif s.lower().startswith("do next:"):
            do_next = s
        elif s.lower().startswith("never:"):
            never = s
    return {"do_now": do_now, "do_next": do_next, "never": never}


def build_carousel_from_text(text: str) -> list[dict]:
    paras = _split_paras(text)
    hook = paras[0] if paras else "Identity drift is the quiet breach."
    pov = next(
        (p for p in paras if "continuity" in p.lower() or "risk" in p.lower()),
        paras[1] if len(paras) > 1 else "",
    )
    proof = next((p for p in paras if p.lower().startswith("data point:")), "")
    micro_src = next(
        (
            p
            for p in paras
            if p.lower().startswith("do now:")
            or "do next:" in p.lower()
            or p.lower().startswith("never:")
        ),
        "",
    )
    micro = _extract_micro(micro_src)
    cta = next(
        (
            p
            for p in paras
            if "see how ardent can help" in p.lower() or "book an assessment" in p.lower()
        ),
        "",
    )

    slides = [
        {"title": "Hook", "bullets": [hook]},
        {"title": "Executive POV", "bullets": [pov] if pov else []},
        {"title": "Proof", "bullets": [proof] if proof else []},
        {"title": "Do now", "bullets": [micro["do_now"]] if micro["do_now"] else []},
        {"title": "Do next", "bullets": [micro["do_next"]] if micro["do_next"] else []},
        {"title": "Never", "bullets": [micro["never"]] if micro["never"] else []},
        {"title": "CTA", "bullets": [cta] if cta else []},
    ]
    return slides
