# Independent Writing Voice Selector — bounded implementation

> Current owner-adopted correction — November 5, 2026: `essential-checks-v1` replaces numeric90 admission in the current source candidate. All four essentials must pass with reasons: factual integrity, reader relevance, practical value and argument/voice fidelity. Scores are advisory; missing evidence pauses; failed essentials allow at most one guarded targeted rewrite; unavailable evaluation fails closed. Passing means human-review eligibility only. Evidence: `evidence/essential-review-gate-20261105/REPORT.md` and `MILESTONE.json`. Installed release0c099d7 remains on its historical90 policy until separately promoted. This supersedes older90 instructions below for new source runs; historical receipts remain immutable. All26 AT/11 E2E and human/visual/baseline/publishing obligations remain.


Goal: separate author identity from writing style in the existing Python engine. Operator authorized this repair after the read-only recovered catalogue.

Spec: hold author, story, factual evidence, audience, objective/central argument and generation settings fixed; vary only a verified style definition. Preserve all26 AT/11 E2E obligations and existing90/one guarded quality rewrite/selected-visual identity.

- [x] Add failing actual-consumer tests for nine style projections (eight recovered templates plus current Relatable Provocateur), alias lookup, unknown rejection, equal inputs, judge/baseline parity and zero-call reopen.
- [x] Add one versioned config and small style resolver. Reuse pinned V2 preset traits, not its biographies, target audiences, stock phrases, anecdotes or author-imitation instructions. Generic runtime names; legacy names remain provenance/aliases only. Keep existing Graham/Ardent identity behavior when selection is omitted.
- [x] Carry optional writing_voice_id through request -> integration -> run_generation -> writer/judge/guarded rewrite and baseline. The explicit selected style governs tone/rhythm/structure; existing factual/POV/safety boundaries remain.
- [x] Record exact selected style version/hash in telemetry. Unknown or malformed explicit IDs fail before generation; no fallback to an empty profile.
- [x] Run focused and full local CI, review coherent diff, preserve observed RED/GREEN and fix Important findings. Reconcile packet/plan/prompt/evidence plus candidate/main/PR/runtime states.

No new engine, database, UI, automatic publishing or scorer changes. No paid API, hosted CI, merge, deployment or installation promotion. This slice qualifies controlled prompt flow; actual perceptible voice differences and human writing quality remain open. No new posts are required to claim the selector works. A later controlled writing comparison must retain exact frozen inputs and actual prompts, varying only writing_voice_id; machine fixtures cannot stand in for that human result.

Interfaces: config/writing_voices.json -> src/app/writing_voice.py:resolve_writing_voice(id)->prompt-safe style block; LinkedInContentRequest.writing_voice_id optional -> run_generation -> _persona_profile writing_voice block -> existing draft/evaluator/rewriters and baseline voice_context.

Review focus: conflicting default vs selected guidance; aliases and missing config; leaking identity/source examples; baseline parity; unknown IDs and cold replay. Existing dated evidence directory is the execution ledger; no parallel authority registry.

## Observed result

17 initial RED cases became GREEN; fresh-review fixes reproduced5 further failures and preserved safety checks. Final195 local tests PASS. All9 resolved styles share one identical non-style prompt/context hash in consumer-observations.json. Aliases are exact, definitions type-checked, and style version/content SHA256 recorded. Unfinished retained comparison refuses changed definitions; completed historical replay remains0-call. No new native model calls or API spending. Human perceptible style/quality still NOT_EVALUATED. Receipt: evidence/writing-voice-selector-20261104/MILESTONE.json.

## Controlled writing-voice comparison — 2026-11-04

Current receipt: evidence/controlled-voice-comparison-20261104/MILESTONE.json and REPORT.md. Nine actual unedited first drafts now hold Graham Hill, story, facts, audience, argument, model and constraints fixed; only the verified writing_voice changes. The existing drafting stage is isolated before critic/humanizer/scoring, so these are not full engine acceptance runs. Nine native model executions,27 physical starts,107.900 cumulative CLI seconds/API0; fresh-process reopen adds0 calls. Frozen product/config/tests and26 AT/11 E2E definitions remain unchanged. PDF:13 pages, linked contents, raw text verified and all pages visually reviewed.

Fresh full local CI:195 PASS (1.96s); log retained. Machine result GO; human voice/quality acceptance HOLD. All9 hooks begin “An approval screen”; factual paragraphs and takeaways are similar. Preserve this weak differentiation finding and do not infer a winner or regenerate to manufacture contrast. Earlier identity/angle sampler remains historical. Next eligible action is human inspection of retained drafts and specific passage feedback; no scoring/keep/example promotion inferred. Candidate-only/unmerged; no hosted CI, installation promotion, deployment or publishing.

## Three-style native comparison — 2026-11-04

CURRENT RESULT: machine GO; useful differentiation modest/observable; human quality and nine-style expansion HOLD. Latest receipt: evidence/effective-voice-comparison-20261104/MILESTONE.json; raw drafts: COMPARISON.md and per-style JSON; expected/observed and limitations: REPORT.md in that directory. Exact tested implementation e11b384; full207 PASS and source/config/tests unchanged afterward.

Actual Codex batch:3 first drafts,9 physical starts,35.997 cumulative CLI seconds/API0; distinct native requests/threads/results and exact output hashes. Fresh-process reopen exit0 with0 added calls. Within this batch all non-style input is identical; only3 version2 styles vary. Counts162/162/168 words; approximate sentence averages12.46/13.50/16.80. Concise compresses, reflective emphasizes qualified responsibility, technical develops a causal dependency and ends on scope limits. Shared early factual summary and similar overall reasoning remain. These are descriptive observations, not scores or human acceptance; combined repair is not single-factor causal proof. Shared central argument/recommendation is deliberately controlled.

Superseding next action: owner exact-text feedback on these3 retained versions; no expansion or automatic rewrite/retuning. Preserve weak nine-style results, all26 AT/11 E2E, original simpler-LLM pilot requirements, measured editing-effort and visual gates. Drafting-stage diagnostic only; full engine/baseline paths verified offline, not natively accepted by this batch. Candidate-only/unmerged; no hosted CI, merge/install/deploy/render/publish.
