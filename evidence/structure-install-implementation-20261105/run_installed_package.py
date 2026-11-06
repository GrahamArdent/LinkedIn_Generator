"""Evidence driver: calls installed public commands only; never edits generated text."""
from pathlib import Path
import json,subprocess,time
P=Path(__file__).resolve().parent
LAUNCHER='/home/graham/.local/bin/linkedin-codex'
admission=json.loads((P/'ADMISSION.json').read_text())
assert admission['max_model_executions']==12 and admission['api_spend']==0
spent=sum(x['seconds'] for x in json.loads((P/'INSTALLATION.json').read_text())['preflight'])
commands=[]
def run(args,name):
 global spent
 start=time.monotonic()
 try:r=subprocess.run([LAUNCHER,*args],text=True,capture_output=True,timeout=max(1,900-spent))
 except subprocess.TimeoutExpired:
  spent+=time.monotonic()-start
  (P/'COMMANDS.json').write_text(json.dumps({'commands':commands,'active_wall_envelope_seconds':spent,'status':'UNKNOWN_TIMEOUT_RECONCILE_ORIGINAL'},indent=2)+'\n')
  raise
 elapsed=time.monotonic()-start;spent+=elapsed
 (P/name).write_text(r.stdout+r.stderr)
 commands.append({'args':args,'exit_code':r.returncode,'wall_seconds':elapsed})
 (P/'COMMANDS.json').write_text(json.dumps({'commands':commands,'active_wall_envelope_seconds':spent},indent=2)+'\n')
 print(name, r.returncode, round(elapsed,3),flush=True)
 return r
r=run(['prepare','--request',str(P/'input-request.json'),'--evidence-bundle',str(P/'input-source-bundle.json'),'--out',str(P/'prepared')],'installed-prepare.log')
assert r.returncode==0,r.stderr
trial=P/'trial'
if (trial/'trial.json').exists():
 raise RuntimeError('RECONCILE_EXISTING_TRIAL; this driver must not restart an existing package')
args=['generate','--request',str(P/'prepared/request.json'),'--evidence-bundle',str(P/'prepared/source-bundle.json'),'--out',str(trial),'--score-baseline']
r=run(args,'installed-generate.log')
if r.returncode:
 old=json.loads((trial/'trial.json').read_text()) if (trial/'trial.json').exists() else {}
 if old.get('state')=='failed' and old.get('error_code')=='NO_QUALIFIED_CANDIDATE':
  # Known failed selection, original engine retained. Only the already-admitted control is finished.
  args[0]='complete-comparison'
  r=run(args,'installed-comparison-continuation.log')
assert r.returncode==0,r.stderr
print('Installed package completed; human judgment pending',flush=True)
