# LinkedIn Generator — Durable Test Objectives and Success Criteria (v4)

> Current owner-adopted correction — November 5, 2026: `essential-checks-v1` replaces numeric90 admission in the current source candidate. All four essentials must pass with reasons: factual integrity, reader relevance, practical value and argument/voice fidelity. Scores are advisory; missing evidence pauses; failed essentials allow at most one guarded targeted rewrite; unavailable evaluation fails closed. Passing means human-review eligibility only. Evidence: `evidence/essential-review-gate-20261105/REPORT.md` and `MILESTONE.json`. Installed release0c099d7 remains on its historical90 policy until separately promoted. This supersedes older90 instructions below for new source runs; historical receipts remain immutable. All26 AT/11 E2E and human/visual/baseline/publishing obligations remain.


**Prepared:** 2026-11-04
**Status:** Current detailed acceptance definitions, adopted by `CURRENT_WORK_PACKET.md` and the M1–M5 completion plan. All 26 AT objectives and 11 E2E scenarios remain required; historical proposed wording below records package provenance, not a pending adoption gate.
**Evidence status:** The objectives below are **planned**. A file containing a test and a previously recorded manual score are not observed executions of these new gates.
**Companions:** [Game Plan](LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md) · [Evidence and Challenge](LINKEDIN_GENERATOR_EVIDENCE_AND_CHALLENGE_V4_2026-11-04.md) · [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md) · [Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) · [Start Here](LINKEDIN_GENERATOR_PACKAGE_README_V4_2026-11-04.md).

## 1. What success actually means

A post is not successful just because Python completed, a model returned JSON, or the model's quality evaluator gave it 90/100. The product must reliably convert a real, supported idea into a post that the human author **would actually publish**, in a recognizable voice, with no invented facts, practical/novel insight, an appropriate visual, and less editing friction than a simpler approach. Operational correctness and editorial usefulness are separately necessary.

### Definition of valid review material

- A **subject** is one genuine distinct idea backed by available real context and evidence. Draft A/B/retries are **one subject**, not multiple votes. Thin subjects may legitimately be skipped and **do not count as eligible drafts**.
- A **light edit** changes wording, clarity, brevity or punctuation without changing the main claim, evidence, argument, audience or structure. An altered argument or factual basis is a **structural edit**.
- **Fixture** evaluation validates control flow only; **live** means the real configured repository provider was invoked and a receipt recorded; **human** means an explicit reviewer decision tied to the exact candidate hash.
- **Publish ready** means permitted for *human editorial review*, not approved to publish. Dedication owns external publication approval and receipt.
- Status vocabulary: `PLANNED`, `NOT_RUN`, `PASS`, `FAIL`, `BLOCKED`, `NOT_YET_EVALUABLE`, `HOLD`. Never fill missing real observations with fixture scores.
- The existing current owner packet requires ≥5 genuine subjects and ≥4 of the *first six drafted* kept/light-edited. Six eligible drafted subjects are required to evaluate that fraction. Its maximum of eight subject trials remains the default envelope; if not enough eligible drafts exist, return `NOT_YET_EVALUABLE` and seek owner disposition, **not a manufactured sixth post**.

## 2. Test objectives: expected outcomes and observable proof

These are the **sole detailed AT-01..AT-26 definitions in the v4 package**. The [Game Plan](LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md) maps phases and work; the [Evidence](LINKEDIN_GENERATOR_EVIDENCE_AND_CHALLENGE_V4_2026-11-04.md) explains why each test exists. Future implementation must produce receipts at the tested commit.

| ID | Phase | Objective | Stimulus | Expected observable result | Required proof |
|---|---|---|---|---|---|
| **AT-01** | P1** | Candidate identity and visual parity** | Fixture A fails reader check (87 advisory), safe B passes (93 advisory), one rewrite** | Both drafts retained; selected B score 93; visual-source SHA256 exactly B bytes; wrong-source plan rejected/deferred; legacy body semantics preserved** | pytest fixture call log; A/B bytes; selected/visual hashes; source SHA |
| **AT-02** | P1** | Do not rewrite or promote unnecessarily** | A passes essentials at80 or92; A fails with unsafe/failed B; missing essential assessment** | Passing A: zero rewrites; unsafe/failed/missing essentials: no selected candidate or final visual plan; no unexplained model calls** | fixture counts, guard reasons, selection and result status |
| **AT-03** | P1/P2** | Evidence opportunity gate** | Thin/missing evidence, skip, needs_more_evidence** | No drafted body or visual; at most one targeted question if clarification is warranted; no draft calls after terminal preflight** | fixture trace + human real-subject review |
| **AT-04** | P2** | Review real, distinct subjects** | At least five genuine subjects; gather six eligible drafts to evaluate first-six** | At least 4/6 eligible subjects kept or lightly edited; no synthetic subjects; Draft B not a second subject; no unsupported factual specificity or unjustified POV in accepted text** | per-subject manifest, edit_scope, reviewer decision and owner Challenge receipt |
| **AT-05** | P2** | Live provider acceptance** | At least two distinct subjects via actual repository provider** | At least two genuinely generated and human-accepted posts, with model/config and redacted provider invocation records; fixture results excluded** | provider mode=live; run/attempt IDs, hashes, human verdicts |
| **AT-06** | P3** | Headless fresh-process persistence** | CLI generate then independent show/export after restart** | Exactly same run/candidate bytes, voice version, sources; zero generation calls on reads** | subprocess logs; saved hashes; provider spy |
| **AT-07** | P3** | Duplicate request control** | Repeat normalized identical request ID; then same ID with modified input** | Identical request returns original stored receipt with zero launches; changed input conflicts with zero launches** | idempotency key/fingerprint, launch counter and error |
| **AT-08** | P3** | Interrupted/unknown effect recovery** | Kill process before result saved or simulate provider response loss** | Unknown or exact recoverable receipt, never falsely completed or blindly re-dispatched** | fault injection trace, restart and launch counters |
| **AT-09** | P4** | Versioned human-authorized voice learning** | Approve one voice example; reject another; activate revision** | Only approved examples eligible, max 3 injected, new runs bind active version/hash, old runs remain immutable** | immutable voice refs, prompt spy and reviewer receipts |
| **AT-10** | P5** | Browser/headless parity** | CLI run opened in browser, voice changed in UI, new CLI run** | Identical run ID/candidate/body/hash/voice version/sources across adapters; reload does not generate** | browser action log, HTTP+CLI output diff, model spy |
| **AT-11** | P6** | Actual, useful rendered visuals** | Approved single-image and 4-8 slide carousel plans** | Physical rendered assets, legible mobile typography, source fidelity, reviewer-approved value and alt text; not JSON plan alone** | image files/checksums, mobile review and provider receipt |
| **AT-12** | P7** | Approval-gated, externally verified publishing** | Stale/duplicate attempts and one independently approved live publish** | No duplicate/unauthorized effect; unknown != published; with separate authorization, one real URL/URN matches exact approved revision and Dedication outcome** | mock negative tests, publisher receipt and independently observed URL |
| **AT-13** | P5/P7** | Edit invalidation** | Material edit after scoring/visual planning/approval** | New candidate/hash; stale score/claims/visual/approval blocked until recheck; old history preserved** | revision trace, stale-rejection test and updated validation |
| **AT-14** | P2** | Non-numeric unsupported-claim detection** | Insert plausible but unsupported qualitative assertion** | Not accepted as fact without source; checked, qualified or removed; regex-only guard insufficient** | claim-by-claim ledger, reviewer factual disposition |
| **AT-15** | P3/P5** | Export exact selected content** | Export B to JSON and Markdown; reopen and materially edit** | Same selected text/hash in all exports; A/B stored separately; stale export blocked after edit** | byte comparison, UTF-8/line break and manifest checks |
| **AT-16** | P0/P3** | Traceable records and actionable errors** | Success, failed provider, corrupt record, unknown attempt** | UTC, request/run/attempt, input and code hashes, mode, exact action, cause code and truthfully labeled status, no secrets** | structured logs/report, exit codes, restart test |
| **AT-17** | P5/P7** | UI isolation and no hidden side effects** | Malicious HTML/link, preview/reopen, remote bind, mock publisher** | Escaped unsafe content; loopback-only by default; no external write on read/preview; publication delegated to admitted path** | browser/HTTP security test and outbound call spies |
| **AT-18** | P4/P5** | Persona privacy and factual isolation** | Switch Graham to Ardent; include private illustrative voice material** | No cross-persona voice leakage; no invented biography or private anecdote; current factual evidence separate from style** | voice/profile prompt snapshots + human inspection |
| **AT-19** | P2** | Publish-worthiness, not just formatting** | Six distinct, natural draft-worthy subjects** | At least 4/6 are kept or need only light edits; each has a reviewer-rated substantive insight and audience usefulness; structural reject counts against gate** | human usefulness rubric, actual final drafts, rejection reasons |
| **AT-20** | P2/P4** | Authentic voice across domains** | Review Graham posts on varied genuine subjects** | Each accepted Graham post receives >=4/5 human voice fit or is revised/rejected; record why, avoid generic confident AI prose** | per-post 1-5 reviewer voice rating, comments, voice/source version |
| **AT-21** | P2** | Factual traceability and source reliability** | For each accepted post enumerate checkable claims, including qualitative ones** | 100% of externally checkable claims supported by relevant current source or clearly qualified/removed; contradictions/staleness flagged** | claim IDs to source IDs, checked_at, human adjudication |
| **AT-22** | P2/P4** | Sequence originality and stylistic non-repetition** | Six-post corpus from varied subjects** | No unexplained recycled hooks, stock metaphors, identical closings or materially duplicated main insights; explicit reviewed exceptions only** | normalized exact-match checks + human semantic repetition verdict |
| **AT-23** | P2** | Value over one simple prompt** | Generate full-engine and plain-prompt drafts for same six eligible subjects with equal facts/context** | Blind paired reviewer prefers full engine on >=4/6; ties do not count as wins; factual safeguards not relaxed; pilot not statistically conclusive** | blinded labels, same-context manifest, per-pair preference and rationale |
| **AT-24** | P2/P3** | Real edit effort and correction reduction** | Time editing both full-engine and baseline drafts; record edit scopes** | Actual none/light/structural/reject, human minutes, revisions; full engine must not increase aggregate correction burden without explicit justification; quantify, do not infer from score** | time/log/evaluation notes, before/after diff, per-method effort totals |
| **AT-25** | P2/P6** | Visual meaning rather than decoration** | Review candidate single-image/carousel briefs, then rendered assets when available** | Reviewer explains how visual adds understanding; reject padded/irrelevant visuals; plans and actual assets scored separately** | format rationale, human value/verdict, image inspection later |
| **AT-26** | P2/P3/P6** | Runtime and model-cost efficiency** | Measure provider calls, latency, token use or billed cost where observable** | Declare caps before paid calls; no invisible/duplicate generation; stage costs/time and error rates within agreed budgets; unknown metrics explicitly UNKNOWN** | actual run/attempt telemetry, spend approvals, provider receipts |

## 3. Composed end-to-end journeys

A combined journey is not a substitute for its internal assertions, and a named test file is not proof that an end-to-end journey happened. Each scenario keeps a real trace from input through visible outputs with mode-specific evidence.

| ID | Phase | Journey | Pass conditions | Covers |
|---|---|---|---|---|
| **E2E-01** | P3** | CLI generate -> saved result -> exit -> new process reopen/export** | Exact selected bytes/hash, evidence/voice, zero provider calls on reads** | AT-01, AT-06, AT-15, AT-16 |
| **E2E-02** | P3** | Duplicate same ID -> modified input conflict -> interrupted attempt -> recovery** | No double launches, unknown effects retained, structured nonzero conflict/errors** | AT-07, AT-08, AT-16 |
| **E2E-03** | P4** | Approve example -> reject another -> version voice -> fresh generate -> reopen old** | Only authorized examples, old binding intact, no persona leakage** | AT-09, AT-18, AT-20 |
| **E2E-04** | P5** | CLI creates post -> browser reviews -> UI changes voice -> new CLI run** | UI/CLI parity and zero read-time generation; new voice bound to new run only** | AT-10, AT-17 |
| **E2E-05** | P5** | Score/visual accepted -> edit text -> reopen and export** | Stale acceptance/visual/handoff blocked; new candidate verified; old history remains** | AT-13, AT-15 |
| **E2E-06** | P2** | Genuine subjects -> real provider -> human text+visual-plan review** | Trial ledger with 6 eligible drafts for 4/6 verdict; >=2 live accepted; claims/voice/visual value reviewed** | AT-03, AT-04, AT-05, AT-14, AT-19, AT-20, AT-21, AT-24, AT-25, AT-26 |
| **E2E-07** | P6** | Accepted plan -> render real image and carousel -> human visual inspection** | Actual bytes, mobile readability, meaning and cost receipts, no unsupported claim** | AT-11, AT-25, AT-26 |
| **E2E-08** | P7** | Editorially accepted revision -> isolated Dedication handoff -> simulated publisher** | Stale/duplicate rejected, timeout unknown, mock never recorded as real publish** | AT-12, AT-13, AT-17 |
| **E2E-09** | P7** | One separately authorized actual LinkedIn publish via Dedication** | One independently verified real post URL/URN, same approved candidate, canonical outcome** | AT-12 |
| **E2E-10** | P2** | Blinded six-pair full-engine vs plain-prompt comparison on equal evidence** | >=4/6 full-engine preference as provisional pilot gate; tie not win; log factual errors and edit effort** | AT-19, AT-21, AT-23, AT-24 |
| **E2E-11** | P2/P4** | Review six-post sequence across domains after voice approval** | Cross-post authenticity >=4/5 on accepted Graham posts, no unexplained reused insights, both voice and substantive value** | AT-19, AT-20, AT-22 |

## 4. Human-review scorecard and outcome gates

Use the included `LINKEDIN_GENERATOR_P2_TRIAL_SCORECARD_V4_2026-11-04.csv` for trial collection. **Do not fill proposed target values as observed results.** Every reviewed candidate has the following fields, recorded against its exact body hash: `subject_id`, `run_id`, `candidate_id/hash`, `voice_version`, `sources`, `claim_refs`, `provider_mode`, `first_six_order`, `decision`, `edit_scope`, `voice_1_to_5`, `specific_insight_1_to_5`, `audience_usefulness_1_to_5`, `claim_disposition`, `format/visual_value`, `edit_minutes`, `model_calls`, `cost`, `latency`, and reviewer/time.

**Rubric:**

- `voice_1_to_5`: 1 = clearly wrong voice, 3 = partially recognizable but requires substantive edits, 4 = convincingly on-voice with at most light edits, 5 = unmistakably natural without imitation or boilerplate. **AT-20 gate:** accepted Graham candidates each rate ≥4; a lower rating triggers edit or reject rather than retroactive relabeling.
- `specific_insight_1_to_5`: 1 = generic truism, 3 = a reasonable but familiar idea, 4 = distinctive grounded point, 5 = original causal or practical insight. Proposed publication-worthy threshold: **≥4** on both insight and usefulness for qualifying keep/light results.
- `audience_usefulness_1_to_5`: 1 = no professional takeaway, 3 = partially useful, 4 = actionable or illuminating, 5 = compelling enough to save/discuss based on a real tradeoff.
- `claim_disposition`: enumerate every externally checkable claim with an evidence source ID and one of `supported`, `qualified`, `removed`, `unresolved`; accepted candidates must have **zero unresolved**. Include qualitative assertions, not just numerical claims.
- `visual_value`: `adds_meaning | neutral | detracts | not_evaluable`; `neutral` does not become a passed AT-25 simply because output is attractive. Single-image and carousel decisions each need an explanation.
- `edit_scope`: `none | light | structural | reject` with saved edit diff and approximate **actual** minutes. Do not claim efficiency from model scoring or number of drafts alone.

**Existing current owner minimum (not revised by this package):** at least five genuine subjects; at least four of the first six eligible drafted subjects kept or lightly edited; ≥2 human-accepted subjects through real repository provider; zero invented factual details in approved candidates; correct visual-format choices; a focused Challenge Gate. See EV-03/EV-19.

**Additional proposed v4 quality gates, requiring reconciliation into owner authority:** six-subject review with all accepted Graham posts voice ≥4/5 and insight/usefulness ≥4/5; claim ledger has zero unresolved items; no unexplained duplicate hook/insight patterns; blinded equal-input comparison with full-engine preferred on ≥4 of 6 eligible pairs (ties are not wins); meaningful edit effort tracked against that baseline; accepted visuals add meaning; model call/latency/cost budgets declared **before** any paid trial. A six-subject comparison is a **pilot smoke gate**, not statistical evidence of higher population engagement or business results.

**Baseline comparison design (AT-23/24):** the plain-prompt model gets the same underlying source facts, subject and audience. It does not receive proprietary voice instructions unavailable in the simple workflow; evaluate *product advantage* and *voice authenticity* separately so an unfair missing-voice comparison is not confused with overall content quality. Use anonymized order, same evaluation rubric, distinct candidate IDs and editing time. Never silently pick the stronger baseline output to rescue the engine's score.

## 5. Test receipt contract and failure semantics

For any `AT-*` or `E2E-*` result labeled PASS, retain: source commit SHA; UTC test/review timestamp; phase; test ID; mode (`fixture|subprocess|browser|live|human|render|publish`); exact input/subject and expected result; exact command or review action; result/exit code; all request/run/attempt/candidate/voice IDs; output hash; evidence/review references; model call count and cost if available; and structured error/unknown disposition. **Missing receipts mean `NOT_RUN` or `BLOCKED`, not PASS.**

- Provider response loss after dispatch is `unknown` until reconciled; no blind retry that risks duplicate paid calls.
- Human edit invalidates approval, scoring, factual disposition and visual plan for the new revision until rechecked, while older immutable evidence remains.
- A fixture test named `test_end_to_end_generation.py` is an **engine integration test**, not a fresh-process, browser, live model, visual rendering or external publication pass.
- No tests in this package were executed against source code. This document records **test specifications**, not test results.

## 6. Historical package reconciliation checklist

The current owner packet and completion plan retain these objectives and gates. This original checklist is historical; budget and consequential effects still require the current admission described in the completion plan.

1. Add AT-19..26 and E2E-10..11 as acceptance policy to the current live work packet without rewriting the existing owner gate or forcing drafts to hit sample counts.
2. Set concrete spending/latency caps for AT-26 **before** provider-bound tests; records may be `UNKNOWN` where a provider exposes no actual usage.
3. Determine whether a 4-of-6 blinded pilot threshold should be an early HOLD gate or evidence for iteration. The v4 recommendation is **HOLD if not achieved**, inspect why, and do not confuse it with statistical or published-impact proof.
4. Record the open V2 architecture PR as a separate proposal, preserve the existing Python contract, and keep Dedication's publishing authority distinct.

## 7. First work chat scope

Start with **P0/QB-00 baseline + conditionally owner-authorized P1/IT-01 selected-candidate correction**. Then continue to P2 and later phases in bounded steps once prerequisites and the necessary human/provider permissions are satisfied. AT-19..26 are defined now but principally **P2 and later**; they are not pre-implemented proof and must not be forced into P0/P1. The P2 scorecard is the next substantive product gate after P1. See [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md).
