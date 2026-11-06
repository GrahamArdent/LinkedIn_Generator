"""Thin loopback review UI over the exact CLI application service."""
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import secrets
from urllib.parse import urlsplit,parse_qs

PAGE='''<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Graham authoring</title>
<style>body{font:17px system-ui;margin:24px auto;padding:0 16px;max-width:900px;background:#f5f5f2;color:#202520}input,textarea,select,button{font:inherit;box-sizing:border-box;margin:6px 0;padding:10px;max-width:100%;width:100%}button{background:#173e39;color:white;border:0;border-radius:5px;cursor:pointer}pre{font:inherit;line-height:1.5;white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:18px}label{display:block;margin-top:10px}h1{font-size:1.6rem}</style></head>
<body><h1>Graham authoring</h1><p>Prepare sourced writing, review exact candidates and export. Human judgment is required. This app does not publish.</p>
<button id="history">History</button><button id="voices">Voices</button><button id="newrequest">New request (no generation)</button><p id="status" role="status"></p><pre id="output"></pre>
<label>Request ID<input id="job" placeholder="A stable unique ID"></label>
<label>Parent request ID (optional revision link)<input id="parent"></label><label>Topic<input id="topic"></label><label>Source URLs (one per line, optional)<textarea id="urls"></textarea></label>
<label>Notes<textarea id="notes"></textarea></label><label>Voice<input id="voice" value="concise_challenger"></label>
<label>Narrative<select id="narrative"><option>literal</option><option>symbolic</option></select></label>
<button id="create">Create once</button><button id="show">Review / status</button><button id="resume">Reconcile / resume original</button>
<label>Exact candidate hash<input id="hash"></label>
<label>Your decision<select id="decision"><option value="">Still reviewing</option><option value="keep">Keep</option><option value="light">Light edit</option><option value="structural">Structural edit</option><option value="reject">Reject</option></select></label><label>Preference (optional)<input id="preference"></label><label>Notes on facts, voice, construction or usefulness<textarea id="note"></textarea></label><label>Actual editing minutes (optional)<input id="minutes" type="number" min="0"></label><label><input id="voiceapproval" type="checkbox" style="width:auto"> Explicitly approve this text as a reusable voice example</label><button id="savefeedback">Record feedback</button>
<label>Human revision<textarea id="edit"></textarea></label><button id="saveedit">Save revision (invalidates reviews and visuals)</button>
<button id="activate">Activate explicitly approved voice example</button><button id="export">Export selected text and manifest</button>
<div id="items"></div><details><summary>Provenance and history</summary><pre id="details"></pre></details>
<script>
const token=TOKEN;const el=id=>document.getElementById(id);
async function call(path,data){el('status').textContent='Working…';try{let r=await fetch(path,data?{method:'POST',headers:{'Content-Type':'application/json','X-Local-Token':token},body:JSON.stringify(data)}:{});let v=await r.json();render(v);el('status').textContent=r.ok?(v.state||'Saved / read complete'):(v.error||'Action needs attention');return v}catch(e){el('status').textContent=String(e)}}
function render(v){if(v.input&&v.id){el('job').value=v.id;localStorage.setItem('graham-job',v.id);for(const k of ['topic','notes','voice','narrative','parent'])el(k).value=v.input[k]||({voice:'concise_challenger',narrative:'literal'}[k]||'');el('urls').value=(v.input.urls||[]).join('\\n')}el('details').textContent=JSON.stringify(v,null,2);el('items').replaceChildren();const selected=v.current_selected||v.result?.selected_candidate||(v.body&&v.content_sha256?v:null);if(selected||v.text||v.error||v.result?.error_code)el('output').textContent=selected?.body||v.text||v.error||v.result?.error_code;if(selected?.content_sha256){for(const k of ['decision','note','preference','minutes'])el(k).value='';el('voiceapproval').checked=false;el('hash').value=selected.content_sha256;el('edit').value=selected.body}if(Array.isArray(v)){for(const job of v){const b=document.createElement('button');b.textContent=(job.input?.topic||job.id)+' · '+job.state+' · '+job.id;b.onclick=()=>{el('job').value=job.id;call('/api/job?id='+encodeURIComponent(job.id))};el('items').append(b)}}if(v.catalogue){for(const [id,voice]of Object.entries(v.catalogue.voices)){const b=document.createElement('button');b.textContent=voice.label;b.onclick=()=>{el('voice').value=id;el('status').textContent='Voice selected; no generation started'};el('items').append(b)}}}
function action(a,extra={}){if(a==='create'&&!el('job').value)el('job').value='graham-'+crypto.randomUUID();if(el('job').value)localStorage.setItem('graham-job',el('job').value);return call('/api/action',{action:a,id:el('job').value,...extra})}
el('newrequest').onclick=()=>{for(const k of ['job','parent','topic','urls','notes','hash','edit','note','preference','minutes'])el(k).value='';el('decision').value='';el('voiceapproval').checked=false;localStorage.removeItem('graham-job');el('output').textContent='';el('details').textContent='';el('status').textContent='New request; generation has not started'};
el('history').onclick=()=>call('/api/list');el('voices').onclick=()=>call('/api/voices');
el('create').onclick=()=>action('create',{topic:el('topic').value,urls:el('urls').value.split('\\n').filter(Boolean),notes:el('notes').value,voice:el('voice').value,narrative:el('narrative').value,parent:el('parent').value||null});
el('show').onclick=()=>call('/api/job?id='+encodeURIComponent(el('job').value));el('resume').onclick=()=>action('resume');
el('savefeedback').onclick=()=>{const d={candidate_hash:el('hash').value,note:el('note').value};if(el('decision').value)d.decision=el('decision').value;if(el('preference').value)d.preference=el('preference').value;if(el('minutes').value!=='')d.editing_minutes=Number(el('minutes').value);if(el('voiceapproval').checked)d.approve_voice_example=true;action('feedback',{data:d})};
el('saveedit').onclick=()=>action('edit',{text:el('edit').value});el('activate').onclick=()=>action('activate-voice',{hash:el('hash').value});
el('export').onclick=async()=>{const v=await call('/api/export?id='+encodeURIComponent(el('job').value));if(v.text){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([v.text],{type:'text/markdown'}));a.download=v.manifest.selected_hash+'.md';a.click();URL.revokeObjectURL(a.href)}};
if(localStorage.getItem('graham-job')){el('job').value=localStorage.getItem('graham-job');call('/api/job?id='+encodeURIComponent(el('job').value))}
</script></body></html>'''


def handler(app,token):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def send(self,value,status=200,html=False):
            raw=value.encode() if html else json.dumps(value,ensure_ascii=False).encode()
            self.send_response(status);self.send_header('Content-Type','text/html; charset=utf-8' if html else 'application/json; charset=utf-8')
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY')
            self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def valid_host(self):
            return self.headers.get('Host') in ('127.0.0.1:'+str(self.server.server_port),'localhost:'+str(self.server.server_port))
        def do_GET(self):
            if not self.valid_host():return self.send({'error':'INVALID_HOST'},403)
            parsed=urlsplit(self.path);query=parse_qs(parsed.query)
            try:
                if parsed.path=='/':return self.send(PAGE.replace('TOKEN',json.dumps(token)),html=True)
                if parsed.path=='/api/list':return self.send([app.show(r['id']) for r in app.store.list()])
                if parsed.path=='/api/job':return self.send(app.show(query.get('id',[''])[0]))
                if parsed.path=='/api/export':return self.send(app.export(query.get('id',[''])[0]))
                if parsed.path=='/api/voices':
                    from .writing_voice import CATALOG_PATH
                    return self.send({'catalogue':json.loads(CATALOG_PATH.read_bytes()),'active_examples':app.active_voice()})
                self.send({'error':'NOT_FOUND'},404)
            except Exception as exc:self.send({'error':str(exc)},400)
        def do_POST(self):
            if not self.valid_host() or not secrets.compare_digest(self.headers.get('X-Local-Token',''),token):return self.send({'error':'LOCAL_TOKEN_REQUIRED'},403)
            origin=self.headers.get('Origin')
            if origin and origin not in ('http://127.0.0.1:'+str(self.server.server_port),'http://localhost:'+str(self.server.server_port)):return self.send({'error':'INVALID_ORIGIN'},403)
            try:
                length=int(self.headers.get('Content-Length','0'))
                if self.path!='/api/action' or not 0<length<=32768:raise ValueError('INVALID_ACTION')
                d=json.loads(self.rfile.read(length));a=d['action'];job=d['id']
                if a=='create':result=app.create(job,d['topic'],urls=d.get('urls',[]),notes=d.get('notes',''),voice=d.get('voice','concise_challenger'),narrative=d.get('narrative','literal'),parent=d.get('parent'),new_budget=d.get('new_budget',False))
                elif a=='resume':result=app.resume(job)
                elif a=='feedback':result=app.feedback(job,d['data'])
                elif a=='edit':result=app.edit(job,d['text'])
                elif a=='activate-voice':result=app.activate_voice(job,d['hash'])
                else:raise ValueError('UNSUPPORTED_ACTION')
                self.send(result)
            except Exception as exc:self.send({'error':str(exc)},400)
    return Handler


def serve(app,port=8765):
    server=HTTPServer(('127.0.0.1',port),handler(app,secrets.token_urlsafe(32)))
    print('Graham authoring at http://127.0.0.1:'+str(server.server_port),flush=True)
    server.serve_forever()
