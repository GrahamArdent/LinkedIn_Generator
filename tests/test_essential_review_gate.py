import json
from functools import partial

import pytest

from src.app.api import run_generation
from src.app.contracts import LinkedInContentRequest
from src.app.integration import generate_content
from src.app.publish_quality import WEIGHTS, assess_publish_quality
from test_publish_quality_review import ORIGINAL, REWRITE
from test_end_to_end_generation import fixture_visual_planner

KEYS = ("factual_integrity", "reader_relevance", "practical_value", "argument_voice")

def judgment(*, rating=4, failure=None, verdict="revise", dimension_override=None):
    dims = {k: rating for k in WEIGHTS}
    dims.update(dimension_override or {})
    checks = {k: {"verdict": "pass", "reason": "This fixture meets the supplied brief."} for k in KEYS}
    if failure:
        checks[failure] = {"verdict": verdict, "reason": "Concrete fixture defect requiring correction."}
    return {**dims, "essential_checks": checks, "gaps": ["Reach could improve."],
            "rationale": "Fixture judgment, not a real quality label."}

class Client:
    def __init__(self, first, second=None, rewrite=REWRITE):
        self.outputs = [first] + ([second] if second is not None else [])
        self.calls = []
        self.rewrite = rewrite
    def call(self, system, user, response_json=True):
        self.calls.append((system, user))
        if "strict LinkedIn publish-quality evaluator" in system:
            item = self.outputs.pop(0)
            return {"text": json.dumps(item)}
        if "one bounded publish-quality rewrite" in system:
            return {"text": self.rewrite}
        return {"text": ORIGINAL}

def run(client):
    calls = []
    def planner(**kw):
        calls.append(kw)
        return fixture_visual_planner(**kw)
    req = LinkedInContentRequest(topic="AI planning and repeated work", origin="test",
        audience="AI builders and operators", opportunity_gate=False,
        evidence=[{"title": "Build note", "fact": "A planning step reopened settled decisions."}])
    result = generate_content(req, generator=partial(run_generation, llm_client=client), visual_planner=planner)
    return result, calls

@pytest.fixture(autouse=True)
def one_variant(monkeypatch):
    monkeypatch.setenv("N_VARIANTS", "1")

def test_strong_80_reaches_human_review_and_visual_without_rewrite():
    client = Client(judgment())
    result, calls = run(client)
    assert result.selected_candidate is not None
    assert result.selected_candidate.score == 80
    assert result.review["policy_version"] == "essential-checks-v1"
    assert result.review["threshold_enforced"] is False
    assert result.review["review_status"] == "reviewable"
    assert result.review["human_approval"] == "pending"
    assert result.review["rewrite_triggered"] is False
    assert len(calls) == 1
    assert calls[0]["post_text"] == result.selected_candidate.body

@pytest.mark.parametrize("key,dimension", [("practical_value","practical_usefulness"),("argument_voice","voice_authenticity")])
def test_core_failure_cannot_be_compensated_by_high_total(key, dimension):
    bad = judgment(rating=5, failure=key, dimension_override={dimension:0})
    client = Client(bad, bad)
    result, calls = run(client)
    assert result.review["original"]["score"] >= 90
    assert result.review["review_status"] == "needs_rework"
    assert result.selected_candidate is None
    assert calls == []
    assert result.review["rewrite_triggered"] is True
    assert sum("one bounded publish-quality rewrite" in s for s,u in client.calls) == 1

def test_unsupported_claim_blocks_even_at_100_without_inventing_evidence():
    client = Client(judgment(rating=5, failure="factual_integrity", verdict="needs_evidence"))
    result, calls = run(client)
    assert result.review["original"]["score"] == 100
    assert result.review["review_status"] == "needs_evidence"
    assert result.review["rewrite_triggered"] is False
    assert result.selected_candidate is None
    assert calls == []

def test_low_reach_is_advisory_when_all_essentials_pass():
    result, calls = run(Client(judgment(dimension_override={"novel_insight":1,
        "emotional_tension":1,"conversation_potential":1,"shareability":1})))
    assert result.selected_candidate is not None
    assert result.review["rewrite_triggered"] is False

def test_one_targeted_rewrite_can_qualify_even_with_lower_score():
    client = Client(judgment(rating=5,failure="reader_relevance"), judgment(rating=3))
    result, calls = run(client)
    assert result.selected_candidate.source == "rewrite"
    assert result.selected_candidate.score == 60
    assert result.body == ORIGINAL
    assert result.review["original"]["body"] == ORIGINAL
    assert result.review["rewrite"]["body"] == REWRITE
    assert len(calls) == 1
    rewrite_user = next(u for s,u in client.calls if "one bounded publish-quality rewrite" in s)
    assert "Concrete fixture defect" in rewrite_user

def test_rejected_rewrite_preserves_original_and_blocks_visual():
    client = Client(judgment(failure="argument_voice"), rewrite=REWRITE+" Results improve 42%.")
    result, calls = run(client)
    assert result.body == ORIGINAL
    assert result.review["rewrite"]["guard_accepted"] is False
    assert result.selected_candidate is None
    assert result.review["review_status"] == "needs_rework"
    assert calls == []

@pytest.mark.parametrize("mutation", ["missing","unknown","blank","partial","numeric"])
def test_malformed_essential_checks_are_unavailable_not_legacy_fallback(mutation):
    data = judgment(rating=5)
    if mutation == "missing": del data["essential_checks"]
    elif mutation == "unknown": data["essential_checks"]["practical_value"]["verdict"] = "maybe"
    elif mutation == "blank": data["essential_checks"]["practical_value"]["reason"] = ""
    elif mutation == "partial": del data["essential_checks"]["practical_value"]
    else: data["essential_checks"]["practical_value"]["verdict"] = 5
    client = Client(data)
    result, calls = run(client)
    assert result.review["review_status"] == "assessment_unavailable"
    assert result.review["rewrite_triggered"] is False
    assert result.selected_candidate is None
    assert calls == []

def test_actual_evaluator_prompt_requests_checks_and_keeps_context():
    client = Client(judgment())
    assess_publish_quality(text=ORIGINAL,audience="Business leaders",content_goal="authority",
        evidence=[{"title":"Record","fact":"A planning step reopened settled decisions."}],
        persona_profile={"editorial_context":{"central_argument":"Review must earn its cost."}},client=client)
    system,user = client.calls[0]
    data=json.loads(user)
    assert set(data["required_output"]["essential_checks"]) == set(KEYS)
    assert data["audience"] == "Business leaders"
    assert data["editorial_brief"]["central_argument"] == "Review must earn its cost."
    assert "advisory" in system.lower()

def test_factual_violation_remains_blocked_after_one_failed_repair():
    bad = judgment(rating=5, failure="factual_integrity")
    result, calls = run(Client(bad, bad))
    assert result.review["review_status"] == "blocked"
    assert result.selected_candidate is None
    assert calls == []

@pytest.mark.parametrize("change", ["missing_checks","failed_check","unknown_policy","false_eligibility","unsafe_rewrite"])
def test_selector_rechecks_essentials_instead_of_trusting_ready_flag(change):
    from copy import deepcopy
    from src.app.integration import _publish_candidate
    candidate = {**judgment(), "body": ORIGINAL, "score": 80, "policy_version":"essential-checks-v1",
                 "review_status":"reviewable"}
    payload = {"status":"drafted","review":{"policy_version":"essential-checks-v1",
        "publish_ready":True,"review_eligible":True,"review_status":"reviewable",
        "recommendation":"original","original":candidate}}
    assert _publish_candidate(payload,threshold=90) is not None
    altered = deepcopy(payload)
    review = altered["review"]
    if change == "missing_checks": del review["original"]["essential_checks"]
    elif change == "failed_check": review["original"]["essential_checks"]["practical_value"]["verdict"]="revise"
    elif change == "unknown_policy": review["policy_version"]="unknown"
    elif change == "false_eligibility": review["review_eligible"]=False
    else:
        review["recommendation"]="rewrite"
        review["rewrite"]={**candidate,"guard_accepted":False}
    assert _publish_candidate(altered,threshold=90) is None

def test_legacy_completed_native_results_reopen_without_calls_or_relabeling():
    import hashlib
    from pathlib import Path
    from src.app.codex_trial import run_trial, show_trial
    root=Path(__file__).resolve().parents[1]
    directory=root/"evidence/six-building-blocks-20261105/security/trial"
    before=(directory/"trial.json").read_bytes()
    old=show_trial(directory)
    class Never:
        def generate(self,**kwargs):
            raise AssertionError("Reopening must not execute a model")
    observed=run_trial(old["input"],directory,Never(),model=old["model"],
        score_baseline=old.get("score_baseline",False),evidence_bundle=old.get("evidence_bundle"))
    assert observed==old
    assert hashlib.sha256((directory/"trial.json").read_bytes()).digest()==hashlib.sha256(before).digest()
    assert "policy_version" not in observed["engine"]["review"]

def test_retired_score_environment_cannot_break_new_admission(monkeypatch):
    monkeypatch.setenv("PUBLISH_QUALITY_MIN_SCORE", "retired-value")
    result = run_generation(topic="AI planning",services=[],persona_key="graham",
        audience="Business leaders",opportunity_gate=False,publish_quality_gate=True,
        publish_quality_threshold=None,allowed_sources=[{"title":"Build note","fact":"A step reopened decisions."}],
        llm_client=Client(judgment()),hashtags=[])
    assert result["review"]["review_status"] == "reviewable"

def test_actual_evaluator_requires_coherent_development_separately_from_voice_fidelity():
    client=Client(judgment())
    assess_publish_quality(text=ORIGINAL,audience='Business leaders',content_goal='authority',
        evidence=[{'title':'Record','fact':'A step reopened settled decisions.'}],
        persona_profile={'editorial_context':{'handoff':{'meaning':{'qualification':'One observation only.'}}}},client=client)
    system,user=client.calls[0];data=json.loads(user)
    definition=data['essential_check_definitions']['argument_voice'].lower()
    assert 'coherent development' in definition
    assert 'voice' in definition
    assert 'construction' in system.lower() and 'voice' in system.lower()
    assert len(data['essential_check_definitions'])==4
    assert data['editorial_brief']['handoff']['meaning']['qualification']=='One observation only.'

def test_construction_defect_with_high_voice_score_remains_unqualified_after_failed_rewrite():
    bad=judgment(rating=5,failure='argument_voice')
    bad['essential_checks']['argument_voice']['reason']='Voice fits, but repeated conclusions precede the evidence and the argument does not develop.'
    result,calls=run(Client(bad,bad))
    assert result.selected_candidate is None and calls==[]
    assert result.review['original']['score']==100
    assert result.review['original']['essential_checks']['argument_voice']['reason'].startswith('Voice fits')
    assert result.review['rewrite_triggered'] is True
