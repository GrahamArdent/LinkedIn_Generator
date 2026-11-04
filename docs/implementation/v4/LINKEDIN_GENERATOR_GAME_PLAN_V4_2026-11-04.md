# LinkedIn Generator — Verified-Outcomes Implementation Game Plan (v4)

> **For agentic workers:** Use a bounded test-driven implementation workflow, such as `superpowers:executing-plans` or `superpowers:subagent-driven-development`, task by task. Every unchecked item is **proposed work**, not completed work. No task here independently grants write, merge, deployment, provider-spend, or publishing authorization.

**Status:** Owner-adopted direction; P0/P1 and Codex connection locally qualified; P2 evidence-first repairs fixture-qualified; substantive native trial completed; human writing acceptance HOLD.
**Prepared:** 2026-11-04
**Primary code owner:** `GrahamArdent/LinkedIn_Generator` (`main` observed at `a714d1ef355ade9ca47a52b301ea477bd0c14f34`)
**Present authoritative work packet:** `LIG-CONTENT-VISUAL-ACCEPTANCE-2026-09-01`
**Goal:** One evidence-grounded LinkedIn writing engine, callable headlessly or through a compact **Voices / Create / Review** interface, that preserves user-approved voice, produces reliably reviewable text and visual plans, and later hands off to Dedication for publication.
**Architecture:** Retain the existing Python generation implementation and its typed `LinkedInContentRequest` / `LinkedInContentResult` interface. Add the smallest shared application service for headless and UI use, then a durable local content-artifact store if needed. Do not create a second writing engine, scheduler, or publication authority.
**Tech stack:** Existing Python/Pydantic/pytest/LLM provider boundary. Proposed: a small CLI, local durable records; **FastAPI with server-rendered templates and SQLite are candidate implementation choices at their milestones, not immediate dependencies or pre-approved architectural commitments**.
**Spec/decision basis:** The user-approved *direction* from the current discussion, this plan's **§1 Product contract**, and the live [`README.md`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/README.md) plus [`CURRENT_WORK_PACKET.md`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/CURRENT_WORK_PACKET.md). The current Python/Codex continuation is reconciled in the owner packet; later stack or cutover choices require their own admission.
**Test authority:** [Durable Test Objectives and Success Criteria](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) is the sole detailed definition of **AT-01..AT-26 and E2E-01..E2E-11**. This plan owns **phase sequence, task implementation and gate mapping**. The evidence file owns sources, risks and adjudications; the prompt owns current bounded execution instructions. These supporting documents **do not outrank** the current repository work packet. Actual AT/E2E status is in the packet and execution receipts; the evidence-first continuation preserves actual machine receipts without claiming human/product acceptance.
**Related files:** [Evidence and Challenge](LINKEDIN_GENERATOR_EVIDENCE_AND_CHALLENGE_V4_2026-11-04.md) · [Durable Test Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) · [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md) · [Package Readme](LINKEDIN_GENERATOR_PACKAGE_README_V4_2026-11-04.md)

## 1. Product contract and deliberate non-goals

### One product, two entry points

```text
Manual subject, current evidence, voice choice
                  |
       LinkedInContentRequest
                  |
         shared Python engine
   evidence gate -> draft -> critic/quality -> at most one rewrite
                  |
    explicit selected candidate + original/rewrite history
                  |
       structured single-image/carousel plan
                  |
      retained, reviewable content package
             /                 \
         headless CLI         thin Voices/Create/Review UI
             \                 /
        same IDs, voice versions, selected text, feedback
                  |
             human content review
                  |
 [later, separately admitted] rendering -> Dedication publish approval
                  |
          independently verified external receipt
```

**Product decisions to reconcile (D-01 through D-08):**

| ID | Proposed decision | Effect/limit | Evidence |
|---|---|---|---|
| D-01 | `LinkedIn_Generator` is the **implementation home** for the current Python engine; V2 is preserved as historical source/competing draft, not auto-merged. | Must record an explicit owner disposition before changing architecture; do not close V2 PR #6 by implication. | EV-02, EV-15 |
| D-02 | One typed engine entry; CLI/UI are adapters using exactly the same service. | No separate prompt, persona, quality or fact-check logic in the UI. | EV-04, EV-05 |
| D-03 | Voice **style** and factual/identity **claims** are independent. | Current supplied facts outrank illustrative source material; no inferred biography or private anecdotes. | EV-09, EV-10, EV-11 |
| D-04 | Preserve `90/100` quality threshold and **at most one guarded rewrite**; score is never permission to publish. | Maintain original/rewrite history and independent human review. | EV-03, EV-07 |
| D-05 | A text candidate and its visual plan must share an explicit candidate identity/hash (the visual plan needs an optional compatible hash reference, not just its existing `source_candidate`). | Preserve existing top-level `body` semantics until compatibility is proved. | EV-04, EV-05 |
| D-06 | The generator owns **working content artifacts, voice versions, and editorial feedback**; Dedication owns canonical post/publication state, approval workflow, scheduling, notifications, and external effects. | An editorial `keep` is **not** final publishing authorization. | EV-02, EV-12, EV-16 |
| D-07 | Prove real-subject writing and useful visual planning **before** paying for rendering; renderer first adapter remains subject to current provider evidence. | No arbitrary image API, publishing/OAuth, or old Selenium restoration in early milestones. | EV-03, EV-08, EV-17 |
| D-08 | Initial workflow is single-user/local and headless-first. A minimal browser interface follows; local HTTP framework/store are chosen when requirements are observed. | No premature public SaaS, remote unauthenticated UI, or separate FastAPI service just to run CLI. | EV-02, EV-13, CH-02 |

**Non-goals for the first release:** autonomous publishing; comments/feed crawling; post-performance learning; a generic multi-user SaaS; new LangGraph/FastAPI microservices; restoring the legacy date-driven scheduler; paid image rendering before acceptance; reproducing V2's entire dashboard. Capture good deferred ideas in the existing `IDEA_LEDGER.md`, not this plan's executable scope.

### Global invariants

- The product's existing `CURRENT_WORK_PACKET.md` remains the **single active execution pointer**. This document is a subordinate proposal, not a new Master Game Plan. Reconcile accepted deltas there and preserve its current trials. Acceptance objectives AT-19..26 are proposed additional criteria until owner-reconciled, not an unapproved change to the current trial gate.
- **Evidence first:** verified/source-supported facts or clearly marked opinion; never invent quotes, personal experiences, statistics, or sources. Do not treat the Voice Bible as factual evidence.
- **Voice precedence:** explicit current instruction; user-edited/published approved examples; current request evidence for claims; Graham Spoken Voice for conversational expression; the original Voice Bible-derived profile for rhetorical architecture; legacy defaults only as fallback. Personal and Ardent personas must remain isolated.
- `publish_quality_threshold=90`; preserve Draft A and at most one guarded Draft B. Preserve 4–8 carousel slides and existing visual copy guards. Human review is required. No “high model score = approved” shortcut.
- **No model call on read:** show, list, preview, review, export, page reload, or reopening an existing run must not trigger generation.
- **Idempotency:** same `request_id` + identical normalized input returns the same completed receipt; same `request_id` + changed input returns a conflict. Unknown/interrupted effect is reconciled; never blindly repeat a potentially completed generation or publishing call. A deliberate new version gets a new request/attempt ID.
- Keep real and fixture/simulated provider results distinguishable. Model quality 90/100 is not human approval; require claim-level review, credible voice and useful insight before content acceptance. All test claims require observed execution receipts; historical test files do not constitute a new passing run.
- Recheck `GrahamArdent/paths/CHATGPT.md` from the default branch and current owner contracts at the start of a work session. Follow its JIT recovery on actual route failures. No full registry sweep merely to prove a functioning tool works.

## 2. Critical-path sequence and acceptance dependency map

**Current next work:** P0/P1, the local Codex connection and evidence-first machine repairs have receipts; do not restart them. Phase4 substantive trial is retained and awaits exact-text human disposition. P2 now proceeds through Phase0 checkpoint → Phase1 evidence brief → Phase2 source-specific writing → Phase3 scorer alignment → Phase4 substantive trial in [the current Codex P2 subplan](CODEX_FIRST_TRIAL_GAME_PLAN_2026-11-04.md). These are subphases, not a second product roadmap. Retain the earlier weak trial outputs and all26 AT/11 E2E obligations.

```text
P0 authority/baseline
    |
P1 selected-candidate contract and targeted safety fix
    |
P2 finish existing multi-subject text+visual-plan human/provider trials  <-- CURRENT OWNER MILESTONE
    |
    +--> P3 headless generation + durable output records
              |
              +--> P4 one versioned voice registry
                         |
                         +--> P5 compact UI (Voices/Create/Review)
    |
    +--> [only if human gate clears] P6 rendering adapter and real assets
P2 + P3/P4 + P6 accepted + Dedication owner admission
          --> P7 editorial handoff -> Dedication publishing integration
P5 UI is a parallel usability milestone, **not a mandatory publishing prerequisite**
After actual outcomes exist --> deferred analytics/learning
```

**Correction from v1:** The original M5 trials were placed after persistence, voice generalization and UI. That turned optional infrastructure into a blocker for the **already-active** product-quality milestone. P2 now follows P1. P3–P5 improve usability afterward; they must not retroactively gate P2. P2 also adds blinded simple-prompt comparison, per-post voice and insight judgments, claim mapping, sequence repetition review, actual edit effort, visual value and bounded provider cost. If P2 identifies a decisive text-quality defect, fix it narrowly before scaling interfaces. See CH-01, CH-02, CH-07 in the evidence file.

## 3. Reuse and proposed file responsibility map

| Status | File/surface | Responsibility / action |
|---|---|---|
| Reuse | `src/app/contracts.py` | Existing typed request/result/feedback/visual contracts; add a backwards-compatible **selected-candidate** field, plus an optional visual-plan source-content hash, only when P1 failing tests prove need. |
| Reuse | `src/app/integration.py` | The existing orchestration bridge `generate_content(request)`; choose the same text for review and visual plan, and reject/defer planner output that declares a different source. |
| Reuse | `src/app/api.py`, `generation.py`, `llm.py`, `publish_quality.py` | Existing opportunity, drafting, critique, LLM injection and bounded rewrite; do not rewrite until trials identify a specific deficiency. |
| Reuse | `config/graham_voice_profile.yaml`, `config/graham_spoken_voice.yaml`, `config/personas.yaml` | Approved Graham public architecture and spoken expression, with separate Ardent settings. |
| Reuse as provenance | `LinkedInGenV2/data/Voice_Bible_Graham (1).md`, V2 preservation study | Preserve original voice concepts without unverified identity claims or template copying. |
| Reuse | `src/app/feedback.py` | Convert explicit feedback to approved examples; **no persistence** provided today. |
| Reuse | `src/app/visual_assets.py` | Provider-neutral single-image and 4–8-slide carousel plans, not image rendering. |
| Reference only | `src/app/cli.py`, `ui/`, old schedule/topics/Streamlit | Historical behavior and migration evidence. Do not reactivate legacy date-driven scheduling or call it the new headless path. |
| Proposed after P2 | `src/app/content_service.py`, `src/app/post_cli.py` | One shared use-case service and CLI adapter; exact paths rechecked against checkout before implementation. |
| Proposed after P2 | `src/app/record_store.py` | Local run/voice/feedback artifact persistence; choose atomic files versus SQLite with explicit test-backed decision, not as an automatic prerequisite. |
| Proposed after P3 | `src/app/voice_registry.py` | Versioned voice identities, active versions and reference provenance; same read path for CLI/UI. |
| Proposed at P5 | `src/app/web_app.py`, `src/app/templates/` | If chosen at P5: simple loopback-only FastAPI/Jinja2 interface that calls the same service; no frontend-only generation business logic. |
| Proposed after P2 GO | `src/app/rendering/` | Provider-neutral rendering, deterministic typography and carousel layout; human review retained. |

Every proposed path is a **candidate**, not an existing file. Name collisions or new repo changes require reconciliation, not duplicate modules.

## 4. Bounded tasks, tests, and GO/NO-GO conditions

The execution rhythm for implementation tasks is **one failing focused test → observed expected failure → smallest implementation → focused passing test → affected regressions → source review → durable receipt**. See **§5** for each test's expected outcome, test layer, evidence and stage gate. The explicit end-to-end tests are **not** all due in the first implementation slice. Run `pytest -q` at local convergence and a current-owner-admitted hosted check at coherent release milestones, not a costly hosted run for every tiny edit. Record exact command, exit status, commit and test environment.

### P0 — Resolve ownership and capture a truthful baseline (documentation + read-only first)

**Depends on:** nothing. **Purpose:** no ambiguous competing production authority.

- [x] **P0.1** Read current default-branch Paths guide, primary README/work packet, V2 PR #6, V2 ADR on that open branch, and relevant Dedication owner overview. Capture current heads and file blob SHAs. Identify which claims are static source, accepted owner decision, historical illustration, or unproved runtime assertion. **Evidence:** EV-01/02/03/15/16. Record the test baseline under **QB-00** (§5.4), not as a fictional green status.
- [x] **P0.2** Capture a short decision proposal specifying the single Python engine, shared CLI/UI adapter contract, legacy salvage rules, and Dedication boundary. Compare it to V2's **branch-local** Next.js+Supabase ADR. An authorized owner must accept or alter the decision before architectural repository writes; do not unilaterally merge/close PR #6. **Check:** no two active owners for generation or publishing; no new Master Game Plan.
- [x] **P0.3** On a permitted checkout run `pytest -q`, and focused `tests/test_end_to_end_generation.py`, `test_publish_quality_review.py`, `test_spoken_voice_authority.py`, `test_voice_bible_authority.py`, `test_visual_asset_planning.py`; record Python/dependency versions and exact failures. Code review alone does **not** count as PASS.
- [x] **P0.4** Reconcile the active packet's stale `AUTHORITY_RECONCILED: pending merge` wording if confirmed on default branch, while preserving its existing trial obligations and status. **Evidence:** CH-13.

**P0 GO:** owner architecture disposition is recorded, current working packet remains active, baseline and unknowns have receipts; the QB-00 actual test run/command/exit status is retained even if red (a red baseline is diagnosed, not misreported as ready). **P0 HOLD:** unresolved authorizations or competing architecture semantics. Do not hold read-only work merely because merge is gated.

### P1 — Candidate identity and factual-safety handoff (small code correction)

**Depends on:** P0 owner admission for the scoped fix. **Objective:** protect one selected text/visual pair.

- [x] **P1.1 Test first:** Create `tests/test_selected_candidate.py`. Cases: (i) original score 87/accepted rewrite 93 selects rewrite; (ii) original 92 selects original; (iii) unsafe rewrite or score below 90 selects **none**; (iv) `skipped`/`needs_more_evidence` selects none; (v) visual-planning uses the exact selected text and stores matching candidate identity/hash; (vi) existing `body` semantics remain compatible; (vii) malformed quality payload is not publish-ready. Verify the initial relevant failure occurs and save the first red receipt. Use **AT-01/02/03** and **IT-01** (§5); do not call this a complete headless E2E test.
- [x] **P1.2 Implement:** extend `LinkedInContentResult` with an **optional** typed `selected_candidate` (fields: `candidate_id`, `source` `original|rewrite`, `body`, `score`, `content_sha256`; keep source/rewrite review details). Define `candidate_id` deterministically from source and full content SHA-256 (no run ID is available yet in P1), and add an optional `VisualAssetPlan.source_content_sha256` for exact attachment to that candidate while keeping existing `source_candidate` compatibility. Resolve exactly once in `integration.py`; assign visual provenance **from the selected text** and reject/defer mismatched planner source rather than trusting it. Do **not** overwrite `result.body` or break old consumers until the explicit consumer contract is accepted. For generated drafts without a qualified candidate use `null`.
- [x] **P1.3 Verify:** `pytest -q tests/test_selected_candidate.py tests/test_end_to_end_generation.py tests/test_publish_quality_review.py tests/test_visual_asset_planning.py`, then `pytest -q`; independently inspect diff and record commit and receipt. A digest must be from actual UTF-8 selected content; no invented IDs.

**P1 PASS:** **IT-01** and the P1 rows of **AT-01/02/03** have observed green receipts, with source SHA and unchanged regression results; downstream receives an unambiguous optional selected candidate, original/rewrite remain preserved, visual plan references the same content; unavailable quality never masquerades as ready. **P1 NO-GO:** selected visual and returned approved text can silently differ. **Evidence:** EV-04/05/07/08; challenge CH-03.

### P2 — Finish the existing **current** content + visual-plan acceptance

**Depends on:** P1 if the handoff discrepancy impacts the trial outputs; no UI, database or renderer required. **Purpose:** prove the actual product value before building infrastructure.

- [ ] **P2.1** Choose genuine subjects with grounded facts for Trials #2–#5 in the current packet, covering natural single image, natural carousel, ambiguous format with a justified choice, and (if available) weak evidence requiring skip or one specific question. Assign `trial_id`, evidence/source identifiers, and author POV. Do not manufacture events or use a historical example as proof.
- [ ] **P2.2** Use the existing pipeline and explicit voice authority. For each trial retain original Draft A, optional guarded Draft B (max one), score/rationale, selected candidate/hash, source claims, visual type/brief or deferral, `keep|edit|reject` plus reason codes. **Run fixture and real-provider modes separately and label them.** Record timestamps, request/model/prompt refs, provider errors and human review.
- [ ] **P2.3** When the same substantive defect recurs, repair the **smallest owner rule**, rerun focused regressions and record what changed. Explicitly audit **non-numeric** new claims as well as numbers/URLs/quotes: the existing visual-copy guard is a structural check, not complete factual verification. Do not add multi-agent orchestration or new UI simply to make the output look sophisticated.
- [ ] **P2.4** Accept the milestone **only** using the packet's actual gate: **at least 5 genuine subjects** (use up to 8 when needed to reach diverse evidence), at least **4 of the first 6 distinct genuine drafted subject-level candidates** kept or lightly edited (**do not count Draft B as an additional subject; do not claim this met before 6 eligible drafts exist**), **zero approved fabricated factual specificity**, no unsupported first-person collective framing or unexplained internal jargon, one-rewrite/90 threshold enforcement, useful varied visual briefs, at least **2 human-accepted subjects through the real repository provider**, and a focused owner Challenge Gate `clear`/explicit `conditional` with named residual debt. An accepted visual *plan* is not a rendered visual.

- [ ] **P2.4** Before the real trial series, freeze the [P2 Trial Scorecard](LINKEDIN_GENERATOR_P2_TRIAL_SCORECARD_V4_2026-11-04.csv) schema, reviewer rubrics, candidate hashing, sources/claims review, blind baseline method, and per-provider call/cost/latency budget. Reuse trials already valid under the packet; do **not** fabricate post volume for a denominator.
- [ ] **P2.5** Run **E2E-10** paired basic-prompt comparison and **E2E-11** six-post voice/originality review with the same grounded subject inputs and reviewer-blinded order. Retain source IDs, edit minutes, publication-worthiness and visual usefulness separately from model's 90-point score. If the result is weak, fix the minimum causal issue and repeat *only* affected verification; do not introduce a new writing engine.

**P2 PASS:** actual completed **AT-03/04/05/14/19/20/21/22/23/24/25/26** and **E2E-06/10/11** evidence meet the existing packet's outcome gate plus any **explicitly owner-adopted** additional v4 thresholds. No use of fixture or model-score results as human verdicts. Review [Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) §4 before first human trial. A six-subject baseline comparison is a pilot gate, **not** statistical proof of future LinkedIn engagement. **P2 HOLD:** missing real provider access/human review, insufficient eligible first-six denominator, poor comparative quality or repeat quality failures; continue only legitimate offline subtasks and report exactly what's unproved. **No paid rendering or publishing on P2 HOLD.** Evidence: EV-03/06/07/08/14.

### P3 — Build one durable, genuinely headless entry

**Depends on:** P1 and recorded P2 disposition. Build production-facing P3 after P2 GO; if P2 is blocked solely by human/provider admission, an explicitly authorized **separate fixture-only P3 preparation slice** may proceed, but cannot substitute for P2 acceptance. Only one implementation slice is active at a time.

- [ ] **P3.1** Define `SavedRun` and minimal durable record contract in `src/app/content_service.py` and/or a small contracts module. Include `request_id`, normalized-input fingerprint, new `run_id` and `attempt_id`, source URLs/evidence refs, voice version, provider/model, prompt/config versions, candidate IDs/hashes, visual plan, quality notes, timestamps in UTC, status `pending|running|completed|failed|unknown`, review and error records. Keep secrets out. **Test:** old run opens byte-identically in a new process.
- [ ] **P3.2** Compare the repository's existing output/logging mechanisms with simple atomic JSON/Markdown files and SQLite. Record a one-paragraph storage choice after testing file integrity, safe concurrent CLI/UI reads/writes, recovery and migrations. **Recommendation:** avoid an upfront DB just for the trial artifacts; choose SQLite if the permanent voice/edit/review workflow needs transactions/concurrency. No new canonical Dedication post table.
- [ ] **P3.3** Implement `content_service.generate(request)` and `content_service.get_run(run_id)` with injected model provider for fixtures. A repeated identical completed request returns its saved receipt; a reused ID with changed input is a conflict; a prior `unknown` attempt is inspected before any retry. No automatic LLM call on read, review, preview or export. Tests in proposed `tests/test_content_service.py` and `tests/test_record_store.py` cover duplicates, corruption, interrupted write, unknown provider result, and fresh-process recovery.
- [ ] **P3.4** Introduce an **explicit new CLI**, not date-driven `src/app/cli.py`: proposed `python -m src.app.post_cli generate --request request.json --json`, `show --run-id X`, `review --run-id X`. Voice registry commands (`voices list/show/version/set-active`) belong to **P4**, not the first P3 CLI. `--preview` validates only, never spends model tokens. Standard output is machine-readable with stable status/IDs; failures use stderr and nonzero codes. Tests verify same service contract as P1 and no hidden scheduler use.
- [ ] **P3.5** Generate UTF-8 Markdown + structured JSON for the selected candidate and review bundle, with references to original/rewrite history, warnings and visual brief. Do not equate a local content record with `published`.

**P3 PASS:** **AT-06/07/08/15/16/26** plus **E2E-01/02** have actual subprocess/fresh-process receipts; one command can create a reviewable saved package; a separate process reopens it without a model call; unknown/duplicate requests do not silently double-generate. **P3 NO-GO:** missing provenance, ambiguous selected text or records stored only in volatile memory. Evidence EV-04/05/12/13.

### P4 — Unify voice authority and approved feedback

**Depends on:** P3's storage/read contract; source authority already exists and must not be rewritten from scratch.

- [ ] **P4.1** Implement a versioned voice resolver/registry (proposed `src/app/voice_registry.py`). Seed `graham` from **both** existing YAMLs, retaining the original V2 Voice Bible file path **and blob SHA**. Version the derived prompt projection, mark active version, and preserve immutable earlier versions for old posts. Separate factual job/company context from style. Do not copy historical incidents as personal claims.
- [ ] **P4.2** Reuse `VoiceExample`, `LinkedInContentFeedback` and `voice_example_from_feedback` from existing contracts/helper. Store actual user-edited/approved examples with provenance; rejected samples become correction evidence, never positive model exemplars. Cap prompt examples at current 3 unless evidence justifies changing the contract. Verify Grahams's voice never leaks into `ardent_v2`.
- [ ] **P4.3** Support `voices list/show/version/set-active` and revisions via the same storage/service boundary (UI support comes next). **Tests:** cross-profile isolation, new version activation, old run still bound to old voice/hash, no silent voice mutation on feedback, no private source anecdotes, conflicting edits rejected, no model call on voice read.

**P4 PASS:** **AT-09/18/20/22** plus **E2E-03/11** (with P2 human sequence receipts reused until invalidated) have receipts; a voice/version selected by the CLI produces the same runtime authority that the UI will later select; approved examples are traceable, not fabricated or silently promoted. Evidence EV-09/10/11/12.

### P5 — Small local browser UI: Voices / Create / Review

**Depends on:** P3/P4. **Does not gate P2.**

- [ ] **P5.1** At this milestone confirm the actual single-user vs remote/multi-user requirement. For local/single-user use, default to a **thin FastAPI + server-rendered templates** interface if its test setup and dependency surface are smaller than alternatives. This is a **candidate choice**, not proof the framework is required. No deployment or external exposure without an explicit auth/security decision. Keep UI listening to loopback by default.
- [ ] **P5.2** **Voices:** inspect Graham/Ardent without mixing; adjust an approved profile by a new version with diff and rollback; attach approved examples; preview a proposed voice using a labeled *new explicit generation*, not hidden autosave calls. **Create:** topic/evidence/goal/voice/visual preference; submit once, display `needs_more_evidence`, `skipped` or reviewable output. **Review:** selected and original/rewrite drafts, claims/sources, score/rationale, visual brief, edit/keep/reject, exports and run history. A material text edit creates a new candidate/revision, **invalidates previous quality/claim verification and any visual plan**, and requires revalidation before being accepted for handoff.
- [ ] **P5.3** Browser/CLI parity test: UI changes active Graham voice version → new headless generation uses it; prior run remains unchanged; CLI-generated run opens in UI with same hash; refresh and review do not regenerate. Test on mobile-sized viewport and escaped HTML/unsafe URLs; protect local data and secrets.

**P5 PASS:** **AT-10/13/17** plus **E2E-04/05** pass in a real browser/HTTP session; an actual person can maintain voices and review the very same saved headless runs; no parallel UI generation algorithm or second scheduling state. Evidence EV-02/04/09/13; CH-02/08.

### P6 — Render images/carousels **only after the visual-planning gate**

**Depends on:** P2 explicit GO and proper approval for paid provider calls. P5 is useful but **not an inherent prerequisite** for renderer prototype work.

- [ ] **P6.1** Refresh current provider/model capabilities, image quality, latency, licensing and cost at decision time. Replicate is an **expected candidate** under the current packet, not a permanent provider mandate. Record a small comparison and spend cap. Do not reuse stale API assumptions as facts.
- [ ] **P6.2** Render from the selected approved visual plan, not from an invented generic image prompt. Image providers produce imagery; typography and carousel slide layout are deterministic. Preserve plan/candidate/model/prompt/asset IDs and alt text. Tests reject fabricated visual claims, unreadable text, padded carousel, wrong candidate hash, failed provider and unsupported asset.
- [ ] **P6.3** Human-inspect real single-image and carousel outputs at mobile readability, bound retries/regeneration and capture visual reason codes when a repeated defect justifies them. A visual plan `status=planned` is **not** a rendered asset or publication permission.

**P6 PASS:** **AT-11/25/26** plus **E2E-07** show actual rendered files and human inspection receipts; useful inspected rendered assets with provenance and bounded provider cost. **P6 NO-GO:** weak repeated visuals or unverified factual overlays. Evidence EV-03/08/17.

### P7 — Editorial handoff and Dedication-owned publication (separate releases)

**Depends on:** accepted P2 content, durable P3 records, P4 voice binding, P6 rendered visual package for the accepted normal publish path, current Dedication owner contracts, and explicit publication authorization. **P5 browser UI is not a technical prerequisite** because editorial review/handoff can use the headless interface; if P5 is present it must pass its independent safety tests.

- [ ] **P7.1** Build a read-only-to-orchestrator editorial handoff with `run_id`, `selected_candidate_id/hash`, voice version, evidence refs, human editorial decision and optional render IDs. Keep editorial approval distinct from **Dedication's canonical publication approval state**. Test that editing creates a new candidate revision and invalidates stale quality/claim review, visual plan, and handoff approvals; the edited candidate must be rechecked and replanned before publication handoff.
- [ ] **P7.2** Read Dedication's current canonical owner docs **just in time**; integrate via its existing command/Action/Outcome boundary. Reconcile user/day/post state there, not a parallel generator scheduler/notification path. Test duplicate handoffs, stale content revisions and interrupted responses.
- [ ] **P7.3** Select current supported LinkedIn publisher/adaptor only after checking real API product approval, scopes and media upload requirements. Start with mock/isolation tests, then explicitly authorized one-post acceptance; verify actual post URL/URN and receipt externally. Missing/ambiguous response remains `unknown`/not confirmed; no blind retry, fake success or autonomously posted comments.

**P7 PASS:** **AT-12** plus **E2E-08** (isolated negative cases) and **E2E-09** (separately authorized real publication) have verified receipts; verified human-approved version becomes one externally observable post with one canonical Dedication outcome. **P7 NO-GO:** any approval, authorization, access or external receipt uncertainty. Evidence EV-02/15/16/17.

**Deferred after P7:** measured-post outcome learning and selected comment/reply assistance remain `IDEA_LEDGER.md` candidates. They must be promoted through the actual owner only after sufficient real outcomes exist.

## 5. Test strategy, measurable outcomes, and traceability

### 5.1 Proof levels: what a PASS actually means

A misleading filename is not evidence. The current `tests/test_end_to_end_generation.py` uses an injected `FixtureClient` and `fixture_visual_planner`: **it is an engine-level integration regression, not a real CLI/browser/live-provider E2E** (EV-14, EV-20). Likewise `tests/test_publish_quality_review.py` tests scripted 87/92/93 outcomes, **not measured LinkedIn impact or real-world voice quality** (EV-07, CH-19).

| Layer | Runner / boundary | What a pass establishes | What it does **not** establish |
|---|---|---|---|
| **UT** (unit) | `pytest`, pure validator, schema, hash, decision, feedback helper | A rule behaves deterministically on defined inputs | Complete workflow, human voice fit, live provider |
| **IT** (integration with injected clients) | `pytest` drives `run_generation` / `generate_content` and fakes for model/planner | Real Python contracts and branches are connected; fake call counts enforce efficiency | Real external model, CLI process, UI, publishing |
| **E2E-OFFLINE** | Real CLI subprocesses, actual store, fresh process; later actual local web server and browser; injected provider only at external boundary | Full *local user-visible workflow*, persistence, screen and headless parity | Quality of a real LLM or LinkedIn posting |
| **E2E-LIVE + HUMAN** | Real configured generation provider and genuine supplied evidence, with explicit reviewer verdict | Actual model path and useful accepted text/visual plans for observed subjects | Scalable statistical virality, renderer or publishing |
| **E2E-RENDER** | Real image adapter/assets, human mobile inspection | Rendered media exists and fits the inspected post | LinkedIn publishing |
| **E2E-PUBLISH** | Authorised Dedication approval and actual supported LinkedIn publish transport plus independent external receipt | One real approved version published and traceable | Broad permission to autonomously publish afterward |

**Rule:** fixtures may establish correctness of branching, not author voice authenticity; model scores alone do not prove factual accuracy; visual plans are not image files; mock publisher receipts are not real posts. `PASS` means executed checks with retained evidence, not a test plan checkbox.

### 5.2 Acceptance register and phase mapping

The complete stimulus → expected observation → required proof for **AT-01..AT-26** lives in the [Durable Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) §2. That companion is the **single detailed definition** of these requirements; this section is an execution-stage map only.

| Phase | Acceptance criteria, including the new outcome tests | Why it is gated |
|---|---|---|
| P0 | AT-16 baseline portion, QB-00 | Get truthful source/runner receipt, not new product readiness |
| P1 | AT-01/02/03, IT-01 | Candidate/visual hash and no incorrect readiness |
| P2 | AT-03/04/05/14/19/20/21/22/23/24/25/26 | Human editorial value + real provider + factual and comparative baseline evidence |
| P3 | AT-06/07/08/15/16/26 | Durable headless workflow and measurable cost/recovery |
| P4 | AT-09/18/20/22 | Voice version/corpus fidelity and privacy |
| P5 | AT-10/13/17 | Browser/headless parity, edit invalidation and safe preview |
| P6 | AT-11/25/26 | Actually rendered, useful visual with bounded provider expense |
| P7 | AT-12/13/17 | Dedication approval, unknown/duplicate protections and independent external receipt |

At P2, the **current owner gate** (≥5 genuine subjects, ≥4 of first six eligible drafted subjects keep/light, ≥2 human-accepted live-provider subjects, required visual diversity and Challenge) remains authoritative. Additional v4 AT-19..26 thresholds are **proposed** until recorded in the owner packet; do not claim a score is a publishing permission. For fewer than six legitimate drafted subjects, first-six evaluation is `NOT_YET_EVALUABLE`, not a pass; do not force the sixth draft.

### 5.3 Composed E2E journey mapping

The detailed **E2E-01..E2E-11** journeys and test-level distinctions live in [Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) §3–5. Existing scenarios retain their IDs; **E2E-10/11 are new P2 editorial comparison and multi-post sequence checks**. Map them as follows:

| Phase | E2E scenarios | Proof type |
|---|---|---|
| P2 | E2E-06, E2E-10, E2E-11 | Live provider + human reviewed corpus, claim ledger, blinded basic-prompt comparator |
| P3 | E2E-01/02 | Actual CLI subprocess and fresh-process persistence/failure behavior |
| P4 | E2E-03; reuse E2E-11 if still valid | Versioned voices and accepted examples |
| P5 | E2E-04/05 | Real local HTTP/browser and headless parity |
| P6 | E2E-07 | Real images/carousel and human visual acceptance |
| P7 | E2E-08 isolated mock, E2E-09 separately authorized external | No fake publish receipt or implicit approval |

Do not call injected `tests/test_end_to_end_generation.py` a CLI/browser/live E2E. Never mark a later E2E PASS in a first P0/P1 chat just because its acceptance criterion is documented.

### 5.4 Historical initial-slice test checklist and reusable gate receipts

**QB-00 (P0 baseline, existing code):** in a valid authorized checkout, run and capture the complete exit statuses of:

```bash
python -m pytest -q tests/test_end_to_end_generation.py tests/test_publish_quality_review.py tests/test_spoken_voice_authority.py tests/test_voice_bible_authority.py tests/test_visual_asset_planning.py tests/test_opportunity_gate.py
python -m pytest -q
```

These commands are **requirements for the implementation chat**, not executions from this review. If checkout/import/dependency failure occurs, preserve exact error and distinguish environment from code failure. Do not weaken test assertions to hide a baseline failure.

**IT-01 (P1 composed contract integration, new):** add `tests/test_selected_candidate.py` and run:

```bash
python -m pytest -q tests/test_selected_candidate.py tests/test_end_to_end_generation.py tests/test_publish_quality_review.py tests/test_visual_asset_planning.py tests/test_opportunity_gate.py
python -m pytest -q
```

IT-01 **expected**: test function/assertions cover A87→B93 (one rewrite and `source_content_sha256` parity in visual; wrong-source planner output rejected/deferred), A92→A (no rewrite), A87→unsafe/low B (no selection), missing quality (no readiness), skipped/needs evidence (no full draft), legacy top-level body unchanged, SHA equals selected UTF-8 body, and no accidental hidden external effect. Capture the first expected **RED** result, then **GREEN** with actual commands/exit codes/commit. Do not write a green receipt into the plan before executing it.

**One normalized execution receipt per check or grouped run** (actual stage/P0/P1/P2 or E2E):

```json
{
  "test_id": "IT-01",
  "phase": "P1",
  "status": "NOT_RUN|PASS|FAIL|BLOCKED|NOT_YET_EVALUABLE",
  "mode": "fixture|live|human|browser|render|publish",
  "checked_at_utc": "<actual UTC timestamp>",
  "repository": "GrahamArdent/LinkedIn_Generator",
  "head_sha": "<actual tested commit>",
  "command_or_action": "<exact command or reviewer action>",
  "exit_code_or_verdict": "<real result>",
  "request_id": "<if applicable>",
  "run_id": "<if applicable>",
  "attempt_id": "<if applicable>",
  "artifact_refs": ["<retained logs/output/visuals/review refs>"],
  "expected": "<assertion in §5.2 or §5.3>",
  "observed": "<what actually happened>",
  "error_code_or_blocker": "<if any>"
}
```

Replace all angle-bracket placeholders **only with observed values**, never examples presented as actual checks. `NOT_RUN` is a valid truthful status before a gate starts, **not** PASS. Keep fixture and live results in separate receipts. User-written/human feedback contains approval authority, not an automatic evaluator score.

### 5.5 Release gate / scenario coverage map

| Release checkpoint | Must be observed before `PASS` | Must remain gated |
|---|---|---|
| **P0** baseline | QB-00 + owner disposition + current heads; red baseline diagnosed explicitly | Architectural effects if owner decision unaccepted |
| **P1** selected candidate | IT-01 + AT-01/02/03 + regressions + review/diff at source SHA | Treating the optional selected field as permission to publish |
| **P2** live writing usefulness | AT-04/05/14/19–26 + E2E-06/10/11 human/provider evidence + current owner Challenge Gate | UI, paid rendering, publishing do not become implied acceptance |
| **P3** headless persistence | AT-06/07/08/15/16 + E2E-01/02 | Hidden provider calls on reads, automatic retry of unknown effects |
| **P4** voice management | AT-09/18/20/22 + E2E-03/11 | Unapproved example promotion or changes to older run versions |
| **P5** browser UI | AT-10/13/17 + E2E-04/05 | Unauthenticated remote access or UI-specific generation rules |
| **P6** rendered assets | AT-11/25/26 + E2E-07 | Publishing; visual plans counted as real images |
| **P7** publish integration | AT-12 + E2E-08 mock safety + separately admitted E2E-09 real evidence | Unapproved publish, duplicate, unknown receipt counted as confirmed |

**Historical P0/P1 success criteria (reuse completed receipts unless invalidated):** obtain a truthful **QB-00** baseline, a recorded P0 owner decision/disposition, then **IT-01** showing selected B/selected A/unsafe or missing quality/skip decisions with same text/visual identity, observed red→green and affected full-suite results. **E2E-01..11 are *not* first-milestone requirements**; some can become eligible later in the same ongoing work chat after feature prerequisites and owner gates clear.

## 6. Release / work control

**Mandatory milestone synchronization:** Apply the five-state checkpoint in [the current P2 subplan](CODEX_FIRST_TRIAL_GAME_PLAN_2026-11-04.md) at meaningful milestones throughout P0–P7: source revision, local CI, actual PR/main integration, actual installed/runtime binding, and reconciled continuation docs. A test pass or pushed branch is not a merge/install receipt. Status checks grant no merge, hosted CI or installation authority. CURRENT_WORK_PACKET.md must link the latest dated receipt and next eligible phase.

- **No more than one active implementation slice at a time.** Complete P0/P1 first (small PR or two as the owner permits), then run the **existing P2 trials** before production infrastructure expansion. If a genuine human/provider gate blocks P2, only separately admitted fixture-only groundwork can proceed, never as evidence that P2 passed. P3/P4/P5 form the usable standalone product; P6/P7 are separately gated external-effect work.
- Keep milestones as **testable outcomes**, not one large PR. **Use §5 test-to-gate mapping; a milestone cannot be marked PASS when one required outcome is NOT_RUN, BLOCKED or NOT_YET_EVALUABLE.** Use `task_id`, `attempt_id`, `run_id`, UTC timestamps, base/head SHA, changed files, test commands and exit codes, provider kind (`fixture|live`), feedback/receipt IDs and explicit PASS/HOLD/FAIL at each boundary. Where no run happened, write `NOT_RUN`.
- On an actual tool failure follow Paths JIT diagnostics; on implementation failure preserve error class and test evidence, fix smallest cause, never weaken an assertion just to turn CI green. Do not claim a hosted CI result without an actual check ID.
- **At acceptance/merge time** refresh repo/PR heads, check required reviewers, current branch policies, CI budgets and owner permissions. Creation of a game plan authorizes no new CI, merge, deployment, secrets use or external publishing.
- Keep the existing owner packet **and** this proposal reconciled. If an accepted new decision conflicts, update the owner first, then this proposal; never elevate this proposal by fiat. Leave legacy salvage safely recoverable.

## 7. Handoff for the next execution chat

**Current bounded slice: evidence-first P2 continuation.** P0/P1 and the Codex connection have actual receipts; do not restart them unless relevant source changes invalidate their proof. Follow the [current phased trial plan](CODEX_FIRST_TRIAL_GAME_PLAN_2026-11-04.md) and [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md): Phase0 currentness checkpoint, Phase1 evidence brief, Phase2 writer repair, Phase3 scorer qualification, then Phase4 one substantive comparison and human review. Re-fetch current Paths and owner authority just in time. Preserve QB-00/IT-01 as historical observed baseline/repair evidence, all26 acceptance objectives and11 E2E scenarios. Continue P3–P7 only when their prerequisites and owner gates clear. Every meaningful milestone reconciles source, local CI, PR/merge, runtime/install and authoritative documentation. No plan description authorizes hosted CI, merging, deployment, paid rendering or publishing.

### Completion declaration rules

- **Plan package complete:** All three reviewed v4 documents exist, their AT/E2E/EV/CH cross-references are valid, and the planned results are explicitly labeled NOT_RUN; **does not mean any code was implemented or tested**.
- **P1 complete:** an observed QB-00 baseline plus IT-01 red→green receipts, affected regression tests and accepted source diff exist; documentation claims alone are insufficient.
- **P2 complete:** AT-04/05/14 plus the applicable AT-19..26 owner-adopted criteria and E2E-06/10/11 are genuinely fulfilled, including the first-six denominator, independent human and live-provider proof, with actual records.
- **Product complete:** P3–P7 each accepted as scoped with observable external results where required. No synthetic publish receipt.

**Decision state:** Current continuation adopted through the operator's instructions and CURRENT_WORK_PACKET.md; specific future side effects remain gated. The earlier v1 plan is **superseded as a planning proposal by this v4 review**, not deleted or claimed merged. See the challenge decisions in the [Evidence and Challenge file](LINKEDIN_GENERATOR_EVIDENCE_AND_CHALLENGE_V4_2026-11-04.md).
