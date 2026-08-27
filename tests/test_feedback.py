from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.app.contracts import LinkedInContentFeedback
from src.app.feedback import correction_signals_from_feedback, voice_example_from_feedback


TEXT = "The useful part is rarely the flashy part. Reliability is what people remember after the demo ends."


def test_keep_is_explicit_user_approval():
    example = voice_example_from_feedback(
        LinkedInContentFeedback(
            feedback_id="feedback-1",
            request_id="request-1",
            decision="keep",
            original_text=TEXT,
        )
    )

    assert example is not None
    assert example.example_id == "feedback-1"
    assert example.provenance == "user_approved"
    assert example.text == TEXT


def test_edit_requires_and_promotes_the_user_edited_text():
    with pytest.raises(ValidationError):
        LinkedInContentFeedback(decision="edit", original_text=TEXT)

    edited = "The useful part is not the flashy demo. It is whether the workflow still works tomorrow morning."
    feedback = LinkedInContentFeedback(
        request_id="request-2",
        decision="edit",
        original_text=TEXT,
        edited_text=edited,
        reason_codes=["too_generic", "weak_specificity"],
    )
    example = voice_example_from_feedback(feedback)

    assert example is not None
    assert example.example_id == "request-2"
    assert example.provenance == "user_edited"
    assert example.text == edited
    assert correction_signals_from_feedback(feedback) == {
        "decision": "edit",
        "reason_codes": ["too_generic", "weak_specificity"],
        "has_user_edit": True,
        "promotes_voice_evidence": True,
    }


def test_reject_never_becomes_positive_voice_evidence_but_keeps_correction_reasons():
    feedback = LinkedInContentFeedback(
        request_id="request-3",
        decision="reject",
        original_text=TEXT,
        reason_codes=["too_internal", "wrong_pov", "sounds_like_ai"],
        note="Does not sound like me.",
    )
    example = voice_example_from_feedback(feedback)

    assert example is None
    assert correction_signals_from_feedback(feedback) == {
        "decision": "reject",
        "reason_codes": ["too_internal", "wrong_pov", "sounds_like_ai"],
        "has_user_edit": False,
        "promotes_voice_evidence": False,
    }


def test_publish_is_authoritative_and_can_capture_final_edited_version():
    final_text = "Attention is easy to win once. Trust is what makes the next conversation possible."
    example = voice_example_from_feedback(
        LinkedInContentFeedback(
            request_id="request-4",
            decision="publish",
            original_text=TEXT,
            edited_text=final_text,
            source_ref="linkedin:post:123",
        )
    )

    assert example is not None
    assert example.provenance == "published"
    assert example.text == final_text
    assert example.source_ref == "linkedin:post:123"


def test_feedback_reason_codes_are_bounded_and_validated():
    with pytest.raises(ValidationError):
        LinkedInContentFeedback(
            decision="reject",
            original_text=TEXT,
            reason_codes=["not_a_real_reason"],
        )

    with pytest.raises(ValidationError):
        LinkedInContentFeedback(
            decision="reject",
            original_text=TEXT,
            reason_codes=["wrong_pov", "wrong_pov"],
        )

    with pytest.raises(ValidationError):
        LinkedInContentFeedback(
            decision="reject",
            original_text=TEXT,
            reason_codes=[
                "too_internal",
                "wrong_pov",
                "too_generic",
                "sounds_like_ai",
                "weak_hook",
                "forced_cta",
            ],
        )


def test_feedback_conversion_does_not_persist_or_mutate_external_state():
    feedback = LinkedInContentFeedback(
        request_id="request-5",
        decision="keep",
        original_text=TEXT,
        reason_codes=["other"],
    )
    snapshot = feedback.model_dump()

    voice_example_from_feedback(feedback)
    correction_signals_from_feedback(feedback)

    assert feedback.model_dump() == snapshot
