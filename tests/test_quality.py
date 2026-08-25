from __future__ import annotations

from pathlib import Path

import yaml

from src.app.generation import Pipeline
from src.app.judge import judge_report, judge_score
from src.app.quality import evaluate_quality

ROOT = Path(__file__).resolve().parents[1]

# Synthetic structural fixture only. This is NOT an approved Graham voice exemplar.
STRUCTURAL_PASS = """What changed when we stopped asking whether AI looked impressive?

The better question was simpler: does it remove real friction for the person doing the work?

A buyer conversation made that clear. Novelty got attention, but reliability changed the decision.

That is the useful contrast for me. Build the clever thing, but earn trust with the boring details.

What would make this genuinely easier to use tomorrow?"""


def _graham_persona() -> dict:
    data = yaml.safe_load((ROOT / "config" / "personas.yaml").read_text(encoding="utf-8"))
    return data["personas"]["graham"]


def _rules() -> dict:
    cta = yaml.safe_load((ROOT / "config" / "cta_policies.yaml").read_text(encoding="utf-8"))
    return {
        "emoji_max": 3,
        "allow_em_dash": False,
        "forbidden_phrases": cta["forbidden_phrases"],
        "bullet_char": "🔹",
        "append_sources_block": False,
        "hashtag_min": 0,
        "hashtag_max": 5,
    }


def test_structural_fixture_scores_high_without_190_word_target():
    report = evaluate_quality(STRUCTURAL_PASS, _graham_persona(), _rules())

    assert report["score"] >= 95
    assert report["signals"]["word_count"] < 100
    assert report["signals"]["has_question"] is True
    assert report["signals"]["has_contrast"] is True


def test_subjective_voice_traits_are_explicitly_unscored():
    report = judge_report(STRUCTURAL_PASS, _graham_persona(), _rules())

    assert "direct" in report["signals"]["unscored_traits"]
    assert "humble" in report["signals"]["unscored_traits"]
    assert any("clichés" in item for item in report["signals"]["unscored_traits"])


def test_legacy_prototype_output_is_not_treated_as_graham_positive_evidence():
    legacy = (ROOT / "out" / "2025-10-07_ardent_post.md").read_text(encoding="utf-8")
    report = evaluate_quality(legacy, _graham_persona(), _rules())

    assert report["score"] < judge_score(STRUCTURAL_PASS, _graham_persona(), _rules())
    assert "Publishable body contains a URL." in report["issues"]


def test_judge_selects_better_structural_draft_and_records_score():
    poor = (
        "This is a very short update with no real contrast or question. "
        "Read more at https://example.com — how exposed are you"
    )
    pipe = Pipeline({"prompt_kit": _rules()}, client=object())

    selected = pipe.judge_select({}, _graham_persona(), [poor, STRUCTURAL_PASS])

    assert selected == STRUCTURAL_PASS
    assert pipe.last_judge_report is not None
    assert pipe.last_judge_report["score"] >= 95


def test_selected_quality_score_flows_into_existing_telemetry():
    pipe = Pipeline({"prompt_kit": _rules()}, client=object())
    pipe.judge_select({}, _graham_persona(), [STRUCTURAL_PASS])

    payload = pipe.finalize("graham", STRUCTURAL_PASS, [], [])

    assert payload["telemetry"]["score"] == pipe.last_judge_report["score"]
    assert payload["telemetry"]["persona"] == "graham"
