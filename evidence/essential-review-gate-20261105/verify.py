from pathlib import Path
import hashlib,json,re,sys
p=Path(__file__).resolve().parent
root=p.parents[1]
sys.path.insert(0,str(root))
from src.app.publish_quality import essential_review_status, _weighted_score
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name,digest in json.loads((p/'FILES.sha256.json').read_text()).items():
    assert h(p/name)==digest,name
for name,digest in json.loads((p/'TESTED_SOURCE_HASHES.json').read_text()).items():
    assert h(root/name)==digest,name
attempts={}
for f in (p/'attempts').rglob('attempt.json'):
    d=json.loads(f.read_text());assert d['state']=='succeeded'
    for name in ['request','result']:
        assert h(f.with_name(name+'.json'))==d[name+'_sha256'],str(f)
    attempts[d['attempt_id']]=(f,d)
assert len(attempts)==2
for label,expected in [('retained-security','reviewable'),('unsupported-negative','needs_evidence')]:
    d=json.loads((p/(label+'.json')).read_text())
    assert d['state']=='completed'
    assert json.loads(d['user'])['post']==d['post']
    assert essential_review_status(d['assessment']['essential_checks'])==expected
    assert _weighted_score(d['assessment']['dimensions'])==d['assessment']['score']
    receipt=d['receipts'][0];assert receipt['cache_hit'] is False
    native,_=attempts[receipt['attempt_id']]
    assert json.loads(native.with_name('result.json').read_text())['text']==d['raw']
    assert json.loads(d['raw'])['essential_checks']==d['assessment']['essential_checks']
resource=json.loads((p/'RESOURCE_USE.json').read_text())
assert resource['subscription_evaluations']==2 and resource['active_cli_seconds']<=900 and resource['api_spend']==0
audit=json.loads((p/'ACCEPTANCE_AUDIT.json').read_text())
assert len(audit['acceptance_objectives'])==26 and len(audit['e2e_scenarios'])==11
spec=(root/'docs/implementation/v4/LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md').read_text()
assert set(re.findall(r'\*\*AT-(\d\d)\*\*',spec))=={f'{i:02}' for i in range(1,27)}
assert set(re.findall(r'\*\*E2E-(\d\d)\*\*',spec))=={f'{i:02}' for i in range(1,12)}
print(json.dumps({'status':'PASS','native_executions':2,'tested_source_hashes':'match','AT':26,'E2E':11,'installed':False}))
