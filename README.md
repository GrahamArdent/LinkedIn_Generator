# LinkedIn_Generator

LinkedIn content-generation engine under active rebuild.

The target product is **not a Streamlit application**. The repository still contains historical Streamlit prototype files under `ui/` and legacy UI dependency/run artifacts; treat those as migration evidence until they are explicitly retired or a specific behavior is salvaged.

## Product role

LinkedIn Generator owns LinkedIn-specific content intelligence, including the evolving generation pipeline, persona/voice behavior, evidence/citation handling, hooks/structure, CTA and hashtag policy, validation, and content outputs.

The rebuilt engine is intended to be usable independently for development/testing **and** callable by the Dedication ecosystem.

### Dedication boundary

Dedication owns generic orchestration concerns such as:

- Action selection and prioritization;
- scheduling and Day orchestration;
- canonical user/day state;
- shared permissions and external integration policy;
- notifications/interventions.

LinkedIn Generator must not create competing versions of those mechanisms. It should accept a bounded LinkedIn content request and return a structured LinkedIn result.

## Current repository evidence

The existing implementation under `src/app/` contains useful but prototype-era behavior for:

- persona-aware generation;
- planning/drafting/judging passes;
- research/citations;
- topic selection and legacy scheduling;
- CTA/hashtag/house-rule configuration;
- text and carousel rendering;
- output logging and validation.

These assets are being assessed individually. Existing code is neither discarded merely because it is old nor preserved merely because it exists.

## PROGRAMSTART / PROGRAMBUILD

PROGRAMSTART is adopted in **Mode C** as methodology only. LinkedIn Generator remains the owner of its product implementation and project-specific authority.

## Tests

```bash
pytest -q
```
