from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from .api import run_generation
from .contracts import LinkedInContentRequest, LinkedInContentResult, VisualAssetPlan
from .utils import load_yaml
from .visual_assets import plan_visual_asset

Generator = Callable[..., dict[str, Any]]
VisualPlanner = Callable[..., VisualAssetPlan | dict[str, Any]]
CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def _publish_candidate(payload: dict[str, Any]) -> tuple[str | None, str | None]:
    """Return the 90+ candidate selected by publish-quality review, if any."""

    review = payload.get("review") if isinstance(payload.get("review"), dict) else {}
    if not review or not bool(review.get("publish_ready")):
        return None, None

    recommendation = str(review.get("recommendation") or "")
    if recommendation == "rewrite":
        rewrite = review.get("rewrite") if isinstance(review.get("rewrite"), dict) else {}
        body = str(rewrite.get("body") or "").strip()
        score = rewrite.get("score")
        threshold = int(review.get("threshold") or 90)
        if body and score is not None and int(score) >= threshold and bool(rewrite.get("guard_accepted")):
            return "rewrite", body

    original = review.get("original") if isinstance(review.get("original"), dict) else {}
    body = str(original.get("body") or payload.get("body") or "").strip()
    score = original.get("score")
    threshold = int(review.get("threshold") or 90)
    if body and score is not None and int(score) >= threshold:
        return "original", body
    return None, None


def generate_content(
    request: LinkedInContentRequest,
    *,
    generator: Generator = run_generation,
    visual_planner: VisualPlanner = plan_visual_asset,
) -> LinkedInContentResult:
    """Generate a LinkedIn post package without taking orchestration ownership.

    LinkedIn Generator owns post intelligence and the provider-neutral visual
    companion brief. Dedication or another caller remains the owner of approval,
    scheduling, publishing, notifications, and canonical post state.
    """

    evidence = [item.model_dump() for item in request.evidence]
    payload = generator(
        topic=request.topic,
        services=request.services,
        persona_key=request.persona_key,
        audience=request.audience,
        objective=request.objective,
        author_pov=request.author_pov,
        content_goal=request.content_goal,
        opportunity_gate=request.opportunity_gate,
        publish_quality_gate=request.publish_quality_gate,
        publish_quality_threshold=request.publish_quality_threshold,
        targets=request.targets,
        allowed_sources=evidence,
        voice_examples=[item.model_dump() for item in request.voice_examples],
        # An empty list is intentional: Dedication-origin requests must not
        # inherit legacy cybersecurity hashtags merely because old defaults
        # exist in the prototype runtime.
        hashtags=request.hashtags,
    )

    visual_asset: VisualAssetPlan | None = None
    status = str(payload.get("status") or "drafted")
    if request.visual_asset_plan and status == "drafted":
        source_candidate, candidate_body = _publish_candidate(payload)
        if source_candidate is None or candidate_body is None:
            visual_asset = VisualAssetPlan(
                status="deferred",
                rationale=(
                    "Visual planning waits until the post has a publish-quality score at or above the configured "
                    "threshold, so image/carousel work is not spent on a text candidate that still needs revision."
                ),
                review_required=True,
                warnings=["publish_ready_candidate_required"],
            )
        else:
            style_profile = load_yaml(str(CONFIG_DIR / "visual_style.yaml"))
            telemetry = payload.get("telemetry") if isinstance(payload.get("telemetry"), dict) else {}
            resolved_goal = str(telemetry.get("content_goal") or "").strip() or request.content_goal
            planned = visual_planner(
                post_text=candidate_body,
                source_candidate=source_candidate,
                audience=request.audience,
                content_goal=resolved_goal,
                evidence=evidence,
                preference=request.visual_asset_preference,
                style_profile=style_profile,
            )
            visual_asset = planned if isinstance(planned, VisualAssetPlan) else VisualAssetPlan.model_validate(planned)

    return LinkedInContentResult(
        request_id=request.request_id,
        origin=request.origin,
        persona_key=request.persona_key,
        status=status,
        body=str(payload.get("body", "")),
        hashtags=list(payload.get("hashtags") or []),
        sources=list(payload.get("sources") or []),
        telemetry=dict(payload.get("telemetry") or {}),
        review=dict(payload.get("review") or {}),
        visual_asset=visual_asset,
    )
