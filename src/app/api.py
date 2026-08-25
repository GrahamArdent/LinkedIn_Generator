from __future__ import annotations

import os
from typing import Any

from .generation import Pipeline
from .utils import load_yaml


LEGACY_TARGETS = ["CFO", "CISO", "Board"]
LEGACY_HASHTAGS = ["#Cybersecurity", "#AdversarialSimulation", "#BoardRisk", "#CISO", "#Identity"]


def _source_for_prompt(item: dict[str, Any]) -> dict[str, str]:
    return {
        "title": str(item.get("title", "")),
        "fact": str(item.get("fact") or item.get("one_liner") or ""),
    }


def run_generation(
    topic: str,
    services: list[str],
    persona_key: str = "ardent_v2",
    *,
    audience: str = "C-suite leaders",
    objective: str = "Educate and convert attention to pipeline",
    targets: list[str] | None = None,
    allowed_sources: list[dict[str, Any]] | None = None,
    hashtags: list[str] | None = None,
    llm_client: Any | None = None,
) -> dict[str, Any]:
    """Run the generation pipeline with explicit caller context.

    Existing positional/default arguments remain for legacy callers. New
    orchestrators should supply audience, objective, targets, evidence and
    hashtags explicitly. `llm_client` exists for deterministic offline
    acceptance testing; live callers normally use the configured provider.
    """

    base = os.path.join(os.path.dirname(__file__), "../../")
    prompt_kit = load_yaml(os.path.join(base, "config/prompt_kit.config.yaml"))
    prompts = load_yaml(os.path.join(base, "config/prompts_packs.yaml"))
    personas = load_yaml(os.path.join(base, "config/personas.yaml"))
    cta_policies = load_yaml(os.path.join(base, "config/cta_policies.yaml"))

    cfg = {
        "prompt_kit": {
            "emoji_max": int(prompt_kit.get("emoji_max", 3)),
            "bullet_char": prompt_kit.get("bullet_char", "🔹"),
            "hashtag_min": int(prompt_kit.get("hashtag_min", 3)),
            "hashtag_max": int(prompt_kit.get("hashtag_max", 5)),
            "strip_links_in_body": prompt_kit.get("strip_links_in_body", "true")
            in ("true", "True", "1"),
            "append_sources_block": prompt_kit.get("append_sources_block", "false")
            in ("true", "True", "1"),
            "allow_em_dash": prompt_kit.get("allow_em_dash", "false") in ("true", "True", "1"),
            "forbidden_phrases": list(cta_policies.get("forbidden_phrases", []) or []),
        }
    }
    pipe = Pipeline(cfg, client=llm_client)
    persona_profile = personas.get("personas", {}).get(persona_key, {})

    plan_ctx = {
        "topic": topic,
        "services": services,
        "targets": list(targets) if targets is not None else list(LEGACY_TARGETS),
    }
    plan = pipe.plan(prompts.get("plan_prompt", {}), plan_ctx)

    source_items = list(allowed_sources) if allowed_sources is not None else list(plan.get("citations", []))
    draft_ctx = {
        "persona_key": persona_key,
        "audience": audience,
        "objective": objective,
        "topic": topic,
        "services": services,
        "angle_options": [plan["angle"]],
        "persona_profile": persona_profile,
        "allowed_sources": [_source_for_prompt(item) for item in source_items],
    }
    drafts = pipe.draft_variants(prompts.get("draft_prompt", {}), draft_ctx)
    best = pipe.judge_select(prompts.get("judge_prompt", {}), persona_profile, drafts)
    crit = pipe.critic(prompts.get("critic_prompt", {}), best, persona_profile)
    hum = pipe.humanize(prompts.get("humanize_prompt", {}), crit, persona_profile)

    citations = [
        str(item.get("url", ""))
        for item in source_items
        if str(item.get("url", "")).startswith("http")
    ]
    final_hashtags = list(hashtags) if hashtags is not None else list(LEGACY_HASHTAGS)
    return pipe.finalize(persona_key, hum, citations, final_hashtags)
