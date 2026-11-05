"""Controlled writing-stage comparison: actual draft consumer, no editing/scoring."""
from pathlib import Path
import copy,hashlib,json,subprocess
from src.app import api
from src.app.contracts import LinkedInContentRequest
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.codex_trial import validate_trial_evidence,save,now,digest
from src.app.llm import LLMClient

ROOT=Path.cwd()
OUT=ROOT/"evidence/effective-voice-comparison-20261104"
STYLE_IDS=["concise_challenger","reflective_leader","technical_explainer"]
base=json.loads((OUT/"request.json").read_text())
bundle=json.loads((OUT/"source-bundle.json").read_text())
cfg=json.loads((ROOT/".codex-linkedin.local.json").read_text())
config=CodexConfig(**{**cfg,"resume_root":Path(cfg["resume_root"]),"python":Path(cfg["python"])})
class Prepared(Exception):pass
class DraftComplete(Exception):pass

def invoke(data,client):
    request=LinkedInContentRequest.model_validate(data)
    bound={**bundle,"request_sha256":digest(json.dumps(data,sort_keys=True,ensure_ascii=False))}
    validate_trial_evidence(data,bound)
    context=copy.deepcopy(bundle)
    context.pop("request_sha256")
    api.run_generation(topic=request.topic,services=request.services,persona_key=request.persona_key,
      audience=request.audience,objective=request.objective,author_pov=request.author_pov,
      content_goal=request.content_goal,opportunity_gate=False,publish_quality_gate=False,
      targets=request.targets,allowed_sources=[e.model_dump() for e in request.evidence],
      voice_examples=[],hashtags=request.hashtags,llm_client=client,editorial_brief=context,
      writing_voice_id=request.writing_voice_id)

prepared=[]
fixed_hash=None
for style in STYLE_IDS:
    data={**base,"writing_voice_id":style}
    class Capture:
        def call(self,system,user,response_json=True):
            self.system,self.user=system,user
            raise Prepared
    capture=Capture()
    try:invoke(data,capture)
    except Prepared:pass
    profile=json.loads(next(x.split(": ",1)[1] for x in capture.user.splitlines() if x.startswith("Persona Profile: ")))
    neutral=copy.deepcopy(profile);voice=neutral.pop("writing_voice")
    fixed={"system":capture.system,"user":capture.user.replace(json.dumps(profile),"<PERSONA>"),
           "persona_without_style":neutral}
    h=digest(json.dumps(fixed,sort_keys=True))
    if fixed_hash is None:fixed_hash=h
    if h!=fixed_hash:raise ValueError("NON_STYLE_CONTEXT_CHANGED")
    prepared.append({"style":style,"request":data,"request_sha256":digest(json.dumps(data,sort_keys=True,ensure_ascii=False)),
      "voice":voice,"system":capture.system,"user":capture.user,"non_style_context_sha256":h})
manifest={"kind":"controlled_first_drafting_stage_only","created_at":now(),
 "candidate":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
 "budget":{"model_executions":3,"physical_starts":9,"cumulative_cli_seconds":900,"api_spend":0},
 "fixed_context_sha256":fixed_hash,"prepared":prepared,"human_decisions":None,
 "method":"Existing run_generation -> Pipeline.draft_variants -> LLMClient/CodexProvider. Stop after known completed first draft, before any critic/humanizer/scorer. Bound request hashes validated outside prompts; prompt source context retains facts/claims/limitations and omits request-binding metadata only.",
 "code_config_hashes":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
  for folder in ["src/app","config"] for p in (ROOT/folder).glob("*") if p.is_file()}}
manifest_path=OUT/"manifest.json"
if manifest_path.exists():
 old=json.loads(manifest_path.read_text())
 if old["prepared"]!=prepared or old["code_config_hashes"]!=manifest["code_config_hashes"]:
    raise ValueError("STUDY_CONFLICT")
else:save(manifest_path,manifest)
for item in prepared:
    profile=json.loads(next(x.split(": ",1)[1] for x in item["user"].splitlines() if x.startswith("Persona Profile: ")))
    assert not {"tone","rhythm","devices","voice_authority","spoken_voice"}.intersection(profile)
    assert item["user"].count(base["objective"])==1
    assert profile["writing_voice"]["version"]==2
    expected_context=dict(bundle);expected_context.pop("request_sha256")
    assert profile["editorial_context"]["source_bundle"]==expected_context
provider=CodexProvider(config,OUT/"codex-attempts","lig-effective-voice-comparison-20261104")
native=LLMClient(model=config.model,provider=provider)
for index,item in enumerate(prepared,1):
 path=OUT/(item["style"]+".json")
 if path.exists():
    existing=json.loads(path.read_text())
    if existing.get("state")!="completed" or existing.get("prepared")!=item:raise ValueError("RECONCILIATION_REQUIRED")
    print(item["style"],"reopened without generation",flush=True)
    continue
 save(path,{"state":"running","prepared":item,"started_at":now()})
 class NativeCapture:
    def call(self,system,user,response_json=True):
        if system!=item["system"] or user!=item["user"]:raise ValueError("PROMPT_CHANGED")
        if not system.startswith("Write a LinkedIn post as graham"):raise ValueError("UNEXPECTED_STAGE")
        result=native.call(system,user,response_json=response_json)
        if provider.error:raise provider.error
        body=result["text"]
        save(path,{"state":"completed","prepared":item,"body":body,"content_sha256":digest(body),
                   "finished_at":now(),"provider_receipts":provider.receipts[-1:],"human_decision":None})
        raise DraftComplete
 try:
    invoke(item["request"],NativeCapture())
 except DraftComplete:
    print(index,item["style"],"completed",flush=True)
 except Exception as exc:
    save(path,{"state":"unknown" if getattr(exc,"code","")=="CODEX_COMPLETION_UNKNOWN" else "failed",
      "prepared":item,"error":str(exc),"provider_receipts":provider.receipts[-1:],"finished_at":now()})
    raise
print("All3 styles completed",flush=True)
