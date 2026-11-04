import json
from pathlib import Path
from subprocess import CompletedProcess
import pytest
import src.app.codex_provider as module

def config(tmp_path):
    return module.CodexConfig(resume_root=tmp_path, python=Path("/qualified/python"),
                              source_sha="a"*40, model="gpt-6-astra")

def test_adapter_passes_existing_prompts_and_unwraps_text_without_api(tmp_path, monkeypatch):
    calls=[]
    def run(argv, **kw):
        calls.append((argv,kw))
        return CompletedProcess(argv,0,json.dumps({"ok":True,"data":{"text":"Exact café.\n"},"attempt_id":"a1","cache_hit":False}),"")
    monkeypatch.setenv("OPENAI_API_KEY","must-not-reach-child")
    p=module.CodexProvider(config(tmp_path),tmp_path/"attempts","trial-1",runner=run)
    assert p.generate(model="gpt-6-astra",system="Write grounded text",user="Fact",temperature=.5)=="Exact café.\n"
    assert len(calls)==1
    assert "OPENAI_API_KEY" not in calls[0][1]["env"]
    sent=json.loads(calls[0][1]["input"])
    assert sent["system"]=="Write grounded text" and sent["user"]=="Fact"
    assert p.receipts[0]["attempt_id"]=="a1"

@pytest.mark.parametrize("code",["CODEX_AUTH_REQUIRED","CODEX_OUTPUT_INVALID","CODEX_COMPLETION_UNKNOWN","CODEX_BUDGET_EXHAUSTED"])
def test_failure_is_retained_and_next_call_never_relaunches(tmp_path,code):
    calls=[]
    def run(argv,**kw):
        calls.append(argv)
        return CompletedProcess(argv,2,json.dumps({"ok":False,"code":code,"attempt_id":"original"}),"")
    p=module.CodexProvider(config(tmp_path),tmp_path/"attempts","trial-1",runner=run)
    for _ in range(2):
        with pytest.raises(module.CodexError,match=code):
            p.generate(model="gpt-6-astra",system="s",user="u",temperature=.5)
    assert len(calls)==1
    assert p.error.code==code and p.receipts[0]["attempt_id"]=="original"

@pytest.mark.parametrize("text",["not-json",json.dumps({"ok":True,"data":{"wrong":"value"}})])
def test_bad_bridge_output_is_not_content(tmp_path,text):
    p=module.CodexProvider(config(tmp_path),tmp_path/"attempts","trial-1",
        runner=lambda argv,**kw:CompletedProcess(argv,0,text,""))
    with pytest.raises(module.CodexError,match="CODEX_BRIDGE_OUTPUT_INVALID"):
        p.generate(model="gpt-6-astra",system="s",user="u",temperature=.5)

def test_api_model_cannot_silently_select_another_model(tmp_path):
    p=module.CodexProvider(config(tmp_path),tmp_path,"trial-1",
        runner=lambda *a,**kw:pytest.fail("must not launch"))
    with pytest.raises(module.CodexError,match="CODEX_MODEL_MISMATCH"):
        p.generate(model="gpt-4.1-mini",system="s",user="u",temperature=.5)
