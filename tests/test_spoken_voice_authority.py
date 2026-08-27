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
        return {
            "text": (
                "I noticed a process that looked careful but kept reopening settled work.\n\n"
                "My first reaction was that more checking meant more safety. But that was only useful "
                "if the check was reducing a real uncertainty.\n\n"
                "The better rule is simpler: keep what is already known, and reopen it only when new "
                "evidence gives you a reason."
            )
        }


def _pipeline(client):
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
    return pipe


def test_graham_profile_loads_spoken_voice_as_separate_authority():
    personas = yaml.safe_load((ROOT / "config/personas.yaml").read_text(encoding="utf-8"))
    profile = _persona_profile(str(ROOT) + "/", personas, "graham", author_pov="individual")

    assert "voice_authority" in profile
    assert "spoken_voice" in profile
    spoken = profile["spoken_voice"]
    assert spoken["name"] == "Graham Spoken Voice"
    assert spoken["schema_version"] == "1.0"
    assert spoken["bridge_model"]["concept"] == "A -> B -> C"
    assert spoken["register"]["primary"][:3] == ["plain_spoken", "conversational", "casual_professional"]
    assert "current explicit user instruction" in spoken["precedence"]["highest_to_lowest"]
    assert "user-edited or published voice examples" in spoken["precedence"]["highest_to_lowest"]


def test_non_graham_persona_does_not_inherit_spoken_voice():
    personas = yaml.safe_load((ROOT / "config/personas.yaml").read_text(encoding="utf-8"))
    profile = _persona_profile(str(ROOT) + "/", personas, "ardent_v2", author_pov="company")

    assert "spoken_voice" not in profile


def test_spoken_voice_schema_contains_no_private_source_anecdotes():
    raw = (ROOT / "config/graham_spoken_voice.yaml").read_text(encoding="utf-8").lower()

    # The schema may name evidence classes, but must not carry private anecdotes
    # from the ENFP source material into a production voice prompt.
    forbidden_private_details = [
        "sexual compatibility",
        "wife",
        "revenge",
        "friendship of nearly twenty years",
        "woman i was involved with",
    ]
    assert not any(item in raw for item in forbidden_private_details)


def test_signature_phrases_are_optional_not_boilerplate():
    spoken = yaml.safe_load((ROOT / "config/graham_spoken_voice.yaml").read_text(encoding="utf-8"))

    assert "not mandatory catchphrases" in spoken["signature_concepts"]["usage"]
    frequencies = {item["phrase"]: item["default_frequency"] for item in spoken["signature_concepts"]["phrases"]}
    assert frequencies["There is always a B."] == "rare"
    assert frequencies["Gotta risk it for the biscuit."] == "very_rare_and_only_when_the_register_is_informal"


def test_draft_prompt_receives_spoken_voice_as_style_not_biography():
    prompts = yaml.safe_load((ROOT / "config/prompts_packs.yaml").read_text(encoding="utf-8"))
    personas = yaml.safe_load((ROOT / "config/personas.yaml").read_text(encoding="utf-8"))
    profile = _persona_profile(str(ROOT) + "/", personas, "graham", author_pov="individual")
    client = CapturingClient()
    pipe = _pipeline(client)

    pipe.draft_variants(
        prompts["draft_prompt"],
        {
            "persona_key": "graham",
            "audience": "AI builders and operators",
            "objective": "share a useful lesson from real work",
            "author_pov": "individual",
            "content_goal": "authority",
            "opportunity_assessment": {"decision": "draft", "score": 78},
            "ending_guidance": "End with the strongest useful insight.",
            "topic": "when verification becomes unnecessary rework",
            "services": [],
            "angle_options": ["More checking is useful only when it reduces real uncertainty."],
            "persona_profile": profile,
            "approved_voice_examples": [],
            "allowed_sources": [
                {
                    "title": "Build note",
                    "fact": "A repeated planning step reopened decisions that were already settled.",
                }
            ],
        },
    )

    call = client.calls[0]
    assert "Graham Spoken Voice guidance" in call["system"]
    assert "style/reasoning authority only, not factual evidence or biography" in call["system"]
    assert "thinking-in-motion" in call["system"]
    assert "Do not force the A-to-B-to-C framework" in call["system"]
    assert "curious before certain" in call["user"]
    assert "Do not turn private ENFP material into public biography" in call["user"]
    assert "A repeated planning step reopened decisions" in call["user"]
