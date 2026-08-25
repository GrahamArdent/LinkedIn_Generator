from __future__ import annotations

from typing import Any

from .quality import evaluate_quality


def judge_report(text: str, persona: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    """Return an explainable quality report for deterministic draft selection."""

    return evaluate_quality(text, persona, rules)


def judge_score(text: str, persona: dict[str, Any], rules: dict[str, Any]) -> int:
    return int(judge_report(text, persona, rules)["score"])
