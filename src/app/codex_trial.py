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
from .publish_quality import assess_publish_quality
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

def validate_trial_evidence(data, bundle):
    """Qualify a frozen trial brief before constructing a provider.

    This checks recorded support, not source truth. Human/research review owns
    whether a passage actually entails the claim. Legacy requests stay valid.
    """
    frozen = digest(json.dumps(data, sort_keys=True, ensure_ascii=False))
    if bundle.get("request_sha256") != frozen:
        raise ValueError("EVIDENCE_REQUEST_MISMATCH")
    sources = {s["source_id"]: s for s in bundle.get("sources", [])}
    claims = bundle.get("claims", [])
    central = next((c for c in claims if c.get("claim_id") == bundle.get("central_claim_id")), None)
    if not central or central.get("kind") not in {"fact", "observation"}:
        raise ValueError("EVIDENCE_SUPPORT_REQUIRED: central factual anchor")
    facts = {s.get("fact") for s in data.get("evidence", [])}
    for claim in claims:
        if claim.get("kind") not in {"fact", "observation", "inference", "opinion"}:
            raise ValueError("EVIDENCE_SUPPORT_REQUIRED: unknown claim kind")
        refs = claim.get("source_ids", [])
        if claim.get("kind") in {"fact", "observation"} and (not refs or claim.get("text") not in facts):
            raise ValueError("EVIDENCE_SUPPORT_REQUIRED: unmapped fact")
        for ref in refs:
            source = sources.get(ref, {})
            if source.get("status") != "usable" or not source.get("checked_at") or not source.get("limitations"):
                raise ValueError("EVIDENCE_SUPPORT_REQUIRED: missing, stale or contradictory source")

def run_trial(data,directory,provider,*,model,engine=None,resume_comparison=False,score_baseline=False):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    with (directory/".trial.lock").open("a+") as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise ValueError("TRIAL_BUSY")
        path=directory/"trial.json"
        retained=None
        if path.exists():
            old=show_trial(directory)
            if old["input"]!=data or old.get("model",model)!=model: raise ValueError("REQUEST_CONFLICT")
            if old["state"]=="completed": return old
            if (resume_comparison and old["state"]=="failed"
                    and old.get("error_code")=="NO_QUALIFIED_CANDIDATE"
                    and old.get("engine",{}).get("body")):
                retained=old["engine"]
                if not (directory/"engine-gate-failure.json").exists():
                    save(directory/"engine-gate-failure.json",old)
            else:
                raise ValueError("RECONCILIATION_REQUIRED")
        request=LinkedInContentRequest.model_validate(data)
        record={"schema_version":"1","state":"running","input":data,"model":model,
                "mode":provider.mode,"started_at_utc":now(),"api_spend":0,
                "human_decision":None}
        if retained is not None: record["engine_origin"]="engine-gate-failure.json"
        save(path,record)
        client=LLMClient(model=model,provider=provider)
        try:
            if retained is not None:
                result=retained
            elif engine is None:
                result=generate_content(request,
                    generator=partial(run_generation,llm_client=client,opportunity_client=client,publish_quality_client=client),
                    visual_planner=partial(plan_visual_asset,client=client))
                result=result.model_dump()
            else:
                result=engine(request,client=client,visual_planner=partial(plan_visual_asset,client=client))
            record["engine"]=result
            if provider.error: raise provider.error
            selected=result.get("selected_candidate")
            if not selected:
                if retained is None: raise ValueError("NO_QUALIFIED_CANDIDATE")
                # Comparison material only. Never promote it to selected/ready.
                selected={"body":retained["body"]}
                record["engine_gate"]="HOLD_NO_QUALIFIED_CANDIDATE"
            else:
                record["engine_gate"]="QUALIFIED_FOR_HUMAN_REVIEW"
            baseline_system=("Write one useful LinkedIn post in the supplied author's voice. Use only supplied facts; "
                             "never invent experience, quotes, statistics or biography. Return only the finished post.")
            baseline_data={"topic":request.topic,"audience":request.audience,"objective":request.objective,
                           "author_pov":request.author_pov,"content_goal":request.content_goal,
                           "services":request.services,"targets":request.targets,"hashtags":request.hashtags,
                           "evidence":[x.model_dump() for x in request.evidence],
                           "voice":voice_context(request),
                           "approved_voice_examples":[x.model_dump() for x in request.voice_examples],
                           "format_rules":load_yaml(str(ROOT/"config/prompt_kit.config.yaml"))}
            baseline_user=json.dumps(baseline_data,ensure_ascii=False)
            baseline=client.call(baseline_system,baseline_user)["text"]
            record["baseline"]={"body":baseline,"content_sha256":digest(baseline),
                                "system":baseline_system,"user":baseline_data}
            if score_baseline:
                context = result.get("review", {}).get("evaluation_context")
                if not isinstance(context, dict):
                    raise ValueError("BASELINE_EVALUATION_CONTEXT_MISSING")
                quality = assess_publish_quality(
                    text=baseline, audience=request.audience,
                    content_goal=result.get("telemetry", {}).get("content_goal") or request.content_goal,
                    evidence=[x.model_dump() for x in request.evidence],
                    persona_profile=context, client=client,
                )
                record["baseline"]["quality"] = quality.as_dict()
                if provider.error: raise provider.error
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

def complete_comparison(data,directory,provider,*,model,score_baseline=False):
    """Finish only the baseline after a known retained quality rejection."""
    return run_trial(data,directory,provider,model=model,resume_comparison=True,score_baseline=score_baseline)
