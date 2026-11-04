"""Single-subject engine/baseline trial; reads never generate."""
from __future__ import annotations
from functools import partial
import fcntl
import hashlib
import json
from pathlib import Path
import secrets
from datetime import datetime, timezone

from .api import run_generation, _persona_profile
from .contracts import LinkedInContentRequest
from .integration import generate_content
from .llm import LLMClient
from .utils import load_yaml
from .visual_assets import plan_visual_asset

ROOT=Path(__file__).resolve().parents[2]
def now(): return datetime.now(timezone.utc).isoformat()
def digest(body): return hashlib.sha256(body.encode("utf-8")).hexdigest()
def save(path,data):
    temporary=path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
    temporary.replace(path)

def show_trial(directory):
    return json.loads((Path(directory)/"trial.json").read_text())

def voice_context(request):
    return _persona_profile(str(ROOT),load_yaml(str(ROOT/"config/personas.yaml")),
                            request.persona_key,author_pov=request.author_pov)

def run_trial(data,directory,provider,*,model,engine=None):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    with (directory/".trial.lock").open("a+") as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise ValueError("TRIAL_BUSY")
        path=directory/"trial.json"
        if path.exists():
            old=show_trial(directory)
            if old["state"]!="completed": raise ValueError("RECONCILIATION_REQUIRED")
            if old["input"]!=data or old["model"]!=model: raise ValueError("REQUEST_CONFLICT")
            return old
        request=LinkedInContentRequest.model_validate(data)
        record={"schema_version":"1","state":"running","input":data,"model":model,
                "mode":provider.mode,"started_at_utc":now(),"api_spend":0,
                "human_decision":None}
        save(path,record)
        client=LLMClient(model=model,provider=provider)
        try:
            if engine is None:
                result=generate_content(request,
                    generator=partial(run_generation,llm_client=client,opportunity_client=client,publish_quality_client=client),
                    visual_planner=partial(plan_visual_asset,client=client))
                result=result.model_dump()
            else:
                result=engine(request,client=client,visual_planner=partial(plan_visual_asset,client=client))
            record["engine"]=result
            if provider.error: raise provider.error
            selected=result.get("selected_candidate")
            if not selected: raise ValueError("NO_QUALIFIED_CANDIDATE")
            baseline_system=("Write one useful LinkedIn post in the supplied author's voice. Use only supplied facts; "
                             "never invent experience, quotes, statistics or biography. Return only the finished post.")
            baseline_data={"topic":request.topic,"audience":request.audience,"objective":request.objective,
                           "author_pov":request.author_pov,"content_goal":request.content_goal,
                           "evidence":[x.model_dump() for x in request.evidence],
                           "voice":voice_context(request),
                           "approved_voice_examples":[x.model_dump() for x in request.voice_examples],
                           "format_rules":load_yaml(str(ROOT/"config/prompt_kit.config.yaml"))}
            baseline_user=json.dumps(baseline_data,ensure_ascii=False)
            baseline=client.call(baseline_system,baseline_user)["text"]
            record["baseline"]={"body":baseline,"content_sha256":digest(baseline),
                                "system":baseline_system,"user":baseline_data}
            pairs=[("engine",selected["body"]),("baseline",baseline)]
            secrets.SystemRandom().shuffle(pairs)
            mapping={label:method for label,(method,body) in zip(("A","B"),pairs)}
            review={"candidates":{label:{"body":body,"content_sha256":digest(body)}
                                 for label,(method,body) in zip(("A","B"),pairs)},
                    "human_decision":None}
            save(directory/"blind-mapping.json",mapping)
            save(directory/"review.json",review)
            text="# LinkedIn writing comparison\n\nHuman review pending. Labels are randomized.\n"
            for label,c in review["candidates"].items(): text+=f"\n## Draft {label}\n\n{c['body']}\n"
            text+="\n## Review\n\nChoose A, B or tie; mark keep/light/structural/reject, voice/insight/usefulness 1–5 and actual editing minutes.\n"
            (directory/"review.md").write_text(text)
            record.update(state="completed",review=review)
        except Exception as exc:
            code=getattr(exc,"code",str(exc))
            record.update(state="unknown" if code=="CODEX_COMPLETION_UNKNOWN" else "failed",error_code=code)
            raise
        finally:
            record.update(finished_at_utc=now(),provider_receipts=provider.receipts)
            save(path,record)
        return record
