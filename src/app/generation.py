from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from config.hashtags import ensure_hashtags_in_body, generate_hashtags

from .judge import judge_report
from .llm import LLMClient
from .models import PostJSON, Telemetry
from .rag import retrieve
from .rewrite_guard import evaluate_rewrite
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
    def __init__(self, config: dict[str, Any], *, client: Any | None = None):
        self.cfg = config
        self.client = client or LLMClient(
            temperature=float(os.getenv("TEMPERATURE", "0.5")), seed=int(os.getenv("SEED", "42"))
        )
        # One full draft is the efficient default. The zero-cost planner supplies
        # several angle options inside that one generation call. N_VARIANTS
        # remains an explicit escape hatch for experiments.
        self.n_variants = max(1, int(os.getenv("N_VARIANTS", "1")))
        self.last_judge_report: dict[str, Any] | None = None
        self.rewrite_reports: list[dict[str, Any]] = []

    def plan(self, plan_prompt: dict[str, str], ctx: dict[str, Any]) -> dict[str, Any]:
        targets = [str(target) for target in (ctx.get("targets") or []) if str(target).strip()]
        audience_lens = ", ".join(targets) if targets else "the intended professional audience"
        topic = str(ctx.get("topic", "")).strip()
        subject = topic or "the topic"
        angle_options = [
            f"Plain-language lesson: explain why {subject} matters to {audience_lens}.",
            (
                "Second-order consequence: show what gets harder, slower, more expensive, "
                f"or less trustworthy when the underlying problem in {subject} is ignored."
            ),
            (
                "Contrarian angle: identify the reasonable-sounding assumption around "
                f"{subject} that the supplied evidence complicates."
            ),
        ]
        return {
            "angle": angle_options[0],
            "angle_options": angle_options,
            "sections": ["hook", "context", "insight", "takeaway", "closer"],
            "micro_plays": [],
            "citations": retrieve(topic, angle_options[0], k=3),
        }

    def draft_variants(self, draft_prompt: dict[str, str], ctx: dict[str, Any]) -> list[str]:
        system = build_prompt(draft_prompt["system"], **ctx)
        user = build_prompt(draft_prompt["user_template"], **ctx)
        variants = []
        for _ in range(self.n_variants):
            out = self.client.call(system, user, response_json=True)
            variants.append(out.get("text", ""))
        return variants

    def judge_select(
        self, judge_prompt: dict[str, str], persona_profile: dict[str, Any], drafts: list[str]
    ) -> str:
        rules = self.cfg["prompt_kit"]
        best, best_s, best_report = None, -1, None
        for draft in drafts:
            report = judge_report(draft, persona_profile, rules)
            score = int(report["score"])
            if score > best_s:
                best, best_s, best_report = draft, score, report
        self.last_judge_report = best_report
        return best or ""

    def _rewrite(
        self,
        prompt: dict[str, str],
        text: str,
        persona_profile: dict[str, Any],
        *,
        stage: str,
        voice_examples: list[dict[str, str]] | None = None,
    ) -> str:
        # Do not spend an additional model call when the deterministic gate has
        # no concrete issue to repair. Approved voice examples already guide the
        # draft pass; rewrite passes use them only when a repair is warranted.
        if self.last_judge_report is not None and not self.last_judge_report.get("issues"):
            self.rewrite_reports.append(
                {
                    "stage": stage,
                    "skipped": True,
                    "accepted": False,
                    "reasons": ["deterministic quality gate has no repairable issue"],
                    "original_report": self.last_judge_report,
                    "candidate_report": self.last_judge_report,
                }
            )
            return text

        prompt_voice_examples = list(voice_examples or [])
        system = build_prompt(
            prompt.get("system", ""),
            post=text,
            persona_profile=persona_profile,
            approved_voice_examples=prompt_voice_examples,
        )
        user = build_prompt(
            prompt.get("user_template", "{post}"),
            post=text,
            persona_profile=persona_profile,
            approved_voice_examples=prompt_voice_examples,
        )
        out = self.client.call(system, user, response_json=True)
        candidate = str(out.get("text", "") if isinstance(out, dict) else out).strip()
        report = evaluate_rewrite(
            text,
            candidate,
            persona_profile,
            self.cfg["prompt_kit"],
        )
        self.rewrite_reports.append({"stage": stage, "skipped": False, **report})
        if report["accepted"]:
            self.last_judge_report = report["candidate_report"]
            return candidate
        return text

    def critic(
        self,
        critic_prompt: dict[str, str],
        text: str,
        persona_profile: dict[str, Any],
        *,
        voice_examples: list[dict[str, str]] | None = None,
    ) -> str:
        return self._rewrite(
            critic_prompt,
            text,
            persona_profile,
            stage="critic",
            voice_examples=voice_examples,
        )

    def humanize(
        self,
        humanize_prompt: dict[str, str],
        text: str,
        persona_profile: dict[str, Any],
        *,
        voice_examples: list[dict[str, str]] | None = None,
    ) -> str:
        return self._rewrite(
            humanize_prompt,
            text,
            persona_profile,
            stage="humanize",
            voice_examples=voice_examples,
        )

    def finalize(
        self,
        persona_key: str,
        text: str,
        citations: list[str],
        hashtags: list[str],
        *,
        voice_reference_count: int = 0,
        voice_reference_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        body_no_links, urls = remove_links(text)
        urls.extend([c for c in citations if c.startswith("http")])
        urls = list(dict.fromkeys(urls))
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
        selected_score = None
        if self.last_judge_report is not None:
            selected_score = int(self.last_judge_report["score"])
        telemetry = Telemetry(
            emoji_count=0,
            bullet_char=bullet,
            persona=persona_key,
            score=selected_score,
            voice_reference_count=voice_reference_count,
            voice_reference_ids=list(voice_reference_ids or []),
        )
        payload = PostJSON(hashtags=hashtags, body=clean_body, sources=urls, telemetry=telemetry)
        return payload.model_dump()
