# Codex-first execution ledger
Plan: docs/implementation/v4/CODEX_FIRST_TRIAL_GAME_PLAN_2026-11-04.md
Base: 5bc99fb70bb1c3963f09bbaa4fa1c2a231c587d7.
Execution authorized by current user to complete all machine-solvable work.

Preflight: API default model must not leak into Codex stages; one injected client supplies draft/opportunity/quality/visual; baseline uses same model and approved voice facts. Original selected-candidate contract remains.
Ruling: run on Execution Node where the qualified Codex login/environment exists; keep VPS as source/test evidence only. Cost if wrong: installed execution environment must be requalified, not disguised as API equivalence.
Ruling: use a detached pinned Resume source snapshot and existing interpreter, called through a small subprocess bridge. No resume runtime/source/results are changed. Cost if wrong: this intentionally local dependency needs repinning if its interpreter or qualified CLI changes.
Ruling: existing client counts three physical starts per new model request (version/auth/exec). One shared invocation has max36 starts and900 cumulative seconds, giving at most12 model executions. No budget reset. API temperature is recorded as requested but not applied by Codex; actual model/reasoning are the comparable settings.
Baseline: VPS full122 PASS; initial EN use of resume venv lacked pandas. An isolated LinkedIn venv installed declared dependencies; resume environment unchanged.
New adapter/trial tests first failed because the modules did not exist. Targeted34 PASS after implementation. Actual full/client outcomes recorded separately.
Human review remains pending; no generated quality score may substitute.

Actual results: full142 LinkedIn tests PASS; reused client30 PASS. Native original A73; one rewrite guard-rejected; no selected candidate/visual. Native engine4model executions. Explicit comparison-only recovery added after2 observed failing regressions; it used retained A and generated1baseline, not another engine attempt.
Independent review:2Important findings,6RED regressions, fixes and full142green. No minors. Review excludes human judgments and the later comparison-only delta; that delta has separate regression/native evidence.
Actual launcher show and duplicate generate in fresh processes left the shared budget unchanged at5model/15physical/49.2318sec. Human review pending.
Ruling: allow comparison of retained rejected engine text for measurement without promotion; missing selection still blocks normal generation success, unknown effects still block continuation. Cost if wrong: comparison completion could be mistaken for product acceptance, so engine_gate explicitly remains HOLD_NO_QUALIFIED_CANDIDATE and original failure is retained.
