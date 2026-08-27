from __future__ import annotations

import os
from typing import Any

from .generation import Pipeline
from .llm import LLMClient
from .opportunity import assess_opportunity, ending_guidance
from .utils import load_yaml


LEGACY_TARGETS = ["CFO", "CISO", "Board"]
LEGACY_HASHTAGS = ["#Cybersecurity", "#AdversarialSimulation", "#BoardRisk", "#CISO", "#Identity"]


def _source_for_prompt(item: dict[str, Any]) -> dict[str, str]:
    return {
        "title": str(item.get("title", "")),
        "fact": str(item.get("fact") or item.get("one_liner") or ""),
    }


def _voice_for_prompt(item: dict[str, Any]) -> dict[str, str]:
    return {
        "example_id": str(item.get("example_id") or ""),
        "provenance": str(item.get("provenance") or ""),
        "text": str(item.get("text") or ""),
    }


def _persona_profile(
    base: str,
    personas: dict[str, Any],
    persona_key: str,
    *,
    author_pov: str,
) -> dict[str, Any]:
    """Return persona configuration plus authorized voice and active POV context."""

    profile = dict(personas.get("personas", {}).get(persona_key, {}) or {})
    profile["active_author_pov"] = author_pov
    if persona_key != "graham":
        return profile

    voice_authority = load_yaml(os.path.join(base, "config/graham_voice_profile.yaml"))
    if voice_authority:
        # Voice Bible governs public rhetorical shape. It is style/reasoning
        # authority only and never factual evidence.
        profile["voice_authority"] = voice_authority

    spoken_voice = load_yaml(os.path.join(base, "config/graham_spoken_voice.yaml"))
    if spoken_voice:
        # Spoken Voice governs conversational wording, skepticism, reasoning
        # cadence and first-person authenticity. It is also style/reasoning
        # authority only and must never leak private-source biography.
        profile["spoken_voice"] = spoken_voice
    return profile


def _goal_without_gate(content_goal: str) -> tuple[str, str]:
    goal = content_goal if content_goal in {"reach", "conversation", "authority"} else "authority"
    if goal == "conversation":
        guidance = (
            "A question may be used only if the supplied context contains a genuine tradeoff or experience "
            "worth discussing. Never ask for generic thoughts, agreement, likes, or comments."
        )
    elif goal == "reach":
        guidance = "End with a memorable stand-alone insight; do not force a question."
    else:
        guidance = "End with the strongest useful insight or earned provocation; a question is optional."
    return goal, guidance


def run_generation(
    topic: str,
    services: list[str],
    persona_key: str = "ardent_v2",
    *,
    audience: str = "C-suite leaders",
    objective: str = "Educate and convert attention to pipeline",
    author_pov: str = "individual",
    content_goal: str = "auto",
    opportunity_gate: bool = False,
    targets: list[str] | None = None,
    allowed_sources: list[dict[str, Any]] | None = None,
    voice_examples: list[dict[str, Any]] | None = None,
    hashtags: list[str] | None = None,
    llm_client: Any | None = None,
    opportunity_client: Any | None = None,
) -> dict[str, Any]:
    """Run the generation pipeline with explicit caller context.

    Existing positional/default arguments remain for legacy callers. New
    orchestrators should supply audience, objective, author POV, content goal,
    evidence and hashtags explicitly. Voice authority and approved examples are
    style and reasoning evidence, never factual evidence. Dedication-style
    requests may enable the opportunity preflight so weak subjects are skipped
    before a full draft is generated.
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
    persona_profile = _persona_profile(base, personas, persona_key, author_pov=author_pov)

    plan_ctx = {
        "topic": topic,
        "services": services,
        "targets": list(targets) if targets is not None else list(LEGACY_TARGETS),
    }
    plan = pipe.plan(prompts.get("plan_prompt", {}), plan_ctx)

    source_items = list(allowed_sources) if allowed_sources is not None else list(plan.get("citations", []))
    citations = [
        str(item.get("url", ""))
        for item in source_items
        if str(item.get("url", "")).startswith("http")
    ]

    if opportunity_gate:
        gate_client = opportunity_client or llm_client
        if gate_client is None:
            gate_model = os.getenv("OPPORTUNITY_MODEL", "").strip() or None
            gate_client = LLMClient(model=gate_model, temperature=0.1, seed=42)
        minimum_score = max(0, min(100, int(os.getenv("OPPORTUNITY_MIN_SCORE", "60"))))
        assessment = assess_opportunity(
            topic=topic,
            audience=audience,
            objective=objective,
            evidence=source_items,
            client=gate_client,
            requested_goal=content_goal,
            minimum_score=minimum_score,
        )
        opportunity = assessment.as_dict()
        resolved_goal = assessment.goal
        ending = ending_guidance(assessment)
        if assessment.decision == "skip":
            return {
                "status": "skipped",
                "body": "",
                "hashtags": [],
                "sources": list(dict.fromkeys(citations)),
                "telemetry": {
                    "persona": persona_key,
                    "opportunity_score": assessment.score,
                    "opportunity_decision": assessment.decision,
                    "opportunity_reason": assessment.reason,
                    "opportunity_dimensions": assessment.dimensions,
                    "opportunity_warnings": list(assessment.warnings),
                    "content_goal": assessment.goal,
                    "earned_question": assessment.earned_question,
                },
            }
    else:
        resolved_goal, ending = _goal_without_gate(content_goal)
        opportunity = {
            "score": None,
            "decision": "draft",
            "goal": resolved_goal,
            "earned_question": False,
            "reason": "Opportunity preflight disabled for this caller.",
            "dimensions": {},
            "warnings": ["opportunity_gate_disabled"],
        }

    # Keep the deterministic quality gate aligned with the chosen strategy.
    # Questions are optional unless a conversation-goal opportunity explicitly earned one.
    persona_profile["active_content_goal"] = resolved_goal
    persona_profile["earned_question"] = bool(opportunity.get("earned_question", False))

    voice_items = list(voice_examples or [])[:3]
    prompt_voice_examples = [_voice_for_prompt(item) for item in voice_items]
    angle_options = list(plan.get("angle_options") or [plan["angle"]])
    draft_ctx = {
        "persona_key": persona_key,
        "audience": audience,
        "objective": objective,
        "author_pov": author_pov,
        "content_goal": resolved_goal,
        "opportunity_assessment": opportunity,
        "ending_guidance": ending,
        "topic": topic,
        "services": services,
        "angle_options": angle_options,
        "persona_profile": persona_profile,
        "allowed_sources": [_source_for_prompt(item) for item in source_items],
        "approved_voice_examples": prompt_voice_examples,
    }
    drafts = pipe.draft_variants(prompts.get("draft_prompt", {}), draft_ctx)
    best = pipe.judge_select(prompts.get("judge_prompt", {}), persona_profile, drafts)
    crit = pipe.critic(
        prompts.get("critic_prompt", {}),
        best,
        persona_profile,
        voice_examples=prompt_voice_examples,
    )
    hum = pipe.humanize(
        prompts.get("humanize_prompt", {}),
        crit,
        persona_profile,
        voice_examples=prompt_voice_examples,
    )

    voice_reference_ids = [
        str(item.get("example_id"))
        for item in voice_items
        if item.get("example_id")
    ]
    final_hashtags = list(hashtags) if hashtags is not None else list(LEGACY_HASHTAGS)
    payload = pipe.finalize(
        persona_key,
        hum,
        citations,
        final_hashtags,
        voice_reference_count=len(voice_items),
        voice_reference_ids=voice_reference_ids,
        opportunity=opportunity,
    )
    payload["status"] = "drafted"
    return payload
