# Voice convergence diagnosis — 2026-11-05

Disposition: delivery/integrity GO; comparison usefulness FAIL; precise causal attribution HOLD. This corrects the prior next-step recommendation: human preference review should not be used to qualify a comparison with weak style differentiation.

## What was actually checked

Ran audit.py against the retained comparison manifest, all nine native request bindings, final.json model outputs, provider receipts and attempt/thread identities. Each model-bound task/input equals its captured drafting prompt; each raw final.text equals the retained post. All nine cache_hit flags are false. Nine request hashes, nine attempt IDs, nine thread IDs and nine output hashes are distinct. Separate ephemeral executions disable tools/project instructions and do not resume prior conversations. Deliberate substituted native input and output controls are rejected for all nine records (18 negative checks). No new model execution or API spending.

The common prefix is already present in model output: neither PDF formatting nor later critic/humanizer/scoring introduced it. The diagnostic harness stopped immediately after drafting, so subsequent stages cannot explain this batch. No evidence of cache replay, dropped selector, wrong PDF text or shared conversation.

Observed: all nine hooks start “An approval screen”; two hooks are identical in full. Seven of nine factual paragraphs are identical in full. Nine distinct bodies do not establish meaningful stylistic variation.

## Confirmed process defects

1. **Over-specified, repeated copy brief.** The same full objective is supplied as Objective, Editorial Plan.takeaway, Persona Profile.editorial_context.objective and that context's plan.takeaway. It already dictates the concrete opening concept, managerial recommendation and destination. “approval screen” appears five times in each user prompt. Holding the proposition constant was appropriate; repeating a near-copy outline and its wording four times was unnecessary and reduces room for style.

2. **Default style still physically reaches all nine models.** src/app/api.py::_persona_profile adds writing_voice and then loads the full Graham Voice Bible/Spoken Voice regardless of selection. The inherited blocks occupy5888 serialized characters; selected style_traits occupy roughly500–650. The prompt says selected style wins, but also retains multiple default-style instructions. Verbal precedence is weaker isolation than passing one effective style. This is instruction competition, not failure to transmit the selector. Character volume is descriptive evidence, not proof of model attention.

3. **Generic composition still steers structure.** The actual config/prompts_packs.yaml drafting template ends by asking for one concise hook → concrete detail → explanation → consequence → natural ending. The plan and repeated brief reinforce the same route. Legacy config/prompts.yaml and composer.py contain other rigid templates, but they were NOT the active cause in these retained requests.

4. **Recovered settings were treated as effective prose controls without qualification.** Eight profiles are mostly numeric attributes such as colon_freq25, professional_tone60 and vulnerability_comfort0.8, with no operational units or concrete explanation; they receive the same “guidance, not rigid quotas” disclaimer. Historical data was preserved, but its ability to direct distinct writing was not established. The blanket short length, authority framing and supplied takeaway also narrow options. No invented anecdote, client claim or statistic should be introduced to compensate.

5. **Acceptance tested transport, not the intended writing outcome.** tests/test_writing_voice.py checks selected ID/version/hash at actual consumers and equal non-style inputs, not whether blind readers can distinguish useful delivery differences. Green195 remains valid for those assertions. It does not demonstrate effective voice separation. The prior comparison preserved weak results honestly, but asking the owner to choose among near-duplicates was premature.

## What is inferred, not yet proved

Leading hypothesis: repeated thesis/outline plus competing inherited style and weakly operationalized selected traits caused prompt-driven convergence. Model tendencies and fixed model/reasoning may contribute. The shared client explicitly does not apply API temperature; changing a nominal temperature or seed is not a demonstrated remedy. No causal ablation was run here, so no single factor is proved necessary/sufficient. Do not describe this as an execution outage, claim all voices are equivalent, or treat repeated prefix alone as a universal quality failure.

## Smallest recommended next action

Repair the existing effective prompt projection, not the engine architecture:
- Preserve author identity/POV, factual evidence/limitations and house rules. When a style is explicit, omit conflicting default rhetorical style; omission must retain existing default behavior.
- State the central proposition once in neutral semantic terms. Keep choice of opening, evidence placement, rhythm and ending available to the selected style. Deduplicate objective/planning copies at the actual consumer.
- Give selected traits concise, observable writing instructions rather than relying on unexplained frequency numbers. Preserve original definitions/version provenance; record any accepted revised projection.
- Add offline actual-consumer assertions for one effective style, no lost facts/POV/safety, no repeated whole objective, unchanged omitted-selection behavior and baseline/evaluator parity. Retain the original tests and all26 AT/11 E2E obligations.
- Then run a small, separately declared Codex-only three-style test (concise, reflective, technical) with fixed author/story/facts/audience/proposition. Predeclare what should differ: sentence rhythm, opening approach, evidence placement and rhetorical structure. Judge actual readability and meaningful distinction; duplicated hooks are a diagnostic flag, not a mechanical demand to use different synonyms. No retries or manual edits to manufacture contrast. Expand to nine only if this diagnostic works. Exact native budget/admission must be recorded before launch.

No production repair or new writing batch was made in this diagnostic. Existing nine results/PDF remain unchanged. No human preference, keep, approved example, baseline win, merge, installation promotion, hosted CI, deployment or publishing inferred.
