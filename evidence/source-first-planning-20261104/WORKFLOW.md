# Replicate the source-first planning experiment

This directory is the complete experiment packet. Start with REPORT.md for the observed outcome and MILESTONE.json for the machine receipt. The public primary source HTML, extracted advisory bodies, exact planner input/output, source review, compiled common brief, native attempts, engine/baseline outputs and verification manifest are retained here.

## Workflow and decision ownership

1. Fetch the October and November primary advisories. extract_sources.py saves original HTML and extracts the full advisory editorial body with Python's standard HTML parser. It excludes scripts/navigation before the advisory ID and the site disclaimer/footer. sources.json records URLs, UTC retrieval times and both byte hashes.
2. Resolve Graham's individual POV and Technical Explainer v3 before planning. run_planner.py gives the model the full source bodies, audience and expertise area. Its system task asks for one useful point, supporting passages, reader action, forwarding rationale, format and limitations. Prior drafts, scores and the old payment thesis are withheld.
3. Retain the raw JSON plan. The assistant checks every exact excerpt against the source and reviews whether the plan adds a supported mechanism or concrete action. brief-review.json records this editorial admission. Verbatim matching alone does not prove entailment or writing quality.
4. On GO, compile_brief.py converts the admitted plan into the existing request/source-bundle contract. All seven selected factual claims remain supported and typed. The complete plan travels in the bundle. request.json and source-bundle.json are shared by both writers.
5. run_pair.py reuses the existing run_trial and complete_comparison. Engine drafting/evaluator/single guarded rewrite are exercised with opportunity preflight and visuals disabled for this fixed-subject diagnostic. The simple baseline receives one drafting call. Both use the same model/reasoning, voice and factual/semantic context. A known engine qualification HOLD can finish the baseline without rerunning the engine.
6. Verify native request/output bindings, identical evaluator context except post, exact file hashes and zero-call cold reopening. Record actual time/call resources and inspect the raw writing. Human approval remains explicit.

## Environment

Repository GrahamArdent/LinkedIn_Generator, branch fix/selected-candidate-v4-20261104. Observed checkout /home/graham/work/linkedin-codex-trial-20261104 on Execution Node. Use current default-branch GrahamArdent/paths/CHATGPT.md for access/recovery in another chat.

The existing ignored .codex-linkedin.local.json selects the pinned Resume Codex client, its Python executable, gpt-6-astra and medium reasoning. ChatGPT CLI authentication is reused. Credentials stay in the existing authentication store. Source commit and config hashes are in manifest.json. Native receipts capture exact model version, source binding, attempt and thread identities.

## Inspect and reopen this completed experiment

Run from the checkout.

```bash
.venv/bin/python evidence/source-first-planning-20261104/verify.py
PYTHONPATH=. .venv/bin/python evidence/source-first-planning-20261104/run_planner.py --show
PYTHONPATH=. .venv/bin/python evidence/source-first-planning-20261104/run_planner.py
PYTHONPATH=. .venv/bin/python evidence/source-first-planning-20261104/run_pair.py
```

The completed planner and trial reopen their saved results. verify.py checks the saved files without provider access. The completion receipt records the observed zero additional native launches. A running, failed or unknown state requires original-receipt reconciliation.

## Reproduce a fresh experiment

Use a new evidence directory and new run ID. Copy the scripts and adjust their OUT/run-ID literals to that directory/identity. Declare the complete batch budget before launch. Preserve this original directory.

```bash
python3 evidence/NEW_DIRECTORY/extract_sources.py
PYTHONPATH=. .venv/bin/python evidence/NEW_DIRECTORY/run_planner.py
```

Review the actual plan and passages, record the decision, then run the compiler and pair only if the brief qualifies.

```bash
python3 evidence/NEW_DIRECTORY/compile_brief.py
PYTHONPATH=. .venv/bin/python evidence/NEW_DIRECTORY/run_pair.py
```

Source retrieval, planner output and model sampling can change. Fresh replication tests the procedure rather than promising byte-identical prose. This run's frozen inputs and outputs remain inspectable by hash. Never delete an unknown attempt to obtain a new sample. The budget for this experiment is at most12 native calls and900 cumulative CLI seconds, with API spending0.

## Scope

The full-source input, planning call and new brief change together relative to the old experiment. This design can demonstrate feasibility and output differences. It cannot isolate ordering alone as the cause. This remains the same payment subject in the broader acceptance ledger. Human writing quality, six-subject diversity, editing effort, calibrated scoring, visual usefulness and the blinded pilot require their own evidence. Publishing, hosted CI, merge, installation promotion and deployment keep their existing owner gates.
