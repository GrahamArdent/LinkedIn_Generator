# CURRENT_WORK_PACKET.md

PACKET_ID: LIG-CONTENT-VISUAL-ACCEPTANCE-2026-09-01
STATUS: active
PROJECT: LinkedIn_Generator
ENTRY_MODE: PROGRAMSTART Mode C
CURRENT_STAGE_OR_MILESTONE: Multi-post content + visual-plan acceptance before paid rendering
AUTHORITY_SPINE: `README.md` product role + Dedication boundary, current explicit operator decisions, accepted project contracts/voice authority, validated implementation state on `main`, and this bounded packet
AUTHORITY_VERSION_OR_COMMIT: LinkedIn_Generator `c51eb4afc30977bbbb3dc2193d6f14f3ea84fcdd`; current PROGRAMSTART inspected at `4ece1af3bc6afff9834e551bc9f4e2d8e791b317`; downstream adopted methodology overlay is not yet fully reconciled to that PROGRAMSTART head
BLOCKER_SCOPE: milestone
SAFE_EXECUTION_LANE: A/B — human content acceptance, provider-neutral visual-plan validation, idea preservation, evidence gathering, and reversible repo corrections can proceed
BLOCKED_ACTION: Replicate/paid rendering, scheduling, and publishing remain gated until content + visual planning earn progression; final repo-provider acceptance still requires the actual generation path in a runtime with valid provider credentials

## PROGRAMSTART Routing Decision

This is an in-flight project. Do not create a new Master Game Plan or restart from Stage 0.

Current reevaluation on 2026-09-01 changed the immediate sequence:

1. Visual Asset Planning Slice A is **implemented** in PR #21 / `c51eb4af...`.
2. Slice A is **not yet empirically accepted** across enough real posts to justify paid rendering.
3. Trial #1 text was accepted after one bounded rewrite, and its first conceptual carousel plan is directionally useful, but one post is insufficient evidence for renderer architecture/quality investment.
4. Before Replicate, run several additional genuine subjects through the complete current pipeline and require meaningful variation in visual-format decisions.
5. Preserve worthwhile future ideas in `IDEA_LEDGER.md`; captured/shelved ideas do not become scope or priority.
6. A separate PROGRAMSTART methodology-distribution defect is now under investigation because current PROGRAMSTART changes were not automatically reconciled into this already-adopted repository.

## Durable Product Decisions

1. **90 remains the publish-ready text threshold.** A sub-90 Draft A is preserved and receives at most one automatic guarded Draft B for review.
2. **A normal publishable post package includes a visual companion.** Text-only remains an exceptional/test path, not the target product flow.
3. **Format is a content decision.** Use `single_image` for one sharp visual idea; use `carousel` when progression, comparison, layers, steps, or multiple distinct takeaways genuinely improve the post.
4. **Visual planning precedes rendering.** Do not send a generic post directly to an image model and rely on the model to invent layout/strategy.
5. **Typography is separate from generative imagery.** Overlay text and carousel copy remain deterministic structured fields.
6. **Replicate is the expected first renderer adapter, not permanent architecture authority.** Renderer/provider substitution must remain possible.
7. **Human approval remains mandatory before publishing.** Scores and generated visual plans never authorize posting by themselves.
8. **Dedication owns schedule/publish orchestration.** Do not restore the legacy LinkedIn Generator scheduler as a second scheduling system.
9. **Ideas are preserved separately from execution authority.** `IDEA_LEDGER.md` may retain accepted, candidate, and shelved ideas, but execution occurs only after promotion/reconciliation into the owning authority.

## Execution Sequence

### Slice A — Visual Asset Planning / Carousel Planner — IMPLEMENTED; VALIDATION IN PROGRESS

Implemented in PR #21 / `c51eb4afc30977bbbb3dc2193d6f14f3ea84fcdd`.

Implemented surface:

- typed `single_image | carousel` visual-plan contracts;
- `auto | single_image | carousel` request preference;
- visual planning only for a 90+ publish-quality candidate;
- preservation of whether the visual plan belongs to Draft A or Draft B;
- single-image concept, overlay copy, composition, provider-neutral prompt, negative guidance, and alt text;
- carousel cover/design system plus 4–8 ordered slide specs;
- anti-cliché visual policy;
- typography separated from generated imagery;
- fail-closed handling for malformed plans, format mismatches, unsupported new numbers/URLs/quoted claims, and overlong single-image overlay text;
- Dedication-facing result integration with no scheduling/publishing state.

Implementation acceptance evidence:

- [x] typed/validated single-image and carousel structures exist;
- [x] carousel is bounded to 4–8 ordered slides;
- [x] imagery prompt requires no embedded typography/logos/watermarks;
- [x] visual copy guard blocks new URLs, numeric claims, and quoted claims absent from the approved text candidate;
- [x] explicit format preference is honored or deferred;
- [x] visual planning is not spent on a below-threshold text candidate;
- [x] source candidate (`original` or `rewrite`) is preserved;
- [x] planner remains provider-neutral and creates no scheduling/publishing state.

Remaining Slice A validation:

- [ ] validate at least one clear single-image case on a genuine subject;
- [ ] validate at least one clear carousel case on a genuine subject;
- [ ] validate one genuinely ambiguous format decision;
- [ ] observe whether the planner becomes repetitive or defaults to generic metaphors;
- [ ] confirm the visual brief itself is useful enough to deserve a paid renderer call.

### Slice B — Renderer + Replicate Adapter — GATED

Do not begin until the remaining Slice A validation is sufficient.

Expected design if promoted:

- provider-neutral renderer interface owned by LinkedIn Generator;
- Replicate adapter as first implementation;
- single-image imagery generation from provider-neutral prompt;
- deterministic overlay typography after image generation;
- deterministic carousel slide layout/rendering from structured slide copy;
- bounded candidate/regeneration behavior driven by explicit visual-quality reasons;
- rendered-asset quality checks before human review;
- prompt/model/version/provenance metadata preserved.

### Slice C — Approval Package — AFTER RENDERER ACCEPTANCE

Present one coherent review unit containing selected text candidate + score, visual asset(s), visual metadata, source/evidence references, and explicit `approve | edit | reject` actions.

### Slice D — Dedication Scheduling + Approval-Gated LinkedIn Publishing

After approval, Dedication owns schedule/timing, approval state, publish trigger, canonical post state, notifications, and follow-up. The LinkedIn publishing adapter owns OAuth/provider-specific API execution and returns the final LinkedIn post ID/URN and provider result.

### Later — Analytics + Comment Assistance

Preserved in `IDEA_LEDGER.md`; not current execution. Includes performance learning, human-approved reply assistance, selected external-post comment assistance, and broader API-triggered possibilities when official LinkedIn access changes.

## Content + Visual Acceptance Track

Use 5–8 genuine professional subjects. Stop at 5 only if the result is already decisive; continue toward 8 when correction/format patterns remain ambiguous.

For each trial:

1. establish a real subject and factual evidence;
2. run the opportunity/evidence decision without inventing specificity;
3. if `needs_more_evidence`, ask one targeted factual question and resume the same opportunity;
4. produce one full draft around the strongest grounded detail;
5. apply deterministic compliance checks;
6. score Draft A on the separate publish-quality model;
7. if Draft A scores 90+, do not spend a rewrite call;
8. if Draft A scores below 90, preserve A and generate exactly one guarded Draft B;
9. score a safe Draft B independently and never silently replace A;
10. once a 90+ candidate exists, create the visual companion plan;
11. present applicable text candidate(s) and visual plan for human review;
12. record `keep`, `edit`, or `reject` plus reason codes;
13. do not promote generated text to positive voice evidence without explicit human authority;
14. record future/non-current opportunities in `IDEA_LEDGER.md` instead of expanding this packet.

## Trusted Evidence + Invalidation

| Evidence | Why reusable | Invalidated by |
|---|---|---|
| Graham Voice Bible provenance/runtime profile | explicitly authorized and merged | explicit operator reversal or newer approved voice authority |
| Graham Spoken Voice schema | derived from authorized conversational evidence and directly confirmed as sounding like Graham | repeated trial feedback showing systematic voice mismatch |
| Public-language + individual POV rules | defects directly observed and corrected | repeated approved examples proving rule too restrictive |
| Opportunity/evidence gate | exact-evidence anchoring and `needs_more_evidence` state merged | repeated trial failures in topic/evidence routing |
| 90 publish-ready threshold | explicit operator decision + bounded one-rewrite rule | later explicit reversal or systematic bad outcomes |
| Visual companion requirement | explicit operator decision | later explicit reversal or evidence that text-only must be a first-class normal path |
| Slice A implementation | merged PR #21 | later code change or validation showing structural defect |
| LinkedIn content/API research | current 2026 research | material platform/ranking/API changes |

## Methodology Distribution Dependency — ACTIVE INVESTIGATION

Observed on 2026-09-01:

- LinkedIn Generator's `.programstart-manifest.json` was created from PROGRAMSTART `f74d51f...` and contains only the attach-time managed file list.
- Current PROGRAMSTART is `4ece1af3...` and includes later reusable methodology/control assets and newer idea-preservation/learning architecture semantics.
- `programstart sync` currently reads the downstream manifest's existing `files` list; newly managed assets added after attachment are therefore not discoverable through that old manifest.
- `programstart sync` is an explicitly invoked dry-run/`--confirm` mechanism, not an automatic fan-out service by itself.
- PROGRAMSTART's current Idea Ledger template is deliberately **not** a mandatory generated-project artifact; this project's `IDEA_LEDGER.md` is an explicit project-specific adoption, not evidence that automatic template distribution should have created it.

Required outcome:

- diagnose/fix the reusable downstream sync/distribution semantics in PROGRAMSTART rather than patching only this repo;
- distinguish managed reusable controls from optional/project-specific artifacts;
- ensure existing attached repos can discover newly added managed assets without destructive re-attach;
- ensure sync/reconciliation updates downstream provenance/manifest state so staleness is observable;
- separately decide what runtime (Program Store/central controller/Watchtower/execution worker) is responsible for invoking safe downstream reconciliation automatically.

Until corrected, do not claim this repo's adopted PROGRAMSTART overlay is fully current merely because selected files were manually synced earlier.

## Current Acceptance Criteria Before Replicate/Publishing Progression

- [ ] At least 5 genuine subjects reviewed; use up to 8 if evidence remains ambiguous.
- [ ] Zero approved candidates contain invented factual specificity.
- [ ] Zero approved candidates require unexplained internal terminology to understand the main point.
- [ ] Zero individual-author candidates use unjustified collective `we/us/our` framing.
- [ ] Every finished draft below 90 preserves Draft A and triggers no more than one automatic Draft B.
- [ ] Publish-ready requires publish-quality >=90 plus existing factual/safety guardrails.
- [ ] At least 4 of the first 6 drafted candidates receive `keep` or only a light edit rather than structural rejection.
- [ ] Major correction categories do not recur after a focused fix.
- [x] Slice A implementation/contract acceptance is complete.
- [ ] Slice A human visual-plan validation covers single-image, carousel, and ambiguous cases without showing a repetitive/generic planning failure.
- [ ] At least two human-accepted subjects are exercised through the actual repository generation provider before declaring the content core ready for publishing integration.
- [ ] Focused Challenge Gate concludes `clear` or explicitly `conditional` for renderer progression.

## Verification

| Changed / at-risk surface | Check | Result |
|---|---|---|
| PROGRAMSTART managed overlay | prior selective sync to `59a9bf4f...` | superseded as currentness evidence; current PROGRAMSTART is newer and distribution defect is under investigation |
| Publish-quality threshold/rewrite | 90+ no rewrite; sub-90 preserves A and creates one B; unsafe B rejected | implemented PR #20; provider smoke pending |
| Voice/public-language quality | human decisions + reason codes | Trial #1 positive; more trials pending |
| Visual planner contracts/guardrails | focused contract/planner/integration review | implemented PR #21 |
| Visual planner usefulness | varied genuine post trials | pending |
| Provider-path equivalence | minimum two accepted subjects through actual repo provider | blocked until suitable runtime credential available |
| Rendering quality | real Replicate/render outputs | gated; not started |
| Methodology downstream distribution | PROGRAMSTART root-cause/fix + existing-repo retest | active parallel learning case |

## Trial Evidence

| # | Subject | Gate outcome | Draft A score | Draft B score | Human decision | Visual outcome | Notes |
|---:|---|---|---:|---:|---|---|---|
| 1 | AI planning system creating rework by forgetting settled decisions | draft | manual ~87 | manual ~93–95 | keep Draft B | conceptual carousel direction accepted as useful enough for further validation, not renderer acceptance | Voice confirmed as sounding like Graham; scores are manual estimates, not repo-provider telemetry. |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |

## Stop / Escalation Conditions

- Do not recursively rewrite text until a score is reached; one automatic review rewrite is the cost/quality boundary.
- Do not move to paid image rendering if structured visual plans are weak, repetitive, padded, or generic.
- Do not let an image model typeset finished LinkedIn graphics when deterministic typography/layout can do it more reliably.
- Do not begin LinkedIn OAuth/publishing before content + visual package acceptance is clear or explicitly conditional with a narrow known blocker.
- Do not let missing provider credentials block human content/visual-plan validation that can safely proceed.
- Do not let a methodology-distribution defect silently redefine project authority; fix the reusable owner and then reconcile downstream deliberately.
- Escalate rather than invent facts, visuals, screenshots, metrics, quotations, or access permissions.

## Close-Out

OUTCOME: pending
VERIFICATION_SUMMARY: Slice A code/contract complete; human validation and provider smoke remain open
EVIDENCE_INVALIDATED_OR_REUSED: existing voice/content architecture reused; prior claim of current PROGRAMSTART overlay invalidated by newer live methodology and sync/distribution findings
AUTHORITY_RECONCILED: project execution authority is current to LinkedIn Generator `c51eb4af...`; PROGRAMSTART downstream overlay reconciliation remains an active external dependency
REMAINING_BLOCKERS: varied visual-plan validation, actual provider smoke, and PROGRAMSTART downstream-distribution correction before claiming methodology-currentness
NEXT_RECOMMENDED_SLICE: continue Trials #2–#5 with varied visual-plan outcomes while PROGRAMSTART downstream-distribution defect is fixed in parallel; only then run focused Challenge for Replicate Slice B
