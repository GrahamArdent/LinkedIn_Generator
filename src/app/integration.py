from __future__ import annotations

from collections.abc import Callable
from hashlib import sha256
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .api import run_generation
from .contracts import LinkedInContentRequest, LinkedInContentResult, SelectedCandidate, VisualAssetPlan
from .utils import load_yaml
from .visual_assets import plan_visual_asset

Generator = Callable[..., dict[str, Any]]
VisualPlanner = Callable[..., VisualAssetPlan | dict[str, Any]]
CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def _publish_candidate(
    payload: dict[str, Any], *, threshold: int
) -> SelectedCandidate | None:
    """Resolve one qualified candidate, failing closed on malformed review data."""

    if payload.get("status", "drafted") != "drafted":
        return None
    review = payload.get("review")
    if not isinstance(review, dict) or review.get("publish_ready") is not True:
        return None
    if type(review.get("threshold")) is not int or review["threshold"] != threshold:
        return None
    source = review.get("recommendation")
    if source not in ("original", "rewrite"):
        return None
    candidate = review.get(source)
    if not isinstance(candidate, dict):
        return None
    if source == "rewrite" and candidate.get("guard_accepted") is not True:
        return None
    body, score = candidate.get("body"), candidate.get("score")
    if not isinstance(body, str) or not body.strip():
        return None
    if type(score) is not int or not threshold <= score <= 100:
        return None
    # Preserve the actual UTF-8 bytes: normalization would break provenance.
    digest = sha256(body.encode("utf-8")).hexdigest()
    return SelectedCandidate(
        candidate_id=f"{source}:{digest}",
        source=source,
        body=body,
        score=score,
        content_sha256=digest,
    )


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
    voice_selection = {"writing_voice_id": request.writing_voice_id} if request.writing_voice_id is not None else {}
    payload = generator(
        **voice_selection,
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
    selected = _publish_candidate(payload, threshold=request.publish_quality_threshold)
    if request.visual_asset_plan and status == "drafted":
        if selected is None:
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
                post_text=selected.body,
                source_candidate=selected.source,
                audience=request.audience,
                content_goal=resolved_goal,
                evidence=evidence,
                preference=request.visual_asset_preference,
                style_profile=style_profile,
            )
            try:
                visual_asset = planned if isinstance(planned, VisualAssetPlan) else VisualAssetPlan.model_validate(planned)
            except ValidationError:
                visual_asset = VisualAssetPlan(
                    status="deferred",
                    rationale="The visual planner returned an invalid plan.",
                    warnings=["invalid_visual_plan"],
                )
            if visual_asset.status == "planned":
                if (
                    visual_asset.source_candidate != selected.source
                    or visual_asset.source_content_sha256 not in (None, selected.content_sha256)
                ):
                    visual_asset = VisualAssetPlan(
                        status="deferred",
                        rationale="The visual planner returned a different text candidate.",
                        warnings=["selected_candidate_mismatch"],
                    )
                else:
                    visual_asset = visual_asset.model_copy(
                        update={"source_content_sha256": selected.content_sha256}
                    )


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
        selected_candidate=selected,
        visual_asset=visual_asset,
    )
