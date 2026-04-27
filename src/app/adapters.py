from __future__ import annotations

from .rag import retrieve


def pick_quote(topic: str, angle: str) -> str:
    items = retrieve(topic, angle, k=1)
    if not items:
        return ""
    it = items[0]
    return f"{it.get('title','')} — {it.get('one_liner','')}"


def pick_stat(topic: str, angle: str) -> str:
    items = retrieve(topic, angle, k=1)
    if not items:
        return ""
    it = items[0]
    return it.get("one_liner", "")
