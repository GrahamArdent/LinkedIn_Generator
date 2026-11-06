# LinkedIn Generator — completion game plan
Updated November 5, 2026. Current authority pointer: CURRENT_WORK_PACKET.md (repository root).
Execution entry: LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md.
Broader P0–P7 roadmap: LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md.
Detailed acceptance definitions remain solely in LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md.

## Current checkpoint

| Concern | Observed state |
|---|---|
| Active scope | Graham-only Q1–Q4 complete; Q5 machine package complete, actual human judgment first unmet |
| Installed product |5bd3478709d98e5eb3ff5fd11168718aa3868cbd;275 installed tests; previous2c2daf3 rollback |
| Current technical proof | evidence/structure-install-implementation-20261105/{QUALIFICATION,INSTALLATION,RESULTS}.json;275 local/archive/installed tests and actual installed package; earlier receipts historical for unchanged bytes |
| Editorial feedback | Version1 voice preferred, construction rejected; structured chat72946 positively reviewed; installed structured pair now awaits actual Graham judgment |
| Scope/research/references | GRAHAM_CONTENT_DIRECTION_2026-11-05.md and evidence/graham-black-box-voices-20261105/STRUCTURE_FEEDBACK.json |
| Prior Challenge | evidence/structure-install-challenge-20261105/CONVERGENCE.md cleared its exact earlier pair for planning; later edits require current review |
| Current pair audit | evidence/prompt-plan-hardening-20261105/RESULTS.json; not a new implementation/release proof |
| Remaining product acceptance | All26 AT/11 E2E retained; first-six eligibility and human/native/render/publish proofs remain scoped/pending |

## One owner per concern
- GRAHAM_CONTENT_DIRECTION_2026-11-05.md owns editorial intent, the scaffold and recorded feedback.
- This completion game plan alone owns product steps Q1–Q6, dependencies, budgets, tests, release
  sequence, stop conditions and technical/editorial completion boundaries. It remains within M1–M5.
- LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md owns execution mechanics: discovery,
  bounded autonomous continuation, receipt recovery, safe handoff and final reporting. It points here
  instead of maintaining a second product checklist.
- The acceptance document alone defines detailed AT/E2E success criteria; the broader P0–P7 roadmap
  owns later dependencies. Referenced criteria remain binding without duplicating all their text here.
- CURRENT_WORK_PACKET.md is a derived resume pointer to the first unmet Q step and evidence.
  It cannot override the plan, accepted user decisions or current factual runtime state.
- Audit/Challenge receipts certify their exact reviewed snapshots, not later changes. Historical
  security/style diagnostics remain immutable evidence, not the current generation target.

## Active structure-to-install slice — first unmet Q step

This is the current bounded work inside the existing M1–M5 spine, not another master plan.
Goal: make the Graham workflow deliberately prepare structure, carry it through actual writing/review,
and run from a verified fixed release. “Reliable” means repeatable preparation, traceable execution,
coherent reviewed output and safe read/recovery behavior; deterministic prose is not promised.
Spec: GRAHAM_CONTENT_DIRECTION_2026-11-05.md, especially Adopted structure and workflow.
Historical planning baseline2c2daf3/251 tests applies only to its unchanged bytes. Planning source baseline
was365964983373611279f0c2e4f14ae7c6587fb135. Current source/runtime outcomes are in the checkpoint and installation evidence above.

### Q1 — prove and standardize normal Graham request preparation
- [x] Inspect/reuse src/app/editorial_handoff.py, src/app/api.py, src/app/codex_trial.py,
  scripts/linkedin_codex_trial.py and existing consumer fixtures. Existing strict version1 handoff supports
  literal/symbolic narratives,1–8 beats and1–2 load-bearing facts. Do not invent another engine/schema.
- [x] Add reproducing tests in tests/test_graham_structure.py before implementation. Cases: documented
  five-part default, explicit alternate narrative preserved, missing meaning/evidence rejected before calls,
  unsupported persona rejected in Graham preparation, and same input produces byte-identical prepared data.
- [x] Add minimal reusable src/app/editorial_structure.py: prepare_graham_request(data:dict,bundle:dict)
  returns prepared_request, prepared_bundle. Input must explicitly supply editorial_handoff.meaning
  (thesis, reader_consequence,1–2 sourced facts,qualification); do not infer claims/credentials from a voice.
  If narrative is absent, supply literal five semantic beats matching the adopted scaffold; if present,
  validate/preserve it exactly and mark provenance caller-selected. No finished hook/copy in the outline.
  Reuse freeze_handoff/validate_handoff and validate_trial_evidence; reject unsupported facts/source IDs.
- [x] Expose this no-model preparation as prepare in the existing scripts/linkedin_codex_trial.py command.
  Reuse --request/--evidence-bundle/--out; write request.json and source-bundle.json in the preparation
  directory without creating a running trial or constructing a provider. Reject conflicting existing output;
  identical preparation reopens without writes/calls. Preserve full source records and recompute request_sha256
  only after compilation. Bind structure id graham-structured-v1, version1, definition/input hashes and voice
  selection in source-bundle metadata retained by the existing request/bundle fingerprint and saved result.
- [x] Enforce the qualification boundary in normal Graham CLI generate: for every NEW execution,
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
- [x] Add subprocess no-call negatives for absent preparation metadata, changed beat/definition hash,
  stale version and mismatched request/bundle. Prove these cannot reach provider dispatch. Also prove
  historical show/exact completed replay remains0 calls after active structure version changes.
- [x] Prove subprocess prepare→normal generate consumer propagation with injected model boundary:
  selected structure/meaning/limits reach actual writer, guarded rewrite, evaluator and equal-context control.
  Changing a selected beat must change the actual prompt; malformed or changed facts must stop before calls.
Expected: normal installed Graham workflow requires validated prepare→generate for new executions,
independent of this chat/evidence helper; missing/stale preparation can never silently bypass structure.
No implicit rewrite of explicit alternate narratives. Direct API/UI parity remains an unproved later scope.
If existing code already meets an item with proof, reuse it; do not add duplicate abstractions.

### Q2 — evaluate voice and construction without a new score gate
- [x] Extend the existing argument_voice essential definition/prompt in src/app/publish_quality.py to
  require both selected voice fidelity and coherent development of the selected narrative. Keep exactly
  four essential IDs and advisory scores; no fifth gate or numeric structure cutoff. Reasons must identify
  actual voice/construction strengths or defects, not mandatory heading/keyword counts.
- [x] Add tests in tests/test_editorial_handoff.py and tests/test_essential_review_gate.py: identical factual
  content but disordered/repetitive argument is not admitted when the injected essential says revise;
  strong voice/high score cannot compensate; corrected evaluation can admit a supported rewrite;
  at most one targeted rewrite; unavailable evaluation/missing support still fail closed.
- [x] Preserve Version1 and chat72946 as separate exact-hash feedback records. Neither reference text
  is automatically injected as an approved voice example or used as a copied expected output. The new
  claim is coherent construction, not reproducing those exact words. A qualitative human comparison is
  required for writing success; a fixture proves control flow only.
Expected: selected structure reaches the real review and revision path, with separate voice/construction
findings within the existing essential. No extra default model stage; optional planning calls, if used,
consume the same budget. Do not turn every beat into a paragraph or force a CTA/checklist.

### Q3 — local qualification and fresh post-implementation challenge
- [x] Run affected regressions RED→GREEN, then .venv/bin/python -m pytest -q and a clean archive at the
  exact candidate; record commands/exits/source/config/test/script hashes and actual lint availability.
  Reuse unrelated historical proofs; product changes invalidate the affected251-test receipt.
- [x] Challenge the actual changed persistence/provider boundary under Gate §2.1, Parts E/H as relevant:
  same request+same template reopens0 calls; changed template/bundle under same ID conflicts0 calls;
  process interruption after native dispatch stays unknown/reconciles original attempt; it never blindly
  retries. Evidence content cannot smuggle finished copy/unsupported claims past preparation.
- [x] Obtain independent whole-candidate review; fix material findings and freshly review the corrected
  candidate. Inspect workflow triggers. Existing approval permits focused hosted CI when applicable after
  local pass; current repository has no active workflow. Record NOT_APPLICABLE with reason rather than
  activating historical commented pipelines solely for ceremony or claiming a hosted pass.
Expected: one reviewed candidate ready for technical release, separately from editorial acceptance.

### Q4 — merge and install exact qualified bytes (M2)
- [x] Reuse recorded continued merge/install/testing authority; no repeat permission request. Refresh
  exact candidate/base/main/reviews and original merge results; revalidate currentness before consequence.
- [x] Merge only the verified head and use existing fixed-release worktree/launcher procedure. Retain
  previous2c2daf3 installation and exact rollback command; do not patch live files. Verify installed prepare
  command, imported module paths and source/config/script hashes, subscription auth/client binding,
  installed suite and historical result reopening0 calls. Record tested/main/installed identities separately.
- [x] If no product/script/config bytes changed, verify/reuse the existing installation and record why
  reinstall is unnecessary; documentation-only main advancement never creates an installation gap.
Expected: the installed command actually contains the qualified preparation/review path and usable rollback.
Technical install GO is not approval of the new post or the complete26/11 product.

### Q5 — one installed structured package and direct control (M3/M4)
- [x] Start with the retained AI black-box idea, Graham individual POV, concise_challenger v2 voice and
  the adopted literal progression. Reuse three primary research records, rechecking material currentness
  as needed. Select1–2 load-bearing facts for the strict handoff; preserve remaining source qualifications
  as context, not unsupported extra claims. Keep incomplete understanding distinct from total ignorance.
- [x] Freeze reader, intended decision/question, meaning, sources/limits, chosen structure/voice and
  review questions. Prepare using the installed public command, then normal installed generate with mandatory preparation validation. Do not
  invoke the evidence-only diagnostic harness or manually edit outputs to manufacture a successful post.
- [x] Before any invocation declare one shared cap12 subscription executions/900 cumulative active CLI
  seconds/API0, including preflight, draft, review, optional guarded rewrite/planning, visual and control.
  Save actual prompts/raw results/attempt IDs/usage or UNKNOWN; no blind retries, paid fallback or cap reset.
- [x] Keep normal four-essential admission, selected/visual exact hash identity and same-context control.
  Record valid HOLD without forcing a pass; use existing comparison-only continuation only after known
  NO_QUALIFIED_CANDIDATE and within the original shared budget. Never render an unqualified candidate.
- [x] Fresh-process show/export/repeated identical request must preserve exact prepared/selected/source/
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
The planning request does not itself execute Q1–Q6. The subsequent user execution instruction is now
active; its completed proof and exact Q5 human checkpoint are in evidence/structure-install-implementation-20261105/RESULTS.json. Existing essential
checks, API0, budget, human editorial/render/publish gates and privacy boundaries remain. Use directly
callable routes first, exact selectors, original receipt lookup for unknown effects, Paths diagnostics on
real failure and independently verified target readback. Never infer authority or global outage from lookup.
Q5 is technical completion with human review pending, not overall product acceptance. Final editorial
reliability requires actual human-supported transfer and retained later acceptance obligations. At a
machine-solvable blocker continue legitimate independent work; stop only at a precise budget, judgment,
external or owner gate. Preserve rollback and active work; never reset the project to Stage0.

## M1–M5 and later roadmap mapping

This mapping replaces the older repeated task lists. Execute Q1–Q6 in dependency order; do not run
another parallel M checklist or restart completed work.

| Existing milestone | Active owning steps |
|---|---|
| M1 coherent source qualification | Q1–Q3 |
| M2 release/promotion | Q4, only if installed product/script/config bytes change |
| M3 installed acceptance package | Q5 |
| M4 human judgment/calibration | Q5 human review plus retained calibration below |
| M5 bounded P2 completion, then P3–P7 | Q6 and the existing broader roadmap |

## Retained acceptance beyond the first installed package

The acceptance document remains the sole detailed26-AT/11-E2E authority. In particular retain:
- At least5 genuine subjects and4 of first6 eligible drafts kept/light-edited; at least2 distinct live-provider
  human-accepted subjects; default envelope at most8 subject trials. Do not reset eligibility after repairs.
- Six equal-input blind engine/control pairs, engine preferred on at least4/6; ties are not wins. Record
  factual errors, substantive usefulness and actual editing burden. Fewer eligible pairs is NOT_YET_EVALUABLE;
  the pilot does not establish engagement/business impact or statistical superiority.
- Human voice/insight/usefulness and claim support, six-post semantic originality, useful single-image/
  carousel/ambiguous format decisions, actual effort, calibrated review and cost/latency evidence.
- Use8–12 retained exact-text examples for calibration when available. Freeze holdout by underlying
  subject before rubric changes; draft variants are not independent subjects. Reuse existing labels, leave
  missing labels pending, preserve old results, inspect false accepts/rejects, and never add a numeric gate
  from advisory model ratings or generate a broad batch solely to fill calibration counts.
- Any winning hybrid must transfer to a different concept before being called a winner. Avoid nine-style
  expansion without useful small-comparison differentiation. The liked chat text is not an active voice
  example, native result, numerical label or publication approval merely because it was praised.
- Later P3–P7: durable headless exports/recovery, authorized versioned voice examples, lightweight UI/
  headless parity and isolation, material-edit invalidation, real rendered image/carousel mobile inspection,
  Dedication-owned canonical approval/scheduling/publication, duplicate/unknown handling and independently
  verified external publication. Plan approval alone closes none of these.

## Milestone evidence and continuation

At each meaningful boundary record one owner evidence pointer: exact candidate/base/main/PR and
source/config/test/script hashes, commands/exits, expected versus observed outcome, imported/runtime
revision and rollback, original run/attempt/candidate/voice/structure/source bindings, resource usage or
UNKNOWN, human judgments or PENDING, retained unknown effects and the first unmet Q step.

Use current tools and actual owner admission through the companion execution prompt. Reuse still-valid
receipts and classify blockers narrowly. Routine authorized machine waits are not operator gates; accepted
return evidence resumes at the recorded point. A new security/destructive/spending/render/publish effect
still needs its actual admission, not a generic assumption from this plan.

On an unknown native or publication effect, retain the original identity and receipt, reconcile it through
its owner and independently read back the target before retry. Never overwrite earlier results or restart
attempt state to produce green tests. Preserve active work and rollback. No overall success claim from a
local fix, green suite, source merge, technical install or advisory score alone.

Before material handoff/closure, run known-information retention and semantic complete-pair review,
including a missing-item/altered-byte negative control. Scope covered/total to the enumerated source set;
retain omissions and unproved future work. Product/source changes require new affected proof; a new
chat alone does not invalidate unchanged evidence.
