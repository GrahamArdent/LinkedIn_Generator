from pathlib import Path
import json,sys,hashlib
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.codex_trial import save,now,voice_context
from src.app.contracts import LinkedInContentRequest
from src.app.llm import LLMClient
ROOT=Path.cwd();OUT=ROOT/"evidence/source-first-planning-20261104"
if "--show" in sys.argv:
 print((OUT/"planner-result.json").read_text());raise SystemExit
if (OUT/"planner-result.json").exists():
 d=json.loads((OUT/"planner-result.json").read_text())
 if d["state"]!="completed":raise ValueError("RECONCILIATION_REQUIRED")
 print("Reopened without generation");raise SystemExit
sources=json.loads((OUT/"sources.json").read_text())
request=LinkedInContentRequest(topic="CERT-In financial-sector campaign update",persona_key="graham",audience="Business and IT leaders responsible for payment systems",objective="Find one useful evidence-supported professional insight.",writing_voice_id="technical_explainer")
user={"author":"Graham Hill, individual","audience":request.audience,"expertise_area":"Business implications of cybersecurity","voice":voice_context(request),"sources":sources}
system="""Read the complete primary sources and propose one evidence-backed editorial brief for this author and audience. Choose the point only after examining the sources. Output JSON only with decision (draft or needs_more_evidence), angle, useful_difference_from_generic_advice, reader_action, forward_who_to_whom_and_why, format, facts (array of source_id, claim, exact_excerpt, locator), inference, limitations and rejected_angles. Each excerpt must actually occur in the source. Select a concrete mechanism, consequence or tradeoff rather than summarizing the news. Keep author identity and voice separate from factual evidence. Attribute agency claims. Do not invent events, personal expertise, metrics or AI capabilities. A decision to request more evidence is valid. Do not write a post."""
save(OUT/"planner-input.json",{"system":system,"user":user})
cfg=json.loads((ROOT/".codex-linkedin.local.json").read_text());cfg.update(resume_root=Path(cfg["resume_root"]),python=Path(cfg["python"]))
provider=CodexProvider(CodexConfig(**cfg),OUT/"codex-attempts","lig-source-first-planning-20261104")
save(OUT/"planner-result.json",{"state":"running","started_at":now()})
try:
 raw=LLMClient(model=cfg["model"],provider=provider).call(system,json.dumps(user,ensure_ascii=False))["text"]
 if provider.error:raise provider.error
 save(OUT/"planner-result.json",{"state":"completed","raw":raw,"plan":json.loads(raw),"provider_receipts":provider.receipts,"finished_at":now()})
 print(raw)
except Exception as exc:
 save(OUT/"planner-result.json",{"state":"unknown" if getattr(exc,"code","")=="CODEX_COMPLETION_UNKNOWN" else "failed","error":str(exc),"provider_receipts":provider.receipts});raise
