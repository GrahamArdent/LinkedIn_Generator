#!/usr/bin/env python3
"""Verify a sealed, read-only request against the installed LinkedIn draft."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.app.operational import Application, release_fingerprint
from src.app.operational_store import Store

OWNER = "GrahamArdent/LinkedIn_Generator"
SCHEMA = "linkedin.backbone.draft-readback.v1"
MAX_REQUEST_BYTES = 4096
BINDING_KEYS = {
    "item", "release_fingerprint", "brief_revision", "text_version",
    "draft_sha256", "review_sha256", "export_sha256",
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"),
    ).encode()


def strict_object(items):
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError("DUPLICATE_REQUEST_KEY")
        out[key] = value
    return out


def verify_request(request, installed_fingerprint):
    if not isinstance(request, dict) or set(request) != {"schema", "request_id", "binding", "input_sha256"}:
        raise ValueError("INVALID_BACKBONE_REQUEST")
    if request["schema"] != SCHEMA or not isinstance(request["request_id"], str) or not re.fullmatch(
        r"req-[a-z0-9][a-z0-9-]{6,95}", request["request_id"],
    ):
        raise ValueError("INVALID_BACKBONE_REQUEST")
    binding = request["binding"]
    if not isinstance(binding, dict) or set(binding) != BINDING_KEYS:
        raise ValueError("INVALID_DRAFT_BINDING")
    if not isinstance(binding["item"], str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,99}", binding["item"]):
        raise ValueError("INVALID_DRAFT_BINDING")
    for key in ("brief_revision", "text_version"):
        if type(binding[key]) is not int or binding[key] <= 0:
            raise ValueError("INVALID_DRAFT_BINDING")
    for key in ("release_fingerprint", "draft_sha256", "review_sha256", "export_sha256"):
        if not isinstance(binding[key], str) or not re.fullmatch(r"[0-9a-f]{64}", binding[key]):
            raise ValueError("INVALID_DRAFT_BINDING")
    expected_input = digest(canonical({key: request[key] for key in ("schema", "request_id", "binding")}))
    if request["input_sha256"] != expected_input:
        raise ValueError("BACKBONE_INPUT_DIGEST_MISMATCH")
    if binding["release_fingerprint"] != installed_fingerprint:
        raise ValueError("STALE_LINKEDIN_RELEASE")
    return binding


def readback(request, app, installed_fingerprint):
    binding = verify_request(request, installed_fingerprint)
    item = app.store.writing(binding["item"])
    text = item["current_text"]
    if (not text or item["brief_revision"] != binding["brief_revision"]
            or text["version"] != binding["text_version"] or text["review_status"] != "reviewable"):
        raise ValueError("STALE_OR_UNREVIEWABLE_DRAFT")
    if (text["content_sha256"] != binding["draft_sha256"]
            or digest(text["body"].encode()) != binding["draft_sha256"]
            or digest(canonical(text["review"])) != binding["review_sha256"]):
        raise ValueError("DRAFT_OR_REVIEW_DIGEST_MISMATCH")
    exported = app.export(binding["item"])
    manifest = exported["manifest"]
    if (manifest["revision"] != binding["text_version"]
            or manifest["brief_revision"] != binding["brief_revision"]
            or manifest["review_status"] != "reviewable"
            or manifest["selected_hash"] != binding["draft_sha256"]
            or digest(exported["text"].encode()) != binding["export_sha256"]
            or exported["text"] != text["body"]):
        raise ValueError("EXPORT_DIGEST_MISMATCH")
    return {
        "schema": SCHEMA,
        "owner": OWNER,
        "status": "verified",
        "request_id": request["request_id"],
        "input_sha256": request["input_sha256"],
        "binding": binding,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(MAX_REQUEST_BYTES + 1)
        if len(raw) > MAX_REQUEST_BYTES:
            raise ValueError("BACKBONE_REQUEST_TOO_LARGE")
        request = json.loads(raw, object_pairs_hook=strict_object)
        fingerprint = release_fingerprint()
        verify_request(request, fingerprint)
        result = readback(request, Application(Store(args.data_root), None), fingerprint)
    except (ValueError, KeyError, TypeError, OSError):
        print(json.dumps({"status": "rejected"}), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
