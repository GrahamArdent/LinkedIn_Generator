from __future__ import annotations

from pathlib import Path

import yaml

from src.app.api import _persona_profile
from src.app.generation import Pipeline


ROOT = Path(__file__).resolve().parents[1]


class CapturingClient:
    def __init__(self):
        self.calls = []

    def call(self, system, user, response_json=True):
        self.calls.append({"system": system, "user": user, "response_json": response_json})
        return {"text": "A concise draft with enough words to make the test path observable and stable."}


def test_graham_profile_carries_authorized_voice_bible_provenance():
    personas = yaml.safe_load((ROOT / "config/personas.yaml").read_text(encoding="utf-8"))
    profile = _persona_profile(str(ROOT) + "/", personas, "graham")

    authority = profile["voice_authority"]
    assert authority["source"] == {
        "authority": "Graham Voice Bible",
        "repository": "GrahamArdent/LinkedInGenV2",
        "path": "data/Voice_Bible_Graham (1).md",
        "blob_sha": "e35aad7f324ea9cc691ea8fd5ca5fc3c7da5a5fd",
        "role": "primary historical voice authority explicitly authorized for reuse",
    }
    assert authority["profile"]["persona"] == "The Relatable Provocateur"
    assert "Stephen King" not in yaml.safe_dump(authority, allow_unicode=True)


def test_non_graham_persona_does_not_inherit_graham_voice_authority():
    personas = yaml.safe_load((ROOT / "config/personas.yaml").read_text(encoding="utf-8"))
    profile = _persona_profile(str(ROOT) + "/", personas, "ardent_v2")

    assert "voice_authority" not in profile


def test_draft_prompt_receives_voice_bible_as_style_not_evidence():
    prompts = yaml.safe_load((ROOT / "config/prompts_packs.yaml").read_text(encoding="utf-8"))
    personas = yaml.safe_load((ROOT / "config/personas.yaml").read_text(encoding="utf-8"))
    profile = _persona_profile(str(ROOT) + "/", personas, "graham")
    client = CapturingClient()
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
        client=client,
    )
    pipe.n_variants = 1

    pipe.draft_variants(
        prompts["draft_prompt"],
        {
            "persona_key": "graham",
            "audience": "AI builders and operators",
            "objective": "share a useful lesson from real work",
            "topic": "planning should accelerate execution",
            "services": [],
            "angle_options": ["planning becomes harmful when ceremony outruns uncertainty reduction"],
            "persona_profile": profile,
            "approved_voice_examples": [],
            "allowed_sources": [{"title": "Repository evidence", "fact": "A Mode-C prompt defect restarted existing work from Stage 0."}],
        },
    )

    call = client.calls[0]
    assert "authorized Voice Bible guidance" in call["system"]
    assert "it is not factual evidence" in call["system"]
    assert "The Relatable Provocateur" in call["user"]
    assert "bold, witty, empathetic, direct and conversational" in call["user"]
    assert "do not assume cybersecurity" in call["user"]
    assert "A Mode-C prompt defect restarted existing work from Stage 0." in call["user"]
