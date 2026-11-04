# LinkedIn Generator — v4 Implementation Handoff Package

**Prepared:** 2026-11-04 · **Status:** Reviewed **planning/evidence** package; implementation acceptance remains `NOT_RUN` here.

## Start here

The user wants an evidence-grounded, authentic LinkedIn post generator with **one Python content engine**, rapid **headless use**, and a compact **Voices/Create/Review UI** sharing identical saved content and voice profiles. Existing owner packet `LIG-CONTENT-VISUAL-ACCEPTANCE-2026-09-01` already puts real subject/visual-plan acceptance before paid rendering; new plans do not supersede it.

| File | Role | Authority |
|---|---|---|
| [Game Plan](LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md) | P0–P7 sequencing, implementation responsibilities, QB-00/IT-01 commands and milestone gates | Supporting implementation proposal |
| [Evidence and Challenge](LINKEDIN_GENERATOR_EVIDENCE_AND_CHALLENGE_V4_2026-11-04.md) | EV-01..24 source register, CH-01..32 challenge register, reuse and risk decisions | Supporting evidence, not automatic product authority |
| [Durable Test Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) | **Only detailed definition** of AT-01..26 and E2E-01..11; human outcomes and review rubric | Proposed acceptance contract pending owner reconciliation |
| [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md) | Sequential execution instruction: starts P0 + authorized P1; continues through eligible gated phases | Execution instruction only, no side-effect authorization |
| [P2 Trial Scorecard](LINKEDIN_GENERATOR_P2_TRIAL_SCORECARD_V4_2026-11-04.csv) | Blank template for up to eight genuine subjects | **NOT_RUN**, contains no generated results |

## Scope in the next chat

- Read [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md); attach this bundle or its extracted files.
- Fetch current Paths `CHATGPT.md` + live owner packet and verify repos/PR states before any implementation.
- P0 baseline and then P1 minimal selected-candidate parity with independent test receipts. Continue to eligible P2 quality work after P1; progress to later phases only when their prerequisites and owner gates clear.
- **Do not** jump to UI, paid images or publishing in the first slice. P2 human/editorial ratings and AT-19..26/E2E-10/11 can run only with genuine human/provider evidence and owner-reconciled thresholds, not by automatic inference. Continue through milestones as eligibility allows.

## Truthful status

- Observed repository source used in this bundle: primary main `a714d1ef355ade9ca47a52b301ea477bd0c14f34`; Paths guide blob `ba7463b91398ae9378a4ad09eba4974dedd5df40`; `LinkedInGenV2` PR #6 observed open/draft, unmerged. Refresh in the new chat.
- No code changes, pytest executions, live model calls, human trial adjudications, rendering, publishing, hosted CI or deployment **were performed to make this documentation package**.
- It is permissible to say **document integrity PASS** after checking cross-references and manifest; it is not permissible to translate that into product PASS.

## User's highest-value challenge now made durable

**Make the system earn its complexity.** Success is not “90/100” or “JSON returned”. It is six genuine, eligible subject evaluations (without forcing fake subjects), human-approved accurate posts with recognizable voice, original useful insights, meaningful visuals, documented edit effort and a blinded simple-prompt comparison. Existing required first-six 4-of-6 and provider evidence remain intact. Any new proposed thresholds need owner reconciliation before enforcement.

## Source-of-truth order

User intent + applicable owner contract + current repository implementation + actual execution receipts **override** this package. The unmerged V2 Next.js/Supabase ADR is a conflicting *branch proposal* rather than automatically accepted architecture in `LinkedIn_Generator`. The next implementation must not create duplicate schedulers or claim authorizing external publication; Dedication owns final approval/publish.

## Copy/paste handoff

```text
Continue the GrahamArdent LinkedIn Generator implementation using the attached v4 ZIP. Read PACKAGE_README, EXECUTION_PROMPT, GAME_PLAN, TEST_OBJECTIVES and EVIDENCE together. Fetch current default-branch GrahamArdent/paths/CHATGPT.md and the current LinkedIn_Generator owner packet. Begin with P0/QB-00 and, if owner-admitted, P1/IT-01 selected-candidate repair with actual red→green receipts. Then continue P2 and later phases in coherent, verified milestones as their owner permissions and human/provider gates clear; do not permanently stop after P1. Preserve AT-19..26 and E2E-10/11 human outcome gates for P2, and never count model scores or fixtures as editorial acceptance. No premature UI, paid rendering, hosted CI, merge or publishing. Return GO/HOLD/FAIL, exact evidence and next eligible step at each checkpoint.
```