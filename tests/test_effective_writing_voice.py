"""Consumer regressions for competing style and duplicated editorial authority."""
import copy,json
import pytest
from src.app import api
from src.app.codex_trial import run_trial
from src.app.contracts import LinkedInContentRequest
from src.app.integration import generate_content
from src.app.publish_quality import WEIGHTS

BODY="A payment approval is only part of the evidence.\n\nThe supplied advisory describes payment-interface abuse. I would examine what permission the transfer actually requires.\n\nA review should connect the approved decision to the final instruction."
OBJECTIVE="Authorization must remain enforceable at the point of transfer."
FACT="The supplied advisory describes payment-interface abuse."
DATA=dict(topic="Payment authorization",persona_key="graham",audience="Business and IT leaders",
 objective=OBJECTIVE,author_pov="individual",content_goal="authority",opportunity_gate=False,
 publish_quality_gate=True,visual_asset_plan=False,evidence=[{"title":"S1","fact":FACT}],hashtags=[])
STYLES=["concise_challenger","reflective_leader","technical_explainer"]
FORBIDDEN={"tone","rhythm","devices","voice_authority","spoken_voice"}

class Capture:
    def __init__(self):self.calls=[]
    def call(self,system,user,response_json=True):
        self.calls.append({"system":system,"user":user})
        if "publish-quality evaluator" in system:
            return {"text":json.dumps({**{k:5 for k in WEIGHTS},"gaps":[],"rationale":"Fixture only."})}
        return {"text":BODY}

def run(style,brief=None):
    c=Capture()
    api.run_generation(DATA["topic"],[],persona_key="graham",audience=DATA["audience"],
       objective=OBJECTIVE,author_pov="individual",allowed_sources=DATA["evidence"],
       writing_voice_id=style,opportunity_gate=False,publish_quality_gate=True,
       llm_client=c,hashtags=[],editorial_brief=brief)
    draft=next(x for x in c.calls if x["system"].startswith("Write a LinkedIn post as"))
    profile=json.loads(next(x.split(": ",1)[1] for x in draft["user"].splitlines() if x.startswith("Persona Profile: ")))
    judge=json.loads(next(x["user"] for x in c.calls if "publish-quality evaluator" in x["system"]))
    return c,draft,profile,judge

@pytest.mark.parametrize("style",STYLES)
def test_explicit_style_is_the_only_rhetorical_authority_at_actual_consumers(style):
    c,draft,p,j=run(style)
    assert not FORBIDDEN.intersection(p), "default rhetoric still competes with selected style"
    assert not FORBIDDEN.intersection(j["voice_context"])
    assert p["active_author_pov"]=="individual"
    assert "em_dashes" in p["donts"]
    assert j["voice_context"]["writing_voice"]==p["writing_voice"]
    assert p["writing_voice"]["version"]==(3 if style=="technical_explainer" else 2)
    assert not any(k.endswith("_freq") for k in p["writing_voice"]["style_traits"])
    assert "hook → evidence" not in draft["user"]
    assert "Open with a clear hook, ground the post" not in draft["user"]

@pytest.mark.parametrize("style",STYLES)
def test_objective_is_stated_once_in_writer_and_evaluator_inputs(style):
    _,draft,p,j=run(style)
    assert draft["user"].count(OBJECTIVE)==1
    assert json.dumps(j).count(OBJECTIVE)==1
    assert p["editorial_context"]["objective"]==OBJECTIVE
    assert j["editorial_brief"]["objective"]==OBJECTIVE
    assert "takeaway" not in p["editorial_context"]["plan"]

def test_selected_style_preserves_source_types_limits_and_central_anchor():
    brief={"central_claim_id":"C1","claims":[{"claim_id":"C1","kind":"fact","text":FACT,"source_ids":["S1"]},
       {"claim_id":"I1","kind":"inference","text":OBJECTIVE,"source_ids":["S1"]}],
       "sources":[{"source_id":"S1","limitations":"Historical scope only; not proof every system is vulnerable."}]}
    _,draft,p,j=run("technical_explainer",brief)
    assert p["editorial_context"]["source_bundle"]==brief
    assert j["editorial_brief"]["source_bundle"]==brief
    assert p["editorial_context"]["plan"]["factual_anchor"]["fact"]==FACT
    assert j["grounded_evidence"]==[{"title":"S1","fact":FACT}]

def test_omitted_selection_retains_default_rhetoric_and_existing_plan():
    _,draft,p,j=run(None)
    assert "writing_voice" not in p
    assert p["tone"]==["direct","humble"]
    assert p["voice_authority"]["profile"]["persona"]=="The Relatable Provocateur"
    assert "curious before certain" in p["spoken_voice"]["runtime_summary"]
    assert p["editorial_context"]["plan"]["takeaway"]==OBJECTIVE
    assert "Open with a clear hook, ground the post" in draft["user"]

def test_actual_trial_baseline_and_evaluator_keep_one_selected_style_and_equal_facts(tmp_path):
    class Provider:
        mode="fixture";error=None;receipts=[]
        def __init__(self):self.capture=Capture()
        def generate(self,**kw):return self.capture.call(kw["system"],kw["user"])["text"]
    p=Provider()
    result=run_trial({**DATA,"writing_voice_id":"technical_explainer"},tmp_path,p,model="fixture",score_baseline=True)
    baseline=result["baseline"]["user"]
    engine_context=result["engine"]["review"]["evaluation_context"]
    assert not FORBIDDEN.intersection(baseline["voice"])
    assert baseline["voice"]["writing_voice"]==engine_context["writing_voice"]
    assert baseline["objective"]==engine_context["editorial_context"]["objective"]==OBJECTIVE
    assert baseline["evidence"]==[{"title":"S1","fact":FACT,"url":None}]
    judgments=[json.loads(x["user"]) for x in p.capture.calls if "publish-quality evaluator" in x["system"]]
    assert len(judgments)==2
    for j in judgments:
        assert not FORBIDDEN.intersection(j["voice_context"])
        assert j["voice_context"]["writing_voice"]==baseline["voice"]["writing_voice"]
        assert j["grounded_evidence"]==[{"title":"S1","fact":FACT}]
        assert json.dumps(j).count(OBJECTIVE)==1
    before=len(p.capture.calls)
    assert run_trial({**DATA,"writing_voice_id":"technical_explainer"},tmp_path,p,model="fixture",score_baseline=True)==result
    assert len(p.capture.calls)==before

@pytest.mark.parametrize("style",STYLES)
def test_explicit_style_keeps_public_language_guardrails_and_rewrite_rejection(style):
    from src.app.codex_trial import voice_context
    from src.app.quality import evaluate_quality
    from src.app.rewrite_guard import evaluate_rewrite
    profile=voice_context(LinkedInContentRequest(**DATA,writing_voice_id=style))
    bad=BODY+" Here's the thing: the work packet confirms the result."
    report=evaluate_quality(bad,profile,{})
    assert report["signals"]["matched_internal_terms"]==["work packet"]
    assert report["signals"]["matched_generic_phrases"]==["here's the thing"]
    assert evaluate_rewrite(BODY,bad,profile,{})["accepted"] is False
