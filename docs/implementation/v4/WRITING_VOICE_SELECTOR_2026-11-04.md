# Independent Writing Voice Selector — bounded implementation

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
