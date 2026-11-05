# CURRENT_WORK_PACKET.md

PACKET_ID: LIG-CONTENT-VISUAL-ACCEPTANCE-2026-09-01
STATUS: active
PROJECT: LinkedIn_Generator
ENTRY_MODE: PROGRAMSTART Mode C
CURRENT_STAGE_OR_MILESTONE: Independent writing-voice selector machine GO; controlled voice comparison ready; P2 human/content acceptance HOLD
AUTHORITY_SPINE: `README.md` product role + Dedication boundary, current explicit operator decisions, accepted project contracts/voice authority, validated implementation state on `main`, and this bounded packet
AUTHORITY_VERSION_OR_COMMIT: main a714d1ef355ade9ca47a52b301ea477bd0c14f34; candidate production code436a165; exact source/config/test hashes and integration/runtime state in latest receipt
BLOCKER_SCOPE: milestone
SAFE_EXECUTION_LANE: A/B — human content acceptance, provider-neutral visual-plan validation, idea preservation, evidence gathering, review, and reversible repo corrections can proceed
BLOCKED_ACTION: paid image rendering, Replicate/render-provider implementation, and publishing remain gated until the current validation evidence is sufficient; final repo-provider acceptance also requires the actual generation path in a runtime with valid provider credentials

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
| Current authority reconciliation | compare live `main` and packet authority | prior reconciliation present on main at a714d1e; v4 continuation delta on feature branch |
| Idea preservation | project ledger follows current PROGRAMSTART non-authoritative semantics | ledger present on main at a714d1e; no idea promoted by this continuation |
| Publish-quality threshold/rewrite | 90+ no rewrite; sub-90 preserves A and creates one B; unsafe B rejected | implemented PR #20; native Codex exercised one guarded rewrite; generated posts remain unqualified |
| Voice/public-language quality | human decisions + reason codes | Trial #1 positive; more trials pending |
| Visual planner contracts/guardrails | focused contract/planner/integration coverage | implemented PR #21; human validation pending |
| Provider-path equivalence | minimum two accepted subjects through actual repo provider | native Codex runtime exercised; >=2 human-accepted subjects still pending; API configuration not qualified |
| Rendering quality | real rendered outputs | intentionally not started |
| Publishing readiness | focused Challenge Gate | pending |

## Trial Evidence

| # | Subject | Gate outcome | Draft A score | Draft B score | Human decision | Visual plan | Notes |
|---:|---|---|---:|---:|---|---|---|
| 1 | AI planning system creating rework by forgetting settled decisions | draft | manual ~87 | manual ~93–95 | keep Draft B | 5-slide carousel concept; human visual-plan validation not yet explicit | Voice confirmed as sounding like Graham; Draft B explicitly liked. Scores are manual review estimates, not repository-provider telemetry. |
| 2 | Draft/visual revision ambiguity | drafted; unqualified | 73 | guard-rejected, not scored | limited preference for original (display B); no editorial approval | deferred | Native Codex connection canary; retain the weak outcome, do not count preference as a quality-gate pass. |
| 3 | Before adding AI steps, show what they improve | drafted; unqualified | 78 | 77 | pending | deferred | Native Codex transparent diagnostic with exact prompts and changes; not a blinded pilot vote. |
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
AUTHORITY_RECONCILED: prior packet update landed on main at a714d1e; v4 continuation delta is on a feature branch, not merged; no competing Master Game Plan
REMAINING_BLOCKERS: multi-subject visual-plan evidence, real repo-provider acceptance, rendered-asset evidence, publishing integration
NEXT_RECOMMENDED_SLICE: complete Trials #2–#5 and run a focused Challenge decision; promote Slice B only if the planner earns it

## v4 continuation — 2026-11-04

Authority: current operator instruction to execute the v4 handoff, begin P0 and the authorized selected-draft contract repair, preserve all 26 AT objectives and 11 E2E scenarios, and continue only through eligible gates.

### Accepted bounded decisions

- Continue the existing Python content engine in this owner. CLI/UI remain future adapters of the same service; no framework/database/cutover is admitted by P1. V2 PR #6 remains an open draft proposal, unchanged.
- Preserve the approved voice sources, current 90 threshold and at most one guarded rewrite. Legacy top-level body remains Draft A; optional selected_candidate is the explicit qualified editorial candidate, with deterministic source:full-content-SHA256 identity and exact UTF-8 body.
- A planned visual must match that candidate source and content hash. Legacy planners may omit the optional hash: the trusted caller binds it to the exact text passed. Declared mismatch or malformed plan defers without retry.
- Adopt the v4 AT-01..AT-26 and E2E-01..E2E-11 as execution targets from docs/implementation/v4/LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md. Keep the existing owner gate; preserve six-subject first-six denominator, up-to-eight subject envelope, >=2 real-provider human-accepted subjects, claims review, human voice/insight/usefulness ratings, sequence originality, measured editing effort and blinded >=4/6 engine preference pilot. A failed pilot means HOLD and diagnosis, not statistical proof of business impact.
- Editorial acceptance remains distinct from Dedication publication approval. P2 GO precedes production P3; rendering and publication retain separate gates. No fixture-only P3 exception has been admitted here.
- All handoff documents under docs/implementation/v4 are preserved planning snapshots. This packet and actual evidence receipts own current execution status.

### Expected versus observed

| Check | Expected | Observed |
|---|---|---|
| QB-00 focused | Existing integration/voice/visual/opportunity tests run | 31 PASS in isolated venv; initial system dependency errors retained |
| QB-00 full | Baseline accurately reported and diagnosed | 99 PASS/1 stale fixture FAIL; same assertions preserved after current signatures/configuration restored; 100 PASS |
| IT-01 initial | New selected-candidate assertions fail before fix | 18 FAIL observed |
| IT-01 repair | Safe B93 selected, A92 selected without rewrite, low/unsafe/missing quality no candidate, terminal preflight no draft/visual | All18 new cases PASS; targeted40/full118 PASS |
| Independent review correction | Malformed declared provenance defers safely | 4 additional RED cases, then 22 candidate tests/full122 PASS |
| P2 live and human | Real provider receipts and exact candidate-bound human verdicts | NOT_RUN; no local generation credential, approved spend envelope or new human verdicts |

Evidence: evidence/v4-20261104/REPORT.md, PROGRESS.md, REVIEW.md, P1-candidate-observations.json, command/UTC/exit/log-hash JSON receipts, acceptance-status.json, and P2_PREPARATION.md.
Current execution environment: isolated VPS feature checkout; no deployment. All enabled GitHub workflow files are absent (only .yml.disabled retained); none were enabled.

P0/P1 disposition: GO for completed local contract milestone, subject to the recorded review fix and final committed-source receipt; this is not hosted-CI, merge or product acceptance.
P2 disposition: HOLD. Three grounded source-backed candidate ideas prepared, none counted as a drafted or accepted subject; no forced sixth subject. Trial #1 remains owner-recorded, not current live-provider evidence.
Next eligible action: secure an admitted provider runtime and explicit spending envelope, approve genuine varied subjects, then run the paired P2 pilot and obtain actual human reviews. Do not bypass P2 with infrastructure work.

## Codex-first continuation — 2026-11-04

The operator requested a quick, economical plan covering the eight Codex-first steps. Controlling slice: [Codex-first trial game plan](docs/implementation/v4/CODEX_FIRST_TRIAL_GAME_PLAN_2026-11-04.md).

This supersedes the proposed US$5/70-call API trial envelope. Paid API budget is zero; no API fallback. Reuse Resume Creator's subscription execution client through one thin adapter, retaining the existing LinkedIn engine and records. First proposed batch: one subject, at most12 model executions and15 minutes cumulative execution; no hidden retries. Subscription allowance is consumed.

Planning is complete; adapter implementation, runtime qualification, new native trials and human verdicts remain NOT_RUN. Planning alone is not model-execution authorization. Preserve all26 AT objectives and11 E2E scenarios. Native engine-integrated Codex receipts may establish that provider's real execution; they do not qualify the unchanged API configuration. P2's factual, human, comparison and corpus gates remain intact.

Next eligible implementation step: follow the short plan through adapter/offline qualification and one bounded comparison pair, subject to actual runtime admission and execution authorization. No new resume W7 invocation, CI, merge, deployment, rendering or publishing is admitted by this planning update.

## Codex-first actual execution — 2026-11-04

Current user explicitly authorized the short plan and all machine-solvable prerequisites. Steps1–6 have actual machine evidence; step7 human verdict and step8 expansion remain open. See evidence/codex-first-20261104/REPORT.md and docs/implementation/v4/LINKEDIN_CODEX_QUICKSTART.md.

GO: local launcher/isolated LinkedIn venv on Execution Node, bridge to pinned Resume subscription client, full142 LinkedIn tests and30 reused-client tests, actual native engine/baseline execution and fresh-process replay with0 additional model launches.
HOLD: native engine A scored73; exactly one B was guard-rejected; selected_candidate remains null and visual deferred. The comparison includes the retained unqualified original for diagnosis only. No new engine invocation was used to rescue the score.
Actual budget:5 native model executions,15 physical starts,49.2318 cumulative CLI seconds, no unknown/in-flight effect. No API key/fallback or API spending; subscription usage cost in dollars is unknown.

Human review: evidence/codex-first-20261104/trial/review.md. Record exact-hash A/B/tie preference, keep/light/structural/reject, voice/insight/usefulness, visual disposition and actual edit minutes. No human verdict is inferred.
First-six denominator remains unfulfilled; no AT04/05/19–26 or E2E06/10/11 PASS is claimed. AT03 controlled deferral is reused; later AT/E2E remain as previously gated. Rendering, CI, merge, deployment and publishing remain unadmitted.

Next eligible action: Graham reviews the first pair; repair only a demonstrated defect or continue to further real subjects after that decision. Do not bypass the content gate with P3 infrastructure.

## Limited feedback and transparent evaluation — 2026-11-04

User explicitly requested recording the earlier display-B preference without overemphasis, then authorized a more transparent evaluation. Saved feedback: evidence/codex-first-20261104/trial/human-feedback.json, exact text SHA2564998b459b8574d1c8cba5cafe8a7c929ffe06769a8758d31e2fffb87f072fa04. This is preference only: no keep/light verdict, ratings, editing-time result, voice-example promotion or publication approval inferred.

New subject draws only on Graham's actual requests for economical Codex reuse and understanding model context/feedback use. Exact brief, sources, voice hashes, all6 actual model prompts/results, original-to-rewrite diff and raw baseline are in evidence/transparent-evaluation-20261104/EVALUATION.md.
Native original78; one safe rewrite77; no selected candidate/visual. Baseline generated once from the same factual/voice context. All original weak outputs remain visible; neither this diagnostic nor the earlier limited preference may silently supply a blinded pilot win or an editorial keep.

Transport and environment remain GO; P2 content acceptance HOLD. Human feedback now should identify factual alignment, a voice mismatch, a useful/unhelpful rewrite change or actual edit, rather than only pick a winner. No new production code, CI, merge, rendering, deployment or publishing occurred.

## Evidence-first phased continuation — 2026-11-04

Current operator decision: strengthen substantive evidence before further opinion-only diagnostics, phase the work, and check local CI plus actual merge/install currentness after each meaningful milestone. Narrow conversational/code observations are evidence of those observations; they do not establish broader client or business outcomes. Opinion is permitted when clearly framed; central factual claims require adequate support, not an arbitrary citation count.

CURRENT_MILESTONE_RECEIPT: evidence/writing-voice-selector-20261104/MILESTONE.json
NEXT_ELIGIBLE_PHASE: Controlled writing-voice comparison; freeze author/story/facts/audience/central argument and vary only writing_voice_id

Controlling plan and execution prompt are the updated v4 companions. Sequence: currentness checkpoint → substantive evidence brief → source-specific writer repair → scorer qualification → one bounded substantive comparison and human disposition → controlled expansion. All26 AT objectives and11 E2E scenarios remain intact. Prior weak trials stay in the record; limited draft preferences are not editorial keeps or approved voice examples. Trial3's simple-baseline preference is limited feedback, not a blinded pilot win.

This milestone changes planning/status documents only. Writer/scorer repairs and substantive new generation remain PLANNED. The milestone receipt records actual local CI, source, PR/main and launcher observations. Native Codex connection remains reusable; no API spend, model launch, hosted workflow, merge, installation promotion, deployment, rendering or publishing is admitted by this documentation update. P2 human/content acceptance remains HOLD.

Phase0 observed:142 tests PASS; acceptance definitions unchanged; relative links valid; initial whitespace-only diff check failed and was repaired, then passed. PR24 remains draft/unmerged; launcher runs candidate checkout, not a merged-main release. See latest receipt.

## Phase1 execution checkpoint — 2026-11-04

Operator authorized execution of the updated prompt. Frozen substantive MFA recovery brief: evidence/evidence-first-20261104/request.json and source-bundle.json. Primary advisory tactics and recommendations are separated from inference/opinion; historical dates and limitations retained. Optional trial source bundle is checked before provider construction, without changing the existing request schema. Source truth still requires research/human review. Five admission fixtures RED→GREEN; full147 PASS; no generation. Source/PR/runtime checkpoint in phase1.json. Continue Phase2; unmerged candidate is not a release.

## Phase2 execution checkpoint — 2026-11-04

Two actual writer consumer regressions RED→GREEN; full150 PASS after updating the stale injected planner fixture to the expanded input/output contract while preserving original context assertions. Evidence-bound plan and full voice reach drafting. Missing anchor changes actual preflight readiness even with overconfident model ratings. No extra model planning call. Human writing quality remains unproved. Source/main/PR/runtime observations: evidence/milestones/evidence-first-execution-20261104/phase2.json. Candidate-only, no merge/install promotion.

## Phase3 execution checkpoint — 2026-11-04

Seven scorer/comparison regressions RED→GREEN; full157 PASS. Writer and evaluator share factual brief, full relevant voice and approved examples; concrete0–5 anchors added. Missing/noninteger/out-of-range ratings become unavailable, never silently fabricated. Baseline can receive the identical evaluator context and rubric; reopen remains zero-call. Weights/90 unchanged, one targeted guarded rewrite. No exact-text human calibration corpus established; calibration remains explicitly missing. Source/main/PR/runtime observations: evidence/milestones/evidence-first-execution-20261104/phase3.json. Candidate-only, no merge/install promotion.

### Fresh review correction before Phase4

Review held c51d737 for source reverse coverage/context propagation, study identity, partial assessment recovery and malformed judgments. All Important findings reproduced and fixed; base persona/goal parity included because same-context comparison is required. Full171 PASS; review-fix.json and REVIEW.md retain findings, RED/GREEN and rulings. Native all-evidence-omitted preflight correctly returned needs_more_evidence (1 model execution). Stronger actual CLI negative retained peripheral Canadian recommendation but omitted central reset facts; admission blocked before provider creation (0 model executions). No post generated yet. Aggregate subject budget remains <=12 executions/900 seconds including the earlier negative.

## Phase4 actual substantive trial — 2026-11-04

Evidence/evidence-first-20261104/EVALUATION.md retains source-backed MFA recovery subject, exact prompts, original/rewrite/baseline, claim mapping, freeze and negative/reopen evidence. Original73, safe guarded quality rewrite75, simple baseline75 under the same rubric/context. Selected candidate remains null, visual deferred. The known engine HOLD was retained; complete-comparison generated only the baseline and its assessment, never regenerated the engine. Aggregate10 native executions/30 physical starts/73.838 CLI seconds/API0; subscription dollar cost unknown.

GO: local machine repairs and source-consumption/recovery checks. HOLD: factual/voice/insight/usefulness human verdict, measured editing effort, calibrated reference corpus, first-six/blinded pilot/corpus/visual gates. No new keep, approved voice example, engagement claim or publication permission inferred. Existing weak trials remain visible. Human review must examine actual retained text; no score-chasing regeneration. Candidate remains unmerged and runtime candidate-only; local tests do not establish a release. Latest phase4 receipt owns exact source/CI/main/PR/runtime observations.

Post-push integration readback: GitHub PR24 head16df725128a7ef8f91befa5cfc0556e246abf1f5, open/draft/unmerged; maina714d1ef355ade9ca47a52b301ea477bd0c14f34. Later documentation/evidence commits reuse full171 only while production/config/tests remain unchanged from f89e3d3.

## Current AI news voice sampler — 2026-11-04

Operator requested a current reputable AI story, several versions per configured voice, and a PDF with linked contents. Prepared3 Graham and3 Ardent drafts using one existing native Codex bridge call per voice, based on CERT-In primary news/advisories. This is explicitly an exploratory sampler, not6 full engine runs, a paired pilot or human acceptance. No scorer used. Original prompts/outputs, source limitations, light presentation edits and actual execution receipts: evidence/ai-news-voice-sampler-20261104/. PDF validated9 pages/8 contents links/9 bookmarks; all pages visually reviewed. No production code/config/test change; prior171 local test result reused for unchanged code. No human keep, voice-example promotion, merge/install/render/publish permission inferred. P2 remains HOLD; next is review of retained writing.

## Independent writing voice — 2026-11-04

Operator authorized the recommended bounded selector repair. Recovered eight V2 presets plus existing Relatable Provocateur now have generic craft-only runtime definitions in config/writing_voices.json. Historical names remain provenance/aliases; biographies, audience fields, stock phrases and example experiences excluded. Optional writing_voice_id travels through the existing request/integration/engine/writer/judge/rewriters/baseline, independently of persona_key and author_pov. Omission retains previous defaults. Explicit selection takes precedence over inherited style and compatible-only examples; default Graham rhythm/contrast penalties cannot steer explicit styles back to Graham. House rules, factual guardrails,90 threshold, one guarded quality rewrite and exact selected/visual provenance remain.

Expected/observed: all9 actual consumers have identical non-style context hash; unknown/malformed selection blocks before model call; style version/hash is visible even on terminal preflight; altered style cannot silently finish a retained comparison; completed historical show/reopen uses original records with0 additional calls. Final195 local tests PASS with original and review RED/GREEN logs retained. No native model call or API spending in this milestone. Fresh review and rulings: evidence/writing-voice-selector-20261104/REVIEW.md. Candidate-only launcher; no hosted CI, merge, install promotion, deployment or publishing.

The previous PDF remains an identity/angle sampler, not controlled voice evidence. No new human keep, approved example or style-quality claim is inferred. Next controlled comparison fixes the author, subject, factual support, audience, objective/argument, model and constraints; only the explicit style changes. All26 AT and11 E2E definitions are retained.
