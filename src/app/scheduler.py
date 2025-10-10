
from __future__ import annotations
from pathlib import Path
from datetime import date
from typing import Dict, Any
import yaml

_CANON = {
    "monday": "monday", "mon": "monday",
    "tuesday": "tuesday", "tue": "tuesday", "tues": "tuesday",
    "wednesday": "wednesday", "wed": "wednesday",
    "thursday": "thursday", "thu": "thursday", "thur": "thursday", "thurs": "thursday",
    "friday": "friday", "fri": "friday",
    "saturday": "saturday", "sat": "saturday",
    "sunday": "sunday", "sun": "sunday",
}

def _canonize_day_key(k: str) -> str:
    return _CANON.get(str(k).strip().lower(), str(k).strip().lower())

def load_schedule(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"days": {}}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    # normalize days map
    days = data.get("days", {}) or {}
    norm: Dict[str, str] = {}
    for k, v in days.items():
        norm[_canonize_day_key(k)] = v
    data["days"] = norm
    # normalize skip_dates to ISO strings
    skips = data.get("skip_dates", []) or []
    data["skip_dates"] = [str(s).strip() for s in skips]
    data["pause"] = bool(data.get("pause", False))
    return data

def resolve_persona_for_date(schedule: Dict[str, Any], d: date) -> str | None:
    """Return persona key for the given date, honoring pause/skip_dates."""
    if schedule.get("pause"):
        return None
    if d.isoformat() in schedule.get("skip_dates", []):
        return None
    dow = d.strftime("%A").lower()  # e.g., "tuesday"
    return schedule.get("days", {}).get(dow)
