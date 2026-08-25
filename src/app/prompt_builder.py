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


def _persona_family(persona_key: str) -> str:
    if persona_key.startswith("ardent"):
        return "ardent"
    if persona_key.startswith("graham"):
        return "graham"
    return persona_key


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


def _default_hashtags(policy: dict[str, Any], family: str) -> list[str]:
    core = list(policy.get("core") or [])
    brand = list(policy.get("brand") or []) if family == "ardent" else []
    trending = list(policy.get("trending_priority") or [])
    banlist = set(policy.get("banlist") or [])
    max_per_post = int(policy.get("max_per_post", 5))
    tags = [tag for tag in _unique(core + brand + trending) if tag not in banlist]
    return tags[:max_per_post]


def build_prompt_blocks(config_dir: Path) -> dict[str, Any]:
    """Load the native LinkedIn content-policy assets into one runtime shape.

    `personas.yaml` owns persona/style traits, `cta_policies.yaml` owns CTA
    policy, and `hashtag_policy.yaml` owns hashtag policy. Older runtime code
    expects each persona to expose `cta_patterns` and `hashtag_set`; those
    compatibility fields are derived here rather than duplicated across YAML
    files.
    """

    raw_personas = _load_yaml(config_dir / "personas.yaml").get("personas", {})
    cta_policy = _load_yaml(config_dir / "cta_policies.yaml")
    hashtag_policy = _load_yaml(config_dir / "hashtag_policy.yaml")

    if not raw_personas:
        raise KeyError(
            "No personas found. Expected config/personas.yaml with keys under 'personas'."
        )

    safe_ctas = cta_policy.get("safe_ctas", {})
    if not isinstance(safe_ctas, dict):
        raise ValueError("cta_policies.yaml safe_ctas must be a mapping/object.")

    personas: dict[str, dict[str, Any]] = {}
    hashtag_sets: dict[str, list[str]] = {}

    for persona_key, raw_profile in raw_personas.items():
        if not isinstance(raw_profile, dict):
            raise ValueError(f"Persona '{persona_key}' must be a mapping/object.")

        family = _persona_family(persona_key)
        profile = dict(raw_profile)

        ctas = list(profile.get("cta_patterns") or safe_ctas.get(family) or [])
        if not ctas:
            raise KeyError(
                f"Persona '{persona_key}' has no CTA policy. Add a persona-specific "
                "cta_patterns list or a matching safe_ctas entry in cta_policies.yaml."
            )

        hashtag_set = str(profile.get("hashtag_set") or f"{family}_default")
        tags = _default_hashtags(hashtag_policy, family)

        profile["cta_patterns"] = ctas
        profile["hashtag_set"] = hashtag_set
        personas[persona_key] = profile
        hashtag_sets[hashtag_set] = tags

    skeleton_cfg = _load_yaml(config_dir / "skeleton.yaml")
    sections = skeleton_cfg.get("sections") if skeleton_cfg else None
    if not sections:
        sections = list(DEFAULT_SECTIONS)

    return {
        "personas": personas,
        "hashtags": hashtag_sets,
        "prompts": {
            "skeleton": {"sections": sections},
            "section_templates": {},
        },
    }
