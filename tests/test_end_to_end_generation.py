from __future__ import annotations

from functools import partial

from src.app.api import run_generation
from src.app.contracts import LinkedInContentRequest, SourceEvidence
from src.app.integration import generate_content


class FixtureClient:
    def __init__(self):
        self.calls = []

    def call(self, system: str, user: str, response_json: bool = True):
        self.calls.append(
            {
                "system": system,
                "user": user,
                "response_json": response_json,
            }
        )
        return {
            "text": (
                "The model wasn't the interesting part.\n\n"
                "Reliability — not novelty — was the buyer's priority.\n\n"
                "- Start with the failure mode.\n"
                "- Measure the handoff.\n\n"
                "That changes what I would build next."
            )
        }


def test_dedication_style_request_survives_end_to_end(monkeypatch):
    monkeypatch.setenv("N_VARIANTS", "1")
    client = FixtureClient()
    request = LinkedInContentRequest(
        request_id="dedication-linkedin-1",
        origin="dedication",
        topic="What a buyer conversation taught us about AI workflow adoption",
        persona_key="graham",
        audience="AI founders and operators",
        objective="turn real professional activity into useful visibility",
        services=["workflow discovery"],
        targets=["AI founders", "operators"],
        evidence=[
            SourceEvidence(
                title="Buyer conversation note",
                fact="Reliability mattered more than novelty.",
                url="https://example.com/buyer-note",
            )
        ],
        hashtags=[],
    )

    result = generate_content(
        request,
        generator=partial(run_generation, llm_client=client),
    )

    assert result.request_id == "dedication-linkedin-1"
    assert result.origin == "dedication"
    assert result.persona_key == "graham"
    assert result.sources == ["https://example.com/buyer-note"]
    assert result.hashtags == []

    assert "\n\n" in result.body
    assert "🔹 Start with the failure mode." in result.body
    assert "🔹 Measure the handoff." in result.body
    assert "—" not in result.body
    assert "http" not in result.body

    call = client.calls[0]
    assert "AI founders and operators" in call["system"]
    assert "Reliability mattered more than novelty." in call["user"]
    assert "Never invent statistics" in call["system"]
