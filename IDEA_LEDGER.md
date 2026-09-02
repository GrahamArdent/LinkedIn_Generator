# LinkedIn Generator Idea Ledger

**Status:** optional non-authoritative preservation surface  
**Purpose:** preserve worthwhile LinkedIn Generator ideas without turning them into current scope, priority, sequencing, or permission to execute.

> **Capture broadly. Promote deliberately. Execute only from authority.**

This file follows the current PROGRAMSTART Idea Ledger semantics. `CURRENT_WORK_PACKET.md`, accepted architecture/contracts, and explicit operator decisions remain execution authority. A ledger status never makes an idea executable by itself.

## Status Vocabulary

- `CAPTURED` — worth remembering; not yet evaluated enough to imply priority.
- `CANDIDATE` — worth deliberate future evaluation against current evidence.
- `INVESTIGATING` — a bounded validation/research step is actively testing the idea.
- `SHELVED` — deliberately not current; preserve a revisit trigger.
- `ACCEPTED` — promoted into the artifact that actually owns the decision; link that authority.
- `REJECTED` — not adopted under current evidence; preserve rationale/reconsideration trigger.
- `SUPERSEDED` — replaced by another idea/decision.

---

## IDEA-linkedin-direct-publishing

TITLE: Direct LinkedIn personal-profile publishing adapter  
STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn publishing integration  
IDEA: Use LinkedIn's supported personal-profile publishing capability directly after human approval instead of requiring a third-party scheduler as the permanent publishing path.  
WHY_INTERESTING: Preserves control of the product boundary and can eliminate copy/paste once the content + visual package is trusted.  
ORIGIN_OR_EVIDENCE: 2026 LinkedIn API research in this project found approved personal publishing materially more feasible than arbitrary feed-reading automation.  
RELATED: Buffer fallback; Dedication approval/scheduling boundary.  
PROMOTION_OR_REVISIT_TRIGGER: Revisit after content + visual acceptance and renderer acceptance, immediately before approval-gated publishing Slice D.  
DECISION_OR_RATIONALE: Not current because publishing before package quality is proven would automate the wrong bottleneck.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

## IDEA-buffer-publishing-fallback

TITLE: Buffer as publishing/scheduling fallback  
STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn publishing integration  
IDEA: Keep Buffer available as a fallback/accelerator if direct LinkedIn publishing access or implementation becomes materially harder than expected.  
WHY_INTERESTING: Could shorten time-to-production without forcing LinkedIn Generator to own scheduling.  
ORIGIN_OR_EVIDENCE: Current API research identified Buffer's API as a credible supported intermediary.  
RELATED: IDEA-linkedin-direct-publishing.  
PROMOTION_OR_REVISIT_TRIGGER: Compare against direct LinkedIn API at Slice D provider-selection time.  
DECISION_OR_RATIONALE: Do not adopt merely for convenience before direct-path evidence is known.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

## IDEA-comment-reply-assistance

TITLE: Human-approved replies to comments on Graham's posts  
STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: Post-publication engagement  
IDEA: Surface legitimate comments on Graham-authored posts, draft a Graham-voice reply using the original post + comment context, and require approve/edit/ignore before sending.  
WHY_INTERESTING: Reduces response effort while preserving human relationship judgment and may improve useful conversation around posts.  
ORIGIN_OR_EVIDENCE: LinkedIn engagement research and supported third-party comment-management paths reviewed in this project.  
RELATED: analytics learning loop; publishing adapter.  
PROMOTION_OR_REVISIT_TRIGGER: After approval-gated publishing is reliable and a supported comment-read/reply path is available.  
DECISION_OR_RATIONALE: Do not build before publishing exists; do not default to autonomous replies.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

## IDEA-selected-external-post-comments

TITLE: Selected external-post comment assistant  
STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: Professional-network engagement  
IDEA: When an external LinkedIn post is legitimately supplied to the system, evaluate whether Graham has something genuinely useful to add, draft a comment only when the contribution is substantive, and require human approval.  
WHY_INTERESTING: Could create high-value visibility without generic engagement spam.  
ORIGIN_OR_EVIDENCE: API/policy research found arbitrary home-feed crawling restricted/risky while selected known-post assistance remains a safer product direction.  
RELATED: comment quality scoring; supported post/comment APIs.  
PROMOTION_OR_REVISIT_TRIGGER: After publishing/comment assistance is stable and supported access to the target post is legitimate.  
DECISION_OR_RATIONALE: Never promote this into feed crawling, mass commenting, or unsupported browser automation.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

## IDEA-post-performance-learning-loop

TITLE: Learn content strategy from actual post outcomes  
STATUS: CANDIDATE  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn content intelligence / learning architecture  
IDEA: After reliable publishing, associate legitimate performance signals with the post's goal, opportunity dimensions, format, hook/structure, visual format, and human feedback so future selection can improve from Graham-specific evidence rather than generic benchmarks alone.  
WHY_INTERESTING: The largest long-term quality gain may come from learning which subjects/formats actually work for Graham's audience, not endlessly adding static prompt rules.  
ORIGIN_OR_EVIDENCE: LinkedIn performance research + current PROGRAMSTART owner-routed learning architecture.  
RELATED: single-image-vs-carousel learning; comment/reply assistance.  
PROMOTION_OR_REVISIT_TRIGGER: After enough reliably published posts exist to avoid learning from tiny/noisy samples; design must route learned behavior to the LinkedIn Generator owner without overriding deterministic authority.  
DECISION_OR_RATIONALE: Worth deliberate future design, but premature before stable publishing/analytics data exists.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

## IDEA-format-performance-learning

TITLE: Learn when single images versus carousels perform better  
STATUS: CAPTURED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: Visual companion intelligence  
IDEA: Compare real outcomes by post structure and visual format so the planner can eventually use Graham-specific evidence when choosing `single_image` versus `carousel`.  
WHY_INTERESTING: Current research suggests carousels can perform strongly, but the product should not force a carousel when one image communicates the idea better.  
ORIGIN_OR_EVIDENCE: 2026 LinkedIn benchmark research + current visual planner format policy.  
RELATED: IDEA-post-performance-learning-loop.  
PROMOTION_OR_REVISIT_TRIGGER: After a meaningful sample of published single-image and carousel posts exists.  
DECISION_OR_RATIONALE: Preserve now; no extra implementation until outcome data exists.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

## IDEA-render-provider-comparison

TITLE: Compare Replicate models and alternate render providers behind one interface  
STATUS: CANDIDATE  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: Visual rendering provider selection  
IDEA: Keep the renderer provider-neutral and benchmark a small number of current image models/providers for conceptual editorial quality, instruction following, consistency, latency, and cost instead of permanently binding the product to the first Replicate model used.  
WHY_INTERESTING: Previous image-generation quality was poor enough that provider/model choice can materially affect review burden and regeneration cost.  
ORIGIN_OR_EVIDENCE: Operator experience with repeated poor Replicate image outputs + accepted Slice B provider-interface direction.  
RELATED: Replicate renderer slice; rendered-asset quality gate.  
PROMOTION_OR_REVISIT_TRIGGER: Immediately before or during Slice B provider/model selection; use current live provider/model evidence rather than stale assumptions.  
DECISION_OR_RATIONALE: Replicate remains expected first adapter, but provider/model selection should be evidence-based at implementation time.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

## IDEA-visual-quality-feedback

TITLE: Reason-coded visual review feedback  
STATUS: CAPTURED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: Visual rendering quality  
IDEA: Extend human review with compact visual reason codes such as `too_generic`, `wrong_metaphor`, `too_busy`, `bad_typography`, `too_ai_looking`, `weak_focal_point`, `carousel_padded`, and `does_not_add_value`, then use recurring defects to improve the planner/renderer owner rather than simply regenerating indefinitely.  
WHY_INTERESTING: Mirrors the successful text-feedback approach and directly attacks the prior loop of repeatedly regenerating bad images without learning why they failed.  
ORIGIN_OR_EVIDENCE: Operator reported excessive bad-image regeneration; current text system already benefits from reason-coded review.  
RELATED: Slice B rendered-asset quality; IDEA-post-performance-learning-loop.  
PROMOTION_OR_REVISIT_TRIGGER: During Slice B if rendered-image review shows repeated failure patterns.  
DECISION_OR_RATIONALE: Capture now; only promote if actual render evidence shows the codes will reduce correction cost.  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## Hygiene

- Do not duplicate current accepted decisions from `CURRENT_WORK_PACKET.md` here.
- Prefer updating an existing record over creating synonyms.
- Do not infer priority from status or age.
- When an idea becomes accepted, reconcile it into the actual owning requirement/architecture/work packet first, then set `STATUS: ACCEPTED` and fill `PROMOTED_TO`.
- Preserve useful shelved/rejected reasoning so later work does not reconstruct the same analysis from chat memory.
