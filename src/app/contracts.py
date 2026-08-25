from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class SourceEvidence(BaseModel):
    """Bounded source material that may ground a LinkedIn draft."""

    title: str = Field(min_length=1)
    fact: str = Field(min_length=1)
    url: str | None = None


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
    services: list[str] = Field(default_factory=list)
    targets: list[str] = Field(default_factory=list)
    evidence: list[SourceEvidence] = Field(default_factory=list)
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
