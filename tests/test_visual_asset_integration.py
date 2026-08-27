from __future__ import annotations

from src.app.contracts import LinkedInContentRequest, VisualAssetPlan
from src.app.integration import generate_content


class CapturingPlanner:
    def __init__(self):
        self.calls = []

    def __call__(self, **kwargs):
        self.calls.append(kwargs)
        return VisualAssetPlan(
            status="planned",
            source_candidate=kwargs["source_candidate"],
            asset_type="single_image",
            rationale="One visual metaphor fits the post.",
            creative_goal="Make the core tension visible.",
            single_image={
                "concept": "A clean forward path with one unnecessary loop back.",
                "overlay_text": "When careful becomes rework",
                "composition": "One strong focal path with negative space.",
                "style": "Clean editorial conceptual illustration.",
                "generation_prompt": "A clean forward path with one unnecessary loop. No embedded text, lettering, logos, watermarks, fake interface labels, or pseudo-typography.",
                "negative_guidance": ["robots", "neon dashboards"],
                "alt_text": "A forward path is interrupted by an unnecessary loop.",
            },
        )


def test_publish_ready_rewrite_is_the_visual_planning_source():
    planner = CapturingPlanner()

    def fake_generator(**_kwargs):
        return {
            "status": "drafted",
            "body": "Draft A",
            "hashtags": [],
            "sources": [],
            "telemetry": {"content_goal": "authority"},
            "review": {
                "threshold": 90,
                "publish_ready": True,
                "recommendation": "rewrite",
                "original": {"body": "Draft A", "score": 87},
                "rewrite": {"body": "Draft B", "score": 94, "guard_accepted": True},
            },
        }

    result = generate_content(
        LinkedInContentRequest(
            topic="A real AI workflow lesson",
            visual_asset_plan=True,
            visual_asset_preference="auto",
        ),
        generator=fake_generator,
        visual_planner=planner,
    )

    assert len(planner.calls) == 1
    assert planner.calls[0]["post_text"] == "Draft B"
    assert planner.calls[0]["source_candidate"] == "rewrite"
    assert result.visual_asset is not None
    assert result.visual_asset.status == "planned"
    assert result.visual_asset.source_candidate == "rewrite"
    # The public body remains the preserved Draft A; review identifies the recommended B.
    assert result.body == "Draft A"


def test_below_threshold_text_defers_visual_planning_without_spending_a_call():
    planner = CapturingPlanner()

    def fake_generator(**_kwargs):
        return {
            "status": "drafted",
            "body": "Draft A",
            "hashtags": [],
            "sources": [],
            "telemetry": {},
            "review": {
                "threshold": 90,
                "publish_ready": False,
                "recommendation": "rewrite_below_threshold",
                "original": {"body": "Draft A", "score": 86},
                "rewrite": {"body": "Draft B", "score": 89, "guard_accepted": True},
            },
        }

    result = generate_content(
        LinkedInContentRequest(topic="A topic", visual_asset_plan=True),
        generator=fake_generator,
        visual_planner=planner,
    )

    assert planner.calls == []
    assert result.visual_asset is not None
    assert result.visual_asset.status == "deferred"
    assert result.visual_asset.warnings == ["publish_ready_candidate_required"]


def test_visual_planning_can_be_disabled_without_changing_generation():
    planner = CapturingPlanner()

    def fake_generator(**_kwargs):
        return {
            "status": "drafted",
            "body": "Publish-ready post",
            "hashtags": [],
            "sources": [],
            "telemetry": {},
            "review": {
                "threshold": 90,
                "publish_ready": True,
                "recommendation": "original",
                "original": {"body": "Publish-ready post", "score": 92},
                "rewrite": None,
            },
        }

    result = generate_content(
        LinkedInContentRequest(topic="A topic", visual_asset_plan=False),
        generator=fake_generator,
        visual_planner=planner,
    )

    assert planner.calls == []
    assert result.visual_asset is None


def test_non_drafted_result_does_not_plan_a_visual():
    planner = CapturingPlanner()

    def fake_generator(**_kwargs):
        return {
            "status": "needs_more_evidence",
            "body": "",
            "hashtags": [],
            "sources": [],
            "telemetry": {"missing_evidence_question": "What happened?"},
            "review": {},
        }

    result = generate_content(
        LinkedInContentRequest(topic="A topic"),
        generator=fake_generator,
        visual_planner=planner,
    )

    assert planner.calls == []
    assert result.visual_asset is None
