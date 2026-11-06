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
