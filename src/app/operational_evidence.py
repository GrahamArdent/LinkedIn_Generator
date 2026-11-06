"""Bounded public evidence acquisition. Network content is never authority."""
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import http.client
import ipaddress
import json
import socket
import ssl
import time
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
    passages=[{'locator':f'extracted characters {i}:{min(i+4000,len(text))}', 'excerpt':text[i:i+4000]} for i in range(0,min(len(text),24000),4000)]
    return {'status':'usable','requested_url':requested,'url':final,'title':title,'publisher':urlsplit(final).hostname,
            'checked_at':datetime.now(timezone.utc).isoformat(),'content_sha256':hashlib.sha256(raw).hexdigest(),
            'content_type':content_type,'passages':passages,'limitations':'Extracted page text only; verify relevance, study scope and contradictions. Not evidence of personal experience; no universal or causal claim is implied.'}


class Evidence:
    def __init__(self, deadline=None):
        self.deadline=deadline or time.time()+900;self.discovery_requests=0;self.source_fetches=0;self.activity=[]

    def fetch(self,url,*,discovery=False):
        original=url
        for _ in range(4):
            if time.time()>=self.deadline:raise ValueError('WALL_BUDGET_EXHAUSTED')
            field='discovery_requests' if discovery else 'source_fetches';limit=8 if discovery else 6
            if getattr(self,field)>=limit:raise ValueError('EVIDENCE_BUDGET_EXHAUSTED')
            setattr(self,field,getattr(self,field)+1)
            u,address=public_address(url)
            port=u.port or (443 if u.scheme=='https' else 80)
            connection=http.client.HTTPConnection(u.hostname,port,timeout=min(15,max(0.1,self.deadline-time.time())))
            # Pin the connection to the validated address, preserving TLS SNI/hostname validation.
            sock=socket.create_connection((address,port),timeout=connection.timeout)
            if u.scheme=='https':sock=ssl.create_default_context().wrap_socket(sock,server_hostname=u.hostname)
            connection.sock=sock
            began=time.monotonic()
            try:
                connection.request('GET',(u.path or '/')+('?' + u.query if u.query else ''),headers={'User-Agent':'GrahamResearch/1.0 public-source qualification','Accept':'text/html,application/xml,application/json,text/plain','Accept-Encoding':'identity'})
                r=connection.getresponse();raw=r.read(MAX_BYTES+1)
                self.activity.append({'url':url,'status':r.status,'seconds':time.monotonic()-began,'bytes':len(raw)})
                if len(raw)>MAX_BYTES:raise ValueError('SOURCE_SIZE_LIMIT')
                if r.status in (301,302,303,307,308):
                    url=urljoin(url,r.getheader('Location') or '');continue
                if r.status!=200:raise ValueError('SOURCE_HTTP_'+str(r.status))
                return url,raw,r.getheader('Content-Type','')
            finally:connection.close()
        raise ValueError('SOURCE_REDIRECT_LIMIT')

    def discover(self,topic):
        # Metadata is navigation only; facts must come from separately fetched publisher/author text.
        url='https://api.crossref.org/works?'+urlencode({'query.title':topic,'rows':6,'select':'DOI,title,URL,link,resource,publisher'})
        _,raw,_=self.fetch(url,discovery=True)
        works=json.loads(raw)['message']['items']
        urls=[]
        for w in works:
            primary=w.get('resource',{}).get('primary',{}).get('URL')
            for u in [primary]+[x.get('URL') for x in w.get('link',[])]+[w.get('URL')]:
                if u and u not in urls:urls.append(u)
        return urls[:6]

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
        if not all(any(f['text'] in p['excerpt'] for p in indexed[ref]['passages']) for ref in f['source_ids']):raise ValueError('UNSUPPORTED_MEANING')
    return meaning
