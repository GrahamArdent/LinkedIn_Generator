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
VisualAssetPreference = Literal["auto", "single_image", "carousel"]


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


class CarouselSlide(BaseModel):
    slide_number: int = Field(ge=1, le=8)
    role: Literal["cover", "context", "insight", "proof", "takeaway", "closer"]
    headline: str = Field(min_length=1, max_length=120)
    body: str = Field(default="", max_length=320)
    visual_direction: str = Field(min_length=1, max_length=600)


class SingleImageBrief(BaseModel):
    concept: str = Field(min_length=1, max_length=1000)
    overlay_text: str = Field(default="", max_length=160)
    composition: str = Field(min_length=1, max_length=800)
    style: str = Field(min_length=1, max_length=500)
    generation_prompt: str = Field(min_length=1, max_length=1800)
    negative_guidance: list[str] = Field(default_factory=list, max_length=12)
    alt_text: str = Field(min_length=1, max_length=1000)


class CarouselBrief(BaseModel):
    cover_headline: str = Field(min_length=1, max_length=120)
    design_system: str = Field(min_length=1, max_length=1000)
    slides: list[CarouselSlide] = Field(min_length=4, max_length=8)
    alt_text: str = Field(min_length=1, max_length=1200)


class VisualAssetPlan(BaseModel):
    """Provider-neutral visual companion for one publish-ready text candidate."""

    status: Literal["planned", "deferred"]
    source_candidate: Literal["original", "rewrite"] | None = None
    asset_type: Literal["single_image", "carousel"] | None = None
    rationale: str = Field(default="", max_length=800)
    creative_goal: str = Field(default="", max_length=500)
    aspect_ratio: str = "4:5"
    single_image: SingleImageBrief | None = None
    carousel: CarouselBrief | None = None
    review_required: bool = True
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_asset_shape(self):
        if self.status == "deferred":
            if self.asset_type is not None or self.single_image is not None or self.carousel is not None:
                raise ValueError("deferred visual plans cannot contain a renderable asset")
            return self
        if self.source_candidate is None or self.asset_type is None:
            raise ValueError("planned visual assets require source_candidate and asset_type")
        if self.asset_type == "single_image":
            if self.single_image is None or self.carousel is not None:
                raise ValueError("single_image plan requires only single_image brief")
        if self.asset_type == "carousel":
            if self.carousel is None or self.single_image is not None:
                raise ValueError("carousel plan requires only carousel brief")
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
    publish_quality_gate: bool = True
    publish_quality_threshold: int = Field(default=90, ge=0, le=100)
    visual_asset_plan: bool = True
    visual_asset_preference: VisualAssetPreference = "auto"
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
    status: Literal["drafted", "skipped", "needs_more_evidence"] = "drafted"
    body: str
    hashtags: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    telemetry: dict[str, Any] = Field(default_factory=dict)
    review: dict[str, Any] = Field(default_factory=dict)
    visual_asset: VisualAssetPlan | None = None
