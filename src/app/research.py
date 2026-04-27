from __future__ import annotations

import csv
import random
from pathlib import Path


def pick_quote(data_dir: Path, topic: str | None = None) -> dict[str, str]:
    quotes_path = data_dir / "quotes.csv"
    with quotes_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if topic:
        rows = [r for r in rows if r.get("topic") == topic] or rows
    return random.choice(rows) if rows else {}


def pick_stat(data_dir: Path, metric: str | None = None) -> dict[str, str]:
    stats_path = data_dir / "stats.csv"
    with stats_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if metric:
        rows = [r for r in rows if r.get("metric") == metric] or rows
    return random.choice(rows) if rows else {}
