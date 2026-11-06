from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[3];folder=Path(__file__).resolve().parent
d=json.loads((folder/'HISTORY.json').read_bytes());native=json.loads((folder/'CANONICAL_READBACK.json').read_bytes())
def check(rows):
 assert len(rows)==10 and len({r['request_id'] for r in rows})==10,'missing original trial'
 assert [r['started_at_utc'] for r in rows]==sorted(r['started_at_utc'] for r in rows),'order'
 for r in rows:
  raw=json.loads((root/r['source']).read_bytes())
  assert raw['input']['request_id']==r['request_id'] and raw['started_at_utc']==r['started_at_utc'] and raw['engine_gate']==r['engine_gate']
 assert [r['request_id'] for r in rows]==[r['id'] for r in native['rows']]
 for x,y in zip(rows,native['rows']):assert x['started_at_utc']==y['started'] and x['engine_gate']==y['gate']
def integrity(raw,wanted):assert hashlib.sha256(raw).hexdigest()==wanted,'source changed'
check(d['rows'])
for name,h in d['source_sha256'].items():integrity((root/name).read_bytes(),h)
assert native['legacy_records_verified']==10 and native['jobs_unchanged'] and native['new_model_effects']==0 and not native['pending_stages']
assert native['model_stages_before']==native['model_stages_after']==17
try:check(d['rows'][1:])
except AssertionError:missing=True
else:raise AssertionError('missing negative failed')
name,wanted=next(iter(d['source_sha256'].items()));raw=(root/name).read_bytes()
try:integrity(bytes([raw[0]^1])+raw[1:],wanted)
except AssertionError:altered=True
else:raise AssertionError('altered negative failed')
result={'status':'PASS','original_trials':10,'exact_source_files':len(d['source_sha256']),'original_canonical_bindings_verified':10,'missing_trial_rejected':missing,'altered_source_rejected':altered,'no_model_dispatch':True,'scope':'Declared original record/source chronology and bytes; not eligible subject count or human acceptance'}
(folder/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
