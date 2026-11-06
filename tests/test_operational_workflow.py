import json
import pytest
from src.app.operational_store import Store
from src.app import operational as m

class Native:
    mode='fixture';error=None
    def __init__(self):self.calls=0;self.receipts=[]
    def generate(self,**kw):self.calls+=1;self.receipts.append({'ok':True,'attempt_id':'original'});return 'saved'
    def reconcile(self,**kw):return {'text':'saved','receipt':{'ok':True,'attempt_id':'original'}}


def test_provider_duplicate_and_pending_reconcile_never_dispatch(tmp_path):
    s=Store.initialize(tmp_path/'data');s.admit('one',{}, {'model':'test'})
    n=Native();p=m.DurableProvider(s,'one',n)
    args=dict(model='test',system='s',user='u',temperature=0)
    assert p.generate(**args)=='saved' and n.calls==1
    assert m.DurableProvider(s,'one',n).generate(**args)=='saved' and n.calls==1
    key=m.call_key(dict(model='test',system='s2',user='u',temperature=0))
    s.reserve('one','model:'+key,dict(model='test',system='s2',user='u',temperature=0))
    assert m.DurableProvider(s,'one',n).generate(model='test',system='s2',user='u',temperature=0)=='saved'
    assert n.calls==1


def test_budget_limits_are_persisted_across_provider_instances(tmp_path):
    s=Store.initialize(tmp_path/'data');s.admit('one',{}, {'model':'test'})
    n=Native()
    for i in range(12):m.DurableProvider(s,'one',n).generate(model='test',system=str(i),user='u',temperature=0)
    with pytest.raises(ValueError,match='MODEL_BUDGET_EXHAUSTED'):
        m.DurableProvider(s,'one',n).generate(model='test',system='extra',user='u',temperature=0)
    assert n.calls==12


def test_preference_only_and_material_edit_export_invalidation(tmp_path):
    s=Store.initialize(tmp_path/'data');s.admit('one',{}, {})
    text='A long enough selected text for a human-approved voice example.'
    s.finish('one','completed',{'selected_candidate':{'body':text,'content_sha256':m.text_hash(text)},'visual_asset':{'status':'planned'}})
    a=m.Application(s,None)
    f=a.feedback('one',{'candidate_hash':m.text_hash(text),'preference':'B'})
    with pytest.raises(ValueError,match='VOICE_APPROVAL_REQUIRED'):a.activate_voice('one',m.text_hash(text))
    assert a.export('one')['text']==text
    revised=a.edit('one','A human changes the argument and factual interpretation.')
    assert revised['review_status']=='revalidation_required'
    exported=a.export('one')
    assert exported['text']==revised['body'] and exported['manifest']['review_status']=='revalidation_required'
    assert exported['manifest']['visual_asset'] is None and not exported['manifest']['publication_approved']
    assert s.get('one')['result']['selected_candidate']['body']==text


def test_explicit_voice_activation_new_version_is_frozen(tmp_path):
    s=Store.initialize(tmp_path/'data');s.admit('one',{}, {})
    text='A long enough selected text for explicit human approval as an example.'
    h=m.text_hash(text);s.finish('one','completed',{'selected_candidate':{'body':text,'content_sha256':h}})
    a=m.Application(s,None);a.feedback('one',{'candidate_hash':h,'decision':'keep','approve_voice_example':True})
    v=a.activate_voice('one',h)
    assert v['examples'][0]['text']==text and v['version']==1
    assert a.active_voice()==v


def test_linked_revision_cannot_reset_shared_budget(tmp_path):
    s=Store.initialize(tmp_path/'data');s.admit('parent',{}, {'admission':'parent'})
    n=Native()
    for i in range(12):m.DurableProvider(s,'parent',n).generate(model='test',system=str(i),user='u',temperature=0)
    s.admit('child',{}, {'admission':'parent'})
    with pytest.raises(ValueError,match='MODEL_BUDGET_EXHAUSTED'):
        m.DurableProvider(s,'child',n).generate(model='test',system='extra',user='u',temperature=0)
    assert n.calls==12
