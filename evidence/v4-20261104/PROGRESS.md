# Execution ledger — v4 LinkedIn Generator continuation

Plan: docs/implementation/v4/LINKEDIN_GENERATOR_GAME_PLAN_V4_2026-11-04.md
Spec: docs/implementation/v4/LINKEDIN_GENERATOR_TEST_OBJECTIVES_AND_SUCCESS_CRITERIA_V4_2026-11-04.md
Base: a714d1ef355ade9ca47a52b301ea477bd0c14f34
Workspace: isolated fresh clone, feature branch fix/selected-candidate-v4-20261104.

Pre-flight: P1 selected body/ID/hash is the common input for later visual, export, headless and UI consumers. Legacy body stays A; no later consumer may infer selection from body. P2 must precede P3 production and P6 rendering. Human approval and provider receipt cannot be replaced by fixtures.

P0: current Paths guide ba7463b91398ae9378a4ad09eba4974dedd5df40; live primary README and packet refreshed. V2 PR6 open/draft/unmerged at 6f093236da24ee5953e0668da3b63ebbd369b647; no V2 effects. Dedication README adbdc1ba0952e98a60461ae3f7c2fcaf17450632 confirms canonical state/orchestration boundary.

Ruling: execute the user-authorized compatible P1 correction in the current Python owner; the competing V2 draft does not supersede default-branch owner authority. No cutover or new framework is chosen. Cost if wrong: broader product architecture still requires reconciliation at the later architectural milestone.

P0 route: scratch git mirror clone failed for missing username. VPS gh clone recovered the same repository; no global outage. Older VPS Paths checkouts lacked new scripts; fresh clone d6eea4daa0fb5a90dfa02be60941354b3576ac92 supplied the catalog and diagnostic. paths-diagnosis.json retains classification.

P0 baseline: system Python lacked pydantic (focused 6 collection errors; full17 collection errors, exit2). Isolated venv installed declared requirements plus pytest. Focused31 PASS. Full99 PASS/1 FAIL, stale FakePipeline configuration/signatures. Retained every assertion, refreshed fixture to current dependency boundary; full100 PASS. No production fix to hide this failure.

P1: new selected-candidate tests observed18 FAIL, then targeted40 PASS/full118 PASS. First code commit e856859c044213458bbc1a0cb68df0e3ec87a55d; committed full suite118 PASS. Candidate observations retain actual fixture A/B, hashes, planner inputs and call counts.

Final review: one Important malformed provenance finding; four regression failures observed before repair. See REVIEW.md and REVIEW-01 receipts. No minors deferred.

P2: preparation only, real provider and human acceptance HOLD. Local process has no configured provider key; spending not approved. All26 objectives/11 scenarios preserved. No live generation, human rating, render, publish, merge, deployment or hosted CI occurred.
