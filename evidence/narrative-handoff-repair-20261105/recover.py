"""One explicitly admitted recovery; retain original symbolic HOLD and native plan."""
from pathlib import Path
import importlib.util,json,sys,secrets,subprocess,hashlib
sys.argv=[sys.argv[0],"recovery"]
spec=importlib.util.spec_from_file_location("bounded_trial",Path(__file__).with_name("run.py"));r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
e=r.OUT
paths=["src/app/editorial_handoff.py","src/app/api.py","src/app/generation.py","config/prompts_packs.yaml","tests/test_editorial_handoff.py"]
admission={"source_commit":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
 "source_hashes":{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths},
 "run_id":"narrative-handoff-recovery-20261105","max_model_calls":3,"max_cumulative_cli_seconds":900,
 "api_spend":0,"auto_retry":False,"original_outcome":"symbolic-outcome.json",
 "reason":"Initial symbolic delivery annotations251/241 exceeded unchanged240-character guard. Refine planning instruction to target80-160 and reference claim IDs rather than restating facts. No prior draft exists to improve.",
 "scope":"corrected symbolic plan, one original raw draft, blinded pair audit"}
f=e/"RECOVERY_ADMISSION.json"
if f.exists():
 prior=json.loads(f.read_text());admission["source_commit"]=prior["source_commit"];assert prior==admission,"recovery binding changed"
else:r.save(f,admission)
r.provider=r.CodexProvider(r.CodexConfig(**r.cfg),e/"attempts",admission["run_id"])
r.MAX_MODEL_CALLS=3
out=e/"symbolic-recovery-outcome.json"
if not out.exists():
 try:
  handoff=r.plan_writing(r.frozen["symbolic"],r.packet["voice"],r.sources,r.Recorder("symbolic-recovery-plan"))
  r.save(e/"symbolic-recovery-handoff.json",handoff)
  try:
   r.run_generation(r.packet["question"],[],persona_key="graham",audience=r.packet["audience"],
    objective=r.meaning["thesis"],author_pov="individual",content_goal="authority",
    allowed_sources=r.allowed,editorial_brief=r.source_bundle,editorial_handoff=handoff,
    writing_voice_id=r.packet["voice"]["id"],llm_client=r.FirstDraftOnly("symbolic-recovery-draft"),
    opportunity_gate=False,publish_quality_gate=False,hashtags=[])
  except r.DraftCaptured:pass
  r.save(out,{"status":"DRAFTED","original_hold":"symbolic-outcome.json","scope":"first raw draft, stop before judge/editors/finalization","human_preference":None})
 except Exception as exc:r.save(out,{"status":"HOLD","reason":str(exc),"human_preference":None})
if json.loads(out.read_text())["status"]=="DRAFTED":
 drafts={"literal":json.loads((e/"literal-draft.json").read_text())["raw"],"symbolic":json.loads((e/"symbolic-recovery-draft.json").read_text())["raw"]}
 f=e/"review-mapping.json"
 if f.exists():mapping=json.loads(f.read_text())
 else:
  names=list(drafts);secrets.SystemRandom().shuffle(names);mapping={f"N{i+1:02}":n for i,n in enumerate(names)};r.save(f,mapping)
 blind={k:drafts[n] for k,n in mapping.items()}
 (e/"BLIND_REVIEW.md").write_text("# Private shuffled narrative comparison\n\nHuman preferences pending. Review labels are not provider IDs.\n\n"+"\n\n".join("## "+label+"\n\n"+body for label,body in blind.items())+"\n\nFor each draft: paraphrase the argument, identify its support, assess usefulness and voice, explain how its telling changes understanding, and record required edits. Actual editing time remains unavailable until measured.\n")
 r.Recorder("audit").call("Audit two shuffled private LinkedIn drafts against frozen meaning and sources. Return JSON with factual_support, meaning_parity, narrative_difference, voice_fit, usefulness, effort_estimates and limitations. Distinguish an analogy used throughout reasoning from a cosmetic opening. Cite exact short passages. No numeric readiness score, winner or inferred human preference. Editing time is an estimate, not measurement.",json.dumps({"drafts":blind,"meaning":r.meaning,"sources":r.sources,"voice":r.packet["voice"],"human_preference":None},ensure_ascii=False))
print("Recovery outcomes and available audit saved",flush=True)
