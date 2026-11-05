"""Promote one reviewed merged revision through the existing local launcher."""
from pathlib import Path
import subprocess,json,hashlib,os,shutil,tempfile,sys
repo=Path('/home/graham/work/linkedin-codex-trial-20261104')
e=repo/'evidence/release-integration-20261105'
merged='0c099d70fc807044355af089d62d1bef049cbb95'
previous='93a9ee3ae85a5f3fcb35ea3cda4d5d44c553809a'
releases=Path('/home/graham/work/linkedin-generator-releases');releases.mkdir(exist_ok=True)
launcher=Path('/home/graham/.local/bin/linkedin-codex')
backup=releases/'rollback-20261105';backup.mkdir(exist_ok=True)
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def run(args,**kwargs):
 r=subprocess.run([str(a) for a in args],capture_output=True,text=True,**kwargs)
 if r.returncode:raise RuntimeError(f"COMMAND_FAILED {args}: "+(r.stdout+r.stderr)[-1800:])
 return r
subprocess.run(['git','-C',str(repo),'fetch','origin','main'],check=True)
assert run(['git','-C',repo,'rev-parse','origin/main']).stdout.strip()==merged
before={str(f.relative_to(repo)):h(f) for f in (repo/'evidence').rglob('attempt.json')}
original=launcher.read_bytes()
(backup/'original-launcher.sh').write_bytes(original)
def release(sha):
 target=releases/sha
 if not target.exists():run(['git','-C',repo,'worktree','add','--detach',target,sha])
 assert run(['git','-C',target,'rev-parse','HEAD']).stdout.strip()==sha
 assert not run(['git','-C',target,'diff','--name-only']).stdout.strip()
 v=target/'.venv'
 if not v.exists():v.symlink_to(repo/'.venv',target_is_directory=True)
 config=target/'.codex-linkedin.local.json'
 if config.exists():assert h(config)==h(repo/'.codex-linkedin.local.json')
 else:shutil.copy2(repo/'.codex-linkedin.local.json',config)
 return target
old=release(previous);new=release(merged)
old_text=original.decode().replace('lig_checkout='+str(repo),'lig_checkout='+str(old))
new_text=original.decode().replace('lig_checkout='+str(repo),'lig_checkout='+str(new))
assert old_text!=original.decode() and new_text!=original.decode()
rollback=backup/'rollback-launcher.sh';rollback.write_text(old_text);rollback.chmod(0o755)
(e/'PROMOTION_INTENT.json').write_text(json.dumps({'merged':merged,'previous':previous,'new_release':str(new),'rollback_release':str(old),'launcher':str(launcher),'prior_launcher_sha256':hashlib.sha256(original).hexdigest(),'new_launcher_sha256':hashlib.sha256(new_text.encode()).hexdigest(),'rollback_launcher':str(rollback)},indent=2)+'\n')
# Test target before activation, with the existing qualified dependency environment.
test=run([new/'.venv/bin/python','-m','pytest','-q'],cwd=new)
(e/'installed-pytest.log').write_text(test.stdout+test.stderr)
cfg=json.loads((new/'.codex-linkedin.local.json').read_text())
assert run(['git','-C',cfg['resume_root'],'rev-parse','HEAD']).stdout.strip()==cfg['source_sha']
assert not run(['git','-C',cfg['resume_root'],'status','--porcelain','--','v6_nextjs_migration/backend/app/services/codex_cli_client.py','v6_nextjs_migration/backend/app/services/run_records.py','v6_nextjs_migration/backend/app/settings.py']).stdout.strip()
auth=run(['/usr/local/bin/codex','login','status'])
assert 'chatgpt' in (auth.stdout+auth.stderr).lower()
version=run(['/usr/local/bin/codex','--version']).stdout.strip()
# Atomic replacement preserves the existing command and leaves the previous runtime intact.
temporary=launcher.with_name(launcher.name+'.promoting')
temporary.write_text(new_text);temporary.chmod(0o755);os.replace(temporary,launcher)
assert h(launcher)==hashlib.sha256(new_text.encode()).hexdigest()
saved=repo/'evidence/codex-first-20261104/trial'
expected=json.loads((saved/'trial.json').read_text())
show=run([launcher,'show','--out',saved]);observed=json.loads(show.stdout)
assert observed['state']==expected['state']=='completed'
assert observed['engine_gate']==expected['engine_gate']=='HOLD_NO_QUALIFIED_CANDIDATE'
run([launcher,'--help'])
# Rollback target is usable without switching the active launcher.
rollback_show=run([rollback,'show','--out',saved])
assert json.loads(rollback_show.stdout)['state']=='completed'
imports=run([new/'.venv/bin/python','-c','import json,src.app.api as a,src.app.contracts as c,src.app.integration as i; print(json.dumps({"api":a.__file__,"contracts":c.__file__,"integration":i.__file__,"request_handoff":"editorial_handoff" in c.LinkedInContentRequest.model_fields}))'],cwd=new)
modules=json.loads(imports.stdout)
assert all(str(new) in modules[k] for k in ['api','contracts','integration'])
assert modules['request_handoff']
after={str(f.relative_to(repo)):h(f) for f in (repo/'evidence').rglob('attempt.json')}
assert before==after
receipt={'status':'GO','merged_revision':merged,'installed_revision':run(['git','-C',new,'rev-parse','HEAD']).stdout.strip(),'installed_root':str(new),'launcher':str(launcher),'launcher_sha256':h(launcher),'rollback_root':str(old),'rollback_launcher':str(rollback),'rollback_command':'install -m 755 '+str(rollback)+' '+str(launcher),'original_launcher_backup':str(backup/'original-launcher.sh'),'installed_tests':test.stdout.strip(),'module_imports':modules,'codex_version':version,'codex_auth':'ChatGPT login status PASS; no credentials retained','resume_client_sha':cfg['source_sha'],'saved_result_expected':{'state':'completed','engine_gate':'HOLD_NO_QUALIFIED_CANDIDATE'},'saved_result_observed':observed,'rollback_saved_result_smoke':'PASS without activation','native_attempts_before':len(before),'native_attempts_after':len(after),'native_attempt_hashes_unchanged':True,'new_model_calls':0,'api_spend':0,'hosted_ci':False,'publishing':False}
(e/'INSTALLATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
(releases/'INSTALLATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
