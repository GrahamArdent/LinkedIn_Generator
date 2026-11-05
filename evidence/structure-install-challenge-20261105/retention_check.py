from pathlib import Path
import hashlib,json,subprocess,copy
p=Path(__file__).resolve().parent;root=p.parents[1]
EXPECTED=['objective', 'one_spine', 'planning_boundary', 'author', 'broad_topics', 'credentials', 'five_beats', 'alternatives', 'meaning', 'contract_bounds', 'normal_route', 'no_model_prepare', 'immutable_binding', 'actual_consumers', 'four_essentials', 'construction', 'feedback_version1', 'feedback_chat', 'old_reference', 'security_rejection', 'calendar', 'installed_identity', 'reuse', 'local_release', 'approval_ci', 'rollback', 'idempotency', 'unknown', 'budget', 'baseline', 'visual', 'human', 'transfer', 'history', 'full_acceptance', 'later_scope', 'retention', 'currentness', 'stopping', 'packet', 'mandatory_preparation']
h=lambda data:hashlib.sha256(data).hexdigest()
def check_inventory(items):
 assert len(items)==len(EXPECTED) and {x['id'] for x in items}==set(EXPECTED),'missing/duplicate requirement'
 for x in items:
  loc=x['location'];assert loc['literal'] in (root/loc['path']).read_text(),x['id']
 return len(items)
def check_bytes(data,entry):
 assert len(data)==entry['bytes'] and h(data)==entry['sha256'],'baseline byte mismatch'
def main():
 source=json.loads((p/'SOURCE_SET.json').read_text());inventory=json.loads((p/'RETENTION_INVENTORY.json').read_text())
 for entry in source['files']:
  data=subprocess.check_output(['git','show',entry['revision']+':'+entry['path']],cwd=root);check_bytes(data,entry)
 count=check_inventory(inventory['items'])
 try:check_inventory(inventory['items'][1:])
 except AssertionError:missing=True
 else:raise AssertionError('missing-item negative not rejected')
 entry=source['files'][0];data=subprocess.check_output(['git','show',entry['revision']+':'+entry['path']],cwd=root);altered=bytes([data[0]^1])+data[1:]
 try:check_bytes(altered,entry)
 except AssertionError:changed=True
 else:raise AssertionError('altered-byte negative not rejected')
 result={'status':'PASS','covered':count,'total':len(EXPECTED),'baseline_files_verified':len(source['files']),'missing_item_rejected':missing,'same_length_altered_byte_rejected':changed,'scope':inventory['audited_source_set'],'proof_limit':'Deterministic source/anchor retention only; semantic review required separately; not implementation or universal coverage'}
 (p/'RETENTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
