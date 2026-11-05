# Hardcore audit of LinkedIn quality scoring

## Decision
Recommend replacing the uncalibrated aggregate90 gate for access to human review. Keep the existing score as a versioned diagnostic, retain factual/POV/safety checks, and keep publication approval human-owned. Do not substitute an equally unvalidated75 gate or relabel old scores. This audit does not change installed code, thresholds, historical results or acceptance definitions.

There are TWO problems: the writing has recurring editorial weaknesses, and the current score-to-decision policy is not validated for Graham's actual publishing judgment. A correct arithmetic result is not a validated decision.

## What the score means mathematically
Production formula: round(sum(weight × dimension/5)); weights total100. Ratings are integers0–5. The prompt defines3 as adequate but ordinary,4 as strong with minor weakness, and5 as exceptional.

| Rating pattern | Actual score | Gate at90 |
|---|---:|---|
| All adequate3 |60|Fail|
| All strong4 |80|Fail|
| All exceptional5 |100|Pass|
| Novelty/emotion/shareability fixed3, EVERYTHING ELSE5 |87|Fail|
| Everything5 except practical usefulness0 |90|Pass|
| Everything5 except voice authenticity0 |95|Pass|

ARITHMETIC.json records the calculation. COMPENSATION_PROBES.json also calls the actual _publish_candidate function with the last two synthetic vectors; both are accepted. These are counterexamples to the gate's design, NOT ratings returned by a model or real post approvals.

Reaching90 requires weighted average4.5. Starting from all4, dimensions totaling at least50 weight points must rise to5. We have effectively required work to be exceptional across much of the rubric before it may progress to human editorial review. Conversely, exceptionally scored unrelated qualities can mathematically compensate for total absence of usefulness or authentic voice.

## Recomputed historical evidence
COHORT.json contains19 available numeric assessments from native_codex trial.json records: engine originals, scored rewrites and baselines. Every total recomputes correctly. Range71–81; no arithmetic bug. There are10 distinct rating vectors.

Scores:71×2,72×2,73×5,74×4,75×2,77×1,78×2,81×1. At thresholds70/75/80/85/90, the descriptive pass counts are19/6/1/0/0. This is NOT evidence that70,75 or80 is a correct cutoff.

The cohort contains repeated subjects, related drafts, changed prompts/voices and correlated assessments. It is not19 independent subjects or a representative sample. Missing scores after rejected rewrites are excluded from numeric counts, not converted to zero. No human false-negative rate can be calculated because exact-text publishability labels are unavailable.

## Why the recent drafts land at71–74
The repeated pattern is4 for clarity, professional relevance, specificity and usefulness, with3 for novelty, emotional tension and shareability. Conversation and voice move between3 and4.

For the74 pattern: clarity12 + relevance12 + specificity12 + novelty9 + usefulness8 + emotion6 + conversation6.4 + shareability4.2 + voice4 =73.6, rounded74. Improve voice3→4 and the total moves only1 point. Improve conversation3→4 and it moves1.6 before rounding. Many visible improvements therefore barely affect the aggregate.

Novelty15 + emotion10 + conversation8 + shareability7 consume40% of the weight. Voice authenticity receives only5%, despite its central role in this project. Weights do not change with content_goal: authority, conversation and reach use the same aggregation. The goal enters the judgment prompt but not the formula.

The novelty question asks for a non-obvious lesson without explicitly defining novelty relative to the intended reader. The repeated criticism that access versus permission is familiar may reflect an expert-oriented standard even for nontechnical approvers. That is a plausible audience-validity concern, not a proven cause of each low rating.

Shareability/emotion ratings are editorial predictions, not observed LinkedIn reach, sharing or expertise signals. No engagement calibration supports them.

## Actual evaluator-only tests
Budget declared: at most6 subscription executions/900 CLI seconds, no paid API. No new post generation.

Four initial distinct requests were executed: security rescore, AI rescore, generic negative and unsupported-claim negative. The second identical security/AI requests returned cached receipts. Their files remain preserved and explicitly classified as cache reads, not independent samples.

Two remaining executions used new run IDs/native contexts with EXACTLY identical system/user text to the first respective assessments:
- Security:72 initially,72 in the fresh independent context; dimensions identical.
- AI:73 initially,74 independently; only voice authenticity moved3→4.
- Deliberately generic negative:14.
- Deliberately unsupported negative:62; the evaluator explicitly identified the invented87% personal company outcome and universal guarantee.

The negative fixtures are intentionally invalid test text, not factual claims or candidate posts. The scorer is not stuck in the70s and can recognize obvious weakness. One-point variability also warns against treating a1–3-point engine/control margin as a precise quality measurement. Two texts with two independent judgments each do not establish general reliability. Stable judgments do not establish agreement with Graham.

Six unique native executions plus two cached reads are retained. The repeat-cache mistake and its correction are part of the evidence. Exact prompts/raw results/IDs and result hashes are retained. RESOURCE_USE.json owns actual totals.

## What the writing genuinely lacks
The audit should not become an excuse to dismiss useful critique:
- The same conclusion is restated in hook, interpretation, practical takeaway and closer.
- Incidents/studies are often summarized in two blocks, then wrapped in qualifications. This makes the posts read as careful research summaries rather than independent thinking.
- The practical action sometimes remains an instruction to inspect or measure, without enough assistance deciding what result changes the next step.
- Familiar concepts get repeated rather than developed into a sharper, source-earned implication.
- Voice sometimes fades when the post enters the evidence and limitation paragraphs.

These are observed editorial judgments in retained drafts, not proof all should be rejected. Graham's earlier response that both posts were good but specialist-oriented is legitimate feedback. It is not an exact publish-ready rating or a complete calibration dataset.

The prompt also requires extensive factual/analogy/causal boundaries, then the evaluator penalizes their prominence. Preserve necessary uncertainty, but select which limit materially affects the reader's decision and keep remaining provenance in the evidence package. Do not erase material limitations merely to gain score.

## Threshold provenance and validity
The owner packet deliberately chose90 and one guarded rewrite. Repository history shows publish-threshold wiring in925af211a7e968ac9a6a6e228d01b9c9f4318e1a, with later rewrite work in03736f1. This was an intentional product policy, not a statistically fitted threshold, LinkedIn standard or documented predictor of Graham's publishing judgment.

The code itself reports NOT_CALIBRATED_TO_HUMAN_JUDGMENTS. No exact-text human gold set or threshold validation was found in the active trial evidence. Test fixtures that return high ratings prove arithmetic, validation, rewrite branching and selected-text binding;230 green engineering tests do not calibrate editorial quality.

The result name publish_ready actually means eligible for human editorial review under the current contract, not publication approval. Yet a sub90 result stops candidate selection and visual planning. All19 numeric records fail90, so the threshold prevents downstream product evaluation in this cohort. Safe failure is operationally correct, but the policy can still be a poor fit.

The unsupported negative received62 rather than a dedicated fatal-factual status. Its rationale recognizes a blocker, while the aggregate blends it with ordinary style weaknesses. A total alone cannot distinguish unsafe facts from merely ordinary writing. Existing request-evidence checks validate recorded support and mapping; numeric/quote rewrite guards are conservative checks, not a universal entailment proof for every original post.

## Recommended replacement policy — proposed, not installed
1. **Blocking readiness findings, separate from taste.** Report specific unsupported/contradictory claims, invented experience or quotes, wrong author/POV, critical missing evidence, and unreadability for the declared audience. Attach passages/source IDs and uncertainty. A high score cannot cancel a blocker. Preserve existing house, factual, safety and candidate-hash rules.
2. **Human-review eligibility instead of the hard90 total.** Supported, intelligible, relevant and useful work without a concrete blocker can be offered as a review candidate. Mark serious editorial defects needs_rework, unsupported facts needs_evidence, unavailable assessment explicitly unavailable. Being reviewable is not human acceptance, readiness to render paid assets, or permission to publish.
3. **Advisory quality dimensions.** Show reader clarity, decision usefulness, evidence discipline and voice separately. Assess novelty relative to the reader and goal. Treat emotion/conversation/shareability as goal-specific diagnostics, not universal requirements for every useful authority post. Do not publish replacement numeric weights as if calibrated.
4. **One targeted rewrite only when there is an actionable defect.** Do not require all useful work to be rewritten simply because a strict total is below90. Preserve original/rewrite/guard outcomes. A rejected rewrite does not destroy the supported original.
5. **Calibrate before automating selection again.** Reuse8–12 varied saved drafts: Graham labels keep/light/structural/reject, factual concerns and voice/usefulness reasons on exact text. Reserve some as a holdout rather than tuning on all examples. Compare reviewer/LLM blocker decisions and review eligibility, false passes/false holds and paired preferences. This is a small initial calibration, not statistical proof. No new writing batch is necessary just to collect these labels.
6. **Retain history and owner gates.** Store rubric/policy version and distinguish old90-qualified candidates from new review candidates. Visual planning should follow an explicit selected text and its exact hash under the accepted policy. Human editorial and publishing approval stay mandatory; all26 AT/11 E2E, baseline pilot and visual evaluation requirements remain.

Specific next implementation, if this policy is accepted: add separate blocker/eligibility fields in the existing evaluator/result path; make90 advisory for human review rather than merely change it to75; regression-test all-strong80 review eligibility, non-compensable usefulness/voice defects, unsupported claims despite a high total, rejected rewrites retaining originals, evaluator unavailability and old-record reopening. Then qualify locally and use the existing reviewed promotion procedure. This audit alone has not changed those runtime semantics.

## Research cross-check
OpenAI evaluation guidance recommends task-specific criteria, calibration to human judgment, reference examples and pairwise or pass/fail judgments rather than treating an uncalibrated total as sufficient. This supports the proposed method, not a particular LinkedIn threshold:
https://developers.openai.com/api/docs/guides/evaluation-best-practices
Locators: human calibration1011–1017; comparison1040; reference-guided grading and reliability1177–1193. Read2026-11-05.

The MT-Bench/Chatbot Arena paper documents judge limitations including position, verbosity and self-enhancement biases:
https://arxiv.org/abs/2306.05685
Abstract, revised December24,2023. This establishes reasons to validate locally, not proof a specific bias caused our scores or that findings transfer unchanged to this model. The present audit did not test positional bias, multiple judge models, verbosity manipulations or engagement prediction.

## Disposition
Arithmetic and storage GO. Basic weak-versus-supported discrimination observed. General reliability and human calibration unproved. The hard90 admission policy is not justified by available acceptance evidence; replace its role rather than chase it with repeated rewrites. Content still deserves focused editorial improvement. Runtime remains installed0c099d7 with its existing90 policy until the proposed change is explicitly adopted.
