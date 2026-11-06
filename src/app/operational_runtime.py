"""Live supported-model observation; never infer an alias or select a fallback."""
import json
import select
import subprocess
import time


def model_list():
    process=subprocess.Popen(['codex','app-server','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    try:
        for message in ({'id':1,'method':'initialize','params':{'clientInfo':{'name':'graham-authoring','version':'1'}}},
                        {'method':'initialized'},{'id':2,'method':'model/list','params':{'includeHidden':True}}):
            process.stdin.write(json.dumps(message)+'\n');process.stdin.flush()
        deadline=time.monotonic()+20
        while time.monotonic()<deadline:
            if select.select([process.stdout],[],[],min(1,deadline-time.monotonic()))[0]:
                line=process.stdout.readline()
                if not line:break
                response=json.loads(line)
                if response.get('id')==2:
                    result=response.get('result',{})
                    if result.get('nextCursor'):raise ValueError('MODEL_LIST_INCOMPLETE')
                    if not isinstance(result.get('data'),list):raise ValueError('MODEL_LIST_UNAVAILABLE')
                    return result['data']
        raise ValueError('MODEL_LIST_UNAVAILABLE')
    finally:
        process.terminate()
        try:process.wait(timeout=3)
        except subprocess.TimeoutExpired:process.kill();process.wait()


def select_model(requested,models,reasoning='medium'):
    matched=[m for m in models if m.get('id')==requested and m.get('model')==requested]
    if len(matched)!=1:raise ValueError('REQUESTED_MODEL_UNAVAILABLE: '+requested)
    if reasoning not in [x['reasoningEffort'] for x in matched[0].get('supportedReasoningEfforts',[])]:raise ValueError('REQUESTED_REASONING_UNAVAILABLE')
    return requested


def qualify_model(config):
    models=model_list();select_model(config.model,models,config.reasoning)
    return {'model':config.model,'reasoning':config.reasoning,'supported_models':[m['id'] for m in models]}
