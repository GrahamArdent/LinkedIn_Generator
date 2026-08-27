from __future__ import annotations

import json

from src.app.visual_assets import plan_visual_asset


POST = (
    "I built an AI planning system to save me time. Then I caught it creating work by forgetting what it already knew.\n\n"
    "The useful rule became simple: keep what is already known and reopen a decision only when new evidence gives you a reason."
)

STYLE = {
    "shared_style": ["clean_editorial", "modern_professional"],
    "hard_avoids": ["generic robot heads", "embedded generated text"],
}


class FixtureClient:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def call(self, system: str, user: str, response_json: bool = True):
        self.calls.append({"system": system, "user": user, "response_json": response_json})
        return {"text": json.dumps(self.payload)}


def single_payload():
    return {
        "asset_type": "single_image",
        "rationale": "The post is one sharp tension, so one metaphor is stronger than a sequence.",
        "creative_goal": "Make unnecessary rework feel immediately visible.",
        "aspect_ratio": "4:5",
        "single_image": {
            "concept": "A clean path moving forward while a second loop unnecessarily circles back to a completed checkpoint.",
            "overlay_text": "When careful becomes rework",
            "composition": "One dominant forward path with a small looping detour, generous negative space for later typography.",
            "style": "Clean editorial conceptual illustration, grounded and professional.",
            "generation_prompt": "Editorial conceptual illustration of a forward path with an unnecessary loop returning to a completed checkpoint",
            "negative_guidance": ["robot heads", "neon dashboards", "stock office scenes"],
            "alt_text": "A forward path is interrupted by an unnecessary loop back to a completed checkpoint.",
        },
        "carousel": None,
    }


def carousel_payload(*, unsafe_number: bool = False):
    slide_body = "Reopen it only when new evidence gives you a reason."
    if unsafe_number:
        slide_body = "This creates 42% more work."
    return {
        "asset_type": "carousel",
        "rationale": "The post benefits from showing the surface problem, consequence, and better rule in sequence.",
        "creative_goal": "Turn the lesson into a short progression a reader can swipe through.",
        "aspect_ratio": "4:5",
        "single_image": None,
        "carousel": {
            "cover_headline": "When careful becomes rework",
            "design_system": "Minimal editorial cards with one strong sentence and one simple visual motif per slide.",
            "slides": [
                {
                    "role": "cover",
                    "headline": "When careful becomes rework",
                    "body": "",
                    "visual_direction": "A clean forward line interrupted by a loop back.",
                },
                {
                    "role": "context",
                    "headline": "The system forgot what it already knew",
                    "body": "Settled decisions started coming back into the conversation.",
                    "visual_direction": "Completed checkpoint appearing again on the path.",
                },
                {
                    "role": "insight",
                    "headline": "Another check is not automatically safer",
                    "body": "A check earns its place when it reduces a real uncertainty.",
                    "visual_direction": "One useful checkpoint contrasted with one redundant loop.",
                },
                {
                    "role": "closer",
                    "headline": "Keep what is already known",
                    "body": slide_body,
                    "visual_direction": "Forward path continuing cleanly beyond the checkpoint.",
                },
            ],
            "alt_text": "A four-slide carousel showing how repeated checking can turn into rework and why settled decisions should stay settled unless new evidence appears.",
        },
    }


def test_single_image_plan_separates_typography_from_generated_imagery():
    client = FixtureClient(single_payload())

    plan = plan_visual_asset(
        post_text=POST,
        source_candidate="rewrite",
        audience="AI builders and operators",
        content_goal="authority",
        evidence=[{"title": "Build evidence", "fact": "The planning system reopened settled decisions."}],
        preference="auto",
        style_profile=STYLE,
        client=client,
    )

    assert plan.status == "planned"
    assert plan.asset_type == "single_image"
    assert plan.source_candidate == "rewrite"
    assert plan.single_image is not None
    assert plan.single_image.overlay_text == "When careful becomes rework"
    assert "No embedded text" in plan.single_image.generation_prompt
    assert plan.carousel is None
    assert "generic robot" in client.calls[0]["system"]


def test_carousel_plan_requires_a_real_sequence_and_keeps_slide_count_bounded():
    client = FixtureClient(carousel_payload())

    plan = plan_visual_asset(
        post_text=POST,
        source_candidate="original",
        audience="AI builders and operators",
        content_goal="authority",
        evidence=[],
        preference="carousel",
        style_profile=STYLE,
        client=client,
    )

    assert plan.status == "planned"
    assert plan.asset_type == "carousel"
    assert plan.carousel is not None
    assert len(plan.carousel.slides) == 4
    assert [slide.slide_number for slide in plan.carousel.slides] == [1, 2, 3, 4]
    assert plan.single_image is None


def test_visual_copy_cannot_introduce_a_new_numeric_claim():
    client = FixtureClient(carousel_payload(unsafe_number=True))

    plan = plan_visual_asset(
        post_text=POST,
        source_candidate="rewrite",
        audience="AI builders",
        content_goal="authority",
        evidence=[],
        preference="carousel",
        style_profile=STYLE,
        client=client,
    )

    assert plan.status == "deferred"
    assert plan.asset_type is None
    assert "new number" in " ".join(plan.warnings)


def test_explicit_format_preference_mismatch_defers_instead_of_guessing():
    client = FixtureClient(single_payload())

    plan = plan_visual_asset(
        post_text=POST,
        source_candidate="original",
        audience="AI builders",
        content_goal="reach",
        evidence=[],
        preference="carousel",
        style_profile=STYLE,
        client=client,
    )

    assert plan.status == "deferred"
    assert plan.warnings == ["visual_format_preference_mismatch"]


def test_invalid_carousel_structure_defers_without_fabricating_missing_slides():
    payload = carousel_payload()
    payload["carousel"]["slides"] = payload["carousel"]["slides"][:2]
    client = FixtureClient(payload)

    plan = plan_visual_asset(
        post_text=POST,
        source_candidate="original",
        audience="AI builders",
        content_goal="authority",
        evidence=[],
        preference="carousel",
        style_profile=STYLE,
        client=client,
    )

    assert plan.status == "deferred"
    assert any(item.startswith("visual_plan_invalid:") for item in plan.warnings)
