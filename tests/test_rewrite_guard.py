from __future__ import annotations

import pytest

from src.app.generation import Pipeline
from src.app.rewrite_guard import evaluate_rewrite

PERSONA = {
    "tone": ["direct", "humble"],
    "rhythm": ["tight", "punchy"],
    "devices": ["question", "contrast"],
    "donts": ["clichés", "em_dashes"],
    "emoji_max": 3,
}

RULES = {
    "emoji_max": 3,
    "allow_em_dash": False,
    "forbidden_phrases": ["how exposed are you"],
    "bullet_char": "🔹",
    "append_sources_block": False,
    "hashtag_min": 0,
    "hashtag_max": 5,
}

ORIGINAL = """What mattered in the buyer conversation?

Reliability mattered more than novelty.

That contrast changes what I would build next."""

SAFE_REWRITE = """What mattered most in the buyer conversation?

Not novelty. Reliability mattered more.

That contrast changes what I would build next."""


@pytest.mark.parametrize(
    ("candidate", "reason"),
    [
        (SAFE_REWRITE + "\n\nRead https://example.com", "rewrite introduces a new URL"),
        (SAFE_REWRITE + "\n\nIt improved outcomes by 42%.", "rewrite introduces a new number"),
        (SAFE_REWRITE + '\n\n"This changes everything."', "rewrite introduces a new quoted claim"),
        (SAFE_REWRITE + "\n\nHow exposed are you?", "rewrite introduces a repository-forbidden CTA phrase"),
    ],
)
def test_rewrite_guard_rejects_new_claim_vectors(candidate, reason):
    report = evaluate_rewrite(ORIGINAL, candidate, PERSONA, RULES)

    assert report["accepted"] is False
    assert reason in report["reasons"]


def test_rewrite_guard_accepts_safe_equal_or_better_rephrase():
    report = evaluate_rewrite(ORIGINAL, SAFE_REWRITE, PERSONA, RULES)

    assert report["accepted"] is True
    assert report["reasons"] == []
    assert report["candidate_report"]["score"] >= report["original_report"]["score"]


def test_rewrite_guard_rejects_quality_regression():
    worse = "Reliability mattered more than novelty, but this sentence keeps going " + "word " * 80
    report = evaluate_rewrite(ORIGINAL, worse, PERSONA, RULES)

    assert report["accepted"] is False
    assert "rewrite lowers deterministic quality score" in report["reasons"]


class OneShotClient:
    def __init__(self, candidate: str):
        self.candidate = candidate
        self.calls = []

    def call(self, system: str, user: str, response_json: bool = True):
        self.calls.append({"system": system, "user": user, "response_json": response_json})
        return {"text": self.candidate}


def _pipeline(candidate: str) -> Pipeline:
    return Pipeline({"prompt_kit": RULES}, client=OneShotClient(candidate))


def test_critic_falls_back_to_original_when_candidate_is_unsafe():
    pipe = _pipeline(SAFE_REWRITE + "\n\nThe result improved by 73%.")
    pipe.last_judge_report = {"score": 89, "issues": ["repairable"], "signals": {}}
    prompt = {
        "system": "Edit conservatively for {persona_profile}.",
        "user_template": "Persona: {persona_profile}\nPost: {post}",
    }

    result = pipe.critic(prompt, ORIGINAL, PERSONA)

    assert result == ORIGINAL
    assert pipe.rewrite_reports[-1]["stage"] == "critic"
    assert pipe.rewrite_reports[-1]["skipped"] is False
    assert pipe.rewrite_reports[-1]["accepted"] is False


def test_humanize_accepts_safe_rewrite_and_updates_quality_report():
    pipe = _pipeline(SAFE_REWRITE)
    pipe.last_judge_report = {"score": 80, "issues": ["repairable"], "signals": {}}
    prompt = {
        "system": "Improve rhythm for {persona_profile}.",
        "user_template": "Persona: {persona_profile}\nPost: {post}",
    }

    result = pipe.humanize(prompt, ORIGINAL, PERSONA)

    assert result == SAFE_REWRITE
    assert pipe.rewrite_reports[-1]["stage"] == "humanize"
    assert pipe.rewrite_reports[-1]["skipped"] is False
    assert pipe.rewrite_reports[-1]["accepted"] is True
    assert pipe.last_judge_report == pipe.rewrite_reports[-1]["candidate_report"]

    client = pipe.client
    assert "direct" in client.calls[0]["system"]
    assert ORIGINAL in client.calls[0]["user"]


def test_rewrite_stage_skips_provider_when_judge_has_no_concrete_issue():
    pipe = _pipeline("this candidate should never be requested")
    pipe.last_judge_report = {"score": 100, "issues": [], "signals": {}}
    prompt = {"system": "unused", "user_template": "{post}"}

    result = pipe.critic(prompt, ORIGINAL, PERSONA)

    assert result == ORIGINAL
    assert pipe.client.calls == []
    assert pipe.rewrite_reports[-1]["stage"] == "critic"
    assert pipe.rewrite_reports[-1]["skipped"] is True
    assert pipe.rewrite_reports[-1]["accepted"] is False
