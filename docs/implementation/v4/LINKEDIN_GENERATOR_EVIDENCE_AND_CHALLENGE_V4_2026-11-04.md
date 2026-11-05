# LinkedIn Generator — Test Evidence, Reuse Map, and Adversarial Challenge (v4)

**Date checked:** 2026-11-04
**Current continuation:** Original review sections below are historical. The dated §9 addendum records the evidence-first change; CURRENT_WORK_PACKET.md and actual receipts determine execution status.
**Mode:** READ-ONLY analysis of connected GitHub sources + the previously generated 2026-11-04 plan and v2 audit package; this turn also verified current Paths and primary owner contract files. No product code, GitHub state, CI, models, rendering, or publishing were changed or executed for this review.
**Evidence standard:** `OBSERVED-SOURCE` = file or PR content inspected; `OWNER-RECORDED` = an assertion in the current owner packet but **not independently re-executed**; `PROPOSAL` = unimplemented design; `UNKNOWN` = evidence still required.
**Companion documents:** [Revised Game Plan](LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md) · [Durable Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) · [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md) · [Start Here](LINKEDIN_GENERATOR_PACKAGE_README_V4_2026-11-04.md). This file explains *why* the plan changed and what the current tests can/cannot prove. It does not supersede live project authority.

## 1. Executive assessment: what survives the challenge

**Retained product direction:** One existing Python LinkedIn content-generation engine, one typed request/result boundary, a quick headless path, one small voice/create/review UI, and later gated rendering and Dedication publication orchestration. This matches the standalone repository's purpose more closely than starting the unfinished V2 Next.js/Supabase rebuild as a second production engine.

**Material corrections to previous proposals, including the v3 test-objective critique:**

1. The earlier plan put the active human content trials **after** new storage, voice registry, and UI milestones. That is backwards. The accepted `CURRENT_WORK_PACKET.md` already makes the real multi-subject trial the next product gate. **Moved earlier to P2.**
2. It prematurely specified **FastAPI and SQLite** as if necessary to prove writing. Keep them as candidate local UI/persistence choices, subject to an owner architecture decision and milestone-specific tests. **Do not make them prerequisites for current trials or first headless contract proof.**
3. It proposed durable run records and a selected-candidate contract but did not sharply distinguish editorial `keep` from publication approval or unknown effects from safe retries. These are now explicit invariants with negative tests.
4. It recognized V2 PR #6 but insufficiently separated **“ADR accepted inside an open branch”** from **“cross-repository product decision accepted on default branches.”** The owner must formally reconcile the competing directions before implementation/cutover.
5. The first plan had too many milestone dependencies for a narrow quality gate and occasionally suggested new modules before proving that existing code lacked a reusable equivalent. The revised plan uses JIT inspections, smaller tasks, and a single named owner per concern.

**Verdict:** **GO to begin a new implementation chat with P0/QB-00 read-only baseline and conditional, owner-admitted P1/IT-01; HOLD declaring implementation tests passed, broad rollout, paid rendering and live publishing.** Neither current product readiness nor new test PASS is established by this document.

## 2. Source-of-truth snapshot and precedence

| Rank | Surface | Authority/role | What was observed |
|---|---|---|---|
| 1 | Current explicit user decision + platform/tool/owner permissions | Material product intent and authorization | One engine, headless+UI, preserve voices. Request for review documents is **not** itself permission to modify/migrate/publish. |
| 2 | [`LinkedIn_Generator/README.md`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/README.md), [`CURRENT_WORK_PACKET.md`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/CURRENT_WORK_PACKET.md), accepted contracts, `main` implementation | Primary product owner and in-flight execution pointer | Python content engine and Dedication division; current stage is multi-subject validation before paid rendering. |
| 3 | [`GrahamArdent/paths/CHATGPT.md`](https://github.com/GrahamArdent/paths/blob/main/CHATGPT.md) | How to discover/read/diagnose connected ecosystem routes | Read on default `main`, blob `ba7463b91398ae9378a4ad09eba4974dedd5df40`. Routes are not semantic permission. |
| 4 | [`LinkedInGenV2` PR #6](https://github.com/GrahamArdent/LinkedInGenV2/pull/6), its branch-local ADR/work packet | Competing architectural **proposal** / salvage evidence | Open **draft**, unmerged; branch ADR calls Next.js/Supabase “accepted” *within that branch*. Executable R0-03 verification still pending. |
| 5 | Older V2/V3 Python/Streamlit/Next.js/automation code, README badges, examples | Historical design, failure cases, and selective salvage | Valuable voice and research assets, but no blanket inheritance of legacy functionality or status claims. |
| 6 | 2026-11-04 previous headless-first game-plan file | Prior **planning proposal** (not product authority) | Reviewed as the material being challenged; its decisions do not outrank live owner contracts. |

**Checked repository heads:**

- `GrahamArdent/LinkedIn_Generator` default `main`: `a714d1ef355ade9ca47a52b301ea477bd0c14f34`.
- `GrahamArdent/LinkedInGenV2` default `main`: `e5608e94948684283aebb6149414791680463a52`.
- `LinkedInGenV2` PR #6 head: `6f093236da24ee5953e0668da3b63ebbd369b647`; state: open/draft/unmerged (last displayed updated at `2026-09-05T16:03:37Z`).
- `paths/CHATGPT.md` file blob: `ba7463b91398ae9378a4ad09eba4974dedd5df40`.

These are **retrieval-time snapshots**, not promises that a new execution chat will see unchanged heads.

## 3. Evidence registry (stable IDs shared with the revised plan)

| ID | Source / exact provenance | Evidence class | Finding; disposition |
|---|---|---|---|
| **EV-01** | [Paths `CHATGPT.md`](https://github.com/GrahamArdent/paths/blob/main/CHATGPT.md), blob `ba7463b9...` | OBSERVED-SOURCE | JIT route discovery, direct known-operation fast path, exact-error diagnosis only on failure. **Follow at every new session; do not confuse tool exposure with authority.** |
| **EV-02** | [Primary `README.md`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/README.md), blob `8352096f...` | OBSERVED-SOURCE | `LinkedIn_Generator` owns LinkedIn content intelligence, **not** scheduling/publish approval; independent engine callable by Dedication; target **not** the legacy Streamlit app. **Use as product boundary.** |
| **EV-03** | [Primary `CURRENT_WORK_PACKET.md`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/CURRENT_WORK_PACKET.md), blob `2d0cee3f...` | OBSERVED-SOURCE / OWNER-RECORDED | `LIG-CONTENT-VISUAL-ACCEPTANCE-2026-09-01` active. Visual planning Slice A recorded as implemented, Trials #2–#5 open, >=5 genuine subjects, >=4 of first 6 draft candidates kept/light edit, >=2 accepted subjects through real provider, 90 quality threshold and <=1 guarded rewrite. **Current mandatory gate.** |
| **EV-04** | [`src/app/contracts.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/contracts.py), blob `1af1febf...` | OBSERVED-SOURCE | Existing Pydantic `LinkedInContentRequest/Result`, `VoiceExample`, `LinkedInContentFeedback`, `VisualAssetPlan`. Result has top-level `body`, `review`, `visual_asset` but **no explicit selected-candidate object**. **Extend compatibly.** |
| **EV-05** | [`src/app/integration.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/integration.py), blob `f81a8443...` | OBSERVED-SOURCE | `_publish_candidate` may choose a qualified **rewrite** for visual planning; return still sets top-level result `body` from `payload.body`, which may be original. **Contract ambiguity, not proven live failure.** |
| **EV-06** | [`src/app/api.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/api.py), blob `511cdccb...`, and [`src/app/llm.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/llm.py) | OBSERVED-SOURCE | User context flows through plan/draft/critic/humanize, opportunity and quality gates; injectable OpenAI Responses provider exists. **Reuse; live provider not re-tested here.** |
| **EV-07** | [`tests/test_publish_quality_review.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_publish_quality_review.py), blob `54e69c49...` | OBSERVED-SOURCE | Fixture assertions cover original 87/rewrite 93, good 92, unsafe rewrite, unavailable quality. **Excellent regression seed, NOT a test PASS in this review.** |
| **EV-08** | [`src/app/visual_assets.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/visual_assets.py), [`tests/test_visual_asset_planning.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_visual_asset_planning.py), test blob `7656862a...` | OBSERVED-SOURCE | Provider-neutral single-image/carousel planner, format rationale, structured slide text, copy-guard. **Reuse, not image rendering or empirical visual usefulness.** |
| **EV-09** | [`config/graham_voice_profile.yaml`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/config/graham_voice_profile.yaml), blob `1dc61a4d...`; [`config/graham_spoken_voice.yaml`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/config/graham_spoken_voice.yaml), blob `f2113955...`; [`config/personas.yaml`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/config/personas.yaml) | OBSERVED-SOURCE | Two **complementary** voice authorities: rhetorical architecture and natural expression. Separate `graham` and `ardent_v2`; explicit precedence and anti-anecdote rules. **Seed registry, do not rebuild voice from scratch.** |
| **EV-10** | [Original V2 Graham Voice Bible](https://github.com/GrahamArdent/LinkedInGenV2/blob/main/data/Voice_Bible_Graham%20(1).md), exact blob `e35aad7f324ea9cc691ea8fd5ca5fc3c7da5a5fd` | OBSERVED-SOURCE | Primary historical source of writing traits, causal POV ladders, narrative techniques. Some passages illustrative/cyber-specific. **Preserve provenance; never treat examples as current real-world facts.** |
| **EV-11** | [V2 Voice Bible preservation study, PR #6 branch](https://github.com/GrahamArdent/LinkedInGenV2/blob/audit/rebuild-blueprint-2026-08-24/docs/rebuild/salvage/GRAHAM_VOICE_BIBLE_PRESERVATION_2026-08-24.md), blob `4782bf7d...` | OBSERVED-SOURCE / BRANCH PROPOSAL | Prior high-value salvage research: voice core, approved examples, negative examples, separation from changing role/identity. **Reuse analysis, not branch-local architecture as default-branch authority.** |
| **EV-12** | [`src/app/feedback.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/feedback.py), blob `49d96797...` | OBSERVED-SOURCE | `keep/edit/publish` can promote positive voice examples; `reject` cannot; **helper performs no persistence or Dedication state change**. **Add durable human feedback later, preserve approval boundary.** |
| **EV-13** | [`src/app/cli.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/cli.py), blob `0e93c0c5...`; [`requirements.txt`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/requirements.txt), blob `ff485de9...` | OBSERVED-SOURCE | CLI uses date/scheduler/topics/legacy composer and imports `dotenv` although inspected requirements do not list `python-dotenv`. **Not the new request-driven headless CLI; verify before reuse.** |
| **EV-14** | [`tests/test_end_to_end_generation.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_end_to_end_generation.py), blob `b5b353b2...`; [`tests/test_spoken_voice_authority.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_spoken_voice_authority.py), blob `0755b059...` | OBSERVED-SOURCE | Injected test clients prove intended boundaries and voice prompt assembly *when run*. No actual provider acceptance established in this audit. **Reuse fixtures as focused baseline.** |
| **EV-15** | [V2 draft PR #6](https://github.com/GrahamArdent/LinkedInGenV2/pull/6), branch [ADR-001](https://github.com/GrahamArdent/LinkedInGenV2/blob/audit/rebuild-blueprint-2026-08-24/docs/rebuild/decisions/ADR-001_APPLICATION_ARCHITECTURE.md), ADR blob `7930050d...` | OBSERVED-SOURCE / OPEN DRAFT | Competing single-app Next.js/Supabase rebuild, avoiding separate FastAPI; R0-03 still lacks type/build/boot/HTTP smoke proof. **Cannot silently combine with active Python runtime; owner disposition required.** |
| **EV-16** | [`Dedication/README.md`](https://github.com/GrahamArdent/Dedication/blob/main/README.md), blob `adbdc1ba...` | OBSERVED-SOURCE | Canonical Day/Action/Outcome, operational state, notification, later integration are Dedication concerns. README requires **JIT current Level 1/2 owner contracts** before modifying them. **Preserve publication/state ownership.** |
| **EV-17** | [`LinkedIn_Generator/IDEA_LEDGER.md`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/IDEA_LEDGER.md), blob `f3ed5cf7...` | OBSERVED-SOURCE | Direct API vs Buffer, comments, analytics/post performance learning, rendering model comparison are captured/shelved/candidate, **not executable approval**. **Reuse idea register; avoid scope creep.** |
| **EV-18** | Prior file `LinkedIn_Generator_Headless_First_Implementation_Game_Plan_2026-11-04.md` (this conversation's earlier generated artifact) | LOCAL DOCUMENT / PROPOSAL | Previous M0–M9 roadmap and E2E matrix; not a repository authority. **Superseded as a planning proposal by v2**, preserved for audit comparison. |
| **EV-19** | Owner packet's Trial Evidence table/Close-Out (EV-03) | OWNER-RECORDED | Only Trial #1 has recorded human writing acceptance, with **manual** approximate 87 and 93–95 scores and no explicit completed human visual approval. Trials #2–#5 blank. **Do not describe quality gate as passed.** |
| **EV-20** | [`tests/test_end_to_end_generation.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_end_to_end_generation.py), blob `b5b353b24a...` | OBSERVED-SOURCE | Uses injected `FixtureClient` and `fixture_visual_planner` to call `generate_content`; tests **engine integration**, not subprocess/CLI/UI, real LLM, rendered media or actual LinkedIn delivery. **Label it IT, not full product E2E.** |
| **EV-21** | [`tests/test_publish_quality_review.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_publish_quality_review.py), blob `54e69c49...`; [`tests/test_visual_asset_planning.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_visual_asset_planning.py), blob `7656862a...`; [`tests/test_spoken_voice_authority.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/tests/test_spoken_voice_authority.py), blob `0755b059...` | OBSERVED-SOURCE | Scripted score/rewrite cases, plan-structure and prompt-injection assertions are reusable **UT/IT fixtures**, not human authentic-voice verdicts, output-fact review or real rendered-image inspection. |
| **EV-22** | [`src/app/integration.py`](https://github.com/GrahamArdent/LinkedIn_Generator/blob/main/src/app/integration.py), `src/app/contracts.py`, the active packet; this v4 plan's composed E2E scope | OBSERVED-SOURCE + TEST-GAP INFERENCE | Current result has no explicit selected-candidate field; existing tests do not exercise *real CLI subprocess→fresh-process reopen→actual browser→live provider→render/publish* as one proven program. **Those are proposed future scenarios, not reported defects or PASSES.** |

| **EV-23** | User's 2026-11-04 point-by-point critique of testing objectives (this conversation); captured in [Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) | USER DIRECTION / PROPOSED MEASURES | 8 added measures AT-19..26 distinguish human publish-worthiness, voice, claims, originality, simple-prompt comparison, edit effort, visual value and operational cost from mere test execution. Not independently proven outcomes. |
| **EV-24** | [Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) rubric, P2 scorecard and E2E-10/11 | PROPOSED TEST DESIGN | 6 eligible blinded paired subjects with same source inputs, non-forced denominator, separately logged human voice/insight ratings, edit minutes and claim ledger. ≥4/6 is a **pilot proposed acceptance threshold**, not evidence of impact or statistical superiority. |

### Confidence and invalidation

- **High for repository content:** confirmed source paths, file blob SHAs, code shape, open PR state as retrieved.
- **Medium for behavioral conclusions from inspection:** selected-candidate handoff is a credible interface risk, but no live package was produced in this review; tests must demonstrate its actual observable behavior.
- **Owner-recorded, not independently proven:** current packet's “Slice A implemented”, Trial #1 preference, previous PR merged claims and test expectations. Inspect actual receipts if implementation requires a stronger assertion.
- **Unknown:** whether a usable provider credential/runtime is currently authorized, actual generated-post acceptance across subjects, real rendered images, real LinkedIn publishing, current API permissions/scopes and provider pricing.
- **Invalidation triggers:** new default-branch commit to contract/generator/voice/planner, V2 PR #6 merged/closed/rebased, user architecture reversal, accepted Dedication contract change, fresh provider/API change, newly observed real acceptance evidence.

## 4. Challenge register: adversarial audit of v1/v2

| CH ID | Problem challenged | Original risk | Decision and mitigation in revised plan | Status |
|---|---|---|---|---|
| **CH-01** | **Milestone order** | v1 M5 placed the owner's active multi-subject quality trials after three infrastructure milestones. Could build a polished interface to a weak writing engine. | Bring acceptance forward: **P0→P1→P2** is critical path; UI/store not needed to prove quality. | Resolved in plan §2/P2 |
| **CH-02** | **FastAPI/SQLite prematurely fixed** | They were recommendations portrayed as selected commitments without a demonstrated multi-user, browser or concurrency requirement. | Retain Python engine. Treat FastAPI/Jinja2 and SQLite as **milestone choices**, assess at P3/P5; no extra service for CLI. | Resolved conditionally; decision gate explicit |
| **CH-03** | **Original vs selected rewrite ambiguity** | `body` may remain A while visual uses B; a consumer could display the wrong one. | Optional `selected_candidate` plus optional visual `source_content_sha256`; one resolver; no breaking `body` change; mismatched planner-source rejection and hash/ref parity tests AT-01/02. | Open implementation; design settled |
| **CH-04** | **Competing V2 architecture** | V2 PR #6 branch ADR says Next.js/Supabase is accepted, primary standalone repo owns Python content. Two apparent execution spines. | Classify branch-local acceptance separately; owner must reconcile and preserve salvage; do not auto-merge/close. | Human architecture gate |
| **CH-05** | **Editorial vs publishing approval collision** | `keep`/`publish` in feedback schema could be misread as permission to post or canonical outcome. | Generator editorial feedback only; Dedication final publication approval and receipt. Separate tests P7. | Design resolved; code to prove |
| **CH-06** | **Weak idempotency definition** | “Same request_id returns receipt” ignores changed-input ID collision; unknown effects might get repeated. | Compare normalized input fingerprint; conflict on mismatch; recover `unknown` without automatic retry; AT-07/08. | Planned tests P3 |
| **CH-07** | **Mocks mistaken for quality proof** | Repo contains E2E fixtures and the packet contains manual scores, but neither proves real-provider quality. | Explicit live-vs-fixture records; at least two real-provider accepted subjects and all existing human trial gates. | OPEN until actual evidence |
| **CH-08** | **Duplicate UI/headless business rules** | A GUI with its own voice/prompt pipeline drifts from CLI. | Both use the same service, registry, record store and candidate contract; CLI/UI parity AT-10. | Planned P3–P5 |
| **CH-09** | **Legacy migration trap** | Date-driven CLI and Streamlit carry obsolete scheduler and may miss current dependencies. | Inventory, do not make legacy code new entry point; new request-driven CLI; selective UI salvage only. | Planned P3/P5 |
| **CH-10** | **Voice authority confused with facts** | V2 examples include illustrative cyber incidents, old identity context and signature lines; risk of fabricated first-person post. | Separate voice/style from current factual evidence; preserve SHA; approved-example lineage and privacy tests. | Planned P4 |
| **CH-11** | **Premature rendering/publishing** | Visual brief might be treated as completed image; high model score as publish approval. | Respect P2 GO then actual P6 image tests; no publication until Dedication + real receipt. | Design resolved; later gates OPEN |
| **CH-12** | **Unnecessary breadth / overlapping tasks** | v1 had M0–M9 and 42 actions; persistence, review, state, and approval appeared in several phases. | Single owner per concern: P1 selection, P2 quality, P3 run artifacts, P4 voice, P5 UI, P6 render, P7 Dedication. | Resolved structurally |
| **CH-13** | **Stale in-flight status text** | Packet on `main` still says `AUTHORITY_RECONCILED: pending merge`, despite blob being in current default branch. | P0 reconcile only verified stale facts; no assumption about additional unseen pending work. | Open docs reconciliation |
| **CH-14** | **Unqualified new dependency** | Old CLI imports `dotenv`, but current inspected `requirements.txt` omits `python-dotenv`. | Baseline first; do not rely on legacy CLI or fake a passing smoke; pin any required dependency only when new chosen path needs it. | Open local validation |
| **CH-15** | **Historical / current API assumptions** | Old V2 Selenium, social API reports, and provider cost decisions could be imported as current. | JIT actual provider/API eligibility check only at P6/P7; idea ledger preserved with no automatic promotion. | Deferred by design |
| **CH-16** | **Evidence / error observability** | Repeated tool/model calls without IDs, timestamps, input refs or cause codes would make debugging and recovery unreliable. | Run/attempt/request IDs, UTC timestamps, hashes, exact command/exit code, model mode, structured error and disposition at P3; AT-06/08. | Planned P3 |
| **CH-17** | **Human edit invalidates earlier acceptance** | A text edit after scoring or visual planning might retain outdated status/plan and be published without rechecking claims. | New revision/hash on edit; invalidate old quality/claims/visual and handoff; require fresh check. AT-13. | Planned P5/P7 |
| **CH-18** | **Structural copy guard is not factual proof** | New unsupported claims need not introduce numbers, links or quotations, so regex copy checks alone can miss them. | Human claim/source review and deliberate adversarial non-numeric claim trial, AT-14; no misleading “fully fact-checked” claim. | Planned P2 |
| **CH-19** | **Mock integration mislabeled E2E** | A test with “end-to-end” in its filename could be used to declare CLI/browser/real provider complete. | Define UT/IT/E2E-OFFLINE/E2E-LIVE/HUMAN/RENDER/PUBLISH separately; current fixture tests are IT; E2E-01..11 have explicit receipts. | Resolved in test design; executions NOT_RUN |
| **CH-20** | **Undefined quality denominators** | Five real subjects could be incorrectly presented as satisfying “4 of first 6 drafted”; Draft B or fixtures might inflate count. | Need six unique eligible drafted subject results to calculate first-six ratio; B is same subject; human `none/light/structural` classification, no fake additional drafts. | Resolved criteria; P2 HUMAN HOLD |
| **CH-21** | **Generic pass/fail without expected observations** | “Tests pass” could hide wrong selection, extra provider calls, wrong file, omitted approval, or no actual output. | AT-01..26 now have a single detailed owner in the acceptance file; E2E-01..11 map observable journeys, including human editorial outcomes. | Resolved in documents; tests PLANNED |
| **CH-22** | **No reproducible test evidence contract** | Future summaries lack tested commit, exact command, exit code, UTC time, provider mode and artifact identifiers. | §5.4 requires a structured receipt per check; distinguish `NOT_RUN`, `PASS`, `FAIL`, `BLOCKED`, `NOT_YET_EVALUABLE`. | Resolved in documents; no run evidence yet |
| **CH-23** | **Unsafe “exactly once” claims for ambiguous external attempts** | Model/publisher timeout after dispatch could be called again and double-charge or double-publish, despite local tests. | Attempt `unknown` is quarantined until original provider receipt is reconciled; no blind launch, and no “exactly-once external” guarantee without provider evidence. | Resolved semantics; P3/P7 open |
| **CH-24** | **Testing later features in the first chat / false readiness** | Requiring UI, paid rendering and actual LinkedIn posts at P0/P1 would create impossible gates or premature effects. | First chat is QB-00 plus IT-01 only; later E2Es phase-gated; GO to start P0/conditional P1, not GO for product or publishing. | Resolved sequencing; live readiness open |

| **CH-25** | **Passing model score mistaken for worthy post** | A 90+ evaluator score can coexist with human rejection or generic content. | AT-19 separately records publish-worthiness, insight/usefulness and actual human verdicts; keep deterministic guard tests. | New P2 proposed gate; NOT_RUN |
| **CH-26** | **Voice only tested on one domain** | A good cybersecurity post can hide poor general Graham voice on AI, business or reflective subjects. | AT-20 sets human ≥4/5 rating for each accepted Graham post and links exact voice version + subject. | New P2/P4 proposed gate; NOT_RUN |
| **CH-27** | **Unsupported qualitative facts overlooked** | Numeric/URL regex catches a subset; unsourced qualitative assertions still harm trust. | AT-21 claim ledger enumerates all checkable assertions with source provenance and stale-source disposition. | New P2 proposed gate; NOT_RUN |
| **CH-28** | **Single-post quality masks corpus repetition** | Repeated metaphors/catchphrases can make six individually plausible drafts look synthetic together. | AT-22/E2E-11 test the full sequence for duplicated insights, hooks, patterns and editorial exceptions. | New P2/P4 proposed gate; NOT_RUN |
| **CH-29** | **Complex engine may not outperform a simple prompt** | Architecture, multiple stages and costs could produce no human-perceived value. | AT-23/E2E-10 use blinded paired same-fact baseline; ≥4/6 preferred is only a pilot bar, ties not wins. | New P2 proposed gate; NOT_RUN |
| **CH-30** | **Edit burden unmeasured** | Higher AI scores do not imply less work for the author. | AT-24 records edit scope, actual minutes, revision count against baseline; no claimed savings without measured comparison. | New P2/P3 proposed gate; NOT_RUN |
| **CH-31** | **Visuals cosmetically valid but meaningless** | Image/carousel can look polished yet add nothing or pad the message. | AT-25 separates plan rationale and actual rendered asset usefulness, with human review per format. | New P2/P6 proposed gate; NOT_RUN |
| **CH-32** | **Efficiency claims without budgets** | Background regenerations and cost/latency overhead may erase productivity benefit. | AT-26 records provider launches, latency and available billing; require pre-agreed caps and flag unknown provider metrics. | New P2/P3/P6 proposed gate; NOT_RUN |

**No issue was “fixed in the repository” by this audit.** “Resolved” above means the **plan wording/design** no longer has the contradiction; the acceptance test or owner decision still needs execution.

## 5. Selective reuse matrix: keep, inspect, defer, reject

| Asset / approach | Classification | Reason | Plan owner |
|---|---|---|---|
| Original Graham Voice Bible Markdown and SHA | **KEEP / immutable provenance** | Distinctive rhetorical/causal guidance; prevents re-derivation and wrong variant. | P4 |
| Graham Voice Profile + Spoken Voice YAML | **REUSE active** | Already reconciles rhetorical architecture with natural phrasing, avoids private anecdotes. | P2/P4 |
| Current `LinkedInContentRequest` / `LinkedInContentResult` and source/voice schemas | **REUSE and extend carefully** | Existing cross-product boundary and Pydantic validation. | P1/P3 |
| `run_generation` + injected LLM client + quality evaluator | **REUSE; qualify** | Avoid new prompt machinery until genuine acceptance reveals need. | P1/P2 |
| Selected-candidate logic | **REPAIR smallest seam** | Text/visual risk is localized. | P1 |
| Visual planner & carousel schema | **REUSE; human test** | Already has structure, text separation, alt text and fail-closed copy checks. | P2/P6 |
| Feedback promotion helper | **REUSE; add storage when needed** | Explicit human authority; currently ephemeral. | P3/P4 |
| Test fixtures / existing `test_end_to_end_generation.py`, voice, visual and rewrite tests | **REUSE as UT/IT baseline** | Negative and pipeline assertions; injected client does **not** prove headless/browser/live E2E, and no fresh tests were run. | P0–P4 |
| V2 Voice Bible preservation/salvage study | **REFERENCE** | Strong methodology on examples, identity and performance claims. | P0/P4 |
| Legacy CLI, Streamlit, schedule CSV/scripts | **REFERENCE / quarantine as runtime** | Date-driven pipeline would create two product routes. | P0/P3/P5 |
| V2 PR #6 Next.js/Supabase architecture | **CONFLICTING OPEN PROPOSAL** | Cannot simultaneously be the one production engine and preserve Python as the selected runtime without a decision. | P0 |
| Old V2 publishing/Selenium/comment automation | **DEFER / do not reuse directly** | Policy/access and current owner state unverified; not needed for content acceptance. | P7+ |
| Dedication scheduler, post canonical state, approval/notifications | **REUSE at owner boundary, JIT** | Prevent duplicated infrastructure/state models. | P7 |
| FastAPI/UI and SQLite | **PROPOSED choices, not current runtime proof** | Appropriate only after actual UI/data needs and owner acceptance. | P3/P5 |
| Replicate/direct LinkedIn/Buffer | **RESEARCH LATER** | Providers require live capability, permission, quality and cost comparison. | P6/P7 |

## 6. Cross-document and owner-boundary consistency audit

The three deliverables intentionally divide responsibility as follows. **The Test Objectives and Success Criteria companion alone defines AT-01..26 and E2E-01..11; Game Plan §5 maps implementation and gates**; this evidence file records why those gates exist and observed proof gaps.

| Question | Authoritative location inside this package | Where referenced |
|---|---|---|
| **What** outcome and **what sequence**? | [Game Plan §1–§4](LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md) | Prompt startup + task selection |
| **Why** reuse or change it? | This file EV-01..EV-22 and CH-01..CH-24 | Game Plan decision IDs and milestone evidence |
| **How** to start a new execution chat? | [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md) | Game Plan §7; this file header |
| **What presently controls the repository?** | Live `LinkedIn_Generator` README/packet and relevant owner contracts, **outside this package** | All three; this package is subordinate |
| **What tests and pass outcomes?** | [Acceptance definitions](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md), mapped in Game Plan §5 (QB-00/IT-01 retained) | Prompt first-chat scope; this file source-to-claim table |
| **What is finished?** | Actual code/test/human/provider receipts and owner packet updates | Never inferred from checkboxes, historical test code or this audit |

### Formal consistency checks to perform on the proposed wording

1. **One product owner:** LinkedIn Generator content, Dedication orchestration/publication, Paths capability discovery, PROGRAMSTART methodology. No role overlap in the proposed design.
2. **One generator:** CLI and UI only call one shared use-case/engine. V2's divergent draft branch not silently merged.
3. **One current gate:** P2 is the existing multi-subject acceptance; P3/P5 cannot be mistaken for a prerequisite. If P2 hits a genuine human/provider blocker, fixture-only groundwork may be a separate admitted slice, not proof that P2 passed.
4. **One candidate:** original/rewrite history stays visible, selected candidate binds visual/handoff/export. `body` compatibility is explicit. Edits create new candidate revisions and require new checks/visual plans.
5. **One approval meaning per domain:** editorial keep/edit/reject is not publication approval.
6. **No false evidence:** fixtures ≠ actual provider; visual plan ≠ rendered image; prepared package ≠ posted LinkedIn content; source text ≠ executed test.
7. **Prompt obeys plan:** execution prompt asks for P0/QB-00 and P1/IT-01 bounded work, not future E2E UI/publishing; provider/CI/writes are current-owner gated.
8. **No extra Master:** the primary `CURRENT_WORK_PACKET.md` remains active; the three-file package is only review/implementation guidance until owner reconciliation.

### Residual questions that require a **later explicit** decision (not missing facts to invent now)

- Can the standalone app remain local-only, or must the UI be remotely available to multiple authenticated users? Decide at P5; determines authentication and database requirements. Do not pretend the current request has already authorized public deployment.
- Does P3 truly need SQLite rather than atomic JSON/Markdown output files for single-user workflows? Choose after exercising concurrency/recovery/voice-edit tests, not by preference alone.
- Is the current live generation provider available through an approved runtime/credential path? Verify at P2 without exposing secrets or using fake receipts.
- Which rendering and publishing provider actually has acceptable current access/cost/quality? Defer to P6/P7 with fresh evidence and explicit effect admission.

## 7. Evidence-to-test trace and truthful initial test status

### 7.1 Evidence → acceptance expectations (no fictional runs)

| Source evidence | What was inspected | Tests it motivates | State on 2026-11-04 |
|---|---|---|---|
| **EV-04/05/07** | Source selection, A/B and quality fixtures | **IT-01**, AT-01/02/03; later E2E-01 | Source and planned tests inspected; new IT-01 **NOT_RUN** |
| **EV-03/06/19/21** | Current owner trial gates, model injection and synthetic evaluator tests | AT-04/05/14/19..26, E2E-06/10/11 | Only Trial #1 owner-recorded; trials #2–#5 and live acceptance **NOT_RUN / NOT_YET_EVALUABLE** |
| **EV-08/21** | Visual-plan contracts and tests | AT-11, E2E-07 | Structured-plan source exists; real render & inspection **NOT_RUN** |
| **EV-13/20/22** | Legacy CLI and fixture-bound “end_to_end” test | AT-06/07/08/15/16, E2E-01/02 | New headless flow/store **NOT_IMPLEMENTED / NOT_RUN** |
| **EV-09/10/11/12/21** | Voice sources, prompt-projection tests, feedback helper without durable storage | AT-09/18, E2E-03 | Voice material exists; versioned approval workflow **NOT_IMPLEMENTED / NOT_RUN** |
| **EV-02/04/13/20** | Primary product boundary, no new UI golden path | AT-10/13/17, E2E-04/05 | Full browser parity/edit invalidation **NOT_RUN** |
| **EV-02/16/17** | Dedication boundary and shelved publication ideas | AT-12, E2E-08/09 | Publication deferred; **NOT_RUN**, no consent implied |

**Known existing test files, not yet freshly executed in this chat:** `tests/test_end_to_end_generation.py` (injected engine integration), `tests/test_publish_quality_review.py`, `tests/test_spoken_voice_authority.py`, `tests/test_voice_bible_authority.py`, `tests/test_visual_asset_planning.py`, and `tests/test_opportunity_gate.py`. Existence or historical owner claims about passing are not a v4 test result.

### 7.1a New product-outcome test coverage (user-directed v4 additions)

| Source/decision | Proposed tests | What evidence is still absent |
|---|---|---|
| EV-23 human publish-worthiness + voice | AT-19/20, E2E-06/11 | Six subject-level reviewer ratings with selected text/hash and real provenance |
| EV-23 factual provenance, originality | AT-21/22, E2E-06/11 | Independent claim ledger for accepted drafts and six-post similarity review |
| EV-24 simple baseline + editing effort | AT-23/24, E2E-10 | Same-input blinded six-pair reviewer preferences and actual edit time |
| EV-23 visual usefulness + measured economics | AT-25/26, E2E-06/07 | Human format usefulness, provider model-call/latency/cost budgets and receipts |

**These entries are not observed product PASS.** The existing owner packet must adopt any new P2 hold threshold before an implementation agent treats it as binding. A small six-pair pilot cannot establish population-level effectiveness or LinkedIn performance.

### 7.2 Minimum retained receipt for a future PASS

`test_id → acceptance AT IDs → phase → checked_at_utc → tested commit SHA → exact command/action → test layer → environment/provider kind → result/exit code → request/run/attempt IDs → observed output/hash → review/receipt references → blocker (if any)`.

A **human** result must identify subject, evidence/claims, selected text and `keep|edit|reject`, plus `none|light|structural` for edit scope and visual verdict. A **live provider** result must be labeled `live` with nonsecret model/version and actual invocation record. An **external publish** requires independently visible URL/URN plus Dedication's canonical outcome. A mock has neither authority nor proof of the latter.

**Receipt states:** `NOT_RUN` (no execution), `PASS` (all specified observations), `FAIL` (executed and contradicted requirement), `BLOCKED` (could not perform required effect), `NOT_YET_EVALUABLE` (e.g., first-six threshold with <6 eligible drafted subjects). Distinguish a failed precondition from a failed assertion. Never transform BLOCKED into PASS by quoting code or mocks.

### 7.3 Adversarial re-check of implementation-readiness

- **Scope:** New execution chat can start with current Paths → owner packet → **QB-00** baseline → authorized **IT-01** selected-candidate correction, without DB/UI/render/publish. **GO** for this bounded start.
- **Architecture:** V2 PR #6 open/draft and competing ADR remain unresolved across repos. **HOLD architectural repository writes until an owner disposition is recorded**; preserve source and branch provenance.
- **Tests:** Explicit stimulus/outcome/observable evidence for every AT and phase-specific E2E in Plan §5. **No observed P1/P2/new E2E PASS**, therefore **NO-GO** for declaring full implementation complete.
- **Human/provider gates:** Do not count mocked model results as accepted voice; do not claim >=4/6 when denominator unavailable; no paid renderer or publishing without separate permission.
- **Recovery:** A timed-out provider invocation with uncertain completion stays `unknown`, not automatically retried. No assertion of external exactly-once without provider evidence.
- **Ownership:** Saved editorial package is not a second Dedication canonical post state; UI and headless share one engine and candidate ID.

## 8. Verification statement and route forward

**What was performed:** compared the prior generated game plan to live default-branch Paths/primary owner files, contracts, voice YAMLs and original V2 Bible, legacy CLI and requirements, existing test sources, V2 open PR/ADR, Dedication boundary and idea ledger. Challenged scope, sequencing, state ownership, failure recovery, quality evidence and architecture overlap; defined explicit expected outcomes and stage-specific E2E coverage and audited the existing fixture-only test label. Reviewed cross-references among the revised package and exposed the remaining human gates.

**What was not performed:** no checkout tests, provider generation, content trials, score validation, rendering, GitHub writes, hosted CI, PR merge, or posting to LinkedIn. Claims about earlier merges/Trial #1 are explicitly **owner-recorded** until corroborated by runtime receipts.

**Document-only consistency check:** use the package `MANIFEST.sha256` and cross-link/ID validation before declaring the v4 bundle complete. The acceptance file contains one detailed definition each for **26 AT and 11 E2E**; this evidence file retains **24 EV and 32 CH** definitions. The checks are document integrity only, never product PASS.

**Next action:** use the [Execution Prompt](LINKEDIN_GENERATOR_EXECUTION_PROMPT_V4_2026-11-04.md) and [Acceptance Objectives](LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md) to undertake **Game Plan P0/QB-00 → P1/IT-01** after owner admission, then deliver the current **P2** trial evidence before expanding into new persistence or UI infrastructure. Keep this file as the source/risk index; refresh individual entries only when the relevant source changes.
## 9. Evidence-first continuation and state freshness — 2026-11-04

Accepted operator direction: improve substantive evidence, then writer/scorer alignment in separate phases; perform local CI and inspect merge/installation at meaningful milestones; keep continuation artifacts current. Current P2 execution detail is CODEX_FIRST_TRIAL_GAME_PLAN_2026-11-04.md; the P0–P7 roadmap and26 AT/11 E2E definitions remain.

Observed basis:
- The real trials consumed conversation summaries and source/fixture findings, not zero evidence. They establish what was requested/observed in that narrow setting, not customer outcomes or measured professional benefit.
- Voice Bible-derived profile, Spoken Voice and draft prompts exist. generation.py supplies generic angle scaffolding; its named plan prompt does not invoke source-specific model planning. Critic/humanizer model stages were absent in the saved call traces because deterministic checks found no issues; semantic publish-quality assessment and the single rewrite still ran. Activating more named stages is not automatically an improvement.
- publish_quality.py defines project-specific weights and model0–5 ratings, not a LinkedIn engagement metric. All4/5 yields80. Calibration against Graham's editorial labels is unproved in these trials. The evaluator sees a shortened voice context; actual runs supplied0 approved examples. Original78/rewrite77 and original73 are retained, not relabeled as product success.
- The simple baseline preferred in the last discussion was not rated under the same model rubric. Preference alone is not keep/light approval, a voice example or a calibrated score.
- Code safety/house-rule checks, factual support, editorial ratings and publication approval are distinct. Opinion is legitimate; external statistics are not compulsory. Assertions still need appropriate support, and inference must not be presented as observed fact.

Decision: next phases prepare a real source bundle/claim map, improve the existing source-specific editorial brief, align/calibrate the scorer without score inflation, then run one substantive trial. No mandatory extra review layers or architecture. Factual-omission tests must demonstrate behavior at the actual consumer; prompt inclusion alone is insufficient causal proof.

Currentness control: one milestone receipt covers candidate/main/PR, local CI, actual runtime/launcher, source/config hashes, expected/observed outcomes and next action. The packet links the latest receipt. Read status before acting; an unmerged but explicitly identified trial candidate can continue authorized source work without pretending it is installed from main. Merge/installation promotion retain their gates.

This amendment changes documentation only. No new post, writer/scorer implementation, threshold change, hosted CI, merge, install promotion, render or publication is claimed. Local CI/current runtime inspection for this documentation milestone is recorded under evidence/milestones/evidence-first-plan-20261104/.

### Evidence-first Phase1 execution

Five source-admission cases failed before implementation, then passed; full suite147 PASS. The optional sidecar binds exact request hash and claim/source qualifications, blocking missing/stale/contradictory support before provider construction. It does not establish that a source entails a claim. Primary ASD/Canadian Cyber Centre sources and factual/inference/opinion mapping are retained in evidence/evidence-first-20261104/source-bundle.json. No generated content or human acceptance inferred. Latest checkpoint: evidence/milestones/evidence-first-execution-20261104/phase1.json.

Current checkpoint: Phase2 machine GO. Two actual writer consumer regressions RED→GREEN; full150 PASS after updating the stale injected planner fixture to the expanded input/output contract while preserving original context assertions. Evidence-bound plan and full voice reach drafting. Missing anchor changes actual preflight readiness even with overconfident model ratings. No extra model planning call. Human writing quality remains unproved. Next: Phase3 scorer qualification. Status authority remains CURRENT_WORK_PACKET and actual receipts.

Current checkpoint: Phase3 machine GO. Seven scorer/comparison regressions RED→GREEN; full157 PASS. Writer and evaluator share factual brief, full relevant voice and approved examples; concrete0–5 anchors added. Missing/noninteger/out-of-range ratings become unavailable, never silently fabricated. Baseline can receive the identical evaluator context and rubric; reopen remains zero-call. Weights/90 unchanged, one targeted guarded rewrite. No exact-text human calibration corpus established; calibration remains explicitly missing. Next: Phase4 one substantive bounded comparison. Status authority remains CURRENT_WORK_PACKET and actual receipts.

Fresh review corrections: evidence/milestones/evidence-first-execution-20261104/REVIEW.md. Full171 PASS after reverse source coverage, explicit bound brief propagation, study identity, pre-assessment pair persistence, and strict judgment validation. Central-source omission with peripheral evidence blocks actual CLI admission without provider creation. Native no-evidence negative is retained separately and consumes one execution; no human verdict inferred.

### Phase4 substantive actual trial

Primary-source MFA recovery brief consumed through corrected existing engine. Expected/observed and all10 native prompts/results: evidence/evidence-first-20261104/EVALUATION.md and execution-trace.json. Original73, one safe quality rewrite75, same-rubric simple baseline75. No selected candidate and visual deferred; source grounding did not itself solve report-like voice/familiar framing. These different-topic/different-evaluator results cannot establish causal quality improvement versus earlier trials.30 physical starts,73.838 cumulative CLI seconds, API0; subscription dollar cost unknown. Exact source-to-output mapping and both negative checks retained. Fresh show/duplicate request caused0 new executions. Machine execution GO; P2 human quality/calibration HOLD. No further trial or publication inferred.

### Writing-voice catalogue and consumer correction

The PDF selected identities instead of style profiles. Pinned V2 preset source was recovered (e5608e9; persona_presets blob f008ebd). Nine craft-only runtime projections now reach the existing writer/evaluator/rewriters/baseline independently of author POV and identity. Independent review matched all152 values from8 source templates; ninth reuses authorized local craft traits.17 original RED→GREEN cases plus reviewed source-drift/precedence/schema/trace/default-style penalty corrections; final195 PASS. Original reviewer findings, rulings, expected-vs-observed and exact source/consumer hashes: evidence/writing-voice-selector-20261104/. No native model execution, style-quality judgment or P2 human acceptance inferred. Source and runtime remain a development candidate, unmerged.
