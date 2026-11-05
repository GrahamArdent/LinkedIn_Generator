# Eight-workflow trial procedure

Run from /home/graham/work/linkedin-codex-trial-20261104 on branch fix/selected-candidate-v4-20261104. The frozen catalogue is docs/implementation/v4/EDITORIAL_WORKFLOW_OPTIONS.md at9001c2f855261f4dbeab70ce5018d8d930683d7a. packet.json contains the exact extracted route1–8 instructions, concept, author, audience, selected voice/version/hash and source material.

## Evidence and context

CERT-In's October and November advisories form one reporting chain. Cloudflare's February2024 first-person account of its November2023 incident is an independent origin. The Cloudflare page was read through public search rendering; direct HTML download returned403. Its packet record retains selected claims, locator, URL and a short excerpt with that retrieval limitation. CERT-In full extracted source bodies come from the earlier saved primary snapshots. No prior post, score or assigned thesis is supplied.

Relatable Provocateur is the fixed primary voice. Alternate voices are resolved from the same versioned catalogue for the controlled voice comparison. Existing .codex-linkedin.local.json supplies the pinned Resume client source SHA, interpreter, model and reasoning settings. Authentication stays in the existing Codex ChatGPT store. Run/attempt/thread IDs are read from native receipts. Missing provider identifiers must be marked unavailable.

## Stage execution

run.py routes starts at most3 independent route workers. These are isolated model calls through the existing CodexProvider, each using a fresh ephemeral native thread. Each route uses its own shared-budget run ID eight-route-N. The common system contract requires supported claims, explicit inference and GO/HOLD decisions.

Route4's initial belief call sees no source evidence. Route7's first call excludes the November update. Its eligible packet ends at the October2026 source. Route6 creates separate business and technical role calls. Each route then receives its own prior-stage outputs only. Supported stages pass into meaning freeze, voice-and-attribution planning and one private160–220-word draft. Voice and attribution handoffs are combined in one planning call, an implementation choice to avoid a redundant call. The raw route prompts and inputs expose the exact packaging.

A model HOLD or a stage error yields a recorded route HOLD, with the original stage artifact retained. Unknown native effects require original-attempt reconciliation. The runner does not automatically regenerate a failed stage.

## Commands

```bash
PYTHONPATH=. .venv/bin/python evidence/eight-workflow-trial-20261104/run.py routes
PYTHONPATH=. .venv/bin/python evidence/eight-workflow-trial-20261104/run.py controls
PYTHONPATH=. .venv/bin/python evidence/eight-workflow-trial-20261104/finalize.py audit
```

Run controls only after all8 route-N.json outcomes exist. The control brief is the first admitted route in numerical order, selected before ranking. Its thesis/facts/action/qualification are frozen in controlled-brief.json. The direct-prompt control and three tellings receive that brief. All three voices receive the same literal explanatory instruction, four-part outline and brief. The fresh literal primary-voice output is the reference for voice comparison. A documented-case telling must stay within the source incidents in that fixed brief.

Repeated commands reopen completed stages while checking task/input equality. A cached draft is not a new sample. Each route is capped by an admitted batch of at most7 calls/900 CLI seconds, with control/audit batch at most12/900. API spending0. Native receipts, rather than assumed call counts, establish actual resources.

## Review and interpretation

The finalizer shuffles all retained drafts and stores the identity mapping separately. The blind review requests a paraphrased thesis, evidence that earned it, forwarding recipient/reason, specific required edits and actual editing effort. Human responses remain null until Graham reviews. Any assistant editing-time estimate must be labeled as an estimate.

Audit happens after all route outcomes and control outputs. The audit inspects claim support, source independence, analogy boundaries, distinct telling, voice and effort. Model audit is separately labeled. A model preference is never a human pilot win.

This first concept can identify candidate strengths or yield no advantage. A proposed hybrid requires a second concept and comparison with the strongest individual route and simple control before any winner is declared. If this audit supports no specific hybrid, record that outcome and keep the experiment bounded.

## Reproduction

The packet includes exact system/task/input/output and receipt references for every stage. To perform a new sampling run use a new evidence directory and new run IDs, preserving these originals. Record source/model/voice hashes, all prompts and all HOLDs. Human assessments, publishing approval, hosted CI, merge and deployment remain separate owner effects.


## Observed setup corrections and replay
Initial route4 and route7 HOLDs remain in route-4-initial.json and route-7-initial.json. INPUT_REPAIRS.json and run_input_repairs.py retain the exact corrections: permit a non-empirical hypothetical prior belief before evidence; replace route7's unresolved cutoff placeholder with 2026-10-09. Fresh corrected run IDs preserve the original attempts. This is input repair, not quality-based regeneration. The two repairs overlapped the original three-worker batch, so actual worker concurrency could reach five. That exceeds the stated concurrency plan; per-run call/time ceilings remained unchanged. Do not describe actual concurrency as three.

Completed DRAFTED outcomes are adopted on routes replay, preserving corrected outcomes instead of revisiting initial HOLD inputs. Per-stage cache reads still assert exact task/input equality. Use verify.py for archive verification without credentials or model calls. A new experiment needs new output paths/run IDs; never delete originals to obtain a new sample.

The finalizer uses one blinded model audit after all eight outcomes and seven control drafts exist. A proposed hybrid triggers three second-concept drafts (hybrid, strongest single approach, direct control) under the same 12-call batch ceiling. A second-concept review is shuffled separately. Neither an audit preference nor a transfer draft establishes a winner.

The optional second-concept blinded audit is run with second_review.py after all three transfer drafts exist. It consumes the twelfth and final call of the control/audit batch. RESOURCE_USE.json records actual totals; REPLAY.json proves reopening routes and controls added zero calls. verify.py reads FILES.sha256.json; the manifest excludes itself, transient locks/bytecode and the separately retained archive receipt to avoid self-referential hashes.
