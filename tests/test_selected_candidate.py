from __future__ import annotations

import hashlib
import json
from functools import partial

import pytest

from src.app.api import run_generation
from src.app.contracts import LinkedInContentRequest
from src.app.integration import generate_content
from test_publish_quality_review import ORIGINAL, REWRITE, ReviewClient
from test_end_to_end_generation import fixture_visual_planner
from test_opportunity_gate import SequenceClient, payload as opportunity_payload


@pytest.fixture(autouse=True)
def one_variant(monkeypatch):
    monkeypatch.setenv("N_VARIANTS", "1")


def request(**kwargs):
    return LinkedInContentRequest(
        origin="test", topic="When AI planning creates repeated work",
        opportunity_gate=False, audience="AI builders and operators",
        evidence=[{"title": "Build note", "fact": "One planning step reopened settled decisions."}],
        **kwargs,
    )


def run(client, *, visual=True, planner=None):
    calls = []

    def capture(**kwargs):
        calls.append(kwargs)
        return (planner or fixture_visual_planner)(**kwargs)

    result = generate_content(
        request(visual_asset_plan=visual),
        generator=partial(run_generation, llm_client=client),
        visual_planner=capture,
    )
    return result, calls


def rewrite_calls(client):
    return sum("one bounded publish-quality rewrite" in c["system"] for c in client.calls)


def test_rewrite_selected_once_preserves_a_and_b_and_visual_bytes():
    client = ReviewClient(first_score=87, second_score=93)
    result, calls = run(client)
    selected = result.selected_candidate
    assert selected is not None
    assert selected.source == "rewrite"
    assert selected.body == REWRITE
    assert selected.score == 93
    digest = hashlib.sha256(REWRITE.encode("utf-8")).hexdigest()
    assert selected.content_sha256 == digest
    assert selected.candidate_id == "rewrite:" + digest
    assert result.body == ORIGINAL
    assert result.review["original"]["body"] == ORIGINAL
    assert result.review["rewrite"]["body"] == REWRITE
    assert rewrite_calls(client) == 1
    assert client.quality_calls == 2
    assert len(calls) == 1
    assert calls[0]["post_text"] == selected.body
    assert result.visual_asset.source_candidate == "rewrite"
    assert result.visual_asset.source_content_sha256 == digest
    assert json.loads(result.model_dump_json())["selected_candidate"]["body"] == REWRITE


@pytest.mark.parametrize("visual", [True, False])
def test_original_selected_without_rewrite_even_when_visual_disabled(visual):
    client = ReviewClient(first_score=92)
    result, calls = run(client, visual=visual)
    assert result.selected_candidate.source == "original"
    assert result.selected_candidate.body == ORIGINAL
    assert result.selected_candidate.score == 92
    assert rewrite_calls(client) == 0
    assert client.quality_calls == 1
    assert len(calls) == int(visual)
    if not visual:
        assert result.visual_asset is None


@pytest.mark.parametrize("unsafe", [False, True])
def test_low_or_unsafe_b_never_selected_or_planned(unsafe):
    client = ReviewClient(
        first_score=87, second_score=None if unsafe else 87,
        rewrite=REWRITE + (" It improves results by 42%." if unsafe else ""),
    )
    result, calls = run(client)
    assert result.selected_candidate is None
    assert result.body == ORIGINAL
    assert result.review["publish_ready"] is False
    assert result.visual_asset.status == "deferred"
    assert calls == []
    assert rewrite_calls(client) == 1
    assert client.quality_calls == (1 if unsafe else 2)


def test_unavailable_quality_does_not_trigger_rewrite_or_visual():
    class UnavailableQuality(ReviewClient):
        def call(self, system, user, response_json=True):
            if "strict LinkedIn publish-quality evaluator" in system:
                self.quality_calls += 1
                return {"text": "not json"}
            return super().call(system, user, response_json)
    client = UnavailableQuality(first_score=92)
    result, calls = run(client)
    assert result.selected_candidate is None
    assert result.review["original"]["score"] is None
    assert result.review["publish_ready"] is False
    assert result.visual_asset.status == "deferred"
    assert rewrite_calls(client) == 0
    assert client.quality_calls == 1
    assert calls == []


@pytest.mark.parametrize("decision", ["skipped", "needs_more_evidence"])
def test_terminal_preflight_never_drafts_selects_or_plans(decision):
    dims = dict(concrete_evidence=2, distinctiveness=2, strongest_evidence_index=-1,
                missing_evidence_question="What did the system make you redo?")
    if decision == "skipped":
        dims = {k: 1 for k in ("outsider_clarity", "professional_relevance", "concrete_evidence",
                 "distinctiveness", "novel_insight", "practical_usefulness", "emotional_tension",
                 "conversation_potential", "shareability", "voice_fit")}
    gate = SequenceClient([opportunity_payload(**dims)])
    client = SequenceClient([])
    calls = []
    result = generate_content(
        LinkedInContentRequest(topic="A potential lesson", evidence=[], origin="test"),
        generator=partial(run_generation, llm_client=client, opportunity_client=gate),
        visual_planner=lambda **kw: calls.append(kw),
    )
    assert result.status == decision
    assert result.body == ""
    assert result.selected_candidate is None
    assert result.visual_asset is None
    assert len(gate.calls) == 1
    assert client.calls == []
    assert calls == []
    if decision == "needs_more_evidence":
        assert result.telemetry["missing_evidence_question"] == dims["missing_evidence_question"]


def ready_payload():
    return {"status": "drafted", "body": "  Exact café draft.\n\n",
            "review": {"publish_ready": True, "threshold": 90, "recommendation": "original",
                       "original": {"body": "  Exact café draft.\n\n", "score": 92}}}


@pytest.mark.parametrize("score", [None, "bad", "93", True, 93.9, 101, {}])
def test_malformed_quality_is_not_ready_and_does_not_call_planner(score):
    payload = ready_payload()
    payload["review"]["original"]["score"] = score
    calls = []
    result = generate_content(request(), generator=lambda **kw: payload,
                              visual_planner=lambda **kw: calls.append(kw))
    assert result.selected_candidate is None
    assert calls == []
    assert result.visual_asset.status == "deferred"


def test_selection_hashes_exact_utf8_bytes_and_is_stable():
    payload = ready_payload()
    a = generate_content(request(visual_asset_plan=False), generator=lambda **kw: payload)
    b = generate_content(request(visual_asset_plan=False), generator=lambda **kw: payload)
    assert a.selected_candidate.body == payload["body"]
    assert a.selected_candidate.content_sha256 == hashlib.sha256(payload["body"].encode("utf-8")).hexdigest()
    assert a.selected_candidate.candidate_id == b.selected_candidate.candidate_id


@pytest.mark.parametrize("wrong", ["source", "hash"])
def test_wrong_source_visual_plan_is_deferred_without_retry(wrong):
    def planner(**kwargs):
        plan = fixture_visual_planner(**kwargs)
        if wrong == "source":
            plan.source_candidate = "original"
        else:
            # model_validate also exercises dict-returning adapters.
            return {**plan.model_dump(), "source_content_sha256": "0" * 64}
        return plan
    client = ReviewClient(first_score=87, second_score=93)
    result, calls = run(client, planner=planner)
    assert result.selected_candidate.source == "rewrite"
    assert len(calls) == 1
    assert result.visual_asset.status == "deferred"
    assert result.visual_asset.single_image is None
    assert result.visual_asset.carousel is None
    assert "selected_candidate_mismatch" in result.visual_asset.warnings

@pytest.mark.parametrize("field,value", [
    ("source_content_sha256", "incorrect-hash"),
    ("source_content_sha256", ""),
    ("source_content_sha256", 123),
    ("source_candidate", "unknown"),
])
def test_malformed_planner_provenance_defers_instead_of_aborting(field, value):
    def planner(**kwargs):
        return {**fixture_visual_planner(**kwargs).model_dump(), field: value}
    result, calls = run(ReviewClient(first_score=92), planner=planner)
    assert result.selected_candidate.source == "original"
    assert len(calls) == 1
    assert result.visual_asset.status == "deferred"
    assert result.visual_asset.single_image is None
    assert result.visual_asset.carousel is None
    assert "invalid_visual_plan" in result.visual_asset.warnings
