"""Replicable isolated editorial workflow trial, reusing the existing Codex provider."""
from pathlib import Path
import json,sys,re,concurrent.futures
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.codex_trial import save,now
from src.app.writing_voice import resolve_writing_voice
from src.app.llm import LLMClient
ROOT=Path.cwd();OUT=ROOT/"evidence/eight-workflow-trial-20261104"
packet=json.loads((OUT/"packet.json").read_text())
cfg=json.loads((ROOT/".codex-linkedin.local.json").read_text());cfg.update(resume_root=Path(cfg["resume_root"]),python=Path(cfg["python"]))
COMMON="Prepare an evidence-backed independent editorial artifact for Graham Hill, individual author, business and IT leaders. Separate reported facts, inference and hypothetical illustration. Cite source IDs for facts. No invented events, quotes, personal experience or motives. Return JSON with decision GO or HOLD, artifact, claim_support and limitations. HOLD when the requested approach lacks support. No post until explicitly requested."
def call(provider,label,task,inputs,draft=False):
 path=OUT/(label+".json")
 if path.exists():
  d=json.loads(path.read_text())
  if d["state"]!="completed":raise ValueError("RECONCILE "+label)
  assert d["task"]==task and d["inputs"]==inputs
  return d["output"]
 save(path,{"state":"running","task":task,"inputs":inputs,"started_at":now()})
 try:
  raw=LLMClient(model=cfg["model"],provider=provider).call(COMMON if not draft else "Write one private LinkedIn draft as Graham Hill. Follow the supplied brief, telling and selected voice. Preserve source attribution and uncertainty. No invented personal experience, no em dashes or body URLs. Return only the post.",json.dumps({"task":task,"input":inputs},ensure_ascii=False))["text"]
  if provider.error:raise provider.error
  output=raw if draft else json.loads(raw)
  save(path,{"state":"completed","task":task,"inputs":inputs,"output":output,"raw":raw,"receipts":provider.receipts[-1:],"finished_at":now()})
  return output
 except Exception as exc:
  save(path,{"state":"unknown" if getattr(exc,"code","")=="CODEX_COMPLETION_UNKNOWN" else "failed","error":str(exc),"task":task,"inputs":inputs});raise
def route(n):
 provider=CodexProvider(CodexConfig(**cfg),OUT/"attempts","eight-route-"+str(n)+"-corrected-input")
 stages=list(packet["routes"][str(n)])
 if n==7:stages[0]=stages[0].replace("[cutoff]","2026-10-09")
 if n==4:stages[0]+=" This step deliberately requests a hypothetical prior belief before sources. Return GO for a coherent explicitly hypothetical belief with no asserted empirical claims. Source support is evaluated in the next stage."
 history=[]
 try:
  for i,task in enumerate(stages):
   if n==6 and i==0:
    notes=[]
    for role in ["business owner","technical owner"]:
     notes.append(call(provider,f"r{n}fix-role-{role.replace(' ','-')}",task+" Take only the "+role+" perspective.",{"question":packet["question"],"sources":packet["sources"]}))
    out={"decision":"GO","artifact":notes}
   else:
    src=packet["sources"]
    if n==4 and i==0:src=[]
    if n==7 and i==0:src=[s for s in src if s["source_id"]!="CIAD-2026-0058"]
    out=call(provider,f"r{n}fix-s{i}",task,{"question":packet["question"],"sources":src,"prior":history,"voice":packet["voice"]})
   history.append(out)
   if out.get("decision")=="HOLD":
    save(OUT/f"route-{n}.json",{"status":"HOLD","stage":i,"reason":out});return
  brief=call(provider,f"r{n}fix-brief","Freeze one thesis, reader consequence, at most two load-bearing facts with IDs, one necessary qualification and narrative beats. HOLD if unsupported.",{"route":history,"sources":packet["sources"]})
  if brief.get("decision")=="HOLD":save(OUT/f"route-{n}.json",{"status":"HOLD","reason":brief});return
  voice=call(provider,f"r{n}fix-voice","Make the writing plan and natural attribution. Describe rhythm, evidence placement, transition, and map any analogy to facts with its limit.",{"brief":brief,"voice":packet["voice"],"sources":packet["sources"]})
  draft=call(provider,f"r{n}fix-draft","Write160-220 words using the brief and its narrative form.",{"brief":brief,"plan":voice,"voice":packet["voice"],"sources":packet["sources"]},True)
  save(OUT/f"route-{n}.json",{"status":"DRAFTED","brief":brief,"draft":draft,"human_preference":None})
 except Exception as exc:save(OUT/f"route-{n}.json",{"status":"HOLD","reason":str(exc)})
if sys.argv[1]=="repair":
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(route,[4,7]))
 print("Input repairs completed",flush=True)
elif sys.argv[1]=="routes":
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(route,range(1,9)))
 print("Eight outcomes recorded",flush=True)
elif sys.argv[1]=="controls":
 outcomes=[json.loads((OUT/f"route-{i}.json").read_text()) for i in range(1,9)]
 chosen=next(d for d in outcomes if d["status"]=="DRAFTED")
 brief=chosen["brief"];p=CodexProvider(CodexConfig(**cfg),OUT/"attempts","eight-controls")
 call(p,"control","Write160-220 words expressing this supported brief.",{"brief":brief,"voice":packet["voice"],"sources":packet["sources"]},True)
 for telling in ["literal explanation","analogy with an explicit boundary","documented case from supplied sources"]:
  call(p,"telling-"+telling.split()[0],"Write160-220 words. Use "+telling+". Keep thesis, facts, action and qualification identical to the frozen brief.",{"brief":brief,"voice":packet["voice"],"sources":packet["sources"]},True)
 for style in ["relatable_provocateur","concise_challenger","reflective_leader"]:
  call(p,"voice-"+style,"Write160-220 words. Use the literal explanatory telling. Keep the thesis, facts, action and qualification identical.",{"brief":brief,"telling_outline":["central distinction and one factual anchor","explain the relationship","one practical reader action","necessary scope qualification"],"voice":resolve_writing_voice(style),"sources":packet["sources"]},True)
 save(OUT/"controlled-brief.json",{"selection_rule":"first admitted route in numerical order, frozen before assessment","brief":brief})
 print("Controls completed",flush=True)
