"""Writing voice is an independent, versioned input; fixtures do not establish human quality."""
import copy,json,inspect
import pytest
from pathlib import Path
from src.app import api
from src.app.contracts import LinkedInContentRequest
from src.app.integration import generate_content
from src.app.codex_trial import voice_context,run_trial
from src.app.publish_quality import WEIGHTS

STYLE_IDS=["concise_challenger","reflective_leader","counterintuitive_analyst","direct_motivator","purpose_led","practical_experimenter","balanced_authority","technical_explainer","relatable_provocateur"]
BODY="The approval screen is part of a payment.\n\nThe supplied advisory describes payment-interface abuse. I would trace authorization through to the transfer itself.\n\nA review earns its place when it shows where permission is checked."
DATA=dict(topic="Payment authorization",persona_key="graham",audience="Business and IT leaders",
 objective="Trace payment approval through to the transfer.",author_pov="individual",content_goal="authority",
 opportunity_gate=False,publish_quality_gate=True,visual_asset_plan=False,
 evidence=[{"title":"S1","fact":"The supplied advisory describes payment-interface abuse."}],hashtags=[])

def request(style):
    assert "writing_voice_id" in LinkedInContentRequest.model_fields, "independent writing voice is missing"
    return LinkedInContentRequest(**DATA,writing_voice_id=style)

class Capture:
    def __init__(self):self.calls=[]
    def call(self,system,user,response_json=True):
        self.calls.append({"system":system,"user":user})
        if "publish-quality evaluator" in system:
            return {"text":json.dumps({**{k:5 for k in WEIGHTS},"gaps":[],"rationale":"Synthetic fixture only."})}
        return {"text":BODY}

def prompts(style):
    r=request(style);client=Capture()
    result=generate_content(r,generator=lambda **kw:api.run_generation(**kw,llm_client=client))
    draft=next(x for x in client.calls if "Write a LinkedIn post as" in x["system"])
    persona=json.loads(next(line.split(": ",1)[1] for line in draft["user"].splitlines() if line.startswith("Persona Profile: ")))
    judgment=json.loads(next(x["user"] for x in client.calls if "publish-quality evaluator" in x["system"]))
    return r,client,result,draft,persona,judgment

@pytest.mark.parametrize("style",STYLE_IDS)
def test_each_recovered_style_reaches_actual_drafting_and_judging_consumer(style):
    r,client,result,draft,profile,judgment=prompts(style)
    block=profile.get("writing_voice",{})
    assert block.get("id")==style
    assert block.get("version")==1 and len(block.get("content_sha256",""))==64
    assert judgment["voice_context"]["writing_voice"]==block
    assert result.telemetry["writing_voice"]==block
    assert "selected Writing Voice" in draft["system"]
    assert result.persona_key=="graham"
    assert r.audience==DATA["audience"] and r.objective==DATA["objective"]
    assert r.model_dump()["evidence"]==LinkedInContentRequest(**DATA).model_dump()["evidence"]

def test_prompt_difference_is_only_the_selected_style_block():
    a=prompts("concise_challenger");b=prompts("technical_explainer")
    assert a[3]["system"]==b[3]["system"]
    assert a[4]["writing_voice"]!=b[4]["writing_voice"]
    pa=copy.deepcopy(a[4]);pb=copy.deepcopy(b[4]);pa.pop("writing_voice");pb.pop("writing_voice")
    assert pa==pb
    ua=a[3]["user"].replace(json.dumps(a[4]),"<SAME_PERSONA>")
    ub=b[3]["user"].replace(json.dumps(b[4]),"<SAME_PERSONA>")
    assert ua==ub
    ja=copy.deepcopy(a[5]);jb=copy.deepcopy(b[5])
    ja["voice_context"].pop("writing_voice");jb["voice_context"].pop("writing_voice")
    assert ja==jb

@pytest.mark.parametrize("bad",["not_a_voice","../personas","", "Seth Godin"])
def test_unknown_explicit_voice_is_rejected_at_request_admission(bad):
    assert "writing_voice_id" in LinkedInContentRequest.model_fields
    with pytest.raises(ValueError,match="writing_voice"):
        LinkedInContentRequest(**DATA,writing_voice_id=bad)

def test_direct_engine_unknown_voice_fails_before_any_client_call():
    assert "writing_voice_id" in inspect.signature(api.run_generation).parameters
    client=Capture()
    with pytest.raises(ValueError,match="writing_voice"):
        api.run_generation("topic",[],writing_voice_id="no_such_voice",llm_client=client)
    assert client.calls==[]

def test_legacy_alias_projects_traits_without_named_author_or_biography():
    r=request("seth_godin");profile=voice_context(r);block=profile.get("writing_voice",{})
    assert block.get("id")=="concise_challenger"
    text=json.dumps(block).lower()
    for forbidden in ["seth","godin","marketing strategist","entrepreneurs","purple_cow","here's the thing","credentials"]:
        assert forbidden not in text
    assert block.get("style_traits",{}).get("avg_sentence_length")==12.0
    assert profile["active_author_pov"]=="individual"
    assert voice_context(LinkedInContentRequest(**DATA)).get("writing_voice") is None

def test_baseline_and_trial_identity_keep_selected_style_and_no_call_reopen(tmp_path):
    r=request("technical_explainer")
    class Provider:
        mode="fixture"
        error=None
        receipts=[]
        def __init__(self):self.calls=[]
        def generate(self,**kwargs):self.calls.append(kwargs);return BODY
    provider=Provider()
    def engine(req,**kwargs):
        return {"selected_candidate":{"body":BODY},"telemetry":{"content_goal":"authority"}}
    data=r.model_dump();result=run_trial(data,tmp_path,provider,model="fixture",engine=engine)
    assert result["baseline"]["user"]["voice"]["writing_voice"]==voice_context(r)["writing_voice"]
    assert run_trial(data,tmp_path,provider,model="fixture",engine=engine)==result
    with pytest.raises(ValueError,match="REQUEST_CONFLICT"):
        run_trial({**data,"writing_voice_id":"concise_challenger"},tmp_path,provider,model="fixture",engine=engine)
    assert len(provider.calls)==1
