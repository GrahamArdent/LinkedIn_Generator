import json
from pathlib import Path
import subprocess
import pytest
from src.app.codex_provider import CodexConfig,CodexProvider,CodexError


def test_recovery_is_explicit_no_dispatch_and_preserves_receipt(tmp_path):
    seen=[]
    def runner(argv,**kw):
        seen.append(json.loads(kw['input']))
        return subprocess.CompletedProcess(argv,0,json.dumps({'ok':True,'data':{'text':'original'},'attempt_id':'original','cache_hit':True}),'')
    p=CodexProvider(CodexConfig(tmp_path,Path('/python'),'sha','sol'),tmp_path/'attempts','one',runner=runner)
    r=p.reconcile(model='sol',system='s',user='u',temperature=0)
    assert seen[0]['operation']=='recover_only' and r['receipt']['attempt_id']=='original'
    assert r['text']=='original'


def test_recovery_has_read_only_allowance_after_dispatch_deadline(tmp_path):
    import time
    seen=[]
    def runner(argv,**kw):
        seen.append(kw['timeout'])
        return subprocess.CompletedProcess(argv,0,json.dumps({'ok':True,'data':{'text':'original'},'cache_hit':True}),'')
    p=CodexProvider(CodexConfig(tmp_path,Path('/python'),'sha','sol'),tmp_path,'one',runner=runner);p.deadline=time.time()-900
    assert p.reconcile(model='sol',system='s',user='u',temperature=0)['text']=='original'
    assert seen[0]>=20
