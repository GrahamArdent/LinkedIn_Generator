"""Thin subscription-only bridge to the existing Resume Codex client."""
from __future__ import annotations
import asyncio
from dataclasses import dataclass, asdict
import json
import os
from pathlib import Path
import subprocess
import sys
import time

@dataclass(frozen=True)
class CodexConfig:
    resume_root: Path
    python: Path
    source_sha: str
    model: str
    reasoning: str = "medium"

class CodexError(RuntimeError):
    def __init__(self, code, attempt_id=None):
        self.code, self.attempt_id = code, attempt_id
        super().__init__(code)

class CodexProvider:
    mode = "native_codex"
    def __init__(self, config, directory, run_id, *, runner=None):
        self.config, self.directory, self.run_id = config, Path(directory).resolve(), run_id
        self.runner = runner or subprocess.run
        self.receipts, self.error = [], None

    def reconcile(self, **args):
        text=self._invoke(operation="recover_only",**args)
        if not self.receipts[-1].get("cache_hit"):
            raise CodexError("CODEX_RECONCILIATION_REQUIRED")
        return {"text":text,"receipt":self.receipts[-1]}

    def generate(self, **args):
        return self._invoke(operation="execute",**args)

    def _invoke(self, *, operation, model, system, user, temperature):
        if self.error:
            raise self.error
        if model != self.config.model:
            raise CodexError("CODEX_MODEL_MISMATCH")
        payload = {**{k:str(v) for k,v in asdict(self.config).items()},
                   "directory":str(self.directory),"run_id":self.run_id,
                   "system":system,"user":user,"requested_temperature":temperature,"operation":operation,
                   "remaining_wall_seconds":max(0.1,getattr(self,"deadline",time.time()+920)-time.time())}
        # Credentials stay in Codex's own authentication store.
        env = {k:os.environ[k] for k in ("HOME","PATH","CODEX_HOME","LANG","SSL_CERT_FILE") if k in os.environ}
        argv = [str(self.config.python),str(Path(__file__).resolve()),"--bridge"]
        try:
            completed = self.runner(argv,input=json.dumps(payload),text=True,capture_output=True,
                                    timeout=min(920,payload["remaining_wall_seconds"]),env=env)
            result = json.loads(completed.stdout)
            if not isinstance(result,dict) or type(result.get("ok")) is not bool:
                raise CodexError("CODEX_COMPLETION_UNKNOWN")
            self.receipts.append(result)
            if not result["ok"]:
                raise CodexError(result.get("code","CODEX_BRIDGE_FAILED"),result.get("attempt_id"))
            data=result["data"]
            if completed.returncode or not isinstance(data,dict) or not isinstance(data.get("text"),str) or not data["text"].strip():
                raise CodexError("CODEX_COMPLETION_UNKNOWN")
            return data["text"]
        except subprocess.TimeoutExpired:
            self.error=CodexError("CODEX_COMPLETION_UNKNOWN")
            raise self.error from None
        except CodexError as exc:
            self.error=exc
            raise
        except (ValueError,KeyError,TypeError):
            self.error=CodexError("CODEX_COMPLETION_UNKNOWN")
            raise self.error from None

def bridge(payload):
    root=Path(payload["resume_root"]).resolve()
    source=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    paths=["v6_nextjs_migration/backend/app/services/codex_cli_client.py",
           "v6_nextjs_migration/backend/app/services/run_records.py",
           "v6_nextjs_migration/backend/app/settings.py"]
    dirty=subprocess.check_output(["git","-C",str(root),"status","--porcelain","--",*paths],text=True)
    if source != payload["source_sha"] or dirty:
        return {"ok":False,"code":"CODEX_SOURCE_MISMATCH"}
    sys.path.insert(0,str(root/"v6_nextjs_migration/backend"))
    from app.services.codex_cli_client import CodexClient, CodexFailure, ExecutionContext, Limits
    schema={"type":"object","properties":{"text":{"type":"string"}},"required":["text"],"additionalProperties":False}
    # One shared invocation budget: each model request uses version/auth/exec.
    client=CodexClient(model=payload["model"],reasoning=payload["reasoning"],
                       limits=Limits(max_launches=36,max_seconds=900,process_timeout=min(300,payload.get("remaining_wall_seconds",300))))
    request={"task":payload["system"],
             "input":payload["user"],
             "output_instruction":"Perform the task using the input. Put the exact requested output in the text field. If the task requests JSON, text must contain that JSON, not commentary.",
             "temperature_note":"Codex uses the pinned model/reasoning configuration; API temperature is not applied."}
    context=ExecutionContext(Path(payload["directory"]),payload["run_id"],"linkedin")
    try:
        if payload.get("operation")=="recover_only":
            from app.services.codex_cli_client import CONTRACT, CONFIG, INSTRUCTION, DISABLED, digest, reconcile_attempt
            from app.services.run_records import json_bytes
            binding={"contract":CONTRACT,"request":request,"schema":schema,"instruction":INSTRUCTION,
                     "model":client.model,"reasoning":client.reasoning,"config":CONFIG,"disabled":DISABLED,
                     "executable_sha256":digest(Path(client.executable).read_bytes())}
            receipt=context.folder()/digest(json_bytes(binding))/"attempt.json"
            if not receipt.is_file():
                return {"ok":False,"code":"CODEX_RECONCILIATION_REQUIRED"}
            result=reconcile_attempt(receipt,by="linkedin-operational-recovery",reason="Reconcile original exact prompt after local interruption; no redispatch")
            return {"ok":True,**result,"source_sha":source,"auth":"chatgpt","execution_kind":"native_cli"}
        result=asyncio.run(client.execute_structured(request,schema,context))
        return {"ok":True,**result,"source_sha":source,"auth":"chatgpt","execution_kind":"native_cli"}
    except CodexFailure as exc:
        return {"ok":False,"code":exc.code,"attempt_id":exc.attempt_id,"error_id":exc.error_id}

if __name__=="__main__":
    try:
        result=bridge(json.load(sys.stdin))
    except Exception as exc:
        result={"ok":False,"code":"CODEX_BRIDGE_SETUP_FAILED","error_class":type(exc).__name__}
    print(json.dumps(result))
    sys.exit(0 if result["ok"] else 2)
