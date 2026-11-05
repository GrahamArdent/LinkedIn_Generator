from pathlib import Path
import json,hashlib,re
p=Path(__file__).resolve().parent;root=p.parents[1];installed=Path('/home/graham/work/linkedin-generator-releases/2c2daf39398a993b698d1f225008a06217b14a7c')
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name,digest in json.loads((p/'FILES.sha256.json').read_text()).items():assert h(p/name)==digest,name
manifest=json.loads((p/'manifest.json').read_text());assert manifest['kind']=='controlled_first_drafting_stage_only' and len(manifest['prepared'])==2
assert len({x['non_style_context_sha256'] for x in manifest['prepared']})==1
for name,digest in manifest['code_config_hashes'].items():assert h(installed/name)==digest,name
attempts={json.loads(f.read_text())['attempt_id']:f for f in (p/'codex-attempts').rglob('attempt.json')};assert len(attempts)==2
for style in ['concise_challenger','reflective_leader']:
 d=json.loads((p/(style+'.json')).read_text());assert d['state']=='completed' and d['human_decision'] is None
 assert hashlib.sha256(d['body'].encode()).hexdigest()==d['content_sha256']
 assert d['prepared']['request']['persona_key']=='graham' and not d['prepared']['request']['services']
 receipt=d['provider_receipts'][0];assert receipt['ok'] and not receipt['cache_hit']
 f=attempts[receipt['attempt_id']];a=json.loads(f.read_text());assert a['state']=='succeeded'
 for key in ['request','result']:assert h(f.with_name(key+'.json'))==a[key+'_sha256']
 assert json.loads(f.with_name('final.json').read_text())['text']==d['body']
reopen=json.loads((p/'REOPEN.json').read_text());assert reopen['exit']==0 and reopen['new_model_calls']==0 and reopen['saved_style_manifest_attempt_hashes_unchanged']
b=json.loads(next((p/'codex-attempts').rglob('budget.json')).read_text());assert b['model_execution_slots']==2 and b['launches']==6 and b['active_seconds']<=900 and b['in_flight'] is None
calendar=json.loads((p/'GRAHAM_CALENDAR_RECOVERY.json').read_text());assert calendar['row_count']==len(calendar['rows'])==48
ref=json.loads((p/'DECISIONS.json').read_text());assert ref['chat_reference']['utf8_sha256']==h(p/'CHAT_REFERENCE.md')
spec=(root/'docs/implementation/v4/LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md').read_text();assert len(set(re.findall(r'\*\*AT-(\d\d)\*\*',spec)))==26 and len(set(re.findall(r'\*\*E2E-(\d\d)\*\*',spec)))==11
print(json.dumps({'status':'PASS','scope':'Graham only','raw_installed_drafts':2,'model_executions':2,'cli_starts':6,'reopen_calls':0,'calendar_ideas':48,'AT':26,'E2E':11,'human_acceptance':'pending'}))
