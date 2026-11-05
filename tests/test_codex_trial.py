from pathlib import Path
import json
import pytest
from src.app.codex_trial import run_trial, show_trial

INPUT={"request_id":"trial-one","origin":"manual","topic":"One real lesson",
       "evidence":[{"title":"Build note","fact":"A selected text and visual could refer to different revisions."}]}
class Provider:
    mode="fixture"
    def __init__(self): self.calls=[];self.error=None;self.receipts=[]
    def generate(self,**kw):
        self.calls.append(kw)
        return "Supported text."

def engine(request,*,client,visual_planner):
    client.call("system","facts")
    return {"selected_candidate":{"body":"Engine text.","content_sha256":"x"},
            "status":"drafted","visual_asset":{"status":"deferred"}}

def test_same_request_reopens_without_launch_and_changed_input_conflicts(tmp_path):
    p=Provider()
    first=run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=engine)
    assert len(p.calls)==2
    second=run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=engine)
    assert second==first and len(p.calls)==2
    assert show_trial(tmp_path)==first and len(p.calls)==2
    with pytest.raises(ValueError,match="REQUEST_CONFLICT"):
        run_trial({**INPUT,"topic":"changed"},tmp_path,p,model="gpt-6-astra",engine=engine)
    assert len(p.calls)==2

def test_interrupted_record_never_restarts_engine(tmp_path):
    tmp_path.mkdir(exist_ok=True)
    (tmp_path/"trial.json").write_text(json.dumps({"state":"running","input":INPUT}))
    p=Provider()
    with pytest.raises(ValueError,match="RECONCILIATION_REQUIRED"):
        run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=engine)
    assert p.calls==[]

def test_engine_and_baseline_share_facts_and_provider_without_api(tmp_path,monkeypatch):
    from src.app.llm import OpenAIResponsesProvider
    monkeypatch.setattr(OpenAIResponsesProvider,"generate",lambda *a,**kw:pytest.fail("API forbidden"))
    p=Provider()
    r=run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=engine)
    assert len(p.calls)==2 and r["mode"]=="fixture"
    assert INPUT["evidence"][0]["fact"] in p.calls[1]["user"]
    assert sorted(r["review"]["candidates"])==["A","B"]
    assert r["review"]["human_decision"] is None
    assert r["input"]==INPUT

def test_error_or_missing_selected_candidate_does_not_invent_a_pair(tmp_path):
    p=Provider()
    with pytest.raises(ValueError,match="NO_QUALIFIED_CANDIDATE"):
        run_trial(INPUT,tmp_path,p,model="gpt-6-astra",
                  engine=lambda *a,**kw:{"selected_candidate":None})
    assert p.calls==[]
    assert json.loads((tmp_path/"trial.json").read_text())["state"]=="failed"

def test_comparison_completion_uses_retained_unqualified_engine_without_regeneration(tmp_path):
    from src.app.codex_trial import complete_comparison
    p=Provider()
    def unqualified(request,*,client,visual_planner):
        client.call("system","facts")
        return {"body":"Retained engine draft.","selected_candidate":None,
                "review":{"original":{"score":73}}}
    with pytest.raises(ValueError,match="NO_QUALIFIED_CANDIDATE"):
        run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=unqualified)
    assert len(p.calls)==1
    result=complete_comparison(INPUT,tmp_path,p,model="gpt-6-astra")
    assert len(p.calls)==2
    assert result["engine"]["selected_candidate"] is None
    assert result["engine_gate"]=="HOLD_NO_QUALIFIED_CANDIDATE"
    assert (tmp_path/"engine-gate-failure.json").exists()
    assert complete_comparison(INPUT,tmp_path,p,model="gpt-6-astra")==result
    assert len(p.calls)==2

def test_comparison_completion_cannot_relaunch_an_unknown_attempt(tmp_path):
    from src.app.codex_trial import complete_comparison
    (tmp_path/"trial.json").write_text(json.dumps({"state":"unknown","input":INPUT,
        "model":"gpt-6-astra","error_code":"CODEX_COMPLETION_UNKNOWN"}))
    p=Provider()
    with pytest.raises(ValueError,match="RECONCILIATION_REQUIRED"):
        complete_comparison(INPUT,tmp_path,p,model="gpt-6-astra")
    assert p.calls==[]

def test_baseline_receives_every_explicit_engine_constraint(tmp_path):
    p=Provider()
    data={**INPUT,"services":["discovery"],"targets":["operators"],"hashtags":["#AI"]}
    r=run_trial(data,tmp_path,p,model="gpt-6-astra",engine=engine)
    for key in ("services","targets","hashtags"):
        assert r["baseline"]["user"][key]==data[key]

def test_opt_in_baseline_score_uses_engine_context_and_reopen_launches_nothing(tmp_path):
    import inspect
    from src.app.publish_quality import WEIGHTS
    assert "score_baseline" in inspect.signature(run_trial).parameters, "same-rubric baseline assessment is missing"
    class ScoringProvider(Provider):
        def generate(self,**kw):
            self.calls.append(kw)
            if "strict LinkedIn publish-quality evaluator" in kw["system"]:
                return json.dumps({**{k:4 for k in WEIGHTS},"essential_checks":{key:{"verdict":"pass","reason":"Meets the fixture brief."} for key in ("factual_integrity","reader_relevance","practical_value","argument_voice")},"gaps":["Ordinary insight."],"rationale":"Fixture."})
            return "Supported baseline text."
    context={"editorial_context":{"objective":"Review recovery.","approved_voice_examples":[]},
             "voice_authority":{"runtime_guidance":{"causal_summary":"Use supported consequences only."}}}
    def qualified(request,**kwargs):
        return {"selected_candidate":{"body":"Engine text."},"telemetry":{"content_goal":"authority"},
                "review":{"evaluation_context":context}}
    p=ScoringProvider()
    result=run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=qualified,score_baseline=True)
    assert result["baseline"]["quality"]["score"]==80
    judgment=json.loads(p.calls[-1]["user"])
    assert judgment["editorial_brief"]["objective"]=="Review recovery."
    assert judgment["voice_context"]["voice_authority"]==context["voice_authority"]
    assert result["human_decision"] is None
    assert len(p.calls)==2
    assert run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=qualified,score_baseline=True)==result
    assert len(p.calls)==2

def test_study_options_are_part_of_identity_and_conflicts_launch_nothing(tmp_path):
    p=Provider()
    run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=engine)
    with pytest.raises(ValueError,match="REQUEST_CONFLICT"):
        run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=engine,score_baseline=True)
    assert len(p.calls)==2

def test_missing_scoring_context_is_detected_before_baseline_model_call(tmp_path):
    p=Provider()
    with pytest.raises(ValueError,match="BASELINE_EVALUATION_CONTEXT_MISSING"):
        run_trial(INPUT,tmp_path,p,model="gpt-6-astra",score_baseline=True,
            engine=lambda *a,**kw:{"selected_candidate":{"body":"Engine text."}})
    assert p.calls==[]

def test_unknown_optional_assessment_preserves_pair_for_zero_call_review(tmp_path):
    from src.app.codex_provider import CodexError
    class FailingAssessment(Provider):
        def generate(self,**kw):
            self.calls.append(kw)
            if "strict LinkedIn publish-quality evaluator" in kw["system"]:
                self.error=CodexError("CODEX_COMPLETION_UNKNOWN")
                raise self.error
            return "Known completed baseline."
    p=FailingAssessment()
    with pytest.raises(CodexError):
        run_trial(INPUT,tmp_path,p,model="gpt-6-astra",score_baseline=True,
          engine=lambda *a,**kw:{"selected_candidate":{"body":"Engine text."},
            "review":{"evaluation_context":{}},"telemetry":{"content_goal":"authority"}})
    record=show_trial(tmp_path)
    assert record["state"]=="unknown"
    assert record["baseline"]["body"]=="Known completed baseline."
    assert (tmp_path/"review.md").exists()
    assert sorted(record["review"]["candidates"])==["A","B"]
    assert len(p.calls)==2

def test_bound_bundle_is_passed_to_actual_engine_and_baseline_and_bound_on_reopen(tmp_path):
    import inspect,hashlib
    assert "evidence_bundle" in inspect.signature(run_trial).parameters
    bundle={"sources":[{"source_id":"S1","status":"usable","checked_at":"2026-11-04","limitations":"No broader claims.",
          "title":"Build record","publisher":"Owner","record":"fixture-only",
          "passages":[{"locator":"record","excerpt":INPUT["evidence"][0]["fact"]}]}],
        "claims":[{"claim_id":"C1","kind":"observation","text":INPUT["evidence"][0]["fact"],"source_ids":["S1"]}],
        "central_claim_id":"C1","request_sha256":hashlib.sha256(json.dumps(INPUT,sort_keys=True,ensure_ascii=False).encode()).hexdigest()}
    p=Provider()
    def bound_engine(request,**kwargs):
        assert kwargs["editorial_brief"]==bundle
        return {"selected_candidate":{"body":"Engine text."},"telemetry":{"content_goal":"authority"}}
    result=run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=bound_engine,evidence_bundle=bundle)
    assert result["baseline"]["user"]["source_bundle"]==bundle
    assert result["baseline"]["user"]["content_goal"]=="authority"
    assert run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=bound_engine,evidence_bundle=bundle)==result
    with pytest.raises(ValueError,match="REQUEST_CONFLICT"):
        run_trial(INPUT,tmp_path,p,model="gpt-6-astra",engine=bound_engine)
    assert len(p.calls)==1
