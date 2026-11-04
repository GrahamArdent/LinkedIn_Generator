# LinkedIn Generator v4 — P0/P1 actual outcome and P2 HOLD

## Disposition

**GO: P0 baseline verification and authorized P1 selected-draft correction, locally qualified.**
**HOLD: P2 real-provider/human content acceptance.** P3–P7 remain gated; all26 AT objectives and all11 E2E scenarios are retained.

Tested final source commit: `1afd1b3738dba1eada53d8839d77fe6699c9b085`.
Base: `a714d1ef355ade9ca47a52b301ea477bd0c14f34`.
Feature branch: `fix/selected-candidate-v4-20261104`.
Actual final full-suite check: 2026-11-04T21:56:47Z, Python3.14.4, isolated declared-dependency venv.
Command: `.venv/bin/python -m pytest -q`; exit0; **122 passed**.
Receipt: [P1-final-committed.json](P1-final-committed.json); [full output](P1-final-committed.log).
No hosted CI, deployment, merge, provider generation, rendering or publishing was run.

## Expected versus observed

| Requirement | Actual observation | Evidence |
|---|---|---|
| QB-00 truthfully reports baseline | Focused31 PASS. Full99 PASS/1 FAIL due stale test double. System Python's missing pydantic errors retained separately. After declared environment and unchanged-assertion fixture repair, full100 PASS. | QB-00*.log/json; environment-install.log; environment-freeze.txt |
| A87 → safeB93, one rewrite | Selected rewrite score93; legacy body still A; review preserves A/B; planner receives exactly B and its attached hash matches B bytes. | P1-candidate-observations.json; test_selected_candidate.py |
| A92 needs no rewrite | Selected original score92, zero rewrites; selection also works when visual planning is disabled. | same observations, candidate tests |
| Unsafe/low/missing/malformed quality | No selected candidate or renderable plan. Unsafe B is retained, never accepted. No planner call on disqualification. | candidate tests; REVIEW-01/P1 receipts |
| Terminal weak evidence | Real pipeline with injected opportunity response returns skipped/needs_more_evidence, empty body, no full-draft or planner call; one question for the latter. | candidate tests + existing opportunity tests |
| Exact identity | Deterministic source:full-SHA256; UTF-8 whitespace/non-ASCII preserved; JSON roundtrip keeps selected text. | test_selection_hashes_exact_utf8_bytes_and_is_stable |
| Wrong visual provenance | Wrong source/valid wrong hash defers; malformed hash/source schema now defers while preserving valid selected text, with no retry. | REVIEW.md; REVIEW-01-red/green; P1-final-committed |
| Tests can catch defects |18 new tests observed red before repair;4 reviewer regressions observed red before repair;22 candidate cases now green. | IT-01-red.log; REVIEW-01-red.log; REVIEW-01-green.log |
| All acceptance targets preserved |26 AT records and11 E2E records with separate fixture/human states. AT01/02 fixture PASS; AT03 human portion open; later E2Es NOT_RUN/HOLD. | acceptance-status.json; preserved v4 objectives |

The inherited test named end_to_end_generation is fixture engine integration. None of these results is a live/CLI/browser/render/publish E2E PASS.

## What changed and what remains

Production change is limited to contracts.py and integration.py: optional SelectedCandidate, optional visual content hash, one selection decision, strict review interpretation, compatible top-level body, provenance mismatch/malformed-plan deferral. No new engine, UI, persistence, provider, scheduler, renderer or publication authority.

The baseline test double in test_api_contract.py now matches current configuration and signatures; original assertions remain. Independent review identified one Important edge case, fixed with observed RED→GREEN and a green full suite. Review limitations/rulings are in REVIEW.md.

Current work packet adopts the operator's v4 continuation targets while preserving the existing live/human gate and Dedication boundary. Historical handoff wording is preserved as a snapshot; it does not overwrite observed execution status.

## P2 next eligible action

[P2_PREPARATION.md](P2_PREPARATION.md) contains three evidence-backed candidate ideas, a frozen blinded comparison/review protocol and a proposed spending envelope. They are not generated or approved subjects and do not satisfy the required cross-domain corpus or six-subject denominator.

Observed local runtime has no generation credential configured. This does not establish ecosystem-wide absence. A live trial also needs explicit spend approval, current admitted provider configuration, cost/call enforcement and actual human review. Proposed envelope: US$5 maximum,70 dispatches maximum,15 minutes cumulative provider time maximum; not approved or spent.

Next: approve budget/credential route and genuine varied subject inputs, run P2 with actual receipts, then obtain exact-candidate human verdicts and blinded preferences. No production P3 exception has been admitted. Rendering, CI, deployment and publishing retain their separate gates.
