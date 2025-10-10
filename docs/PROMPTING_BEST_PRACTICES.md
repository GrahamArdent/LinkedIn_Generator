# Prompting Best Practices We Apply

**Goals:** clarity, credibility, and consistency across personas.

## 1) Structured prompting
- Separate `system`, `user_template`, `critique`, and `constrain` prompts.
- Constrain to a JSON schema, then format to text; reject invalid outputs.
- Keep word targets and rhetorical structure explicit (hook, POV, proof, plays, quote, CTA).

## 2) Persona-true voice
- Voice traits (`config/personas.yaml`) are injected into context.
- We never “switch tone randomly”; persona is resolved by schedule or explicit override.

## 3) Source hygiene
- Quotes can be from anywhere (with attribution).
- Proof sources are filtered to whitelisted domains (`config/source_whitelist.yaml`).
- Links go in the **first comment** to preserve reach.

## 4) Safety & claims
- Avoid guarantees and private data.
- Encourage anonymized examples and precise verbs.
- Require a single, realistically attributable proof-point.

## 5) Review loop
- Optional LLM rewrite → critique → constraint to JSON → render to text.
- Built-in validators: hashtag count, no em dashes, link stripping.

