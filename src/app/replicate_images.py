"""Small pinned-version Replicate HTTP boundary; no retries or credential logging."""
import json
import os
from urllib.request import Request, build_opener, HTTPRedirectHandler

from .image_rendering import delivery_url


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ReplicateImages:
    def __init__(self):
        self.token = os.environ.get("REPLICATE_API_TOKEN", "").strip()
        if not self.token:
            raise ValueError("IMAGE_CREDENTIAL_REQUIRED")
        self.opener = build_opener(NoRedirect())

    def _api(self, path, data=None):
        raw = None if data is None else json.dumps(data).encode()
        request = Request("https://api.replicate.com/v1/" + path, data=raw,
            headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"})
        with self.opener.open(request, timeout=40) as response:
            raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("IMAGE_PROVIDER_RESPONSE_TOO_LARGE")
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError("IMAGE_INVALID_PROVIDER_RESPONSE")
        return value

    def submit(self, value):
        brief = value["brief"]
        return self._api("predictions", {"version": value["model"]["version"], "input": {
            "prompt": brief["generation_prompt"] + " No text, lettering, logos or watermarks.",
            "aspect_ratio": "4:5", "num_outputs": 1, "output_format": "png",
            "disable_safety_checker": False}})

    def get(self, prediction_id):
        import re
        if not re.fullmatch("[a-zA-Z0-9_-]{1,100}", prediction_id):
            raise ValueError("IMAGE_INVALID_PROVIDER_ID")
        return self._api("predictions/" + prediction_id)

    def download(self, url):
        if not delivery_url(url):
            raise ValueError("IMAGE_UNSAFE_OUTPUT")
        # Never forward the API token to an asset host or follow a redirect.
        with self.opener.open(Request(url), timeout=40) as response:
            raw = response.read(20_000_001)
        if len(raw) > 20_000_000:
            raise ValueError("IMAGE_UNSUPPORTED_ASSET")
        return raw
