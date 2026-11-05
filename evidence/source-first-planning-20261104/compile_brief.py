from pathlib import Path
import json,hashlib
p=Path('/home/graham/work/linkedin-codex-trial-20261104');e=p/'evidence/source-first-planning-20261104'
plan=json.loads((e/'planner-result.json').read_text())['plan'];sources=json.loads((e/'sources.json').read_text());by={x['source_id']:x for x in sources}
checks=[]
for f in plan['facts']:
 ok=f['exact_excerpt'] in by[f['source_id']]['article'];checks.append(ok)
assert all(checks),checks
review={'reviewer':'assistant source/novelty review','decision':'GO_TO_BOUNDED_PAIR','facts_checked':len(checks),'verbatim_passages_found':all(checks),'assessment':'Same broad authorization thesis independently recovered. Newly usable details include valid credentials on trusted infrastructure, dummy references without records, and concrete validation-stage dependencies. Reader action identifies accountable owners and proposed negative checks. Seven supporting facts and multiple paths may overload a short post; preserve this weakness for actual comparison.','human_approval':None,'scope':'Assistant admission of evidence brief, no human writing approval'}
(e/'brief-review.json').write_text(json.dumps(review,indent=2)+'\n')
data=json.loads((p/'evidence/equal-input-engine-baseline-20261104/request.json').read_text())
data['request_id']='lig-source-first-planning-20261104'
data['topic']='CERT-In financial-sector campaign update'
data['objective']=plan['angle']+' Proposed reader action: '+plan['reader_action']+' Intended sharing: '+plan['forward_who_to_whom_and_why']+' Format: '+plan['format']+' Write140-180 words, with one main point and no sales CTA or generic engagement question.'
data['evidence']=[{'title':f['source_id']+' / evidence '+str(i+1),'url':by[f['source_id']]['url'],'fact':f['claim']} for i,f in enumerate(plan['facts'])]
bundle={'schema_version':'1','request_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'central_claim_id':'C1','sources':[],'claims':[],'planning_brief':plan,'human_approval':None}
for src in sources:
 bundle['sources'].append({'source_id':src['source_id'],'title':src['source_id'],'publisher':'CERT-In / CSIRT-Fin','url':src['url'],'checked_at':'2026-11-04','status':'usable','limitations':'Agency-reported Indian campaign. Public report lacks comparative AI causal measurements, losses, control-effectiveness measurements and restricted indicators. Proposed tests are advice, not observed outcomes.','passages':[{'locator':f['locator'],'excerpt':f['exact_excerpt']} for f in plan['facts'] if f['source_id']==src['source_id']]})
for i,f in enumerate(plan['facts']):bundle['claims'].append({'claim_id':'C'+str(i+1),'kind':'fact','text':f['claim'],'source_ids':[f['source_id']]})
bundle['claims'] += [{'claim_id':'I1','kind':'inference','text':plan['inference'],'source_ids':list(by)},{'claim_id':'O1','kind':'opinion','text':plan['reader_action'],'source_ids':[]}]
for n,v in [('request.json',data),('source-bundle.json',bundle)]:(e/n).write_text(json.dumps(v,indent=2)+'\n')
h=(p/'evidence/equal-input-engine-baseline-20261104/run_comparison.py').read_text().replace('equal-input-engine-baseline-20261104','source-first-planning-20261104')
(e/'run_pair.py').write_text(h)
print('Seven source excerpts verified; pair inputs frozen.')
