# LinkedIn writing comparison

Human review pending. Labels are randomized.

## Draft A

A working office key opens the lock. It doesn’t give its holder permission to take the equipment.

I’d apply that distinction to accepted credentials: access alone does not establish authority for the next action.

Cloudflare reports that credentials stolen in the October 2023 Okta compromise were mistakenly considered unused and left unrotated. Attackers later used them to access its Atlassian environment.

The key still worked. The lock accepted it.

Separate permission to act is the next issue. CERT-In reports that attackers used stolen API credentials from victims’ own whitelisted infrastructure to call fund-transfer APIs directly. They bypassed application-level checks and transferred funds to mule accounts.

An accepted credential and an allowed network origin did not, by themselves, establish that those payouts were authorized.

The office-key image has limits. Digital credentials can be copied and used remotely; a physical key doesn’t capture shared network origins or validation at each transaction stage. Taking equipment is only an illustration, not an allegation about Cloudflare.

These are different accounts involving different systems. They support the distinction between accepted access and authorized action. They don’t show that a particular defense explains different outcomes or would have prevented the reported losses.

My practical takeaway: pick one sensitive payout and inspect the final point where the system allows money to move. Identify the evidence of authorization required there: an approved record, the necessary approvals, beneficiary validation and transaction limits. Check whether a direct API call must satisfy those requirements too.

The key opening the door is one check. Permission for the specific action needs its own evidence.

## Draft B

Your office key works. Does that give you permission to take the equipment home?

The lock has answered one question. Permission is another.

Cloudflare reports that credentials stolen in the October 2023 Okta compromise were mistakenly considered unused and left unrotated. Attackers later used them to access its Atlassian environment.

The key still worked. The lock accepted it.

That separate question of permission matters when money moves, too. CERT-In reports that attackers used stolen API credentials from victims’ own whitelisted infrastructure to call fund-transfer APIs directly, bypass application-level checks and send funds to mule accounts.

Accepted credentials. Allowed network origin. Unauthorized transfers.

The office-key image has limits: digital credentials can be copied and used remotely. A physical key does not capture shared network origins or transaction-stage validation. And taking equipment is an illustration, not an allegation about Cloudflare.

These are different accounts involving different systems. They illustrate the distinction between accepted access and authorized action; they do not prove that a particular defense caused different outcomes or would have prevented losses.

My practical takeaway: pick one sensitive action and inspect the point where it can actually proceed.

For a payout, what evidence of authorization must accompany an accepted credential or network path? Must a direct API call satisfy the required approvals and business checks, including an approved record, beneficiary validation and transaction limits?

Ask your team to show you what enforces those requirements at the final payment step.

A working key answers whether you can get in. Your payout controls still need to answer whether this money may move.

#Cybersecurity #APISecurity #BusinessRisk

## Review

Choose A, B or tie; mark keep/light/structural/reject, voice/insight/usefulness 1–5 and actual editing minutes.
