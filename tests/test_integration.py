from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.app.contracts import LinkedInContentRequest, SourceEvidence, VoiceExample
from src.app.integration import generate_content


def test_request_requires_non_empty_topic():
    with pytest.raises(ValidationError):
        LinkedInContentRequest(topic="")


def test_dedication_contract_forwards_linkedin_domain_context_only():
    captured = {}

    def fake_generator(**kwargs):
        captured.update(kwargs)
        return {
            "status": "drafted",
            "body": "A useful post from real work.",
            "hashtags": ["#AI"],
            "sources": ["https://example.com/evidence"],
            "telemetry": {"persona": kwargs["persona_key"]},
        }

    request = LinkedInContentRequest(
        request_id="action-123",
        topic="What a buyer conversation taught me about AI workflow adoption",
        persona_key="graham",
        audience="AI founders and operators",
        objective="turn real professional activity into useful visibility",
        author_pov="individual",
        content_goal="authority",
        opportunity_gate=True,
        services=["discovery"],
        targets=["founders", "operators"],
        evidence=[
            SourceEvidence(
                title="Buyer conversation note",
                fact="The buyer cared more about workflow reliability than model novelty.",
                url="https://example.com/evidence",
            )
        ],
        voice_examples=[
            VoiceExample(
                example_id="published-1",
                provenance="published",
                text="The useful part is rarely the flashy part.\n\nReliability is what people remember.",
            )
        ],
        hashtags=["#AI"],
    )

    result = generate_content(request, generator=fake_generator)

    assert captured == {
        "topic": request.topic,
        "services": ["discovery"],
        "persona_key": "graham",
        "audience": "AI founders and operators",
        "objective": "turn real professional activity into useful visibility",
        "author_pov": "individual",
        "content_goal": "authority",
        "opportunity_gate": True,
        "targets": ["founders", "operators"],
        "allowed_sources": [
            {
                "title": "Buyer conversation note",
                "fact": "The buyer cared more about workflow reliability than model novelty.",
                "url": "https://example.com/evidence",
            }
        ],
        "voice_examples": [
            {
                "example_id": "published-1",
                "provenance": "published",
                "text": "The useful part is rarely the flashy part.\n\nReliability is what people remember.",
                "source_ref": None,
            }
        ],
        "hashtags": ["#AI"],
    }
    assert result.request_id == "action-123"
    assert result.origin == "dedication"
    assert result.status == "drafted"
    assert result.body == "A useful post from real work."
    assert result.sources == ["https://example.com/evidence"]


def test_needs_more_evidence_status_and_question_propagate_to_orchestrator():
    question = "What did the system actually make you redo that had already been decided?"

    def fake_generator(**_kwargs):
        return {
            "status": "needs_more_evidence",
            "body": "",
            "hashtags": [],
            "sources": [],
            "telemetry": {
                "opportunity_decision": "needs_more_evidence",
                "missing_evidence_question": question,
            },
        }

    result = generate_content(
        LinkedInContentRequest(topic="Why too much AI verification can create rework"),
        generator=fake_generator,
    )

    assert result.status == "needs_more_evidence"
    assert result.body == ""
    assert result.telemetry["missing_evidence_question"] == question


def test_dedication_request_does_not_inherit_legacy_security_hashtags():
    captured = {}

    def fake_generator(**kwargs):
        captured.update(kwargs)
        return {"body": "Draft", "hashtags": [], "sources": [], "telemetry": {}}

    generate_content(
        LinkedInContentRequest(topic="A lesson from today's professional work"),
        generator=fake_generator,
    )

    assert captured["hashtags"] == []
    assert captured["voice_examples"] == []
    assert captured["author_pov"] == "individual"
    assert captured["content_goal"] == "auto"
    assert captured["opportunity_gate"] is True
    assert "schedule" not in LinkedInContentRequest.model_fields
    assert "scheduled_at" not in LinkedInContentRequest.model_fields
    assert "priority" not in LinkedInContentRequest.model_fields
