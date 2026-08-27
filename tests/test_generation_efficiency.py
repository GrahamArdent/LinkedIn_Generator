from __future__ import annotations

from src.app.generation import Pipeline


class FakeClient:
    def __init__(self):
        self.calls = []

    def call(self, system: str, user: str, response_json: bool = True):
        self.calls.append((system, user, response_json))
        return {"text": "One useful full draft."}


def _config():
    return {
        "prompt_kit": {
            "emoji_max": 3,
            "bullet_char": "🔹",
            "hashtag_min": 0,
            "hashtag_max": 5,
            "strip_links_in_body": True,
            "append_sources_block": False,
            "allow_em_dash": False,
            "forbidden_phrases": [],
        }
    }


def test_default_generation_spends_one_full_draft_call(monkeypatch):
    monkeypatch.delenv("N_VARIANTS", raising=False)
    client = FakeClient()
    pipe = Pipeline(_config(), client=client)

    drafts = pipe.draft_variants(
        {"system": "Write for {audience}", "user_template": "Angles: {angle_options}"},
        {"audience": "professional readers", "angle_options": ["one", "two", "three"]},
    )

    assert pipe.n_variants == 1
    assert drafts == ["One useful full draft."]
    assert len(client.calls) == 1


def test_planner_supplies_three_zero_cost_angle_lenses(monkeypatch):
    monkeypatch.setattr("src.app.generation.retrieve", lambda *args, **kwargs: [])
    client = FakeClient()
    pipe = Pipeline(_config(), client=client)

    plan = pipe.plan(
        {},
        {
            "topic": "what a planning bug taught me about AI development",
            "services": [],
            "targets": ["builders", "operators"],
        },
    )

    assert len(plan["angle_options"]) == 3
    assert plan["angle"] == plan["angle_options"][0]
    assert any("Plain-language lesson" in angle for angle in plan["angle_options"])
    assert any("Second-order consequence" in angle for angle in plan["angle_options"])
    assert any("Contrarian angle" in angle for angle in plan["angle_options"])
    assert "cta" not in plan["sections"]
    assert client.calls == []
