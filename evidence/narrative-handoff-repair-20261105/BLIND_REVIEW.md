# Private shuffled narrative comparison

Human preferences pending. Review labels are not provider IDs.

## N01

An office key can open the door. It cannot give you permission to take the equipment home.

I think that distinction deserves more attention when leaders review trusted access.

Cloudflare reports that credentials stolen in the October 2023 Okta compromise were mistakenly considered unused and left unrotated. Attackers later used them to access its Atlassian environment.

The key still worked. The lock accepted it. Neither established that the person using it belonged there.

Permission to take a specific action adds another requirement. CERT-In reports that attackers used stolen API credentials from victims’ own whitelisted infrastructure to call fund-transfer APIs directly. They bypassed application-level checks and transferred funds to mule accounts.

In the office illustration, opening the door and permission to remove equipment are separate decisions. In the payment case, an accepted credential and an allowed network origin did not establish that a payout was authorized.

The illustration has limits. Digital credentials can be copied and used remotely. A physical key does not capture shared network origins or the checks required at each transaction stage. And taking equipment is an illustration, not an allegation about Cloudflare.

These are different accounts involving different systems. They support the distinction between accepted access and authorized action. They do not show that a particular defense explains different outcomes or would have prevented the reported losses.

My practical takeaway: pick one sensitive action and inspect the last point where it can be stopped.

For a payout, identify the evidence of authorization required before money moves. Check whether a direct API call must still satisfy the necessary approvals and business checks, including a match to an approved payment record.

A working key tells you something about access. Permission for the action still needs its own evidence.

## N02

Cloudflare reports that credentials stolen in the October 2023 Okta compromise were mistakenly considered unused and left unrotated. Attackers later used them to access its Atlassian environment.

CERT-In reports a different case: attackers used stolen API credentials from victims’ own whitelisted infrastructure to call fund-transfer APIs directly, bypass application-level checks and send funds to mule accounts.

The credentials were accepted. That did not make the actions legitimate.

I see a distinction leaders need to make explicit: an accepted account or an allowed network origin does not, by itself, establish authorization for a particular business action. Where a request comes from and what it is permitted to do are separate judgments.

I would start with one sensitive action and inspect the final point where the system permits or rejects it. What evidence of authorization must accompany the accepted account or network path?

For a payout, trace a direct API call. Check whether it must satisfy the required approvals and business checks before money can move, including when it skips the application screens where those checks normally happen.

These are different accounts, supporting a distinction between accepted access and authorized action. They do not establish that a particular defense explains the different outcomes, or that it would have prevented the reported losses.

For each draft: paraphrase the argument, identify its support, assess usefulness and voice, explain how its telling changes understanding, and record required edits. Actual editing time remains unavailable until measured.
