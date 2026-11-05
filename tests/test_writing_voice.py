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
    assert block.get("version")==(2 if style in {"concise_challenger","reflective_leader","technical_explainer"} else 1) and len(block.get("content_sha256",""))==64
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

def test_malformed_catalogue_never_resolves_partial_alias_or_biography(monkeypatch,tmp_path):
    from src.app import writing_voice
    original=json.loads(writing_voice.CATALOG_PATH.read_text())
    cases=[]
    a=copy.deepcopy(original);a["voices"]["concise_challenger"]["aliases"]="seth_godin";cases.append((a,"seth"))
    a=copy.deepcopy(original);a["voices"]["concise_challenger"]["style_traits"]["avg_sentence_length"]={"credentials":"Invented biography"};cases.append((a,"concise_challenger"))
    a=copy.deepcopy(original);a["voices"]=[];cases.append((a,"concise_challenger"))
    path=tmp_path/"voices.json";monkeypatch.setattr(writing_voice,"CATALOG_PATH",path)
    for catalog,voice in cases:
        path.write_text(json.dumps(catalog))
        with pytest.raises(ValueError,match="writing_voice"):
            writing_voice.resolve_writing_voice(voice)

def test_selected_voice_has_one_precedence_rule_in_writer_and_editors():
    import yaml
    prompts=yaml.safe_load(Path("config/prompts_packs.yaml").read_text())
    for stage in ["draft_prompt","critic_prompt","humanize_prompt","publish_rewrite_prompt"]:
        system=prompts[stage]["system"]
        assert "Approved examples may supply compatible details only" in system,stage
    assert "When no writing_voice is selected" in prompts["humanize_prompt"]["system"]
    assert "Current explicit instructions and approved/edited voice examples take precedence" not in prompts["draft_prompt"]["system"]

def test_terminal_preflight_preserves_selected_style_trace():
    r=request("technical_explainer")
    class Skip(Capture):
        def call(self,*a,**kw):
            return {"text":json.dumps({"outsider_clarity":0,"professional_relevance":0})}
    result=generate_content(r.model_copy(update={"opportunity_gate":True}),
        generator=lambda **kw:api.run_generation(**kw,llm_client=Skip()))
    assert result.status=="skipped"
    assert result.telemetry.get("writing_voice",{}).get("id")=="technical_explainer"

def test_retained_completion_rejects_changed_voice_before_baseline_call(tmp_path,monkeypatch):
    from src.app import writing_voice
    from src.app.codex_trial import complete_comparison
    r=request("concise_challenger");data=r.model_dump();old_voice=voice_context(r)
    class Provider:
        mode="fixture";error=None;receipts=[]
        def __init__(self):self.calls=[]
        def generate(self,**kwargs):self.calls.append(kwargs);return BODY
    p=Provider()
    with pytest.raises(ValueError,match="NO_QUALIFIED_CANDIDATE"):
        run_trial(data,tmp_path/"trial",p,model="fixture",
          engine=lambda *a,**kw:{"body":BODY,"selected_candidate":None,
              "review":{"evaluation_context":old_voice}})
    catalog=json.loads(writing_voice.CATALOG_PATH.read_text())
    catalog["voices"]["concise_challenger"]["style_traits"]["avg_sentence_length"]=13
    path=tmp_path/"changed.json";path.write_text(json.dumps(catalog));monkeypatch.setattr(writing_voice,"CATALOG_PATH",path)
    with pytest.raises(ValueError,match="WRITING_VOICE_CHANGED"):
        complete_comparison(data,tmp_path/"trial",p,model="fixture")
    assert p.calls==[]

def test_selected_style_is_not_penalized_for_inherited_contrast_and_punchy_rhythm():
    from src.app.quality import evaluate_quality
    prose="A payment system needs to carry the approved amount and recipient through every stage of the transfer so that the final instruction can be checked against the same decision the responsible person originally reviewed and accepted before funds leave the account."
    base=voice_context(LinkedInContentRequest(**DATA))
    selected=voice_context(request("technical_explainer"))
    legacy=evaluate_quality(prose,base,{})
    chosen=evaluate_quality(prose,selected,{})
    assert any("contrast" in x for x in legacy["issues"])
    assert any("punchy rhythm" in x for x in legacy["issues"])
    assert not any("contrast" in x or "punchy rhythm" in x for x in chosen["issues"])
    assert chosen["score"]==100

def test_explicit_style_keeps_house_pov_and_factual_rewrite_checks():
    from src.app.quality import evaluate_quality
    from src.app.rewrite_guard import evaluate_rewrite
    persona=voice_context(request("technical_explainer"))
    result=evaluate_quality(BODY+" We promise protection. https://example.com —",persona,{"allow_em_dash":False})
    assert any("URL" in x for x in result["issues"])
    assert any("em dash" in x for x in result["issues"])
    assert any("collective" in x for x in result["issues"])
    assert evaluate_rewrite(BODY,BODY+" Revenue grew 50%.",persona,{})["accepted"] is False

def test_completed_historical_trial_reopens_without_revalidating_changed_catalogue(tmp_path,monkeypatch):
    from src.app import writing_voice
    r=request("concise_challenger");data=r.model_dump()
    class Provider:
        mode="fixture";error=None;receipts=[]
        def __init__(self):self.calls=[]
        def generate(self,**kwargs):self.calls.append(kwargs);return BODY
    p=Provider()
    engine=lambda *a,**kw:{"selected_candidate":{"body":BODY},"telemetry":{"content_goal":"authority"}}
    original=run_trial(data,tmp_path/"trial",p,model="fixture",engine=engine)
    path=tmp_path/"unavailable.json";monkeypatch.setattr(writing_voice,"CATALOG_PATH",path)
    assert run_trial(data,tmp_path/"trial",p,model="fixture",engine=engine)==original
    assert len(p.calls)==1
