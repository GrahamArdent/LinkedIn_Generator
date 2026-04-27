# Streamlit UI — Topic picker, carousel editor, clipboard/download
from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

# Load .env so OPENAI_API_KEY (and friends) are available to the LLM path
try:
    from dotenv import load_dotenv  # pip install python-dotenv (already in your venv)

    load_dotenv(dotenv_path=ROOT / ".env")
except Exception:
    # Non-fatal; the non-LLM path still works if .env is missing
    pass

import streamlit as st
from streamlit.components.v1 import html

from app import logger
from app.api import generate_post
from app.renderer import render_to_files
from app.scheduler import load_schedule, resolve_persona_for_date
from app.topics_loader import load_topics

st.set_page_config(page_title="LinkedIn Generator", layout="wide")


def copy_button(label: str, text: str):
    """Client-side clipboard copy button."""
    safe = (text or "").replace("\\", "\\\\").replace("`", "\\`")
    html(
        f"""
        <button onclick="navigator.clipboard.writeText(`{safe}`)"
                style="padding:6px 10px;margin:4px 0;">
            {label}
        </button>
        """,
        height=40,
    )


def find_ardent_topics_file(data_dir: Path) -> Path | None:
    """
    Prefer explicit env var; otherwise try new and old filename patterns.
    Supports e.g. ardent_linkedin_20week_schedule.csv.
    """
    # 1) ENV override wins
    a_env = os.getenv("ARDENT_TOPICS_CSV")
    if a_env:
        p = Path(a_env)
        return p if p.exists() else None

    # 2) Flexible autodiscovery (new patterns first, legacy last)
    patterns = [
        "ardent_*_schedule.csv",
        "ardent*week*schedule*.csv",
        "ardent_*schedule*.csv",
        "Ardent_12Week*.csv",  # legacy
    ]
    for pat in patterns:
        matches = sorted((data_dir).glob(pat), reverse=True)
        if matches:
            return matches[0]
    return None


def load_topics_for_persona(data_dir: Path, persona: str):
    """
    Return (topics_list, path_used).
    Accepts headers: topic | title | post_topic | theme | subject | hook
    """
    if persona == "graham":
        p = data_dir / "Graham_120Day_Final.csv"
    else:
        p = find_ardent_topics_file(data_dir)
    topics = load_topics(p) if p and p.exists() else []
    return topics, p


st.title("LinkedIn Generator — Preview & Edit")

today = dt.date.today()
date_val = st.date_input("Date", value=today)

# Persona auto-resolves from schedule, but allow override
sched = load_schedule(ROOT / "config" / "schedule.yaml")
auto_persona = resolve_persona_for_date(sched, date_val) or "graham"
persona = st.selectbox(
    "Persona", options=["graham", "ardent"], index=0 if auto_persona == "graham" else 1
)

ptype = st.radio("Post type", options=["text", "doc_carousel"], horizontal=True)
use_llm = st.checkbox("Use LLM rewrite", value=False, help="Requires OPENAI_API_KEY in .env")

# Topic picker (from your planning CSVs)
topics, topics_path = load_topics_for_persona(ROOT / "data", persona)
topic_options = [t.get("topic") for t in topics if t.get("topic")] if topics else []

if topic_options:
    override_topic = st.selectbox("Topic (from your plan)", options=topic_options, index=0)
else:
    # Allow manual entry if no CSV topics found
    override_topic = st.text_input("Topic (manual — no CSV topic detected)", value="")

with st.expander("Topic source (debug)", expanded=False):
    st.write("**Topics file:**", str(topics_path) if topics_path else "—")
    st.write("**Topics found:**", len(topic_options))
    if topic_options:
        st.write("**Preview:**", topic_options[:5])

if st.button("Generate preview", use_container_width=True):
    try:
        with st.spinner("Generating..."):
            selected = override_topic.strip() if override_topic else None
            if not selected:
                selected = None  # pass None if empty
            payload = generate_post(
                date_val,
                persona_key=persona,
                post_type=ptype,
                use_llm=use_llm,
                override_topic=selected,
            )
        st.session_state["payload"] = payload
    except Exception as e:
        # Show any errors (e.g., missing OPENAI_API_KEY) without crashing the app
        st.error(str(e))

# -------- Preview pane --------
if "payload" in st.session_state:
    payload = st.session_state["payload"]
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Body")
        st.text_area("Body (read-only)", payload["body"], height=260, key="body_ro")
        copy_button("Copy Body", payload["body"])
        st.download_button(
            "Download Body .txt",
            data=payload["body"],
            file_name=f"{date_val.isoformat()}_{persona}_{ptype}_body.txt",
        )

        st.subheader("First comment")
        st.text_area("First comment (read-only)", payload["first_comment"], height=160, key="fc_ro")
        copy_button("Copy First Comment", payload["first_comment"])
        st.download_button(
            "Download First Comment .txt",
            data=payload["first_comment"],
            file_name=f"{date_val.isoformat()}_{persona}_{ptype}_firstcomment.txt",
        )

        st.subheader("Citations")
        for c in payload["citations"]:
            st.write(
                f"- {c.get('title')} ({c.get('publisher')}, {c.get('pub_date')}) — {c.get('url')}"
            )

    with col2:
        st.subheader("Meta")
        st.json(
            {
                "persona": payload["persona"],
                "post_type": payload["post_type"],
                "hashtags": payload["metadata"].get("hashtags"),
                "image_brief": payload["metadata"].get("image_brief"),
                "selected_topic": payload["metadata"].get("selected_topic"),
            }
        )

        # Inline carousel editor (for doc_carousel posts)
        if payload.get("post_type") == "doc_carousel":
            st.subheader("Carousel slides (edit before saving)")
            slides = payload.get("carousel") or []
            new_slides = []
            for i, s in enumerate(slides, 1):
                with st.expander(f"Slide {i}: {s.get('title','')}", expanded=(i <= 3)):
                    title = st.text_input(f"Title {i}", s.get("title", ""), key=f"title_{i}")
                    bullets_text = "\n".join(s.get("bullets", []))
                    bullets_text = st.text_area(
                        f"Bullets {i} (one per line)", bullets_text, height=120, key=f"bullets_{i}"
                    )
                    new_slides.append(
                        {
                            "title": title.strip(),
                            "bullets": [b.strip() for b in bullets_text.splitlines() if b.strip()],
                        }
                    )
            if st.button("Apply slide edits"):
                payload["carousel"] = new_slides
                st.session_state["payload"] = payload
                st.success("Slides updated in preview. Remember to Save to out/.")

st.divider()

# -------- Save block --------
if st.button("Save to out/", type="primary", use_container_width=True):
    if "payload" not in st.session_state:
        st.error("Nothing to save yet — click Generate preview first.")
    else:
        payload = st.session_state["payload"]
        out_dir = ROOT / "out"
        basename = f"{date_val.isoformat()}_{persona}_{ptype}"
        paths = render_to_files(payload, out_dir, basename)
        log_path = logger.append_log(
            out_dir,
            {
                "date": date_val.isoformat(),
                "persona": persona,
                "post_type": ptype,
                "body": payload["body"],
                "hashtags": payload["metadata"].get("hashtags", []),
                "citations": payload.get("citations", []),
                "paths": paths,
            },
        )
        st.success(f"Saved {paths['md'].name} and {paths['meta'].name}. Logged to {log_path.name}.")
