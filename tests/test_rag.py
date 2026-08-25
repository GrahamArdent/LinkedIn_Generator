from __future__ import annotations

from src.app import rag


def test_retrieve_returns_only_approved_positive_relevance(monkeypatch):
    monkeypatch.setattr(rag, "load_whitelist", lambda _config: {"ibm.com"})
    monkeypatch.setattr(
        rag,
        "load_citations",
        lambda _data: [
            {
                "title": "IBM identity risk report",
                "one_liner": "Identity controls affect breach risk.",
                "url": "https://www.ibm.com/reports/identity",
            },
            {
                "title": "IBM unrelated storage report",
                "one_liner": "Storage hardware update.",
                "url": "https://www.ibm.com/reports/storage",
            },
            {
                "title": "Random identity blog",
                "one_liner": "Identity risk opinion.",
                "url": "https://random.example/identity",
            },
        ],
    )

    results = rag.retrieve("identity risk", "control reliability", k=3)

    assert [item["title"] for item in results] == ["IBM identity risk report"]


def test_retrieve_fails_closed_without_source_whitelist(monkeypatch):
    monkeypatch.setattr(rag, "load_whitelist", lambda _config: set())
    monkeypatch.setattr(
        rag,
        "load_citations",
        lambda _data: [
            {
                "title": "Relevant but ungoverned evidence",
                "one_liner": "identity risk",
                "url": "https://example.com/evidence",
            }
        ],
    )

    assert rag.retrieve("identity risk", "control reliability") == []
