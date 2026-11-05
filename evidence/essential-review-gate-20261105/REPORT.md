# Essential review gate correction and chat audit
Disposition: GO for locally verified source correction. HOLD for installed-release acceptance and human product acceptance.
Owner authority: Graham explicitly instructed implementation of the four-essential recommendation and subsequent chat audit.
Parent source commit: 0143ebe03aae7b00092f7ba7a8187d923c8e8074. Branch: fix/essential-review-gate-20261105.
Current Paths CHATGPT.md was retrieved through connected GitHub, blob ba7463b91398ae9378a4ad09eba4974dedd5df40.

## What changed
The existing evaluator now independently returns four verdicts with reasons:
factual_integrity, reader_relevance, practical_value, argument_voice.
Verdicts are pass, revise or needs_evidence. Every essential must pass.
Missing/invalid verdicts yield assessment_unavailable; no fallback to legacy ratings.
Unsupported evidence pauses. A contradicted/unsafe claim blocks; fixable failures permit at most
one targeted rewrite, preserving the original. Only a guarded rewrite that passes all essentials
can replace it. A numerical improvement alone cannot select a rewrite.
Scores and weights remain diagnostic. The legacy threshold field is retained as request metadata
with threshold_enforced=false; the retired score environment no longer affects admission.
The version is essential-checks-v1. publish_ready is retained as a compatibility alias for
review_eligible, never human approval; human_approval remains pending.
The actual candidate consumer independently rechecks essentials, valid scores and rewrite guard.
Visual planning still uses exact selected bytes/hash. Unknown policy versions fail closed.
Old stored reviews retain their legacy policy; reopening does not regenerate, migrate or relabel them.
Writer, evidence admission, selected voice, narrative, source limits and existing safety guards remain.
Baseline and engine use the same updated evaluator, context and checks.

## Expected versus observed
| Check | Expected | Observed |
|---|---|---|
| Strong80/all essentials pass | Review eligible, no rewrite; exact text can reach visual planner | PASS fixture |
| Usefulness or voice failure despite90+ | No selection/visual; at most one targeted repair | PASS fixture |
| Unsupported claim despite100 | needs_evidence, no speculative rewrite or visual | PASS fixture |
| Low novelty/emotion/sharing but essentials pass | No automatic disqualification | PASS fixture |
| Lower-score rewrite fixes failed essential | Can qualify; original retained | PASS fixture, rewrite60 |
| Unsafe rewrite | Retained for audit, never selected | PASS fixture |
| Missing/malformed essentials | Unavailable; no rewrite/visual | PASS fixture |
| Forged ready flag/unknown policy | Consumer rejects | PASS fixture |
| Old native result reopening | Same historical policy and byte-identical record, zero calls | PASS local test using retained actual record |
| Real retained security draft | Judge independent essentials; reviewability is not approval | 72, all four pass, reviewable |
| Deliberately unsupported negative | Identify invented company result and universal guarantee | 69, factual needs_evidence and argument/voice revise; held |

The two native examples are retained exact texts, not new post generation. The negative example
is deliberately invalid. The first verdict is the model's judgment, not Graham's acceptance.
The negative result is semantic evidence beyond regex-only numeric detection; it does not prove
exhaustive detection of all unsupported claims.

## Tests and reproduction
- Initial13 focused regressions failed before implementation: red.log.
- Initial correction:13 passed, green.log.
- Full suite exposed fixtures missing the newly required explicit verdict schema. Their verdicts
  were made explicit; factual, provenance and guard assertions were retained.
- A later regression reproduced a stale environment parsing crash, retained-environment-red.log
  (actual filename retired-environment-red.log); removed dependence on that retired setting.
- Final local suite:251 passed, full-local.log;21 new test cases versus the230-test baseline.
- git diff --check passed.
- Ruff was attempted but is not installed in this venv: No module named ruff. No lint PASS claimed.
- Reproduce local tests: .venv/bin/python -m pytest -q.
- Native evaluator reproduction: native_smoke.py preserves exact old inputs, updated prompts,
  raw responses and native attempt receipts. Existing completed records cause no further calls.
  New executions require a new evidence directory/run ID and declared budget.
- verify.py checks file/source hashes, native results, policy semantics and the26/11 inventory.

Native resource use:2 subscription evaluations,6 physical starts,38.311 cumulative active CLI seconds,
37.616 model seconds, API spend0. Actual tokens/attempt IDs in RESOURCE_USE.json; dollar cost unavailable.
No paid API, hosted CI, merge, installation, deployment, rendering or publishing performed.

## Audit against this chat
| Requested outcome | Assessment |
|---|---|
| Reuse one engine, Codex-first, economical execution | GO: existing engine/bridge reused; no competing architecture |
| Concept and multiple reputable independent origins before writing | Existing two-origin briefs retained; not re-researched in this correction |
| Separate author, reader, meaning, evidence, narrative and voice | Existing six-building-blocks packet and handoff tests retained |
| Preserve selected narrative; prevent premature prose; verify literal versus symbolic | Earlier bounded evidence retained; regression suite passes; human comparison remains pending |
| Eight workflow routes, direct control, three tellings and fixed-telling voice changes | Earlier results retained; no new rerun or winner claim |
| Test proposed hybrid on second concept | Historical experiment exists; no accepted winner inferred |
| Avoid equal-word-count constraints | No equal-length gate introduced; length alone is not an essential failure |
| Explain recurring70s and remove arbitrary90 admission | GO: arithmetic audit retained, explicit essentials implemented, real72 now reviewable |
| Evidence-backed factual checking | Stronger semantic output and negative smoke; still an LLM judgment requiring claim-level human adjudication |
| Human writing quality and editing effort | HOLD: no exact six-subject keep/light/structural/reject and timed-edit dataset |
| Better than simpler LLM approach | HOLD: controls exist, but six blinded preferences/effort results missing |
| Meaningful visuals | Typed planner and identity checks retained; real human usefulness/format diversity not complete |
| Local milestone verification and up-to-date packet | GO source: local suite, exact evidence and packet/game-plan/prompt reconciliation |
| Everything merged and installed | NO: source candidate only; installed0c099d7 unchanged and retains old90 gate |
| Lightweight UI, learning lifecycle and approval-gated publishing | Future milestones; not delivered by this correction |
|26 acceptance objectives and11 E2E scenarios | Preserved and individually audited in ACCEPTANCE_AUDIT.json |

This chat's full objective is not complete. The decisive remaining gap is human evaluation of useful
writing against the simpler baseline, not another attempt to raise model scores. The existing opportunity
preflight still uses its own topic/evidence heuristic; this change concerns finished-draft admission,
not proof that topic selection is optimal. Review that boundary if good subjects are repeatedly skipped.
Do not infer LinkedIn algorithm performance, virality, voice mastery or a workflow winner from these tests.

## Next eligible action
Review this source candidate and promote it through the existing merge/release/rollback admission.
Then run one bounded installed package trial under the new policy with the retained same-evidence
direct control, save the selected visual plan if qualified and reopen with zero added calls.
Graham's factual accuracy, audience usefulness, voice and editing-effort judgments remain pending.
Use existing exact texts for calibration before new broad drafting, nine-voice expansion or selecting
another numerical threshold. Keep original first-six, baseline, visual and publishing gates.
