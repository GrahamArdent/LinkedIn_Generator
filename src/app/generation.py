from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from config.hashtags import ensure_hashtags_in_body, generate_hashtags

from .judge import judge_score
from .llm import LLMClient
from .models import PostJSON, Telemetry
from .rag import retrieve
from .validators import (
    append_sources_block,
    apply_house_rules,
    clamp_hashtags,
    extract_hashtags,
    remove_links,
)

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def sanitize_and_validate(text: str, *, persona: str = "ardent", topic: str | None = None) -> str:
    clean_text, _issues = apply_house_rules(text)
    hashtags = generate_hashtags(clean_text, persona=persona, topic=topic, config_dir=CONFIG_DIR)
    return ensure_hashtags_in_body(clean_text, hashtags)


def build_prompt(template: str, **kwargs) -> str:
    out = template
    for k, v in kwargs.items():
        token = "{" + k + "}"
        out = out.replace(token, json.dumps(v) if isinstance(v, (dict, list)) else str(v))
    return out


class Pipeline:
    def __init__(self, config: dict[str, Any]):
        self.cfg = config
        self.client = LLMClient(
            temperature=float(os.getenv("TEMPERATURE", "0.5")), seed=int(os.getenv("SEED", "42"))
        )
        self.n_variants = int(os.getenv("N_VARIANTS", "4"))

    def plan(self, plan_prompt: dict[str, str], ctx: dict[str, Any]) -> dict[str, Any]:
        targets = [str(target) for target in (ctx.get("targets") or []) if str(target).strip()]
        audience_lens = ", ".join(targets) if targets else "the intended professional audience"
        topic = str(ctx.get("topic", "")).strip()
        angle = f"{topic} — practical relevance for {audience_lens}" if topic else audience_lens
        return {
            "angle": angle,
            "sections": ["hook", "context", "evidence_or_experience", "takeaway", "cta"],
            "micro_plays": [],
            "citations": retrieve(topic, angle, k=3),
        }

    def draft_variants(self, draft_prompt: dict[str, str], ctx: dict[str, Any]) -> list[str]:
        system = build_prompt(draft_prompt["system"], **ctx)
        user = build_prompt(draft_prompt["user_template"], **ctx)
        variants = []
        for _ in range(self.n_variants):
            out = self.client.call(system, user, response_json=True)
            variants.append(out.get("text", "(placeholder draft)"))
        return variants

    def judge_select(
        self, judge_prompt: dict[str, str], persona_profile: dict[str, Any], drafts: list[str]
    ) -> str:
        rules = self.cfg["prompt_kit"]
        best, best_s = None, -1
        for d in drafts:
            s = judge_score(d, persona_profile, rules)
            if s > best_s:
                best, best_s = d, s
        return best

    def critic(self, critic_prompt: dict[str, str], text: str) -> str:
        return text

    def humanize(self, humanize_prompt: dict[str, str], text: str) -> str:
        return text

    def finalize(
        self, persona_key: str, text: str, citations: list[str], hashtags: list[str]
    ) -> dict[str, Any]:
        body_no_links, urls = remove_links(text)
        urls.extend([c for c in citations if c.startswith("http")])
        bullet = self.cfg["prompt_kit"]["bullet_char"]
        emoji_max = self.cfg["prompt_kit"]["emoji_max"]
        allow_em_dash = self.cfg["prompt_kit"]["allow_em_dash"]
        clean_body, _issues = apply_house_rules(
            body_no_links, bullet=bullet, emoji_max=emoji_max, allow_em_dash=allow_em_dash
        )
        if self.cfg["prompt_kit"]["append_sources_block"]:
            clean_body = append_sources_block(clean_body, urls)
        if not hashtags:
            hashtags = extract_hashtags(text)
        hashtags = clamp_hashtags(
            hashtags, self.cfg["prompt_kit"]["hashtag_min"], self.cfg["prompt_kit"]["hashtag_max"]
        )
        telemetry = Telemetry(emoji_count=0, bullet_char=bullet, persona=persona_key)
        payload = PostJSON(hashtags=hashtags, body=clean_body, sources=urls, telemetry=telemetry)
        return payload.model_dump()
