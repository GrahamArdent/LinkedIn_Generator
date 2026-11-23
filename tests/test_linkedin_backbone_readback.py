import json
import sqlite3
from types import SimpleNamespace

import pytest

from scripts import linkedin_backbone_readback as receiver


def specimen():
    body = "Exact saved draft"
    review = {"original": {"essential_checks": {}}, "review_status": "reviewable"}
    body_digest = receiver.digest(body.encode())
    current = {"version": 22, "body": body, "content_sha256": body_digest,
               "review_status": "reviewable", "review": review}
    item = {"brief_revision": 1, "current_text": current}
    export = {"text": body, "manifest": {"revision": 22, "brief_revision": 1,
              "review_status": "reviewable", "selected_hash": body_digest}}
    binding = {"item": "fixture", "release_fingerprint": "a" * 64, "brief_revision": 1,
               "text_version": 22, "draft_sha256": body_digest, "export_sha256": body_digest,
               "review_sha256": receiver.digest(receiver.canonical(review))}
    request = {"schema": receiver.SCHEMA, "request_id": "req-linkedin-fixture", "binding": binding}
    request["input_sha256"] = receiver.digest(receiver.canonical(request))
    app = SimpleNamespace(store=SimpleNamespace(writing=lambda _: item), export=lambda _: export)
    return request, item, export, app


def test_exact_readback_replays_without_exporting_draft_or_review():
    request, _, _, app = specimen()
    first = receiver.readback(request, app, "a" * 64)
    assert receiver.readback(request, app, "a" * 64) == first
    assert first["request_id"] == request["request_id"]
    assert first["input_sha256"] == request["input_sha256"]
    assert "Exact saved draft" not in json.dumps(first)


@pytest.mark.parametrize("change, message", [
    ("release", "STALE_LINKEDIN_RELEASE"),
    ("request", "BACKBONE_INPUT_DIGEST_MISMATCH"),
    ("brief", "STALE_OR_UNREVIEWABLE_DRAFT"),
    ("text", "STALE_OR_UNREVIEWABLE_DRAFT"),
    ("review_status", "STALE_OR_UNREVIEWABLE_DRAFT"),
    ("body", "DRAFT_OR_REVIEW_DIGEST_MISMATCH"),
    ("review", "DRAFT_OR_REVIEW_DIGEST_MISMATCH"),
    ("export", "EXPORT_DIGEST_MISMATCH"),
])
def test_refuses_drift(change, message):
    request, item, export, app = specimen()
    release = "a" * 64
    if change == "release":
        release = "b" * 64
    elif change == "request":
        request["request_id"] = "req-other-fixture"
    elif change == "brief":
        item["brief_revision"] = 2
    elif change == "text":
        item["current_text"]["version"] = 23
    elif change == "review_status":
        item["current_text"]["review_status"] = "revalidation_required"
    elif change == "body":
        item["current_text"]["body"] += " altered"
    elif change == "review":
        item["current_text"]["review"]["original"] = {}
    elif change == "export":
        export["text"] += " altered"
    with pytest.raises(ValueError, match=message):
        receiver.readback(request, app, release)


def test_refuses_duplicate_request_keys():
    with pytest.raises(ValueError, match="DUPLICATE_REQUEST_KEY"):
        json.loads('{"schema":"x","schema":"x"}', object_pairs_hook=receiver.strict_object)


def test_receiver_store_connection_rejects_writes(tmp_path):
    root = tmp_path / "store with spaces"
    receiver.Store.initialize(root)
    store = receiver.ReadOnlyStore(root)
    with store.connection() as connection:
        assert connection.execute("SELECT count(*) FROM metadata").fetchone()[0] > 0
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            connection.execute("DELETE FROM metadata")
