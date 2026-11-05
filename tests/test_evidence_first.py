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
      "sources":[{"source_id":"S1","status":"usable","checked_at":"2026-11-04","limitations":"Historical tactic; not incidence today.","title":"Advisory","publisher":"Agency","record":"fixture-only","passages":[{"locator":"record","excerpt":"Help desks were socially engineered to reset MFA."}]}],
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

from src.app.publish_quality import assess_publish_quality, WEIGHTS as QUALITY_WEIGHTS

class QualityCapture(WriterCapture):
    def call(self,system,user,response_json=True):
        self.calls.append({"system":system,"user":user})
        if "strict LinkedIn publish-quality evaluator" in system:
            return {"text":json.dumps({**{k:5 for k in QUALITY_WEIGHTS},"gaps":[],"rationale":"Fixture, not human evaluation."})}
        return {"text":"Account recovery is part of identity security.\n\nThe advisory describes help-desk resets. A review should include that path.\n\nTest the process before assuming the sign-in screen tells the whole story."}

def test_real_evaluator_receives_same_brief_full_voice_examples_and_rating_anchors():
    client=QualityCapture()
    example={"example_id":"reference-fixture","provenance":"user_approved","text":"A synthetic style fixture only; never real acceptance evidence."}
    run_generation("Recovery",[],persona_key="graham",audience="IT leaders",objective="Review identity recovery.",
        allowed_sources=[{"title":"S1","fact":"Help desks reset tokens."}],voice_examples=[example],
        opportunity_gate=False,publish_quality_gate=True,llm_client=client,hashtags=[])
    call=next(c for c in client.calls if "strict LinkedIn publish-quality evaluator" in c["system"])
    data=json.loads(call["user"])
    assert data.get("editorial_brief",{}).get("objective")=="Review identity recovery."
    assert data["editorial_brief"]["plan"]["factual_anchor"]["fact"]=="Help desks reset tokens."
    assert "trace_operational_friction" in json.dumps(data["voice_context"])
    assert data.get("approved_voice_examples")==[example]
    assert set(data.get("rating_anchors",{}))=={str(i) for i in range(6)}
    assert data.get("calibration_status")=="NOT_CALIBRATED_TO_HUMAN_JUDGMENTS"

@pytest.mark.parametrize("bad",["missing",True,8,2.5,"five"])
def test_incomplete_or_invalid_model_rating_is_unavailable_not_an_invented_score(bad):
    dims={k:4 for k in QUALITY_WEIGHTS}
    if bad=="missing": dims.pop("voice_authenticity")
    else: dims["voice_authenticity"]=bad
    class Invalid:
        def call(self,*args,**kwargs):return {"text":json.dumps(dims)}
    result=assess_publish_quality(text="A post",audience="IT leaders",content_goal="authority",evidence=[],persona_profile={},client=Invalid())
    assert result.score is None
    assert result.warnings

def test_all_request_facts_require_coverage_not_just_declared_claims():
    data,bundle=fixture()
    data["evidence"].append({"title":"S2","fact":"A second factual assertion."})
    bundle["request_sha256"]=hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    with pytest.raises(ValueError,match="EVIDENCE_SUPPORT_REQUIRED"): validate_trial_evidence(data,bundle)

@pytest.mark.parametrize("mutation",["no_passage","duplicate_source","blank_claim"])
def test_source_records_and_unique_ids_required(mutation):
    data,bundle=fixture()
    if mutation=="no_passage":bundle["sources"][0].pop("passages",None)
    if mutation=="duplicate_source":bundle["sources"].append(copy.deepcopy(bundle["sources"][0]))
    if mutation=="blank_claim":bundle["claims"][0]["claim_id"]=""
    with pytest.raises(ValueError,match="EVIDENCE_SUPPORT_REQUIRED"):validate_trial_evidence(data,bundle)

def test_bound_central_anchor_limits_and_labels_reach_both_consumers():
    import inspect
    assert "editorial_brief" in inspect.signature(run_generation).parameters, "bound semantics are discarded"
    data,bundle=fixture()
    class AlternateAnchor(QualityCapture):
        def call(self,system,user,response_json=True):
            if "content-opportunity" in system:
                self.calls.append({"system":system,"user":user})
                return {"text":json.dumps({**{k:5 for k in OPPORTUNITY_WEIGHTS},"strongest_evidence_index":1})}
            return super().call(system,user,response_json)
    client=AlternateAnchor()
    run_generation("Recovery",[],persona_key="graham",audience="IT leaders",objective="Review recovery.",
        allowed_sources=[*data["evidence"],{"title":"Other","fact":"MFA is recommended."}],
        editorial_brief=bundle,opportunity_gate=True,publish_quality_gate=True,llm_client=client,hashtags=[])
    draft=next(c for c in client.calls if "Write a LinkedIn post as" in c["system"])
    plan=json.loads(next(x.split(": ",1)[1] for x in draft["user"].splitlines() if x.startswith("Editorial Plan: ")))
    assert plan["factual_anchor"]["fact"]==data["evidence"][0]["fact"]
    assert bundle["sources"][0]["limitations"] in draft["user"]
    judge=json.loads(next(c["user"] for c in client.calls if "strict LinkedIn publish-quality evaluator" in c["system"]))
    assert judge["editorial_brief"]["source_bundle"]["claims"]==bundle["claims"]

@pytest.mark.parametrize("mutation",["no_rationale","empty_rationale","no_gaps","invalid_gap"])
def test_malformed_judgment_metadata_cannot_qualify_a_post(mutation):
    dims={**{k:5 for k in QUALITY_WEIGHTS},"gaps":[],"rationale":"Strong fixture."}
    if mutation=="no_rationale":dims.pop("rationale")
    if mutation=="empty_rationale":dims["rationale"]=""
    if mutation=="no_gaps":dims.pop("gaps")
    if mutation=="invalid_gap":dims["gaps"]=[{"invented":"not a gap string"}]
    class Bad:
        def call(self,*a,**kw):return {"text":json.dumps(dims)}
    result=assess_publish_quality(text="A post",audience="IT leaders",content_goal="authority",evidence=[],persona_profile={},client=Bad())
    assert result.score is None

def test_base_persona_reaches_evaluator_for_non_graham_author():
    client=QualityCapture()
    assess_publish_quality(text="A post",audience="IT",content_goal="authority",evidence=[],
        persona_profile={"tone":["direct"],"rhythm":"varied","donts":["no cliches"]},client=client)
    voice=json.loads(client.calls[0]["user"])["voice_context"]
    assert voice.get("tone")==["direct"]
    assert voice.get("rhythm")=="varied"
    assert voice.get("donts")==["no cliches"]
