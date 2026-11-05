from pathlib import Path
import json,sys,hashlib,subprocess,time
root=Path('/home/graham/work/linkedin-codex-trial-20261104');sys.path.insert(0,str(root))
from src.app.publish_quality import assess_publish_quality
from src.app.codex_provider import CodexConfig,CodexProvider
from src.app.llm import LLMClient
e=root/'evidence/essential-review-gate-20261105'
if (e/'MILESTONE.json').exists():
 print('Completed evidence retained; no model calls.');sys.exit(0)
save=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
save(e/'ADMISSION.json',{'max_subscription_evaluations':2,'max_cumulative_cli_seconds':900,'api_spend':0,'generation':False,'purpose':'Existing-text evaluator semantic smoke, not human calibration'})
cfg=json.loads((root/'.codex-linkedin.local.json').read_text());cfg.update(resume_root=Path(cfg['resume_root']),python=Path(cfg['python']))
provider=CodexProvider(CodexConfig(**cfg),e/'attempts','essential-checks-evaluation-20261105')
for label,source in [('retained-security','security-repeat-1.json'),('unsupported-negative','deliberately-unsupported-negative.json')]:
 f=e/(label+'.json')
 if f.exists():
  assert json.loads(f.read_text())['state']=='completed';continue
 old=json.loads((root/'evidence/scoring-audit-20261105'/source).read_text())
 record={'state':'running','post':old['post'],'request_context':old['request_context'],
         'persona_context':old['persona_context'],'negative_fixture':label=='unsupported-negative',
         'source_record':str(Path('evidence/scoring-audit-20261105')/source),
         'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
         'working_tree_patch_sha256':hashlib.sha256(subprocess.check_output(['git','diff'],cwd=root)).hexdigest()}
 save(f,record)
 class Capture:
  def call(self,system,user,response_json=True):
   record.update(system=system,user=user);save(f,record)
   out=LLMClient(model=cfg['model'],provider=provider).call(system,user,response_json=response_json)
   if provider.error:raise provider.error
   record['raw']=out['text'];return out
 req=old['request_context']
 result=assess_publish_quality(text=old['post'],audience=req['audience'],content_goal='authority',
       evidence=req['evidence'],persona_profile=old['persona_context'],client=Capture())
 record.update(state='completed',assessment=result.as_dict(),receipts=provider.receipts[-1:])
 save(f,record);print(label,result.score,result.review_status,flush=True)

