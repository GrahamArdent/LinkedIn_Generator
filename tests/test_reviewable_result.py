from __future__ import annotations

from src.app.api import run_generation
from src.app.contracts import LinkedInContentRequest
from src.app.integration import generate_content


CLEAN_DRAFT = (
    "What actually earns trust after an AI demo?\n\n"
    "The flashy feature gets attention, but reliability decides whether the workflow survives real use.\n\n"
    "A useful test is simple. Watch the handoff. Watch the recovery path. "
    "Ask what happens when one dependency fails.\n\n"
    "That is the part worth improving before the next demo."
)


class CleanClient:
    def __init__(self):
        self.calls = []

    def call(self, system: str, user: str, response_json: bool = True):
        self.calls.append({"system": system, "user": user, "response_json": response_json})
        return {"text": CLEAN_DRAFT}


def test_integration_maps_typed_review_metadata():
    def fake_generator(**_kwargs):
        report = {
            "score": 94,
            "issues": ["Configured contrast device is absent."],
            "signals": {"has_question": True, "has_contrast": False},
        }
        return {
            "body": "Reviewable draft",
            "hashtags": [],
            "sources": [],
            "telemetry": {"score": 94},
            "quality_report": report,
            "rewrite_reports": [
                {
                    "stage": "critic",
                    "skipped": False,
                    "accepted": True,
                    "reasons": [],
                    "original_report": report,
                    "candidate_report": {
                        "score": 97,
                        "issues": [],
                        "signals": {"has_question": True, "has_contrast": True},
                    },
                }
            ],
        }

    result = generate_content(
        LinkedInContentRequest(topic="review metadata"),
        generator=fake_generator,
    )

    assert result.quality_report is not None
    assert result.quality_report.score == 94
    assert result.quality_report.signals["has_question"] is True
    assert len(result.rewrite_reports) == 1
    assert result.rewrite_reports[0].stage == "critic"
    assert result.rewrite_reports[0].accepted is True
    assert result.rewrite_reports[0].candidate_report.score == 97


def test_real_pipeline_exposes_review_safe_audit_without_internal_prompts(monkeypatch):
    monkeypatch.setenv("N_VARIANTS", "1")
    client = CleanClient()

    payload = run_generation(
        topic="AI workflow reliability",
        services=[],
        persona_key="graham",
        audience="AI operators",
        objective="share a useful lesson",
        targets=["operators"],
        allowed_sources=[],
        voice_examples=[],
        hashtags=[],
        llm_client=client,
    )

    assert len(client.calls) == 1
    assert payload["quality_report"]["score"] == 100
    assert payload["quality_report"]["issues"] == []
    assert [item["stage"] for item in payload["rewrite_reports"]] == ["critic", "humanize"]
    assert all(item["skipped"] is True for item in payload["rewrite_reports"])
    assert all(item["accepted"] is False for item in payload["rewrite_reports"])

    # Public review metadata must not leak provider prompts or model-call payloads.
    serialized = repr(
        {
            "quality_report": payload["quality_report"],
            "rewrite_reports": payload["rewrite_reports"],
        }
    )
    assert "system" not in serialized
    assert "user_template" not in serialized
    assert "api_key" not in serialized
    assert "OPENAI_API_KEY" not in serialized
