from __future__ import annotations

import csv
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

LOG_HEADERS = [
    "date",
    "persona",
    "post_type",
    "words",
    "hashtags",
    "source_domains",
    "md_path",
    "meta_path",
]


def _word_count(text: str) -> int:
    import re

    return len(re.findall(r"\b\w+\b", text))


def _domains(citations: list[dict[str, str]]) -> str:
    doms = []
    for c in citations or []:
        u = (c.get("url") or "").strip()
        if not u:
            continue
        host = urlparse(u).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        if host:
            doms.append(host)
    # unique, stable order
    seen = set()
    out = []
    for d in doms:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return ";".join(out)


def append_log(out_dir: Path, info: dict[str, Any]) -> Path:
    """
    info needs: date, persona, post_type, body, hashtags(list), citations(list), paths(dict)
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "log.csv"
    row = {
        "date": info.get("date"),
        "persona": info.get("persona"),
        "post_type": info.get("post_type"),
        "words": _word_count(info.get("body") or ""),
        "hashtags": len(info.get("hashtags") or []),
        "source_domains": _domains(info.get("citations") or []),
        "md_path": str(info.get("paths", {}).get("md", "")),
        "meta_path": str(info.get("paths", {}).get("meta", "")),
    }
    write_header = not log_path.exists()
    with log_path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LOG_HEADERS)
        if write_header:
            w.writeheader()
        w.writerow(row)
    return log_path
