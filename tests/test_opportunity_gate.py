from __future__ import annotations

import json

from src.app.api import run_generation
from src.app.opportunity import assess_opportunity


class SequenceClient:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def call(self, system, user, response_json=True):
        self.calls.append({"system": system, "user": user, "response_json": response_json})
        text = self.outputs.pop(0)
        return {"text": text}


def payload(**overrides):
    base = {
        "outsider_clarity": 4,
        "professional_relevance": 4,
        "specificity": 4,
        "novel_insight": 4,
        "practical_usefulness": 4,
        "emotional_tension": 3,
        "conversation_potential": 3,
        "shareability": 4,
        "voice_fit": 4,
        "reason": "The topic contains a concrete lesson that travels beyond the source project.",
    }
    base.update(overrides)
    return json.dumps(base)


def test_weighted_opportunity_score_is_computed_in_code():
    client = SequenceClient([payload()])
    assessment = assess_opportunity(
        topic="A concrete lesson from AI workflow design",
        audience="AI builders",
        objective="share a useful professional lesson",
        evidence=[{"title": "Build note", "fact": "A repeated planning step reopened settled decisions."}],
        client=client,
        minimum_score=60,
    )

    assert assessment.score == 76
    assert assessment.decision == "draft"
    assert assessment.goal == "reach"
    assert assessment.earned_question is False
    assert len(client.calls) == 1


def test_auto_conversation_goal_only_earns_question_with_real_conversation_signal():
    client = SequenceClient([
        payload(
            outsider_clarity=4,
            specificity=4,
            conversation_potential=5,
            emotional_tension=4,
            novel_insight=3,
        )
    ])
    assessment = assess_opportunity(
        topic="When do safeguards become bureaucracy?",
        audience="AI builders and operators",
        objective="start a useful professional discussion",
        evidence=[{"title": "Build note", "fact": "Repeated checks created unnecessary rework."}],
        client=client,
    )

    assert assessment.decision == "draft"
    assert assessment.goal == "conversation"
    assert assessment.earned_question is True


def test_explicit_authority_goal_overrides_auto_conversation_goal():
    client = SequenceClient([payload(conversation_potential=5, emotional_tension=5)])
    assessment = assess_opportunity(
        topic="A lesson from AI workflow design",
        audience="AI builders",
        objective="demonstrate useful expertise",
        evidence=[{"title": "Build note", "fact": "The system reopened settled decisions."}],
        client=client,
        requested_goal="authority",
    )

    assert assessment.goal == "authority"
    assert assessment.earned_question is False


def test_weak_opportunity_skips_before_full_draft_call():
    gate_client = SequenceClient([
        payload(
            outsider_clarity=1,
            professional_relevance=1,
            specificity=1,
            novel_insight=1,
            practical_usefulness=1,
            emotional_tension=1,
            conversation_potential=1,
            shareability=1,
            voice_fit=2,
            reason="The subject is too internal and too thin for an outsider-facing post.",
        )
    ])
    draft_client = SequenceClient([
        "This output must never be consumed because the opportunity should be skipped before drafting."
    ])

    result = run_generation(
        topic="Internal housekeeping update",
        services=[],
        persona_key="graham",
        audience="professional network",
        objective="share useful professional insight",
        author_pov="individual",
        content_goal="auto",
        opportunity_gate=True,
        allowed_sources=[{"title": "Internal note", "fact": "A file name changed."}],
        hashtags=[],
        llm_client=draft_client,
        opportunity_client=gate_client,
    )

    assert result["status"] == "skipped"
    assert result["body"] == ""
    assert result["telemetry"]["opportunity_decision"] == "skip"
    assert len(gate_client.calls) == 1
    assert len(draft_client.calls) == 0


def test_strong_opportunity_runs_one_preflight_and_one_clean_full_draft():
    gate_client = SequenceClient([payload()])
    clean_draft = (
        "AI can save time, but it can also automate unnecessary work.\n\n"
        "I saw that happen when a planning step reopened decisions I had already made. "
        "The process looked careful, yet it created rework instead of reducing it.\n\n"
        "That changed the question for me: good automation is not about doing more checks. "
        "It is about knowing which decisions still need attention and which ones should stay settled."
    )
    draft_client = SequenceClient([clean_draft])

    result = run_generation(
        topic="What unnecessary rework taught me about AI automation",
        services=[],
        persona_key="graham",
        audience="AI builders and operators",
        objective="share a useful professional lesson",
        author_pov="individual",
        content_goal="authority",
        opportunity_gate=True,
        allowed_sources=[
            {
                "title": "Build note",
                "fact": "A planning step reopened decisions that had already been settled.",
            }
        ],
        hashtags=[],
        llm_client=draft_client,
        opportunity_client=gate_client,
    )

    assert result["status"] == "drafted"
    assert result["telemetry"]["opportunity_decision"] == "draft"
    assert result["telemetry"]["content_goal"] == "authority"
    assert len(gate_client.calls) == 1
    assert len(draft_client.calls) == 1
    assert "Content Goal: authority" in draft_client.calls[0]["user"]
    assert "Ending Guidance:" in draft_client.calls[0]["user"]


def test_malformed_preflight_fails_open_with_visible_warning():
    client = SequenceClient(["not json"])
    assessment = assess_opportunity(
        topic="A potentially useful professional lesson",
        audience="professional network",
        objective="share useful insight",
        evidence=[],
        client=client,
    )

    assert assessment.decision == "draft"
    assert assessment.goal == "authority"
    assert assessment.earned_question is False
    assert assessment.warnings
    assert assessment.warnings[0].startswith("preflight_unavailable:")
