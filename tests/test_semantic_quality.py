from __future__ import annotations

from src.app.quality import evaluate_quality


def _persona(*, author_pov: str = "individual"):
    return {
        "active_author_pov": author_pov,
        "voice_authority": {
            "semantic_quality": {
                "default_author_pov": "individual",
                "internal_terms_needing_translation": [
                    "mode c",
                    "stage 0",
                    "execution spine",
                    "canonical intake",
                    "regression coverage",
                ],
                "generic_phrases": [
                    "in today's fast-paced world",
                    "game changer",
                    "here's the thing",
                ],
            }
        },
    }


def _rules():
    return {
        "emoji_max": 3,
        "allow_em_dash": False,
        "forbidden_phrases": [],
    }


def test_internal_project_language_is_not_treated_as_public_ready():
    draft = (
        "I found a small process bug while rebuilding a tool.\n\n"
        "Mode C was sending the project back to Stage 0, even though the work already existed. "
        "The canonical intake and regression coverage looked correct on paper, but the result was repeated work.\n\n"
        "That is the part I care about: planning should remove work, not recreate it."
    )

    report = evaluate_quality(draft, _persona(), _rules())

    assert report["score"] < 100
    assert set(report["signals"]["matched_internal_terms"]) == {
        "mode c",
        "stage 0",
        "canonical intake",
        "regression coverage",
    }
    assert any("internal project language" in issue for issue in report["issues"])


def test_individual_author_is_penalized_for_unjustified_collective_voice():
    draft = (
        "I found a planning problem that looked harmless at first.\n\n"
        "We kept reopening decisions we had already made, and our process started creating work instead of removing it.\n\n"
        "I changed the rule so existing projects keep what they already know."
    )

    report = evaluate_quality(draft, _persona(author_pov="individual"), _rules())

    assert report["score"] < 100
    assert report["signals"]["collective_pronoun_count"] >= 3
    assert any("Individual-author post" in issue for issue in report["issues"])


def test_team_author_pov_allows_collective_voice():
    draft = (
        "We found a planning problem that looked harmless at first.\n\n"
        "Our process was reopening decisions the team had already made. We changed the rule so existing projects keep what they already know.\n\n"
        "The lesson is simple: process should remove work, not recreate it."
    )

    report = evaluate_quality(draft, _persona(author_pov="team"), _rules())

    assert not any("Individual-author post" in issue for issue in report["issues"])


def test_stock_linkedin_language_is_penalized():
    draft = (
        "In today's fast-paced world, AI is a game changer.\n\n"
        "Here's the thing: useful systems still have to solve a real problem for a real person. "
        "I care more about whether the work gets easier than whether the demo looks impressive.\n\n"
        "That is where useful automation starts."
    )

    report = evaluate_quality(draft, _persona(), _rules())

    assert set(report["signals"]["matched_generic_phrases"]) == {
        "in today's fast-paced world",
        "game changer",
        "here's the thing",
    }
    assert any("stock LinkedIn/AI phrasing" in issue for issue in report["issues"])


def test_plain_first_person_public_language_avoids_new_semantic_penalties():
    draft = (
        "Good planning should make building easier.\n\n"
        "I found a part of my process that was treating an existing project like it was brand new. "
        "That meant I could end up answering questions I had already answered and reopening decisions I had already made.\n\n"
        "I changed the rule so existing projects keep what they already know. The lesson is simple: process should remove work, not recreate it."
    )

    report = evaluate_quality(draft, _persona(), _rules())

    assert report["signals"]["matched_internal_terms"] == []
    assert report["signals"]["matched_generic_phrases"] == []
    assert report["signals"]["collective_pronoun_count"] == 0
    assert not any("internal project language" in issue for issue in report["issues"])
    assert not any("stock LinkedIn/AI phrasing" in issue for issue in report["issues"])
    assert not any("Individual-author post" in issue for issue in report["issues"])
