# What this evaluation actually did

## Input brief
**Subject:** Before adding more AI steps, show me what they improve.
**Audience:** Professionals deciding how to use AI at work.
**Requested point:** Reuse what works; require visible usefulness before adding complexity.
**Facts:** Your actual request to reuse Codex, your request for a quick economical solution, and your questions about what generated the earlier post and how your preference would be used. No measured savings or invented customer story.
**Voice:** Existing Graham rhetorical profile and Spoken Voice projection, individual POV. No new voice example was learned from your earlier B preference.
**Constraints:** Evidence-backed opinion, no invented experience or figures, no em dashes, no hashtags requested. Same90 threshold and one rewrite.
[Exact frozen request](request.json) · [voice source hashes](voice-source-hashes.json).

## Exact context sent to Codex
The links below contain the complete task/system prompt, supplied input and result for every actual model call. They show what was transmitted; inclusion of voice material alone does not prove its causal influence.
| Call | Purpose | Exact prompt/result |
|---|---|---|
| 1 | Opportunity and evidence check | [attempt-43fc7eaf…](prompts/stage-01.md) |
| 2 | Initial draft | [attempt-26951fdd…](prompts/stage-02.md) |
| 3 | Publish-quality evaluation | [attempt-f45f5153…](prompts/stage-03.md) |
| 4 | One guarded rewrite | [attempt-9d8d01be…](prompts/stage-04.md) |
| 5 | Publish-quality evaluation | [attempt-34432b2c…](prompts/stage-05.md) |
| 6 | Simple-prompt baseline | [attempt-49271be3…](prompts/stage-06.md) |

Both methods used gpt-6-astra/medium and the same factual brief and approved voice material. Codex does not apply API temperature. Drafting received the existing engine prompt; the baseline received one plain writing prompt. This is a transparent diagnostic; do not count it as a blinded pilot win.

## What each stage changed
- Opportunity check: assessed the supplied facts and decided whether to draft; it did not write the post.
- Initial drafting: converted those facts and voice context into the original below. The engine's deterministic house rules were retained.
- First quality evaluation: score78. Reasons: No concrete comparison shows what an added step actually changed; the examples remain hypothetical.; The professional stakes stay broad, with no specific work situation showing why the distinction matters.; The middle repeats the need to understand the process without substantially advancing the argument.
- One rewrite: changed the opening from “I liked the AI draft. That proved very little.” to “I preferred one AI draft. The process still had to earn its place.”. It added the concrete paid-API-versus-Codex episode and a before/after inspection method. See the [exact wording diff](original-to-rewrite.diff).
- Rewrite evaluation: score77; guard accepted=True. Reasons: The paid-API detour introduces a second decision without making its connection to draft evaluation immediately clear.; The central distinction between liking an output and validating a process repeats more than it develops.; No concrete before-and-after writing example shows how the proposed evaluation would change a decision.
- Selection: neither reached90. No selected candidate or visual plan was promoted. The original was retained for comparison rather than regenerated.
- Baseline: one independent prompt produced its raw output below. It added hashtags despite the empty supplied list; that is observed editing burden, not silently repaired.

## Engine original
I liked the AI draft. That proved very little.

I preferred one version, but I still wanted to know what had shaped it: the brief, the information the model had been given, and what each extra step changed in the final writing.

I also wanted to know what would happen with my preference. Would it inform a useful change, or just count as a vote for the winner?

That distinction matters when deciding how much AI to put into everyday work. Liking an answer is a useful signal. It doesn’t tell me which steps deserve the credit.

My starting point is to reuse what works and keep the process simple. If another step helps, show me where: a mistake caught, a clearer explanation, a requirement finally met.

I’m willing to add complexity. I want to see what it earns.

## Engine's single rewrite
I preferred one AI draft. The process still had to earn its place.

The comparison was basic. I wanted to see the brief, the context given to the model, what changed at each stage, and the final writing. I also wanted to know what my preference would be used to change.

Picking a favourite answers one question. It doesn’t tell me which steps helped, or which were unnecessary.

That mattered when a paid-API trial was proposed. I already had a Codex subscription environment that could be reused, so I questioned the need for another route. I asked for a quick, economical solution, with extra layers deferred.

That wasn’t evidence of measured savings. It was a reason to make the case for adding something.

The same standard applies to the writing process. Show me the draft before a step and after it, alongside the requirement that step was meant to address. Then I can judge the change instead of giving the whole process credit for an answer I happen to like.

I’m willing to add complexity. My preference alone doesn’t justify it.

## Simple-prompt output
Before adding more AI steps, show me what improves.

My first question is whether something I already have can do the job. If it can, I’d rather start there and leave the extra layers until there’s a reason to add them.

That’s practical skepticism, but I need to apply it to my own judgments too.

I can prefer one draft without knowing why it’s better, or whether the process behind it deserves any credit. A preference is a starting point. It doesn’t settle the question.

What was it asked to do? What information did it have? What did each extra step actually change?

Those questions matter when deciding how much AI to put into everyday work. Otherwise, it’s easy to add another review, another tool, another subscription, while still being unclear about what any of them contributes.

I want a clear reason to keep each addition: a mistake caught, a clearer answer, a result that better meets the brief. Something I can inspect, rather than just a more elaborate description of the process.

I’m open to more steps. I just want them to earn their place.

#AI #PracticalAI #FutureOfWork

## What this establishes
The context and all6 native model calls are reconstructable; the shared budget recorded57.39 cumulative CLI seconds and18 physical starts. No API fallback or spending occurred. This does not establish a publishable post, lower editing effort or engine superiority.

The original directly reflects your concern about what generated a draft and how feedback would be used. The rewrite makes the Codex/API episode more explicit, but its scorer judged that detour less clear. Those are observed outputs and model judgments, not your verdict.

## Your useful next feedback
1. Does the original express what you actually mean, or turn it into a point you would not make?
2. Which opening sounds most like you, and which sentence sounds least like you?
3. Does the rewrite add useful specificity or just make the post more technical?
4. What would you actually change before posting? Record actual editing minutes if you edit.

That feedback will be attached to exact text hashes. Factual corrections update the source brief; tone/structure feedback identifies a narrow drafting issue; a preference alone does not change voice authority, pass a gate or authorize publication.
