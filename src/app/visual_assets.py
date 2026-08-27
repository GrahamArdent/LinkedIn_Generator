from __future__ import annotations

import json
import os
import re
from typing import Any

from pydantic import ValidationError

from .contracts import CarouselBrief, CarouselSlide, SingleImageBrief, VisualAssetPlan
from .llm import LLMClient


_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)
_URL_RE = re.compile(r"https?://\S+")
_NUMBER_RE = re.compile(r"(?<!\w)\d[\d,.]*%?(?!\w)")
_QUOTE_RE = re.compile(r"[\"“]([^\"”]{2,})[\"”]")
_NO_TEXT_SUFFIX = (
    " No embedded text, lettering, logos, watermarks, fake interface labels, or pseudo-typography."
)


def _parse_payload(text: str) -> dict[str, Any]:
    match = _JSON_RE.search(text.strip())
    if not match:
        raise ValueError("visual planner returned no JSON object")
    payload = json.loads(match.group(0))
    if not isinstance(payload, dict):
        raise ValueError("visual planner JSON must be an object")
    return payload


def _normalized_matches(pattern: re.Pattern[str], text: str) -> set[str]:
    return {match.strip().lower() for match in pattern.findall(text)}


def _copy_guard(post_text: str, visual_copy: str) -> list[str]:
    """Block obvious new factual tokens from visual copy.

    Visuals may simplify or paraphrase the approved post, but they should not
    introduce new URLs, numbers, or quoted claims. The image-generation prompt
    is intentionally excluded from this check because it describes composition,
    not publishable factual copy.
    """

    reasons: list[str] = []
    new_urls = _normalized_matches(_URL_RE, visual_copy) - _normalized_matches(_URL_RE, post_text)
    new_numbers = _normalized_matches(_NUMBER_RE, visual_copy) - _normalized_matches(_NUMBER_RE, post_text)
    new_quotes = _normalized_matches(_QUOTE_RE, visual_copy) - _normalized_matches(_QUOTE_RE, post_text)
    if new_urls:
        reasons.append("visual copy introduces a new URL")
    if new_numbers:
        reasons.append("visual copy introduces a new number")
    if new_quotes:
        reasons.append("visual copy introduces a new quoted claim")
    return reasons


def _visual_copy(plan: VisualAssetPlan) -> str:
    if plan.asset_type == "single_image" and plan.single_image is not None:
        return plan.single_image.overlay_text
    if plan.asset_type == "carousel" and plan.carousel is not None:
        parts = [plan.carousel.cover_headline]
        for slide in plan.carousel.slides:
            parts.extend([slide.headline, slide.body])
        return "\n".join(parts)
    return ""


def _single_image(payload: dict[str, Any]) -> SingleImageBrief:
    raw = payload.get("single_image") if isinstance(payload.get("single_image"), dict) else {}
    generation_prompt = str(raw.get("generation_prompt") or "").strip()
    if _NO_TEXT_SUFFIX.strip().lower() not in generation_prompt.lower():
        generation_prompt = generation_prompt.rstrip(". ") + "." + _NO_TEXT_SUFFIX
    return SingleImageBrief(
        concept=str(raw.get("concept") or "").strip(),
        overlay_text=str(raw.get("overlay_text") or "").strip(),
        composition=str(raw.get("composition") or "").strip(),
        style=str(raw.get("style") or "").strip(),
        generation_prompt=generation_prompt,
        negative_guidance=[str(item).strip() for item in raw.get("negative_guidance", []) if str(item).strip()][
            :12
        ],
        alt_text=str(raw.get("alt_text") or "").strip(),
    )


def _carousel(payload: dict[str, Any]) -> CarouselBrief:
    raw = payload.get("carousel") if isinstance(payload.get("carousel"), dict) else {}
    slides_raw = raw.get("slides") if isinstance(raw.get("slides"), list) else []
    slides = [
        CarouselSlide(
            slide_number=index,
            role=str(item.get("role") or ("cover" if index == 1 else "insight")),
            headline=str(item.get("headline") or "").strip(),
            body=str(item.get("body") or "").strip(),
            visual_direction=str(item.get("visual_direction") or "").strip(),
        )
        for index, item in enumerate(slides_raw[:8], start=1)
        if isinstance(item, dict)
    ]
    return CarouselBrief(
        cover_headline=str(raw.get("cover_headline") or "").strip(),
        design_system=str(raw.get("design_system") or "").strip(),
        slides=slides,
        alt_text=str(raw.get("alt_text") or "").strip(),
    )


def _deferred(reason: str, *, warning: str | None = None) -> VisualAssetPlan:
    return VisualAssetPlan(
        status="deferred",
        rationale=reason,
        warnings=[warning] if warning else [],
    )


def plan_visual_asset(
    *,
    post_text: str,
    source_candidate: str,
    audience: str,
    content_goal: str,
    evidence: list[dict[str, Any]],
    preference: str = "auto",
    style_profile: dict[str, Any] | None = None,
    client: Any | None = None,
) -> VisualAssetPlan:
    """Create one provider-neutral visual companion for a publish-ready post.

    The planner chooses single image versus carousel unless the caller overrides
    the format. It never renders an asset, schedules a post, or publishes. The
    returned brief is explicitly review-required and is designed to feed a later
    renderer such as a Replicate adapter plus a deterministic typography layer.
    """

    if source_candidate not in {"original", "rewrite"}:
        return _deferred("Visual planning requires a known publish candidate.")
    if preference not in {"auto", "single_image", "carousel"}:
        return _deferred("Visual asset preference is unsupported.")

    source_facts = [
        {
            "title": str(item.get("title") or "").strip(),
            "fact": str(item.get("fact") or item.get("one_liner") or "").strip(),
        }
        for item in evidence
        if str(item.get("fact") or item.get("one_liner") or "").strip()
    ]
    style_profile = dict(style_profile or {})
    planner_client = client
    if planner_client is None:
        model = os.getenv("VISUAL_PLANNER_MODEL", "").strip() or None
        planner_client = LLMClient(model=model, temperature=0.2, seed=42)

    system = (
        "You are a strict LinkedIn visual editor. Create one visual companion plan for a finished, publish-ready "
        "post. Do not render an image. Choose single_image or carousel based on whether the idea is best understood "
        "as one strong visual or a short sequence. Follow the supplied visual style policy. The visual should add "
        "meaning, not merely restate the post. Do not invent facts, metrics, quotations, screenshots, UI, logos, or "
        "claims. Keep typography separate from AI image generation: overlay text and carousel copy are structured "
        "fields, while image-generation prompts must request imagery without embedded text. Avoid generic robot, "
        "glowing-brain, neon-dashboard, and stock-corporate AI clichés. Return JSON only."
    )
    user = json.dumps(
        {
            "post": post_text,
            "audience": audience,
            "content_goal": content_goal,
            "format_preference": preference,
            "grounded_evidence": source_facts,
            "visual_style_policy": style_profile,
            "required_output": {
                "asset_type": "single_image or carousel; obey a non-auto preference",
                "rationale": "why this format helps this specific post",
                "creative_goal": "what the visual should make the reader notice or understand",
                "aspect_ratio": "4:5",
                "single_image": {
                    "concept": "one visual concept or scene",
                    "overlay_text": "optional, maximum 12 words, derived from the post",
                    "composition": "mobile-first composition",
                    "style": "provider-neutral art direction",
                    "generation_prompt": "imagery-only provider prompt; explicitly no text/logos/watermarks",
                    "negative_guidance": "array of visual failure modes to avoid",
                    "alt_text": "concise accessible description",
                },
                "carousel": {
                    "cover_headline": "concise hook derived from the post",
                    "design_system": "one consistent layout/art-direction system",
                    "slides": "4-8 ordered objects with role, headline, body, visual_direction; every slide must advance the idea",
                    "alt_text": "concise accessible summary of the carousel",
                },
                "rule": "Return only the object matching asset_type; the other object should be null.",
            },
        },
        ensure_ascii=False,
    )

    try:
        out = planner_client.call(system, user, response_json=True)
        raw = str(out.get("text", "") if isinstance(out, dict) else out)
        payload = _parse_payload(raw)
        asset_type = str(payload.get("asset_type") or "").strip()
        if preference != "auto" and asset_type != preference:
            return _deferred(
                "Visual planner did not honor the explicit format preference.",
                warning="visual_format_preference_mismatch",
            )
        if asset_type not in {"single_image", "carousel"}:
            return _deferred("Visual planner returned an unsupported asset type.", warning="visual_invalid_type")

        plan = VisualAssetPlan(
            status="planned",
            source_candidate=source_candidate,
            asset_type=asset_type,
            rationale=str(payload.get("rationale") or "").strip(),
            creative_goal=str(payload.get("creative_goal") or "").strip(),
            aspect_ratio="4:5",
            single_image=_single_image(payload) if asset_type == "single_image" else None,
            carousel=_carousel(payload) if asset_type == "carousel" else None,
            review_required=True,
        )
        copy_reasons = _copy_guard(post_text, _visual_copy(plan))
        if copy_reasons:
            return _deferred(
                "Visual copy introduced unsupported factual tokens and requires replanning.",
                warning="; ".join(copy_reasons),
            )
        return plan
    except (ValidationError, ValueError, TypeError, KeyError) as exc:
        return _deferred(
            "Visual planner returned an invalid structured brief.",
            warning=f"visual_plan_invalid:{type(exc).__name__}",
        )
    except Exception as exc:
        return _deferred(
            "Visual planning was unavailable; do not fabricate a fallback asset brief.",
            warning=f"visual_plan_unavailable:{type(exc).__name__}",
        )
