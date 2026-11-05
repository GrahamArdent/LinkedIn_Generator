"""Fresh same-input engine/simple-prompt comparison via the existing trial runner."""
from pathlib import Path
import hashlib,json,subprocess
from src.app.codex_trial import run_trial,complete_comparison,validate_trial_evidence,save,now,digest
from src.app.contracts import LinkedInContentRequest
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.writing_voice import resolve_writing_voice

ROOT=Path.cwd();OUT=ROOT/"evidence/source-first-planning-20261104"
data=json.loads((OUT/"request.json").read_text())
bundle=json.loads((OUT/"source-bundle.json").read_text())
request=LinkedInContentRequest.model_validate(data)
validate_trial_evidence(data,bundle)
assert request.writing_voice_id=="technical_explainer" and resolve_writing_voice(request.writing_voice_id)["version"]==3
assert request.publish_quality_gate and not request.opportunity_gate and not request.visual_asset_plan
cfg=json.loads((ROOT/".codex-linkedin.local.json").read_text())
config=CodexConfig(**{**cfg,"resume_root":Path(cfg["resume_root"]),"python":Path(cfg["python"])})
binding={"request":data,"source_bundle":bundle,"writing_voice":resolve_writing_voice(request.writing_voice_id),
 "model":config.model,"reasoning":config.reasoning,"score_baseline":True,
 "product_hashes":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
    for folder in ["src/app","config"] for p in (ROOT/folder).glob("*") if p.is_file()}}
manifest=OUT/"manifest.json"
if manifest.exists():
 if json.loads(manifest.read_text())["binding"]!=binding:raise ValueError("STUDY_CONFLICT")
else:save(manifest,{"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"created_at":now(),"binding":binding})
provider=CodexProvider(config,OUT/"codex-attempts","lig-source-first-planning-20261104")
trial=OUT/"trial"
# Known quality rejection is recoverable; unknown effects or other failures are not.
path=trial/"trial.json"
if path.exists():
 prior=json.loads(path.read_text())
 if prior["state"]=="failed" and prior.get("error_code")=="NO_QUALIFIED_CANDIDATE":
  result=complete_comparison(data,trial,provider,model=config.model,score_baseline=True,evidence_bundle=bundle)
 else:
  result=run_trial(data,trial,provider,model=config.model,score_baseline=True,evidence_bundle=bundle)
else:
 try:
  result=run_trial(data,trial,provider,model=config.model,score_baseline=True,evidence_bundle=bundle)
 except ValueError as exc:
  if str(exc)!="NO_QUALIFIED_CANDIDATE":raise
  print("Known engine quality HOLD retained; completing baseline without engine regeneration",flush=True)
  result=complete_comparison(data,trial,provider,model=config.model,score_baseline=True,evidence_bundle=bundle)
assert result["state"]=="completed"
attempts=[json.loads(p.read_text()) for p in OUT.rglob("attempt.json")]
assert len(attempts)<=12 and sum(x["elapsed_seconds"] for x in attempts)<=900
save(OUT/"completion.json",{"completed_at":now(),"state":result["state"],"engine_gate":result.get("engine_gate"),
 "model_calls":len(attempts),"api_spend":0,"human_decision":None})
print(json.dumps({"state":result["state"],"engine_gate":result.get("engine_gate"),"model_calls":len(attempts)}),flush=True)
