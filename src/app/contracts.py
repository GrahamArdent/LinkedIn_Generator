from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


FeedbackReason = Literal[
    "too_internal",
    "wrong_pov",
    "too_generic",
    "too_long",
    "too_short",
    "sounds_like_ai",
    "not_my_voice",
    "weak_hook",
    "forced_cta",
    "unclear_point",
    "weak_specificity",
    "too_salesy",
    "unsupported_claim",
    "wrong_tone",
    "other",
]
ContentGoal = Literal["auto", "reach", "conversation", "authority"]


class SourceEvidence(BaseModel):
    """Bounded source material that may ground a LinkedIn draft."""

    title: str = Field(min_length=1)
    fact: str = Field(min_length=1)
    url: str | None = None


class VoiceExample(BaseModel):
    """Human-authoritative writing evidence used only as a voice reference.

    Generated drafts are intentionally not an accepted provenance. A generated
    draft may become voice evidence only after an explicit user approval/edit
    or after the user chooses to publish it.
    """

    example_id: str | None = None
    provenance: Literal["published", "user_approved", "user_edited"]
    text: str = Field(min_length=20, max_length=3500)
    source_ref: str | None = None


class LinkedInContentFeedback(BaseModel):
    """Explicit human review of one LinkedIn draft/result.

    Feedback is a domain event, not persistence. Dedication or another caller
    may store it, but only explicit approval-bearing decisions may be promoted
    to positive voice evidence. Reason codes preserve why the user changed or
    rejected a draft without requiring a long free-text explanation.
    """

    feedback_id: str | None = None
    request_id: str | None = None
    decision: Literal["keep", "edit", "reject", "publish"]
    original_text: str = Field(min_length=1, max_length=3500)
    edited_text: str | None = Field(default=None, max_length=3500)
    source_ref: str | None = None
    reason_codes: list[FeedbackReason] = Field(default_factory=list, max_length=5)
    note: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_decision_payload(self):
        edited = (self.edited_text or "").strip()
        if self.decision == "edit" and not edited:
            raise ValueError("edited_text is required when decision='edit'")
        if self.edited_text is not None and not edited:
            raise ValueError("edited_text cannot be blank when supplied")
        if len(self.reason_codes) != len(set(self.reason_codes)):
            raise ValueError("reason_codes must not contain duplicates")
        return self


class LinkedInContentRequest(BaseModel):
    """Scheduler-independent request contract for LinkedIn content generation.

    Dedication may create these requests, but Dedication remains the owner of
    orchestration, Action selection, scheduling, permissions, and canonical
    state. This contract carries only LinkedIn-domain generation inputs.
    """

    request_id: str | None = None
    origin: Literal["dedication", "manual", "test"] = "dedication"
    topic: str = Field(min_length=1)
    persona_key: str = Field(default="graham", min_length=1)
    audience: str = Field(default="professional network", min_length=1)
    objective: str = Field(
        default="turn real professional activity into useful LinkedIn visibility",
        min_length=1,
    )
    author_pov: Literal["individual", "team", "company"] = "individual"
    content_goal: ContentGoal = "auto"
    opportunity_gate: bool = True
    services: list[str] = Field(default_factory=list)
    targets: list[str] = Field(default_factory=list)
    evidence: list[SourceEvidence] = Field(default_factory=list)
    voice_examples: list[VoiceExample] = Field(default_factory=list, max_length=3)
    hashtags: list[str] = Field(default_factory=list)


class LinkedInContentResult(BaseModel):
    """Structured result returned to an orchestrator such as Dedication."""

    request_id: str | None = None
    origin: Literal["dedication", "manual", "test"]
    persona_key: str
    status: Literal["drafted", "skipped"] = "drafted"
    body: str
    hashtags: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    telemetry: dict[str, Any] = Field(default_factory=dict)
