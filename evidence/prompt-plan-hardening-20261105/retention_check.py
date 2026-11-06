from pathlib import Path
import hashlib,json,subprocess,copy
p=Path(__file__).resolve().parent;root=p.parents[1]
EXPECTED=['objective', 'one_spine', 'planning_boundary', 'author', 'broad_topics', 'credentials', 'five_beats', 'alternatives', 'meaning', 'contract_bounds', 'normal_route', 'no_model_prepare', 'immutable_binding', 'actual_consumers', 'four_essentials', 'construction', 'feedback_version1', 'feedback_chat', 'old_reference', 'security_rejection', 'calendar', 'installed_identity', 'reuse', 'local_release', 'approval_ci', 'rollback', 'idempotency', 'unknown', 'budget', 'baseline', 'visual', 'human', 'transfer', 'history', 'full_acceptance', 'later_scope', 'retention', 'currentness', 'stopping', 'packet', 'mandatory_preparation', 'template_grounding', 'template_modec', 'template_environment', 'template_jit', 'template_recommendation', 'template_capture', 'template_lanes', 'template_surfaces', 'template_cost', 'template_handoff', 'template_resume', 'template_wait', 'template_autofix', 'template_adversarial', 'template_checklist', 'template_learning', 'template_governance', 'template_research', 'ownership', 'later_calibration', 'pilot_threshold', 'no_background_claim', 'review_binding', 'current_builder_challenge_request', 'execution_request', 'qualified_source_outcome', 'installed_target_outcome', 'native_human_checkpoint', 'self_operating_request', 'audit_inputs', 'audit_registry', 'audit_legacy', 'audit_docs', 'audit_dependencies', 'audit_feedback', 'draft_b_preference', 'symbolism_adopted', 'engine_frozen', 'positive_self_operation', 'truthful_insufficient', 'sequencing_correction', 'registry_global', 'stable_data_backup', 'stage_original_recovery', 'legacy_import', 'research_outsidechat', 'research_positive_admission', 'url_source_safety', 'meaning_autonomous', 'runtime_reproducible', 'economical_model', 'budget_total', 'normal_entry', 'typed_status', 'feedback_persistence', 'edit_invalidation', 'explicit_voice_activation', 'selected_export', 'shared_ui', 'entry_coverage', 'real_independent_acceptance', 'quality_transfer', 'real_docs_handoff', 'renderer_boundary', 'publisher_boundary', 'completion_levels', 'prompt_standalone_proof', 'prompt_continue_independent']
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
 for entry in json.loads((p/'OPERATIONAL_SOURCE_SET.json').read_text())['files']:
  data=subprocess.check_output(['git','show',entry['revision']+':'+entry['path']],cwd=root);check_bytes(data,entry)
 count=check_inventory(inventory['items'])
 try:check_inventory(inventory['items'][1:])
 except AssertionError:missing=True
 else:raise AssertionError('missing-item negative not rejected')
 entry=source['files'][0];data=subprocess.check_output(['git','show',entry['revision']+':'+entry['path']],cwd=root);altered=bytes([data[0]^1])+data[1:]
 try:check_bytes(altered,entry)
 except AssertionError:changed=True
 else:raise AssertionError('altered-byte negative not rejected')
 result={'status':'PASS','covered':count,'total':len(EXPECTED),'baseline_files_verified':len(source['files']), 'operational_source_files_verified':len(json.loads((p/'OPERATIONAL_SOURCE_SET.json').read_text())['files']),'missing_item_rejected':missing,'same_length_altered_byte_rejected':changed,'scope':inventory['audited_source_set'],'proof_limit':'Deterministic source/anchor retention only; semantic review required separately; not implementation or universal coverage'}
 (p/'RETENTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
