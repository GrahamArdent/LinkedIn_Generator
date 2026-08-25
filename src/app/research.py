from __future__ import annotations

import csv
from pathlib import Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _exact_match(rows: list[dict[str, str]], field: str, value: str | None) -> list[dict[str, str]]:
    if value is None:
        return rows
    wanted = value.strip().casefold()
    return [row for row in rows if str(row.get(field, "")).strip().casefold() == wanted]


def pick_quote(data_dir: Path, topic: str | None = None) -> dict[str, str]:
    """Return repository-backed quote evidence only.

    Missing files or a requested topic with no exact match return no evidence.
    We deliberately do not substitute an unrelated quote.
    """

    rows = _exact_match(_read_rows(data_dir / "quotes.csv"), "topic", topic)
    return rows[0] if rows else {}


def pick_stat(data_dir: Path, metric: str | None = None) -> dict[str, str]:
    """Return repository-backed statistic evidence only.

    Missing files or a requested metric with no exact match return no evidence.
    We deliberately do not substitute an unrelated statistic.
    """

    rows = _exact_match(_read_rows(data_dir / "stats.csv"), "metric", metric)
    return rows[0] if rows else {}
