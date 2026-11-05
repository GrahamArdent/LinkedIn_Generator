"""Verify this evidence packet offline without credentials or provider calls."""
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
read=lambda f:json.loads(f.read_text())
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name,digest in read(p/'FILES.sha256.json').items():assert h(p/name)==digest,name
attempts={};threads=[]
for f in (p/'attempts').rglob('attempt.json'):
 a=read(f);assert a['state']=='succeeded',str(f)
 for name in ['request','result']:assert h(f.with_name(name+'.json'))==a[name+'_sha256'],str(f)
 assert a['attempt_id'] not in attempts
 attempts[a['attempt_id']]=(f,a)
 threads.extend(e['thread_id'] for e in a['events'] if e['type']=='thread.started')
stages=0
for f in p.glob('*.json'):
 d=read(f)
 if isinstance(d,dict) and 'raw' in d and 'receipts' in d:
  assert d['state']=='completed',f.name
  for receipt in d['receipts']:
   path,a=attempts[receipt['attempt_id']]
   assert read(path.with_name('result.json'))['text']==d['raw'],f.name
   assert receipt['result_sha256']==a['result_sha256'],f.name
  stages+=1
assert stages==len(attempts)==len(set(threads))==6
admission=read(p/'ADMISSION.json')
root=p.parents[1]
if (root/'src/app').is_dir():
 for name,digest in read(p/'RECOVERY_ADMISSION.json')['source_hashes'].items():assert h(root/name)==digest,name
writers=[]
for form,label in [('literal','literal'),('symbolic','symbolic-recovery')]:
 handoff=read(p/(label+'-handoff.json'))
 assert handoff['meaning']==admission['meaning']
 assert handoff['narrative']==admission['narratives'][form]
 assert handoff['writing_plan']==json.loads(read(p/(label+'-plan.json'))['raw'])
 assert all(len(b['delivery'])<=240 for b in handoff['writing_plan']['beats'])
 writer=read(p/(label+'-draft.json'))
 profile_line=next(s for s in writer['user'].splitlines() if s.startswith('Persona Profile: '))
 profile=json.loads(profile_line.split(': ',1)[1])
 assert profile['editorial_context']['handoff']==handoff
 assert profile['writing_voice']==admission['voice']
 assert profile['active_author_pov']=='individual'
 # Compare the actual consumer contexts after removing only the intended treatment.
 profile['editorial_context']['handoff'].pop('narrative')
 profile['editorial_context']['handoff'].pop('writing_plan')
 writers.append((writer['system'],profile,[s for s in writer['user'].splitlines() if not s.startswith('Persona Profile: ')]))
assert writers[0]==writers[1],'unintended non-narrative input difference'
assert read(p/'symbolic-outcome.json')['status']=='HOLD'
assert read(p/'symbolic-recovery-outcome.json')['status']=='DRAFTED'
bad=json.loads(read(p/'symbolic-plan.json')['raw'])
assert any(len(b['delivery'])>240 for b in bad['beats'])
assert read(p/'REPLAY.json')['added_model_calls']==0
print(json.dumps({'status':'PASS','native_attempts':len(attempts),'unique_threads':len(set(threads)),'exact_raw_receipts':stages,'writer_non_narrative_context_equal':True,'selected_narrative_preserved':True,'initial_hold_retained':True,'model_calls_from_verifier':0}))
