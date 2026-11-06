"""Bounded public evidence acquisition. Network content is never authority."""
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import http.client
import ipaddress
import json
import base64
import multiprocessing
import socket
import ssl
import time
import re
import xml.etree.ElementTree as ET
import fcntl
from pathlib import Path
from contextlib import contextmanager
from urllib.parse import urlsplit, urljoin, urlencode

MAX_BYTES=2*1024*1024


def public_address(url):
    try:
        u=urlsplit(url)
        if u.scheme not in ('https','http') or not u.hostname or u.username or u.password or u.port not in (None,80 if u.scheme=='http' else 443):raise ValueError()
        addresses=socket.getaddrinfo(u.hostname,u.port or (443 if u.scheme=='https' else 80),type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):raise ValueError()
        return u,addresses[0][4][0]
    except (ValueError,OSError):raise ValueError('UNSAFE_URL') from None


class _Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.hidden=0;self.title=[];self.in_title=False
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','nav','noscript'):self.hidden+=1
        if tag=='title':self.in_title=True
        if tag in ('p','div','section','h1','h2','br'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','nav','noscript'):self.hidden=max(0,self.hidden-1)
        if tag=='title':self.in_title=False
        if tag in ('p','div','section','h1','h2'):self.parts.append('\n')
    def handle_data(self,data):
        if not self.hidden:self.parts.append(data)
        if self.in_title:self.title.append(data)


def source_record(requested,final,raw,content_type):
    if 'html' in content_type or 'xml' in content_type:
        parser=_Text();parser.feed(raw.decode('utf-8',errors='replace'))
        text='\n'.join(' '.join(x.split()) for x in ''.join(parser.parts).splitlines() if x.strip())
        title=''.join(parser.title).strip() or urlsplit(final).hostname
    elif 'text/plain' in content_type:
        text=raw.decode('utf-8',errors='replace');title=urlsplit(final).hostname
    else:raise ValueError('UNSUPPORTED_SOURCE_FORMAT')
    if len(text.strip())<20:raise ValueError('SOURCE_TOO_THIN')
    # Bound prompt exposure; retain offsets and exact fetched byte identity.
    passages=[];used=0
    for index,line in enumerate(text.splitlines(),1):
        if not line.strip() or len(line)>8000:continue
        if used+len(line)>24000:break
        passages.append({'locator':f'complete extracted paragraph {index}','excerpt':line})
        used+=len(line)
    if not passages:raise ValueError('SOURCE_TOO_THIN')
    return {'status':'usable','requested_url':requested,'url':final,'title':title,'publisher':urlsplit(final).hostname,
            'checked_at':datetime.now(timezone.utc).isoformat(),'content_sha256':hashlib.sha256(raw).hexdigest(),
            'content_type':content_type,'passages':passages,'limitations':('Author-submitted preprint abstract page only; peer review is not established. Abstracts cannot support unstated methods or results. ' if urlsplit(final).hostname=='arxiv.org' else '')+'Extracted page text only; verify relevance, study scope and contradictions. Not evidence of personal experience; no universal or causal claim is implied.'}


@contextmanager
def discovery_rate_slot(url):
    # One host-wide legacy arXiv API connection, at least three seconds apart.
    # Content pages are not the legacy API. All product execution is on this host.
    try:host=urlsplit(url).hostname
    except ValueError:host=None
    if host!='export.arxiv.org':
        yield;return
    directory=Path.home()/'.cache/graham-linkedin';directory.mkdir(parents=True,exist_ok=True)
    with (directory/'arxiv-api.lock').open('a+') as guard:
        fcntl.flock(guard,fcntl.LOCK_EX)
        guard.seek(0)
        try:last=float(guard.read() or '0')
        except ValueError:last=0
        delay=max(0,min(3,3-(time.time()-last)))
        if delay:time.sleep(delay)
        guard.seek(0);guard.truncate();guard.write(str(time.time()));guard.flush()
        yield


def _network_worker(pipe,url,timeout):
    try:
        with discovery_rate_slot(url):
            _network_exchange(pipe,url,timeout)
    except Exception as exc:
        try:pipe.send({'error':str(exc)})
        finally:pipe.close()


def _network_exchange(pipe,url,timeout):
    connection=None
    try:
        u,address=public_address(url)
        port=u.port or (443 if u.scheme=='https' else 80)
        connection=http.client.HTTPConnection(u.hostname,port,timeout=timeout)
        sock=socket.create_connection((address,port),timeout=timeout)
        if u.scheme=='https':sock=ssl.create_default_context().wrap_socket(sock,server_hostname=u.hostname)
        connection.sock=sock
        connection.request('GET',(u.path or '/')+('?' + u.query if u.query else ''),headers={'User-Agent':'GrahamResearch/1.0 public-source qualification','Accept':'text/html,application/xml,application/json,text/plain','Accept-Encoding':'identity'})
        r=connection.getresponse();raw=r.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:raise ValueError('SOURCE_SIZE_LIMIT')
        pipe.send({'status':r.status,'raw':base64.b64encode(raw).decode(),'content_type':r.getheader('Content-Type',''),'location':r.getheader('Location','')})
    except Exception as exc:pipe.send({'error':str(exc)})
    finally:
        if connection:connection.close()
        pipe.close()


def bounded_request(url,timeout):
    # A child process bounds DNS, TLS, headers and slow trickle bodies together.
    ctx=multiprocessing.get_context('fork')
    parent,child=ctx.Pipe(duplex=False)
    process=ctx.Process(target=_network_worker,args=(child,url,timeout),daemon=True);process.start();child.close()
    try:
        if not parent.poll(timeout):raise ValueError('SOURCE_TOTAL_TIMEOUT')
        result=parent.recv()
        if 'error' in result:raise ValueError(result['error'])
        return result
    finally:
        parent.close()
        if process.is_alive():process.terminate()
        process.join(timeout=1)
        if process.is_alive():process.kill();process.join()


class Evidence:
    def __init__(self, deadline=None, *, store=None, job=None):
        self.deadline=deadline or time.time()+900;self.discovery_requests=0;self.source_fetches=0;self.activity=[]
        self.store,self.job=store,job

    def once(self,url,discovery):
        field='discovery_requests' if discovery else 'source_fetches';limit=8 if discovery else 6
        inputs={'url':url,'kind':field}
        if self.store is not None:
            from .operational_store import sha
            with self.store.transaction() as con:
                rows=con.execute('SELECT * FROM stages WHERE job=? AND name LIKE ?',(self.job,'http:'+field+':%')).fetchall()
                for row in rows:
                    if row['input_hash']==sha(inputs) and row['state']=='completed':
                        result=self.store.read_blob(row['result_hash'])
                        self.activity.append({'url':url,'cache_hit':True,'status':result['status']})
                        return result
                # Share only recent successful fetched bytes across canonical jobs. No new HTTP effect.
                cached=con.execute('SELECT stages.result_hash,jobs.created FROM stages JOIN jobs ON jobs.id=stages.job WHERE stages.input_hash=? AND stages.state="completed" AND stages.name LIKE "http:%" ORDER BY jobs.created DESC',(sha(inputs),)).fetchall()
                for row in cached:
                    if time.time()-row['created']>86400:continue
                    value=self.store.read_blob(row['result_hash'])
                    if value.get('status')==200:
                        self.activity.append({'url':url,'cache_hit':True,'status':200,'shared_cache':True,'source_result_hash':row['result_hash']})
                        return value
                if len(rows)>=limit:raise ValueError('EVIDENCE_BUDGET_EXHAUSTED')
                name='http:'+field+':'+str(len(rows)+1)
                con.execute('INSERT INTO stages VALUES (?,?,?,?,NULL)',(self.job,name,sha(inputs),'reserved'))
                setattr(self,field,len(rows)+1)
        else:
            if getattr(self,field)>=limit:raise ValueError('EVIDENCE_BUDGET_EXHAUSTED')
            setattr(self,field,getattr(self,field)+1)
        remaining=self.deadline-time.time()
        if remaining<=0:raise ValueError('WALL_BUDGET_EXHAUSTED')
        began=time.monotonic();result=bounded_request(url,min(15,remaining))
        self.activity.append({'url':url,'status':result['status'],'seconds':time.monotonic()-began,'bytes':len(base64.b64decode(result['raw']))})
        if self.store is not None:self.store.commit_stage(self.job,name,result)
        return result

    def fetch(self,url,*,discovery=False):
        for _ in range(4):
            r=self.once(url,discovery)
            if r['status'] in (301,302,303,307,308):url=urljoin(url,r['location']);continue
            if r['status']!=200:raise ValueError('SOURCE_HTTP_'+str(r['status']))
            return url,base64.b64decode(r['raw']),r['content_type']
        raise ValueError('SOURCE_REDIRECT_LIMIT')

    def discover_crossref(self,topic):
        # Metadata is navigation only; facts must come from separately fetched publisher/author text.
        url='https://api.crossref.org/works?'+urlencode({'query.title':topic,'rows':6,'select':'DOI,title,URL,link,resource,publisher'})
        _,raw,_=self.fetch(url,discovery=True)
        works=json.loads(raw)['message']['items']
        urls=[];seen_works=set()
        for w in works:
            # One representation per work: inaccessible landing/PDF/DOI variants
            # must not crowd all other papers out of the six-fetch admission.
            doi=str(w.get('DOI') or '').strip().lower()
            if doi and doi in seen_works:continue
            if doi:seen_works.add(doi)
            primary=w.get('resource',{}).get('primary',{}).get('URL')
            links=w.get('link',[])
            typed=[(x.get('URL'),str(x.get('content-type') or '').split(';')[0].strip().lower()) for x in links]
            pdf_urls=[u for u,kind in typed if kind=='application/pdf']
            candidates=[primary]+[u for u,kind in typed if kind=='text/html']
            candidates += [u for u,kind in typed if kind not in ('application/pdf','text/html')]+[w.get('URL')]
            for u in candidates:
                if not isinstance(u,str) or not u or u in pdf_urls or u in urls:continue
                try:
                    if urlsplit(u).path.lower().endswith('.pdf'):continue
                except ValueError:continue
                urls.append(u);break
        return urls[:6]

    def discover(self,topic):
        # Both feeds are navigation only; source passages require a separate fetch.
        routes=[]
        try:routes=self.discover_crossref(topic)
        except (ValueError,OSError,http.client.HTTPException,KeyError,TypeError) as exc:
            self.activity.append({'discovery_route':'crossref','error':str(exc)})
        arxiv=[]
        terms=re.findall(r"[A-Za-z0-9]+",topic)[:16]
        if terms:
            query=' AND '.join('all:'+term for term in terms)
            url='https://export.arxiv.org/api/query?'+urlencode({'search_query':query,'start':0,'max_results':3})
            try:
                _,raw,_=self.fetch(url,discovery=True)
                root=ET.fromstring(raw)
                for node in root.findall('{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}id'):
                    value=node.text or ''
                    if re.fullmatch(r'https?://arxiv\.org/abs/(?:[0-9]{4}\.[0-9]{4,5}|[a-z-]+(?:\.[A-Z]{2})?/[0-9]{7})(?:v[0-9]+)?',value):
                        target=value.replace('http://','https://',1)
                        if target not in arxiv:arxiv.append(target)
            except (ValueError,OSError,http.client.HTTPException,ET.ParseError) as exc:
                self.activity.append({'discovery_route':'arxiv','error':str(exc)})
        # Reserve room for both routes; an inaccessible first publisher cannot
        # consume the entire source budget before public author pages get a chance.
        return list(dict.fromkeys(arxiv+routes))[:6]

    def acquire(self,topic,urls=()):
        targets=list(urls) if urls else self.discover(topic)
        sources=[];errors=[]
        for url in targets[:6]:
            try:
                final,raw,kind=self.fetch(url)
                s=source_record(url,final,raw,kind);s['source_id']='S'+str(len(sources)+1);sources.append(s)
            except (ValueError,OSError,http.client.HTTPException) as exc:errors.append({'url':url,'error':str(exc)})
            if self.source_fetches>=6:break
        return {'sources':sources,'errors':errors,'http_activity':self.activity,'discovery_requests':self.discovery_requests,'source_fetches':self.source_fetches}


def validate_meaning(meaning,sources):
    from .editorial_handoff import freeze_handoff
    from .editorial_structure import DEFAULT_BEATS
    freeze_handoff(meaning,{'form':'literal','beats':DEFAULT_BEATS,'symbol':None})
    indexed={s['source_id']:s for s in sources}
    for f in meaning['facts']:
        if any(ref not in indexed for ref in f['source_ids']):raise ValueError('UNSUPPORTED_MEANING')
        # Exact quotation is a conservative first-release claim mapping. Interpretation is in thesis/limits.
        if not all(any(f['text'].strip() in [line.strip() for line in p['excerpt'].splitlines() if line.strip()] for p in indexed[ref]['passages']) for ref in f['source_ids']):raise ValueError('UNSUPPORTED_MEANING')
    return meaning


def resolve_meaning(meaning,sources):
    from copy import deepcopy
    result=deepcopy(meaning);indexed={s['source_id']:s for s in sources}
    for index,fact in enumerate(result.get('facts',[])):
        if set(fact)!={'claim_id','source_id','locator'}:raise ValueError('UNSUPPORTED_MEANING')
        source=indexed.get(fact['source_id'],{})
        matches=[p['excerpt'] for p in source.get('passages',[]) if p['locator']==fact['locator']]
        if len(matches)!=1 or not 1<=len(matches[0])<=600:raise ValueError('UNSUPPORTED_MEANING')
        result['facts'][index]={'claim_id':fact['claim_id'],'text':matches[0],'source_ids':[fact['source_id']]}
    return validate_meaning(result,sources)
