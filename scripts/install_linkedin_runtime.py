#!/usr/bin/env python3
"""Build an isolated candidate runtime. Does not promote a launcher or modify the client owner."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def run(*args,**kwargs):return subprocess.run(args,check=True,**kwargs)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--runtime-root',required=True,type=Path)
    p.add_argument('--client-source',required=True,type=Path)
    p.add_argument('--client-sha',required=True)
    p.add_argument('--python',required=True)
    a=p.parse_args();target=a.runtime_root.resolve();source=Path(__file__).resolve().parents[1]
    if target.exists():raise ValueError('RUNTIME_DESTINATION_EXISTS')
    if subprocess.check_output(['git','-C',str(a.client_source),'rev-parse',a.client_sha+'^{commit}'],text=True).strip()!=a.client_sha:raise ValueError('CLIENT_REVISION_MISMATCH')
    target.mkdir(parents=True,mode=0o700)
    run('git','clone','--no-hardlinks','--no-checkout',str(a.client_source),str(target/'client'))
    run('git','-C',str(target/'client'),'checkout','--detach',a.client_sha)
    run('uv','venv','--copies','--python',a.python,str(target/'venv'))
    run('uv','pip','install','--python',str(target/'venv/bin/python'),'-r',str(source/'requirements-operational.lock'))
    config={'resume_root':str(target/'client'),'python':str(target/'venv/bin/python'),'source_sha':a.client_sha,
            'model':'gpt-6-sol','reasoning':'medium'}
    (target/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    files={str(p.relative_to(target/'client')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (target/'client/v6_nextjs_migration/backend/app').rglob('*.py')}
    (target/'MANIFEST.json').write_text(json.dumps({'client_sha':a.client_sha,'client_files':files,'requirements_sha256':hashlib.sha256((source/'requirements-operational.lock').read_bytes()).hexdigest(),'python':subprocess.check_output([str(target/'venv/bin/python'),'--version'],text=True).strip()},indent=2)+'\n')
    print(json.dumps({'runtime_root':str(target),'config':str(target/'config.json'),'promotion':'NOT_PERFORMED','requested_model':'gpt-6-sol'}))

if __name__=='__main__':main()
