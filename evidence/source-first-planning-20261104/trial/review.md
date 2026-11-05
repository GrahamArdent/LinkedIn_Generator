# LinkedIn writing comparison

Human review pending. Labels are randomized.

## Draft A

Valid credentials and a trusted origin do not establish business approval for a transfer. The execution endpoint must enforce that dependency.

CERT-In/CSIRT-Fin reports attackers using stolen credentials to invoke fund-transfer APIs from victims’ whitelisted infrastructure, bypassing application controls. Dummy transaction references had no corresponding records. Its November update reports modified clients defeating assumptions about legitimate callers and recommends server-side validation and maker-checker approval for merchant settlements.

My verification question: does the fund-moving endpoint independently enforce the approved transaction and its preceding validation stages?

Payment leaders should ask the payment engineering lead and finance control owner to trace one disbursement path and one merchant settlement path together. In an authorized test environment, verify rejection of requests carrying valid credentials but lacking an approved record, missing preceding validation, or exceeding applicable transaction or daily limits. Record where each rejection occurs, then extend the review to every fund-movement path.

Assess cryptographic binding between validation and debit as a design requirement, consistent with CERT-In’s recommendation. These are proposed checks, not reported test results.

#PaymentSecurity #CyberRisk #APISecurity

## Draft B

Permission to call a payment API does not establish approval for the transfer it executes. I would examine whether the endpoint that moves funds enforces that distinction.

CERT-In/CSIRT-Fin reports in CIAD-2026-0046 that attackers stole credentials and invoked fund-transfer APIs from victims’ whitelisted infrastructure, bypassing application controls. Attackers supplied transaction references without corresponding records. The November update, CIAD-2026-0058, reports modified applications defeating assumptions that only legitimate clients would call APIs, and explicitly recommends approval controls for merchant settlements.

My verification question is: what prevents execution when business approval is absent?

Ask payment engineering and finance control owners to trace one disbursement and one merchant settlement path together. In an authorized test environment, check that valid credentials cannot enable execution without an approved record, without preceding validation, or above applicable limits. Record where rejection occurs, then extend the review to every fund-movement path.

Assess CERT-In’s recommended cryptographic binding: making debit execution depend on proof of preceding validation. These are proposed checks, not reported test results; the advisories provide neither implementation specifications nor measured control effectiveness.

## Review

Choose A, B or tie; mark keep/light/structural/reject, voice/insight/usefulness 1–5 and actual editing minutes.
