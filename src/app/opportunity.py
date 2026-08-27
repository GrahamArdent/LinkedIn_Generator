from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


WEIGHTS: dict[str, int] = {
    "outsider_clarity": 15,
    "professional_relevance": 15,
    "specificity": 15,
    "novel_insight": 15,
    "practical_usefulness": 10,
    "emotional_tension": 10,
    "conversation_potential": 8,
    "shareability": 7,
    "voice_fit": 5,
}

_DIMENSION_KEYS = tuple(WEIGHTS)
_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


@dataclass(frozen=True)
class OpportunityAssessment:
    score: int
    decision: str
    goal: str
    earned_question: bool
    reason: str
    dimensions: dict[str, int]
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "decision": self.decision,
            "goal": self.goal,
            "earned_question": self.earned_question,
            "reason": self.reason,
            "dimensions": dict(self.dimensions),
            "warnings": list(self.warnings),
        }


def _clamp_dimension(value: Any) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = 0
    return max(0, min(5, parsed))


def _score(dimensions: dict[str, int]) -> int:
    total = 0.0
    for key, weight in WEIGHTS.items():
        total += (dimensions[key] / 5.0) * weight
    return int(round(total))


def _auto_goal(dimensions: dict[str, int]) -> str:
    if (
        dimensions["conversation_potential"] >= 4
        and dimensions["specificity"] >= 3
        and dimensions["outsider_clarity"] >= 3
    ):
        return "conversation"
    if (
        dimensions["outsider_clarity"] >= 4
        and dimensions["professional_relevance"] >= 4
        and dimensions["novel_insight"] >= 4
    ):
        return "reach"
    return "authority"


def _decision(score: int, dimensions: dict[str, int], minimum_score: int) -> str:
    # A post with almost no outsider clarity or professional relevance should not
    # be drafted merely because other dimensions happen to score well.
    if dimensions["outsider_clarity"] <= 1 or dimensions["professional_relevance"] <= 1:
        return "skip"
    return "draft" if score >= minimum_score else "skip"


def _parse_payload(text: str) -> dict[str, Any]:
    raw = text.strip()
    match = _JSON_RE.search(raw)
    if not match:
        raise ValueError("opportunity preflight returned no JSON object")
    payload = json.loads(match.group(0))
    if not isinstance(payload, dict):
        raise ValueError("opportunity preflight JSON must be an object")
    return payload


def assess_opportunity(
    *,
    topic: str,
    audience: str,
    objective: str,
    evidence: list[dict[str, Any]],
    client: Any,
    requested_goal: str = "auto",
    minimum_score: int = 60,
) -> OpportunityAssessment:
    """Run a bounded preflight before spending on a full LinkedIn draft.

    This is a usefulness/relevance heuristic, not a virality predictor. The model
    only scores nine named 0-5 dimensions. The weighted total, gate decision,
    goal selection, and earned-question rule are deterministic in code.
    """

    source_facts = [
        {
            "title": str(item.get("title", "")),
            "fact": str(item.get("fact") or item.get("one_liner") or ""),
        }
        for item in evidence
    ]
    system = (
        "You are a strict LinkedIn content-opportunity evaluator. Decide whether a real professional "
        "topic has enough value to justify drafting a post. Do not write the post. Do not predict "
        "virality or invent evidence. Score each named dimension from 0 (absent) to 5 (exceptional) "
        "using only the supplied topic, audience, objective, and evidence. Return JSON only."
    )
    user = json.dumps(
        {
            "topic": topic,
            "audience": audience,
            "objective": objective,
            "evidence": source_facts,
            "dimensions": {
                "outsider_clarity": "Can a smart stranger understand why this matters?",
                "professional_relevance": "Is it professionally useful to the intended audience?",
                "specificity": "Is there a concrete detail, observation, or evidence rather than a generic theme?",
                "novel_insight": "Is there a non-obvious lesson, tension, or reframing?",
                "practical_usefulness": "Can the reader carry a useful idea into their own work?",
                "emotional_tension": "Is there recognition, surprise, frustration, curiosity, relief, or another earned human stake?",
                "conversation_potential": "Is there a genuine tradeoff or experience that qualified readers could discuss?",
                "shareability": "Would sharing this make another professional look useful rather than merely agreeable?",
                "voice_fit": "Does this topic support a direct, human, causally insightful point rather than empty promotion?",
            },
            "required_output": {
                **{key: "integer 0-5" for key in _DIMENSION_KEYS},
                "reason": "one concise sentence explaining the strongest reason to draft or skip",
            },
        },
        ensure_ascii=False,
    )

    try:
        out = client.call(system, user, response_json=True)
        text = str(out.get("text", "") if isinstance(out, dict) else out)
        payload = _parse_payload(text)
        dimensions = {key: _clamp_dimension(payload.get(key)) for key in _DIMENSION_KEYS}
        score = _score(dimensions)
        goal = requested_goal if requested_goal in {"reach", "conversation", "authority"} else _auto_goal(dimensions)
        decision = _decision(score, dimensions, minimum_score)
        earned_question = (
            decision == "draft"
            and goal == "conversation"
            and dimensions["conversation_potential"] >= 4
        )
        reason = str(payload.get("reason") or "Opportunity scored from the supplied topic and evidence.").strip()
        return OpportunityAssessment(
            score=score,
            decision=decision,
            goal=goal,
            earned_question=earned_question,
            reason=reason[:500],
            dimensions=dimensions,
        )
    except Exception as exc:
        # Availability beats a brittle classifier. A malformed preflight should
        # be visible in telemetry but should not silently block a good post.
        goal = requested_goal if requested_goal in {"reach", "conversation", "authority"} else "authority"
        fallback = {key: 3 for key in _DIMENSION_KEYS}
        return OpportunityAssessment(
            score=_score(fallback),
            decision="draft",
            goal=goal,
            earned_question=False,
            reason="Opportunity preflight was unavailable; drafting conservatively instead of blocking the request.",
            dimensions=fallback,
            warnings=(f"preflight_unavailable:{type(exc).__name__}",),
        )


def ending_guidance(assessment: OpportunityAssessment) -> str:
    if assessment.goal == "conversation" and assessment.earned_question:
        return (
            "A genuine question is earned here. End with one specific question that invites relevant "
            "experience, judgment, or a real tradeoff; never ask for likes, agreement, or generic 'thoughts'."
        )
    if assessment.goal == "reach":
        return (
            "End with a memorable stand-alone insight. Prefer broad professional usefulness over a forced question."
        )
    return (
        "End with the strongest useful insight or earned provocation. A question is optional and should be omitted "
        "unless the reader genuinely has something substantive to contribute."
    )
