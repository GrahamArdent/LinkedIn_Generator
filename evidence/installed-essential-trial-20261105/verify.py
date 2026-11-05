from pathlib import Path
import hashlib,json,re
p=Path(__file__).resolve().parent;root=p.parents[1]
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for folder in [p,root/'evidence/release-essential-20261105']:
 for name,digest in json.loads((folder/'FILES.sha256.json').read_text()).items():assert h(folder/name)==digest,name
d=json.loads((p/'trial/trial.json').read_text());e=d['engine'];candidate=e['selected_candidate'];v=e['visual_asset'];reopen=json.loads((p/'REOPEN.json').read_text());resources=json.loads((p/'RESOURCE_USE.json').read_text())
assert d['state']=='completed' and d['engine_gate']=='QUALIFIED_FOR_HUMAN_REVIEW' and d['human_decision'] is None
assert candidate['content_sha256']==hashlib.sha256(candidate['body'].encode()).hexdigest()==v['source_content_sha256']
assert e['review']['policy_version']=='essential-checks-v1' and not e['review']['rewrite_triggered']
assert all(x['verdict']=='pass' and x['reason'] for x in e['review']['original']['essential_checks'].values())
assert e['review']['human_approval']=='pending' and v['review_required'] is True
assert d['baseline']['user']['editorial_handoff']==d['input']['editorial_handoff']
assert d['baseline']['user']['source_bundle']==d['evidence_bundle']
assert e['review']['evaluation_context']['writing_voice']==d['baseline']['user']['voice']['writing_voice']
assert reopen['exit']==0 and reopen['all_trial_file_hashes_unchanged'] and reopen['model_calls_added']==0 and reopen['trial_sha256']==h(p/'trial/trial.json')
assert resources['actual_model_executions']==6<=12 and resources['actual_cli_launches']==18 and resources['cumulative_active_cli_seconds']<=900
attempts={json.loads(f.read_text())['attempt_id']:f for f in (p/'trial').rglob('attempt.json')}
assert len(attempts)==len(d['provider_receipts'])==6
for receipt in d['provider_receipts']:
 f=attempts[receipt['attempt_id']];a=json.loads(f.read_text());assert a['state']=='succeeded' and receipt['cache_hit'] is False
 for key in ['request','result']:assert h(f.with_name(key+'.json'))==a[key+'_sha256']
freeze=json.loads((p/'CALIBRATION_FREEZE.json').read_text())['examples'];assert len(freeze)==12
assert not ({x['subject_group'] for x in freeze if x['partition']=='calibration'} & {x['subject_group'] for x in freeze if x['partition']=='holdout'})
assert all(x['human_label'] is None and hashlib.sha256(x['body'].encode()).hexdigest()==x['content_sha256'] for x in freeze)
spec=(root/'docs/implementation/v4/LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md').read_text();assert len(set(re.findall(r'\*\*AT-(\d\d)\*\*',spec)))==26 and len(set(re.findall(r'\*\*E2E-(\d\d)\*\*',spec)))==11
print(json.dumps({'status':'PASS','live_executions':6,'AT':26,'E2E':11,'human_acceptance':'pending','fresh_reopen_calls':0,'installed':'2c2daf39398a993b698d1f225008a06217b14a7c'}))
