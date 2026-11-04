# Evidence-first substantive trial

Disposition: machine execution GO; content acceptance HOLD. This is a transparent diagnostic, not a blinded pilot win. No candidate reached90, selected_candidate remains null and visual planning is deferred. Earlier weak trials stay in the record.

## Expected versus observed

| Check | Expected | Observed |
|---|---|---|
| Source admission | Missing central support blocks despite peripheral facts | Actual CLI blocked before provider construction;0 calls |
| Native negative | No facts cannot earn a draft | needs_more_evidence;1 call retained |
| Writer | Frozen C1 plus limitations/claim types reach real draft | Exact prompts retained; source bundle and central anchor present |
| Quality | Valid ratings, one guarded quality rewrite, threshold90 | Original73; rewrite75; guard accepted=True |
| Comparator | Equal facts/voice/goal; same rubric | Baseline75; model judgments remain uncalibrated |
| Budget | <=12 model executions/900sec; zero API | 10 executions;30 physical starts;73.838sec; API0 |
| Recovery | Show + duplicate generate launch nothing | Fresh processes PASS;0 additional executions |
| Human acceptance | Exact-text verdict/ratings/editing effort | PENDING; not inferred |

## Interpretation

Grounding/provenance and negative admission worked. This does not establish a writing-quality improvement: topics and scorer context changed, so scores cannot be compared causally with earlier trials. This subject still produced report-like wording, familiar framing and unexplained security terms. More sources alone did not solve voice or originality. The same-model baseline did not lose under the model rubric; neither approach has human acceptance. Do not regenerate to chase90.

## Engine original — model score 73

Content SHA256: a3454852cdbe14fc96e9370d5d94ff14df4f3e6aba1cf3f029978ed1b95c916e

MFA is enabled. How does account recovery work?

The joint Scattered Spider advisory, revised July 29, 2025, describes attackers gathering password-reset information through calls, then persuading IT help-desk staff to reset passwords and/or transfer MFA tokens. That enabled account takeovers in single sign-on environments.

Recovery matters because it determines who gets access when the usual proof is unavailable.

The same advisory recommends phishing-resistant MFA, including FIDO/WebAuthn or PKI-based implementations. That recommendation belongs alongside the recovery lesson.

My takeaway: an MFA review should examine account recovery as carefully as normal sign-in.

I’d start with one practical question: when someone cannot provide their usual proof, what independent evidence must the help desk verify before authorizing a password reset or MFA-token transfer?

Enabling MFA is a meaningful step. Verifying who gets to reset access is part of the protection.

## One guarded rewrite — model score 75

Content SHA256: 0ce3c656025feba4f3688a4c67348106c6e6ef8885b6151020b7aaf0188b5939

MFA is enabled. Who can reset it?

The joint Scattered Spider advisory, revised July 29, 2025, describes attackers gathering password-reset information through calls, then persuading IT help-desk staff to reset passwords and/or transfer MFA tokens. That enabled account takeovers in single sign-on environments.

The distinction matters: convincing someone to reset access is different from defeating the technology protecting it. The same advisory recommends phishing-resistant MFA, including FIDO/WebAuthn or PKI-based implementations.

I’d include one question in an MFA review: when someone cannot provide their usual proof, what independent evidence must the help desk verify before authorizing a password reset or MFA-token transfer?

That’s a decision about who gets trusted as the account owner. It deserves the same scrutiny as sign-in.

## Simple baseline — model score 75

Content SHA256: 4c34af21eb7063aa06dbbb9f51115cb2a2888c377d1db6b2279cedaa2c8fdb69

MFA is enabled. Who can reset it?

The joint Scattered Spider advisory, revised July 29, 2025, describes attackers gathering password-reset information through calls, then persuading IT help-desk staff to reset passwords or transfer MFA tokens. That enabled account takeovers in single sign-on environments.

The mechanism matters: attackers persuaded someone to change access through recovery. They did not need to break the cryptography.

And the same advisory recommends phishing-resistant MFA, including FIDO/WebAuthn or PKI-based implementations. That recommendation still belongs in the conversation.

My takeaway: an MFA review should follow the account through recovery, too. Checking the sign-in screen alone can miss how someone gets trusted again when their normal proof is unavailable.

For IT and business leaders, I’d bring one question to the review:

Who can authorize a recovery reset, what independent evidence must they require, and what happens when the person requesting it cannot provide the normal proof?

The answer tells you something an “MFA enabled” checkbox cannot.

#Cybersecurity #IdentitySecurity #MFA

## Evidence and next human gate

Frozen facts/limits: source-bundle.json. Exact request: request.json. All prompts/results and model receipts: execution-trace.json and prompts/. Source-to-output mapping: claim-map.json. Exact A/B package: trial/review.md (unqualified original versus baseline; guarded rewrite above is preserved separately). Review the actual text for factual accuracy, voice, usefulness/insight, keep/light/structural/reject and actual editing effort. A preference alone is insufficient. Expansion, rendering and publishing remain gated.
