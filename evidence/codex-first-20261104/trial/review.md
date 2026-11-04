# LinkedIn writing comparison

Human review pending. Labels are randomized.

## Draft A

Which draft is final? The workflow should know.

A verified finding in the LinkedIn generator showed how that answer could become ambiguous. The main output could keep the original draft while the visual plan used a qualified rewrite.

Both versions were available. But someone using the output had to work out which one counted.

The repair made the choice explicit: identify the selected draft and tie the visual to a fingerprint of that draft’s exact text. That gives the next step something precise to check.

This was verified in source and automated tests. It wasn’t evidence of a wrong post being published.

My takeaway: improving a draft and selecting a draft are separate jobs. A rewrite can be better without the rest of the workflow knowing it is final.

If you’re building or using AI tools at work, check the handoff. Can the next step identify the chosen version and verify that its supporting material belongs to it?

“Final” needs to be a shared decision, not a local opinion.

#AI #ContentWorkflow #Automation

## Draft B

Two drafts. One workflow. Which version is final?

A finding in a LinkedIn post generator made that question surprisingly concrete: it could return the original draft as the main text while preparing a visual plan from a revised version.

That left the next step to work out which draft counted.

The mismatch was verified in source code and automated tests. There’s no evidence here of an incorrectly published post. But the ambiguity matters: checking the words and checking the visual separately won’t tell you whether they belong together.

The repair made the selected draft explicit and tied the visual plan to a digital fingerprint of that exact text.

My takeaway: choosing the final version is part of the work. Every step that follows needs to use that choice.

A reliable handoff shouldn’t ask the next person, or the next tool, to guess what “final” means.

## Review

Choose A, B or tie; mark keep/light/structural/reject, voice/insight/usefulness 1–5 and actual editing minutes.
