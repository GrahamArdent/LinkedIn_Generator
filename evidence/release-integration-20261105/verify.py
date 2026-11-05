from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name,digest in json.loads((p/'FILES.sha256.json').read_text()).items():assert h(p/name)==digest,name
review=json.loads((p/'REVIEW.json').read_text());root=p.parents[1]
if (root/'src/app').is_dir():
 for f in review['files']:assert h(root/f['path'])==f['sha256'],f['path']
i=json.loads((p/'INSTALLATION.json').read_text());m=json.loads((p/'MERGE.json').read_text())
assert m['merged'] and m['merge_commit']==i['merged_revision']==i['installed_revision']=='0c099d70fc807044355af089d62d1bef049cbb95'
assert i['native_attempts_before']==i['native_attempts_after']==109 and i['native_attempt_hashes_unchanged']
assert i['new_model_calls']==i['api_spend']==0
assert '230 passed' in i['installed_tests']
assert i['saved_result_observed']['engine_gate']==i['saved_result_expected']['engine_gate']
assert i['module_imports']['request_handoff']
print(json.dumps({'status':'PASS','reviewed_files':len(review['files']),'merged_revision':m['merge_commit'],'installed_revision':i['installed_revision'],'tests':230,'new_model_calls':0}))
