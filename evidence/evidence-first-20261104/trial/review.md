# LinkedIn writing comparison

Human review pending. Labels are randomized.

## Draft A

MFA is enabled. How does account recovery work?

The joint Scattered Spider advisory, revised July 29, 2025, describes attackers gathering password-reset information through calls, then persuading IT help-desk staff to reset passwords and/or transfer MFA tokens. That enabled account takeovers in single sign-on environments.

Recovery matters because it determines who gets access when the usual proof is unavailable.

The same advisory recommends phishing-resistant MFA, including FIDO/WebAuthn or PKI-based implementations. That recommendation belongs alongside the recovery lesson.

My takeaway: an MFA review should examine account recovery as carefully as normal sign-in.

I’d start with one practical question: when someone cannot provide their usual proof, what independent evidence must the help desk verify before authorizing a password reset or MFA-token transfer?

Enabling MFA is a meaningful step. Verifying who gets to reset access is part of the protection.

## Draft B

MFA is enabled. Who can reset it?

The joint Scattered Spider advisory, revised July 29, 2025, describes attackers gathering password-reset information through calls, then persuading IT help-desk staff to reset passwords or transfer MFA tokens. That enabled account takeovers in single sign-on environments.

The mechanism matters: attackers persuaded someone to change access through recovery. They did not need to break the cryptography.

And the same advisory recommends phishing-resistant MFA, including FIDO/WebAuthn or PKI-based implementations. That recommendation still belongs in the conversation.

My takeaway: an MFA review should follow the account through recovery, too. Checking the sign-in screen alone can miss how someone gets trusted again when their normal proof is unavailable.

For IT and business leaders, I’d bring one question to the review:

Who can authorize a recovery reset, what independent evidence must they require, and what happens when the person requesting it cannot provide the normal proof?

The answer tells you something an “MFA enabled” checkbox cannot.

#Cybersecurity #IdentitySecurity #MFA

## Review

Choose A, B or tie; mark keep/light/structural/reject, voice/insight/usefulness 1–5 and actual editing minutes.
