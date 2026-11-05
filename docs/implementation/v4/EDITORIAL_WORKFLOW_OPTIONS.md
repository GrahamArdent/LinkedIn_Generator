# Eight workflows for an independent LinkedIn argument
November 4, 2026 design · November5 handoff correction: see CURRENT_WORK_PACKET.md and evidence/narrative-handoff-repair-20261105/REPORT.md. The original catalogue commit remains9001c2f.

## Set up the common research

A news item supplies a question. For example, an alert about payment fraud could raise the broader question “When does proof of access give a decision-maker misplaced confidence?” Keep that wording provisional. Alternative concepts might concern early warning signals or how organizations decide an incident is over. Pick one question for the eight-way trial before choosing its answer.

**Call 0A — Discover.** “Given [news item], [Graham's area of expertise] and [reader], propose three underlying questions that would still matter six months from now. For each, state the decision at stake, the kinds of evidence that could change the answer and a search likely to uncover a counterexample. Return questions, not theses.”

**Call 0B — Research.** “For [chosen question], retrieve complete, reputable sources with different evidentiary roles. Aim for a first-hand incident or observation, independent research or data, and a contrasting case or credible boundary condition. Trace stories quoting the same release back to their origin. For each claim save source ID, publisher, date, URL, passage locator, short excerpt, population, and limits. Say whether each source confirms, complements or challenges another. HOLD if fewer than two independent origins contribute materially or the concept relies on unsupported extrapolation.”

A standard describing how a system should work and an incident showing what happened can complement one another. Neither measures how frequently something happens. Two updates from CERT-In can establish a timeline while counting as one institutional reporting chain. Freeze the resulting evidence ledger, the neutral question, audience and author before the eight runs. Use identical snapshots across routes.

## Separate three decisions

**Meaning:** what can Graham reasonably conclude, how far does it travel, and what decision changes? **Narrative form:** how does the reader discover that meaning (case, comparison, symbol, dialogue, timeline)? **Voice:** how does Graham sound while developing it (pace, precision, humour, directness)? Set the author and preferred voice early. Keep source extraction neutral. Apply voice to the telling after the argument has survived a challenge. A technical explanation can use an analogy; a provocateur can write a documented case.

## Eight routes and their copyable prompts

Each numbered instruction is a fresh call. Supply the frozen ledger/full source access to factual calls. Bracketed outputs come from the named previous call. Hide other routes, historical drafts and model scores. Each route ends with the shared handoff below. The first two calls per route produce a brief and narrative outline, not public copy.

### 1. Two cases, one telling difference
1. “Find two independently documented cases that address [question]. Match them on the relevant feature and identify one material difference. Attach claim IDs on both sides. Say which differences in context prevent a causal conclusion.”
2. “Arrange [matched cases] as a parallel comparison: same reader question at each beat, then the point where the cases diverge. State the narrow implication and the detail a reader should inspect in their own situation. HOLD if the resemblance is superficial.”
Output: paired case outline. Story shape comes from contrast.

### 2. A symbol with a limit
1. “Across independent sources identify one recurring relationship behind [question]. Describe it literally, with its conditions and evidence. Freeze the literal explanation before suggesting imagery.”
2. “Generate three familiar objects or situations that could illustrate [relationship]. Map the parts of each analogy to the actual evidence. Identify where each comparison breaks. Choose one whose failure does not change the conclusion. Outline image → real mechanism → boundary → action. If none fits, HOLD.”
Output: a symbolic explanation with an explicit mapping. The image illustrates the claim and supplies zero factual evidence.

### 3. Follow one documented incident
1. “Choose one traceable incident. Extract its sequence and the moment that changes a reader's understanding. Use an independent source to test whether the mechanism also applies elsewhere. Keep their events and dates separate.”
2. “Outline [incident] starting at the consequential moment, then recover only the earlier detail needed to explain it. Label the transition from this case to the independent evidence. Remove imagined dialogue, private motives and invented scene detail.”
Output: one factual story whose relevance extends beyond the headline.

### 4. Put the ordinary belief on trial
1. “Before seeing the evidence, state a competent reader's strongest plausible belief about [neutral question]. Give its rationale and the conditions under which it works. Treat it as hypothetical unless sourced.”
2. “Read the ledger. Find the best evidence for [belief] and the strongest independent exception. Build an outline that earns the belief first, introduces the exception second and ends with a revised rule. If the ordinary belief survives intact, say so.”
Output: a supported change of mind without forcing contrarianism.

### 5. Investigate an ambiguous word
1. “Find a consequential term used by multiple sources. Read their definitions, measurement methods and qualifications. Identify two readings that could produce different decisions. Separate ambiguous language from genuinely conflicting findings.”
2. “Build [two readings] into a short investigation. Present the consequential phrase, test both meanings against named sources and identify the observation that resolves the question or leaves it open. Attribute intentional ambiguity only with direct evidence of intent.”
Output: an interpretive puzzle with a defensible resolution or a precise unknown.

### 6. View the same facts from two desks
1. “Give [evidence] independently to a business owner and a technical owner. For each, identify the decision they own, the evidence they can see and what they must learn from the other. Mark hypothetical responsibilities as assumptions.” Run once per role in isolated contexts.
2. “Join [role notes] around one shared decision. Outline the story from each desk in turn. Identify the handoff that matters, who would forward the post to whom, and what answer would change the next step. Do not invent attributed speech.”
Output: two perspectives on one event with a practical handoff.

### 7. Read the evidence in historical order
1. “Using only sources available by [cutoff], freeze what a prudent reader could know and recommend then. Cite the dated support and write down one uncertainty.”
2. “Now reveal later evidence and the independent cross-check. Identify what was learned versus what actually changed in the world. Outline before → revealing detail → revised decision. HOLD if the apparent change comes only from a new headline.”
Output: a discovery story that preserves what was knowable at the time.

### 8. Work backward from a test
1. “From [reader's decision] and the multi-source evidence, identify two plausible explanations or operating conditions. Design the smallest safe, hypothetical observation that would distinguish them. State what each possible result would mean.”
2. “Outline a thought experiment. Begin with the choice the reader faces, invite a prediction, reveal the source-supported mechanism, and show how the answer changes the decision. Clearly distinguish a proposed test from one an investigator actually performed.”
Output: an interactive reasoning sequence that a reader could use with a colleague.

## Common handoff and voice change

**Freeze meaning and narrative separately.** Return planning data only: meaning contains one thesis, reader consequence, up to two supported facts with claim/source IDs, and qualification. Narrative independently contains the selected form, ordered beats, and any selected symbol with its mapping and boundary. Label inference in the evidence record. Do not return a title, post body or complete editorial draft. After admission, copy these data with the existing freeze_handoff function instead of asking another summarizer to reconstruct or replace the selected form. Preserve the full evidence trail outside this compact handoff. HOLD if the conclusion outruns the sources. The bounded implementation currently supports literal/symbolic only; do not coerce case, timeline or other routes to literal. Extending another form requires explicit validation before reuse.

**Apply voice inside the selected narrative.** Use plan_writing with the validated handoff, verified voice and source ledger. Return only ordered beat delivery annotations and source-bound attribution. Target80–160 characters per fragment, hard maximum240; reference claim IDs rather than retell facts. No replacement meaning/narrative, hook copy, title, body or finished paragraphs. attach_writing_plan preserves the original selection. Malformed output is HOLD before drafting; retain it and reconcile an explicitly admitted correction rather than silently retry. The author, facts and qualification survive voice application. Prose begins only at the explicit writer call.

**Attribute naturally.** “For each load-bearing claim, identify whose observation it is and how to name the source in ordinary language. Use the source's role in the argument: one report documented the event, another study establishes a boundary. Drop citations that add prestige alone. Store full URLs and passage locators in the source record. Flag any external link that would materially help a reader verify or use the information.”

For the first comparison use the existing house rule of no URLs in the post body, inline source names where needed, and a source list in the review package. LinkedIn supports external links. Its help documentation describes sharing mechanics and gives no universal reach penalty. Placement can be a separate later test. [LinkedIn Help](https://www.linkedin.com/help/linkedin/answer/a525301)

## Run all eight before the audit

1. Predeclare one concept, frozen sources, author, audience, verified voice/version, word range, model/settings, stopping rules and call budget. Use isolated contexts and record exact prompts, inputs, outputs and resource use. Batch in groups within existing execution limits. A HOLD counts as a route result. Record why instead of forcing a draft.
2. **Compare approaches.** Run every route once on that common packet with the same voice. For each admitted brief generate a single private draft with its own outline. Keep the original, with no score-seeking retries. Save every route result before ranking anything.
3. **Test Graham's specific hypothesis.** Choose one supported thesis and freeze the SAME facts, audience, action and qualification. Using that identical brief, compare literal explanation, analogy and documented-case telling with voice fixed. Then hold one telling fixed and switch between two verified voices. This distinguishes effects of story construction from voice and from changing the argument. A case route must have a documented case in the frozen facts.
4. **Audit afterward.** Randomize labels. Ask a blinded reader to paraphrase the thesis, name what evidence earned it, say who might forward it and why, identify what they would edit, and estimate or measure editing effort (label which). Inspect whether an analogy implies an unsupported fact, and whether multiple independent sources actually change the reasoning. Record ties, rejected drafts and human judgments separately from model scores.
5. Use a plain direct-prompt draft on the same brief as the cost/quality control. Report provenance, substantive usefulness, distinctness of telling, fit to voice, editing effort and calls separately. No universal winner from one concept. If two routes contribute identifiable strengths, combine only those steps and test that candidate against the strongest single route and the control on a second, materially different concept. Decide winner, hybrid or no advantage after that evidence.

This edition replaces the previous design catalogue at the same path. Git history preserves the earlier eight options. These are proposed experimental routes. No live route trials, preference audit or publishing action are part of this design revision.
