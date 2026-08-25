from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from src.app.contracts import LinkedInContentRequest, VoiceExample
from src.app.generation import Pipeline


CONFIG = Path(__file__).resolve().parents[1] / "config"


class CapturingClient:
    def __init__(self):
        self.calls = []

    def call(self, system, user, response_json=True):
        self.calls.append({"system": system, "user": user, "response_json": response_json})
        return {"text": "draft"}


def _pipeline():
    pipe = Pipeline(
        {
            "prompt_kit": {
                "bullet_char": "🔹",
                "emoji_max": 3,
                "allow_em_dash": False,
                "append_sources_block": False,
                "hashtag_min": 0,
                "hashtag_max": 5,
                "forbidden_phrases": [],
            }
        },
        client=CapturingClient(),
    )
    pipe.n_variants = 1
    return pipe


def test_generated_draft_cannot_be_voice_evidence_without_human_authority():
    with pytest.raises(ValidationError):
        VoiceExample(
            provenance="generated",
            text="This draft was generated but never explicitly approved by the user.",
        )


def test_request_caps_voice_examples_to_bounded_prompt_context():
    examples = [
        VoiceExample(
            example_id=f"e-{i}",
            provenance="user_approved",
            text=f"Approved writing example number {i} with enough text to satisfy validation.",
        )
        for i in range(6)
    ]
    with pytest.raises(ValidationError):
        LinkedInContentRequest(topic="voice test", voice_examples=examples)


def test_draft_prompt_receives_approved_examples_as_style_only_evidence():
    prompts = yaml.safe_load((CONFIG / "prompts_packs.yaml").read_text(encoding="utf-8"))
    pipe = _pipeline()
    approved = [
        {
            "example_id": "post-1",
            "provenance": "published",
            "text": "The flashy part gets attention. The reliable part earns trust.",
        }
    ]

    pipe.draft_variants(
        prompts["draft_prompt"],
        {
            "persona_key": "graham",
            "audience": "operators",
            "objective": "share a useful lesson",
            "topic": "reliability",
            "services": [],
            "angle_options": ["practical reliability lesson"],
            "persona_profile": {"tone": ["direct", "humble"]},
            "approved_voice_examples": approved,
            "allowed_sources": [],
        },
    )

    call = pipe.client.calls[0]
    assert "style evidence only" in call["system"]
    assert "do not copy distinctive phrases" in call["system"]
    assert "The flashy part gets attention" in call["user"]


def test_voice_reference_usage_is_visible_in_result_telemetry():
    pipe = _pipeline()
    payload = pipe.finalize(
        "graham",
        "A useful point with enough context to stand on its own.",
        [],
        [],
        voice_reference_count=2,
        voice_reference_ids=["approved-1", "published-2"],
    )

    assert payload["telemetry"]["voice_reference_count"] == 2
    assert payload["telemetry"]["voice_reference_ids"] == ["approved-1", "published-2"]
