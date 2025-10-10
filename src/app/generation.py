from __future__ import annotations
from typing import Dict, Any, List
import os, json
from .llm import LLMClient
from .models import PostJSON, Telemetry
from .validators import remove_links, append_sources_block, apply_house_rules, clamp_hashtags, extract_hashtags
from .rag import retrieve
from .judge import judge_score
from .adapters import pick_quote, pick_stat

def build_prompt(template:str, **kwargs)->str:
    out = template
    for k,v in kwargs.items():
        token = "{" + k + "}"
        out = out.replace(token, json.dumps(v) if isinstance(v,(dict,list)) else str(v))
    return out

class Pipeline:
    def __init__(self, config:Dict[str,Any]):
        self.cfg = config
        self.client = LLMClient(
            temperature=float(os.getenv("TEMPERATURE", "0.5")),
            seed=int(os.getenv("SEED", "42"))
        )
        self.n_variants = int(os.getenv("N_VARIANTS","4"))

    def plan(self, plan_prompt:Dict[str,str], ctx:Dict[str,Any]) -> Dict[str,Any]:
        angle = "CFO cost and risk lens"
        return {
            "angle": angle,
            "sections": ["hook","exec_pov","proof_point","micro_plays","quote","cta","hashtags"],
            "micro_plays": ["Run a tabletop", "Pilot an adversarial sim", "Board-level metrics refresh"],
            "citations": retrieve(ctx["topic"], angle, k=3)
        }

    def draft_variants(self, draft_prompt:Dict[str,str], ctx:Dict[str,Any]) -> List[str]:
        user = build_prompt(draft_prompt["user_template"], **ctx)
        variants = []
        for _ in range(self.n_variants):
            out = self.client.call(draft_prompt["system"], user, response_json=True)
            variants.append(out.get("text","(placeholder draft)"))
        return variants

    def judge_select(self, judge_prompt:Dict[str,str], persona_profile:Dict[str,Any], drafts:List[str]) -> str:
        rules = self.cfg["prompt_kit"]
        best, best_s = None, -1
        for d in drafts:
            s = judge_score(d, persona_profile, rules)
            if s > best_s:
                best, best_s = d, s
        return best

    def critic(self, critic_prompt:Dict[str,str], text:str)->str:
        return text

    def humanize(self, humanize_prompt:Dict[str,str], text:str)->str:
        return text

    def finalize(self, persona_key:str, text:str, citations:List[str], hashtags:List[str]) -> Dict[str,Any]:
        body_no_links, urls = remove_links(text)
        urls.extend([c for c in citations if c.startswith("http")])
        bullet = self.cfg["prompt_kit"]["bullet_char"]
        emoji_max = self.cfg["prompt_kit"]["emoji_max"]
        allow_em_dash = self.cfg["prompt_kit"]["allow_em_dash"]
        clean_body, _issues = apply_house_rules(body_no_links, bullet=bullet, emoji_max=emoji_max, allow_em_dash=allow_em_dash)
        if self.cfg["prompt_kit"]["append_sources_block"]:
            clean_body = append_sources_block(clean_body, urls)
        if not hashtags:
            hashtags = extract_hashtags(text)
        hashtags = clamp_hashtags(hashtags, self.cfg["prompt_kit"]["hashtag_min"], self.cfg["prompt_kit"]["hashtag_max"])
        telemetry = Telemetry(emoji_count=0, bullet_char=bullet, persona=persona_key)
        payload = PostJSON(hashtags=hashtags, body=clean_body, sources=urls, telemetry=telemetry)
        return payload.model_dump()
