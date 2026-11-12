"""Transport contracts: pinned input, bounded asset host, no credential forwarding."""
import json
import pytest
from src.app.replicate_images import ReplicateImages


class Response:
    def __init__(self, raw): self.raw = raw
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, size): return self.raw[:size]


def test_pinned_request_keeps_safety_enabled_and_no_text(monkeypatch):
    monkeypatch.setenv("REPLICATE_API_TOKEN", "synthetic-test-only")
    provider = ReplicateImages()
    requests = []
    class Transport:
        def open(self, request, timeout):
            requests.append(request)
            return Response(b'{"id":"fixture","status":"starting"}')
    provider.opener = Transport()
    result = provider.submit({"model": {"version": "a"*64},
        "brief": {"generation_prompt": "A parcel."}})
    assert result["id"] == "fixture"
    request = requests[0]
    assert request.full_url == "https://api.replicate.com/v1/predictions"
    body = json.loads(request.data)
    assert body["version"] == "a"*64
    assert body["input"]["num_outputs"] == 1
    assert body["input"]["disable_safety_checker"] is False
    assert body["input"]["aspect_ratio"] == "4:5"
    assert "No text" in body["input"]["prompt"]


def test_download_does_not_forward_api_credential(monkeypatch):
    monkeypatch.setenv("REPLICATE_API_TOKEN", "synthetic-test-only")
    provider = ReplicateImages()
    class Transport:
        def open(self, request, timeout):
            assert not request.has_header("Authorization")
            return Response(b"image")
    provider.opener = Transport()
    assert provider.download("https://replicate.delivery/fixture.png") == b"image"
    for url in ["http://replicate.delivery/a", "https://evil.example/a",
                "https://replicate.delivery.evil.example/a", "https://replicate.delivery:444/a",
                "https://user:password@replicate.delivery/a", "file:///etc/passwd"]:
        with pytest.raises(ValueError, match="IMAGE_UNSAFE_OUTPUT"):
            provider.download(url)


def test_missing_credential_fails_before_any_request(monkeypatch):
    monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
    with pytest.raises(ValueError, match="IMAGE_CREDENTIAL_REQUIRED"):
        ReplicateImages()


def test_structured_visual_constraints_reach_provider_prompt(monkeypatch):
    monkeypatch.setenv("REPLICATE_API_TOKEN", "synthetic-test-only")
    provider = ReplicateImages()
    class Transport:
        def open(self, request, timeout):
            prompt = json.loads(request.data)["input"]["prompt"]
            for part in ("Open parcel", "Clear space above", "Natural light", "No robots"):
                assert part in prompt
            return Response(b'{"id":"fixture","status":"starting"}')
    provider.opener = Transport()
    provider.submit({"model":{"version":"a"*64}, "brief":{
        "generation_prompt":"A parcel.", "concept":"Open parcel",
        "composition":"Clear space above", "style":"Natural light",
        "negative_guidance":["No robots"]}})


def test_api_and_asset_requests_identify_the_real_application(monkeypatch):
    monkeypatch.setenv("REPLICATE_API_TOKEN", "synthetic-test-only")
    provider = ReplicateImages()
    class Transport:
        def open(self, request, timeout):
            assert request.get_header("User-agent") == "LinkedInGenerator/1.0"
            return Response(b'{"id":"fixture","status":"processing"}' if request.has_header("Authorization") else b"image")
    provider.opener = Transport()
    assert provider.get("fixture")["id"] == "fixture"
    assert provider.download("https://replicate.delivery/fixture.png") == b"image"
