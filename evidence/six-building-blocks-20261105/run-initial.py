from pathlib import Path
import json,hashlib,subprocess,sys,os,secrets
r=Path('/home/graham/work/linkedin-codex-trial-20261104');release=Path('/home/graham/work/linkedin-generator-releases/0c099d70fc807044355af089d62d1bef049cbb95');sys.path.insert(0,str(release))
from src.app.editorial_handoff import freeze_handoff
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.llm import LLMClient
e=r/'evidence/six-building-blocks-20261105';e.mkdir(exist_ok=True)
save=lambda p,v:p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
old=r/'evidence/installed-acceptance-20261105';original=json.loads((old/'request.json').read_text());bundle=json.loads((old/'source-bundle.json').read_text())
audience='Managers and professionals responsible for approving work, with no cybersecurity or software-development expertise assumed.'
security=json.loads(json.dumps(original['editorial_handoff']))
security['meaning']['thesis']='Recognizing an account or company is not the same as knowing this particular request is permitted.'
security['meaning']['reader_consequence']='For one sensitive request, check what proves that this particular action is permitted, beyond a familiar account or company.'
security['narrative']['beats']=['Start with the ordinary distinction between having a key and permission to take something.','Explain the two reported incidents in ordinary workplace language; define any indispensable specialist term immediately.','Show why recognizing the account or company does not settle whether this action is permitted.','Give the fixed practical inspection task and retain the limits without a technical lecture.']
security.pop('writing_plan',None);security=freeze_handoff(security['meaning'],security['narrative'])
ai_sources=[
{'source_id':'STANFORD-AI-WORK','title':'Generative AI at Work','publisher':'Stanford Digital Economy Lab','url':'https://digitaleconomy.stanford.edu/publication/generative-ai-at-work/','status':'usable','checked_at':'2026-11-05','limitations':'Customer-support deployment; not every job or tool. Current publisher summary reports15%; earlier NBER version reported about14%.','passages':[{'locator':'Abstract line44','excerpt':'using data from 5,172 customer support agents'}]},
{'source_id':'METR-2025','title':'Early-2025 experienced developer productivity experiment','publisher':'METR','url':'https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/','status':'usable','checked_at':'2026-11-05','limitations':'Small randomized study of experienced contributors on familiar repositories using early-2025 tools; not current universal AI performance. February2026 follow-up has selection and measurement biases; METR considers its later effect estimate unreliable. Neither study isolates checking as the cause of all overhead.','passages':[{'locator':'Core result line53','excerpt':'they take 19% longer to complete issues'}]},
{'source_id':'METR-2026-BOUNDARY','title':'Developer productivity experiment design update','publisher':'METR','url':'https://metr.org/blog/2026-02-24-uplift-update/','status':'usable','checked_at':'2026-11-05','limitations':'Same METR origin, not third independent evidence chain.','passages':[{'locator':'Opening line38','excerpt':'an unreliable signal of the current productivity effect'}]}]
ai_facts=[{'claim_id':'AI-F1','text':'The Stanford-published study of 5,172 customer-support agents reports an average15% increase in issues resolved per hour with AI assistance.','source_ids':['STANFORD-AI-WORK']},{'claim_id':'AI-F2','text':'METR reports that16 experienced open-source developers completing246 tasks took19% longer with early-2025 AI tools in its randomized study.','source_ids':['METR-2025']}]
ai=freeze_handoff({'thesis':'AI saves work only when it helps produce usable finished work, not merely faster first output.','reader_consequence':'For one repeated task, compare the time to usable completion with and without AI, including checking and corrections; treat this as a proposed measurement, not a reported study result.','facts':ai_facts,'qualification':'These studies involve different workers, tasks and tools, not a matched comparison. They do not establish checking as the cause of slowdown. METR’s early-2025 result is historical; its February2026 follow-up has selection and measurement biases and does not provide a reliable current effect estimate.'},{'form':'literal','beats':['Begin with a familiar choice: is the work done when output appears, or when it can be used?','Compare the two attributed findings without pretending the settings are equivalent.','Explain the narrow measurement implication; distinguish proposed checking-and-correction measurement from a proven causal explanation.','End with the practical task comparison and a compact evidence boundary.'],'symbol':None})
blocks={}
for name,h,sources in [('security',security,bundle['sources']),('ai',ai,ai_sources)]:
 p=e/name;p.mkdir(exist_ok=True)
 decisions={'1_reader':audience,'2_decision':h['meaning']['reader_consequence'],'3_concept':h['meaning']['thesis'],'4_evidence':{'sources':sources,'purpose':'Support and bound the concept, rather than dictate a technical news summary.'},'5_telling_voice':{'narrative':h['narrative'],'voice':'relatable_provocateur v1; Graham Hill individual author','instruction':'Explain ordinary decisions. Translate credentials as account access, whitelisted infrastructure as recognized company systems, API calls as direct computer-to-computer requests only if indispensable. No invented work experience, dialogue, screen-location assumptions or measured outcomes.'},'6_review':{'questions':['Can a non-specialist paraphrase the point?','What decision changes?','Which facts earn the inference?','Is the telling useful beyond its opening?','What needs editing?'],'human_preferences':None,'equal_word_count_required':False}}
 blocks[name]=decisions
 d={**original,'request_id':'six-blocks-'+name+'-20261105','audience':audience,'objective':h['meaning']['thesis'],'topic':h['meaning']['thesis'],'editorial_handoff':h,'evidence':[{'title':f['source_ids'][0],'fact':f['text']} for f in h['meaning']['facts']]}
 b={'request_sha256':hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'sources':sources,'claims':[{'kind':'fact',**f} for f in h['meaning']['facts']],'central_claim_id':h['meaning']['facts'][0]['claim_id'],'editorial_building_blocks':decisions}
 save(p/'request.json',d);save(p/'source-bundle.json',b)
save(e/'BUILDING_BLOCKS.json',blocks)
save(e/'ADMISSION.json',{'batches':{'security':{'max_calls':12,'max_cli_seconds':900},'ai':{'max_calls':12,'max_cli_seconds':900,'includes_comparison_audit':True}},'api_spend':0,'installed_revision':release.name,'author':'Graham Hill','audience':audience,'voice':'relatable_provocateur v1','scope':'Audience-first reframing with unchanged security incidents, then cross-subject transfer. Audience/brief/telling change together; not single-factor causal proof.','source_retrieval':'Stanford GSB403; Stanford Digital Economy Lab full abstract read instead. METR original and2026 update read. Short excerpts retained; no invented checking-time causal result.'})
launcher='/home/graham/.local/bin/linkedin-codex'
for name in ['security','ai']:
 p=e/name;trial=p/'trial'
 if (p/'OUTCOME.json').exists():continue
 args=['--request',str(p/'request.json'),'--out',str(trial),'--evidence-bundle',str(p/'source-bundle.json'),'--score-baseline']
 x=subprocess.run([launcher,'generate',*args],capture_output=True,text=True,env={**os.environ,'N_VARIANTS':'1'});(p/'generate.log').write_text(x.stdout+x.stderr)
 if x.returncode and (trial/'trial.json').exists() and json.loads((trial/'trial.json').read_text()).get('error_code')=='NO_QUALIFIED_CANDIDATE':
  x=subprocess.run([launcher,'complete-comparison',*args],capture_output=True,text=True,env={**os.environ,'N_VARIANTS':'1'});(p/'complete.log').write_text(x.stdout+x.stderr)
 state=json.loads((trial/'trial.json').read_text()) if (trial/'trial.json').exists() else {}
 save(p/'OUTCOME.json',{'exit':x.returncode,'state':state.get('state','HOLD'),'error':state.get('error_code'),'engine_gate':state.get('engine_gate'),'human_preferences':None})
 print(name,x.returncode,state.get('state'),flush=True)
items={}
historical=json.loads((old/'trial/trial.json').read_text())
for name,d in [('original-security',historical)]+[(n,json.loads((e/n/'trial/trial.json').read_text())) for n in ['security','ai']]:
 if d.get('engine',{}).get('body'):items[name+'-engine']=d['engine']['body']
 if d.get('baseline',{}).get('body'):items[name+'-control']=d['baseline']['body']
names=list(items);secrets.SystemRandom().shuffle(names);mapping={f'B{i+1:02}':n for i,n in enumerate(names)};save(e/'review-mapping.json',mapping)
blind={k:items[n] for k,n in mapping.items()}
(e/'BLIND_REVIEW.md').write_text('# Shuffled six-building-block comparison\n\nHuman preferences pending. Review labels are not provider IDs.\n\n'+'\n\n'.join('## '+k+'\n\n'+v for k,v in blind.items())+'\n\nAssess accessibility, usefulness, factual support, voice and required edits. Actual editing minutes remain unmeasured.\n')
cfg=json.loads((release/'.codex-linkedin.local.json').read_text());cfg.update(resume_root=Path(cfg['resume_root']),python=Path(cfg['python']))
provider=CodexProvider(CodexConfig(**cfg),e/'ai/trial/codex-attempts','six-blocks-ai-20261105')
system='Audit the saved drafts after both subject outcomes. Return JSON. Compare original versus reframed security for accessibility and preserved meaning, then reframed security versus AI for transfer. Evaluate engine versus direct control within each. Identify jargon with passages, unsupported assumptions, useful decisions, voice and editing burden. Different word counts are not defects. No winner or inferred human preference. The subjects differ in evidence and telling, so no single-factor causal claim.'
user=json.dumps({'drafts':blind,'comparison_groups':{'security_before_after':[k for k,v in mapping.items() if 'security' in v],'new_subjects':[k for k,v in mapping.items() if not v.startswith('original')]},'frozen_blocks':blocks,'human_preferences':None},ensure_ascii=False)
save(e/'audit-request.json',{'system':system,'user':user})
if len(list((e/'ai/trial/codex-attempts').rglob('attempt.json')))<12:
 result=LLMClient(model=cfg['model'],provider=provider).call(system,user)
 if provider.error:raise provider.error
 save(e/'audit.json',{'raw':result['text'],'receipts':provider.receipts})
print('Comparison retained',flush=True)
