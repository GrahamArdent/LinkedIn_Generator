# LinkedIn_Generator

LinkedIn content-generation engine under active rebuild.

The target product is **not a Streamlit application**. The repository still contains historical Streamlit prototype files under `ui/` and legacy UI dependency/run artifacts; treat those as migration evidence until they are explicitly retired or a specific behavior is salvaged.

## Product role

LinkedIn Generator owns LinkedIn-specific content intelligence, including the evolving generation pipeline, persona/voice behavior, evidence/citation handling, hooks/structure, CTA and hashtag policy, validation, publish-quality review, and content outputs.

The intended post package also includes LinkedIn-specific **visual companion intelligence**: deciding whether a publish-ready post is better served by a single image or carousel, producing a structured visual brief/carousel plan, and later supplying renderer-facing asset specifications. Rendering providers are implementation adapters; they do not own the content strategy.

The rebuilt engine is intended to be usable independently for development/testing **and** callable by the Dedication ecosystem.

### Dedication boundary

Dedication owns generic orchestration concerns such as:

- Action selection and prioritization;
- scheduling and Day orchestration;
- canonical user/day/post state;
- shared permissions and external integration policy;
- human approval workflow;
- publish timing/trigger;
- notifications/interventions.

LinkedIn Generator must not create competing versions of those mechanisms. It should accept a bounded LinkedIn content request and return a structured LinkedIn post package for review. A high content score or generated visual plan is never permission to publish by itself.

## Current repository evidence

The existing implementation under `src/app/` contains useful but prototype-era behavior for:

- persona-aware generation;
- planning/drafting/judging passes;
- research/citations;
- topic selection and legacy scheduling;
- CTA/hashtag/house-rule configuration;
- text and carousel rendering;
- output logging and validation.

These assets are being assessed individually. Existing code is neither discarded merely because it is old nor preserved merely because it exists. Legacy scheduling does not override the current Dedication orchestration boundary.

## PROGRAMSTART / PROGRAMBUILD

PROGRAMSTART is adopted in **Mode C** as methodology only. LinkedIn Generator remains the owner of its product implementation and project-specific authority.

`CURRENT_WORK_PACKET.md` is the current bounded execution packet. Do not create a competing Master Game Plan merely to continue an in-flight slice.

## Current Graham workflow

The supported standalone entry is the installed `linkedin-codex create/status/show/resume/feedback/export/serve` application, using a canonical local store and the ChatGPT subscription. See [the current quick-start](docs/implementation/v4/LINKEDIN_CODEX_QUICKSTART.md) and [operational evidence](evidence/operational-implementation-20261106/REPORT.md). Four essential checks admit text for human review; scores do not approve publishing.

The generic direct API and old prototype adapters remain legacy/development surfaces. Their API-key behavior is not the current Graham workflow. Do not restore legacy scheduling or treat old UI/provider instructions as standalone qualification.

## Tests

```bash
pytest -q
```


### Single-image rendering (separately gated)

The standalone CLI can prepare an exact image intent, render one approved request,
and export its durable PNG. This adds no publication or scheduling command.
Use a pinned Replicate FLUX Schnell version, one output, the provider safety
checker enabled, and a currently checked USD estimate in a local model JSON:

```json
{"provider":"replicate","model":"black-forest-labs/flux-schnell","version":"bf53bdb93d739c9c915091cfa5f49ca662d11273a5eb30e7a2ec1939bcf27a00","estimated_cost_usd":"0.003","price_checked_at":"<current check reference/date>"}
```

```sh
linkedin-codex image-prepare --id JOB --model-config model.json --path intent.json
linkedin-codex image-render --id JOB --intent intent.json --approval approval.json
linkedin-codex image-export --id JOB --hash INTENT_SHA256 --path finished.png
```

Preparation is a no-provider read. Optional `--brief brief.json` binds an explicit
replacement single-image brief; it does not approve that brief. The approval
document must record an actual operator decision, with `intent_sha256`,
`approved_by`, `approval_ref`, `text_and_brief_approved: true`,
`paid_render_approved: true`, `max_requests: 1` and `max_cost_usd`.
Do not manufacture that decision from a sample or general execution permission.
Default API0 remains in force without an explicit paid exception. Refresh price,
model/version, rights and account readiness before any actual paid request.
Provide `REPLICATE_API_TOKEN` through the authorized secret owner/runtime;
never put credentials in model, approval or intent files.

The image uses a deterministic upper text band above generated imagery, with a
pinned local DejaVu Sans Bold font hash. Pillow is included in the operational
lock. The final graphic is1080x1350PNG with alt text and asset/source checksums.
The store retains the original request ID and downloaded bytes outside releases.
Repeat the same command to read an existing result or poll that original ID.
An already admitted request recovers under its original saved intent/approval even
if the post has since been edited; its asset remains bound to the historical
candidate hash and never becomes approval of the newer selected post.
No automatic provider submission retry occurs. An uncertain submission without
a durable ID stays held for owner reconciliation; do not create a new intent to
bypass it. Provider failure, cancellation, unsafe output or expired download is
not permission to retry a paid request.

The exported manifest includes saved image receipts. Completion here means saved
machine output, not human visual acceptance. Provider time metrics and a price
estimate do not establish the actual charge: billing remains explicitly unverified
until reconciled with provider billing evidence. A local preflight cap cannot
enforce a provider-side billing ceiling. Carousel rendering, human acceptance and
Dedication publication remain separate. The single current rendering evidence
and continuation are in `LinkedIn_Image_Rendering_Evidence.md` in the LinkedIn
posts document packet; repository receipts and assets are raw proof only.


#### Permanent credential custody on the Execution Node

The operator selected EN-local custody for Replicate. The administrative helper
`scripts/replicate_credential.py` uses real user-scoped systemd credential
encryption with the host key. It is installed as `linkedin-replicate`.
In an interactive EN terminal run `linkedin-replicate set` and enter the token
at the hidden prompt. Never place the token in a command argument or chat.
Existing stored credentials are not overwritten.

Encrypted credential: `~/.local/share/graham-linkedin-credentials/replicate.cred`
(directory0700, file0600). `linkedin-replicate status` checks decryption without
showing the token. `linkedin-replicate render --id JOB --intent intent.json
--approval approval.json` loads it only into the existing renderer subprocess.
The normal app's exact approval, spending and original-result recovery gates
still apply; persistent custody does not authorize extra paid calls.

This ciphertext depends on this host's systemd credential key and user identity.
On loss/rebuild, replace the provider token through Replicate rather than
assuming ciphertext alone is a portable backup. No Infisical identity, secret
sync, custom encryption algorithm or background service is added.
