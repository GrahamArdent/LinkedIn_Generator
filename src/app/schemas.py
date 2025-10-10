from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import List

class PostJSON(BaseModel):
    hook: str
    exec_pov: str = Field(alias="pov")
    proof_point: str
    micro_plays: List[str]
    quote: str
    cta: str
    hashtags: List[str]

    @validator("micro_plays")
    def three_items(cls, v):
        if len(v) != 3:
            raise ValueError("micro_plays must have exactly 3 items")
        return v

    @validator("hashtags")
    def three_to_five(cls, v):
        if not (3 <= len(v) <= 5):
            raise ValueError("hashtags must be 3–5")
        return v
