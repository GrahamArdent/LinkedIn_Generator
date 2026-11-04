"""Consumer tests: source qualification must affect trial admission, not just prompt decoration."""
import copy,json,hashlib
import pytest
from src.app import codex_trial

def validate_trial_evidence(*args):
    assert callable(getattr(codex_trial, "validate_trial_evidence", None)), "trial evidence admission is not implemented"
    return codex_trial.validate_trial_evidence(*args)

def fixture():
    data={"topic":"MFA recovery","evidence":[{"title":"S1 advisory","fact":"Help desks were socially engineered to reset MFA."}]}
    bundle={"request_sha256":hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
      "sources":[{"source_id":"S1","status":"usable","checked_at":"2026-11-04","limitations":"Historical tactic; not incidence today."}],
      "claims":[{"claim_id":"C1","kind":"fact","text":data["evidence"][0]["fact"],"source_ids":["S1"]},
                {"claim_id":"C2","kind":"opinion","text":"Review recovery as well as sign-in.","source_ids":[]}],
      "central_claim_id":"C1"}
    return data,bundle

def test_evidence_brief_admits_supported_fact_and_unstatistical_opinion():
    data,bundle=fixture()
    assert validate_trial_evidence(data,bundle) is None

@pytest.mark.parametrize("status",["missing","stale","contradicted"])
def test_unusable_central_source_blocks_before_provider_launch(status):
    data,bundle=fixture()
    bundle["sources"][0]["status"]=status
    with pytest.raises(ValueError,match="EVIDENCE_SUPPORT_REQUIRED"):
        validate_trial_evidence(data,bundle)

def test_missing_source_and_changed_frozen_request_block():
    data,bundle=fixture()
    bundle["sources"]=[]
    with pytest.raises(ValueError,match="EVIDENCE_SUPPORT_REQUIRED"): validate_trial_evidence(data,bundle)
    data,bundle=fixture();data["evidence"][0]["fact"]="An invented financial loss."
    with pytest.raises(ValueError,match="EVIDENCE_REQUEST_MISMATCH"): validate_trial_evidence(data,bundle)

from src.app.api import run_generation
from src.app.generation import Pipeline
from src.app.opportunity import assess_opportunity, WEIGHTS as OPPORTUNITY_WEIGHTS

class WriterCapture:
    def __init__(self): self.calls=[]
    def call(self,system,user,response_json=True):
        self.calls.append({"system":system,"user":user})
        return {"text":"Account recovery is part of identity security.\n\nThe advisory describes help-desk resets. A review should include that path.\n\nTest the process before assuming the sign-in screen tells the whole story."}

def test_actual_drafting_consumer_gets_source_specific_plan_and_voice():
    client=WriterCapture()
    run_generation("Account recovery",[],persona_key="graham",audience="IT leaders",
        objective="Review how identity is re-established.",allowed_sources=[{"title":"S1","fact":"Help desks reset tokens."}],
        opportunity_gate=False,publish_quality_gate=False,llm_client=client,hashtags=[])
    call=client.calls[0]
    line=next((x for x in call["user"].splitlines() if x.startswith("Editorial Plan: ")),None)
    assert line is not None, "frozen evidence never reaches a source-specific editorial plan"
    plan=json.loads(line.split(": ",1)[1])
    assert plan["factual_anchor"]["fact"]=="Help desks reset tokens."
    assert plan["reader"]=="IT leaders"
    assert plan["takeaway"]=="Review how identity is re-established."
    assert "trace_operational_friction" in call["user"]
    assert "spoken_voice" in call["user"]

def test_changing_source_changes_actual_plan_anchor_without_new_planning_call():
    pipe=Pipeline({"prompt_kit":{}},client=WriterCapture())
    ctx={"topic":"Account recovery","targets":["IT leaders"],"audience":"IT leaders","objective":"Review recovery."}
    a=pipe.plan({},dict(ctx,evidence=[{"title":"S1","fact":"Help desks reset tokens."}]))
    b=pipe.plan({},dict(ctx,evidence=[{"title":"S2","fact":"Provider recovery uses a separate verification path."}]))
    assert a.get("editorial_plan",{}).get("factual_anchor") != b.get("editorial_plan",{}).get("factual_anchor")
    assert pipe.client.calls==[]

def test_real_preflight_cannot_authorize_omitted_anchor_even_with_high_model_rating():
    class Overconfident:
        def call(self,*args,**kwargs):
            return {"text":json.dumps({**{k:5 for k in OPPORTUNITY_WEIGHTS},"strongest_evidence_index":0})}
    kwargs=dict(topic="Recovery verification",audience="IT leaders",objective="Review recovery",client=Overconfident())
    supported=assess_opportunity(evidence=[{"title":"S1","fact":"Help desks reset tokens."}],**kwargs)
    omitted=assess_opportunity(evidence=[],**kwargs)
    assert supported.decision=="draft"
    assert omitted.decision=="needs_more_evidence"
    assert omitted.strongest_evidence_fact==""
