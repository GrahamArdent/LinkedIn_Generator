from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse

import yaml


def load_citations(data_dir: Path) -> list[dict[str, str]]:
    path = data_dir / "citations.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_whitelist(config_dir: Path) -> set[str]:
    path = config_dir / "source_whitelist.yaml"
    if not path.exists():
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    doms = data.get("domains", []) or []
    return {str(d).strip().lower().removeprefix("www.") for d in doms}


def _domain(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
        if not host and url:
            host = url.lower()
        return host.removeprefix("www.")
    except Exception:
        return ""


def _matches_whitelist(host: str, whitelist: set[str]) -> bool:
    if not whitelist:
        return True
    for w in whitelist:
        if host == w or host.endswith("." + w):
            return True
    return False


def filter_to_whitelist(cites: list[dict[str, str]], whitelist: set[str]) -> list[dict[str, str]]:
    if not whitelist:
        return cites
    out: list[dict[str, str]] = []
    for c in cites:
        host = _domain(c.get("url", ""))
        if _matches_whitelist(host, whitelist):
            out.append(c)
    return out


def pick_citations(
    all_cites: list[dict[str, str]], topic: str | None = None, max_items: int = 2
) -> list[dict[str, str]]:
    rows = all_cites
    if topic:
        rows = [r for r in rows if r.get("topic") == topic] or rows
    return rows[:max_items]
