from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .citations import filter_to_whitelist, load_citations, load_whitelist

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def lexical_score(s: str, q: str) -> int:
    s = s.lower()
    score = 0
    for w in re.findall(r"[a-z0-9]{3,}", q.lower()):
        if w in s:
            score += 1
    return score


def retrieve(topic: str, angle: str, k: int = 3) -> list[dict[str, Any]]:
    """Return positively relevant citations from approved source domains only.

    Auto-retrieval is evidence assistance, not permission to fill a draft with
    whatever happens to be available. If the source whitelist is absent, or no
    approved citation has positive lexical relevance, return no evidence.
    """

    whitelist = load_whitelist(CONFIG_DIR)
    if not whitelist:
        return []

    items = filter_to_whitelist(load_citations(DATA_DIR), whitelist)
    query = f"{topic} {angle}".strip()
    scored: list[tuple[int, dict[str, Any]]] = []

    for item in items:
        searchable = " ".join(
            str(item.get(key, ""))
            for key in ("title", "one_liner", "fact", "tags", "domain")
        )
        score = lexical_score(searchable, query)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[: max(1, k)]]
