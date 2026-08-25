from __future__ import annotations

from src.app import api


def test_run_generation_uses_explicit_orchestrator_context(monkeypatch):
    captured = {}

    class FakePipeline:
        def __init__(self, config):
            captured["config"] = config

        def plan(self, _prompt, ctx):
            captured["plan_ctx"] = ctx
            return {"angle": "real-work lesson", "citations": []}

        def draft_variants(self, _prompt, ctx):
            captured["draft_ctx"] = ctx
            return ["draft"]

        def judge_select(self, _prompt, _persona_profile, drafts):
            return drafts[0]

        def critic(self, _prompt, text):
            return text

        def humanize(self, _prompt, text):
            return text

        def finalize(self, persona_key, text, citations, hashtags):
            captured["finalize"] = {
                "persona_key": persona_key,
                "text": text,
                "citations": citations,
                "hashtags": hashtags,
            }
            return {
                "body": text,
                "hashtags": hashtags,
                "sources": citations,
                "telemetry": {"persona": persona_key},
            }

    def fake_load_yaml(path):
        if path.endswith("prompt_kit.config.yaml"):
            return {}
        if path.endswith("prompts_packs.yaml"):
            return {
                "plan_prompt": {},
                "draft_prompt": {},
                "judge_prompt": {},
                "critic_prompt": {},
                "humanize_prompt": {},
            }
        if path.endswith("personas.yaml"):
            return {"personas": {"graham": {"tone": ["direct"]}}}
        raise AssertionError(path)

    monkeypatch.setattr(api, "Pipeline", FakePipeline)
    monkeypatch.setattr(api, "load_yaml", fake_load_yaml)

    result = api.run_generation(
        topic="What real buyer work taught us",
        services=["discovery"],
        persona_key="graham",
        audience="AI founders",
        objective="useful visibility from real work",
        targets=["founders"],
        allowed_sources=[
            {
                "title": "Buyer note",
                "fact": "Reliability mattered more than novelty.",
                "url": "https://example.com/note",
            }
        ],
        hashtags=["#AI"],
    )

    assert captured["plan_ctx"] == {
        "topic": "What real buyer work taught us",
        "services": ["discovery"],
        "targets": ["founders"],
    }
    assert captured["draft_ctx"]["audience"] == "AI founders"
    assert captured["draft_ctx"]["objective"] == "useful visibility from real work"
    assert captured["draft_ctx"]["allowed_sources"] == [
        {"title": "Buyer note", "fact": "Reliability mattered more than novelty."}
    ]
    assert captured["finalize"]["citations"] == ["https://example.com/note"]
    assert captured["finalize"]["hashtags"] == ["#AI"]
    assert result["body"] == "draft"
