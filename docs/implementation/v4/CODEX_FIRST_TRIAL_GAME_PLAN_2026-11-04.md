# Codex-First LinkedIn Trial Implementation Plan

**Goal:** Run the existing LinkedIn engine using the Codex subscription route already used by Resume Creator, then compare its writing with one simple prompt.
**Approach:** One thin provider adapter, one trial script, existing engine and existing Codex attempt/recovery records. No framework, database, shared-package extraction or new orchestration.
**Status:** Plan only; adapter, live trial and human verdicts NOT_RUN.
**Execution:** Implement inline in small steps using executing-plans and test-driven-development. This is a subordinate P2 slice; CURRENT_WORK_PACKET.md stays the active pointer.
**Spec:** The operator's eight-step Codex-first direction plus the preserved v4 acceptance objectives.

## Boundaries

- Zero paid API spending and no API fallback. Codex subscription allowance is still consumed.
- Keep the current 90 threshold, at most one guarded rewrite, selected-candidate/visual hashes, approved voices and A/B history.
- Preserve all 26 AT objectives and 11 E2E scenarios. This slice closes only the portions actually demonstrated.
- No new resume W7 invocation or changes to resume results.
- No UI, rendering, publishing, hosted CI, merge or deployment.
- Stop at genuine human review or unavailable subscription admission; resolve ordinary code/environment issues.
- First live batch: one subject, at most 12 model executions and 15 minutes cumulative execution. Count CLI version/auth processes separately and include them in the existing client's physical-process limit. No automatic retry or reset of a spent budget. Broader batches need their own recorded envelope.

## Small file map

- Create `src/app/codex_provider.py`: implement the existing `TextGenerationProvider.generate(model, system, user, temperature) -> str` contract through a thin bridge to Resume Creator's existing `CodexClient.execute_structured`.
- Create `scripts/linkedin_codex_trial.py`: explicit engine/baseline trial entry; retain request, outputs and receipt references in a chosen output directory.
- Create `tests/test_codex_provider.py` and `tests/test_codex_trial.py`: provider wiring, failure/recovery and trial isolation.
- Reuse `src/app/llm.py`, `api.py`, `integration.py`, `visual_assets.py` and current contracts. Reuse the existing v4 scorecard.
- Use the qualified Resume checkout/environment through the bridge; record its exact source revision. Do not import its full application into LinkedIn or copy its client as a second maintained implementation.

## Eight steps

1. **Freeze one real input.**
   - [ ] Choose one grounded subject from P2_PREPARATION.md; discard it if too thin.
   - [ ] Save exact facts/source IDs, audience, author POV, voice/config hashes and input hash.
   - [ ] Keep the human rubric and comparison rules; do not draft six near-duplicates to fill a quota.
   **Done when:** both methods can consume the same frozen factual input.

2. **Reuse the Codex runtime.**
   - [ ] Inspect the current Resume client, its imports/settings and qualified interpreter; record source/CLI versions and subscription authentication without exposing credentials.
   - [ ] Use an explicitly selected, qualified Codex model for every trial stage and baseline. Do not pass the API-only default model through blindly.
   **Done when:** the existing client can be called from a small bridge; installation/login observations are not falsely called inference proof.

3. **Wire the smallest adapter.**
   - [ ] Send the engine's existing system/user prompts through the client with a simple JSON result schema: `{"text": "..." }`; unwrap text for the unchanged LLMClient.
   - [ ] Assign stable run/stage identities and retain original attempt/result references.
   - [ ] Inject this client into drafting, opportunity, quality and visual planning. The trial script must never fall back to default API clients.
   **Done when:** the actual Python engine uses Codex at every model boundary; Codex does not replace the engine with one all-in-one prompt.

4. **Prove the adapter offline.**
   - [ ] Write and observe failing tests, implement the minimum, then run:
     `python -m pytest -q tests/test_codex_provider.py tests/test_codex_trial.py tests/test_selected_candidate.py`
   - [ ] Cover subscription-auth rejection, malformed JSON/schema, timeout/unknown state, exact stored-result reuse, duplicate request, changed-input conflict and budget exhaustion.
   - [ ] Make API construction a test failure; assert no API calls. Opening/reviewing retained outputs must launch zero model executions.
   - [ ] Run `python -m pytest -q`; preserve actual failures rather than weakening checks.
   **Done when:** targeted and affected full-suite checks pass with real command/exit receipts. Fixtures remain fixtures.

5. **Run the one-subject canary.**
   - [ ] Invoke the trial script once through the existing engine, with the declared limits.
   - [ ] Retain A, optional B, selected hash/score, claims/sources, visual plan or deferral, actual Codex receipts, calls and elapsed time.
   - [ ] Unknown execution stops the batch for reconciliation; quota/auth failure does not trigger API fallback.
   **Done when:** one real Codex-backed engine result is reconstructable. This proves this provider/model configuration, not the old API configuration.

6. **Generate the fair baseline.**
   - [ ] Use one plain prompt with identical facts, audience, factual constraints and the same Codex model/settings; provide the same approved voice material.
   - [ ] Keep engine-specific staging out of the baseline. Retain the exact prompt/output without cherry-picked retries.
   - [ ] Randomize display labels and retain the hidden mapping outside the reviewer-facing bundle.
   **Done when:** one honestly comparable pair exists.

7. **Get Graham's verdict.**
   - [ ] Present blinded text, source/claim review and the engine visual plan; distinguish plan usefulness from rendered-image quality.
   - [ ] Ask keep/light edit/structural edit/reject, voice/insight/usefulness ratings, preferred draft and actual editing minutes.
   - [ ] Bind feedback to exact text hashes. Never fill human fields with model scores.
   **Done when:** the first pair has explicit human feedback, including reasons.

8. **Expand only after the first pair.**
   - [ ] If useful, continue in small batches toward six eligible distinct subjects, at most eight subject trials, with varied domains and natural visual formats.
   - [ ] Preserve the existing gate: >=4/6 keep/light, >=2 real-provider human-accepted subjects, supported claims and useful visual plans. For this slice, real provider means the engine-integrated native Codex route, identified as such.
   - [ ] Complete blinded >=4/6 engine preference, corpus originality, voice and edit-effort checks. Ties are not wins; insufficient legitimate subjects means NOT_YET_EVALUABLE.
   - [ ] Update the packet and scorecard with GO/HOLD/FAIL, receipts, blockers and next action.
   **Done when:** P2 has actual evidence supporting its disposition; one canary alone never closes P2.

## Practical checkpoints

**A:** Adapter + offline tests green.
**B:** One actual engine/baseline pair ready for human review.
**C:** Human-reviewed first pair; expand or repair the smallest demonstrated defect.
**D:** Six-subject P2 disposition before production P3 or rendering.

Self-check: all eight requested steps are mapped; no API spending dependency, parallel architecture, hidden generation, relaxed quality gate or invented acceptance. The first deliverable is one working adapter and one reviewed pair, not a platform rebuild.
