from __future__ import annotations

from pathlib import Path

import pytest

from src.app.prompt_builder import build_prompt_blocks


REPO_CONFIG = Path(__file__).resolve().parents[1] / "config"


def test_checked_in_content_policy_is_runtime_consistent():
    blocks = build_prompt_blocks(REPO_CONFIG)

    graham = blocks["personas"]["graham"]
    ardent = blocks["personas"]["ardent_v2"]

    assert graham["cta_patterns"]
    assert ardent["cta_patterns"]
    assert graham["hashtag_set"] == "graham_default"
    assert ardent["hashtag_set"] == "ardent_default"
    assert blocks["hashtags"]["graham_default"]
    assert "#ArdentSecurity" not in blocks["hashtags"]["graham_default"]
    assert "#ArdentSecurity" in blocks["hashtags"]["ardent_default"]
    assert len(blocks["hashtags"]["graham_default"]) <= 5
    assert len(blocks["hashtags"]["ardent_default"]) <= 5


def test_loader_derives_legacy_runtime_fields_without_duplicating_config(tmp_path):
    (tmp_path / "personas.yaml").write_text(
        "personas:\n  graham:\n    tone: [direct]\n",
        encoding="utf-8",
    )
    (tmp_path / "cta_policies.yaml").write_text(
        "safe_ctas:\n  graham:\n    - Ask a useful question.\n",
        encoding="utf-8",
    )
    (tmp_path / "hashtag_policy.yaml").write_text(
        "max_per_post: 2\n"
        "core: [\"#Core\"]\n"
        "brand: [\"#Brand\"]\n"
        "trending_priority: [\"#Useful\", \"#Extra\"]\n"
        "banlist: []\n",
        encoding="utf-8",
    )

    blocks = build_prompt_blocks(tmp_path)

    assert blocks["personas"]["graham"]["cta_patterns"] == ["Ask a useful question."]
    assert blocks["personas"]["graham"]["hashtag_set"] == "graham_default"
    assert blocks["hashtags"]["graham_default"] == ["#Core", "#Useful"]


def test_loader_fails_clearly_when_persona_has_no_cta_policy(tmp_path):
    (tmp_path / "personas.yaml").write_text(
        "personas:\n  unknown:\n    tone: [direct]\n",
        encoding="utf-8",
    )
    (tmp_path / "cta_policies.yaml").write_text("safe_ctas: {}\n", encoding="utf-8")
    (tmp_path / "hashtag_policy.yaml").write_text("core: []\n", encoding="utf-8")

    with pytest.raises(KeyError, match="has no CTA policy"):
        build_prompt_blocks(tmp_path)
