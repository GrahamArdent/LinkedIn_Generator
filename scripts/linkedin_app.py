#!/usr/bin/env python3
"""Supported standalone Graham entry point; read operations never dispatch."""
import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.app.operational_store import Store,sha,atomic,encoded
from src.app.operational import Application
from src.app.codex_provider import CodexConfig


def import_legacy(store,path):
    path=path.resolve();trial=json.loads((path/'trial.json').read_bytes())
    job=trial['input']['request_id']
    binding={'legacy':True,'record_hash':sha(trial),'policy':'original','source_path':str(path)}
    old=None
    try:old=store.get(job)
    except ValueError as exc:
        if str(exc)!='JOB_NOT_FOUND':raise
    if old:
        if old['input']!=trial['input'] or old['binding'].get('record_hash')!=sha(trial):raise ValueError('LEGACY_ID_COLLISION')
        return old
    store.admit(job,trial['input'],binding)
    with store.transaction() as con:
        row=con.execute('SELECT value FROM metadata WHERE key="trial_history"').fetchone()
        history=json.loads(row['value']) if row else {'status':'unresolved','known_topics':[],'max_subjects':8,'first_six':'Unresolved; no invented judgments or exclusions'}
        topic=trial['input'].get('topic')
        if topic and topic not in history['known_topics']:history['known_topics'].append(topic)
        con.execute('INSERT OR REPLACE INTO metadata VALUES (?,?)',('trial_history',json.dumps(history)))
    # Retain original raw receipts without rewriting policy, subject eligibility or human labels.
    files=[]
    for item in sorted(path.rglob('*')):
        if item.is_file() and not item.is_symlink():
            raw=item.read_bytes()
            import base64
            files.append({'path':str(item.relative_to(path)),'sha256':__import__('hashlib').sha256(raw).hexdigest(),'content_base64':base64.b64encode(raw).decode()})
    store.event(job,'legacy_archive',{'files':files})
    return store.finish(job,'legacy',{**trial.get('engine',{}),'legacy_record':trial})


def main():
    p=argparse.ArgumentParser(description='Graham local authoring: create → review → feedback → export. No publication command.')
    p.add_argument('--data-root',type=Path,default=Path(os.environ.get('LINKEDIN_DATA_ROOT',str(Path.home()/'.local/share/graham-linkedin'))))
    p.add_argument('--config',type=Path,default=Path(os.environ['LINKEDIN_CONFIG']) if os.environ.get('LINKEDIN_CONFIG') else None)
    p.add_argument('action',choices=['init','create','status','list','show','resume','feedback','edit','activate-voice','voices','export','backup','import','serve'])
    p.add_argument('--new-budget',action='store_true');p.add_argument('--parent');p.add_argument('--id');p.add_argument('--topic');p.add_argument('--url',action='append',default=[]);p.add_argument('--notes',default='')
    p.add_argument('--voice',default='concise_challenger');p.add_argument('--narrative',choices=['literal','symbolic'],default='literal')
    p.add_argument('--path',type=Path);p.add_argument('--hash');p.add_argument('--port',type=int,default=8765)
    args=p.parse_args()
    store=Store.initialize(args.data_root) if args.action=='init' else Store(args.data_root)
    cfg=None
    if args.config:
        d=json.loads(args.config.read_bytes());cfg=CodexConfig(**{**d,'resume_root':Path(d['resume_root']),'python':Path(d['python'])})
    app=Application(store,cfg)
    if args.action in ('status','show','resume','feedback','edit','activate-voice','export','create') and not args.id:p.error('action needs --id')
    if args.action=='init':result={'status':'initialized','data_root':str(store.root)}
    elif args.action=='list':result=[app.show(r['id']) for r in store.list()]
    elif args.action in ('show','status'):result=app.show(args.id)
    elif args.action=='resume':result=app.resume(args.id)
    elif args.action=='create':
        if not args.topic:p.error('create needs --topic')
        result=app.create(args.id,args.topic,urls=args.url,notes=args.notes,voice=args.voice,narrative=args.narrative,parent=args.parent,new_budget=args.new_budget)
    elif args.action=='feedback':result=app.feedback(args.id,json.loads(args.path.read_bytes()))
    elif args.action=='edit':result=app.edit(args.id,args.path.read_text())
    elif args.action=='activate-voice':result=app.activate_voice(args.id,args.hash)
    elif args.action=='voices':
        result={'catalogue':json.loads((Path(__file__).resolve().parents[1]/'config/writing_voices.json').read_bytes()),'active_examples':app.active_voice()}
    elif args.action=='export':
        result=app.export(args.id)
        if args.path:
            args.path.mkdir(parents=True,exist_ok=True)
            name=result['manifest']['selected_hash']
            outputs={name+'.md':result['text'].encode(),name+'.json':encoded(result)}
            for filename,raw in outputs.items():
                target=args.path/filename
                if target.exists() and target.read_bytes()!=raw:raise ValueError('EXPORT_CONFLICT')
                if not target.exists():atomic(target,raw)
            result={'files':[str(args.path/n) for n in outputs],**result}
    elif args.action=='backup':store.backup(args.path);result={'backup':str(args.path)}
    elif args.action=='import':result=import_legacy(store,args.path)
    elif args.action=='serve':
        from src.app.operational_ui import serve
        return serve(app,args.port)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'status':'failed','error_code':getattr(exc,'code',str(exc))}),file=sys.stderr);sys.exit(2)
