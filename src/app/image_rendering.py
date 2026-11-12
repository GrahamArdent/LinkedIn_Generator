"""One bounded image intent in the existing store; never automatically re-submit."""
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
import base64
import fcntl
import hashlib
import io
import re
from pathlib import Path
from urllib.parse import urlsplit

from .contracts import SingleImageBrief
from .operational_store import atomic, sha


FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LAYOUT = "single-image-header-v1"
MODEL_VERSION = "bf53bdb93d739c9c915091cfa5f49ca662d11273a5eb30e7a2ec1939bcf27a00"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def money(value):
    try:
        result = Decimal(str(value))
        if not result.is_finite() or result < 0:
            raise ValueError()
        return result
    except (InvalidOperation, ValueError):
        raise ValueError("IMAGE_INVALID_COST") from None


def delivery_url(url):
    try:
        part = urlsplit(url)
        host = part.hostname or ""
        return (part.scheme == "https" and part.port in (None, 443)
                and not part.username and not part.password
                and (host == "replicate.delivery" or host.endswith(".replicate.delivery")))
    except (ValueError, TypeError):
        return False


def prepare(app, job, model, *, font_path=FONT, brief=None):
    selected = app.selected(job)
    if digest(selected["body"].encode()) != selected["content_sha256"]:
        raise ValueError("IMAGE_STALE_CANDIDATE")
    visual = selected.get("visual_asset") or {}
    if (visual.get("status") != "planned" or visual.get("asset_type") != "single_image"
            or visual.get("source_content_sha256") != selected["content_sha256"]
            or visual.get("aspect_ratio") != "4:5"):
        raise ValueError("IMAGE_VALID_PLAN_REQUIRED")
    # An explicit replacement brief is unapproved and gets a new exact intent.
    item = SingleImageBrief.model_validate(brief or visual["single_image"]).model_dump()
    if model.get("provider") != "replicate" or model.get("model") != "black-forest-labs/flux-schnell":
        raise ValueError("IMAGE_UNQUALIFIED_MODEL")
    if not re.fullmatch("[0-9a-f]{64}", model.get("version", "")):
        raise ValueError("IMAGE_PINNED_VERSION_REQUIRED")
    if model["version"] != MODEL_VERSION:
        raise ValueError("IMAGE_UNQUALIFIED_VERSION")
    money(model.get("estimated_cost_usd"))
    if not isinstance(model.get("price_checked_at"), str) or not model["price_checked_at"]:
        raise ValueError("IMAGE_PRICE_REFERENCE_REQUIRED")
    font = Path(font_path).resolve()
    value = {"schema_version": 1, "job": job, "candidate_sha256": selected["content_sha256"],
             "brief": item, "model": dict(model), "layout": LAYOUT, "dimensions": [1080, 1350],
             "font_path": str(font), "font_sha256": digest(font.read_bytes())}
    text_layout(value)  # Reject typography/font failures before approval or paid admission.
    value["intent_sha256"] = sha(value)
    return value


def validate_intent(app, job, value):
    raw = {k: v for k, v in value.items() if k != "intent_sha256"}
    if sha(raw) != value.get("intent_sha256") or value.get("job") != job:
        raise ValueError("IMAGE_INTENT_MISMATCH")
    if app.selected(job)["content_sha256"] != value["candidate_sha256"]:
        raise ValueError("IMAGE_STALE_CANDIDATE")
    expected = prepare(app, job, value["model"], font_path=value["font_path"], brief=value["brief"])
    if expected != value:
        raise ValueError("IMAGE_INTENT_MISMATCH")


def validate_approval(value, approval):
    if not approval or approval.get("text_and_brief_approved") is not True:
        raise ValueError("IMAGE_APPROVAL_REQUIRED")
    if approval.get("intent_sha256") != value["intent_sha256"]:
        raise ValueError("IMAGE_STALE_APPROVAL")
    if not approval.get("approved_by") or not approval.get("approval_ref"):
        raise ValueError("IMAGE_APPROVAL_REFERENCE_REQUIRED")
    if approval.get("paid_render_approved") is not True:
        raise ValueError("IMAGE_SPEND_APPROVAL_REQUIRED")
    if type(approval.get("max_requests")) is not int or approval["max_requests"] != 1:
        raise ValueError("IMAGE_SINGLE_REQUEST_REQUIRED")
    if money(value["model"]["estimated_cost_usd"]) > money(approval.get("max_cost_usd")):
        raise ValueError("IMAGE_COST_CAP_EXCEEDED")


@contextmanager
def locked(store, job):
    path = store.directory(job) / "image-render.lock"
    with path.open("a+b") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def text_layout(value):
    from PIL import ImageFont
    raw = Path(value["font_path"]).read_bytes()
    if digest(raw) != value["font_sha256"]:
        raise ValueError("IMAGE_FONT_CHANGED")
    for size in range(62, 25, -2):
        # Load verified in-memory bytes, never reopen mutable font data after validation.
        font = ImageFont.truetype(io.BytesIO(raw), size)
        lines = []
        line = ""
        for word in value["brief"]["overlay_text"].split():
            candidate = (line + " " + word).strip()
            if font.getlength(candidate) <= 952:
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        if (len(lines) <= 3 and all(font.getlength(x) <= 952 for x in lines)
                and len(lines) * (size + 16) <= 230):
            return font, lines, size
    raise ValueError("IMAGE_OVERLAY_DOES_NOT_FIT")


def compose(raw, value):
    from PIL import Image, ImageDraw, ImageOps
    font, lines, size = text_layout(value)
    try:
        if len(raw) > 20_000_000:
            raise ValueError()
        with Image.open(io.BytesIO(raw)) as source:
            if source.format not in ("PNG", "JPEG", "WEBP") or source.width * source.height > 20_000_000:
                raise ValueError()
            source.load()
            canvas = Image.new("RGB", (1080, 1350), "#14222b")
            canvas.paste(ImageOps.fit(source.convert("RGB"), (1080, 1050)), (0, 300))
    except Exception:
        raise ValueError("IMAGE_UNSUPPORTED_ASSET") from None
    draw = ImageDraw.Draw(canvas)
    y = (300 - len(lines) * (size + 16)) // 2
    for line in lines:
        draw.text((64, y), line, font=font, fill="white", anchor="lt")
        y += size + 16
    output = io.BytesIO()
    canvas.save(output, format="PNG")
    return output.getvalue()


def image_records(app, job):
    return [e["payload"] for e in app.store.events(job) if e["kind"] == "image_completed"]


def image_bytes(app, job, intent_sha256):
    rows = [r for r in image_records(app, job) if r["intent_sha256"] == intent_sha256]
    if not rows:
        raise ValueError("IMAGE_NOT_FOUND")
    result = rows[-1]
    # Ignore persisted paths: derive the only permitted local asset location.
    path = app.store.directory(job) / ("image-" + intent_sha256 + ".png")
    try:
        raw = path.read_bytes()
        if digest(raw) != result["asset_sha256"]:
            raise ValueError()
        return raw
    except (OSError, ValueError):
        raise ValueError("IMAGE_ASSET_CORRUPT") from None


def render(app, job, value, approval, *, provider=None):
    key = value["intent_sha256"]
    stage = "image:" + key
    with locked(app.store, job):
        validate_intent(app, job, value)
        completed = app.store.stage(job, stage)
        if completed:
            image_bytes(app, job, key)
            return completed
        validate_approval(value, approval)
        # All preflight checks before reservation; reservation is irreversible admission.
        if provider is None:
            from .replicate_images import ReplicateImages
            provider = ReplicateImages()
        records = [e["payload"] for e in app.store.events(job)
                   if e["kind"] == "image_request" and e["payload"]["intent_sha256"] == key]
        try:
            app.store.reserve(job, stage, value)
            fresh = True
        except ValueError as exc:
            if str(exc) != "RECONCILIATION_REQUIRED":
                raise
            fresh = False
        if fresh:
            app.store.event(job, "image_admission", {"intent_sha256": key, "approval": approval,
                                                   "intent": value})
            try:
                response = provider.submit(value)
                request_id = response.get("id")
                if not isinstance(request_id, str) or not re.fullmatch("[a-zA-Z0-9_-]{1,100}", request_id):
                    raise ValueError()
                app.store.event(job, "image_request", {"intent_sha256": key, "id": request_id})
            except Exception:
                raise ValueError("IMAGE_SUBMISSION_UNKNOWN") from None
        elif not records:
            raise ValueError("IMAGE_RECONCILIATION_REQUIRED")
        else:
            request_id = records[-1]["id"]
        # Save terminal provider response before asset download so URL expiry is explicit.
        result_stage = stage + ":provider"
        response = app.store.stage(job, result_stage)
        if response is None:
            try:
                response = provider.get(request_id)
            except Exception:
                raise ValueError("IMAGE_PROVIDER_READ_PENDING") from None
            if response.get("id") != request_id:
                raise ValueError("IMAGE_PROVIDER_ID_MISMATCH")
            status = response.get("status")
            if status not in ("succeeded", "failed", "canceled"):
                return {"state": "pending", "intent_sha256": key, "provider_request_id": request_id}
            safe = {"id": request_id, "status": status, "output": response.get("output"),
                    "metrics": response.get("metrics", {})}
            try:
                app.store.reserve(job, result_stage, {"request_id": request_id})
            except ValueError as exc:
                if str(exc) != "RECONCILIATION_REQUIRED":
                    raise
                # A reserved receipt is a read-only original-ID lookup, not another submission.
            app.store.commit_stage(job, result_stage, safe)
            response = safe
        if response["status"] != "succeeded":
            raise ValueError("IMAGE_PROVIDER_" + response["status"].upper())
        outputs = response.get("output")
        if not isinstance(outputs, list) or len(outputs) != 1 or not delivery_url(outputs[0]):
            raise ValueError("IMAGE_UNSAFE_OUTPUT")
        source_stage = stage + ":source"
        source = app.store.stage(job, source_stage)
        if source is None:
            try:
                raw = provider.download(outputs[0])
            except Exception:
                raise ValueError("IMAGE_DOWNLOAD_PENDING") from None
            compose(raw, value)
            source = {"sha256": digest(raw), "base64": base64.b64encode(raw).decode()}
            try:
                app.store.reserve(job, source_stage, {"request_id": request_id})
            except ValueError as exc:
                if str(exc) != "RECONCILIATION_REQUIRED":
                    raise
            app.store.commit_stage(job, source_stage, source)
        raw = base64.b64decode(source["base64"], validate=True)
        if digest(raw) != source["sha256"]:
            raise ValueError("IMAGE_ASSET_CORRUPT")
        asset = compose(raw, value)
        filename = "image-" + key + ".png"
        atomic(app.store.directory(job) / filename, asset)
        result = {"state": "completed", "intent_sha256": key, "candidate_sha256": value["candidate_sha256"],
                  "provider_request_id": request_id, "model": value["model"], "asset_file": filename,
                  "asset_sha256": digest(asset), "source_sha256": digest(raw), "dimensions": [1080, 1350],
                  "mime_type": "image/png", "alt_text": value["brief"]["alt_text"],
                  "usage": response.get("metrics", {}), "cost": {"actual_usd": None,
                      "estimated_usd": value["model"]["estimated_cost_usd"], "acceptance": "unverified"},
                  "human_visual_accepted": False, "publication_approved": False}
        # Event first: an interruption here can safely recreate the same deterministic result.
        if result not in image_records(app, job):
            app.store.event(job, "image_completed", result)
        app.store.commit_stage(job, stage, result)
        return result
