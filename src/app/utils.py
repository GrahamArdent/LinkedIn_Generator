from __future__ import annotations
from typing import Dict, Any

def load_yaml(path:str)->Dict[str,Any]:
    try:
        import yaml
        with open(path,"r",encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        out = {}
        with open(path,"r",encoding="utf-8") as f:
            for ln in f:
                if ":" in ln and not ln.startswith(" "):
                    k,v = ln.split(":",1)
                    out[k.strip()] = v.strip().strip('"')
        return out
