# Graham authoring — current local workflow

Current release and rollback identities are recorded in `evidence/operational-implementation-20261106/INSTALLATION.json` and `CURRENT_WORK_PACKET.md`. The supported entry is `/home/graham/.local/bin/linkedin-codex` on the Execution Node, account graham. It uses GPT-6 SOL medium through the existing ChatGPT subscription; no API fallback. Graham chose this available default after the live model list did not offer6.1 SOL.

Create from an ordinary topic, or add a primary-source URL:

```sh
linkedin-codex create --id my-stable-request --topic 'A topic to examine'
linkedin-codex create --id another-stable-request --topic 'A topic to examine' --url https://publisher.example/article --narrative symbolic
```

A source-insufficient result is a HOLD, not a generated post. Retained exact-topic source URLs and recent successful source fetches are reused automatically. Other topics use bounded Crossref discovery; coverage is limited and blocked/irrelevant sources are reported. The current qualification store preserves unresolved historical first-six/8-subject accounting: new genuine subjects are held until that owner history is reconciled. Do not create another store to avoid this gate.

The command owns evidence, explicit meaning/narrative preparation, the existing writer/four essentials, at most one guarded rewrite and an exact selected-text/visual-plan package. A visual plan is not a rendered image. Scores do not approve publishing.

```sh
linkedin-codex list
linkedin-codex show --id graham-operational-url-symbolic-20261106-r1
linkedin-codex resume --id my-stable-request
linkedin-codex export --id graham-operational-url-symbolic-20261106-r1 --path /absolute/export-directory
linkedin-codex serve --port 18768
```

Open `http://127.0.0.1:18768` on that computer for Create, Voices, Review/history, ordinary feedback controls and download. It binds loopback only. A mobile viewport was tested in a real browser; remote access from Graham's phone is not configured or claimed. Reload, show, feedback and export do not generate. The UI restores the selected job and can start a new request without generating until Create is clicked.

Exact duplicate IDs reopen their original result. Changed same-ID inputs conflict. A deliberate revision uses a new ID plus `--parent original-id`; it inherits the admission's original start, model usage and HTTP allowance. A genuinely new admission requires explicit `--new-budget` under current owner authority; it cannot silently reset an exhausted/unknown admission. Pending effects reconcile original receipts without redispatch. Failed inputs/results remain retained.

The shared cap is12 model executions/900 cumulative active CLI seconds and900 whole-job wall seconds, API0; network is bounded to8 discovery requests/6 source fetches with finite sizes, total timeouts and public-address/redirect checks. Known completed reads work after expiry. Receipt-only recovery has a separate bounded no-dispatch allowance. Never switch output directories or labels to evade a conflict/cap.

Human edits use `edit --id ID --path edited-text.md`; original bytes remain unchanged. The new revision invalidates review/visual/publication readiness. `feedback --id ID --path feedback.json` records supplied judgments only; the UI supplies ordinary form controls. Voice examples require an explicit approval-bearing decision and separate `activate-voice --id ID --hash EXACT_HASH`. Preference alone does not activate examples. Exports include exact selected text plus a source/voice/structure/revision manifest; edited text is clearly marked revalidation-required.

The stable data root is `/home/graham/.local/share/graham-linkedin`, outside releases. Initialization is explicit; missing/corrupt stores never silently relaunch jobs. `backup --path /new/absolute/backup-directory` takes a consistent registry/artifact snapshot. The original ten retained trial records, failures, policy identities, historical usage and B preference were imported without rewriting them. Do not infer human ratings or publication approval.

The runtime is `/home/graham/.local/share/graham-linkedin-runtime/operational-v2-20261106`: a copied interpreter, locked dependencies and independent immutable client clone at `a609c6d344037152c24cb81baabdb0fd9a6e9b00`. It does not import the disposable development environments. Reconstruction: `scripts/install_linkedin_runtime.py --help`; use a new immutable runtime prefix, then qualify before promotion. The installer does not promote a launcher.

`prepare`, `generate`, `complete-comparison`, legacy direct API and historical Streamlit entry points remain compatibility/development surfaces. They are not qualified standalone Graham entry points; use the shared application above. Historical `show --out DIR` remains a zero-call read. Earlier release receipts remain under their owner evidence directories; no raw-generate instructions are current quick-start directions.

Human prose/visual judgments, Q6 transfer and the retained26 AT/11 E2E gates remain separate. Rendering and Dedication-owned approval/scheduling/publication remain gated.
