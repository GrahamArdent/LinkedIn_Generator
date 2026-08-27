from __future__ import annotations

import json

from src.app.api import run_generation
from src.app.publish_quality import WEIGHTS, assess_publish_quality


ORIGINAL = (
    "I built a planning system to reduce repeated work.\n\n"
    "It looked careful, but one part kept reopening decisions I had already settled. "
    "That made the process feel safer while quietly creating more work.\n\n"
    "The useful lesson was simple: another check only helps when it reduces a real uncertainty. "
    "Otherwise the system is not protecting the work. It is repeating it."
)

REWRITE = (
    "I built a planning system to reduce repeated work.\n\n"
    "Then I caught one part reopening decisions I had already settled. It looked careful, but the result was more work, not less.\n\n"
    "That changed the rule for me. A check earns its place when it reduces a real uncertainty. "
    "If nothing changed, reopening a good decision is not extra intelligence. It is rework."
)


def quality_json(score: int) -> str:
    # These fixtures are chosen so the repository's deterministic weighting
    # produces the requested scores exactly.
    if score == 87:
        dims = {
            "outsider_clarity": 5,
            "professional_relevance": 4,
            "specificity": 5,
            "novel_insight": 4,
            "practical_usefulness": 4,
            "emotional_tension": 4,
            "conversation_potential": 4,
            "shareability": 4,
            "voice_authenticity": 5,
        }
    elif score == 92:
        dims = {
            "outsider_clarity": 5,
            "professional_relevance": 5,
            "specificity": 5,
            "novel_insight": 5,
            "practical_usefulness": 4,
            "emotional_tension": 4,
            "conversation_potential": 4,
            "shareability": 4,
            "voice_authenticity": 4,
        }
    elif score == 93:
        dims = {
            "outsider_clarity": 5,
            "professional_relevance": 5,
            "specificity": 5,
            "novel_insight": 5,
            "practical_usefulness": 4,
            "emotional_tension": 4,
            "conversation_potential": 4,
            "shareability": 4,
            "voice_authenticity": 5,
        }
    else:
        raise AssertionError(f"unsupported fixture score: {score}")
    return json.dumps({**dims, "gaps": ["Make the consequence more immediate."], "rationale": "Fixture."})


class ReviewClient:
    def __init__(self, *, first_score: int, rewrite: str = REWRITE, second_score: int | None = None):
        self.first_score = first_score
        self.rewrite = rewrite
        self.second_score = second_score
        self.calls: list[dict[str, str]] = []
        self.quality_calls = 0

    def call(self, system: str, user: str, response_json: bool = True):
        self.calls.append({"system": system, "user": user})
        if "strict LinkedIn publish-quality evaluator" in system:
            self.quality_calls += 1
            score = self.first_score if self.quality_calls == 1 else self.second_score
            assert score is not None
            return {"text": quality_json(score)}
        if "one bounded publish-quality rewrite" in system:
            return {"text": self.rewrite}
        return {"text": ORIGINAL}


def _run(client: ReviewClient):
    return run_generation(
        topic="When AI planning creates repeated work",
        services=[],
        persona_key="graham",
        audience="AI builders and operators",
        objective="share a useful lesson from real work",
        author_pov="individual",
        content_goal="authority",
        opportunity_gate=False,
        publish_quality_gate=True,
        publish_quality_threshold=90,
        allowed_sources=[
            {
                "title": "Build evidence",
                "fact": "One planning step reopened decisions that had already been settled.",
            }
        ],
        hashtags=[],
        llm_client=client,
    )


def test_publish_quality_weights_total_100():
    assert sum(WEIGHTS.values()) == 100


def test_sub_90_draft_is_preserved_and_one_rewrite_is_scored():
    client = ReviewClient(first_score=87, second_score=93)

    result = _run(client)

    assert result["body"] == ORIGINAL
    review = result["review"]
    assert review["threshold"] == 90
    assert review["original"]["score"] == 87
    assert review["original"]["body"] == ORIGINAL
    assert review["rewrite_triggered"] is True
    assert review["rewrite"]["body"] == REWRITE
    assert review["rewrite"]["score"] == 93
    assert review["rewrite"]["guard_accepted"] is True
    assert review["recommendation"] == "rewrite"
    assert review["publish_ready"] is True
    assert client.quality_calls == 2
    assert len([c for c in client.calls if "one bounded publish-quality rewrite" in c["system"]]) == 1


def test_90_plus_draft_does_not_spend_a_rewrite_call():
    client = ReviewClient(first_score=92)

    result = _run(client)

    review = result["review"]
    assert review["original"]["score"] == 92
    assert review["rewrite_triggered"] is False
    assert review["rewrite"] is None
    assert review["recommendation"] == "original"
    assert review["publish_ready"] is True
    assert client.quality_calls == 1
    assert not any("one bounded publish-quality rewrite" in c["system"] for c in client.calls)


def test_unsafe_rewrite_is_kept_for_audit_but_cannot_replace_original():
    unsafe = REWRITE + "\n\nThis improves results by 42%."
    client = ReviewClient(first_score=87, rewrite=unsafe)

    result = _run(client)

    review = result["review"]
    assert result["body"] == ORIGINAL
    assert review["rewrite_triggered"] is True
    assert review["rewrite"]["body"] == unsafe
    assert review["rewrite"]["guard_accepted"] is False
    assert "rewrite introduces a new number" in review["rewrite"]["guard_reasons"]
    assert review["rewrite"]["score"] is None
    assert review["recommendation"] == "original"
    assert review["publish_ready"] is False
    assert client.quality_calls == 1


def test_publish_quality_assessment_unavailable_never_falls_back_to_compliance_100():
    class BrokenClient:
        def call(self, *_args, **_kwargs):
            raise RuntimeError("unavailable")

    assessment = assess_publish_quality(
        text=ORIGINAL,
        audience="AI builders",
        content_goal="authority",
        evidence=[],
        persona_profile={},
        client=BrokenClient(),
    )

    assert assessment.score is None
    assert assessment.warnings == ("publish_quality_unavailable:RuntimeError",)
