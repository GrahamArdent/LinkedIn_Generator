# Writing voice selector — fresh review and correction

Reviewed368236c..a09ca75 read-only. No Critical findings. Initial verdict HOLD.

Reviewer independently matched all152 projected trait values (19 traits x8 presets) to pinned V2 persona_presets.py blob f008ebd158a4840bb6a501db4ee2e9f02afb4524. Ninth profile is craft-only. Omitted selection preserves legacy generator call signatures.

Important findings and observed corrections:
- Retained completion could draft baseline against a changed live style but score against an old frozen context. Record the resolved style, reject changed definitions before completion/baseline calls; historical completed reads remain zero-call even when catalogue is unavailable.
- Inherited examples/Graham prose instructions could override explicit selection. Selected style now wins; examples supply compatible details only; Graham-specific prose instructions apply only when no style is selected.
- Deterministic compact-rhythm/contrast penalties still steered explicit styles back to Graham defaults. Suppressed only these inherited style penalties for explicit selection. URL/em-dash/POV/CTA/generic-language checks and factual rewrite guards remain. Model publish-quality threshold/weights unchanged.
- Catalogue admitted substring aliases and nested biography objects in nominal style traits. Validate catalogue/dictionary/alias/list/scalar/numeric shapes and ranges before resolution. No fallback to an empty profile.
- Selected style was missing from terminal preflight telemetry (reviewer Minor). Included as a trace-completeness correction because an explicit request must retain its resolved version/hash even when no post is generated.

Evidence:17 original RED->GREEN cases; review-red.log shows5 demonstrated failures/18 existing passes. review-green.log initially23 PASS, then one characterization test added for completed historical replay under unavailable catalogue. Full final suite and exact receipt own final counts.

Rulings:
- Use generic craft labels at runtime; historical named-author labels remain provenance/aliases only. Cost: display names differ from old catalogue but avoid identity or imitation instructions.
- Keep optional selection separate from identity, leave omitted selection backward compatible. Cost: old callers still use their inherited defaults until they explicitly select a style.
- Suppress inherited style-specific deterministic penalties without introducing a numeric style scorer. Cost: selected-style fitness remains semantic/human judgment rather than a formatting score.
- Fail closed on changed style during retained completion; never rerun the engine automatically. Cost: a mismatched unfinished comparison requires explicit reconciliation.
- Preserve historical completed reads even after catalogue changes. Cost: historical outputs remain historical; they do not establish the current definition's acceptance.

Declined to judge: perceptible style differences, human writing quality, engagement, deployment or merge readiness. Those remain unproved; fixtures are not human acceptance. No native model calls or paid API spending in this milestone.
