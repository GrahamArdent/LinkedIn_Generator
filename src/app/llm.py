from __future__ import annotations
from typing import Any, Dict, Optional
import json, os

class LLMClient:
    def __init__(self, model:str|None=None, temperature:float=0.5, seed:int|None=None):
        self.model = model or os.getenv("MODEL_NAME", "gpt-4.1-mini")
        self.temperature = temperature
        self.seed = seed

    def call(self, system:str, user:str, response_json:bool=True) -> Dict[str, Any] | str:
        # Wire your provider here; stub JSON for offline tests.
        content = json.dumps({"text": "LLM output would go here."})
        if response_json:
            try:
                return json.loads(content)
            except Exception:
                return {"text": content}
        return content
