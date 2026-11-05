"""Release regression: normal JSON requests must not silently discard narrative selection."""
import copy,json
import pytest
from src.app.contracts import LinkedInContentRequest
from src.app.codex_trial import run_trial
from test_editorial_handoff import frozen,meaning,Capture

def data():
    return {"request_id":"release-handoff-fixture","origin":"test","topic":"Access and authority",
            "persona_key":"graham","audience":"Business and IT leaders","objective":meaning()["thesis"],
            "writing_voice_id":"relatable_provocateur","opportunity_gate":False,
            "publish_quality_gate":True,"visual_asset_plan":False,"hashtags":[],
            "evidence":[{"title":"Fixture source","fact":"The fixture account remained usable."}],
            "editorial_handoff":frozen()}

def test_json_request_preserves_selected_narrative_in_serialized_contract():
    request=LinkedInContentRequest.model_validate(data())
    assert request.model_dump().get("editorial_handoff")==frozen()

def test_invalid_handoff_is_rejected_at_request_admission():
    bad=data();bad["editorial_handoff"]["editorial"]={"body":"Premature public post."}
    with pytest.raises(ValueError,match="PLANNING_CONTRACT"):
        LinkedInContentRequest.model_validate(bad)

def test_actual_orchestrated_trial_writer_evaluator_and_baseline_share_handoff(tmp_path):
    class Provider:
        mode="fixture";error=None;receipts=[]
        def __init__(self):self.capture=Capture()
        def generate(self,**kw):return self.capture.call(kw["system"],kw["user"])["text"]
    p=Provider()
    result=run_trial(data(),tmp_path,p,model="fixture",score_baseline=True)
    writer=next(c for c in p.capture.calls if "Write a LinkedIn post as" in c["system"])
    profile=json.loads(next(s.split(": ",1)[1] for s in writer["user"].splitlines() if s.startswith("Persona Profile: ")))
    assert profile["editorial_context"].get("handoff")==frozen()
    assert result["baseline"]["user"].get("editorial_handoff")==frozen()
    assert "objective" not in result["baseline"]["user"]
    judgments=[json.loads(c["user"]) for c in p.capture.calls if "publish-quality evaluator" in c["system"]]
    assert len(judgments)==2
    assert all(j["editorial_brief"]["handoff"]==frozen() for j in judgments)
    before=len(p.capture.calls)
    assert run_trial(data(),tmp_path,p,model="fixture",score_baseline=True)==result
    assert len(p.capture.calls)==before
