"""One explicit editorial revision, using the existing bounded rewrite and guard."""
from pathlib import Path
import copy,hashlib,json,subprocess
from src.app.codex_trial import voice_context,validate_trial_evidence,save,now,digest
from src.app.contracts import LinkedInContentRequest
from src.app.writing_voice import resolve_writing_voice
from src.app.publish_quality import PublishQualityAssessment,rewrite_for_publish_quality
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.llm import LLMClient
from src.app.utils import load_yaml

ROOT=Path.cwd();OUT=ROOT/"evidence/editorial-single-draft-20261104"
origin=json.loads((ROOT/"evidence/effective-voice-comparison-20261104/technical_explainer.json").read_text())
original=origin["body"]
assert digest(original)==origin["content_sha256"]=="b8a89caf7e0b048152a02cc644677ac07b14c07c68e009372daddc4eb4dd8a1e"
data=copy.deepcopy(origin["prepared"]["request"])
request=LinkedInContentRequest.model_validate(data)
old_profile=json.loads(next(x.split(": ",1)[1] for x in origin["prepared"]["user"].splitlines() if x.startswith("Persona Profile: ")))
profile=voice_context(request)
profile["active_content_goal"]="authority"
profile["earned_question"]=False
profile["editorial_context"]=copy.deepcopy(old_profile["editorial_context"])
assert profile["writing_voice"]["version"]==3
assert not {"tone","rhythm","devices","voice_authority","spoken_voice"}.intersection(profile)
bundle=copy.deepcopy(profile["editorial_context"]["source_bundle"])
bundle["request_sha256"]=digest(json.dumps(data,sort_keys=True,ensure_ascii=False))
validate_trial_evidence(data,bundle)
prompt=copy.deepcopy(load_yaml(str(ROOT/"config/prompts_packs.yaml"))["publish_rewrite_prompt"])
old="You are doing one bounded publish-quality rewrite of a LinkedIn post that scored below the configured publish threshold."
assert old in prompt["system"]
prompt["system"]=prompt["system"].replace(old,"You are making one explicitly requested editorial diagnostic revision of a retained LinkedIn draft. No publish-quality score or human approval has been assigned.")
assessment=PublishQualityAssessment(score=None,dimensions={},gaps=(
 "Remove redundant thesis restatements so each paragraph adds evidence, explanation, a concrete proposed verification task, or a necessary qualification. Preserve both factual anchors and the payment-control argument. Make the action specific: frame checking the approved recipient and amount, and what prevents a changed transfer, as a proposed verification question, never as an observed test or universal failure. Preserve Indian-campaign scope and source limitations; omit a defensive list of outcomes the post never claims. Do not invent an AI-specific mechanism, new event or outcome. Keep the existing140-180-word target without padding with the same thesis.",
),rationale="Assistant paragraph audit of the retained original; not a model score or owner verdict.",
 warnings=("EDITORIAL_DIAGNOSTIC_NOT_HUMAN_ACCEPTANCE",))
kit=load_yaml(str(ROOT/"config/prompt_kit.config.yaml"))
rules={"emoji_max":int(kit.get("emoji_max",3)),"allow_em_dash":False,
 "forbidden_phrases":load_yaml(str(ROOT/"config/cta_policies.yaml"))["forbidden_phrases"]}
kwargs=dict(original=original,assessment=assessment,prompt=prompt,persona_profile=profile,
 evidence=[x.model_dump() for x in request.evidence],voice_examples=[],content_goal="authority",rules=rules)
class Prepared(Exception):pass
class Capture:
 def call(self,system,user,response_json=True):
  self.system,self.user=system,user
  raise Prepared
capture=Capture()
try:rewrite_for_publish_quality(**kwargs,client=capture)
except Prepared:pass
binding={"original_sha256":digest(original),"request":data,"source_bundle":bundle,
 "writing_voice":profile["writing_voice"],"system":capture.system,"user":capture.user,
 "assessment":assessment.as_dict(),"rules":rules,"scope":"explicit one-revision editorial diagnostic, not automatic score-triggered engine run"}
manifest=OUT/"manifest.json"
if manifest.exists():
 if json.loads(manifest.read_text())["binding"]!=binding:raise ValueError("STUDY_CONFLICT")
else:save(manifest,{"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"created_at":now(),"binding":binding})
result_path=OUT/"result.json"
if result_path.exists():
 result=json.loads(result_path.read_text())
 if result.get("state")!="completed":raise ValueError("RECONCILIATION_REQUIRED")
 if digest(result["candidate"])!=result["candidate_sha256"]:raise ValueError("RESULT_CORRUPT")
 print("Reopened completed editorial revision without generation",flush=True)
else:
 cfg=json.loads((ROOT/".codex-linkedin.local.json").read_text())
 config=CodexConfig(**{**cfg,"resume_root":Path(cfg["resume_root"]),"python":Path(cfg["python"])})
 provider=CodexProvider(config,OUT/"codex-attempts","lig-editorial-single-draft-20261104")
 native=LLMClient(model=config.model,provider=provider)
 save(result_path,{"state":"running","started_at":now(),"original_sha256":digest(original)})
 class NativeCapture:
  def call(self,system,user,response_json=True):
   assert system==capture.system and user==capture.user
   out=native.call(system,user,response_json=response_json)
   if provider.error:raise provider.error
   return out
 try:
  candidate,guard=rewrite_for_publish_quality(**kwargs,client=NativeCapture())
  save(result_path,{"state":"completed","original":original,"original_sha256":digest(original),
    "candidate":candidate,"candidate_sha256":digest(candidate),"guard":guard,
    "publish_quality_score":None,"selected_candidate":None,"human_decision":None,
    "provider_receipts":provider.receipts,"finished_at":now()})
  print(json.dumps({"guard":guard,"candidate":candidate},ensure_ascii=False),flush=True)
 except Exception as exc:
  save(result_path,{"state":"unknown" if getattr(exc,"code","")=="CODEX_COMPLETION_UNKNOWN" else "failed",
    "error":str(exc),"provider_receipts":provider.receipts,"finished_at":now()})
  raise
