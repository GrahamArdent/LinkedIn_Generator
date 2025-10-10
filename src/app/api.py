from __future__ import annotations
from typing import Any, Dict, List
import os, json
from .generation import Pipeline
from .utils import load_yaml

def run_generation(topic:str, services:List[str], persona_key:str="ardent_v2")->Dict[str,Any]:
    base = os.path.join(os.path.dirname(__file__), "../../")
    prompt_kit = load_yaml(os.path.join(base, "config/prompt_kit.config.yaml"))
    prompts = load_yaml(os.path.join(base, "config/prompts_packs.yaml"))
    personas = load_yaml(os.path.join(base, "config/personas.yaml"))

    cfg = {"prompt_kit": {
        "emoji_max": int(prompt_kit.get("emoji_max",3)),
        "bullet_char": prompt_kit.get("bullet_char","🔹"),
        "hashtag_min": int(prompt_kit.get("hashtag_min",3)),
        "hashtag_max": int(prompt_kit.get("hashtag_max",5)),
        "strip_links_in_body": prompt_kit.get("strip_links_in_body","true") in ("true","True","1"),
        "append_sources_block": prompt_kit.get("append_sources_block","true") in ("true","True","1"),
        "allow_em_dash": prompt_kit.get("allow_em_dash","false") in ("true","True","1"),
    }}
    pipe = Pipeline(cfg)
    persona_profile = personas.get("personas",{}).get(persona_key, {})

    plan_ctx = {"topic": topic, "services": services, "targets": ["CFO","CISO","Board"]}
    plan = pipe.plan(prompts.get("plan_prompt", {}), plan_ctx)

    draft_ctx = {
        "audience": "C-suite leaders",
        "objective": "Educate and convert attention to pipeline",
        "topic": topic,
        "services": services,
        "angle_options": [plan["angle"]],
        "persona_profile": persona_profile,
        "allowed_sources": [{"title": it.get("title",""), "fact": it.get("one_liner","")} for it in plan.get("citations",[])]
    }
    drafts = pipe.draft_variants(prompts.get("draft_prompt", {}), draft_ctx)
    best = pipe.judge_select(prompts.get("judge_prompt", {}), persona_profile, drafts)
    crit = pipe.critic(prompts.get("critic_prompt", {}), best)
    hum = pipe.humanize(prompts.get("humanize_prompt", {}), crit)

    citations = [it.get("url","") for it in plan.get("citations",[]) if it.get("url")]
    hashtags = ["#Cybersecurity","#AdversarialSimulation","#BoardRisk","#CISO","#Identity"]
    payload = pipe.finalize(persona_key, hum, citations, hashtags)
    return payload
