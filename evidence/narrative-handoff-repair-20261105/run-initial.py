"""Bounded narrative repair diagnostic; reuse actual API drafting consumer and Codex bridge."""
from pathlib import Path
import hashlib,json,os,secrets,subprocess,sys
from src.app.api import run_generation
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.editorial_handoff import freeze_handoff,plan_writing
from src.app.llm import LLMClient
from src.app.codex_trial import now,save
ROOT=Path.cwd();OUT=ROOT/"evidence/narrative-handoff-repair-20261105"
OLD=ROOT/"evidence/eight-workflow-trial-20261104"
rawcfg=json.loads((ROOT/".codex-linkedin.local.json").read_text())
cfg={**rawcfg,"resume_root":Path(rawcfg["resume_root"]),"python":Path(rawcfg["python"])}
packet=json.loads((OLD/"packet.json").read_text())
brief=json.loads((OLD/"controlled-brief.json").read_text())["brief"]["artifact"]
meaning={"thesis":brief["thesis"]["text"],"reader_consequence":brief["reader_consequence"]["text"],
 "facts":[{"claim_id":f["claim_id"],"text":f["text"],"source_ids":f["source_ids"]} for f in brief["load_bearing_facts"]],
 "qualification":brief["necessary_qualification"]["text"]}
route=json.loads((OLD/"r2-s1.json").read_text())["output"]["artifact"]
selected=next(a for a in route["hypothetical_illustrations"] if a["id"]==route["selected_analogy"]["id"])
narratives={
 "literal":{"form":"literal","beats":["Explain the literal relationship through the two attributed facts.","Develop the bounded implication from the evidence.","Give the fixed inspection task.","State the necessary qualification."],"symbol":None},
 "symbolic":{"form":"symbolic","beats":["Introduce the selected office-key image as an illustration.","Use the symbol mapping while developing the two attributed mechanisms; do not leave the image as a decorative hook.","State the image boundary and necessary evidentiary qualification.","Carry the same inspection task back through the access-versus-permission distinction."],
 "symbol":{"image":selected["image"],"mapping":[{"symbol_part":m["part"],"real_relationship":m["evidence"]} for m in selected["mapping"][:3]],"boundary":selected["where_it_breaks"]}}
}
frozen={form:freeze_handoff(meaning,n) for form,n in narratives.items()}
admission={"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
 "max_model_calls":5,"max_cumulative_cli_seconds":900,"max_concurrent_calls":1,"api_spend":0,"auto_retry":False,
 "model":cfg["model"],"reasoning":cfg["reasoning"],"client_source_sha":cfg["source_sha"],
 "run_id":"narrative-handoff-20261105","author":"Graham Hill","audience":packet["audience"],
 "voice":packet["voice"],"meaning":meaning,"narratives":narratives,"sources":packet["sources"],
 "narrative_provenance":"Original route2 selected key. Normalize image/mechanism/boundary/action to bounded beat fragments; retain the first three mapping parts. Omit containment-room mapping because containment is outside the identical two-fact lock. No new symbol or post was generated during preparation.",
 "scope":"Two validated annotation plans and two raw first drafts from actual run_generation consumer; one blinded model audit. Not full engine or publish-ready acceptance."}
if (OUT/"ADMISSION.json").exists():
 prior=json.loads((OUT/"ADMISSION.json").read_text());assert prior==admission,"source/experiment changed; do not relaunch"
else:save(OUT/"ADMISSION.json",admission)
provider=CodexProvider(CodexConfig(**cfg),OUT/"attempts",admission["run_id"])
class Recorder:
 def __init__(self,label):self.label=label
 def call(self,system,user,response_json=True):
  path=OUT/(self.label+".json")
  if path.exists():
   d=json.loads(path.read_text());assert d["system"]==system and d["user"]==user
   if d["state"]!="completed":raise ValueError("RECONCILE_ORIGINAL_ATTEMPT "+self.label)
   return {"text":d["raw"]}
  if len(list((OUT/"attempts").rglob("attempt.json")))>=5:raise ValueError("BATCH_CALL_LIMIT")
  save(path,{"state":"running","system":system,"user":user,"started_at":now()})
  try:
   out=LLMClient(model=cfg["model"],provider=provider).call(system,user,response_json=response_json)
   if provider.error:raise provider.error
   save(path,{"state":"completed","system":system,"user":user,"raw":out["text"],
              "receipts":provider.receipts[-1:],"finished_at":now()})
   return out
  except Exception as exc:
   save(path,{"state":"unknown" if getattr(exc,"code","")=="CODEX_COMPLETION_UNKNOWN" else "failed",
              "system":system,"user":user,"reason":str(exc),"receipts":provider.receipts[-1:]});raise
class DraftCaptured(Exception):pass
class FirstDraftOnly:
 def __init__(self,label):self.recorder=Recorder(label)
 def call(self,system,user,response_json=True):
  assert "Write a LinkedIn post as" in system,"only first actual writer consumer is admitted"
  self.recorder.call(system,user,response_json)
  raise DraftCaptured()
os.environ["N_VARIANTS"]="1"
sources=packet["sources"]
allowed=[{"title":next(s["publisher"] for s in sources if s["source_id"]==f["source_ids"][0]),"fact":f["text"]} for f in meaning["facts"]]
source_bundle={"claims":[{"kind":"fact",**f} for f in meaning["facts"]],"central_claim_id":meaning["facts"][0]["claim_id"],"sources":sources}
if sys.argv[1]=="run":
 for form in ["literal","symbolic"]:
  outcome=OUT/(form+"-outcome.json")
  if outcome.exists():continue
  try:
   handoff=plan_writing(frozen[form],packet["voice"],sources,Recorder(form+"-plan"))
   save(OUT/(form+"-handoff.json"),handoff)
   try:
    run_generation(packet["question"],[],persona_key="graham",audience=packet["audience"],
      objective=meaning["thesis"],author_pov="individual",content_goal="authority",
      allowed_sources=allowed,editorial_brief=source_bundle,editorial_handoff=handoff,
      writing_voice_id=packet["voice"]["id"],llm_client=FirstDraftOnly(form+"-draft"),
      opportunity_gate=False,publish_quality_gate=False,hashtags=[])
   except DraftCaptured:pass
   assert (OUT/(form+"-draft.json")).exists()
   save(outcome,{"status":"DRAFTED","scope":"raw first drafting-stage result; intentionally stop before judge/rewrites/finalization","human_preference":None})
  except Exception as exc:save(outcome,{"status":"HOLD","reason":str(exc),"human_preference":None})
 drafts={form:json.loads((OUT/(form+"-draft.json")).read_text())["raw"] for form in narratives if json.loads((OUT/(form+"-outcome.json")).read_text())["status"]=="DRAFTED"}
 if len(drafts)==2:
  m=OUT/"review-mapping.json"
  if m.exists():mapping=json.loads(m.read_text())
  else:
   names=list(drafts);secrets.SystemRandom().shuffle(names);mapping={f"N{i+1:02}":name for i,name in enumerate(names)};save(m,mapping)
  blind={label:drafts[form] for label,form in mapping.items()}
  (OUT/"BLIND_REVIEW.md").write_text("# Private shuffled narrative comparison\n\nHuman preferences pending. Labels are review labels, not provider IDs.\n\n"+"\n\n".join("## "+label+"\n\n"+body for label,body in blind.items())+"\n\nFor each draft: paraphrase its argument, identify support, assess usefulness, explain whether the narrative changes how you understand the point, and record edits plus actual editing time if performed.\n")
  Recorder("audit").call("Audit two shuffled private LinkedIn drafts against the frozen meaning and sources. Return JSON with factual_support, meaning_parity, narrative_difference, voice_fit, usefulness, effort_estimates and limitations. Distinguish an analogy used in the reasoning from a cosmetic opening. Quote exact short passages. No numeric publish-readiness score, winner or human preference. Editing time is an estimate, not measurement.",json.dumps({"drafts":blind,"meaning":meaning,"sources":sources,"voice":packet["voice"],"human_preference":None},ensure_ascii=False))
 print("Diagnostic outcomes and available audit saved",flush=True)
