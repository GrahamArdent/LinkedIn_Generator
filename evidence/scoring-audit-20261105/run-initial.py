from pathlib import Path
import json,sys,subprocess,hashlib,copy,statistics,collections
r=Path('/home/graham/work/linkedin-codex-trial-20261104');release=Path('/home/graham/work/linkedin-generator-releases/0c099d70fc807044355af089d62d1bef049cbb95');sys.path.insert(0,str(release))
from src.app.publish_quality import assess_publish_quality,WEIGHTS,_weighted_score
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.llm import LLMClient
e=r/'evidence/scoring-audit-20261105';e.mkdir(exist_ok=True)
save=lambda f,d:f.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
rows=[]
for f in (r/'evidence').rglob('trial.json'):
 try:d=json.loads(f.read_text())
 except:continue
 if d.get('mode')!='native_codex':continue
 q=d.get('engine',{}).get('review',{})
 for role,v in [('original',q.get('original')),('rewrite',q.get('rewrite')),('baseline',d.get('baseline',{}).get('quality'))]:
  if isinstance(v,dict) and type(v.get('score')) is int:
   body=v.get('body') or (d.get('baseline',{}).get('body') if role=='baseline' else '')
   rows.append({'path':str(f.relative_to(r)),'role':role,'score':v['score'],'recomputed':_weighted_score(v['dimensions']),'dimensions':v['dimensions'],'gaps':v.get('gaps'),'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'context_sha256':hashlib.sha256(json.dumps(q.get('evaluation_context',{}),sort_keys=True).encode()).hexdigest()})
assert all(x['score']==x['recomputed'] for x in rows)
all4={k:4 for k in WEIGHTS};capped={k:5 for k in WEIGHTS}
for k in ['novel_insight','emotional_tension','shareability']:capped[k]=3
maths={'weights':WEIGHTS,'all_adequate_3':_weighted_score({k:3 for k in WEIGHTS}),'all_strong_4':_weighted_score(all4),'all_exceptional_5':_weighted_score({k:5 for k in WEIGHTS}),'ceiling_if_novelty_emotion_shareability_stay_3':_weighted_score(capped),'strong_4_vs_exceptional_5_weights_needed_for90':50,'cohort_rows':len(rows),'unique_rating_vectors':len(set(tuple(x['dimensions'][k] for k in WEIGHTS) for x in rows)),'histogram':dict(collections.Counter(x['score'] for x in rows)),'threshold_sensitivity_descriptive_only':{str(t):sum(x['score']>=t for x in rows) for t in [70,75,80,85,90]},'caution':'Historical repeated subjects, changing prompts/voices and correlated drafts; not a representative independent sample or validated human-label dataset.'}
save(e/'COHORT.json',rows);save(e/'ARITHMETIC.json',maths)
save(e/'ADMISSION.json',{'max_model_calls':6,'max_cli_seconds':900,'api_spend':0,'purpose':'Evaluator-only repeatability and negative controls; no generation, score retuning, product change or publishing','human_gold_labels':'unavailable; prior both-good feedback is not a calibrated publish-ready label'})
cases=[]
for name in ['security','ai']:
 d=json.loads((r/f'evidence/six-building-blocks-20261105/{name}/trial/trial.json').read_text());req=d['input'];ctx=d['engine']['review']['evaluation_context']
 for rep in [1,2]:cases.append((f'{name}-repeat-{rep}',d['engine']['review']['original']['body'],req,ctx))
ai=json.loads((r/'evidence/six-building-blocks-20261105/ai/trial/trial.json').read_text());req=ai['input'];ctx=ai['engine']['review']['evaluation_context']
cases.append(('deliberately-generic-negative','AI changes everything. Work smarter. The future is here. What do you think?',req,ctx))
cases.append(('deliberately-unsupported-negative',ai['engine']['review']['original']['body']+'\n\nIn my own company, AI reduced costs by87% in one week. Every organization will achieve the same result.',req,ctx))
cfg=json.loads((release/'.codex-linkedin.local.json').read_text());cfg.update(resume_root=Path(cfg['resume_root']),python=Path(cfg['python']))
provider=CodexProvider(CodexConfig(**cfg),e/'attempts','scoring-audit-20261105')
for label,body,req,ctx in cases:
 f=e/(label+'.json')
 if f.exists():
  assert json.loads(f.read_text())['state']=='completed';continue
 record={'state':'running','post':body,'request_context':req,'persona_context':ctx,'negative_fixture':label.startswith('deliberately')}
 save(f,record)
 class Capture:
  def call(self,system,user,response_json=True):
   record['system']=system;record['user']=user;save(f,record)
   out=LLMClient(model=cfg['model'],provider=provider).call(system,user,response_json=response_json)
   if provider.error:raise provider.error
   record['raw']=out['text'];return out
 result=assess_publish_quality(text=body,audience=req['audience'],content_goal='authority',evidence=req['evidence'],persona_profile=ctx,client=Capture())
 record.update(state='completed',assessment=result.as_dict(),receipts=provider.receipts[-1:])
 save(f,record);print(label,result.score,flush=True)
print('Evaluator audit complete',flush=True)
