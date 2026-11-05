# LinkedIn Codex Trial Game Plan — evidence-first continuation

**Goal:** Produce useful, grounded LinkedIn writing with the existing Python engine and Codex subscription, then prove whether its extra steps help.
**Status:** Connection qualified; writing acceptance HOLD. Phases1–3 are implemented and fixture-qualified; one substantive native trial completed. Phase4 human review and corpus expansion remain open; scorer/human calibration is missing.
**Authority:** CURRENT_WORK_PACKET.md is the active pointer. This is a P2 subplan within the existing P0–P7 roadmap, not a competing master plan. Preserve all26 AT objectives and11 E2E scenarios.
**Execution:** Inline, one phase at a time; test-first code corrections. Reuse existing code/results. Every meaningful phase ends with the checkpoint below.

## What is settled

Codex bridge/launcher and selected-text/visual identity work locally. Prior qualification:142 LinkedIn tests and30 reused-client tests passed. Two real subjects produced unqualified engine drafts; original73, then78/rewrite77. Historical weak results and limited preferences remain visible, not promoted to approvals or voice examples. Exact source/receipts: evidence/codex-first-20261104 and evidence/transparent-evaluation-20261104.

We used narrow conversation/code evidence, not zero evidence. That supported what happened in our test, but not broader customer outcomes or measured benefits. Opinion is legitimate; factual assertions inside it still need support. More citations alone do not create a better argument.

**Limits:** No paid API/fallback; use the existing qualified Codex route. Preserve score90 and one guarded publish-quality rewrite unless the owner explicitly changes them after calibration. No mandatory extra critic/humanizer calls, database, UI, renderer or new architecture. No resume W7 rerun. Hosted CI, merge, installation promotion and publication require their existing admissions; checking their status does not authorize them.

## Phase 0 — establish one reliable checkpoint

- [x] Refresh Paths, packet, candidate/main heads, PR24 and the actual launcher/config/client binding. Reuse completed connection/P0/P1 work.
- [x] Run local CI at this documentation milestone; retain source/config hashes and exact outcomes. During subsequent implementation, reuse the existing receipt patterns rather than add a status service.
- [x] At every phase boundary record the five states below and update packet + plan + evidence in the same logical change.

**Pass:** cold continuation can identify the next phase and distinguish tested candidate, merged main and actual runtime. A green test is not proof of merge or installation.
**Verification:** local pytest, diff/integrity checks, GitHub readback and launcher/module-path inspection. All observation must avoid model generation.

## Phase 1 — prepare evidence before changing the writer

- [x] Choose one substantive audience question from existing Graham/Ardent subject material. Avoid another post about our testing process. Define the reader, main point and supported consequence.
- [x] Assemble a small source bundle: source ID, title/URL or record, author/publisher, publication/event date where relevant, checked_at, exact supporting passage/record and limitations. Read the source itself; a URL or search snippet is not support.
- [x] Map each checkable claim to support and mark fact / personal observation / inference / opinion. Include material counterevidence, stale information and contradictions. Real user-confirmed experience is a primary source; external research is not mandatory for every opinion.
- [x] For this trial prefer at least one independent primary source or a concrete verified professional observation that supports the central factual anchor. A stronger claim needs stronger evidence; do not impose arbitrary citation counts.
- [x] Freeze request + source bundle before drafting. Keep extra provenance beside the existing SourceEvidence request initially; extend contracts only if consumer tests require it.

**Tests:** sufficient support permits the intended claim; missing central support requests one targeted detail or defers; stale/contradictory sources cannot be silently presented as settled fact; opinion is not rejected merely for lacking a statistic.
**Pass:** one usable evidence brief plus negative fixtures. No invented specificity to satisfy the scorer.
**Maps to:** AT03/14/21/26.

## Phase 2 — make existing writing guidance operational

- [x] Build a compact, source-specific editorial plan: assumption/tension, exact factual anchor, mechanism, supported human/business consequence, takeaway and natural closer.
- [x] Reuse the Voice Bible's causal reasoning and Spoken Voice. Use only supported layers; never force every stakeholder, emotional beat, analogy or financial consequence.
- [x] Supply the same approved voice material to relevant stages. Reuse genuinely approved examples if their provenance is available; a limited preference is not an approved example.
- [x] Replace generic angle scaffolding only where tests demonstrate need. Keep existing engine/provider/contracts and at most one guarded quality rewrite.
- [x] A clean house-rule score must not be described as editorial success. The existing semantic quality assessment already runs: improve its use rather than enable named critic/humanizer stages merely to add calls.

**Tests:** the actual drafting consumer receives the frozen anchor/plan/voice; changing or removing essential support changes the allowed claim/readiness; formatted-but-generic writing is not accepted by a formatting check alone; rewritten text retains support and candidate/visual identity.
**Pass:** fixture-qualified source-specific planning and prompt flow, without extra rewrite loops.
**Maps to:** AT01/02/03/18/19/20/21.

## Phase 3 — align the scorer; do not chase90

- [x] Preserve separate factual/safety checks, house-rule compliance, model editorial ratings and human approval.
- [x] Give the evaluator the same relevant brief, goal, voice guidance and approved examples as the writer. Define concrete0–5 anchors; do not claim these ratings predict LinkedIn engagement.
- [x] Compare against a small existing human-approved/rejected reference set if available; otherwise record calibration as missing. Preferences alone cannot fabricate that set.
- [x] Make critiques identify the largest fixable defect. Missing evidence goes back to the brief; rewriting cannot create facts.
- [x] When numerical comparisons are presented, assess engine and simple baseline with the same rubric. Preserve weights/threshold90 until a separately recorded owner decision changes them.

**Tests:** consistent brief/voice reaches writer and judge; missing dimension or malformed judgment is explicit; supplied human labels remain immutable; uncertainty is reported; one targeted rewrite only; no artificial score inflation.
**Pass:** transparent, test-qualified scoring contract. Model alignment with Graham remains unproved until actual reference judgments exist.
**Maps to:** AT02/16/19/20/23/24.

## Phase 4 — one substantive trial, then controlled expansion

- [x] Freeze the Phase1 evidence brief and Phase2/3 prompt/config hashes. Declare one-subject budget before launch: <=12 model executions, <=900 cumulative CLI seconds, no API fallback or automatic retries.
- [x] Generate one engine result and one same-model/simple-prompt comparison with equal facts, audience, constraints and voice. Score both if showing numerical comparison.
- [x] Retain exact source-to-request-to-prompt-to-claim links, actual stage changes, A/B, selected hash, critiques, costs/usage where observable, and visual plan/deferral.
- [x] Test an omitted critical source through the actual preflight consumer; it must block/qualify the unsupported claim without launching an unauthorized replacement. Prompt inclusion alone is not causal influence proof.
- [ ] Present readable outputs and get exact-hash human feedback: factual accuracy, voice, insight/usefulness, keep/light/structural/reject, actual edit effort and comparison preference. Clearly distinguish transparent diagnosis from a blinded pilot.
- [ ] After the first substantive human disposition, expand in small admitted batches toward six eligible distinct subjects, maximum8 subject trials. Preserve earlier weak results and denominators; do not cherry-pick them away.

**Pass:** actual phase-specific AT/E2E evidence supports P2 disposition. Keep existing >=4/6 keep/light, >=2 native-provider human-accepted subjects, source/voice/visual/originality requirements and blinded >=4/6 preference gate. Ties are not wins; insufficient subjects means NOT_YET_EVALUABLE.
**Maps to:** AT04/05/14/19–26 and E2E06/10/11. P3 production and rendering remain gated.


## Required checkpoint after every meaningful phase

1. **Source:** candidate HEAD, base/main SHA, dirty changes, source/config hashes and reviewed diff.
2. **Local CI:** targeted tests + one full `python -m pytest -q` at code convergence, `git diff --check`, exact interpreter/UTC/command/exit/log refs. Fix machine-solvable failures; never weaken assertions. Documentation milestones check links/objective IDs/status integrity; this update also runs full local CI as requested.
3. **Integration:** PR state/head, required reviews/checks and whether that exact candidate is actually merged. Read status; do not auto-enable hosted workflows or infer merge from a push.
4. **Runtime:** resolved launcher/interpreter/module path, running source/config/client revision, and whether it is a candidate trial checkout or released installation. Inspect/show only; no hidden generation. After an authorized install, verify exact readback plus no-call reopen. Otherwise report NOT_INSTALLED, STALE or CANDIDATE_ONLY truthfully.
5. **Continuation:** reconcile CURRENT_WORK_PACKET, this plan, prompt and evidence. Record GO/HOLD/FAIL, expected versus observed, remaining debt and next eligible action. A later docs-only commit may reuse tests only after proving tested code/config unchanged; report both revisions.

Use one milestone receipt under `evidence/milestones/<milestone>/`, linked by the packet; no new registry or service. The packet names the latest receipt. Stale/missing proof is UNKNOWN/HOLD, never guessed. A clearly recorded unmerged development candidate may continue authorized source phases; it is not a main release. Merge/install only through existing admission, then refresh all affected states.

## Independent voice-selection correction
The previous two-identity PDF did not test writing voices. The bounded selector correction is implemented and locally qualified in [the selector subplan](WRITING_VOICE_SELECTOR_2026-11-04.md). Reuse it; do not recreate the V2 architecture. Nine generic craft-only projections are independent of author identity. The source of truth is config/writing_voices.json; historical labels are provenance/aliases, not imitation instructions.

**Next:** Controlled writing-voice comparison using explicit writing_voice_id, fixing author/story/facts/audience/central argument, model and constraints. Preserve existing source bundle admission and all weak prior outcomes. Compare actual style behavior with human review; do not substitute195 green implementation tests for that result. P2 product/first-six/pilot/calibration/visual gates remain HOLD.

## Controlled writing-voice comparison — 2026-11-04

Current receipt: evidence/controlled-voice-comparison-20261104/MILESTONE.json and REPORT.md. Nine actual unedited first drafts now hold Graham Hill, story, facts, audience, argument, model and constraints fixed; only the verified writing_voice changes. The existing drafting stage is isolated before critic/humanizer/scoring, so these are not full engine acceptance runs. Nine native model executions,27 physical starts,107.900 cumulative CLI seconds/API0; fresh-process reopen adds0 calls. Frozen product/config/tests and26 AT/11 E2E definitions remain unchanged. PDF:13 pages, linked contents, raw text verified and all pages visually reviewed.

Fresh full local CI:195 PASS (1.96s); log retained. Machine result GO; human voice/quality acceptance HOLD. All9 hooks begin “An approval screen”; factual paragraphs and takeaways are similar. Preserve this weak differentiation finding and do not infer a winner or regenerate to manufacture contrast. Earlier identity/angle sampler remains historical. Next eligible action is human inspection of retained drafts and specific passage feedback; no scoring/keep/example promotion inferred. Candidate-only/unmerged; no hosted CI, installation promotion, deployment or publishing.
