# LinkedIn Generator — completion game plan
Updated November 5, 2026. Current authority pointer: CURRENT_WORK_PACKET.md (repository root).
Execution entry: LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md.
Broader P0–P7 roadmap: LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md.
Detailed acceptance definitions remain solely in LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md.

## Current truth
- Verified candidate: branch fix/essential-review-gate-20261105, product commit d3ee2a36d037323c080edec67b53a521bcceb75c;
  evidence follow-up5dccb89689222adae5c83efd0c5fd207a0c3370b.251 local and251 clean-archive tests passed.
- Installed release is2c2daf39398a993b698d1f225008a06217b14a7c, using essential-checks-v1. Previous0c099d7 remains preserved for rollback.
- The candidate's essential-checks-v1 replaces numeric admission with four independent verdicts and reasons:
  factual integrity, reader relevance, practical value, argument/voice fidelity.
  All must pass. Scores are advisory; passing means human review eligibility, never approval.
  Missing evidence pauses; fixable failures allow at most one guarded targeted rewrite; unavailable evaluation fails closed.
- Real evaluator smoke: retained security draft72/reviewable, deliberately unsupported negative69/needs_evidence.
  Two subscription evaluations/38.311 active CLI seconds/API0. These are not human quality labels.
- Evidence: evidence/essential-review-gate-20261105/{REPORT.md,MILESTONE.json,ACCEPTANCE_AUDIT.json}.
- The complete product is not accepted. All26 AT objectives and11 E2E scenarios remain;
  the audit distinguishes fixture checks, historical observations and missing human/live proof.

## Current milestone status
M1/M2 GO: independent review and251 tests qualified the source; PR29 merged/installed2c2daf3,
with rollback0c099d7, hashes/imports/subscription binding and zero-call reopening verified.
M3 security package technically completed, but Graham rejected the subject as unsuitable. It is
historical technical evidence, not a human accepted post. Do not require him to score that unsuitable pair.
Current editorial authority: GRAHAM_CONTENT_DIRECTION_2026-11-05.md. Graham only; varied subjects;
selectable writing style independent of identity/credentials; broad supported perspective permitted.
The liked black-box chat draft is a positive reference, not installed evidence or publication approval.
Current bounded diagnostic: two installed first drafts, concise_challenger v2 and reflective_leader v2,
same facts/author/audience/question;2 model executions/6 CLI starts/32.254 active seconds/API0;
exact-output/hash and zero-call reopen verified. Human feedback pending; no style winner declared.
Receipt: evidence/graham-black-box-voices-20261105/MILESTONE.json. Review COMPARISON.md and
CHAT_REFERENCE.md there. Both native drafts are more formal than the reference in assistant review.
Next: recorded feedback prefers Version1 voice but rejects its construction; chat revision72946 is
positively reviewed. Use the adopted scaffold/workflow in GRAHAM_CONTENT_DIRECTION_2026-11-05.md,
then carry it through existing installed editorial handoff/full-engine/control M3/M4 qualification.
Evaluate voice and coherent progression separately. Current feedback receipt:
 evidence/graham-black-box-voices-20261105/STRUCTURE_FEEDBACK.json. Installed structure behavior remains unproved.
The style diagnostic does not substitute for full-engine/baseline, six-subject, visual or publishing gates.
All26 AT/11 E2E retained; historical first-six eligibility unresolved. No active hosted workflow.

## Document ownership and just-in-time execution
- CURRENT_WORK_PACKET.md owns the current checkpoint and evidence pointer.
- This completion plan owns M1–M5 steps and milestone exit conditions.
- The execution prompt routes the worker; it does not maintain another task list.
- The acceptance document alone owns detailed AT/E2E criteria. The broader roadmap owns later dependencies.
- Historical receipts prove only their recorded scope; later docs do not reinterpret them.
Use known working routes directly. Load only the current milestone's sources/contracts; inspect
later P3–P7 owner documents when their boundary is reached, not as a preload.
Preserve exact failures and follow Paths recovery for actual route failures. Reconcile unknown effects
through original receipts; never blindly retry. Continue independent admitted work while one item is held.
Budget exhaustion or an unrecoverable provider/environment failure is a precise HOLD, not permission
to exceed caps or repeatedly ask the user to perform machine work.

## Active structure-to-install slice — first unmet Q step

This is the current bounded work inside the existing M1–M5 spine, not another master plan.
Goal: make the Graham workflow deliberately prepare structure, carry it through actual writing/review,
and run from a verified fixed release. “Reliable” means repeatable preparation, traceable execution,
coherent reviewed output and safe read/recovery behavior; deterministic prose is not promised.
Spec: GRAHAM_CONTENT_DIRECTION_2026-11-05.md, especially Adopted structure and workflow.
Installed baseline2c2daf3/251 tests remains valid only for unchanged bytes. Current plan source baseline
is365964983373611279f0c2e4f14ae7c6587fb135. No product change or new installation is claimed by this plan.

### Q1 — prove and standardize normal Graham request preparation
- [ ] Inspect/reuse src/app/editorial_handoff.py, src/app/api.py, src/app/codex_trial.py,
  scripts/linkedin_codex_trial.py and existing consumer fixtures. Existing strict version1 handoff supports
  literal/symbolic narratives,1–8 beats and1–2 load-bearing facts. Do not invent another engine/schema.
- [ ] Add reproducing tests in tests/test_graham_structure.py before implementation. Cases: documented
  five-part default, explicit alternate narrative preserved, missing meaning/evidence rejected before calls,
  unsupported persona rejected in Graham preparation, and same input produces byte-identical prepared data.
- [ ] Add minimal reusable src/app/editorial_structure.py: prepare_graham_request(data:dict,bundle:dict)
  returns prepared_request, prepared_bundle. Input must explicitly supply editorial_handoff.meaning
  (thesis, reader_consequence,1–2 sourced facts,qualification); do not infer claims/credentials from a voice.
  If narrative is absent, supply literal five semantic beats matching the adopted scaffold; if present,
  validate/preserve it exactly and mark provenance caller-selected. No finished hook/copy in the outline.
  Reuse freeze_handoff/validate_handoff and validate_trial_evidence; reject unsupported facts/source IDs.
- [ ] Expose this no-model preparation as prepare in the existing scripts/linkedin_codex_trial.py command.
  Reuse --request/--evidence-bundle/--out; write request.json and source-bundle.json in the preparation
  directory without creating a running trial or constructing a provider. Reject conflicting existing output;
  identical preparation reopens without writes/calls. Preserve full source records and recompute request_sha256
  only after compilation. Bind structure id graham-structured-v1, version1, definition/input hashes and voice
  selection in source-bundle metadata retained by the existing request/bundle fingerprint and saved result.
- [ ] Enforce the qualification boundary in normal Graham CLI generate: for every NEW execution,
  require and validate prepared structure id/version/definition hash, input hash and request/bundle
  binding before constructing/invoking the model provider. Missing binding raises
  STRUCTURE_PREPARATION_REQUIRED with the prepare action; stale/inconsistent binding fails closed.
  The normal Graham command must not silently run the legacy unstructured path. Other-persona and
  direct-API legacy callers are outside this Graham-only qualification, not implicitly upgraded.
  For an exact already-completed request, reconcile the saved immutable fingerprint/result first and
  return its original receipt without calls or relabeling; show remains an unchanged historical read.
  A changed same-ID request conflicts0 calls. Never require regeneration of old completed results.
  Hash canonical semantic inputs/source data excluding the binding fields themselves to avoid a
  self-referential hash; keep exact definition hashes/version pinned for new execution validation.
- [ ] Add subprocess no-call negatives for absent preparation metadata, changed beat/definition hash,
  stale version and mismatched request/bundle. Prove these cannot reach provider dispatch. Also prove
  historical show/exact completed replay remains0 calls after active structure version changes.
- [ ] Prove subprocess prepare→normal generate consumer propagation with injected model boundary:
  selected structure/meaning/limits reach actual writer, guarded rewrite, evaluator and equal-context control.
  Changing a selected beat must change the actual prompt; malformed or changed facts must stop before calls.
Expected: normal installed Graham workflow requires validated prepare→generate for new executions,
independent of this chat/evidence helper; missing/stale preparation can never silently bypass structure.
No implicit rewrite of explicit alternate narratives. Direct API/UI parity remains an unproved later scope.
If existing code already meets an item with proof, reuse it; do not add duplicate abstractions.

### Q2 — evaluate voice and construction without a new score gate
- [ ] Extend the existing argument_voice essential definition/prompt in src/app/publish_quality.py to
  require both selected voice fidelity and coherent development of the selected narrative. Keep exactly
  four essential IDs and advisory scores; no fifth gate or numeric structure cutoff. Reasons must identify
  actual voice/construction strengths or defects, not mandatory heading/keyword counts.
- [ ] Add tests in tests/test_editorial_handoff.py and tests/test_essential_review_gate.py: identical factual
  content but disordered/repetitive argument is not admitted when the injected essential says revise;
  strong voice/high score cannot compensate; corrected evaluation can admit a supported rewrite;
  at most one targeted rewrite; unavailable evaluation/missing support still fail closed.
- [ ] Preserve Version1 and chat72946 as separate exact-hash feedback records. Neither reference text
  is automatically injected as an approved voice example or used as a copied expected output. The new
  claim is coherent construction, not reproducing those exact words. A qualitative human comparison is
  required for writing success; a fixture proves control flow only.
Expected: selected structure reaches the real review and revision path, with separate voice/construction
findings within the existing essential. No extra default model stage; optional planning calls, if used,
consume the same budget. Do not turn every beat into a paragraph or force a CTA/checklist.

### Q3 — local qualification and fresh post-implementation challenge
- [ ] Run affected regressions RED→GREEN, then .venv/bin/python -m pytest -q and a clean archive at the
  exact candidate; record commands/exits/source/config/test/script hashes and actual lint availability.
  Reuse unrelated historical proofs; product changes invalidate the affected251-test receipt.
- [ ] Challenge the actual changed persistence/provider boundary under Gate §2.1, Parts E/H as relevant:
  same request+same template reopens0 calls; changed template/bundle under same ID conflicts0 calls;
  process interruption after native dispatch stays unknown/reconciles original attempt; it never blindly
  retries. Evidence content cannot smuggle finished copy/unsupported claims past preparation.
- [ ] Obtain independent whole-candidate review; fix material findings and freshly review the corrected
  candidate. Inspect workflow triggers. Existing approval permits focused hosted CI when applicable after
  local pass; current repository has no active workflow. Record NOT_APPLICABLE with reason rather than
  activating historical commented pipelines solely for ceremony or claiming a hosted pass.
Expected: one reviewed candidate ready for technical release, separately from editorial acceptance.

### Q4 — merge and install exact qualified bytes (M2)
- [ ] Reuse recorded continued merge/install/testing authority; no repeat permission request. Refresh
  exact candidate/base/main/reviews and original merge results; revalidate currentness before consequence.
- [ ] Merge only the verified head and use existing fixed-release worktree/launcher procedure. Retain
  previous2c2daf3 installation and exact rollback command; do not patch live files. Verify installed prepare
  command, imported module paths and source/config/script hashes, subscription auth/client binding,
  installed suite and historical result reopening0 calls. Record tested/main/installed identities separately.
- [ ] If no product/script/config bytes changed, verify/reuse the existing installation and record why
  reinstall is unnecessary; documentation-only main advancement never creates an installation gap.
Expected: the installed command actually contains the qualified preparation/review path and usable rollback.
Technical install GO is not approval of the new post or the complete26/11 product.

### Q5 — one installed structured package and direct control (M3/M4)
- [ ] Start with the retained AI black-box idea, Graham individual POV, concise_challenger v2 voice and
  the adopted literal progression. Reuse three primary research records, rechecking material currentness
  as needed. Select1–2 load-bearing facts for the strict handoff; preserve remaining source qualifications
  as context, not unsupported extra claims. Keep incomplete understanding distinct from total ignorance.
- [ ] Freeze reader, intended decision/question, meaning, sources/limits, chosen structure/voice and
  review questions. Prepare using the installed public command, then normal installed generate with mandatory preparation validation. Do not
  invoke the evidence-only diagnostic harness or manually edit outputs to manufacture a successful post.
- [ ] Before any invocation declare one shared cap12 subscription executions/900 cumulative active CLI
  seconds/API0, including preflight, draft, review, optional guarded rewrite/planning, visual and control.
  Save actual prompts/raw results/attempt IDs/usage or UNKNOWN; no blind retries, paid fallback or cap reset.
- [ ] Keep normal four-essential admission, selected/visual exact hash identity and same-context control.
  Record valid HOLD without forcing a pass; use existing comparison-only continuation only after known
  NO_QUALIFIED_CANDIDATE and within the original shared budget. Never render an unqualified candidate.
- [ ] Fresh-process show/export/repeated identical request must preserve exact prepared/selected/source/
  voice/structure bytes and0 added calls. Changed meaning/structure/evidence under the same ID conflicts
  before launch. New policy/structure runs get new identities; older policy/results remain immutable.
- [ ] Present blind engine/control texts; record real Graham judgments of factual limits, voice and
  construction separately, keep/light/structural/reject, usefulness and actual editing effort. Ask only for
  missing judgments; already recorded feedback is retained. Model scores/review never substitute for this.
Expected: real installed review package or precise nonterminal failure, with no claim of accepted prose
until human disposition. This is the next meaningful operator milestone; stop here for missing judgment.

### Q6 — transfer, bounded acceptance and closure (M5)
- [ ] After initial human disposition, test useful delivery traits on one genuinely different concept,
  using the same path and another separately declared12/900/API0 cap. A retained candidate is AI time to
  usable completion (existing Stanford/METR evidence, including its limits); confirm genuine distinctness
  and historical eligibility before launch. Repeated variants do not create new subjects. Do not exceed
  the existing8-subject envelope; unresolved eligibility stays unresolved and does not silently expand it.
- [ ] Keep first-six history,>=5 genuine subjects,>=4/6 keep/light,>=2 live-provider human-accepted
  subjects and six-pair control/voice/claim/visual/edit-effort requirements. A two-concept slice does not
  close these gates; fewer eligible observations remain NOT_YET_EVALUABLE. Later P3–P7 stays in its roadmap.
- [ ] At each material update and before handoff/closure, rerun the retained-information inventory and
  semantic complete-pair challenge. Save covered/total for the enumerated source set, exact candidate
  hashes, omissions and proof limits. A missing-item/altered-byte negative control must fail. Mechanical
  coverage does not establish semantic completeness or implementation success.
Expected: scope-limited installed workflow qualification, or explicit next owner checkpoint. Preserve all
unproved26 AT/11 E2E, UI/direct-API parity, rendered assets, public publishing and six-subject acceptance.

## Structure slice authority, recovery and terminal rule
Recorded operator approval covers merges, installation and applicable hosted CI/testing after local pass.
The planning request does not itself execute Q1–Q6. This corrected plan/prompt is ready for a subsequent
execution instruction once its scoped Challenge and information retention are clear. Existing essential
checks, API0, budget, human editorial/render/publish gates and privacy boundaries remain. Use directly
callable routes first, exact selectors, original receipt lookup for unknown effects, Paths diagnostics on
real failure and independently verified target readback. Never infer authority or global outage from lookup.
Q5 is technical completion with human review pending, not overall product acceptance. Final editorial
reliability requires actual human-supported transfer and retained later acceptance obligations. At a
machine-solvable blocker continue legitimate independent work; stop only at a precise budget, judgment,
external or owner gate. Preserve rollback and active work; never reset the project to Stage0.

## Ordered remaining work
Use the existing engine, launcher, saved results and receipts. Do not rerun completed research,
eight workflows or nine voices merely to restart this sequence.

### M1 — review and qualify the coherent release candidate
1. Refresh Paths via connected GitHub, current packet, candidate/base/main, relevant PRs and installed launcher.
   Resume from the first unmet milestone. If the candidate is already merged/promoted, verify its receipt
   and advance; do not reset branches, reinstall or regenerate merely because this plan names an older checkpoint.
2. Review the complete pending diff against current main, including earlier unmerged audit documentation.
   Resolve concrete integration defects with reproducing regressions; do not weaken assertions.
3. Reuse251-test/clean-archive receipts if source/config/tests hashes still match. If code changes,
   run focused regressions and the full local suite; save exact command, exit, tested revision and hashes.
   Ruff was unavailable in the previous venv: record actual lint availability/results, never claim lint passed.
4. Verify strong80 can advance,90+ cannot compensate for failed essentials, missing support pauses,
   malformed evaluation fails closed, at most one targeted rewrite, unsafe rewrite preserves A,
   selected/visual bytes match, baseline context matches, and old results reopen without calls.
5. Record GO/HOLD/FAIL for candidate readiness separately from merge and installation.
Expected: one coherent reviewed and tested candidate, with preserved source and historical outputs.
Proof: reviewed diff, regression/full-suite logs, clean archive, source/config/test hashes.
Maps: AT01/02/03/06/07/08/14/15/16/18/26; only mode-specific coverage may be marked passed.

### M2 — merge and promote through the existing release setup
1. Resolve current owner admission for merge/promotion; earlier release authorization is not unlimited authority.
   Inspect automatic workflow triggers before opening/updating a PR or merging. Recorded operator approval
   permits applicable focused hosted CI after local pass. Do not request that authority again. Never disable
   checks or activate an unrelated legacy workflow merely to obtain a hosted run.
2. When admitted, merge the exact verified candidate; record main/merge SHA and reviewed head.
3. Install from the merged revision through the existing fixed-release launcher procedure.
   Preserve the previous release and exact rollback command; do not edit the live installation in place.
4. Verify launcher target, imported module paths, installed source/config hashes, subscription client/auth binding,
   relevant smoke/full installed tests, and reopening a historical completed result with zero added calls.
Expected: exact merged revision is actually running; rollback remains usable.
Proof: merge receipt, installation/rollback receipt, import/hash/readiness/reopen logs.
HOLD if unmerged, wrong installed bytes, uncertain effect or missing admission. Local tests alone cannot close M2.

### M3 — one complete installed acceptance package
1. Use the current Q5 Graham-only AI black-box brief, concise_challenger v2 and selected literal scaffold,
   with at least two independent reputable origins. The older security/symbolic package is historical and
   must not be regenerated or offered as the current editorial target. Preserve its original evidence.
2. Freeze six building blocks: reader, decision, concept/argument, evidence and limits,
   narrative plus verified voice, review questions. Separate fact/observation/inference/opinion.
   Recheck source currentness and material conflicts when needed; do not add unnecessary research.
3. Declare one shared batch budget before launch: at most12 subscription Codex model executions and900
   cumulative CLI seconds, including preflight, draft, evaluation, optional rewrite, visual plan and control.
   Save actual tokens/attempts/launches/time; missing IDs are unavailable, never invented.
4. Run normal installed evidence admission → drafting → four-essential evaluation → at most one guarded
   defect-driven rewrite → exact candidate selection → visual companion planning only if qualified.
   Missing evidence or failed qualification is a valid recorded HOLD; do not force a passing package.
5. Produce the simpler direct-prompt control with identical evidence, author, audience, meaning, voice
   and narrative. Use the same evaluator/context if reporting model assessments.
   If the engine records NO_QUALIFIED_CANDIDATE, retain that HOLD and use its existing comparison-only
   continuation when the budget permits. Never promote the retained unqualified engine text to a selected
   candidate or spend its visual call. If the control cannot run, record NOT_RUN with the reason.
6. Save exact prompts/raw outputs, stage order/handoffs, IDs, code/voice/source bindings and hashes.
   Reopen the completed result in a new process: exact content and zero additional calls.
   Keep result policy/version immutable. A new policy run uses a new run/attempt identity; do not overwrite old results.
7. Shuffle the engine/control texts before human review; keep method mapping separate.
Expected: traceable installed review package, or a precise truthful reason it cannot qualify one.
Proof: installed invocation, saved package/control, visual plan or deferral, receipts and zero-call reopen.
Different word counts do not count against either candidate.
Maps: AT01/02/03/05/06/14/15/16/18/21/25/26 and applicable E2E01/06/10 components.
A single pair does not complete six-subject acceptance.

### M4 — human judgment and calibration
1. Present the shuffled pair with factual support and ask Graham for accuracy, audience usefulness,
   recognizable voice, keep/light/structural/reject, preference/tie and actual editing effort.
   Bind answers to exact candidate hashes. Do not turn general praise into approval or approved voice examples.
2. Use8–12 retained exact-text examples for initial evaluator calibration when available, with a held-out subset.
   Freeze the holdout before adjusting prompts/rubrics and separate it by subject, not draft variant,
   to prevent the same underlying example leaking into both sets.
   Draft variants are calibration examples, not additional independent subjects. Reuse labels already supplied;
   do not require a new broad generation batch just to obtain calibration material.
3. Record false accept/reject cases against human labels and inspect concrete causes. Keep scores advisory.
   Do not introduce another numeric gate without evidence and explicit adoption.
Expected: real labels and editing evidence; unresolved judgments remain pending.
Proof: hash-bound reviewer records, edits/timing where observed, calibration findings and held-out result.
Maps: AT04/05/19/20/21/23/24; no model verdict substitutes for these human requirements.

### M5 — finish P2 in small batches, then follow P3–P7
1. After initial human disposition, expand only in admitted small batches toward six eligible distinct subjects
   within the existing default envelope of at most8 subject trials. Reconcile the existing subject ledger
   and owner-approved eligibility/order before adding subjects; do not reset first-six history after a repair.
   If historical eligibility is ambiguous, retain it as unresolved rather than silently excluding or counting it.
   Do not force thin subjects or cherry-pick failures.
2. Preserve >=5 genuine subjects, >=4/6 keep/light, >=2 live-provider human-accepted subjects;
   evaluate the first-six fraction only when six eligible subjects exist.
3. Complete blinded six-pair engine/control pilot: >=4/6 engine preference, ties not wins; record factual errors
   and actual editing effort. Fewer subjects means NOT_YET_EVALUABLE. This is not statistical proof of impact.
4. Review six-post voice/originality, claim support and useful single-image/carousel/ambiguous visual choices.
   Human visual-plan approval is distinct from approval of rendered assets.
5. Test any proposed winning hybrid on a second concept before declaring a winner. Historical trials remain
   exploratory; do not expand nine voices before useful small-comparison differentiation is established.
6. Resume existing P3–P7 dependencies only as prerequisites and authorizations permit:
   durable headless recovery/exports; human-authorized voice management; lightweight UI/parity/security;
   actual image/carousel rendering and mobile inspection; Dedication-owned approval/publishing integration.
   Keep all unproved AT/E2E entries open, including edit invalidation and external publishing verification.
Expected: complete acceptance evidence, or an explicit bounded HOLD with the missing proof.
Proof: subject ledger, blind reviews/effort, claims, voice/visual records and original AT/E2E receipts.

## Milestone closure and authority
After each meaningful milestone record:
- candidate/base/main/PR state; tested revision and hashes; commands/exits and observed outcomes;
- actual installed revision/imports; rollback binding; no-call reopening where relevant;
- declared/observed resource use, exact IDs or unavailable, human decisions still pending;
- GO/HOLD/FAIL, remaining blockers and next eligible action.

Update CURRENT_WORK_PACKET.md, this plan and the execution prompt together; keep detailed results in
one reproducible evidence packet and link its receipt. The execution prompt routes work; this plan owns
sequence; the acceptance document owns detailed criteria. Preserve historical outcomes instead of
appending competing “current” instructions. Documentation-only changes may reuse matching code tests.
Provider-neutral visual planning is included in M3; image generation/rendering is a separately gated effect.
No paid API/fallback, hosted CI, merge/promotion beyond admitted scope, deployment, rendering or publishing
is granted by this document. Dedication owns canonical approval, scheduling and publication.
