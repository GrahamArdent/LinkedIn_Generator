import json
from pathlib import Path
import pytest
from src.app.operational_store import Store
from src.app.operational import Application,text_hash
from src.app.codex_provider import CodexConfig


def test_public_create_progression_duplicate_and_shared_feedback_without_api(tmp_path,monkeypatch):
    import src.app.operational as m
    s=Store.initialize(tmp_path/'data');calls=[]
    monkeypatch.setattr(m,'qualify_model',lambda config:{'model':config.model})
    source={'source_id':'S1','status':'usable','title':'Study','publisher':'Publisher','url':'https://example.org/paper','checked_at':'2026-11-06','limitations':'Limited study.','passages':[{'locator':'Abstract','excerpt':'A study reported a limited observation.'}]}
    monkeypatch.setattr(m.Evidence,'acquire',lambda *a:{'sources':[source],'errors':[],'http_activity':[]})
    class Provider:
        mode='fixture';error=None
        def __init__(self,*a):self.receipts=[]
        def generate(self,**kw):
            calls.append(kw);self.receipts.append({'ok':True,'attempt_id':str(len(calls))})
            return json.dumps({'status':'ready','reason':'Supported scope.','meaning':{'thesis':'Limited claims need limits.','reader_consequence':'Check applicability.','facts':[{'claim_id':'C1','text':'A study reported a limited observation.','source_ids':['S1']}],'qualification':'One study only.'},'narrative':None})
    monkeypatch.setattr(m,'CodexProvider',Provider)
    def engine(req,**kw):
        assert req.editorial_handoff['meaning']['facts'][0]['text'] in req.evidence[0].fact
        return m.LinkedInContentRequest if False else Result()
    class Result:
        def model_dump(self):return {'selected_candidate':{'body':'A selected qualified body.','content_sha256':text_hash('A selected qualified body.')},'visual_asset':{'status':'deferred'}}
    monkeypatch.setattr(m,'generate_content',engine)
    app=Application(s,CodexConfig(tmp_path,Path('/python'),'sha','fixture'))
    first=app.create('one','A useful ordinary topic')
    assert first['state']=='completed' and len(calls)==1
    assert Application(Store(s.root),None).create('one','A useful ordinary topic')==first
    assert len(calls)==1
    with pytest.raises(ValueError,match='REQUEST_CONFLICT'):app.create('one','Changed same identity')
