import json
from concurrent.futures import ThreadPoolExecutor
import pytest
from src.app import operational_store as m


def test_missing_store_never_initializes_or_relaunches(tmp_path):
    with pytest.raises(ValueError, match='STORE_NOT_INITIALIZED'):
        m.Store(tmp_path/'missing')
    assert not (tmp_path/'missing').exists()


def test_global_identity_conflict_and_corrupt_result(tmp_path):
    s=m.Store.initialize(tmp_path/'data')
    j=s.admit('one', {'topic':'trust'}, {'model':'sol'})
    assert m.Store(s.root).admit('one', {'topic':'trust'}, {'model':'changed'})['binding']==j['binding']
    with pytest.raises(ValueError,match='REQUEST_CONFLICT'):
        s.admit('one', {'topic':'changed'}, {})
    s.finish('one', 'completed', {'selected':'exact'})
    assert m.Store(s.root).get('one')['result']=={'selected':'exact'}
    (s.root/'blobs'/s.get('one')['result_hash']).write_text('corrupt')
    with pytest.raises(ValueError,match='STORE_CORRUPT'):s.get('one')


def test_concurrent_reservation_and_recover_original_result(tmp_path):
    s=m.Store.initialize(tmp_path/'data');s.admit('one',{}, {})
    def reserve(_):
        try:return m.Store(s.root).reserve('one','stage',{'prompt':'same'})
        except ValueError as e:return str(e)
    with ThreadPoolExecutor() as pool:r=list(pool.map(reserve, range(8)))
    assert sum(x=='reserved' for x in r)==1
    assert r.count('RECONCILIATION_REQUIRED')==7
    s.commit_stage('one','stage',{'text':'retained','attempt_id':'original'})
    assert m.Store(s.root).stage('one','stage')['text']=='retained'
    assert s.reserve('one','stage',{'prompt':'same'})=='completed'
    with pytest.raises(ValueError,match='STAGE_CONFLICT'):s.reserve('one','stage',{'prompt':'different'})


def test_backup_relocation_preserves_original_identity(tmp_path):
    s=m.Store.initialize(tmp_path/'data');s.admit('one',{'topic':'x'},{})
    s.finish('one','needs_more_evidence',{'reason':'thin'})
    s.backup(tmp_path/'backup')
    assert m.Store(tmp_path/'backup').get('one')==s.get('one')
    (tmp_path/'backup'/'registry.sqlite3').unlink()
    with pytest.raises(ValueError,match='STORE_CORRUPT'):m.Store(tmp_path/'backup')
