from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from .rewrite_guard import evaluate_rewrite


WEIGHTS: dict[str, int] = {
    "outsider_clarity": 15,
    "professional_relevance": 15,
    "specificity": 15,
    "novel_insight": 15,
    "practical_usefulness": 10,
    "emotional_tension": 10,
    "conversation_potential": 8,
    "shareability": 7,
    "voice_authenticity": 5,
}

_DIMENSION_KEYS = tuple(WEIGHTS)
_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


@dataclass(frozen=True)
class PublishQualityAssessment:
    score: int | None
    dimensions: dict[str, int]
    gaps: tuple[str, ...]
    rationale: str
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "dimensions": dict(self.dimensions),
            "gaps": list(self.gaps),
            "rationale": self.rationale,
            "warnings": list(self.warnings),
        }


def _clamp_dimension(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = 0
    return max(0, min(5, parsed))


def _weighted_score(dimensions: dict[str, int]) -> int:
    total = 0.0
    for key, weight in WEIGHTS.items():
        total += (dimensions[key] / 5.0) * weight
    return max(0, min(100, int(round(total))))


def _parse_payload(text: str) -> dict[str, Any]:
    match = _JSON_RE.search(text.strip())
    if not match:
        raise ValueError("publish-quality evaluator returned no JSON object")
    payload = json.loads(match.group(0))
    if not isinstance(payload, dict):
        raise ValueError("publish-quality evaluator JSON must be an object")
    return payload


def assess_publish_quality(
    *,
    text: str,
    audience: str,
    content_goal: str,
    evidence: list[dict[str, Any]],
    persona_profile: dict[str, Any],
    client: Any,
) -> PublishQualityAssessment:
    """Assess the finished post separately from deterministic compliance quality.

    This score estimates publish readiness, not virality. The model evaluates
    named dimensions from 0-5; weighting and final score calculation are kept
    deterministic in code. Evidence is supplied so specificity can be judged
    against grounded material rather than rewarding invented detail.
    """

    source_facts = [
        {
            "title": str(item.get("title") or "").strip(),
            "fact": str(item.get("fact") or item.get("one_liner") or "").strip(),
        }
        for item in evidence
        if str(item.get("fact") or item.get("one_liner") or "").strip()
    ]
    spoken = persona_profile.get("spoken_voice") if isinstance(persona_profile.get("spoken_voice"), dict) else {}
    voice = persona_profile.get("voice_authority") if isinstance(persona_profile.get("voice_authority"), dict) else {}
    brief = dict(persona_profile.get("editorial_context") or {})
    voice_context = dict(persona_profile)
    if "writing_voice" in voice_context:
        # The same brief is supplied separately below; do not repeat its thesis.
        voice_context.pop("editorial_context", None)

    system = (
        "You are a strict LinkedIn publish-quality evaluator. Score the finished post, not the raw topic, from 0 "
        "(absent) to 5 (exceptional) on each named dimension. Judge whether the post is understandable, useful, "
        "specific, distinctive, interesting, shareable, and authentic enough to publish. Do not reward clickbait, "
        "engagement bait, unsupported specificity, or generic LinkedIn polish. Use the supplied evidence only to "
        "judge whether concrete details are grounded. This is a publish-readiness heuristic, not a promise of "
        "virality. These ratings are not calibrated to the author's human judgments or engagement outcomes. "
        "Apply the rating anchors to each dimension; never inflate scores to meet a threshold. "
        "Use the same brief and voice context as the writer. If writing_voice is present, assess voice fit against "
        "its selected style_traits over default persona style; approved examples supply compatible details only. "
        "Preserve factual and author-POV boundaries. "
        "Identify the largest fixable defect first; "
        "missing factual support is an evidence-brief gap, not permission to invent a better story. Return JSON only."
    )
    user = json.dumps(
        {
            "post": text,
            "audience": audience,
            "content_goal": content_goal,
            "grounded_evidence": source_facts,
            "voice_context": voice_context,
            "editorial_brief": brief,
            "approved_voice_examples": list(brief.get("approved_voice_examples") or []),
            "calibration_status": "NOT_CALIBRATED_TO_HUMAN_JUDGMENTS",
            "rating_anchors": {
                "0": "Absent, contradicted or unusable for this dimension.",
                "1": "Severe weakness; the reader must reconstruct the point.",
                "2": "Partial; generic, unclear or insufficiently supported.",
                "3": "Adequate but ordinary; the dimension works with a material limitation.",
                "4": "Strong; grounded, clear and useful with only a minor weakness.",
                "5": "Exceptional for this supplied brief; explain why the dimension earns this judgment, not merely because no rule was broken.",
            },
            "dimensions": {
                "outsider_clarity": "Can a smart stranger understand the post without project context?",
                "professional_relevance": "Does the post matter to the intended professional audience?",
                "specificity": "Is the post anchored in concrete grounded detail rather than abstractions?",
                "novel_insight": "Does it contain a non-obvious lesson, tension, or reframing?",
                "practical_usefulness": "Can a reader carry something useful into their own work?",
                "emotional_tension": "Is there earned curiosity, recognition, surprise, frustration, relief, or another human stake?",
                "conversation_potential": "Could qualified readers add substantive experience or judgment, whether or not the post ends in a question?",
                "shareability": "Would sharing the post make another professional look useful or insightful?",
                "voice_authenticity": "Does the wording feel natural for the supplied voice rather than generic creator copy?",
            },
            "required_output": {
                **{key: "integer 0-5" for key in _DIMENSION_KEYS},
                "gaps": "array of at most 3 concise weaknesses that most limit publish quality",
                "rationale": "one concise sentence explaining the overall score",
            },
        },
        ensure_ascii=False,
    )

    try:
        out = client.call(system, user, response_json=True)
        raw = str(out.get("text", "") if isinstance(out, dict) else out)
        payload = _parse_payload(raw)
        if any(type(payload.get(key)) is not int or not 0 <= payload[key] <= 5 for key in _DIMENSION_KEYS):
            raise ValueError("missing_or_invalid_publish_quality_dimension")
        dimensions = {key: payload[key] for key in _DIMENSION_KEYS}
        gaps_raw = payload.get("gaps")
        if (not isinstance(gaps_raw, list) or len(gaps_raw) > 3
                or any(not isinstance(g, str) or not g.strip() for g in gaps_raw)
                or not isinstance(payload.get("rationale"), str) or not payload["rationale"].strip()):
            raise ValueError("missing_or_invalid_publish_quality_judgment")
        gaps = tuple(
            str(item).strip()[:300]
            for item in (gaps_raw if isinstance(gaps_raw, list) else [])
            if str(item).strip()
        )[:3]
        rationale = str(payload.get("rationale") or "Publish quality scored from the finished post.").strip()[:500]
        return PublishQualityAssessment(
            score=_weighted_score(dimensions),
            dimensions=dimensions,
            gaps=gaps,
            rationale=rationale,
        )
    except Exception as exc:
        return PublishQualityAssessment(
            score=None,
            dimensions={},
            gaps=(),
            rationale="Publish-quality assessment was unavailable; do not infer publish readiness from the deterministic compliance score.",
            warnings=(f"publish_quality_unavailable:{type(exc).__name__}",),
        )


def _render(template: str, values: dict[str, Any]) -> str:
    out = template
    for key, value in values.items():
        token = "{" + key + "}"
        out = out.replace(token, json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value))
    return out


def rewrite_for_publish_quality(
    *,
    original: str,
    assessment: PublishQualityAssessment,
    prompt: dict[str, str],
    persona_profile: dict[str, Any],
    evidence: list[dict[str, Any]],
    voice_examples: list[dict[str, str]],
    content_goal: str,
    rules: dict[str, Any],
    client: Any,
) -> tuple[str, dict[str, Any]]:
    """Generate exactly one improvement candidate and apply the existing fact guard."""

    values = {
        "post": original,
        "primary_fix": assessment.gaps[0] if assessment.gaps else "Improve only a supported, identifiable weakness; otherwise preserve the original.",
        "publish_quality_report": assessment.as_dict(),
        "persona_profile": persona_profile,
        "allowed_sources": [
            {
                "title": str(item.get("title") or ""),
                "fact": str(item.get("fact") or item.get("one_liner") or ""),
            }
            for item in evidence
            if str(item.get("fact") or item.get("one_liner") or "").strip()
        ],
        "approved_voice_examples": list(voice_examples),
        "content_goal": content_goal,
    }
    system = _render(prompt.get("system", ""), values)
    user = _render(prompt.get("user_template", "{post}"), values)
    out = client.call(system, user, response_json=True)
    candidate = str(out.get("text", "") if isinstance(out, dict) else out).strip()
    guard = evaluate_rewrite(original, candidate, persona_profile, rules)
    return candidate, guard
