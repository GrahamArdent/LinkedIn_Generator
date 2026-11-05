from pathlib import Path
import json,secrets,sys,importlib.util
e=Path('evidence/eight-workflow-trial-20261104')
spec=importlib.util.spec_from_file_location('runner',e/'run.py');r=importlib.util.module_from_spec(spec);sys.argv=['second_review.py','audit'];spec.loader.exec_module(r)
names=['second-hybrid','second-single','second-simple']
drafts={n:json.loads((e/(n+'.json')).read_text()) for n in names}
assert all(d['state']=='completed' for d in drafts.values())
m=e/'second-review-mapping.json'
if m.exists():mapping=json.loads(m.read_text())
else:
 secrets.SystemRandom().shuffle(names);mapping={f'S{i+1:02}':n for i,n in enumerate(names)};r.save(m,mapping)
blind={k:drafts[n]['output'] for k,n in mapping.items()}
(e/'SECOND_CONCEPT_REVIEW.md').write_text('# Second-concept private review\n\nQuestion: What evidence should an organization require before declaring incident remediation complete?\n\nHuman preferences pending. No winner is declared.\n\n'+'\n\n'.join('## '+k+'\n\n'+v for k,v in blind.items())+'\n\nRecord factual support, relevance, usefulness, required edits and actual editing time.\n')
provider=r.CodexProvider(r.CodexConfig(**r.cfg),e/'attempts','eight-controls')
r.call(provider,'second-audit','Audit these three anonymous second-concept drafts against the supplied sources. Assess factual support, relevance to the remediation-completion question, actionable usefulness, narrative differences and editing effort (estimates only). Identify thematic drift. Do not declare a winner or infer human preference. Return JSON artifact with per-draft findings and bounded transfer conclusions.',{'question':'What evidence should an organization require before declaring incident remediation complete?','drafts':blind,'sources':r.packet['sources'],'human_preference':None})
print('Second-concept blinded audit complete')
