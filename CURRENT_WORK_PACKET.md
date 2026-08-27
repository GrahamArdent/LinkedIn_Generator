# CURRENT_WORK_PACKET.md

PACKET_ID: LIG-CONTENT-VISUAL-ACCEPTANCE-2026-08-27
STATUS: active
PROJECT: LinkedIn_Generator
ENTRY_MODE: PROGRAMSTART Mode C
CURRENT_STAGE_OR_MILESTONE: Content + visual-package acceptance before rendering and publishing integration
AUTHORITY_SPINE: `README.md` product role + Dedication boundary, current explicit operator decisions, accepted project contracts/voice authority, and validated implementation state on `main`
AUTHORITY_VERSION_OR_COMMIT: LinkedIn_Generator `03736f197f858426a65a60c18ac9098c31376684`; PROGRAMSTART methodology `59a9bf4f2028b328d38fae64b8e08a7cf4ae685e`
BLOCKER_SCOPE: milestone
SAFE_EXECUTION_LANE: A/B — human content acceptance, provider-neutral visual planning, evidence gathering, review, and reversible repo corrections can proceed
BLOCKED_ACTION: Final repo-provider acceptance cannot be claimed until the real generation path is exercised in an environment with a valid `OPENAI_API_KEY`; rendering/publishing remain later slices

## PROGRAMSTART Routing Decision

This is an in-flight project. Do not create a new Master Game Plan or restart from Stage 0.

The current operator decision adds a real product requirement rather than invalidating the existing architecture:

- Graham does not intend to publish LinkedIn posts without a visual companion in normal use.
- The visual may be a single image or a carousel/document depending on what best serves the post.
- Previous direct image generation produced poor results and excessive regeneration, so rendering must not begin from an unconstrained image prompt.
- The next smallest responsible slice is therefore **Visual Asset Planning / Carousel Planning** before any rendering provider is integrated.
- Dedication remains the owner of scheduling, approval workflow, canonical post state, and publishing orchestration.
- LinkedIn Generator remains the owner of post intelligence, publish-quality assessment, visual-format recommendation, visual brief generation, carousel copy, and renderer-facing asset specifications.

This change is reversible and does not require reopening settled voice, evidence, opportunity, or publish-quality work.

## Durable Product Decisions

1. **90 remains the publish-ready text threshold.** A sub-90 Draft A is preserved and receives at most one automatic guarded Draft B for review.
2. **A publishable post package includes a visual companion plan by default.** Text-only publishing is not the target product path, though the contract may still support disabling visual planning for tests or exceptional use.
3. **Format is a content decision.** Use `single_image` for one strong visual idea; use `carousel` when sequence, comparison, steps, layers, or multiple distinct takeaways genuinely improve understanding.
4. **Visual planning precedes rendering.** Do not send a generic post directly to an image model and hope the provider invents a good design.
5. **Typography is separated from generative imagery.** Image prompts should request imagery without embedded text/logos/watermarks; overlay text and carousel slide copy remain structured fields for a later deterministic layout layer.
6. **Replicate is the expected first rendering provider, not a permanent architecture dependency.** Add it later behind a provider interface so rendering can be replaced without changing content intelligence.
7. **Human approval remains mandatory before publishing.** Neither a 90+ post score nor a visual plan is permission to publish.
8. **Dedication owns schedule/publish orchestration.** Do not rebuild the legacy scheduler as a second scheduling system inside LinkedIn Generator.

## Execution Sequence

### Slice A — Visual Asset Planning / Carousel Planner — ACTIVE

Objective: turn a publish-ready post candidate into one structured provider-neutral visual companion for review.

In scope:

- typed request/result contract for visual planning;
- `auto | single_image | carousel` preference;
- choose single image vs carousel based on the finished post;
- single-image brief: concept, overlay text, composition, style, provider-neutral generation prompt, negative guidance, alt text;
- carousel brief: cover headline, design system, 4–8 ordered slides, slide copy, visual direction, alt text;
- explicit anti-cliché visual policy;
- separate generated imagery from typography;
- do not plan an asset until a 90+ publish-quality candidate exists;
- fail closed when the planner returns malformed structure or adds unsupported numbers/URLs/quoted claims to visual copy;
- return the visual plan through the Dedication-facing content result.

Out of scope for Slice A:

- actual image generation;
- Replicate API calls;
- slide rendering or file creation;
- image quality scoring from rendered pixels;
- scheduling or LinkedIn publishing;
- autonomous commenting or feed crawling.

Acceptance for Slice A:

- [ ] both `single_image` and `carousel` plans have typed/validated structures;
- [ ] carousel contains 4–8 ordered slides and each slide advances the idea;
- [ ] single-image generated-imagery prompt explicitly avoids embedded typography;
- [ ] visual copy cannot introduce a new URL, numeric claim, or quoted claim absent from the approved text candidate;
- [ ] explicit format preference is honored or the plan is deferred;
- [ ] no visual-planning provider call is spent when the text candidate is below the 90 publish threshold;
- [ ] result preserves which candidate (`original` or `rewrite`) the visual plan belongs to;
- [ ] planning remains provider-neutral and creates no scheduling/publishing state.

### Slice B — Renderer + Replicate Adapter — NEXT IF A PASSES

Objective: convert the approved visual specification into reviewable asset files without coupling product logic to one provider.

Expected design:

- renderer interface owned by LinkedIn Generator;
- Replicate adapter as first implementation;
- single-image imagery generation from provider-neutral prompt;
- deterministic overlay typography after image generation;
- deterministic carousel slide layout/rendering from structured slide copy;
- one or a small bounded number of render candidates rather than open-ended regeneration;
- rendered-asset quality checks before human review;
- preserve prompt/model/version/provenance metadata.

Do not begin this slice until the planner output itself is judged useful enough that rendering is worth paying for.

### Slice C — Approval Package — AFTER RENDERER ACCEPTANCE

Objective: present one coherent review unit containing:

- selected text candidate and score;
- visual asset(s);
- format/brief metadata;
- source/evidence references;
- `approve | edit | reject` actions.

Approval remains human-owned. Generated output never becomes published or positive voice evidence merely because it scored well.

### Slice D — Dedication Scheduling + Approval-Gated LinkedIn Publishing

Objective: after approval, hand the post package to Dedication for timing and official LinkedIn publishing.

Dedication owns:

- schedule / timing decisions;
- approval state;
- publish trigger;
- canonical post state;
- notifications and follow-up.

LinkedIn publishing adapter owns:

- OAuth/provider-specific API call;
- posting the approved text + asset/document;
- returning LinkedIn post ID/URN and provider outcome.

Do not restore the legacy LinkedIn Generator scheduler as a competing orchestration system.

### Later — Analytics + Comment Assistance

After publishing is reliable:

- collect legitimate post-performance signals;
- surface comments on Graham's posts through supported access paths;
- generate suggested replies for human approval;
- evaluate selected external posts only when their content is legitimately supplied to the system;
- do not crawl LinkedIn feeds or deploy autonomous engagement bots that violate platform rules.

## Content Acceptance Track — CONTINUES IN PARALLEL

Use 5–8 genuine professional subjects. Stop at 5 only if the result is already decisive; continue toward 8 when correction patterns remain ambiguous.

For each trial:

1. establish the real subject and factual evidence;
2. run/replicate the opportunity decision without inventing specificity;
3. if `needs_more_evidence`, ask one targeted factual question and resume;
4. produce one full draft around the strongest grounded detail;
5. apply deterministic compliance checks;
6. score Draft A on the separate publish-quality model;
7. if Draft A scores 90+, present it without a rewrite call;
8. if Draft A scores below 90, preserve it and generate exactly one guarded Draft B;
9. score a safe Draft B independently and never silently replace Draft A;
10. once a 90+ candidate exists, create the visual companion plan;
11. present the applicable candidate(s) and visual plan for human review;
12. record `keep`, `edit`, or `reject` plus reason codes;
13. do not promote generated text to positive voice evidence without explicit human authority.

## Trusted Evidence + Invalidation

| Evidence | Why reusable | Invalidated by |
|---|---|---|
| Graham Voice Bible provenance/runtime profile | explicitly authorized and merged | explicit operator reversal or newer approved voice authority |
| Graham Spoken Voice schema | derived from authorized conversational evidence and directly confirmed as sounding like Graham | repeated trial feedback showing systematic voice mismatch |
| Public-language + individual POV rules | defects were directly observed and corrected | repeated approved examples proving the rule too restrictive |
| Opportunity/evidence gate | exact-evidence anchoring and `needs_more_evidence` state are merged | repeated trial failures in topic/evidence routing |
| Publish-ready threshold | operator explicitly chose 90 and one bounded automatic rewrite | later explicit operator reversal or evidence of systematic bad behavior |
| Visual companion requirement | operator explicitly stated normal LinkedIn posts should include an image/carousel | later explicit operator reversal or platform/product evidence showing a text-only path is needed |
| LinkedIn content/API research | current 2026 research already completed | material platform/ranking/API changes |

## Assumptions / Unknowns

| Item | Confidence | Action |
|---|---|---|
| Voice is now close to Graham | high after Trial #1 | validate across additional subjects |
| 90-point rewrite rule reduces correction burden | medium-high | track Draft A/B outcomes during remaining trials |
| Structured visual planning will reduce bad-image regeneration | medium-high | validate planner briefs before adding a renderer |
| Carousel should outperform single images for some multi-part ideas | medium | choose by content structure, then measure later rather than forcing carousels |
| Replicate remains a suitable renderer | medium | verify live models/cost/quality immediately before Slice B implementation |
| Current prompt stack behaves similarly under real repo provider | medium | require at least two accepted subjects through actual repo provider before final publishing readiness |

## Current Acceptance Criteria Before Publishing Integration

- [ ] At least 5 genuine subjects reviewed; use up to 8 if evidence remains ambiguous.
- [ ] Zero approved candidates contain invented factual specificity.
- [ ] Zero approved candidates require unexplained internal terminology to understand the main point.
- [ ] Zero individual-author candidates use unjustified collective `we/us/our` framing.
- [ ] Every finished draft below 90 preserves Draft A and triggers no more than one automatic Draft B.
- [ ] Publish-ready requires publish-quality >=90 plus existing factual/safety guardrails.
- [ ] At least 4 of the first 6 drafted candidates receive `keep` or only a light edit rather than structural rejection.
- [ ] Major correction categories do not recur after a focused fix.
- [ ] Visual Asset Planning Slice A passes its acceptance criteria.
- [ ] At least two human-accepted subjects are exercised through the actual repository generation provider before declaring the content core ready for publishing integration.
- [ ] Final focused Challenge Gate concludes `clear` or explicitly `conditional` for renderer/publishing progression.

## Verification

| Changed / at-risk surface | Check | Result |
|---|---|---|
| PROGRAMSTART managed overlay | synced files compared to PROGRAMSTART `59a9bf4f...` | completed in PR #19 |
| Publish-quality threshold/rewrite | 90+ no rewrite; sub-90 preserves A and creates one B; unsafe B rejected | implemented in PR #20; full provider smoke still pending |
| Voice/public-language quality | human decisions + reason codes | Trial #1 positive; more trials pending |
| Visual planner contracts/guardrails | focused contract/planner/integration tests | active Slice A |
| Provider-path equivalence | minimum two accepted subjects through actual repo provider | blocked until suitable runtime credential is available |
| Rendering quality | real Replicate/render outputs | not started; Slice B |
| Publishing readiness | focused Challenge Gate | pending |

## Trial Evidence

| # | Subject | Gate outcome | Draft A score | Draft B score | Human decision | Reason codes / correction | Notes |
|---:|---|---|---:|---:|---|---|---|
| 1 | AI planning system creating rework by forgetting settled decisions | draft | manual ~87 | manual ~93–95 | keep Draft B | none after rewrite | Voice confirmed as sounding like Graham; Draft B explicitly liked. Scores are manual review estimates, not repository-provider telemetry. |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |

## Stop / Escalation Conditions

- Do not recursively rewrite text until it reaches a score; one automatic review rewrite is the cost/quality boundary.
- Do not move to paid image rendering if structured visual plans themselves are weak or repetitive.
- Do not let an image model typeset finished LinkedIn graphics directly when deterministic typography/layout can do it more reliably.
- Do not begin LinkedIn OAuth/publishing before content + visual package acceptance is clear or explicitly conditional with a narrow known blocker.
- Do not let missing repo-provider credentials block human content/visual-plan validation that can safely proceed.
- Escalate rather than invent facts, visuals, screenshots, metrics, or quotations.

## Close-Out

OUTCOME: pending
VERIFICATION_SUMMARY: pending
EVIDENCE_INVALIDATED_OR_REUSED: existing voice/content architecture reused; visual-companion requirement added by explicit operator decision
AUTHORITY_RECONCILED: this packet remains the single current execution packet; no competing Master Game Plan created
REMAINING_BLOCKERS: actual repo-provider acceptance requires a suitable runtime credential; rendered-asset quality is intentionally deferred until Slice B
NEXT_RECOMMENDED_SLICE: complete Visual Asset Planning / Carousel Planner Slice A, validate on Trial #1, then decide whether Replicate renderer Slice B has earned implementation
