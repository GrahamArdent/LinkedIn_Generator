from __future__ import annotations
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
import csv, yaml
from urllib.parse import urlparse

def load_citations(data_dir: Path) -> List[Dict[str, str]]:
    path = data_dir / "citations.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def load_whitelist(config_dir: Path) -> Set[str]:
    path = config_dir / "source_whitelist.yaml"
    if not path.exists():
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    doms = data.get("domains", []) or []
    return {str(d).strip().lower().lstrip("www.") for d in doms}

def _domain(url: str) -> str:
    try:
        host = urlparse(url).netloc.lower()
        if not host and url:
            host = url.lower()
        return host.lstrip("www.")
    except Exception:
        return ""

def _matches_whitelist(host: str, whitelist: Set[str]) -> bool:
    if not whitelist:
        return True
    for w in whitelist:
        if host == w or host.endswith("." + w):
            return True
    return False

def filter_to_whitelist(cites: List[Dict[str, str]], whitelist: Set[str]) -> List[Dict[str, str]]:
    if not whitelist:
        return cites
    out: List[Dict[str, str]] = []
    for c in cites:
        host = _domain(c.get("url", ""))
        if _matches_whitelist(host, whitelist):
            out.append(c)
    return out

def pick_citations(all_cites: List[Dict[str, str]], topic: Optional[str] = None, max_items: int = 2) -> List[Dict[str, str]]:
    rows = all_cites
    if topic:
        rows = [r for r in rows if r.get("topic") == topic] or rows
    return rows[:max_items]
