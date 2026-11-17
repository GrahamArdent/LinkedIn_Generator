import json
from pathlib import Path
import pytest
from src.app.operational import Application,text_hash
from src.app.operational_store import Store
from src.app.integration import generate_content
from src.app.contracts import LinkedInContentRequest
from src.app.publish_quality import ESSENTIAL_CHECKS,REVIEW_POLICY_VERSION


def qualified_payload(score=None):
    candidate={'body':'A complete supported draft.','score':score,'policy_version':REVIEW_POLICY_VERSION,'review_status':'reviewable','essential_checks':{k:{'verdict':'pass','reason':'Supported supplied point.'} for k in ESSENTIAL_CHECKS}}
    return {'body':candidate['body'],'status':'drafted','review':{'publish_ready':True,'review_eligible':True,'policy_version':REVIEW_POLICY_VERSION,'review_status':'reviewable','recommendation':'original','original':candidate}}


def test_valid_essentials_qualify_without_optional_score_and_failed_essentials_stay_closed():
    request=LinkedInContentRequest(topic='My point',visual_asset_plan=False)
    payload=qualified_payload()
    result=generate_content(request,generator=lambda **kw:payload)
    assert result.selected_candidate and result.selected_candidate.score is None
    payload['review']['original']['essential_checks']['factual_integrity']={'verdict':'needs_evidence','reason':'Unsupported number.'}
    assert generate_content(request,generator=lambda **kw:payload).selected_candidate is None
    payload['review'].pop('policy_version');payload['review']['threshold']=90
    assert generate_content(request,generator=lambda **kw:payload).selected_candidate is None


def test_visual_planning_failure_retains_exact_qualified_text():
    def fail(**kw):raise RuntimeError('optional provider failed')
    result=generate_content(LinkedInContentRequest(topic='My point'),generator=lambda **kw:qualified_payload(80),visual_planner=fail)
    assert result.body=='A complete supported draft.'
    assert result.selected_candidate.content_sha256==text_hash(result.body)
    assert result.visual_asset.status=='deferred' and 'visual_planner_unavailable' in result.visual_asset.warnings[0]


def writing(tmp_path):
    app=Application(Store.initialize(tmp_path/'data'),None)
    app.save_idea('item','My intended point',notes='A supplied opinion, not independent empirical proof.')
    text=app.edit('item','An actual saved text long enough to serve as an explicitly approved style reference.',expected_brief=1,expected_text=None)
    return app,text


def test_writing_voice_approval_and_activation_are_separate_exact_version_effects(tmp_path):
    app,text=writing(tmp_path)
    payload={'candidate_hash':text['content_sha256'],'decision':'keep','approve_voice_example':True,'brief_revision':1,'text_version':text['version'],'preference':'B','editing_minutes':3}
    app.feedback('item',payload)
    assert app.active_voice()['version']==0
    value=app.activate_voice('item',text['content_sha256'],expected_brief=1,expected_text=text['version'])
    assert value['version']==1 and value['examples'][0]['text']==text['body']
    assert app.activate_voice('item',text['content_sha256'],expected_brief=1,expected_text=text['version'])==value
    app.save_idea('item','New context',expected_brief=1)
    with pytest.raises(ValueError,match='STALE_WRITING_VERSION'):app.activate_voice('item',text['content_sha256'],expected_brief=1,expected_text=text['version'])
    assert app.active_voice()==value


def test_missing_or_machine_approval_never_activates_voice(tmp_path):
    app,text=writing(tmp_path)
    app.feedback('item',{'candidate_hash':text['content_sha256'],'decision':'keep'})
    with pytest.raises(ValueError,match='VOICE_APPROVAL_REQUIRED'):app.activate_voice('item',text['content_sha256'],expected_brief=1,expected_text=text['version'])
    app.feedback('item',{'candidate_hash':text['content_sha256'],'decision':'keep','approve_voice_example':True,'brief_revision':1,'text_version':text['version'],'test_only':True})
    with pytest.raises(ValueError,match='VOICE_APPROVAL_REQUIRED'):app.activate_voice('item',text['content_sha256'],expected_brief=1,expected_text=text['version'])
    assert app.active_voice()['version']==0


def test_feedback_approval_cannot_certify_a_new_version_with_same_text(tmp_path):
    app,text=writing(tmp_path)
    app.feedback('item',{'candidate_hash':text['content_sha256'],'decision':'keep','approve_voice_example':True,'brief_revision':1,'text_version':text['version']})
    newer=app.edit('item',text['body'],expected_brief=1,expected_text=text['version'])
    with pytest.raises(ValueError,match='VOICE_APPROVAL_REQUIRED'):app.activate_voice('item',newer['content_sha256'],expected_brief=1,expected_text=newer['version'])


def test_later_deliberate_action_has_new_finite_window_without_mutating_expired_original(tmp_path,monkeypatch):
    import src.app.operational as m
    from src.app.codex_provider import CodexConfig
    app,text=writing(tmp_path);app.config=CodexConfig(tmp_path,Path('/python'),'sha','fixture')
    app.store.admit('expired',{'writing_snapshot':{'item':'item'}},{'admission':'expired'})
    with app.store.transaction() as con:con.execute('UPDATE jobs SET created=created-2000 WHERE id="expired"')
    app.store.finish('expired','budget_exhausted',{'original':'preserved'})
    before=app.store.get('expired');monkeypatch.setattr(m,'qualify_model',lambda c:{'model':c.model})
    class Provider:
        def __init__(self,*a):self.receipts=[]
        def generate(self,**kw):
            self.receipts.append({'attempt_id':'fresh-recheck'})
            return json.dumps({'essential_checks':{k:{'verdict':'pass','reason':'Supported'} for k in ESSENTIAL_CHECKS}})
    monkeypatch.setattr(m,'CodexProvider',Provider)
    result=app.recheck_item('item','deliberate-check',expected_brief=1,expected_text=text['version'])
    assert result['state']=='completed' and result['binding']['admission']=='deliberate-check'
    assert app.store.get('expired')==before


def test_partial_essential_findings_survive_without_qualifying_incomplete_review():
    from src.app.publish_quality import assess_publish_quality,WEIGHTS
    class Client:
        def call(self,*a,**kw):return {'text':json.dumps({**{k:5 for k in WEIGHTS},'essential_checks':{'factual_integrity':{'verdict':'needs_evidence','reason':'A number lacks support.'}}})}
    result=assess_publish_quality(text='Saved text.',audience='readers',content_goal='reach',evidence=[],persona_profile={},client=Client())
    assert result.review_status=='assessment_unavailable' and result.score is None
    assert result.essential_checks['factual_integrity']['verdict']=='needs_evidence'


def test_failed_start_is_observed_without_trial_enrollment_or_dispatch(tmp_path):
    app,text=writing(tmp_path)
    with app.store.connection() as con:history=con.execute('SELECT value FROM metadata WHERE key="trial_history"').fetchone()[0]
    with pytest.raises(ValueError,match='CONFIG_REQUIRED'):app.draft_item('item','not-started',expected_brief=1,expected_text=text['version'])
    record=app.show('item');failure=record['events'][-1]
    assert failure['kind']=='action_not_admitted' and failure['payload']['attempt']=='not-started'
    assert failure['payload']['error_code']=='CONFIG_REQUIRED'
    assert app.store.list()==[]
    with app.store.connection() as con:assert con.execute('SELECT value FROM metadata WHERE key="trial_history"').fetchone()[0]==history


@pytest.mark.parametrize('mixed',[False,True])
def test_normal_preparation_preserves_supplied_viewpoint_and_mixed_public_support(tmp_path,monkeypatch,mixed):
    from src.app import operational as m
    from src.app.codex_provider import CodexConfig
    app=Application(Store.initialize(tmp_path/'data'),CodexConfig(tmp_path,Path('/python'),'sha','fixture'))
    note='I prefer authoring to begin with the point I want to make.'
    urls=['https://example.org/study'] if mixed else []
    app.save_idea('item','My viewpoint about authoring',notes=note,urls=urls)
    monkeypatch.setattr(m,'qualify_model',lambda c:{'model':c.model})
    public={'source_id':'S1','status':'usable','title':'Study','publisher':'Publisher','url':urls[0] if mixed else None,'checked_at':'2026-11-16','limitations':'A limited published observation.','passages':[{'locator':'paragraph1','excerpt':'One published study described a limited observation.'}]}
    def acquire(self,topic,seen):
        assert mixed and list(seen)==urls
        return {'sources':[public],'errors':[]}
    monkeypatch.setattr(m.Evidence,'acquire',acquire)
    class Provider:
        def __init__(self,*a):self.receipts=[]
        def generate(self,**kw):
            facts=[{'claim_id':'C1','source_id':'U1','locator':'supplied account 1'}]
            if mixed:facts.append({'claim_id':'C2','source_id':'S1','locator':'paragraph1'})
            self.receipts.append({'attempt_id':'prep'})
            return json.dumps({'status':'ready','intended_reader':'A professional choosing a writing workflow','reason':'A supplied viewpoint, not an invented event.','meaning':{'thesis':'Begin with the intended point.','reader_consequence':'Keep author choice visible.','qualification':'The personal statement is opinion; no measured gain is claimed.','facts':facts},'narrative':{'form':'literal','beats':['Describe the choice.'],'symbol':None},'support_checks':[{'claim_id':f['claim_id'],'relevant':True,'primary_source':True,'entails':True,'contradicted':False,'reason':'Exact supplied statement or limited published sentence.'} for f in facts]})
    monkeypatch.setattr(m,'CodexProvider',Provider)
    def engine(request,**kw):
        bundle=kw['generator'].keywords['editorial_brief']
        assert bundle['author_intent']['notes']==note and bundle['claims'][0]['kind']=='observation'
        assert request.evidence[0].fact==note and request.evidence[0].url is None
        assert request.opportunity_gate is False and len(request.evidence)==(2 if mixed else 1)
        if mixed:assert bundle['claims'][1]['kind']=='fact' and request.evidence[1].url==urls[0]
        kw['generator'].keywords['working_text_sink']('A bounded draft of the supplied viewpoint.','draft')
        class Result:
            def model_dump(self):return {'body':'A bounded draft of the supplied viewpoint.','status':'drafted','review':{'review_status':'assessment_unavailable'},'selected_candidate':None}
        return Result()
    monkeypatch.setattr(m,'generate_content',engine)
    assert app.draft_item('item','draft',expected_brief=1,expected_text=None)['state']=='unqualified'
    assert app.export('item')['text']=='A bounded draft of the supplied viewpoint.'


def test_unknown_extra_essential_key_does_not_turn_retained_checks_into_qualification():
    from src.app.publish_quality import assess_publish_quality
    class Client:
        def call(self,*a,**kw):
            checks={k:{'verdict':'pass','reason':'Supported'} for k in ESSENTIAL_CHECKS};checks['unrecognized']={'verdict':'pass','reason':'Unexpected schema.'}
            return {'text':json.dumps({'essential_checks':checks})}
    result=assess_publish_quality(text='Saved text.',audience='readers',content_goal='reach',evidence=[],persona_profile={},client=Client())
    assert len(result.essential_checks)==4 and result.review_status=='assessment_unavailable' and result.assessment_complete is False


def test_busy_start_is_observed_without_new_attempt(tmp_path):
    import fcntl
    app,text=writing(tmp_path)
    with (app.store.root/('.writing-'+text_hash('item')+'.lock')).open('a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        with pytest.raises(ValueError,match='WRITING_ACTION_BUSY'):app.draft_item('item','busy-start',expected_brief=1,expected_text=text['version'])
    assert app.show('item')['events'][-1]['payload']['error_code']=='WRITING_ACTION_BUSY' and app.store.list()==[]


def test_actual_ui_binds_writing_feedback_and_resets_inherited_approval():
    import subprocess,shutil
    from src.app.operational_ui import PAGE
    node=shutil.which('node')
    if not node:pytest.skip('Node unavailable')
    script=PAGE.split('<script>')[1].split('</script>')[0].replace('TOKEN','"fixture"')
    harness=r'''
const vm=require('vm'),fs=require('fs'),script=JSON.parse(fs.readFileSync(0,'utf8')),fields=new Map(),requests=[];
const get=id=>{if(!fields.has(id))fields.set(id,{value:'',checked:false,textContent:'',replaceChildren(){},append(){}});return fields.get(id)};
const ctx={document:{getElementById:get,createElement(){return {}}},localStorage:{getItem(){return null},setItem(){},removeItem(){}},crypto:{randomUUID(){return 'uuid'}},fetch:async(path,opts)=>{requests.push(JSON.parse(opts.body));return {ok:true,json:async()=>({saved:true})}},console};vm.createContext(ctx);vm.runInContext(script,ctx);
get('decision').value='keep';get('voiceapproval').checked=true;get('minutes').value='4';
vm.runInContext("render({kind:'writing_item',id:'item',brief_revision:2,brief:{topic:'My point'},current_text:{version:7,body:'Current text',content_sha256:'hash'}})",ctx);
if(get('voiceapproval').checked||get('minutes').value!=='')throw Error('inherited approval');get('decision').value='keep';get('voiceapproval').checked=true;get('minutes').value='3';get('savefeedback').onclick();
(async()=>{await Promise.resolve();const r=requests.at(-1);if(r.action!=='feedback'||r.data.brief_revision!==2||r.data.text_version!==7||r.data.editing_minutes!==3||r.data.approve_voice_example!==true)throw Error('feedback lost context');if(requests.some(r=>r.action==='activate-voice'))throw Error('silent activation');get('activate').onclick();await Promise.resolve();const a=requests.at(-1);if(a.action!=='activate-voice'||a.expected_brief!==2||a.expected_text!==7)throw Error('activation lost context');console.log('PASS');})().catch(e=>{console.error(e);process.exitCode=1});
'''
    result=subprocess.run([node,'-e',harness],input=json.dumps(script),capture_output=True,text=True)
    assert result.returncode==0,result.stderr


def test_optional_visual_config_failure_does_not_discard_qualified_text(monkeypatch):
    import src.app.integration as m
    monkeypatch.setattr(m,'load_yaml',lambda *a:(_ for _ in ()).throw(FileNotFoundError('optional visual config absent')))
    result=m.generate_content(LinkedInContentRequest(topic='My point'),generator=lambda **kw:qualified_payload(80))
    assert result.body=='A complete supported draft.' and result.selected_candidate is not None
    assert result.visual_asset.status=='deferred'


def test_durable_visual_unknown_retains_selected_text_and_original_stage(tmp_path,monkeypatch):
    from src.app import operational as m
    from src.app.codex_provider import CodexConfig
    from src.app.operational_store import sha
    app=Application(Store.initialize(tmp_path/'data'),CodexConfig(tmp_path,Path('/python'),'sha','fixture'))
    monkeypatch.setattr(m,'qualify_model',lambda c:{'model':c.model})
    source={'source_id':'S1','status':'usable','title':'Study','publisher':'Publisher','url':'https://example.org/study','checked_at':'2026-11-16','limitations':'Limited study.','passages':[{'locator':'paragraph1','excerpt':'A limited published observation.'}]}
    monkeypatch.setattr(m.Evidence,'acquire',lambda *a,**kw:{'sources':[source],'errors':[]})
    dispatches=[];recoveries=[]
    class Provider:
        def __init__(self,*a):self.receipts=[]
        def reconcile(self,**kw):
            recoveries.append(kw['system'])
            return {'text':'Retained original visual reply','receipt':{'attempt_id':'original-visual','active_seconds':1,'cache_hit':True}}
        def generate(self,**kw):
            dispatches.append(kw['system'])
            if kw['system']=='optional visual':raise ValueError('CODEX_COMPLETION_UNKNOWN')
            self.receipts.append({'attempt_id':'preparation'})
            return json.dumps({'status':'ready','reason':'Supported.','meaning':{'thesis':'A limited point.','reader_consequence':'Check applicability.','qualification':'Limited study.','facts':[{'claim_id':'C1','source_id':'S1','locator':'paragraph1'}]},'narrative':None,'support_checks':[{'claim_id':'C1','relevant':True,'primary_source':True,'entails':True,'contradicted':False,'reason':'Exact study sentence.'}]})
    monkeypatch.setattr(m,'CodexProvider',Provider)
    from src.app.integration import generate_content as integrated
    def engine(request,**kw):
        client=kw['generator'].keywords['publish_quality_client']
        def visual(**args):return client.call('optional visual','exact visual input',response_json=True)
        return integrated(request,generator=lambda **args:qualified_payload(80),visual_planner=visual)
    monkeypatch.setattr(m,'generate_content',engine)
    with pytest.raises(ValueError,match='CODEX_COMPLETION_UNKNOWN'):app.create('original','A supported topic',urls=['https://example.org/study'])
    record=app.store.get('original');assert record['state']=='unknown'
    assert app.export('original')['text']=='A complete supported draft.'
    assert record['result']['selected_candidate']['content_sha256']==text_hash('A complete supported draft.')
    with app.store.connection() as con:pending=con.execute('SELECT input_hash,state FROM stages WHERE job="original" AND state<>"completed"').fetchall()
    assert len(pending)==1 and pending[0]['state']=='reserved'
    assert pending[0]['input_hash']==sha({'model':'fixture','system':'optional visual','user':'exact visual input','temperature':0.5})
    before=list(dispatches)
    resumed=app.resume('original')
    assert resumed['state']=='completed' and app.export('original')['text']=='A complete supported draft.'
    assert dispatches==before and recoveries==['optional visual']
    with app.store.connection() as con:assert not con.execute('SELECT 1 FROM stages WHERE job="original" AND state<>"completed"').fetchone()
