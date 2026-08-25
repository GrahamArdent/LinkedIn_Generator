from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .api import run_generation
from .contracts import LinkedInContentRequest, LinkedInContentResult

Generator = Callable[..., dict[str, Any]]


def generate_content(
    request: LinkedInContentRequest,
    *,
    generator: Generator = run_generation,
) -> LinkedInContentResult:
    """Generate LinkedIn content from a bounded domain request.

    This function deliberately contains no scheduling, task selection,
    notification, or Dedication state logic. Orchestration belongs to the
    caller; LinkedIn Generator owns the content-generation concern.
    """

    payload = generator(
        topic=request.topic,
        services=request.services,
        persona_key=request.persona_key,
        audience=request.audience,
        objective=request.objective,
        targets=request.targets,
        allowed_sources=[item.model_dump() for item in request.evidence],
        # An empty list is intentional: Dedication-origin requests must not
        # inherit legacy cybersecurity hashtags merely because old defaults
        # exist in the prototype runtime.
        hashtags=request.hashtags,
    )

    return LinkedInContentResult(
        request_id=request.request_id,
        origin=request.origin,
        persona_key=request.persona_key,
        body=str(payload.get("body", "")),
        hashtags=list(payload.get("hashtags") or []),
        sources=list(payload.get("sources") or []),
        telemetry=dict(payload.get("telemetry") or {}),
    )
