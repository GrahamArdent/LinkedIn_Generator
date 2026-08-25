from __future__ import annotations

import re
from typing import Any

from .judge import judge_report

URL_RE = re.compile(r"https?://\S+")
NUMBER_RE = re.compile(r"(?<!\w)\d[\d,.]*%?(?!\w)")
QUOTE_RE = re.compile(r"[\"“]([^\"”]{2,})[\"”]")


def _normalized_matches(pattern: re.Pattern[str], text: str) -> set[str]:
    return {match.strip().lower() for match in pattern.findall(text)}


def evaluate_rewrite(
    original: str,
    candidate: str,
    persona: dict[str, Any],
    rules: dict[str, Any],
) -> dict[str, Any]:
    """Decide whether a model rewrite is safe enough to replace the original.

    The guard is intentionally conservative. It blocks common hallucination
    vectors that a critic/humanizer must not introduce and rejects rewrites
    that reduce the deterministic repository quality score.
    """

    original_report = judge_report(original, persona, rules)
    candidate_report = judge_report(candidate, persona, rules)
    reasons: list[str] = []

    if not candidate.strip():
        reasons.append("rewrite is empty")

    original_urls = _normalized_matches(URL_RE, original)
    candidate_urls = _normalized_matches(URL_RE, candidate)
    new_urls = sorted(candidate_urls - original_urls)
    if new_urls:
        reasons.append("rewrite introduces a new URL")

    original_numbers = _normalized_matches(NUMBER_RE, original)
    candidate_numbers = _normalized_matches(NUMBER_RE, candidate)
    new_numbers = sorted(candidate_numbers - original_numbers)
    if new_numbers:
        reasons.append("rewrite introduces a new number")

    original_quotes = _normalized_matches(QUOTE_RE, original)
    candidate_quotes = _normalized_matches(QUOTE_RE, candidate)
    new_quotes = sorted(candidate_quotes - original_quotes)
    if new_quotes:
        reasons.append("rewrite introduces a new quoted claim")

    forbidden_phrases = [
        str(item).strip().lower()
        for item in rules.get("forbidden_phrases", [])
        if str(item).strip()
    ]
    introduced_forbidden = [
        phrase
        for phrase in forbidden_phrases
        if phrase in candidate.lower() and phrase not in original.lower()
    ]
    if introduced_forbidden:
        reasons.append("rewrite introduces a repository-forbidden CTA phrase")

    if int(candidate_report["score"]) < int(original_report["score"]):
        reasons.append("rewrite lowers deterministic quality score")

    return {
        "accepted": not reasons,
        "reasons": reasons,
        "original_report": original_report,
        "candidate_report": candidate_report,
        "new_urls": new_urls,
        "new_numbers": new_numbers,
        "new_quotes": new_quotes,
        "introduced_forbidden_phrases": introduced_forbidden,
    }
