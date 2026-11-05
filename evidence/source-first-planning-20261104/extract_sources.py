from pathlib import Path
import json,re,urllib.request,hashlib,datetime
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=False
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip=True
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=False
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
p=Path('/home/graham/work/linkedin-codex-trial-20261104/evidence/source-first-planning-20261104');sources=[]
for code in ['CIAD-2026-0046','CIAD-2026-0058']:
 url='https://www.cert-in.org.in/s2cMainServlet?VLCODE='+code+'&pageid=PUBVLNOTES02';f=p/(code+'.html')
 raw=f.read_bytes() if f.exists() else urllib.request.urlopen(url,timeout=25).read();f.write_bytes(raw)
 t=Text();t.feed(raw.decode());text=re.sub(r'\s+',' ',' '.join(t.parts));start=text.index(code);end=text.index('Disclaimer',start)
 article=text[start:end].strip();(p/(code+'.txt')).write_text(article)
 sources.append({'source_id':code,'url':url,'article':article,'html_sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256(article.encode()).hexdigest(),'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'extraction':'stdlib HTMLParser, normalize whitespace, heading advisory ID through before disclaimer, full editorial body'})
(p/'sources.json').write_text(json.dumps(sources,indent=2)+'\n');print([(x['source_id'],len(x['article'])) for x in sources])
