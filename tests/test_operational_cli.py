import json,subprocess,sys
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/linkedin_app.py'
def cli(root,*args):return subprocess.run([sys.executable,str(SCRIPT),'--data-root',str(root),*args],capture_output=True,text=True)

def test_fresh_process_init_list_missing_store_and_cross_directory(tmp_path):
    root=tmp_path/'data'
    assert cli(root,'list').returncode==2
    assert not root.exists()
    assert cli(root,'init').returncode==0
    assert json.loads(cli(root,'list').stdout)==[]
    from src.app.operational_store import Store
    s=Store(root);s.admit('original',{'topic':'unchanged'},{'model':'original'});s.finish('original','completed',{'exact':True})
    assert json.loads(cli(root,'status','--id','original').stdout)['result']=={'exact':True}
    assert cli(root,'resume','--id','original').returncode==0


def test_legacy_import_keeps_original_failed_receipt_and_conflicts(tmp_path):
    root=tmp_path/'data';assert cli(root,'init').returncode==0
    old=tmp_path/'old';old.mkdir();(old/'trial.json').write_text(json.dumps({'input':{'request_id':'old','topic':'old'},'state':'failed','error_code':'NO_QUALIFIED_CANDIDATE','engine':{'body':'unqualified'}}))
    assert cli(root,'import','--path',str(old)).returncode==0
    got=json.loads(cli(root,'show','--id','old').stdout)
    assert got['result']['legacy_record']['state']=='failed'
    assert (old/'trial.json').exists()
    assert cli(root,'import','--path',str(old)).returncode==0
    (old/'trial.json').write_text(json.dumps({'input':{'request_id':'old','topic':'changed'},'state':'completed'}))
    assert cli(root,'import','--path',str(old)).returncode==2


def test_imported_unresolved_history_blocks_new_subject_before_model(tmp_path):
    from scripts.linkedin_app import import_legacy
    from src.app.operational_store import Store
    from src.app.operational import Application
    root=tmp_path/'data';s=Store.initialize(root)
    old=tmp_path/'old';old.mkdir();(old/'trial.json').write_text(json.dumps({'input':{'request_id':'old','topic':'Known original subject'},'state':'failed'}))
    import_legacy(s,old)
    import pytest
    with pytest.raises(ValueError,match='SUBJECT_HISTORY_UNRESOLVED'):
        Application(s,None).create('new','A genuinely new subject')
