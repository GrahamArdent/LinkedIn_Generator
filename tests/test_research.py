from __future__ import annotations

from src.app.research import pick_quote, pick_stat


def test_missing_research_files_return_no_evidence(tmp_path):
    assert pick_quote(tmp_path) == {}
    assert pick_stat(tmp_path) == {}


def test_requested_quote_does_not_fall_back_to_unrelated_row(tmp_path):
    (tmp_path / "quotes.csv").write_text(
        "topic,quote,author,source\n"
        "identity,Identity quote,A,Source A\n"
        "ai,AI quote,B,Source B\n",
        encoding="utf-8",
    )

    assert pick_quote(tmp_path, topic="identity")["quote"] == "Identity quote"
    assert pick_quote(tmp_path, topic="missing") == {}


def test_requested_stat_does_not_fall_back_to_unrelated_row(tmp_path):
    (tmp_path / "stats.csv").write_text(
        "metric,value,unit,source,date\n"
        "breach_cost,4.8,million,Source A,2026\n"
        "adoption,42,percent,Source B,2026\n",
        encoding="utf-8",
    )

    assert pick_stat(tmp_path, metric="breach_cost")["value"] == "4.8"
    assert pick_stat(tmp_path, metric="missing") == {}
