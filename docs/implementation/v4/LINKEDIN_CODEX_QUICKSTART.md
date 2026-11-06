# Current use versus historical quick-start

Installed product:5bd3478709d98e5eb3ff5fd11168718aa3868cbd. Current installed prepare/generate usage and rollback:
[evidence/structure-install-implementation-20261105/REPORT.md](../../../evidence/structure-install-implementation-20261105/REPORT.md)
and INSTALLATION.json in that directory. New Graham generation requires validated prepare output and its source bundle.
The ordinary self-operating create/feedback/export workflow in active R1–R8 is planned, not implemented.

The older installation paths, raw generate example and optional-handoff wording below are historical for those releases;
they are not current instructions for a new Graham job. Preserve them as historical receipts, not a second supported workflow.
R7 will replace this legacy section with verified help for the installed operational interface.

---

# LinkedIn + Codex: quick local connection

Ready on **execution-node**, account graham. Uses ChatGPT subscription authentication; no API key or paid API fallback.

- Installed checkout: `/home/graham/work/linkedin-generator-releases/0c099d70fc807044355af089d62d1bef049cbb95` (detached merged revision0c099d7; development checkout and old evidence retained separately)
- LinkedIn Python: `/home/graham/work/linkedin-generator-releases/0c099d70fc807044355af089d62d1bef049cbb95/.venv/bin/python` (reuses the qualified dependency environment)
- Reused Resume Python: `/home/graham/work/resume-v6-smoke-venv/bin/python`
- Pinned Resume client snapshot: `/home/graham/work/linkedin-resume-client-20261104`, source `a609c6d344037152c24cb81baabdb0fd9a6e9b00`
- Codex: `/usr/local/bin/codex`, qualified CLI0.158.0, ChatGPT login, model `gpt-6-astra`, reasoning `medium`
- Local paths/config: `.codex-linkedin.local.json` in the LinkedIn checkout (git-ignored); example in `config/codex_runtime.example.json`. Credentials remain in Codex's own store.

## Use it

Read the retained first trial, with **zero generation**:

```bash
/home/graham/.local/bin/linkedin-codex show --out /home/graham/work/linkedin-codex-trial-20261104/evidence/codex-first-20261104/trial
```

For an explicitly admitted new subject/batch:

```bash
/home/graham/.local/bin/linkedin-codex generate --request /absolute/path/request.json --out /absolute/path/new-trial-directory
```

Run offline checks:

```bash
cd /home/graham/work/linkedin-generator-releases/0c099d70fc807044355af089d62d1bef049cbb95
.venv/bin/python -m pytest -q
```

The launcher supplies the local runtime config. The Python script can also be called directly with `--config .codex-linkedin.local.json`. Use a new request ID/output directory only for a genuinely new admitted trial, never to bypass an exhausted or unknown attempt. No paid fallback exists.

## Behavior

The existing LinkedIn Python engine calls one thin provider bridge. The bridge imports the pinned Resume Codex client in its qualified interpreter; it does not copy that implementation or alter resume results. The model has tools disabled. Exact prompts and validated JSON results are retained by the existing client.

One batch shares a36-physical-process/900-second cumulative budget: at most12 model executions, with version/auth starts counted separately. API temperature is not applied by Codex; model/reasoning are the actual comparable settings. An ambiguous/missing bridge receipt is unknown and blocks replay. Reads return saved results.

First-trial pair is in `evidence/codex-first-20261104/trial/review.md`. Its engine gate remains **HOLD_NO_QUALIFIED_CANDIDATE**; comparison completion is not product acceptance. Human feedback is still required. No renderer, UI, external service, publishing, hosted CI, merge or deployment is installed by this local launcher.

## Select writing style independently

Add optional writing_voice_id to the request JSON. Canonical IDs are concise_challenger, reflective_leader, counterintuitive_analyst, direct_motivator, purpose_led, practical_experimenter, balanced_authority, technical_explainer and relatable_provocateur. persona_key still identifies the author configuration; author_pov still controls I/we. Known historical preset IDs are accepted as aliases and canonicalized. Omit writing_voice_id to retain previous defaults. Unknown explicit IDs and malformed definitions are rejected before generation. Runtime prompts/telemetry include the selected version and content SHA256, excluding historical biographies, audience substitutions and named-author imitation instructions. Catalogue: config/writing_voices.json. For a controlled comparison change only writing_voice_id, keeping all other inputs fixed. Show and completed replay retain original output without launching a new attempt.

## Narrative handoff through normal requests

Optional editorial_handoff now travels through LinkedInContentRequest, generate_content, the writer/evaluator and the simple comparison baseline. Use the validated version1 meaning/narrative shape from src/app/editorial_handoff.py; an optional writing_plan may annotate delivery. Unsupported or malformed shapes fail at request admission. Omission preserves existing behavior. Literal and symbolic are the currently supported forms; no equal post-word-count requirement is imposed. This release is being promoted through the same linkedin-codex launcher with fixed source revisions and rollback; the current installed receipt is maintained in CURRENT_WORK_PACKET.md.

## Installed release and rollback

Product merge and installed revision:0c099d70fc807044355af089d62d1bef049cbb95, PR24. Source, imports, full230-test suite and saved-result reopening verified. Canonical current receipt: evidence/release-integration-20261105/INSTALLATION.json on main; host copy: /home/graham/work/linkedin-generator-releases/INSTALLATION.json. Prior93a9ee3 and original launcher are preserved. The rollback target passed its saved-result smoke check without activation. Rollback command: `install -m 755 /home/graham/work/linkedin-generator-releases/rollback-20261105/rollback-launcher.sh /home/graham/.local/bin/linkedin-codex`. No new model generation, API spend, hosted CI or publication occurred during promotion. A later receipt-only main commit does not require reinstalling identical product code.
