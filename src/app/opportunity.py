from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


# Specificity is intentionally split into two distinct questions while
# preserving the original 100-point weighting: do we have a real concrete
# detail, and is it distinctive enough to make the post feel lived rather than
# interchangeable with generic creator content?
WEIGHTS: dict[str, int] = {
    "outsider_clarity": 15,
    "professional_relevance": 15,
    "concrete_evidence": 9,
    "distinctiveness": 6,
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
    strongest_evidence_title: str = ""
    strongest_evidence_fact: str = ""
    missing_evidence_question: str = ""
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "decision": self.decision,
            "goal": self.goal,
            "earned_question": self.earned_question,
            "reason": self.reason,
            "dimensions": dict(self.dimensions),
            "strongest_evidence_title": self.strongest_evidence_title,
            "strongest_evidence_fact": self.strongest_evidence_fact,
            "missing_evidence_question": self.missing_evidence_question,
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
        and dimensions["concrete_evidence"] >= 3
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
    # Almost no outsider relevance is a weak topic, not a request for more
    # detail. Do not bother the user with follow-up questions for content that
    # should not become a post in the first place.
    if dimensions["outsider_clarity"] <= 1 or dimensions["professional_relevance"] <= 1:
        return "skip"

    evidence_is_thin = dimensions["concrete_evidence"] <= 2 or dimensions["distinctiveness"] <= 2
    promising_subject = (
        dimensions["outsider_clarity"] >= 3
        and dimensions["professional_relevance"] >= 3
        and dimensions["novel_insight"] >= 3
        and dimensions["practical_usefulness"] >= 3
    )
    if evidence_is_thin:
        return "needs_more_evidence" if promising_subject else "skip"

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


def _selected_evidence(payload: dict[str, Any], evidence: list[dict[str, str]]) -> tuple[str, str]:
    """Select an exact supplied evidence item; never accept invented detail text."""

    if not evidence:
        return "", ""
    try:
        index = int(payload.get("strongest_evidence_index", -1))
    except (TypeError, ValueError):
        index = -1
    if index < 0 or index >= len(evidence):
        return "", ""
    item = evidence[index]
    return item["title"], item["fact"]


def _missing_question(payload: dict[str, Any], topic: str) -> str:
    question = str(payload.get("missing_evidence_question") or "").strip()
    if question:
        if not question.endswith("?"):
            question += "?"
        return question[:500]
    return f"What is the clearest concrete example from your actual experience that shows '{topic}'?"[:500]


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
    """Run a bounded evidence-first preflight before a full LinkedIn draft.

    This is a usefulness/relevance heuristic, not a virality predictor. The model
    scores named dimensions and identifies the strongest supplied evidence by
    index. Weighted score, evidence selection, gate decision, goal selection,
    and earned-question rules are deterministic in code. If a promising subject
    lacks concrete/distinctive evidence, the system asks for one targeted detail
    instead of drafting generic filler or inventing specificity.
    """

    source_facts = []
    for item in evidence:
        fact = str(item.get("fact") or item.get("one_liner") or "").strip()
        if fact:
            source_facts.append({"title": str(item.get("title", "")).strip(), "fact": fact})

    system = (
        "You are a strict LinkedIn content-opportunity and evidence evaluator. Decide whether a real professional "
        "topic has enough value and grounded specificity to justify drafting a post. Do not write the post. Do not "
        "predict virality or invent evidence. Score each named dimension from 0 (absent) to 5 (exceptional) using "
        "only the supplied topic, audience, objective, and evidence. Identify the single strongest supplied evidence "
        "item by zero-based index. If the topic is promising but evidence is too generic, return one concise question "
        "that would elicit the missing concrete detail. Return JSON only."
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
                "concrete_evidence": "Do the supplied facts include a specific event, observation, consequence, decision, quote, number, or other real detail that can anchor the post?",
                "distinctiveness": "Does the evidence contain something that feels particular to this actual experience rather than interchangeable with thousands of generic AI/business posts?",
                "novel_insight": "Is there a non-obvious lesson, tension, or reframing?",
                "practical_usefulness": "Can the reader carry a useful idea into their own work?",
                "emotional_tension": "Is there recognition, surprise, frustration, curiosity, relief, or another earned human stake?",
                "conversation_potential": "Is there a genuine tradeoff or experience that qualified readers could discuss?",
                "shareability": "Would sharing this make another professional look useful rather than merely agreeable?",
                "voice_fit": "Does this topic support a direct, human, causally insightful point rather than empty promotion?",
            },
            "required_output": {
                **{key: "integer 0-5" for key in _DIMENSION_KEYS},
                "strongest_evidence_index": "zero-based integer index into evidence, or -1 if no supplied item is concrete enough",
                "missing_evidence_question": "one concise targeted question if concrete_evidence or distinctiveness is below 3; otherwise empty string",
                "reason": "one concise sentence explaining the strongest reason to draft, request evidence, or skip",
            },
        },
        ensure_ascii=False,
    )

    try:
        out = client.call(system, user, response_json=True)
        text = str(out.get("text", "") if isinstance(out, dict) else out)
        payload = _parse_payload(text)
        dimensions = {key: _clamp_dimension(payload.get(key)) for key in _DIMENSION_KEYS}
        title, fact = _selected_evidence(payload, source_facts)

        # The model cannot award itself strong concrete-evidence credit without
        # pointing to an actual supplied item. This closes the path where an LLM
        # could rate an abstract theme as specific and then draft invented detail.
        if dimensions["concrete_evidence"] >= 3 and not fact:
            dimensions["concrete_evidence"] = 2
        if dimensions["distinctiveness"] >= 3 and not fact:
            dimensions["distinctiveness"] = 2

        score = _score(dimensions)
        goal = requested_goal if requested_goal in {"reach", "conversation", "authority"} else _auto_goal(dimensions)
        decision = _decision(score, dimensions, minimum_score)
        earned_question = (
            decision == "draft"
            and goal == "conversation"
            and dimensions["conversation_potential"] >= 4
        )
        reason = str(payload.get("reason") or "Opportunity scored from the supplied topic and evidence.").strip()
        missing_question = _missing_question(payload, topic) if decision == "needs_more_evidence" else ""
        return OpportunityAssessment(
            score=score,
            decision=decision,
            goal=goal,
            earned_question=earned_question,
            reason=reason[:500],
            dimensions=dimensions,
            strongest_evidence_title=title,
            strongest_evidence_fact=fact,
            missing_evidence_question=missing_question,
        )
    except Exception as exc:
        goal = requested_goal if requested_goal in {"reach", "conversation", "authority"} else "authority"
        fallback = {key: 3 for key in _DIMENSION_KEYS}
        warning = (f"preflight_unavailable:{type(exc).__name__}",)
        if not source_facts:
            return OpportunityAssessment(
                score=_score(fallback),
                decision="needs_more_evidence",
                goal=goal,
                earned_question=False,
                reason="Opportunity preflight was unavailable and no grounded detail was supplied; request one concrete example before drafting.",
                dimensions=fallback,
                missing_evidence_question=_missing_question({}, topic),
                warnings=warning,
            )

        # If grounded evidence exists, preserve the previous availability-first
        # behavior. Use the first exact supplied fact as a conservative anchor so
        # a classifier outage cannot turn into invented specificity.
        first = source_facts[0]
        return OpportunityAssessment(
            score=_score(fallback),
            decision="draft",
            goal=goal,
            earned_question=False,
            reason="Opportunity preflight was unavailable; drafting conservatively from supplied evidence instead of blocking the request.",
            dimensions=fallback,
            strongest_evidence_title=first["title"],
            strongest_evidence_fact=first["fact"],
            warnings=warning,
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
