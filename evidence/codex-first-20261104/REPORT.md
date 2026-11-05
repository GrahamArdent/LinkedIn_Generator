# Codex-first LinkedIn trial — actual result

## Outcome

**GO: quick local Codex connection and environment.**
**HOLD: P2 writing acceptance and expansion, pending Graham's review.**

The installed local launcher uses the original LinkedIn Python engine and a thin bridge to the pinned Resume Codex client. No API key, paid API fallback, hosted CI, merge, external deployment, rendering or publishing was used.

Source commits: initial adapter/native engine `769950ad850340868e85f6d8222d21ff0f90ad20`; comparison/recovery correction `af2d458f879e3e4a4520a70851d1af3b73e79e8b`.
Reused Resume source: `a609c6d344037152c24cb81baabdb0fd9a6e9b00`; Codex CLI0.158.0, ChatGPT authentication, gpt-6-astra, medium reasoning.
The source snapshot is isolated; the installed resume launcher/results were not changed.

## Expected versus observed

| Check | Expected | Observed |
|---|---|---|
| Provider integration | Existing engine uses Codex for every model boundary, never API | Native receipts show ChatGPT/native_cli for every attempt; provider injected into draft, opportunity, quality and visual planner |
| Offline adapter/trial checks | Auth/output/unknown/replay/conflict/budget behavior verified | Final full LinkedIn suite142 PASS; reused client focused30 PASS |
| One-subject canary | Real result or truthful quality deferral | Opportunity82; original quality73; exactly one rewrite, rejected by existing deterministic guard; selected_candidate=null, visual deferred |
| Baseline comparison | Same model, facts, audience and approved voice material; no cherry-picking | One baseline generated; original engine result reused without regeneration; randomized pair saved |
| Reopen and duplicate request | Zero additional model executions in fresh processes | Actual launcher show + repeated generate returned saved result; budget byte-equivalent, additional model executions0 |
| Bounded execution | <=12 model executions /900 cumulative seconds |5 model executions,15 total physical processes,49.2318 cumulative CLI seconds; no in-flight process |
| Human acceptance | Explicit exact-hash verdict | NOT_RUN; human fields remain null |
| Later P2 gates | Six eligible distinct subjects + quality/comparison/corpus evidence | NOT_YET_EVALUABLE; one subject is not P2 PASS |

The initial engine command exited2 with NO_QUALIFIED_CANDIDATE. That was a genuine editorial gate result, not a broken connection. [native-trial-receipt.json](native-trial-receipt.json) and [trial/engine-gate-failure.json](trial/engine-gate-failure.json) preserve it. The explicit comparison-only completion exited0; it never promoted the draft or generated another engine candidate. Completed comparison state is distinct from engine quality HOLD.

The simple baseline added hashtags despite the empty supplied hashtag list. Preserve that observed correction burden; do not silently remove them or resample. No human preference or time saving is inferred from model scores.

## Review and bounded corrections

Independent read-only review found two Important defects: missing/broken terminal bridge receipts were misclassified as known failure, and baseline input omitted services/targets/hashtags. Six additional regressions failed before correction, then the full suite passed142. Missing/non-object terminal receipts now become unknown and latch the provider; all explicit constraints are carried into the baseline.

Two additional regressions qualified comparison-only completion from a known quality-rejected result while blocking unknown recovery. The reviewer did not inspect that later delta; its actual tests and retained-native use are the proof here. No Critical or Minor issue was reported.

Rulings: use the Execution Node's qualified environment; pin the reused client without copying its implementation; preserve Codex's actual reasoning configuration rather than pretend API temperature applies; measure rejected engine text instead of rerunning it to force a passing score. These are local trial choices, not a new architecture or authority to publish.

## Evidence and exact commands

- `.venv/bin/python -m pytest -q` → exit0,142 passed: [final-full.log](final-full.log).
- Reused client: `/home/graham/work/resume-v6-smoke-venv/bin/python -m pytest -q tests/test_codex_cli_client.py` from its backend → exit0,30 passed: [reused-client-tests.log](reused-client-tests.log).
- First native command and comparison completion, exact source/UTC/exit/log hashes: [native-trial-receipt.json](native-trial-receipt.json), [comparison-completion-receipt.json](comparison-completion-receipt.json).
- Fresh-process commands, original attempt IDs and unchanged budget: [fresh-process-reopen.json](fresh-process-reopen.json).
- Exact request: [request.json](request.json). Selected/voice/source binding, original outputs and lifecycle/usage: trial directory and source manifest. Subscription billed-dollar cost is UNKNOWN; API spending authorized/used0.
- [Blinded drafts for Graham](trial/review.md); mapping is kept separately and should remain unopened until preference is recorded.
- [Connection and command guide](../../docs/implementation/v4/LINKEDIN_CODEX_QUICKSTART.md).

## Next action

Graham reviews Draft A/B or tie, keep/light/structural/reject and voice/insight/usefulness, with actual editing time. Keep the engine unqualified unless independently rechecked after an explicitly chosen edit. Do not expand to more subjects or rendering before the first-pair human decision.
