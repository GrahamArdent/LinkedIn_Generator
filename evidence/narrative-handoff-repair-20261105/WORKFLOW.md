# Reproduce the narrative handoff correction

Source branch: fix/selected-candidate-v4-20261104. Initial implementation d15bda2fca3f87386007652bb9ba11ce6d853f7c; annotation-prompt refinement 62654ffbc44ae60e08cfed7bfc09c535184e65ae. This is the existing Python engine plus its existing Codex subscription provider. No second content engine, provider or workflow service was installed.

## Contract and order
1. Recover the prior supported meaning from the eight-route controlled-brief.json. Preserve thesis, consequence, two facts with actual claim/source IDs and qualification. No model call is needed to copy or freeze these data.
2. Recover route2's selected office-key symbol. ADMISSION.json records the normalization: retain the first three mappings, omit the containment-room mapping outside the shared two-fact lock, and express image/mechanism/boundary/action as bounded planning beats. The literal branch has an explicit explanation outline. Only narrative form/order and the corresponding delivery annotations vary.
3. freeze_handoff creates a detached, validated copy of meaning and narrative. It does not ask a model to rewrite or summarize the selected form away.
4. Optional plan_writing makes one isolated call returning only beats[{index,delivery}] and attribution[{claim_id,source_name}]. It cannot return a title, body, editorial object, replacement narrative or replacement thesis. Short fragment target80-160 characters; hard maximum240. Every selected beat and fact attribution must be covered once, in order. Publisher attribution is bound to that fact's source IDs.
5. attach_writing_plan validates annotations and carries the original selected narrative unchanged. Invalid planning output is HOLD before drafting; raw output remains retained. Structural checks do not prove that arbitrary natural-language fragments contain zero prose or zero semantic error.
6. The actual run_generation API receives editorial_handoff plus the same author/audience/voice/evidence. Its selected-voice projection keeps the handoff independently of its reduced generic plan. The writer uses the explicit narrative order and voice within that form. The same handoff reaches the existing evaluator/editor context, proven by real-consumer fixture tests.
7. FirstDraftOnly records the actual API's first drafting consumer request/result and deliberately stops before deterministic selection, critics, humanizers, finalization or publish scoring. Raw drafts are never edited. This live diagnostic is not a full engine or publishing acceptance run.
8. Shuffle labels before the model audit. Human review, actual editing time and any winner remain pending.

The optional headless Python argument currently supports literal and symbolic forms only. Existing omitted-selection callers retain their behavior. Do not coerce the other six catalogue narrative forms into literal; their extensions or HOLD decisions must be explicit. No UI/HTTP contract, scorer threshold, voice catalogue or paid provider was changed.

## Actual execution and setup HOLD
Initial admitted batch: at most5 calls/900 CLI seconds, one concurrent call, zero API spend, no automatic retry. It used3 calls: literal plan, literal raw draft, symbolic plan. Symbolic delivery fields251 and241 exceeded the existing240 guard, producing HOLD and no symbolic draft.

A separately declared recovery batch allowed3 calls/900 seconds. It refined only planning guidance to reference claim IDs and aim below the hard ceiling. It did not loosen the guard or regenerate an existing draft. The recovery produced the corrected symbolic plan, its first raw draft, then the blinded audit. Original HOLD, raw plan and original executing script remain: symbolic-outcome.json, symbolic-plan.json, run-initial.py. run.py has subsequent explicit budget/recovery compatibility changes; recover.py is the exact recovery entry point. Native request/result/attempt files retain effective prompt and execution truth.

## Commands and environment
Use the existing candidate checkout /home/graham/work/linkedin-codex-trial-20261104 and its .venv; .codex-linkedin.local.json binds the existing pinned Resume client/interpreter, gpt-6-astra medium and ChatGPT authentication. Credentials stay in the Codex store. Native API temperature is not applied; model/reasoning are pinned. No paid API fallback.

The initial command was PYTHONPATH=. .venv/bin/python evidence/narrative-handoff-repair-20261105/run.py run. The retained run-initial.py records the initial script bytes. The explicit recovery command is PYTHONPATH=. .venv/bin/python evidence/narrative-handoff-repair-20261105/recover.py. Do not run historical scripts to obtain a new sample.

After completion, run.py run and recover.py reopen the saved outcomes/audit under their binding checks; REPLAY.json proves zero added native calls. For read-only archive verification use:
```bash
python3 evidence/narrative-handoff-repair-20261105/verify.py
```
This requires only Python standard library. Verify the manifest before reopening with application code. A fresh sampling experiment requires new evidence paths/run IDs and a new declared budget. Running/failed/unknown stage records must be reconciled, not overwritten.

## Tests and interpretation
Baseline209 passed. Initial regressions observed8 failures/1 pass; actual planner tests observed2 failures/9 pass; unrelated-source attribution observed1 failure/11 pass. Logs preserve those RED results. One old API-contract test also exposed an extra None field for omitted selection; the fix omitted that key without changing the test. Final full suite221 passed. Individual RED process exit codes were not separately persisted by the tail wrapper; failure counts are in the logs.

Tests prove preservation/validation and actual consumer context, not compelling writing or factual infallibility. Native outputs show different telling with the same thesis and two incident facts; the symbolic draft adds source-supported action detail and the literal draft assumes checks happen at screens. REPORT.md distinguishes semantic differences, factual concerns and human acceptance. No scores or editing estimates are human measurements.

RESOURCE_USE.json contains actual run/attempt/thread IDs and provider usage; missing provider response IDs are unavailable. FILES.sha256.json covers packet payloads, excluding itself, transient locks/bytecode and the separately retained archive receipt. ARCHIVE_VERIFICATION.json records a clean git-archive check. Historical eight-route evidence remains unchanged.
