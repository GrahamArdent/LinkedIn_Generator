# CURRENT_WORK_PACKET.md

PACKET_ID: LIG-CONTENT-ACCEPTANCE-2026-08-27
STATUS: active
PROJECT: LinkedIn_Generator
CURRENT_STAGE_OR_MILESTONE: Content-intelligence acceptance before publishing integration
AUTHORITY_SPINE: `README.md` product role + Dedication boundary, current explicit operator decisions, accepted project contracts/voice authority, and validated implementation state on `main`
AUTHORITY_VERSION_OR_COMMIT: LinkedIn_Generator `45655f87ffdf0cd614bdb07eb03e090afc9058e6`; PROGRAMSTART methodology `59a9bf4f2028b328d38fae64b8e08a7cf4ae685e`
BLOCKER_SCOPE: milestone
SAFE_EXECUTION_LANE: A/B — human content acceptance, evidence gathering, review, and reversible repo corrections can proceed; live external publishing remains out of scope
BLOCKED_ACTION: Final repo-provider acceptance cannot be claimed until the real generation path is exercised in an environment with a valid `OPENAI_API_KEY`.

## Objective

Determine whether the current LinkedIn content-intelligence core consistently produces Graham-authored posts that are understandable, distinctive, grounded, useful, and close enough to Graham's real voice that approval requires little or no correction. Use the result to decide whether the next product investment should be approval-gated LinkedIn publishing.

## Why This Is Next

The repository has just completed several linked content-quality slices: public-language/POV rules, reason-coded feedback, opportunity/goal routing, Graham Voice Bible authority, Graham Spoken Voice, and evidence/distinctiveness gating. More prompt or feature work without empirical use would add machinery before proving that the current system solves the actual content-quality problem.

PROGRAMSTART Mode C therefore routes the remaining uncertainty to targeted empirical validation rather than another plan or more research.

## Scope

### In

- Run 5–8 genuine professional subjects through the current content process.
- Prefer subjects grounded in recent real work rather than invented thought-leadership themes.
- For each subject, allow the system to return `skipped`, `needs_more_evidence`, or `drafted`.
- When evidence is missing, ask at most one targeted question at a time and resume the same opportunity.
- Review drafted posts with explicit `keep`, `edit`, or `reject` feedback and reason codes.
- Track recurring correction categories and make a focused generator correction only when evidence shows a repeatable system defect.
- Use current Graham Voice Bible + Graham Spoken Voice + opportunity/evidence rules.
- At the end, run a focused convergence decision on readiness for approval-gated publishing.

### Out

- LinkedIn API/OAuth implementation.
- Automatic publishing or scheduling.
- Image generation or Replicate integration.
- Feed crawling, autonomous commenting, or engagement bots.
- A new Master Game Plan or competing execution spine.
- Broad prompt rewrites unsupported by trial evidence.
- Reactivating recurring CI solely for this trial.

## Required Context

- `README.md` — current product role and Dedication boundary.
- `src/app/contracts.py` — request/result and feedback contract.
- `src/app/opportunity.py` — opportunity, concrete-evidence, and distinctiveness gate.
- `config/graham_voice_profile.yaml` — authorized Voice Bible runtime profile.
- `config/graham_spoken_voice.yaml` — Graham Spoken Voice authority.
- `config/prompts_packs.yaml` — current generation/critic/humanize instructions.
- `src/app/judge.py` — deterministic structural/semantic quality checks.
- `PROGRAMBUILD/PROGRAMBUILD_PLANNING_OPERATING_MODEL.md` and `PROGRAMBUILD/PROGRAMBUILD_WORK_PACKET.md` — Mode C and verification-economy rules.

## Trusted Evidence + Invalidation

| Evidence | Why reusable | Invalidated by |
|---|---|---|
| Graham Voice Bible provenance and runtime profile | explicitly authorized and merged | explicit operator reversal or newer approved voice authority |
| Graham Spoken Voice schema | derived from user-authorized conversational/ENFP evidence and directly confirmed by operator as sounding like him | repeated trial feedback showing a systematic voice mismatch |
| Public-language + individual POV rules | defects were observed directly and corrected in merged code | repeated approved examples showing the rule is too restrictive or contextually wrong |
| Opportunity/evidence gate | merged with exact-evidence anchoring and `needs_more_evidence` state | trial evidence that it routinely blocks good topics, permits generic ones, or asks poor questions |
| LinkedIn performance research | recent 2026 research already completed for content strategy | material LinkedIn platform/ranking/API evidence changes relevant to the decision |
| Local isolated behavior checks from recent slices | directly exercised changed deterministic logic | later code changes to the covered surface |

## Assumptions / Unknowns

| Item | Confidence | Action |
|---|---|---|
| Voice is now close to Graham | medium-high | validate across multiple real subjects rather than one post |
| Current opportunity scoring rejects/pauses the right subjects | medium | observe natural trial outcomes; do not manufacture a skip case |
| Concrete evidence materially closes the 85→95 quality gap | medium-high | compare drafts and correction burden across real evidence-rich subjects |
| Current prompt stack behaves similarly under the real OpenAI provider | medium | require repo-provider smoke acceptance before final publishing-readiness pass |
| Approval-gated publishing should be the next major product slice | medium-high | decide only after trial evidence and focused convergence gate |

## Trial Protocol

Use 5–8 genuine subjects. Stop at 5 only if the result is already decisive; continue toward 8 when correction patterns remain ambiguous.

For each trial:

1. establish the real subject and factual evidence;
2. run/replicate the opportunity decision without inventing specificity;
3. if `needs_more_evidence`, ask one targeted factual question and resume;
4. produce one full draft around the strongest grounded detail;
5. apply the current deterministic quality checks;
6. present one candidate to Graham;
7. record `keep`, `edit`, or `reject` plus reason codes;
8. do not promote generated text to positive voice evidence without explicit human authority;
9. if the same major defect recurs, pause the trial long enough to fix the smallest responsible rule and then continue.

### Candidate subject pool

These are candidates, not a required sequence. Use only when current evidence is strong enough.

- Why an AI system repeatedly checking settled decisions can create more work instead of less.
- What rebuilding a LinkedIn generator taught me about the difference between “good writing” and actually sounding like a person.
- Why one real detail can improve an AI-written post more than another polishing pass.
- Why useful automation sometimes needs to decide **not** to act.
- What self-hosting an AI project methodology taught me about planning becoming bureaucracy.
- Why approval should remain a human decision even when content creation becomes highly automated.
- Why an AI content system should sometimes decide there is nothing worth posting.
- The difference between making an AI workflow more capable and making it more selective.

## Acceptance Criteria

- [ ] At least 5 genuine subjects are reviewed; use up to 8 if evidence remains ambiguous.
- [ ] Zero approved candidates contain invented factual specificity.
- [ ] Zero approved candidates require unexplained internal project terminology to understand the main point.
- [ ] Zero individual-author candidates use unjustified collective `we/us/our` framing.
- [ ] Strong-but-thin subjects request a useful missing detail rather than manufacturing one when that state naturally occurs.
- [ ] Weak subjects may be skipped rather than dressed up when that state naturally occurs.
- [ ] At least 4 of the first 6 drafted candidates, or an equivalent majority if fewer drafts are warranted, receive `keep` or only a light `edit` rather than structural rejection.
- [ ] `not_my_voice`, `sounds_like_ai`, `too_internal`, `wrong_pov`, or `unclear_point` does not recur as a major correction pattern after a focused fix.
- [ ] At least two human-accepted subjects are exercised through the actual repository generation provider before declaring the content core ready for publishing integration.
- [ ] Final focused Challenge Gate concludes `clear` or explicitly `conditional` for approval-gated publishing.

## Verification

| Changed / at-risk surface | Check | Result |
|---|---|---|
| PROGRAMSTART managed overlay | compare synced managed files to PROGRAMSTART `59a9bf4f...` | pending until sync commit reviewed |
| Content opportunity/evidence behavior | real subject outcomes + existing targeted tests/evidence | pending trial |
| Voice/public-language quality | human keep/edit/reject decisions + reason codes | pending trial |
| Provider-path equivalence | minimum two accepted subjects through actual repo provider | blocked until suitable runtime credential is available |
| Publishing-readiness decision | focused Challenge Gate using trial evidence | pending trial completion |

## Stop / Escalation Conditions

- Stop adding content-generation machinery if the current system is already meeting acceptance criteria.
- Pause and fix a bounded defect if the same major correction category recurs across multiple trials.
- Escalate rather than invent facts when distinctive evidence is unavailable.
- Do not begin LinkedIn publishing/OAuth implementation before the content acceptance gate is clear or explicitly conditional with a narrow known blocker.
- Do not let missing repo-provider credentials block human content-quality validation that can safely proceed in Lane A/B.

## Durable Updates On Completion

- execution spine/status: update only the existing project authority/status surface if the acceptance result changes strategic sequencing.
- decision log / ADR: record the decision to proceed, conditionally proceed, or delay approval-gated publishing if it is durable enough to warrant a project decision.
- requirements: update only if the trial proves a new durable content requirement.
- architecture: update only if the acceptance result changes the LinkedIn Generator/Dedication boundary or provider contract.
- tests / registry: add focused regression coverage only for defects actually discovered by the trial.
- release / operations: none until publishing integration is explicitly authorized as the next slice.

## Trial Evidence

| # | Subject | Gate outcome | Human decision | Reason codes / correction | Notes |
|---:|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |

## Close-Out

OUTCOME: pending
VERIFICATION_SUMMARY: pending
EVIDENCE_INVALIDATED_OR_REUSED: pending
AUTHORITY_RECONCILED: pending
REMAINING_BLOCKERS: actual repo-provider acceptance requires a suitable runtime credential until proven otherwise
NEXT_RECOMMENDED_SLICE: pending acceptance trial; expected candidate is approval-gated LinkedIn publishing if the content gate clears
