from __future__ import annotations

import streamlit as st


def render_post(payload: dict):
    st.subheader("Generated Post")
    st.text_area("Body (copyable)", value=payload.get("body", ""), height=300)
    st.write("**Hashtags:**", " ".join(payload.get("hashtags", [])))
    srcs = payload.get("sources", [])
    if srcs:
        with st.expander("Sources", expanded=True):
            for u in srcs:
                st.write(u)
