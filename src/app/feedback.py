from __future__ import annotations

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
