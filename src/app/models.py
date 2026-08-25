from __future__ import annotations

from pydantic import BaseModel, Field


class Telemetry(BaseModel):
    emoji_count: int = 0
    bullet_char: str = "🔹"
    persona: str = "ardent_v2"
    score: int | None = None
    voice_reference_count: int = 0
    voice_reference_ids: list[str] = Field(default_factory=list)


class PostJSON(BaseModel):
    hook: str = ""
    exec_pov: str = ""
    proof_point: str = ""
    micro_plays: list[str] = Field(default_factory=list)
    quote: str = ""
    cta: str = ""
    hashtags: list[str] = Field(default_factory=list)
    body: str = ""
    sources: list[str] = Field(default_factory=list)
    telemetry: Telemetry = Field(default_factory=Telemetry)
