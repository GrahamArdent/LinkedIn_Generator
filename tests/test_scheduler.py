from datetime import date
from pathlib import Path

from src.app.scheduler import load_schedule, resolve_persona_for_date


def test_schedule_resolution(tmp_path: Path):
    content = """
monday: graham_thought_leadership
tuesday: ardent_sales
"""
    f = tmp_path / "schedule.yaml"
    f.write_text(content, encoding="utf-8")
    sched = load_schedule(f)
    assert (
        resolve_persona_for_date(sched, date(2025, 10, 6)) == "graham_thought_leadership"
    )  # Monday
