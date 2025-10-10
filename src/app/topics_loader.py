from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Optional
import csv
import datetime as dt

# -------- Robust CSV loader --------
def _open_csv(path: Path) -> csv.DictReader:
    """
    Open CSV tolerantly:
    - Handles UTF-8 BOM
    - Sniffs delimiter (comma/semicolon/tab)
    """
    data = Path(path).read_text(encoding="utf-8-sig")
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(data[:2048])
    except csv.Error:
        dialect = csv.excel
    return csv.DictReader(data.splitlines(), dialect=dialect)

def _normalize_headers(row: Dict[str, Any]) -> Dict[str, str]:
    return {
        (k or "").strip().lower().replace(" ", "_"): (v or "").strip()
        for k, v in row.items()
    }

def _extract_topic(norm: Dict[str, str]) -> Optional[str]:
    # Accept several common header names
    for key in ("topic", "title", "post_topic", "theme", "subject", "hook"):
        val = norm.get(key)
        if val:
            return val
    return None

def load_topics(path: Optional[Path]) -> List[Dict[str, Any]]:
    """
    Returns a list of rows like:
      {"topic": "<string>", "raw": {all_normalized_columns}}
    If path is None or missing, returns [].
    """
    if not path or not Path(path).exists():
        return []

    items: List[Dict[str, Any]] = []
    try:
        reader = _open_csv(Path(path))
        for row in reader:
            norm = _normalize_headers(row)
            topic = _extract_topic(norm)
            if topic:
                items.append({"topic": topic, "raw": norm})
    except Exception:
        # Fail-safe: no topics if parsing fails
        return []
    return items

# -------- Selection helper used by API --------
def _parse_date(s: str) -> Optional[dt.date]:
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None

def select_topic_for(
    target_date: dt.date,
    persona: str,
    topics_graham: List[Dict[str, Any]],
    topics_ardent: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Pick a topic either from Graham or Ardent lists by date if available,
    otherwise just return the first available topic for that persona.
    """
    pool = topics_graham if persona == "graham" else topics_ardent
    if not pool:
        return None

    best: Optional[Dict[str, Any]] = None
    for item in pool:
        raw = item.get("raw", {})
        # Accept several possible date headers
        d = _parse_date(
            raw.get("date")
            or raw.get("post_date")
            or raw.get("schedule_date")
            or raw.get("planned_date")
            or ""
        )
        if d == target_date:
            return item
        if best is None:
            best = item
    return best
