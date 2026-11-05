# Fresh equal-input engine versus simpler prompt — November4,2026

**GO:** comparison execution, input/evaluator parity and recovery verification.
**HOLD:** publish readiness, human acceptance, engine writing advantage, nine-style expansion and broader P2 acceptance.

## Result

| Method/output | Same-rubric model score | Native calls including assessments | CLI seconds |
|---|---:|---:|---:|
| Engine original plus its assessment |74 |2 |24.678 |
| Engine's single guarded rewrite plus assessment |72 |2 |25.637 |
| Simpler one-draft baseline plus assessment |74 |2 |26.963 |
| Engine total |no qualified candidate |4 |50.315 |

Scores are uncalibrated model judgments, not human grades or measurements of engagement. The two-point rewrite difference is not statistical proof of deterioration; it provides no evidence of improvement in this sample. Threshold90 and one guarded rewrite were preserved. Engine selected_candidate remains null and engine_gate is HOLD_NO_QUALIFIED_CANDIDATE. Recovery completed only the baseline; it did not rerun the engine. The original is used as the engine side of the diagnostic pair because no qualified candidate exists; the rewrite remains visible separately.

## Expected versus observed

| Check | Expected | Observed |
|---|---|---|
| Fresh comparison | Both methods author fresh text; no prior draft supplied | Actual engine draft and baseline calls contain no retained earlier post |
| Equal substantive inputs | Same author profile/individual POV, Technical Explainer v3/hash, story, factual evidence and limits, audience, objective and model/reasoning | All checked against saved native requests and trial records; exact shared source bundle/style verified |
| Same evaluation | Same rubric/context apart from evaluated post | All3 evaluator payloads are byte-equivalent after canonicalization/removing post; hash in observations.json |
| Existing engine policy | At most one guarded quality rewrite; preserve any HOLD | Original74; safe rewrite72; neither promoted; no additional rewrite |
| Simpler method | Existing simple baseline prompt, one draft | Baseline74, assessed once |
| Bounded execution |<=12 calls/900 CLI seconds/API0; no retries |6 succeeded native calls,18 physical starts,77.278 CLI seconds/API0 |
| Local qualification | Full local suite and unchanged production bytes |209 PASS in2.05s; manifest product hashes unchanged;26 AT/11 E2E definitions unchanged |
| Reopen | Read completed records without model execution | Fresh-process exit0; all6 attempt records byte-identical;0 additional calls |
| Native evidence | Retain exact requests and outputs | Six distinct thread/attempt/request identities; native final text matches saved engine original/rewrite/baseline |
| Human/product acceptance | No proxy approval | Human decisions null; no kept example, first-six/pilot win, selected candidate or publication permission |

Same model gpt-6-astra, medium reasoning and ChatGPT authentication were used through the existing pinned Codex bridge. Subscription dollar cost is unknown. API spending was0.

## Critical reading

Neither method produces a convincing finished post for the stated goal. Both devote45–46 whitespace words to the agency-summary paragraph, restate the approval-versus-execution distinction, and end with or prominently include a list of unclaimed findings. The simpler baseline has not solved the underlying editorial weakness; it matched the engine's model judgment with fewer total calls.

The engine original's action asks about recipient/amount enforcement; the simpler baseline's action is slightly more abstract. The guarded rewrite tightens some wording and ends on an action, but repeats the central distinction and retains a separate defensive limitations paragraph. Those observations do not justify a strong winner.

The first drafting calls themselves were similar in resource use: engine10705 input tokens/11.126 seconds; baseline10381/12.666. Most of the engine's extra total work was the additional rewrite and its assessment, not a dramatic initial prompt-cost difference. Do not claim the simpler first draft was faster on this run or invent dollar savings.

The benchmark is same-input in the substantive sense, not identical prompt packaging: the engine adds its normal editorial context and policies, while the baseline uses the existing short system prompt plus shared structured facts/voice/format inputs. Graham identity is selected by the same request/profile; the engine prompt names persona_key and the baseline receives the resolved author profile/POV. Baseline output includes3 inline hashtags; engine keeps the same hashtags in a separate result field. Raw outputs and evaluator inputs were not normalized or silently edited. Baseline168 whitespace words includes those3 hashtag tokens, giving165 prose words versus engine166. These presentation differences and single samples limit attribution.

Opportunity preflight and visuals were deliberately disabled for this fixed-subject writing diagnostic; drafting, ordinary editor eligibility, scorer and single guarded publish rewrite were exercised. This is not complete product E2E acceptance. The deterministic critic/humanizer found no repairable issues and did not make additional model calls. Their absence is recorded behavior, not an omitted simulated pass.

## What this does and does not diagnose

The complex engine prompt is not necessary to reproduce this subject's repetitive news-summary shape: the simpler prompt produces similar weaknesses with the same brief, selected style and model. That weakens a claim that engine-only instructions are the sole cause. It does not isolate which shared input matters, prove the brief is solely responsible, or establish all simple prompts outperform the engine.

The brief supplies an almost-finished thesis, a prescribed recommendation and summary-level evidence. Its retained inference/opinion records echo that thesis. Technical style and model priors may also influence form. The next highest-value read-only diagnosis is to compare the complete primary source with this compressed brief: did we discard a concrete mechanism, consequence or meaningful tradeoff that could support a less repetitive post? Do that before changing more voice instructions, adding a layer or generating another collection.

Keep the existing engine's evidence admission, provenance, recovery and publication guards even if later evidence supports simpler drafting. This sample establishes no general writing-quality benefit from the extra rewrite, not that every engine function lacks value.

## Review and continuation

trial/review.md is the randomized two-draft review; mapping is stored separately in trial/blind-mapping.json. Methods.md exposes all3 exact texts and their scores for transparent technical inspection. Reading methods before the pair removes blindness for that reviewer. The assistant has inspected methods; its analysis is not a blinded human preference.

This is the same repeated payment subject, not a new distinct subject in the first-six denominator, and no6-pair pilot win is counted. Human quality, measured editing effort and the simpler-LLM pilot remain open.

All evidence lives in this directory; CURRENT_WORK_PACKET points to MILESTONE.json, and plan/prompt reference the single narrative here. No production code/config/test changes, hosted CI, merge, installation promotion, deployment, rendering, publishing or voice expansion occurred.
