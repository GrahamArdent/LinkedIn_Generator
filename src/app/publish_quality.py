from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
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

REVIEW_POLICY_VERSION = "essential-checks-v1"
ESSENTIAL_CHECKS = {
    "factual_integrity": "Claims and experiences are supported; preserve source limitations, author POV and safety rules. Missing support means needs_evidence; contradicted or unsafe claims mean revise.",
    "reader_relevance": "The specified audience understands the argument and why it matters without reconstructing specialist context.",
    "practical_value": "The reader gains a useful insight, question or action; a checklist is not mandatory.",
    "argument_voice": "The intended meaning and selected writing voice are preserved, with coherent development of the selected narrative: the evidence advances the thought, transitions connect it, and the landing follows from the argument. Strong voice cannot compensate for disordered or repetitive construction. No invented identity or experience.",
}


def essential_review_status(checks: Any) -> str:
    """Resolve non-compensable verdicts; malformed checks fail closed."""
    if not isinstance(checks, dict) or set(checks) != set(ESSENTIAL_CHECKS):
        return "assessment_unavailable"
    for item in checks.values():
        if (not isinstance(item, dict) or item.get("verdict") not in ("pass", "revise", "needs_evidence")
                or not isinstance(item.get("reason"), str) or not item["reason"].strip()):
            return "assessment_unavailable"
    if any(item["verdict"] == "needs_evidence" for item in checks.values()):
        return "needs_evidence"
    if checks["factual_integrity"]["verdict"] != "pass":
        return "blocked"
    if any(item["verdict"] != "pass" for item in checks.values()):
        return "needs_rework"
    return "reviewable"


_DIMENSION_KEYS = tuple(WEIGHTS)
_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


@dataclass(frozen=True)
class PublishQualityAssessment:
    score: int | None
    dimensions: dict[str, int]
    gaps: tuple[str, ...]
    rationale: str
    warnings: tuple[str, ...] = ()
    essential_checks: dict[str, dict[str, str]] = field(default_factory=dict)
    assessment_complete: bool = True
    revision_comparison: dict[str, str] | None = None

    @property
    def review_status(self) -> str:
        return essential_review_status(self.essential_checks) if self.assessment_complete else "assessment_unavailable"

    def as_dict(self) -> dict[str, Any]:
        return {
            "policy_version": REVIEW_POLICY_VERSION,
            "review_status": self.review_status,
            "essential_checks": self.essential_checks,
            **({"revision_comparison": self.revision_comparison} if self.revision_comparison else {}),
            "assessment_complete": self.assessment_complete,
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
    parent_text: str | None = None,
    passage_review: bool = False,
) -> PublishQualityAssessment:
    """Assess the finished post separately from deterministic compliance quality.

    The score is advisory; explicit essential verdicts determine review admission. The model evaluates
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
        "specific, distinctive, interesting, shareable, and authentic. Scores are advisory and never determine admission. "
        "Independently assess four essential checks with pass, revise or needs_evidence and a concrete reason. "
        "Passing permits human review only, never publication. Failures must identify an exact defect or claim, "
        "not merely ordinary novelty, restrained emotion, length or low sharing potential. "
        "Do not infer essential verdicts from numeric ratings. Novelty is relative to the intended reader. Do not reward clickbait, "
        "engagement bait, unsupported specificity, or generic LinkedIn polish. Use the supplied evidence only to "
        "judge whether concrete details are grounded. This is a publish-readiness heuristic, not a promise of "
        "virality. These ratings are not calibrated to the author's human judgments or engagement outcomes. "
        "Apply the rating anchors to each dimension; never inflate scores to meet a threshold. "
        "Use the same brief and voice context as the writer. If writing_voice is present, assess voice fit against "
        "its selected style_traits over default persona style; approved examples supply compatible details only. "
        "Preserve factual and author-POV boundaries. For argument_voice, report voice fidelity and construction separately "
        "within its concrete reason. Assess coherent development, not beat headings, keyword counts, a mandatory CTA "
        "or one paragraph per beat. Identify actual disordered, repetitive or unsupported reasoning; a strong voice "
        "does not compensate for broken construction. "
        "Identify the largest fixable defect first; "
        "missing factual support is an evidence-brief gap, not permission to invent a better story. Return JSON only."
    )
    request = {
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
            "essential_check_definitions": ESSENTIAL_CHECKS,
            "required_output": {
                "essential_checks": {
                    key: {"verdict": "pass | revise | needs_evidence",
                          "reason": "specific evidence-linked finding, or why the requirement is met"}
                    for key in ESSENTIAL_CHECKS
                },
                **{key: "integer 0-5" for key in _DIMENSION_KEYS},
                "gaps": "array of at most 3 concise weaknesses that most limit publish quality",
                "rationale": "one concise sentence explaining the overall score",
            },
        }
    bundle = brief.get("source_bundle") or {}
    passage_review = passage_review or "brief" in brief or "author_intent" in bundle or parent_text is not None
    if passage_review:
        system += (
            " Ground each essential verdict in this candidate. Cite its exact words under passage. "
            "If the relevant material is absent, report the gap with revise or needs_evidence and an empty passage. "
            "For argument_voice, identify the author's choice, question, comparison or observation and distinguish it "
            "from rhythm, first person and polish. A clear explainer can earn full credit without a quotation. "
            "For reader_relevance, identify the reader's recognizable decision or situation. For practical_value, "
            "explain what the ending gives that reader and whether the reasoning earns it. A readable distinction "
            "alone does not establish value. Unsupported specifics still fail factual_integrity."
        )
        for spec in request["required_output"]["essential_checks"].values():
            spec["passage"] = "exact substring of post supporting the reason, or empty if absent"
    if "author_intent" in bundle or "current_author_sources" in brief:
        system += (
            " For factual_integrity, check ownership of recommendations as well as facts. "
            "A first-person recommendation or opinion requires a supplied Graham account that supports "
            "that specific position. A calendar title, editor's summary or directions, public source, "
            "style example or previous draft cannot establish endorsement. Use current_author_sources "
            "when present, otherwise the supplied Graham account in source_bundle.sources. "
            "If the post presents an editorial proposal as Graham's view without matching support, "
            "return revise and cite the exact wording that assigns it to him. A reader-directed "
            "or conditional recommendation can pass without author endorsement."
        )
    if parent_text is not None:
        system += (
            " Compare the actual parent with this revision. Cite both texts exactly and explain which contribution "
            "or reader benefit was gained, lost, reframed or preserved. Check the ending. An absence in the revision "
            "can be shown by citing what it now says in that location. Judge the current text on its own merits."
        )
        request["parent_post"] = parent_text
        request["required_output"]["revision_comparison"] = {
            "parent_passage": "exact excerpt from parent_post", "current_passage": "exact excerpt from post",
            "change": "gain | loss | mixed | equivalent", "reason": "explain the effect using both passages",
        }
    user = json.dumps(request, ensure_ascii=False)

    try:
        out = client.call(system, user, response_json=True)
        raw = str(out.get("text", "") if isinstance(out, dict) else out)
        payload = _parse_payload(raw)
        checks = payload.get("essential_checks")
        complete=essential_review_status(checks)!="assessment_unavailable"
        comparison = None
        if passage_review and isinstance(checks, dict):
            def grounded(check):
                if not isinstance(check, dict):
                    return False
                passage = check.get("passage")
                if isinstance(passage, str) and passage.strip():
                    return passage in text
                return passage == "" and check.get("verdict") in ("revise", "needs_evidence")

            checks = {key: check for key, check in checks.items() if grounded(check)}
            complete = complete and essential_review_status(checks) != "assessment_unavailable"
        if parent_text is not None:
            value = payload.get("revision_comparison")
            if (isinstance(value, dict) and value.get("change") in ("gain", "loss", "mixed", "equivalent")
                    and all(isinstance(value.get(k), str) and value[k].strip()
                            for k in ("reason", "parent_passage", "current_passage"))
                    and value["parent_passage"] in parent_text and value["current_passage"] in text):
                comparison = {k: value[k] for k in ("change", "reason", "parent_passage", "current_passage")}
            else:
                complete = False
        if not complete:
            # Retain individually valid findings while the incomplete review
            # remains unavailable; advisory scores cannot fill missing verdicts.
            checks={k:v for k,v in (checks.items() if isinstance(checks,dict) else [])
                    if k in ESSENTIAL_CHECKS and isinstance(v,dict)
                    and v.get('verdict') in ('pass','revise','needs_evidence')
                    and isinstance(v.get('reason'),str) and v['reason'].strip()}
        valid_dimensions=all(type(payload.get(key)) is int and 0<=payload[key]<=5 for key in _DIMENSION_KEYS)
        dimensions={key:payload[key] for key in _DIMENSION_KEYS} if valid_dimensions else {}
        gaps_raw=payload.get("gaps")
        gaps=tuple(g[:300] for g in gaps_raw[:3] if isinstance(g,str) and g.strip()) if isinstance(gaps_raw,list) else ()
        rationale=payload.get("rationale")
        rationale=rationale[:500] if isinstance(rationale,str) and rationale.strip() else "Advisory rationale unavailable; essential findings retained."
        return PublishQualityAssessment(
            score=_weighted_score(dimensions) if valid_dimensions and complete else None,
            warnings=(() if valid_dimensions else ("advisory_dimensions_unavailable",)) + (() if complete else ("essential_assessment_incomplete",)),
            assessment_complete=complete,
            revision_comparison=comparison,
            dimensions=dimensions,
            essential_checks=checks,
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
        "primary_fix": "; ".join(
            f"{key}: {item['reason']}" for key, item in assessment.essential_checks.items()
            if item["verdict"] != "pass"
        ) or "Preserve the original; no essential defect was identified.",
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
