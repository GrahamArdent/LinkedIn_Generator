"""Actual no-model preparation and pre-dispatch/replay boundaries.

Breaks caught: omitted/default-overwritten narrative, unsupported fact/source,
mutable bindings, provider construction before validation and legacy regeneration.
"""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]

def fixture():
    fact='The study found that explanations did not always improve appropriate reliance.'
    data={'request_id':'structure-fixture','origin':'test','topic':'Trust and understanding',
          'persona_key':'graham','writing_voice_id':'concise_challenger','opportunity_gate':False,
          'visual_asset_plan':False,'evidence':[{'title':'Fixture study','fact':fact}],
          'editorial_handoff':{'meaning':{'thesis':'Confidence deserves a separate question from understanding.',
           'reader_consequence':'Ask what would change your reliance.',
           'facts':[{'claim_id':'F1','text':fact,'source_ids':['S1']}],
           'qualification':'A controlled study does not describe every current chatbot.'}}}
    bundle={'sources':[{'source_id':'S1','title':'Fixture study','publisher':'Fixture research',
       'record':'fixture-only','status':'usable','checked_at':'2026-11-05','limitations':'Controlled setting only.',
       'passages':[{'locator':'result','excerpt':fact}]}],
       'claims':[{'claim_id':'F1','kind':'fact','text':fact,'source_ids':['S1']}], 'central_claim_id':'F1'}
    bundle['request_sha256']=hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    return data,bundle

def module():
    from src.app import editorial_structure
    return editorial_structure

def test_preparation_compiles_default_and_keeps_source_records_without_mutation():
    data,bundle=fixture();before=copy.deepcopy((data,bundle))
    prepared,bound=module().prepare_graham_request(data,bundle)
    assert prepared['editorial_handoff']['narrative']=={'form':'literal','beats':[
        'Hook: introduce the central question.', 'Tension: develop why the question matters.',
        'Evidence: place the relevant sourced facts.', "Interpretation: develop Graham's reading and its limits.",
        'Landing: earn the closing thought from the argument.'], 'symbol':None}
    assert (data,bundle)==before
    assert bound['sources']==bundle['sources']
    assert bound['structure_preparation']['provenance']=='default'
    assert module().prepare_graham_request(data,bundle)==(prepared,bound)
    module().validate_prepared_request(prepared,bound)

def test_explicit_alternate_narrative_is_preserved():
    data,bundle=fixture();n={'form':'literal','beats':['Start with the implication.','Explore the uncertainty.'],'symbol':None}
    data['editorial_handoff']['narrative']=n
    bundle['request_sha256']=hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    prepared,bound=module().prepare_graham_request(data,bundle)
    assert prepared['editorial_handoff']['narrative']==n
    assert bound['structure_preparation']['provenance']=='caller-selected'

@pytest.mark.parametrize('change',['meaning','evidence','persona','fact','source'])
def test_invalid_preparation_stops_without_provider(change):
    data,bundle=fixture()
    if change=='meaning':del data['editorial_handoff']['meaning']
    elif change=='evidence':bundle=None
    elif change=='persona':data['persona_key']='ardent'
    elif change=='fact':data['editorial_handoff']['meaning']['facts'][0]['text']='Invented fact.'
    else:data['editorial_handoff']['meaning']['facts'][0]['source_ids']=['OTHER']
    with pytest.raises(ValueError):module().prepare_graham_request(data,bundle)

def cli(tmp_path,action,data=None,bundle=None,out=None):
    argv=[sys.executable,str(ROOT/'scripts/linkedin_codex_trial.py'),action,'--out',str(out or tmp_path/'out')]
    if data is not None:
        (tmp_path/'input.json').write_text(json.dumps(data));argv+=['--request',str(tmp_path/'input.json')]
    if bundle is not None:
        (tmp_path/'bundle.json').write_text(json.dumps(bundle));argv+=['--evidence-bundle',str(tmp_path/'bundle.json')]
    # Nonexistent client paths are a tripwire. Preparation/replay must not invoke them.
    cfg={'resume_root':'/nonexistent-resume','python':'/nonexistent-python','source_sha':'none','model':'fixture'}
    (tmp_path/'config.json').write_text(json.dumps(cfg))
    if action!='prepare':argv+=['--config',str(tmp_path/'config.json')]
    return subprocess.run(argv,text=True,capture_output=True,cwd=ROOT)

def test_public_prepare_is_no_model_idempotent_and_rejects_overwrite(tmp_path):
    data,bundle=fixture();r=cli(tmp_path,'prepare',data,bundle)
    assert r.returncode==0,r.stderr
    out=tmp_path/'out';assert not (out/'trial.json').exists()
    before={p.name:(p.read_bytes(),p.stat().st_mtime_ns) for p in out.iterdir() if p.is_file()}
    assert cli(tmp_path,'prepare',data,bundle).returncode==0
    assert before=={p.name:(p.read_bytes(),p.stat().st_mtime_ns) for p in out.iterdir() if p.is_file()}
    data['topic']='Different'
    assert cli(tmp_path,'prepare',data,bundle).returncode==2
    assert before=={p.name:(p.read_bytes(),p.stat().st_mtime_ns) for p in out.iterdir() if p.is_file()}

@pytest.mark.parametrize('change',['missing','beat','definition','version','bundle','request'])
def test_normal_generate_rejects_missing_or_stale_preparation_before_dispatch(tmp_path,change):
    data,bundle=module().prepare_graham_request(*fixture())
    if change=='missing':bundle.pop('structure_preparation')
    elif change=='beat':data['editorial_handoff']['narrative']['beats'][0]='Changed selected beat.'
    elif change=='definition':bundle['structure_preparation']['definition_sha256']='0'*64
    elif change=='version':bundle['structure_preparation']['version']=999
    elif change=='bundle':bundle['sources'][0]['limitations']='Changed limits.'
    else:data['audience']='A different reader'
    r=cli(tmp_path,'generate',data,bundle)
    assert r.returncode==2
    assert 'STRUCTURE_PREPARATION' in r.stderr,r.stderr
    assert not (tmp_path/'out'/'codex-attempts').exists()
    assert not (tmp_path/'out'/'trial.json').exists()

def test_historical_completed_cli_replay_after_definition_change_is_immutable(tmp_path,monkeypatch):
    from src.app.codex_trial import run_trial
    data,_=fixture();data.pop('editorial_handoff')
    out=tmp_path/'out';out.mkdir()
    old={'state':'completed','input':data,'model':'fixture','mode':'native_codex',
         'evidence_bundle_sha256':None,'score_baseline':False,'engine_gate':'HOLD_NO_QUALIFIED_CANDIDATE'}
    raw=json.dumps(old).encode();(out/'trial.json').write_bytes(raw)
    monkeypatch.setattr(module(),'STRUCTURE_VERSION',999)
    r=cli(tmp_path,'generate',data,out=out)
    assert r.returncode==0,r.stderr
    assert (out/'trial.json').read_bytes()==raw
    assert cli(tmp_path,'show',out=out).returncode==0
    data['topic']='Changed'
    r=cli(tmp_path,'generate',data,out=out)
    assert r.returncode==2 and 'REQUEST_CONFLICT' in r.stderr
    assert (out/'trial.json').read_bytes()==raw

def test_subprocess_prepared_structure_reaches_actual_writer_rewrite_review_and_control(tmp_path):
    data,bundle=fixture();r=cli(tmp_path,'prepare',data,bundle)
    assert r.returncode==0,r.stderr
    out=tmp_path/'trial';capture=tmp_path/'calls.json';prepared=tmp_path/'out'
    argv=[str(ROOT/'scripts/linkedin_codex_trial.py'),'generate','--out',str(out),
          '--request',str(prepared/'request.json'),'--evidence-bundle',str(prepared/'source-bundle.json'),
          '--config',str(tmp_path/'config.json')]
    # Only the external provider boundary is injected; actual CLI/API/writer/rewrite/evaluator/control run.
    bootstrap='''
import json,runpy,sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()/'tests'))
from test_publish_quality_review import ORIGINAL,REWRITE
from test_essential_review_gate import judgment
from src.app.codex_provider import CodexProvider
capture=Path(sys.argv[1]);args=json.loads(sys.argv[2]);calls=[];reviews=0
def generate(self,**kw):
 global reviews
 calls.append(kw);capture.write_text(json.dumps(calls))
 if 'strict LinkedIn publish-quality evaluator' in kw['system']:
  reviews+=1
  return json.dumps(judgment(rating=5, failure='argument_voice' if reviews==1 else None))
 if 'one bounded publish-quality rewrite' in kw['system']:return REWRITE
 return ORIGINAL
CodexProvider.generate=generate
sys.argv=args
runpy.run_path(args[0],run_name='__main__')
'''
    r=subprocess.run([sys.executable,'-c',bootstrap,str(capture),json.dumps(argv)],text=True,capture_output=True,cwd=ROOT)
    assert r.returncode==0,r.stderr
    calls=json.loads(capture.read_text());saved=json.loads((out/'trial.json').read_text())
    handoff=json.loads((prepared/'request.json').read_text())['editorial_handoff']
    writer=next(c for c in calls if 'Write a LinkedIn post as' in c['system'])
    profile=json.loads(next(x for x in writer['user'].splitlines() if x.startswith('Persona Profile: ')).split(': ',1)[1])
    assert profile['editorial_context']['handoff']==handoff
    rewrite=next(c for c in calls if 'one bounded publish-quality rewrite' in c['system'])
    assert handoff['meaning']['qualification'] in rewrite['user']
    for beat in handoff['narrative']['beats']:assert beat in rewrite['user']
    reviews=[json.loads(c['user']) for c in calls if 'strict LinkedIn publish-quality evaluator' in c['system']]
    assert len(reviews)==2
    assert all(x['editorial_brief']['handoff']==handoff for x in reviews)
    assert saved['baseline']['user']['editorial_handoff']==handoff
    assert saved['engine']['selected_candidate']['source']=='rewrite'
    assert saved['engine']['review']['original']['essential_checks']['argument_voice']['verdict']=='revise'
    assert saved['evidence_bundle']['structure_preparation']==json.loads((prepared/'source-bundle.json').read_text())['structure_preparation']
    # Same sources/meaning, different caller-selected beat changes the actual writer prompt.
    other=copy.deepcopy(data);other['editorial_handoff']['narrative']={'form':'literal','beats':['Explore the implication first.'],'symbol':None}
    b=copy.deepcopy(bundle);b['request_sha256']=hashlib.sha256(json.dumps(other,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    q,source=module().prepare_graham_request(other,b)
    (tmp_path/'second.json').write_text(json.dumps(q));(tmp_path/'second-bundle.json').write_text(json.dumps(source))
    argv[argv.index(str(prepared/'request.json'))]=str(tmp_path/'second.json')
    argv[argv.index(str(prepared/'source-bundle.json'))]=str(tmp_path/'second-bundle.json')
    argv[argv.index(str(out))]=str(tmp_path/'second-trial')
    r=subprocess.run([sys.executable,'-c',bootstrap,str(capture),json.dumps(argv)],text=True,capture_output=True,cwd=ROOT)
    assert r.returncode==0,r.stderr
    changed=next(c for c in json.loads(capture.read_text()) if 'Write a LinkedIn post as' in c['system'])
    assert changed['user']!=writer['user'] and 'Explore the implication first.' in changed['user']

def test_cli_unknown_result_reconciles_original_without_another_dispatch(tmp_path):
    data,bundle=module().prepare_graham_request(*fixture())
    assert cli(tmp_path,'prepare',data,bundle).returncode==0
    out=tmp_path/'trial';counter=tmp_path/'dispatches'
    argv=[str(ROOT/'scripts/linkedin_codex_trial.py'),'generate','--out',str(out),
       '--request',str(tmp_path/'out/request.json'),'--evidence-bundle',str(tmp_path/'out/source-bundle.json'),
       '--config',str(tmp_path/'config.json')]
    script='''
import json,runpy,sys
from pathlib import Path
from src.app.codex_provider import CodexProvider,CodexError
counter=Path(sys.argv[1]);args=json.loads(sys.argv[2])
def dispatch(self,**kw):
 counter.write_text(counter.read_text()+'dispatch\\n' if counter.exists() else 'dispatch\\n')
 raise CodexError('CODEX_COMPLETION_UNKNOWN','original-attempt')
CodexProvider.generate=dispatch
sys.argv=args
runpy.run_path(args[0],run_name='__main__')
'''
    invoke=lambda:subprocess.run([sys.executable,'-c',script,str(counter),json.dumps(argv)],cwd=ROOT,text=True,capture_output=True)
    first=invoke();assert first.returncode==2 and 'CODEX_COMPLETION_UNKNOWN' in first.stderr
    saved=(out/'trial.json').read_bytes();assert json.loads(saved)['state']=='unknown'
    second=invoke();assert second.returncode==2 and 'RECONCILIATION_REQUIRED' in second.stderr
    assert counter.read_text()=='dispatch\n' and (out/'trial.json').read_bytes()==saved
    data['editorial_handoff']['narrative']['beats'][0]='Changed under same identity.'
    (tmp_path/'out/request.json').write_text(json.dumps(data))
    changed=invoke();assert changed.returncode==2 and 'REQUEST_CONFLICT' in changed.stderr
    assert counter.read_text()=='dispatch\n' and (out/'trial.json').read_bytes()==saved


def test_prepared_completed_cli_replays_even_after_current_structure_definition_changes(tmp_path):
    data,bundle=module().prepare_graham_request(*fixture());out=tmp_path/'out';out.mkdir()
    old={'state':'completed','input':data,'model':'fixture','mode':'native_codex','score_baseline':False,
        'evidence_bundle_sha256':hashlib.sha256(json.dumps(bundle,sort_keys=True,ensure_ascii=False).encode()).hexdigest()}
    raw=json.dumps(old).encode();(out/'trial.json').write_bytes(raw)
    (tmp_path/'request.json').write_text(json.dumps(data));(tmp_path/'sources.json').write_text(json.dumps(bundle))
    (tmp_path/'config.json').write_text(json.dumps({'resume_root':'/absent','python':'/absent','source_sha':'x','model':'fixture'}))
    args=[str(ROOT/'scripts/linkedin_codex_trial.py'),'generate','--out',str(out),
          '--request',str(tmp_path/'request.json'),'--evidence-bundle',str(tmp_path/'sources.json'),
          '--config',str(tmp_path/'config.json')]
    bootstrap='''
import runpy,sys,json
from src.app import editorial_structure as s
from src.app import codex_provider as p
s.STRUCTURE_VERSION=999
s.DEFAULT_BEATS=['New active policy']
def forbidden(*a,**kw):raise AssertionError('provider construction forbidden on read')
p.CodexProvider=forbidden
sys.argv=json.loads(sys.argv[1])
runpy.run_path(sys.argv[0],run_name='__main__')
'''
    r=subprocess.run([sys.executable,'-c',bootstrap,json.dumps(args)],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==0,r.stderr
    assert (out/'trial.json').read_bytes()==raw
