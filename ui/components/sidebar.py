from __future__ import annotations

import streamlit as st


def sidebar_controls(
    personas: list[str], schedules: list[str], display_names: dict, invalid: dict | None = None
):
    st.sidebar.header("Controls")
    persona = st.sidebar.selectbox("Persona", personas, index=0)

    def _fmt(fn: str) -> str:
        alias = display_names.get(fn, fn)
        return f"{alias} ({fn})" if alias != fn else fn

    idx = st.sidebar.selectbox(
        "Schedule",
        range(len(schedules)),
        format_func=lambda i: _fmt(schedules[i]) if i < len(schedules) else "",
        index=0,
    )
    regenerate = st.sidebar.checkbox("Regenerate variants", value=False)
    run_btn = st.sidebar.button("Generate Post")
    with st.sidebar.expander("Debug: discovered calendars"):
        for fn in schedules:
            st.write("•", _fmt(fn))
        if invalid:
            st.write("---")
            st.write("Ignored (not calendar-like or missing topic):")
            for fn in invalid.keys():
                st.write("•", fn)
    return {
        "persona": persona,
        "schedule": schedules[idx] if schedules else "",
        "regenerate": regenerate,
        "run": run_btn,
    }
