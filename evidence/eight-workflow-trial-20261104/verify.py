"""Read-only packet verification. No credentials, provider, imports from app, or model calls."""
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
manifest=json.loads((p/'FILES.sha256.json').read_text())
for name,digest in manifest.items():assert h(p/name)==digest,name
attempts={}
threads=[]
for f in (p/'attempts').rglob('attempt.json'):
 a=json.loads(f.read_text());assert a['state']=='succeeded',(str(f),a['state'])
 for name in ['request','result']:assert h(f.with_name(name+'.json'))==a[name+'_sha256'],str(f)
 assert a['attempt_id'] not in attempts;a['packet_path']=str(f.relative_to(p));attempts[a['attempt_id']]=a
 threads.extend(ev['thread_id'] for ev in a['events'] if ev['type']=='thread.started')
assert len(threads)==len(attempts)==len(set(threads))
stages=0
for f in p.glob('*.json'):
 d=json.loads(f.read_text())
 if isinstance(d,dict) and 'raw' in d and 'receipts' in d:
  assert d['state']=='completed',f.name
  for receipt in d['receipts']:
   a=attempts[receipt['attempt_id']]
   result=json.loads((p/a['packet_path']).with_name('result.json').read_text())
   assert result['text']==d['raw'],f.name
   assert receipt['result_sha256']==a['result_sha256'],f.name
  stages+=1
for n in range(1,9):assert json.loads((p/f'route-{n}.json').read_text())['status']=='DRAFTED'
assert stages==len(attempts),(stages,len(attempts))
for name in ['review-mapping.json','second-review-mapping.json']:
 m=json.loads((p/name).read_text());assert len(m)==len(set(m.values()))
print(json.dumps({'status':'PASS','manifest_files':len(manifest),'native_attempts':len(attempts),'unique_threads':len(set(threads)),'stage_raw_receipts_verified':stages,'routes':8,'model_calls_from_verifier':0}))
