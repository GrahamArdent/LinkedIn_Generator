from __future__ import annotations

from pathlib import Path

import yaml

from src.app import generation
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
            }
        }
    )
    pipe.client = CapturingClient()
    pipe.n_variants = 1
    return pipe


def test_plan_uses_request_topic_and_targets_not_cybersecurity_defaults(monkeypatch):
    monkeypatch.setattr(generation, "retrieve", lambda *_args, **_kwargs: [])
    pipe = _pipeline()

    plan = pipe.plan(
        {},
        {
            "topic": "What a buyer conversation taught us about AI workflow adoption",
            "services": ["discovery"],
            "targets": ["AI founders", "operators"],
        },
    )

    assert "AI workflow adoption" in plan["angle"]
    assert "AI founders, operators" in plan["angle"]
    assert "CFO" not in plan["angle"]
    assert plan["micro_plays"] == []


def test_draft_system_prompt_resolves_persona_and_audience():
    prompts = yaml.safe_load((CONFIG / "prompts_packs.yaml").read_text(encoding="utf-8"))
    pipe = _pipeline()

    drafts = pipe.draft_variants(
        prompts["draft_prompt"],
        {
            "persona_key": "graham",
            "audience": "AI founders and operators",
            "objective": "turn real work into useful visibility",
            "topic": "buyer workflow lesson",
            "services": ["discovery"],
            "angle_options": ["practical lesson"],
            "persona_profile": {"tone": ["direct", "humble"]},
            "allowed_sources": [
                {
                    "title": "Buyer note",
                    "fact": "Reliability mattered more than novelty.",
                }
            ],
        },
    )

    call = pipe.client.calls[0]
    assert drafts == ["draft"]
    assert "as graham" in call["system"]
    assert "AI founders and operators" in call["system"]
    assert "C-suite" not in call["system"]
    assert "{persona_key}" not in call["system"]
    assert "Never invent statistics" in call["system"]
    assert "Reliability mattered more than novelty" in call["user"]
