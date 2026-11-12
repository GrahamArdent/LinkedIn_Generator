"""Protect real asset persistence, exact approvals and no duplicate paid dispatch."""
import hashlib
import io

import pytest
from PIL import Image

from src.app.operational import Application
from src.app.operational_store import Store


def setup(tmp_path):
    store = Store.initialize(tmp_path / "store")
    store.admit("post", {}, {})
    body = "Count the work through delivery."
    selected = {"body": body, "content_sha256": hashlib.sha256(body.encode()).hexdigest()}
    store.finish("post", "completed", {"selected_candidate": selected, "visual_asset": {
        "status": "planned", "asset_type": "single_image", "aspect_ratio": "4:5",
        "source_content_sha256": selected["content_sha256"],
        "single_image": {"concept": "A parcel containing a wooden puzzle",
            "overlay_text": body, "composition": "Parcel at centre", "style": "Editorial",
            "generation_prompt": "An opened parcel and a wooden puzzle. No text or logos.",
            "negative_guidance": [], "alt_text": "An opened parcel holding puzzle pieces."}}})
    return Application(store, None)


MODEL = {"provider": "replicate", "model": "black-forest-labs/flux-schnell",
         "version": "b" * 64, "estimated_cost_usd": "0.003", "price_checked_at": "2026-11-12"}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def intent(app):
    return app.prepare_image("post", MODEL, font_path=FONT)


def approval(value):
    return {"intent_sha256": value["intent_sha256"], "approved_by": "test-operator",
        "approval_ref": "synthetic fixture, no external authority", "text_and_brief_approved": True,
        "paid_render_approved": True, "max_requests": 1, "max_cost_usd": "0.01"}


class Provider:
    def __init__(self):
        self.submissions = 0
        self.reads = 0

    def submit(self, value):
        self.submissions += 1
        return {"id": "prediction1", "status": "starting"}

    def get(self, prediction_id):
        assert prediction_id == "prediction1"
        self.reads += 1
        return {"id": prediction_id, "status": "succeeded",
                "output": ["https://replicate.delivery/fixture.png"], "metrics": {"predict_time": 1}}

    def download(self, url):
        raw = io.BytesIO()
        Image.new("RGB", (800, 1000), "#cab99f").save(raw, format="PNG")
        return raw.getvalue()


def test_asset_survives_reopen_and_export_without_provider(tmp_path):
    app = setup(tmp_path)
    value = intent(app)
    provider = Provider()
    result = app.render_image("post", value, approval(value), provider=provider)
    assert result["state"] == "completed"
    assert result["dimensions"] == [1080, 1350]
    assert result["cost"]["actual_usd"] is None
    assert result["cost"]["acceptance"] == "unverified"
    assert result["alt_text"] == "An opened parcel holding puzzle pieces."
    raw = app.image_bytes("post", value["intent_sha256"])
    assert hashlib.sha256(raw).hexdigest() == result["asset_sha256"]
    assert Image.open(io.BytesIO(raw)).size == (1080, 1350)
    reopened = Application(Store(app.store.root), None)
    assert reopened.render_image("post", value, None, provider=None) == result
    assert provider.submissions == 1
    assert reopened.export("post")["manifest"]["rendered_images"][0]["asset_sha256"] == result["asset_sha256"]


@pytest.mark.parametrize("change,code", [
    ({"text_and_brief_approved": False}, "IMAGE_APPROVAL_REQUIRED"),
    ({"paid_render_approved": False}, "IMAGE_SPEND_APPROVAL_REQUIRED"),
    ({"intent_sha256": "0"*64}, "IMAGE_STALE_APPROVAL"),
    ({"max_cost_usd": "0.001"}, "IMAGE_COST_CAP_EXCEEDED"),
    ({"max_requests": 2}, "IMAGE_SINGLE_REQUEST_REQUIRED"),
])
def test_gates_prevent_dispatch(tmp_path, change, code):
    app = setup(tmp_path); value = intent(app); grant = {**approval(value), **change}
    provider = Provider()
    with pytest.raises(ValueError, match=code):
        app.render_image("post", value, grant, provider=provider)
    assert provider.submissions == 0


def test_changed_post_and_tampered_intent_are_rejected(tmp_path):
    app = setup(tmp_path); value = intent(app); provider = Provider()
    tampered = {**value, "brief": {**value["brief"], "overlay_text": "Changed"}}
    with pytest.raises(ValueError, match="IMAGE_INTENT_MISMATCH"):
        app.render_image("post", tampered, approval(value), provider=provider)
    app.edit("post", "A changed post.")
    with pytest.raises(ValueError, match="IMAGE_STALE_CANDIDATE"):
        app.render_image("post", value, approval(value), provider=provider)
    assert provider.submissions == 0


def test_uncertain_submission_without_id_stays_held(tmp_path):
    app = setup(tmp_path); value = intent(app)
    class Lost(Provider):
        def submit(self, value):
            self.submissions += 1
            raise TimeoutError("private upstream detail")
    provider = Lost()
    with pytest.raises(ValueError, match="IMAGE_SUBMISSION_UNKNOWN"):
        app.render_image("post", value, approval(value), provider=provider)
    with pytest.raises(ValueError, match="IMAGE_RECONCILIATION_REQUIRED"):
        app.render_image("post", value, approval(value), provider=provider)
    assert provider.submissions == 1


def test_resume_original_id_after_interruption_does_not_resubmit(tmp_path):
    app = setup(tmp_path); value = intent(app)
    class Interrupted(Provider):
        def get(self, prediction_id):
            raise KeyboardInterrupt()
    provider = Interrupted()
    with pytest.raises(KeyboardInterrupt):
        app.render_image("post", value, approval(value), provider=provider)
    provider = Provider()
    result = Application(Store(app.store.root), None).render_image("post", value, approval(value), provider=provider)
    assert result["provider_request_id"] == "prediction1"
    assert provider.submissions == 0
    assert provider.reads == 1


@pytest.mark.parametrize("kind", ["failed", "canceled", "bad_output", "invalid_image"])
def test_failure_or_unsupported_output_never_resubmits(tmp_path, kind):
    app = setup(tmp_path); value = intent(app)
    class Bad(Provider):
        def get(self, prediction_id):
            if kind in ("failed", "canceled"):
                return {"id": prediction_id, "status": kind, "error": "upstream"}
            result = super().get(prediction_id)
            if kind == "bad_output": result["output"] = ["http://127.0.0.1/secret"]
            return result
        def download(self, url):
            return b"not an image" if kind == "invalid_image" else super().download(url)
    provider = Bad()
    for _ in range(2):
        with pytest.raises(ValueError):
            app.render_image("post", value, approval(value), provider=provider)
    assert provider.submissions == 1


def test_download_interruption_recovers_original_result(tmp_path):
    app = setup(tmp_path); value = intent(app)
    class Interrupted(Provider):
        def download(self, url):
            raise TimeoutError()
    with pytest.raises(ValueError, match="IMAGE_DOWNLOAD_PENDING"):
        app.render_image("post", value, approval(value), provider=Interrupted())
    provider = Provider()
    assert app.render_image("post", value, approval(value), provider=provider)["state"] == "completed"
    assert provider.submissions == 0


def test_corrupt_saved_asset_is_not_returned_as_success(tmp_path):
    app = setup(tmp_path); value = intent(app)
    result = app.render_image("post", value, approval(value), provider=Provider())
    (app.store.directory("post") / result["asset_file"]).write_bytes(b"corrupt")
    with pytest.raises(ValueError, match="IMAGE_ASSET_CORRUPT"):
        app.image_bytes("post", value["intent_sha256"])


def test_two_processes_share_one_provider_dispatch(tmp_path):
    import multiprocessing
    app = setup(tmp_path); value = intent(app)
    ctx = multiprocessing.get_context("fork")
    calls = ctx.Value("i", 0)
    queue = ctx.Queue()
    class Shared(Provider):
        def submit(self, value):
            with calls.get_lock(): calls.value += 1
            return super().submit(value)
    def worker():
        try:
            result = Application(Store(app.store.root), None).render_image(
                "post", value, approval(value), provider=Shared())
            queue.put(result["asset_sha256"])
        except BaseException as exc:
            queue.put(str(exc))
    processes = [ctx.Process(target=worker) for _ in range(2)]
    for process in processes: process.start()
    for process in processes:
        process.join(15)
        assert process.exitcode == 0
    assert queue.get(timeout=2) == queue.get(timeout=2)
    assert calls.value == 1


def test_provider_receipt_commit_interruption_is_read_only_recoverable(tmp_path, monkeypatch):
    app = setup(tmp_path); value = intent(app); provider = Provider()
    original = app.store.commit_stage
    def interrupted(job, name, result):
        if name.endswith(":provider"): raise KeyboardInterrupt()
        return original(job, name, result)
    monkeypatch.setattr(app.store, "commit_stage", interrupted)
    with pytest.raises(KeyboardInterrupt):
        app.render_image("post", value, approval(value), provider=provider)
    recovered = Application(Store(app.store.root), None)
    assert recovered.render_image("post", value, approval(value), provider=provider)["state"] == "completed"
    assert provider.submissions == 1


def test_normal_cli_prepares_gates_and_exports_saved_asset(tmp_path):
    import json
    import os
    from pathlib import Path
    import subprocess
    import sys
    app = setup(tmp_path); value = intent(app)
    script = Path(__file__).resolve().parents[1] / "scripts/linkedin_app.py"
    model_file = tmp_path / "model.json"; model_file.write_text(json.dumps(MODEL))
    intent_file = tmp_path / "intent.json"
    env = {k: v for k, v in os.environ.items() if k not in ("LINKEDIN_CONFIG", "REPLICATE_API_TOKEN")}
    def cli(*args):
        return subprocess.run([sys.executable, str(script), "--data-root", str(app.store.root), *args],
                              env=env, capture_output=True, text=True)
    prepared = cli("image-prepare", "--id", "post", "--model-config", str(model_file),
                   "--path", str(intent_file))
    assert prepared.returncode == 0, prepared.stderr
    assert json.loads(prepared.stdout) == value
    held = cli("image-render", "--id", "post", "--intent", str(intent_file))
    assert held.returncode == 2
    assert json.loads(held.stderr)["error_code"] == "IMAGE_APPROVAL_REQUIRED"
    app.render_image("post", value, approval(value), provider=Provider())
    reopened = cli("image-render", "--id", "post", "--intent", str(intent_file))
    assert reopened.returncode == 0, reopened.stderr
    exported = tmp_path / "export.png"
    result = cli("image-export", "--id", "post", "--hash", value["intent_sha256"], "--path", str(exported))
    assert result.returncode == 0, result.stderr
    assert exported.read_bytes() == app.image_bytes("post", value["intent_sha256"])


def test_layout_honours_upper_text_space_in_saved_brief(tmp_path):
    app = setup(tmp_path); value = intent(app)
    app.render_image("post", value, approval(value), provider=Provider())
    image = Image.open(io.BytesIO(app.image_bytes("post", value["intent_sha256"])))
    assert image.getpixel((10, 10)) == (20, 34, 43)
    assert image.getpixel((10, 1340)) == (202, 185, 159)
