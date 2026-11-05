"""Offline audit of retained prompt/native/result boundaries. Launches no model."""
import json,hashlib,collections,pathlib,copy
ROOT=pathlib.Path(__file__).resolve().parents[2]
E=ROOT/'evidence/controlled-voice-comparison-20261104'
def sha(b):return hashlib.sha256(b).hexdigest()
def check_native(item,binding,attempt,result,raw):
    assert sha(raw)==attempt['request_sha256'],'native request binding mismatch'
    assert binding['request']['task']==item['prepared']['system'],'native system mismatch'
    assert binding['request']['input']==item['prepared']['user'],'native user mismatch'
    assert result['text']==item['body'],'native output mismatch'
    assert attempt['state']=='succeeded' and attempt['execution_kind']=='native_cli'
    assert item['provider_receipts'][0]['cache_hit'] is False,'cache hit'
m=json.loads((E/'manifest.json').read_text()); rows=[]; threads=[]; objectives=[]
for prepared in m['prepared']:
    item=json.loads((E/(prepared['style']+'.json')).read_text())
    aid=item['provider_receipts'][0]['attempt_id']
    ap=next(p for p in E.rglob('attempt.json') if json.loads(p.read_text())['attempt_id']==aid)
    a=json.loads(ap.read_text());raw=ap.with_name('request.json').read_bytes();b=json.loads(raw);r=json.loads(ap.with_name('final.json').read_text())
    check_native(item,b,a,r,raw)
    p=json.loads(next(x.split(': ',1)[1] for x in prepared['user'].splitlines() if x.startswith('Persona Profile: ')))
    plan=json.loads(next(x.split(': ',1)[1] for x in prepared['user'].splitlines() if x.startswith('Editorial Plan: ')))
    objective=prepared['request']['objective']
    repeated=[objective,plan['takeaway'],p['editorial_context']['objective'],p['editorial_context']['plan']['takeaway']]
    assert all(x==objective for x in repeated)
    assert p['writing_voice']==prepared['voice']
    ts=[x['thread_id'] for x in a['events'] if x.get('type')=='thread.started'];assert len(ts)==1;threads+=ts
    # Prove the audit rejects a mismatched model-bound prompt and a substituted output.
    failures=[]
    for field in ['input','output']:
        bad=copy.deepcopy(b);br=copy.deepcopy(r)
        if field=='input': bad['request']['input']='wrong voice/prompt'
        else:br['text']='substituted output'
        try:check_native(item,bad,a,br,raw)
        except AssertionError:failures.append(field)
    assert failures==['input','output']
    rows.append({'style':prepared['style'],'attempt_id':aid,'thread_id':ts[0],
       'native_request_sha256':a['request_sha256'],'body_sha256':sha(item['body'].encode()),
       'prompt_chars':len(prepared['system'])+len(prepared['user']),
       'selected_traits_chars':len(json.dumps(prepared['voice']['style_traits'])),
       'inherited_default_style_chars':len(json.dumps({k:p[k] for k in ['voice_authority','spoken_voice']})),
       'inherited_default_style_blocks':all(k in p for k in ['voice_authority','spoken_voice']),
       'objective_semantic_copies':len(repeated),'approval_screen_mentions_in_user':prepared['user'].lower().count('approval screen'),
       'opening':item['body'].split('\n\n')[0],'factual_paragraph':item['body'].split('\n\n')[1],
       'cache_hit':False,'boundary_checks':'PASS','mutation_controls':'PASS'})
assert len(set(threads))==9
result={'audit':'offline; no model launch','rows':rows,'unique_native_threads':len(set(threads)),
'unique_native_request_hashes':len({x['native_request_sha256'] for x in rows}),
'unique_body_hashes':len({x['body_sha256'] for x in rows}),
'opening_prefix_shared_count':sum(x['opening'].startswith('An approval screen') for x in rows),
'exact_opening_counts':dict(collections.Counter(x['opening'] for x in rows)),
'exact_factual_paragraph_counts':dict(collections.Counter(x['factual_paragraph'] for x in rows)),
'new_model_calls':0}
(ROOT/'evidence/voice-convergence-diagnosis-20261105/observations.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
print('PROMPT METRICS',json.dumps(rows[0],indent=2))
