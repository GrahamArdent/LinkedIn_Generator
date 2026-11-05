"""Regressions for lost narrative selection and premature public copy.

Fixtures are synthetic. External model calls are replaced only at the LLM boundary.
Removing the handoff from writer/evaluator, allowing body keys in plans, or
replacing the selected beats with default rhetoric must fail these tests.
"""
import copy
import inspect
import json
import pytest
from src.app import api
from src.app import generation
from src.app.publish_quality import WEIGHTS

def functions():
    import importlib.util
    assert importlib.util.find_spec("src.app.editorial_handoff") is not None, "narrative handoff contract is missing"
    from src.app import editorial_handoff as h
    return h

def meaning():
    return {"thesis":"Accepted access alone does not establish action authorization.",
            "reader_consequence":"Inspect authorization at execution.",
            "facts":[{"claim_id":"F1","text":"The fixture account remained usable.","source_ids":["S1"]}],
            "qualification":"One fixture cannot establish prevalence."}

def narrative(form="symbolic"):
    return {"form":form,"beats":["Illustrate the access distinction.","Explain the reported mechanism.","Bound the comparison.","Inspect the execution check."],
            "symbol":{"image":"A working key does not approve an invoice.",
                      "mapping":[{"symbol_part":"working key","real_relationship":"accepted credential"}],
                      "boundary":"Entry and invoice approval are distinct; this is not an incident."} if form=="symbolic" else None}

def frozen():
    return functions().freeze_handoff(meaning(),narrative())

def test_selected_symbol_survives_freeze_without_reauthoring_and_is_detached():
    m,n=meaning(),narrative()
    result=functions().freeze_handoff(m,n)
    n["symbol"]["image"]="Changed by caller"
    m["thesis"]="Changed by caller"
    assert result["narrative"]["symbol"]["image"]=="A working key does not approve an invoice."
    assert result["meaning"]["thesis"]=="Accepted access alone does not establish action authorization."

@pytest.mark.parametrize("bad",[
    {"editorial":{"body":"A finished post."}},
    {"beats":[{"index":1,"delivery":"outline","body":"A finished post."}],"attribution":[]},
    {"beats":[{"index":1,"delivery":"x"*1000}],"attribution":[]},
])
def test_public_copy_or_unbounded_text_is_rejected_before_next_stage(bad):
    with pytest.raises(ValueError,match="PLANNING_CONTRACT"):
        functions().attach_writing_plan(frozen(),bad)

def test_valid_plan_cannot_replace_selected_beats_or_meaning():
    handoff=frozen()
    plan={"beats":[{"index":i,"delivery":"Brief planning fragment"} for i in range(1,5)],
          "attribution":[{"claim_id":"F1","source_name":"Fixture source"}]}
    result=functions().attach_writing_plan(handoff,plan)
    assert result["meaning"]==meaning()
    assert result["narrative"]==narrative()
    assert "writing_plan" not in handoff

class Capture:
    def __init__(self):self.calls=[]
    def call(self,system,user,response_json=True):
        self.calls.append({"system":system,"user":user})
        if "strict LinkedIn publish-quality evaluator" in system:
            return {"text":json.dumps({**{k:5 for k in WEIGHTS},"essential_checks":{key:{"verdict":"pass","reason":"Meets the fixture brief."} for key in ("factual_integrity","reader_relevance","practical_value","argument_voice")},"gaps":[],"rationale":"Synthetic transport fixture, not quality acceptance."})}
        return {"text":"An accepted credential does not prove permission for every action.\n\nThe fixture account remained usable. This single example cannot establish prevalence.\n\nInspect the authorization check where the action executes."}

def generate(client,**extra):
    assert "editorial_handoff" in inspect.signature(api.run_generation).parameters, "actual engine drops narrative handoff"
    return api.run_generation("Access and authority",[],persona_key="graham",audience="Business and IT leaders",
        objective=meaning()["thesis"],writing_voice_id="relatable_provocateur",
        allowed_sources=[{"title":"Fixture source","fact":"The fixture account remained usable."}],
        opportunity_gate=False,publish_quality_gate=True,llm_client=client,hashtags=[],**extra)

def test_actual_writer_and_evaluator_receive_same_selected_symbol_and_boundaries():
    client=Capture();generate(client,editorial_handoff=frozen())
    writer=next(c for c in client.calls if "Write a LinkedIn post as" in c["system"])
    line=next(x for x in writer["user"].splitlines() if x.startswith("Persona Profile: "))
    # Prompt serialization uses JSON, not Python repr.
    profile=json.loads(line.split(": ",1)[1])
    judge=json.loads(next(c["user"] for c in client.calls if "strict LinkedIn publish-quality evaluator" in c["system"]))
    assert profile["editorial_context"]["handoff"]["narrative"]==narrative()
    assert judge["editorial_brief"]["handoff"]==profile["editorial_context"]["handoff"]
    assert profile["editorial_context"]["handoff"]["meaning"]["qualification"]=="One fixture cannot establish prevalence."

def test_unsupported_handoff_fact_rejected_before_any_provider_call():
    client=Capture();h=frozen();h["meaning"]["facts"][0]["text"]="An invented financial loss."
    with pytest.raises(ValueError,match="HANDOFF_FACT_NOT_ALLOWED"):
        generate(client,editorial_handoff=h)
    assert client.calls==[]

def test_selected_plan_does_not_reintroduce_default_rhetorical_tasks():
    pipe=generation.Pipeline({"prompt_kit":{}},client=Capture())
    plan=pipe.plan({},{"topic":"Access","audience":"Leaders","editorial_handoff":frozen(),
                      "evidence":[{"fact":"The fixture account remained usable."}]})
    assert plan["editorial_plan"]["narrative"]["form"]=="symbolic"
    assert not {"tension_task","mechanism_task","consequence_task","closer_task"} & plan["editorial_plan"].keys()
    assert pipe.client.calls==[]

def test_omitted_selection_retains_existing_planner_behavior():
    pipe=generation.Pipeline({"prompt_kit":{}},client=Capture())
    plan=pipe.plan({},{"topic":"Access","evidence":[{"fact":"The fixture account remained usable."}]})
    assert "tension_task" in plan["editorial_plan"]
    assert "narrative" not in plan["editorial_plan"]

def test_actual_planning_consumer_accepts_only_annotations_and_preserves_selection():
    h=functions()
    assert callable(getattr(h,"plan_writing",None)), "planning consumer is missing"
    plan={"beats":[{"index":i,"delivery":"Short delivery fragment"} for i in range(1,5)],
          "attribution":[{"claim_id":"F1","source_name":"Fixture source"}]}
    class Planner:
        def __init__(self):self.calls=[]
        def call(self,system,user,response_json=True):
            self.calls.append((system,json.loads(user)))
            return {"text":json.dumps(plan)}
    client=Planner()
    result=h.plan_writing(frozen(),{"id":"fixture-only"},[{"source_id":"S1","publisher":"Fixture source"}],client)
    assert client.calls[0][1]["handoff"]["narrative"]==narrative()
    assert result["narrative"]==narrative()
    assert result["meaning"]==meaning()

def test_actual_planning_consumer_rejects_finished_copy_instead_of_sending_it_forward():
    h=functions()
    assert callable(getattr(h,"plan_writing",None)), "planning consumer is missing"
    class ProsePlanner:
        def call(self,*args,**kwargs):
            return {"text":json.dumps({"editorial":{"body":"A completed public draft."}})}
    with pytest.raises(ValueError,match="PLANNING_CONTRACT"):
        h.plan_writing(frozen(),{},[],ProsePlanner())

def test_planner_cannot_attribute_a_fact_to_an_unrelated_supplied_source():
    h=functions()
    plan={"beats":[{"index":i,"delivery":"Planning fragment"} for i in range(1,5)],
          "attribution":[{"claim_id":"F1","source_name":"Other source"}]}
    class WrongAttribution:
        def call(self,*args,**kwargs):return {"text":json.dumps(plan)}
    with pytest.raises(ValueError,match="PLANNING_CONTRACT"):
        h.plan_writing(frozen(),{},[{"source_id":"S1","publisher":"Fixture source"},
                                   {"source_id":"S2","publisher":"Other source"}],WrongAttribution())
