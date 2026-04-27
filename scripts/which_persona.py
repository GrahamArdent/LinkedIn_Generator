from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "schedule.yaml"


def load_schedule(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_persona_for_date(schedule, d: date):
    dow = d.strftime("%A")
    return schedule.get("days", {}).get(dow)


def main():
    # If a date is provided, use it; otherwise default to TODAY.
    d = date.today()
    if len(sys.argv) == 2:
        d = date.fromisoformat(sys.argv[1])
    elif len(sys.argv) > 2:
        print("Usage: python scripts/which_persona.py [YYYY-MM-DD]")
        sys.exit(1)

    sched = load_schedule(CONFIG)
    who = resolve_persona_for_date(sched, d)
    print(who or "none")


if __name__ == "__main__":
    main()
