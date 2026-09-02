# CURRENT_WORK_PACKET.md

PACKET_ID: LIG-CONTENT-VISUAL-ACCEPTANCE-2026-09-01
STATUS: active
PROJECT: LinkedIn_Generator
ENTRY_MODE: PROGRAMSTART Mode C
CURRENT_STAGE_OR_MILESTONE: Multi-subject content + visual-plan acceptance before paid rendering and publishing integration
AUTHORITY_SPINE: `README.md` product role + Dedication boundary, current explicit operator decisions, accepted project contracts/voice authority, validated implementation state on `main`, and this bounded packet
AUTHORITY_VERSION_OR_COMMIT: LinkedIn_Generator `c51eb4afc30977bbbb3dc2193d6f14f3ea84fcdd`; PROGRAMSTART current methodology consulted at `4ece1af3bc6afff9834e551bc9f4e2d8e791b317`
BLOCKER_SCOPE: milestone
SAFE_EXECUTION_LANE: A/B — human content acceptance, provider-neutral visual-plan validation, idea preservation, evidence gathering, review, and reversible repo corrections can proceed
BLOCKED_ACTION: paid image rendering, Replicate/provider implementation, and publishing remain gated until the current validation evidence is sufficient; final repo-provider acceptance also requires the actual generation path in a runtime with valid provider credentials

## PROGRAMSTART Routing Decision

This is an in-flight project. Do not create a new Master Game Plan or restart from Stage 0.

Reevaluation on 2026-09-01 found that **Replicate implementation is not yet the highest-value next action**. Visual Asset Planning Slice A is implemented, but it has only one human-reviewed content/visual example. The next uncertainty is empirical: does the current text + visual planner produce consistently good packages across different subjects and correctly distinguish single-image versus carousel use?

Current PROGRAMSTART also now provides an optional Idea Ledger pattern. `IDEA_LEDGER.md` is adopted here as a **non-authoritative preservation surface** so worthwhile future ideas are not lost in chat history and are not accidentally promoted into current scope.

Therefore the current execution lane is:

**reconciled authority + durable idea capture → Trials #2–#5 across varied subject/format shapes → focused Challenge decision → Replicate/rendering only if earned**

## Durable Product Decisions

1. **90 remains the publish-ready text threshold.** A sub-90 Draft A is preserved and receives at most one automatic guarded Draft B for review.
2. **A normal publishable post package includes a visual companion plan.** Text-only publishing is not the target path, though the contract can disable visuals for tests/exceptional cases.
3. **Format is a content decision.** Use `single_image` for one strong visual idea; use `carousel` when sequence, comparison, steps, layers, or multiple distinct takeaways genuinely improve understanding.
4. **Visual planning precedes rendering.** Do not send a generic post directly to an image model and rely on the provider to invent the design.
5. **Typography is separated from generative imagery.** Generated imagery does not typeset the final LinkedIn graphic; text/layout remain structured for deterministic rendering.
6. **Replicate is the expected first rendering adapter, not permanent architecture.** Provider/model choice should be verified with current evidence before implementation.
7. **Human approval remains mandatory before publishing.** A score or generated visual plan is never permission to publish.
8. **Dedication owns scheduling, approval state, canonical post state, publishing orchestration, and notifications.** Do not restore the legacy LinkedIn Generator scheduler as a competing system.
9. **Ideas are preserved separately from execution authority.** `CAPTURED`, `CANDIDATE`, `INVESTIGATING`, and `SHELVED` in `IDEA_LEDGER.md` mean only “worth remembering/evaluating,” not approved scope.

## Current Execution Sequence

### Slice A — Visual Asset Planning / Carousel Planner — IMPLEMENTED; HUMAN VALIDATION IN PROGRESS

Merged in PR #21 at `c51eb4afc30977bbbb3dc2193d6f14f3ea84fcdd`.

Implemented surface:

- typed `single_image | carousel` visual-plan contracts;
- `auto | single_image | carousel` preference;
- visual planning only after a publish-ready text candidate exists;
- single-image brief: concept, overlay text, composition, style, provider-neutral generation prompt, negative guidance, alt text;
- carousel brief: cover headline, design system, 4–8 ordered slides, slide copy, visual direction, alt text;
- anti-cliché visual policy;
- generated imagery separated from typography/layout;
- fail-closed behavior for malformed plans, unsupported format choices, excessive overlay text, missing generation prompts, or new unsupported URLs/numbers/quoted claims;
- result preserves whether the visual belongs to Draft A or Draft B;
- no scheduling/publishing state and no render-provider dependency.

Implementation acceptance evidence:

- [x] both `single_image` and `carousel` plans have typed/validated structures;
- [x] carousel structure is bounded to 4–8 ordered slides;
- [x] single-image generation prompt explicitly separates embedded typography;
- [x] visual copy guard blocks new URL/numeric/quoted factual tokens absent from approved text;
- [x] explicit format preference is honored or deferred;
- [x] below-threshold text does not spend a visual-planning call;
- [x] source candidate (`original` or `rewrite`) is preserved;
- [x] planning remains provider-neutral and owns no scheduling/publishing state;
- [ ] human validation shows the format choice and visual concept are consistently useful across materially different subjects.

### Current Gate — Trials #2–#5 — ACTIVE

Objective: validate the combined text + visual-planning system across different content shapes before paying for rendering integration.

Required trial diversity:

- at least one subject that should naturally become a **single image**;
- at least one subject that should naturally become a **carousel**;
- at least one subject where the format choice is genuinely ambiguous and the planner must justify its choice;
- if naturally encountered, one weak/thin subject that is skipped or requests more evidence instead of being dressed up.

For each trial:

1. establish a genuine subject and grounded factual evidence;
2. run/replicate the opportunity/evidence decision without inventing specificity;
3. if `needs_more_evidence`, ask one targeted factual question and resume;
4. produce Draft A around the strongest grounded detail;
5. apply deterministic compliance checks;
6. score Draft A on publish quality;
7. if Draft A is below 90, preserve it and create exactly one guarded Draft B;
8. select only a 90+ safe candidate as publish-ready for review;
9. create a provider-neutral visual plan for that candidate;
10. review both **content quality and visual-plan usefulness**;
11. record `keep`, `edit`, or `reject` plus reason codes where relevant;
12. if the same major defect recurs, fix the smallest responsible rule before continuing.

### Slice B — Renderer + Replicate Adapter — GATED CANDIDATE

Begin only if the current multi-subject validation shows the visual planner is useful enough that rendering is worth paying for.

Expected design if promoted:

- renderer interface owned by LinkedIn Generator;
- current-model/provider comparison immediately before selection;
- Replicate as expected first adapter if evidence still supports it;
- single-image imagery generation from provider-neutral prompt;
- deterministic overlay typography after image generation;
- deterministic carousel slide layout/rendering from structured slide copy;
- bounded render candidates rather than unlimited regeneration;
- rendered-asset quality checks before human review;
- prompt/model/version/provenance metadata;
- reason-coded visual feedback if real render failures justify it.

### Slice C — Approval Package — AFTER RENDERER ACCEPTANCE

Present one coherent review unit containing the selected text candidate/score, visual asset(s), brief/format metadata, source/evidence references, and `approve | edit | reject` actions. Approval remains human-owned.

### Slice D — Dedication Scheduling + Approval-Gated LinkedIn Publishing

After human approval, Dedication owns timing, approval state, publish trigger, canonical post state, notifications, and follow-up. A LinkedIn publishing adapter owns only provider-specific OAuth/API posting and return of the post ID/URN/outcome.

### Later — Analytics + Comment Assistance

Potential later ideas are preserved in `IDEA_LEDGER.md` rather than expanded here before they are promoted.

## Idea Preservation

`IDEA_LEDGER.md` is the project-specific preservation surface for future/alternative ideas that are worth remembering but are not current authority.

Current captured/shelved areas include:

- direct LinkedIn publishing versus Buffer fallback;
- human-approved reply assistance on Graham's posts;
- selected external-post comment assistance without feed crawling;
- Graham-specific post-performance learning;
- learning when single image versus carousel works best;
- render-provider/model comparison;
- reason-coded visual-quality feedback.

Promotion rule: when one becomes a real candidate for action, evaluate it against current evidence in the correct Mode C entry path, reconcile it into the actual owning artifact if accepted, and execute only from that reconciled authority.

## Trusted Evidence + Invalidation

| Evidence | Why reusable | Invalidated by |
|---|---|---|
| Graham Voice Bible provenance/runtime profile | explicitly authorized and merged | explicit operator reversal or newer approved voice authority |
| Graham Spoken Voice schema | derived from authorized conversational evidence and directly confirmed as sounding like Graham | repeated trial feedback showing systematic voice mismatch |
| Public-language + individual POV rules | defects were directly observed and corrected | repeated approved examples proving a rule too restrictive |
| Opportunity/evidence gate | exact-evidence anchoring and `needs_more_evidence` state are merged | repeated trial failures in topic/evidence routing |
| Publish-ready threshold | operator explicitly chose 90 and one bounded automatic rewrite | later explicit operator reversal or systematic bad outcomes |
| Visual companion requirement | operator explicitly stated normal LinkedIn posts should include an image/carousel | later explicit reversal or contrary product/platform evidence |
| Slice A implementation | merged PR #21 with focused contract/planner/integration coverage | later changes to the same planner/contracts/integration surfaces |
| LinkedIn content/API research | current 2026 research completed | material platform/ranking/API changes |
| Idea Ledger semantics | current PROGRAMSTART `IDEA_LEDGER.md` consulted at `4ece1af3...` | newer methodology changing idea lifecycle semantics |

## Assumptions / Unknowns

| Item | Confidence | Action |
|---|---|---|
| Voice is now close to Graham | high after Trial #1 | validate across additional real subjects |
| 90-point rewrite rule reduces correction burden | medium-high | track Draft A/B outcomes during remaining trials |
| Structured visual planning will reduce bad-image regeneration | medium | validate across single-image, carousel, and ambiguous cases before rendering |
| Visual planner will avoid repetitive metaphors | medium-low | explicitly watch Trials #2–#5 for repeated paths/arrows/checkpoints/AI clichés |
| Replicate remains a suitable first renderer | medium | verify current models/cost/quality immediately before Slice B |
| Current prompt stack behaves similarly under actual repo provider | medium | require at least two human-accepted subjects through real repo provider before final publishing readiness |

## Current Acceptance Criteria Before Rendering/Publishing Progression

- [ ] At least 5 genuine subjects reviewed; use up to 8 if evidence remains ambiguous.
- [ ] Zero approved candidates contain invented factual specificity.
- [ ] Zero approved candidates require unexplained internal terminology to understand the main point.
- [ ] Zero individual-author candidates use unjustified collective `we/us/our` framing.
- [ ] Every finished draft below 90 preserves Draft A and triggers no more than one automatic Draft B.
- [ ] Publish-ready requires publish-quality >=90 plus existing factual/safety guardrails.
- [ ] At least 4 of the first 6 drafted candidates receive `keep` or only a light edit rather than structural rejection.
- [ ] Major correction categories do not recur after a focused fix.
- [x] Visual Asset Planning Slice A implementation criteria are satisfied.
- [ ] Visual plans are human-judged useful across multiple materially different subjects/formats.
- [ ] At least two human-accepted subjects are exercised through the actual repository generation provider before declaring the content core fully ready for publishing integration.
- [ ] Focused Challenge Gate concludes `clear` or explicitly `conditional` before Slice B / publishing progression.

## Verification

| Changed / at-risk surface | Check | Result |
|---|---|---|
| Current authority reconciliation | compare live `main` and packet authority | reconciled on branch; PR pending |
| Idea preservation | project ledger follows current PROGRAMSTART non-authoritative semantics | added on branch; PR pending |
| Publish-quality threshold/rewrite | 90+ no rewrite; sub-90 preserves A and creates one B; unsafe B rejected | implemented PR #20; live provider smoke pending |
| Voice/public-language quality | human decisions + reason codes | Trial #1 positive; more trials pending |
| Visual planner contracts/guardrails | focused contract/planner/integration coverage | implemented PR #21; human validation pending |
| Provider-path equivalence | minimum two accepted subjects through actual repo provider | pending suitable runtime credential |
| Rendering quality | real rendered outputs | intentionally not started |
| Publishing readiness | focused Challenge Gate | pending |

## Trial Evidence

| # | Subject | Gate outcome | Draft A score | Draft B score | Human decision | Visual plan | Notes |
|---:|---|---|---:|---:|---|---|---|
| 1 | AI planning system creating rework by forgetting settled decisions | draft | manual ~87 | manual ~93–95 | keep Draft B | 5-slide carousel concept; human visual-plan validation not yet explicit | Voice confirmed as sounding like Graham; Draft B explicitly liked. Scores are manual review estimates, not repository-provider telemetry. |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |

## Stop / Escalation Conditions

- Do not recursively rewrite text until it reaches a score; one automatic review rewrite is the boundary.
- Do not move to paid image rendering if visual plans are weak, repetitive, padded, or not adding value.
- Do not let an image model typeset finished LinkedIn graphics when deterministic typography/layout can do it more reliably.
- Do not begin LinkedIn OAuth/publishing before content + visual package acceptance is clear or explicitly conditional with a narrow blocker.
- Do not let missing repo-provider credentials block human content/visual-plan validation that can safely proceed.
- Escalate rather than invent facts, visuals, screenshots, metrics, or quotations.
- Preserve worthwhile future ideas in `IDEA_LEDGER.md`; do not add them to the active packet unless promoted.

## Close-Out

OUTCOME: pending
VERIFICATION_SUMMARY: Slice A implemented; multi-subject human validation now active
EVIDENCE_INVALIDATED_OR_REUSED: existing voice/content/visual architecture reused; no settled decision reopened
AUTHORITY_RECONCILED: pending merge of this packet update; no competing Master Game Plan created
REMAINING_BLOCKERS: multi-subject visual-plan evidence, real repo-provider acceptance, rendered-asset evidence, publishing integration
NEXT_RECOMMENDED_SLICE: complete Trials #2–#5 and run a focused Challenge decision; promote Slice B only if the planner earns it
