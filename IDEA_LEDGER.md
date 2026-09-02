# LinkedIn Generator Idea Ledger

**Status:** optional non-authoritative preservation surface  
**Purpose:** preserve worthwhile LinkedIn Generator ideas without turning them into current scope, priority, sequencing, or execution authority.

> **Capture broadly. Promote deliberately. Execute only from authority.**

`CURRENT_WORK_PACKET.md`, README/product boundaries, accepted contracts, and explicit operator decisions remain the execution/authority surfaces. An `ACCEPTED` idea below is a provenance/reference record only and must point to the artifact that actually owns execution.

---

## IDEA-LIG-001 — Visual companion required for normal publishable posts

STATUS: ACCEPTED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn Generator post-package design  
IDEA: Normal publishable LinkedIn post packages should include a visual companion, with the system choosing a single image or carousel/document based on the content.  
WHY_INTERESTING: Graham does not intend to publish normal posts without a visual, and previous unconstrained image generation caused repeated low-quality regeneration.  
ORIGIN_OR_EVIDENCE: operator decision during LinkedIn Generator acceptance work  
RELATED: IDEA-LIG-002, IDEA-LIG-003, IDEA-LIG-004  
PROMOTION_OR_REVISIT_TRIGGER: already promoted  
DECISION_OR_RATIONALE: accepted; visual planning precedes rendering and typography stays separate from generated imagery  
PROMOTED_TO: `CURRENT_WORK_PACKET.md` → Durable Product Decisions / Slice A  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-002 — Provider-neutral renderer with Replicate as first adapter

STATUS: ACCEPTED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn Generator rendering layer  
IDEA: Put actual visual rendering behind a provider interface and use Replicate as the expected first adapter rather than making Replicate the permanent product architecture.  
WHY_INTERESTING: preserves flexibility when model quality, price, or provider capabilities change while reusing Graham's existing Replicate experience.  
ORIGIN_OR_EVIDENCE: operator preference + architecture discussion  
RELATED: IDEA-LIG-003, IDEA-LIG-005  
PROMOTION_OR_REVISIT_TRIGGER: after Visual Asset Planning is validated across multiple real posts  
DECISION_OR_RATIONALE: accepted as the next renderer architecture, but implementation is intentionally gated by visual-plan acceptance  
PROMOTED_TO: `CURRENT_WORK_PACKET.md` → Slice B  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-003 — Deterministic typography and carousel layout

STATUS: ACCEPTED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn Generator renderer  
IDEA: Generate imagery separately, then apply overlay text and carousel slide typography/layout deterministically instead of asking an image model to render final LinkedIn graphics.  
WHY_INTERESTING: directly addresses prior bad text/image outputs, increases consistency, and makes revisions cheaper than regenerating whole images.  
ORIGIN_OR_EVIDENCE: visual-quality review and Slice A architecture  
RELATED: IDEA-LIG-001, IDEA-LIG-002  
PROMOTION_OR_REVISIT_TRIGGER: renderer implementation  
DECISION_OR_RATIONALE: accepted  
PROMOTED_TO: `CURRENT_WORK_PACKET.md` → Durable Product Decisions / Slice B  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-004 — Learn which visual format performs best for Graham's audience

STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: post-performance learning  
IDEA: After enough posts exist, compare single-image versus carousel/document performance by content type and use real Graham-specific outcomes to improve future format recommendations.  
WHY_INTERESTING: current research suggests carousels/documents can perform strongly, but the system should learn from Graham's actual audience rather than permanently applying generic benchmarks.  
ORIGIN_OR_EVIDENCE: LinkedIn performance research + visual-planner design  
RELATED: IDEA-LIG-009, IDEA-LIG-010  
PROMOTION_OR_REVISIT_TRIGGER: enough legitimately published posts exist to make comparison useful  
DECISION_OR_RATIONALE: not current; do not optimize from insufficient sample size  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-005 — Bounded image regeneration driven by quality reasons

STATUS: CANDIDATE  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: renderer quality/review  
IDEA: When a rendered asset fails quality review, preserve the original and allow only a small bounded regeneration attempt targeted at explicit visual failure reasons rather than repeatedly generating from scratch.  
WHY_INTERESTING: mirrors the successful text Draft A/Draft B rule and directly addresses the prior problem of repeatedly redoing poor images.  
ORIGIN_OR_EVIDENCE: operator report that previous images were horrible and required repeated retries; text rewrite policy proved a useful bounded pattern  
RELATED: IDEA-LIG-002, IDEA-LIG-003  
PROMOTION_OR_REVISIT_TRIGGER: Slice B renderer design after first real rendered outputs expose useful quality categories  
DECISION_OR_RATIONALE: candidate; exact retry count/quality model should be evidence-driven rather than guessed now  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-006 — Alternate rendering providers behind the same interface

STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: rendering provider strategy  
IDEA: Keep the renderer contract capable of adding or replacing image-generation providers if Replicate model quality, cost, latency, or availability stops being the best fit.  
WHY_INTERESTING: avoids a costly provider lock-in and lets model selection evolve independently from post/visual intelligence.  
ORIGIN_OR_EVIDENCE: provider-neutral rendering recommendation  
RELATED: IDEA-LIG-002  
PROMOTION_OR_REVISIT_TRIGGER: Replicate fails acceptance, materially better provider evidence appears, or provider economics/capabilities change  
DECISION_OR_RATIONALE: preserve capability, do not implement multiple adapters prematurely  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-007 — Direct LinkedIn publishing with Buffer as a fallback path

STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: approval-gated publishing  
IDEA: Prefer official direct LinkedIn API publishing when practical; retain Buffer as a credible fallback/accelerator if direct integration becomes unnecessarily costly or restrictive.  
WHY_INTERESTING: preserves control while avoiding a hard dependency on an intermediary and keeps a practical alternative available.  
ORIGIN_OR_EVIDENCE: 2026 LinkedIn publishing/API research  
RELATED: IDEA-LIG-008, IDEA-LIG-009  
PROMOTION_OR_REVISIT_TRIGGER: content + visual package acceptance clears and publishing Slice D begins  
DECISION_OR_RATIONALE: publishing architecture is accepted at a high level, provider choice remains deliberately deferred until implementation evidence is current  
PROMOTED_TO: `CURRENT_WORK_PACKET.md` → Slice D (high-level publishing sequence only)  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-008 — Human-approved reply assistance on Graham's own posts

STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: post-publication engagement  
IDEA: Surface comments on Graham's published posts through supported access, draft Graham-voice replies, and require human approve/edit/ignore before posting.  
WHY_INTERESTING: reduces response effort while preserving Graham's reputation and avoiding autonomous relationship management.  
ORIGIN_OR_EVIDENCE: LinkedIn automation research  
RELATED: IDEA-LIG-007, IDEA-LIG-009  
PROMOTION_OR_REVISIT_TRIGGER: publishing is reliable and legitimate comment-read/reply access is available  
DECISION_OR_RATIONALE: later capability; no autonomous reply posting initially  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-009 — Post-performance analytics feedback loop

STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn content learning  
IDEA: Collect legitimate post-performance signals after publishing and compare predicted content goals/quality with actual reach, engagement, comments, shares, and follower/business outcomes to improve future opportunity selection and strategy.  
WHY_INTERESTING: moves the system from generic LinkedIn best practices toward Graham-specific evidence.  
ORIGIN_OR_EVIDENCE: deep LinkedIn performance research + discussion of learning from real published outcomes  
RELATED: IDEA-LIG-004, IDEA-LIG-008, IDEA-LIG-010  
PROMOTION_OR_REVISIT_TRIGGER: enough approved posts have been published through a reliable path and legitimate analytics access exists  
DECISION_OR_RATIONALE: later learning layer; avoid optimizing from tiny samples  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-010 — Learn correction patterns from Graham's human review

STATUS: CANDIDATE  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: content-quality learning  
IDEA: Aggregate explicit keep/edit/reject reason codes and approved/edited posts to identify repeatable generator defects and improve rules only when the evidence shows a stable pattern.  
WHY_INTERESTING: prevents repeating the same manual corrections and makes the generator progressively better without treating raw generated text as voice truth.  
ORIGIN_OR_EVIDENCE: existing reason-coded feedback contract + Graham Spoken Voice work  
RELATED: IDEA-LIG-009  
PROMOTION_OR_REVISIT_TRIGGER: enough review events exist to distinguish a pattern from one-off preference  
DECISION_OR_RATIONALE: current feedback capture exists; automatic learning/promotion remains deliberately unimplemented  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-011 — Selected external-post comment assistance without feed crawling

STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: external LinkedIn engagement  
IDEA: When a relevant external LinkedIn post is legitimately supplied to the system, evaluate whether Graham has something substantive to add and draft a comment for approval; do not crawl the home feed or mass-comment.  
WHY_INTERESTING: can increase useful visibility while respecting current LinkedIn access/policy constraints and avoiding generic engagement bots.  
ORIGIN_OR_EVIDENCE: LinkedIn API/policy research  
RELATED: IDEA-LIG-008  
PROMOTION_OR_REVISIT_TRIGGER: publishing/reply workflow is reliable and a legitimate selected-post input path exists  
DECISION_OR_RATIONALE: intentionally later; feed crawling/autonomous mass commenting remains excluded  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01

---

## IDEA-LIG-012 — Revisit broader member-post/feed automation if official LinkedIn access changes

STATUS: SHELVED  
CAPTURED_AT: 2026-09-01  
OWNER_OR_CONTEXT: LinkedIn API capability monitoring  
IDEA: Re-evaluate broader member-post reading/comment workflows if LinkedIn opens official member feed/post access or materially changes partner eligibility.  
WHY_INTERESTING: the desired engagement workflow is currently constrained more by official access than by our ability to build it.  
ORIGIN_OR_EVIDENCE: LinkedIn API research; existing LinkedIn API Watch automation monitors material changes  
RELATED: IDEA-LIG-008, IDEA-LIG-011  
PROMOTION_OR_REVISIT_TRIGGER: LinkedIn API Watch reports a material access change  
DECISION_OR_RATIONALE: shelved until official access changes; do not work around the restriction with prohibited automation  
PROMOTED_TO:  
LAST_REVIEWED: 2026-09-01
