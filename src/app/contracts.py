from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


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
    to positive voice evidence.
    """

    feedback_id: str | None = None
    request_id: str | None = None
    decision: Literal["keep", "edit", "reject", "publish"]
    original_text: str = Field(min_length=1, max_length=3500)
    edited_text: str | None = Field(default=None, max_length=3500)
    source_ref: str | None = None
    note: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def validate_decision_payload(self):
        edited = (self.edited_text or "").strip()
        if self.decision == "edit" and not edited:
            raise ValueError("edited_text is required when decision='edit'")
        if self.edited_text is not None and not edited:
            raise ValueError("edited_text cannot be blank when supplied")
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
    body: str
    hashtags: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    telemetry: dict[str, Any] = Field(default_factory=dict)
