from __future__ import annotations

from typing import Any


def load_yaml(path: str) -> dict[str, Any]:
    try:
        import yaml

        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        out = {}
        with open(path, encoding="utf-8") as f:
            for ln in f:
                if ":" in ln and not ln.startswith(" "):
                    k, v = ln.split(":", 1)
                    out[k.strip()] = v.strip().strip('"')
        return out
