from __future__ import annotations
from typing import Dict, Any, List, Optional
from pathlib import Path
import csv
import random

def pick_quote(data_dir: Path, topic: Optional[str] = None) -> Dict[str, str]:
    quotes_path = data_dir / "quotes.csv"
    with quotes_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if topic:
        rows = [r for r in rows if r.get("topic") == topic] or rows
    return random.choice(rows) if rows else {}

def pick_stat(data_dir: Path, metric: Optional[str] = None) -> Dict[str, str]:
    stats_path = data_dir / "stats.csv"
    with stats_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if metric:
        rows = [r for r in rows if r.get("metric") == metric] or rows
    return random.choice(rows) if rows else {}
