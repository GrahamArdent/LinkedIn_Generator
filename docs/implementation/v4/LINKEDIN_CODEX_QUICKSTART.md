# Current text feedback, examples and review

The installed P1 loop has an actual ordinary topic→draft→edit/export/reopen receipt. Native pilot and test edits do not establish human acceptance. Current release/proof is selected in CURRENT_WORK_PACKET.md and the same evidence owner.

The shared UI records actual supplied preference, editing effort and explicit reusable-example approval against the current brief/text version. Approval does not activate an example. **Activate explicitly approved voice example** is a separate action; selecting another text/context clears inherited approval fields. Machine test feedback cannot activate a real example. CLI activation of writing items also requires exact versions:

```sh
linkedin-codex activate-voice --id WRITING_ITEM_ID --hash TEXT_SHA256 --expected-brief BRIEF_REVISION --expected-text TEXT_VERSION
```

No score is invented when advisory ratings are unavailable. Complete valid essentials govern qualified selection; incomplete essentials preserve available findings while remaining unavailable. A supplied personal viewpoint is an attributed observation of that statement, not proof of an external event, measured gain or credential. Mixed inputs retain their exact public source support. No arbitrary evidence-free factual route is claimed.

Optional visual-planning failure is deferred independently of saved qualified text. Paid image requests, exact post/image approval and original UNKNOWN provider recovery remain with the existing rendering owner. Failed pre-dispatch authoring starts are retained as item observations, never automatically enrolled in the historical experiment.

---

## P1 ordinary authoring help

# Current ordinary writing workflow — November 16, 2026

Ordinary authoring is separate from the unresolved historical experiment. Its subject-history restriction applies only to explicitly enrolled trials. The prior quick-start below describes historical release behavior; it must not block this ordinary loop.

Use the shared loopback UI: enter a topic and notes, then **Save idea** (no model) or **Draft this / revise**. IDs and version guards are automatic. Current text stays editable/exportable when assessment is unavailable. A conflict retains the unsaved edit; compare before saving against the new current version. **Check current text** assesses without rewriting. Feedback never activates a voice example implicitly.

When turning a conversation into a brief, copy the relevant words directly from the author. In Notes, start a line with `AUTHOR WORDS:` followed by the exact passage. Put your own account of the point on a separate `EDITORIAL SUMMARY:` line. If only a summary exists, use that line alone. A liked chat draft supplies an editorial reference; its first-person sentences are not author testimony. Use `EDITORIAL DIRECTION:` for the intended reader and what they should recognize or decide. Leave Narrative on “Choose for the reader” (CLI: omit `--narrative`) to have preparation select the form and beats after the reader and takeaway. An explicit literal or symbolic selection is honored. Ordinary freeform notes still work. A factual source passage must be complete and at most 600 characters.

When the point or a necessary fact is missing, the same preparation step can return one question about this topic. Answer it in your own words and select “Add my answer to the brief.” Saving the answer preserves your wording and makes no model call. Select “Draft this / revise” to use the updated brief. In the CLI, `show` returns the current `author_question`; update Notes with `save-idea` against the displayed brief revision. If the brief already establishes the point, preparation proceeds directly to writing.

After saving a manual edit, open “Compare this edit with its parent.” Read the two endings and identify which words carry the author’s judgment, what the reader gains, and what the edit cuts or preserves. A manual save makes zero model calls. “Check current text” requests a review of this version against its actual parent. A cited passage and the reviewer’s explanation are shown with each finding. CLI `show` includes the version history and saved review.

CLI uses the same application/store:

```sh
linkedin-codex save-idea --topic 'My intended point' --notes 'My supplied account'
linkedin-codex draft --topic 'My intended point' --notes 'My supplied account'
linkedin-codex show --id WRITING_ITEM_ID
linkedin-codex export --id WRITING_ITEM_ID --path EXPORT_DIRECTORY
linkedin-codex edit --id WRITING_ITEM_ID --path EDITED_TEXT_FILE --expected-brief BRIEF_REVISION --expected-text TEXT_VERSION
linkedin-codex recheck --id WRITING_ITEM_ID
linkedin-codex draft --id WRITING_ITEM_ID
```

`save-idea` without an ID returns a new saved item. A separate new `draft --topic` starts a new item; use the saved ID to continue one item. Deliberate draft/recheck actions generate an attempt ID and capture expected versions automatically; automation can supply explicit `--attempt`, `--expected-brief`, `--expected-text` for idempotent retries. Uncertain existing attempts must reconcile via their original `resume --id ATTEMPT_ID`, not a new attempt. Each deliberate action retains its declared finite allowance; consumed/expired historical requests are unchanged. Capture and read/edit/export need no provider configuration.

Working exports carry exact current bytes/status, not qualified/approved/visual-ready/published claims. Human content/voice/image approval and actual publication remain distinct. Candidate behavior is not installed until exact release receipts establish it. Current results and one RESUME_AT remain in the existing evidence item linked by CURRENT_WORK_PACKET.md.

---

## Prior release quick-start — historical

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
