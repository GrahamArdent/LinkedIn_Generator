from pathlib import Path
import hashlib,json,subprocess
p=Path(__file__).resolve().parent;root=p.parents[1]
ITEMS=[
 ('execution_request','CURRENT_WORK_PACKET.md','Continued merge/install/testing/applicable-CI authority persists'),
 ('model_decision','docs/implementation/v4/LINKEDIN_CODEX_QUICKSTART.md','GPT-6 SOL medium'),
 ('ordinary_create','docs/implementation/v4/LINKEDIN_CODEX_QUICKSTART.md','linkedin-codex create'),
 ('original_history','evidence/operational-implementation-20261106/REPORT.md','10 historical trials'),
 ('original_b','CURRENT_WORK_PACKET.md','Preserve original B'),
 ('failed_originals','evidence/operational-implementation-20261106/REPORT.md','653-character fact'),
 ('shared_admissions','evidence/operational-implementation-20261106/REPORT.md','inherited original start/usage/caps'),
 ('source_scope','evidence/operational-implementation-20261106/REPORT.md','Broader novel-topic Crossref coverage is limited'),
 ('native_receipts','evidence/operational-implementation-20261106/REPORT.md','72.209'),
 ('browser_proof','evidence/operational-implementation-20261106/NATIVE_BROWSER_FINAL.json','"new_model_calls": 0'),
 ('replay_proof','evidence/operational-implementation-20261106/NATIVE_REPLAY.json','"all_attempt_artifact_bytes_unchanged": true'),
 ('backup','evidence/operational-implementation-20261106/NATIVE_BACKUP_RELOCATION.json','"jobs": 14'),
 ('runtime','evidence/operational-implementation-20261106/ISOLATED_RUNTIME_GUARD.json','"status": "PASS"'),
 ('human_gate','CURRENT_WORK_PACKET.md','R5 actual human-approved example lifecycle'),
 ('full_acceptance','evidence/operational-implementation-20261106/ACCEPTANCE_AUDIT.json','"all_marks_hit": false'),
 ('clock_feedback_received','evidence/operational-implementation-20261106/q6-transfer/HUMAN_FEEDBACK.json','Liked the clock comparison; found it fun'),
 ('q6_existing_group','evidence/operational-implementation-20261106/q6-transfer/ADMISSION.json','ai-time-to-usable-completion'),
 ('q6_budget_declared','evidence/operational-implementation-20261106/q6-transfer/ADMISSION.json','"max_model_executions": 12'),
 ('q6_native_outcome','evidence/operational-implementation-20261106/q6-transfer/OUTCOME.json','GO_MACHINE_TRANSFER_HUMAN_REVIEW_PENDING'),
 ('q6_immutable_replay','evidence/operational-implementation-20261106/q6-transfer/REPLAY.json','"all_original_attempt_bytes_unchanged": true'),
 ('q6_human_remaining','CURRENT_WORK_PACKET.md','Graham disposition of the saved parcel candidate'),
 ('merged_composition','evidence/operational-implementation-20261106/MERGED_COMPOSITION.json','29dff9be405b568483d3f69da20e2831ca40190e'),
 ('render_publish_gate','CURRENT_WORK_PACKET.md','R8 rendering/Dedication publishing stays gated'),
 ('parcel_critique','CURRENT_WORK_PACKET.md','too short, bland, does not capture enough'),
 ('editorial_deferral','CURRENT_WORK_PACKET.md','address the draft later'),
 ('source_negatives','evidence/operational-implementation-20261106/r2-discovery/REPORT.md','These negative receipts remain'),
 ('source_proof_limit','evidence/operational-implementation-20261106/r2-discovery/REPORT.md','not general research coverage'),
 ('feed_not_facts','docs/implementation/v4/CODEX_FIRST_TRIAL_GAME_PLAN_2026-11-04.md','feed snippets are never facts'),
]
def check(items):
 assert len(items)==len(ITEMS) and {i[0] for i in items}=={i[0] for i in ITEMS},'missing item'
 for key,path,literal in items:assert literal in (root/path).read_text(),key
 return len(items)
def verify(raw,wanted):assert hashlib.sha256(raw).hexdigest()==wanted,'changed source bytes'
subprocess.run(['python3',str(root/'evidence/prompt-plan-hardening-20261105/retention_check.py')],cwd=root,check=True,capture_output=True)
count=check(ITEMS);manifest=json.loads((p/'QUALIFIED_MANIFEST.json').read_text())
for path,wanted in manifest.items():verify((root/path).read_bytes(),wanted)
try:check(ITEMS[1:])
except AssertionError:missing=True
else:raise AssertionError('missing negative not rejected')
path,wanted=next((k,v) for k,v in manifest.items() if (root/k).stat().st_size);raw=(root/path).read_bytes();altered=bytes([raw[0]^1])+raw[1:]
try:verify(altered,wanted)
except AssertionError:changed=True
else:raise AssertionError('changed-byte negative not rejected')
result={'status':'PASS','known_original_requirements':109,'execution_checkpoint_requirements':count,'declared_total':109+count,'declared_covered':109+count,'qualified_files':len(manifest),'original_baseline_files':22,'original_current_source_files':19,'missing_item_rejected':missing,'altered_byte_rejected':changed,'proof_limit':'Enumerated known obligations, original source snapshots and exact qualified files only. Not universal completeness, human acceptance, or release execution.'}
(p/'RETENTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
