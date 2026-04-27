from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_SECTIONS = [
    "hook",
    "exec_pov",
    "proof_point",
    "micro_plays",
    "quote",
    "cta",
    "hashtags",
]


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    txt = path.read_text(encoding="utf-8")
    data = yaml.safe_load(txt) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a YAML mapping/object.")
    return data


def build_prompt_blocks(config_dir: Path) -> dict[str, Any]:
    """
    Returns a dict shaped like:
    {
      "personas": { "graham": {...}, "ardent": {...} },
      "hashtags": { "security_core": ["#..."] },
      "prompts": {
          "skeleton": {"sections": [...]},
          "section_templates": {}
      }
    }
    """
    personas = _load_yaml(config_dir / "personas.yaml").get("personas", {})
    hashtags = _load_yaml(config_dir / "hashtags.yaml").get("hashtags", {})

    # Optional override file: skeleton.yaml -> sections: [...]
    skeleton_cfg = _load_yaml(config_dir / "skeleton.yaml")
    sections = skeleton_cfg.get("sections") if skeleton_cfg else None
    if not sections:
        sections = list(DEFAULT_SECTIONS)

    # Basic validation
    if not personas:
        raise KeyError(
            "No personas found. Expected config/personas.yaml with keys under 'personas'."
        )
    for key, p in personas.items():
        if "hashtag_set" not in p:
            raise KeyError(f"Persona '{key}' missing 'hashtag_set'.")
        if p["hashtag_set"] not in hashtags:
            raise KeyError(
                f"Persona '{key}' references unknown hashtag_set '{p['hashtag_set']}'. Add it to config/hashtags.yaml."
            )

    blocks: dict[str, Any] = {
        "personas": personas,
        "hashtags": hashtags,
        "prompts": {
            "skeleton": {"sections": sections},
            "section_templates": {},  # not used yet, kept for compatibility
        },
    }
    return blocks
