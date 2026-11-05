from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name,digest in json.loads((p/'FILES.sha256.json').read_text()).items():assert h(p/name)==digest,name
a=json.loads((p/'ARITHMETIC.json').read_text())
assert (a['all_strong_4'],a['all_exceptional_5'],a['ceiling_if_novelty_emotion_shareability_stay_3'])==(80,100,87)
rows=json.loads((p/'COHORT.json').read_text());assert len(rows)==19 and all(x['score']==x['recomputed'] for x in rows)
attempts={}
for f in (p/'attempts').rglob('attempt.json'):
 d=json.loads(f.read_text());assert d['state']=='succeeded'
 for name in ['request','result']:assert h(f.with_name(name+'.json'))==d[name+'_sha256'],str(f)
 attempts[d['attempt_id']]=(f,d)
assert len(attempts)==6
cached=0
for f in p.glob('*.json'):
 d=json.loads(f.read_text())
 if not isinstance(d,dict) or 'assessment' not in d:continue
 assert d['state']=='completed'
 for receipt in d['receipts']:
  cached+=bool(receipt.get('cache_hit'))
  native,meta=attempts[receipt['attempt_id']]
  assert json.loads(native.with_name('result.json').read_text())['text']==d['raw'],f.name
for name in ['security','ai']:
 first=json.loads((p/(name+'-repeat-1.json')).read_text());fresh=json.loads((p/(name+'-independent-repeat.json')).read_text())
 assert (first['system'],first['user'])==(fresh['system'],fresh['user'])
 assert first['receipts'][0]['attempt_id']!=fresh['receipts'][0]['attempt_id']
 assert not fresh['receipts'][0]['cache_hit']
assert cached==2
print(json.dumps({'status':'PASS','historical_totals_recomputed':19,'unique_native_executions':6,'cached_reads_distinguished':2,'independent_same_input_comparisons':2,'runtime_policy_changed':False}))
