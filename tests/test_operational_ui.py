from http.server import HTTPServer
import json,threading,urllib.request,urllib.error
from src.app.operational_store import Store
from src.app.operational import Application
from src.app import operational_ui as m


def test_http_reads_match_shared_store_and_reject_cross_site_write(tmp_path):
    s=Store.initialize(tmp_path/'data');s.admit('one',{},{});s.finish('one','completed',{'safe':'<script>alert(1)</script>'})
    server=HTTPServer(('127.0.0.1',0),m.handler(Application(s,None),'secret'))
    t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
    base='http://127.0.0.1:'+str(server.server_port)
    try:
        with urllib.request.urlopen(base+'/api/job?id=one') as r:assert json.load(r)['result']['safe'].startswith('<script>')
        with urllib.request.urlopen(base+'/') as r:
            html=r.read().decode();assert 'textContent' in html and 'innerHTML' not in html
            assert 'width=device-width' in html
        req=urllib.request.Request(base+'/api/action',data=b'{"action":"resume","id":"one"}',headers={'Content-Type':'application/json'})
        try:urllib.request.urlopen(req);assert False
        except urllib.error.HTTPError as exc:assert exc.code==403
        assert s.get('one')['result']=={'safe':'<script>alert(1)</script>'}
    finally:server.shutdown();server.server_close()
