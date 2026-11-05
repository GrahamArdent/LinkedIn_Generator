# Release integration, merge and launcher promotion

**GO: reviewed implementation merged and installed.** Technical release acceptance is complete for the existing headless launcher. Human approval of posts, broader writing-quality evaluation and publishing remain separate.

## Review and corrections
Reviewed the complete pending implementation against main a714d1ef355ade9ca47a52b301ea477bd0c14f34: the original22 code/config/test files, the CLI/config exclusions, and the release repairs. REVIEW.json records27 paths, hashes, observations and findings.

Two concrete defects were reproduced and fixed:
- Normal JSON requests silently discarded editorial_handoff. Three regressions failed before repair. The contract now validates and retains it; generate_content forwards it; writer, evaluator and simpler baseline receive the same selected meaning/narrative. Existing omitted-selection behavior and zero-call recovery remain covered.
- Numeric extraction consumed trailing punctuation, falsely rejecting an unchanged advisory ID or decimal after a comma. Two regressions failed before repair. Numeric tokens now end with a digit/optional percent, while changed identifiers, decimals and percentages remain rejected. No existing assertions were weakened.

The launcher followed a mutable development checkout. Promotion now points the same command to one detached merged revision; the former release is preserved independently for rollback. This does not create a new engine or service.

Local qualification:230 tests PASS in3.09s; installed checkout:230 PASS in2.58s. Source/config/tests match reviewed sourceba4af210239e113790faf972e0dd15d822942fb5. All26 acceptance objectives/11 E2E definitions remain unchanged.

Different final-post word counts are descriptive and do not fail this release. No same-length writing requirement was added. Human/editorial concerns in retained samples were not silently converted into technical merge blockers or rewritten away.

## Actual merge and installation
PR24 was merged with expected reviewed head00461009db4e1378045986fc4ec68a153b8bf171. GitHub independent readback confirms merge0c099d70fc807044355af089d62d1bef049cbb95.

Installed source:
- Revision:0c099d70fc807044355af089d62d1bef049cbb95
- Root:/home/graham/work/linkedin-generator-releases/0c099d70fc807044355af089d62d1bef049cbb95
- Launcher:/home/graham/.local/bin/linkedin-codex
- Qualified dependency environment reused through the release's .venv symlink. The executable script and imported project modules resolve to the fixed release source.
- Reused Resume client remains pinned ata609c6d344037152c24cb81baabdb0fd9a6e9b00; relevant client paths clean.
- Codex0.158.0, ChatGPT login status verified. No credentials saved.

INSTALLATION.json and PROMOTION_INTENT.json contain exact paths/hashes/commands. promote.py records the one performed transition. It asserts the admitted main revision before acting and is not an automatic updater; do not blindly rerun it after main advances.

## Expected versus observed
| Check | Expected | Observed |
|---|---|---|
| Request narrative propagation | Same selected form reaches actual orchestrated consumers | New real-consumer fixture regressions PASS, including baseline/evaluator and duplicate recovery |
| Numeric factual guard | Punctuation alone allowed; changed numeric value blocked | Positive and negative regressions PASS |
| Merge identity | Exact reviewed candidate merged | GitHub PR24 merged head0046100; merge0c099d7 |
| Installed revision | Launcher bound to merged code | git HEAD0c099d7 at detached release; launcher SHA recorded |
| Imports | Installed release modules | API/contracts/integration __file__ paths all under fixed release; handoff request field present |
| Installed tests | Same full suite passes in target environment |230 PASS |
| Saved-result reopening | Completed historical output recovered without regeneration or promotion | state completed and engine gate HOLD_NO_QUALIFIED_CANDIDATE exactly as retained |
| Rollback | Previous source/config remains usable | Prior93a9ee3 release and rollback launcher preserved; direct rollback-target show smoke PASS without activation |
| Model effects | No generation from release checks |109 existing attempt records before/after, byte hashes unchanged;0 new model calls/API0 |
| Hosted CI/publication | No unrequested effects | Workflows remain .disabled; no hosted CI or LinkedIn publishing |
| Metadata currentness | Work packet says what is merged/installed | Current packet, quickstart, plan and execution prompt updated with exact release/receipt |

Rollback command and original launcher backup are in INSTALLATION.json. The previous root is /home/graham/work/linkedin-generator-releases/93a9ee3ae85a5f3fcb35ea3cda4d5d44c553809a. Rollback was verified as runnable, not activated.

## What remains
The installation is the existing headless Codex trial/generation command, not a new web UI, renderer, scheduler or publishing service. No new native post was generated in this release milestone. Runtime credential/source readiness and saved-result reopening were checked; these checks do not fabricate a fresh end-to-end human-approved generation.

Human writing preference, scorer calibration, broader multi-subject/baseline evaluation and visual/publishing gates remain open. The narrative contract currently supports literal and symbolic forms; other forms must not silently become literal. The old unsupported screen-location wording remains historical draft evidence, not an approved post.

Documentation-only closure can advance main beyond the installed product merge. MILESTONE.json records installed revision0c099d7 and product hashes separately; the installed code must not be described as stale merely because a receipt-only commit advances main. Future code/config changes require a new reviewed promotion.

## Reproduction
Local/installed test commands and exits are retained in logs/INSTALLATION.json. show was invoked through the real installed launcher with the original absolute saved-result directory. Both new and rollback launchers were checked without generation. Native attempt hashes were compared before/after.

verify.py checks packet hashes and reviewed project-file hashes without credentials or model calls. ARCHIVE_VERIFICATION.json records a clean git-archive verification. MERGE.json is the connected-GitHub merge readback. No deployment or merge result is inferred from a local test.
