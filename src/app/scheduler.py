from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import yaml

_CANON = {
    "monday": "monday",
    "mon": "monday",
    "tuesday": "tuesday",
    "tue": "tuesday",
    "tues": "tuesday",
    "wednesday": "wednesday",
    "wed": "wednesday",
    "thursday": "thursday",
    "thu": "thursday",
    "thur": "thursday",
    "thurs": "thursday",
    "friday": "friday",
    "fri": "friday",
    "saturday": "saturday",
    "sat": "saturday",
    "sunday": "sunday",
    "sun": "sunday",
}
_DAY_NAMES = frozenset(_CANON.values())


def _canonize_day_key(k: str) -> str:
    return _CANON.get(str(k).strip().lower(), str(k).strip().lower())


def load_schedule(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"days": {}}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    # normalize both nested `days:` schedules and legacy top-level weekday keys
    days = data.get("days", {}) or {}
    legacy_days = {
        _canonize_day_key(k): v
        for k, v in data.items()
        if _canonize_day_key(k) in _DAY_NAMES and v is not None
    }
    norm: dict[str, str] = {}
    norm.update(legacy_days)
    for k, v in days.items():
        norm[_canonize_day_key(k)] = v
    data["days"] = norm
    # normalize skip_dates to ISO strings
    skips = data.get("skip_dates", []) or []
    data["skip_dates"] = [str(s).strip() for s in skips]
    data["pause"] = bool(data.get("pause", False))
    return data


def resolve_persona_for_date(schedule: dict[str, Any], d: date) -> str | None:
    """Return persona key for the given date, honoring pause/skip_dates."""
    if schedule.get("pause"):
        return None
    if d.isoformat() in schedule.get("skip_dates", []):
        return None
    dow = d.strftime("%A").lower()  # e.g., "tuesday"
    return schedule.get("days", {}).get(dow)
