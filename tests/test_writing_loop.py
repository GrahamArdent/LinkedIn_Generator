import json
from pathlib import Path
import pytest
from src.app.operational_store import Store
from src.app.operational import Application, text_hash


def test_capture_without_provider_and_atomic_stale_edits(tmp_path):
    app=Application(Store.initialize(tmp_path/'data'),None)
    item=app.save_idea('idea','Testing rules obstructed starting with a topic.',notes='This is my supplied account.')
    assert item['brief_revision']==1 and item['current_text'] is None
    assert app.store.list()==[]
    with pytest.raises(ValueError,match='WRITING_ITEM_NOT_EXECUTION'):app.resume('idea')
    a=app.edit('idea','An editable working draft.',expected_brief=1,expected_text=None)
    b=app.edit('idea','A newer manual version.',expected_brief=1,expected_text=a['version'])
    with pytest.raises(ValueError,match='STALE_WRITING_VERSION'):
        app.edit('idea','An obsolete UI save.',expected_brief=1,expected_text=a['version'])
    late=app.store.save_text('idea','Late generated alternative.',1,a['version'],attempt='original',stage='draft')
    assert late['conflict'] and app.show('idea')['current_text']['body']==b['body']
    assert len(app.show('idea')['text_history'])==3
    exported=Application(Store(app.store.root),None).export('idea')
    assert exported['text']==b['body'] and exported['manifest']['qualified'] is False
    assert app.store.list()==[]


def test_capture_updates_guard_brief_and_invalidate_review(tmp_path):
    app=Application(Store.initialize(tmp_path/'data'),None)
    app.save_idea('idea','Original point')
    a=app.edit('idea','My saved text.',expected_brief=1,expected_text=None)
    app.save_idea('idea','Changed context',expected_brief=1)
    assert app.export('idea')['manifest']['review_status']=='revalidation_required'
    with pytest.raises(ValueError,match='STALE_WRITING_VERSION'):app.save_idea('idea','Stale brief',expected_brief=1)
    late=app.store.save_text('idea','Old-brief result.',1,a['version'],attempt='old',stage='draft')
    assert late['conflict'] and app.export('idea')['text']=='My saved text.'


def test_personal_draft_survives_later_engine_failure_and_reopen(tmp_path,monkeypatch):
    from src.app import operational as m
    from src.app.codex_provider import CodexConfig
    app=Application(Store.initialize(tmp_path/'data'),CodexConfig(tmp_path,Path('/python'),'sha','fixture'))
    monkeypatch.setattr(m,'qualify_model',lambda c:{'model':c.model})
    class Provider:
        def __init__(self,*a):self.receipts=[]
        def generate(self,**kw):
            assert 'supplied account' in kw['user']
            self.receipts.append({'attempt_id':'meaning','active_seconds':0})
            return json.dumps({'status':'ready','reason':'Attributed account only.','meaning':{'thesis':'Start from the intended writing.','reader_consequence':'Separate experiments from drafting.','qualification':'Graham supplied this account; no independent outcome claim.','facts':[{'claim_id':'C1','source_id':'U1','locator':'supplied account 1'}]},'narrative':None,'support_checks':[{'claim_id':'C1','relevant':True,'primary_source':True,'entails':True,'contradicted':False,'reason':'Direct account of the author, not measured results.'}]})
    monkeypatch.setattr(m,'CodexProvider',Provider)
    def engine(req,**kw):
        assert req.opportunity_gate is False and req.evidence[0].url is None
        kw['generator'].keywords['working_text_sink']('Complete draft saved before later review fails.','draft')
        raise ValueError('ASSESSMENT_FAILURE')
    monkeypatch.setattr(m,'generate_content',engine)
    app.save_idea('idea','Why testing rules got in the way',notes='Testing rules blocked starting from a topic.')
    with pytest.raises(ValueError,match='ASSESSMENT_FAILURE'):app.draft_item('idea','attempt',expected_brief=1,expected_text=None)
    assert app.store.get('attempt')['state']=='failed'
    assert app.export('idea')['text']=='Complete draft saved before later review fails.'
    assert app.show('idea')['current_text']['review_status']=='assessment_unavailable'
    assert app.active_voice()['version']==0
    assert app.resume('attempt')['state']=='failed'
    app.feedback('idea',{'candidate_hash':text_hash(app.export('idea')['text']),'note':'Machine test feedback','test_only':True})
    with pytest.raises(ValueError,match='NO_SELECTED_CANDIDATE'):app.selected('attempt')
    assert Application(Store(app.store.root),None).export('idea')['text']==app.export('idea')['text']


def test_http_writing_actions_share_cli_state_and_require_parent(tmp_path):
    import threading,urllib.request
    from http.server import HTTPServer
    from src.app.operational_ui import handler
    app=Application(Store.initialize(tmp_path/'data'),None)
    server=HTTPServer(('127.0.0.1',0),handler(app,'secret'))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base='http://127.0.0.1:'+str(server.server_port)
    def post(data):
        request=urllib.request.Request(base+'/api/action',data=json.dumps(data).encode(),headers={'X-Local-Token':'secret','Content-Type':'application/json'})
        with urllib.request.urlopen(request) as response:return json.load(response)
    try:
        item=post({'action':'save-idea','id':'idea','topic':'My actual point','notes':'Supplied account.'})
        edited=post({'action':'edit','id':'idea','text':'Saved from UI.','expected_brief':item['brief_revision'],'expected_text':None})
        assert Application(Store(app.store.root),None).export('idea')['manifest']['revision']==edited['version']
        with urllib.request.urlopen(base+'/api/list') as response:assert json.load(response)[0]['kind']=='writing_item'
    finally:server.shutdown();server.server_close()


def test_advisory_dimensions_do_not_erase_valid_essentials():
    from src.app.publish_quality import assess_publish_quality,ESSENTIAL_CHECKS
    class Client:
        def call(self,*a,**kw):return {'text':json.dumps({'essential_checks':{k:{'verdict':'pass','reason':'Supported'} for k in ESSENTIAL_CHECKS},'outsider_clarity':'bad'})}
    result=assess_publish_quality(text='Saved exact text.',audience='readers',content_goal='reach',evidence=[],persona_profile={},client=Client())
    assert result.review_status=='reviewable' and result.score is None


def test_actual_pipeline_commits_draft_before_critic_failure(monkeypatch):
    from src.app import api
    captured=[]
    monkeypatch.setattr(api.Pipeline,'draft_variants',lambda *a:['A complete bounded draft.'])
    monkeypatch.setattr(api.Pipeline,'critic',lambda *a,**kw:(_ for _ in ()).throw(ValueError('later critic failed')))
    with pytest.raises(ValueError,match='later critic failed'):
        api.run_generation('My writing experience',[],persona_key='graham',allowed_sources=[],working_text_sink=lambda text,stage:captured.append((text,stage)))
    assert captured==[('A complete bounded draft.','draft')]


def test_additive_store_backup_and_old_jobs_survive_new_work(tmp_path):
    store=Store.initialize(tmp_path/'data');store.admit('historical',{'original':True},{'expired':True});store.finish('historical','failed',{'failure':'retained'})
    original=store.get('historical')
    store.backup(tmp_path/'before')
    app=Application(store,None);app.save_idea('new','A saved new idea')
    app.edit('new','Work created after the backup.',expected_brief=1,expected_text=None)
    store.backup(tmp_path/'after')
    assert Store(tmp_path/'after').get('historical')==original
    assert Application(Store(tmp_path/'after'),None).export('new')['text']=='Work created after the backup.'
    assert Store(tmp_path/'before').get('historical')==original
    assert not Store(tmp_path/'before').writing_exists('new')


def test_unknown_attempt_blocks_replacement_but_not_capture(tmp_path):
    app=Application(Store.initialize(tmp_path/'data'),None)
    app.save_idea('idea','An account')
    app.store.admit('unknown',{'writing_snapshot':{'item':'idea'}},{})
    app.store.finish('unknown','unknown',{'error_code':'RECONCILIATION_REQUIRED'})
    app.save_idea('idea','New notes still save',expected_brief=1)
    with pytest.raises(ValueError,match='RECONCILIATION_REQUIRED'):
        app.draft_item('idea','replacement',expected_brief=2,expected_text=None)
    assert len(app.store.list())==1


def test_recheck_exact_bytes_does_not_rewrite_and_late_review_is_not_current(tmp_path,monkeypatch):
    from src.app import operational as m
    from src.app.codex_provider import CodexConfig
    from src.app.publish_quality import ESSENTIAL_CHECKS
    app=Application(Store.initialize(tmp_path/'data'),CodexConfig(tmp_path,Path('/python'),'sha','fixture'))
    app.save_idea('idea','My point')
    current=app.edit('idea','Exact current text.',expected_brief=1,expected_text=None)
    monkeypatch.setattr(m,'qualify_model',lambda c:{'model':c.model})
    class Provider:
        def __init__(self,*a):self.receipts=[]
        def generate(self,**kw):
            assert json.loads(kw['user'])['post']=='Exact current text.'
            app.edit('idea','Newer text while checking.',expected_brief=1,expected_text=current['version'])
            self.receipts.append({'attempt_id':'recheck','active_seconds':0})
            return json.dumps({'essential_checks':{k:{'verdict':'pass','reason':'Supported'} for k in ESSENTIAL_CHECKS}})
    monkeypatch.setattr(m,'CodexProvider',Provider)
    result=app.recheck_item('idea','review-attempt',expected_brief=1,expected_text=current['version'])
    assert result['state']=='completed' and result['result']['review']['review_status']=='reviewable'
    assert app.export('idea')['text']=='Newer text while checking.'
    assert app.export('idea')['manifest']['review_status']=='revalidation_required'
    assert app.show('idea')['events'][-1]['payload']['conflict'] is True
    assert app.recheck_item('idea','review-attempt',expected_brief=1,expected_text=current['version'])==result
