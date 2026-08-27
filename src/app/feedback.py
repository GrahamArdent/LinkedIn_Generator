from __future__ import annotations

from typing import Any

from .contracts import LinkedInContentFeedback, VoiceExample


_PROMOTABLE_PROVENANCE = {
    "keep": "user_approved",
    "edit": "user_edited",
    "publish": "published",
}


def voice_example_from_feedback(feedback: LinkedInContentFeedback) -> VoiceExample | None:
    """Convert explicit human review into reusable positive voice evidence.

    Rejected drafts never become positive examples. Generated text is therefore
    not self-promoted: a keep/edit/publish decision is the human-authority gate.
    This helper performs no persistence and no Dedication state mutation.
    """

    provenance = _PROMOTABLE_PROVENANCE.get(feedback.decision)
    if provenance is None:
        return None

    if feedback.decision in {"edit", "publish"} and feedback.edited_text:
        text = feedback.edited_text.strip()
    else:
        text = feedback.original_text.strip()

    example_id = feedback.feedback_id or feedback.request_id
    return VoiceExample(
        example_id=example_id,
        provenance=provenance,
        text=text,
        source_ref=feedback.source_ref,
    )


def correction_signals_from_feedback(feedback: LinkedInContentFeedback) -> dict[str, Any]:
    """Return compact learning signals without persisting or inferring intent.

    These signals let an orchestrator aggregate correction patterns such as
    `too_internal` or `wrong_pov` separately from positive voice examples.
    They deliberately preserve only explicit human input.
    """

    return {
        "decision": feedback.decision,
        "reason_codes": list(feedback.reason_codes),
        "has_user_edit": bool((feedback.edited_text or "").strip()),
        "promotes_voice_evidence": feedback.decision in _PROMOTABLE_PROVENANCE,
    }
