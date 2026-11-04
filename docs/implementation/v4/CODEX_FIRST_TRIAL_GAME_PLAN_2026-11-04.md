# Codex-First LinkedIn Trial Game Plan

**Goal:** Use the existing LinkedIn engine with the Resume Creator Codex subscription route. Prove one useful post before expanding.
**Status:** Plan only. No adapter implementation or new model execution has occurred.
**Approach:** One thin adapter, one trial script, existing engine and Codex attempt records. Implement inline with test-first corrections; no platform rebuild.
**Authority:** CURRENT_WORK_PACKET.md remains active. This is its bounded P2 slice; retain all26 AT objectives and11 E2E scenarios from the v4 acceptance file.

## Keep it small

Zero API spending or API fallback. Preserve approved voices, score90 threshold, at most one guarded rewrite, A/B history and selected-text/visual hashes. No UI, new database, renderer, publisher, shared-package extraction, hosted CI, merge or deployment. Do not rerun resume W7 or alter its results.

First batch: **one subject, maximum12 model executions and15 minutes cumulative execution**. Count CLI preflight processes separately within the reused client's physical-process budget. No hidden retries or budget resets. Subscription limits still apply.

## The eight steps

1. **Prepare one real subject.**
   - [ ] Choose a grounded subject from P2_PREPARATION.md; skip if thin.
   - [ ] Save facts/source IDs, audience, POV, voice/config hashes and the exact input. Keep human scorecard fields blank.
   **Pass:** engine and baseline have the same frozen facts. No invented personal event.

2. **Reuse the working Codex route.**
   - [ ] Inspect Resume Creator's current `CodexClient.execute_structured`, qualified Python environment, CLI version and subscription login.
   - [ ] Record its source revision and explicitly choose a supported qualified Codex model.
   **Pass:** a small bridge can call the existing client. Login alone is not inference proof.

3. **Add one provider adapter.**
   - [ ] Create `src/app/codex_provider.py`, implementing the existing `TextGenerationProvider.generate(model, system, user, temperature) -> str`.
   - [ ] Through the bridge, pass existing prompts to the Resume client with a simple JSON object containing `text`; unwrap that field. Reuse its attempt/recovery records rather than copying the resume app.
   - [ ] Create `scripts/linkedin_codex_trial.py`; inject the adapter into drafting, opportunity, quality and visual planning. Select the same Codex model throughout; do not inherit the API model accidentally.
   **Pass:** the Python engine makes every generation decision; Codex supplies model responses.

4. **Check it offline first.**
   - [ ] Add `tests/test_codex_provider.py` and `tests/test_codex_trial.py`. Observe relevant failures before fixing them.
   - [ ] Cover wrong auth, malformed output, timeout/unknown state, identical-request reuse, changed-input conflict and exhausted budget. Reopening results launches nothing; API construction must fail the test.
   - [ ] Run those tests plus `tests/test_selected_candidate.py`, then `python -m pytest -q`.
   **Pass:** actual targeted/full-suite receipts; fixtures clearly labeled.

5. **Run one real engine canary.**
   - [ ] Use the trial script under the first-batch limits. Save A/B, selected hash, score, claims/sources, visual plan or deferral, run/stage/attempt refs, actual launches and elapsed time.
   - [ ] Stop/reconcile unknown execution; never fall back to the API.
   **Pass:** one reconstructable native Codex-backed engine result. The old API configuration remains unqualified.

6. **Generate one fair baseline.**
   - [ ] Use one plain prompt with the same facts, audience, factual constraints, approved voice material and Codex model/settings.
   - [ ] Retain exact prompts/results; no cherry-picked retries. Randomize display labels and keep the method mapping outside the reviewer bundle.
   **Pass:** one comparable blinded pair.

7. **Get Graham's review.**
   - [ ] Present both drafts, source/claim checks and the engine visual plan.
   - [ ] Record keep/light/structural/reject, preferred draft, voice/insight/usefulness ratings, visual value and actual edit minutes, against exact hashes.
   **Pass:** real human feedback. Model scores cannot fill these fields.

8. **Expand only if useful.**
   - [ ] Continue in small, separately bounded batches toward six eligible distinct subjects, at most eight trials, across varied domains/formats.
   - [ ] Preserve >=4/6 keep/light; >=2 human-accepted native-provider subjects; supported claims; useful visual plans; voice/originality review; blinded >=4/6 engine preference; measured edit effort. Ties are not wins.
   - [ ] Record Codex as the integrated live provider, not an API-equivalence pass. Insufficient genuine subjects means NOT_YET_EVALUABLE.
   **Pass:** update packet/scorecard with P2 GO/HOLD/FAIL and evidence. One canary does not close P2.

## Finish line

**First milestone:** adapter tests green → one real engine/baseline pair → Graham's verdict.
**Later:** six-subject P2 disposition before production P3 or paid rendering.

Self-check: all eight steps covered; existing architecture reused; no paid-provider dependency or relaxed acceptance. Layers can follow demonstrated need.
