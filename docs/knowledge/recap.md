# Recap for knowledge you can read and retrieve later

English | [简体中文](recap.zh.md) · [All guides](../README.md)

`recap` turns a selected conversation into topic documents preserving explanations, reasons, procedures, and sources. It also queries existing topics and maintains selected knowledge. Use it for material you will need to understand again, such as debugging methods, engineering decisions, and repeatable procedures.

A long conversation may cover two independent questions and later correct one conclusion. The resulting knowledge should explain each topic, identify the correction, and show what supports the current account. A chat date or a few conclusions alone cannot do that.

File descriptions below follow the [execution instructions](../../skills/knowledge/recap/SKILL.md), [document contract](../../skills/knowledge/recap/references/formats.md), and [helper implementation](../../skills/knowledge/recap/scripts/knowledge.py). Reading this guide does not initialize a library.

## Choose a knowledge-library location

Root selection uses an explicit root first, then `RECAP_KNOWLEDGE_ROOT`, then `~/.agents/knowledge`. This is a separate knowledge directory; working on a project does not automatically select that project as the destination.

The helpers need Python 3 and Git. Full-text search normally uses SQLite FTS5 provided through Python. An explicit text-search fallback is available when FTS5 is absent. The assistant reads the library's own `AGENTS.md` before accessing its contents.

**Initialization creates a Git repository and its first commit.** Candidate inspection and formal publication can create further commits. If you require no Git commits, request an uncommitted draft before starting these workflows.

## Request a capture with explicit boundaries

Replace the example directory with your chosen location.

```text
$skills:recap
Turn this conversation's debugging methods and decision reasons into topics.
Use /path/to/my-knowledge and check its existing rules first. Preserve context,
evidence, failed attempts, applicability, and source locations. Show proposed
new or updated topics and actual destinations before running steps that create
Git commits. Wait for my confirmation for those steps. Leave this project's Git
state untouched.
```

This uses the collection's Codex plugin. Use `$recap` standalone or `/skills:recap` in Claude Code. Invocation is explicit; ordinary conversation does not automatically trigger capture.

## Follow capture into publication

The assistant establishes the selected conversation, branch, and inspected coverage, then searches related topics. Existing explanations should absorb appropriate findings instead of producing similar copies for every chat. Guesses, executed checks, and user corrections need distinct treatment.

It prepares topic bodies and necessary source records. Coverage gaps and unread attachments remain visible. Locators support traceability, but deleting the original chat leaves only retained excerpts independently inspectable; full replay is not guaranteed.

The capture workflow has six stages: establish coverage, develop topics, select writing guidance, prepare a candidate, integrate and review, then publish and verify. Each stage states its completion condition. The [command checklist](../../skills/knowledge/recap/references/checklist.md) supplies the ordinary helper sequence.

References are selected by the current step: source recovery, continuity, topic fields, source fields, approval or recovery. A short source uses the same coverage and publication checks. Topic summaries select relevant reading before the assistant opens full topics.

For local extraction, `sessions.py show CHUNK` displays one chunk as text with original locators and fragment offsets. It wraps long lines for display and leaves the JSONL files unchanged. The assistant reads the receipt and one text view per chunk; targeted rereads remain available for truncation or corrections. Whole-output limits still require bounded reading. See [chunk reading](../../skills/knowledge/recap/references/sessions.md#read-extracted-chunks).

Formal updates use a candidate worktree and checks. Concurrent changes to the same content require independent review. Publication uses the same candidate hash that was inspected and approved. Current task authorization and existing approval rules determine when explicit user approval is required. Saved prose and important retrieval must pass verification before cleanup. Claimed incremental progress must have its cursor published with the represented knowledge. `cleanup` removes only the matching published worktree and branch; raw extraction needs separate removal of the exact directory created for this operation. If host policy blocks deletion, report the retained location rather than bypassing the block. Moving or renaming data does not prove deletion. Failed or pending work remains available.

## Know the resulting files

This illustrative layout shows items that may appear after initialization, capture, and search. Topic names should describe a reader's question, normally in the user's language.

```text
my-knowledge/
├── AGENTS.md
├── index.md
├── CHANGELOG.md
├── topics/
│   └── a-specific-topic.md
├── sources/
│   └── host-session-id.md
├── drafts/
├── .git/
├── .state/
│   ├── library.json
│   ├── index.sqlite
│   ├── cursors/
│   └── published/
└── .worktree/
```

| Location | Contents and creation condition |
| --- | --- |
| `topics/**/*.md` | Formal explanations, examples, applicability, and source links |
| `sources/<host>-<session-id>.md` | Source identity, inspected coverage, gaps, and necessary supporting excerpts |
| `index.md` | Generated topic catalog and an introduction maintained through approved candidates; trailing prose is preserved |
| `CHANGELOG.md` | What knowledge changed and why |
| `drafts/` | Unpublished material, including drafts with unresolved coverage gaps |
| `.state/library.json` | Library format, branch, and related machine state |
| `.state/index.sqlite` | Cache created or updated by FTS5 search, not formal topic prose |
| `.state/cursors/` | Incremental-conversation checkpoints when needed, published with the knowledge they represent |
| `.state/published/` | Publication-operation records |
| `.worktree/` | Candidate worktrees; successful cleanup can remove the operation's directory |

Initialization also creates `.gitignore` and internal directories such as `.history/`. These locations do not need manual filler. Machine state, candidates, and search caches cannot replace readable `topics/` content.

## What a topic should look like when opened

A capture of this collection's packaging discussion could begin with this excerpt. It is a teaching example, not a file already saved in your library. Actual publication generates the document metadata.

```markdown
# Checkout policy for external skill submodules

This topic explains why the collection leaves external upstream
repositories unchecked out. It applies to the current packaging layout where
ten bundled skills share categorized directories.

## Rule and reason
The external references are Git submodules with update = none in .gitmodules.
Complete upstream repositories contain other skills that can affect recursive
discovery when checked out.

## Verification
Confirm the external references remain gitlinks and normal initialization skips checkout.
Then verify that installer discovery still returns ten bundled skills.

## Source
Consult the [conversation record](../sources/host-session-id.md), retaining actual
message coverage and necessary excerpts.
```

The topic should explain the reason and when verification matters again. A single sentence saying not to initialize submodules would omit applicability and checks.

## Retrieve the knowledge later

Ask a specific question. Default search covers formal topics rather than mixing drafts and raw source records into ordinary results.

```text
$skills:recap
Find knowledge about export permission checks. Explain why they belong at the
shared service entry point, and identify the relevant topic and source.
Do not add or modify formal knowledge in this query.
```

Queries can update caches and lock files. Query-only use does not imply zero disk writes. State a strict read-only requirement first if that is necessary, so the assistant can establish a suitable access method.

Search uses separate title, alias, summary and body fields. Dates, status and source-path metadata do not create matches. Defined reference-link keys are also excluded; visible labels remain searchable. Keep identifiers such as `session.prompt`, `foo_bar` and `std::vector` intact; their separate components are also searchable. Requesting `session.prompt` excludes pages that mention only `session.stop` and `client.prompt`.

Results include a body excerpt and its original file line number. Excerpts follow normalized token matches, including phrases across punctuation or lines. An alias-only match can show the opening body text, so read the topic before drawing a conclusion. Search still depends on literal terms; use short keywords and alternate wording. For example, ask “Find `session.prompt` and explain its completion behavior” or “Search `并发 写入` and explain the lock requirement.” See the [search contract](../../skills/knowledge/recap/references/search.md) for matching and cache details. Existing search caches rebuild automatically without changing formal topics or their Git history.

From this collection's root, this capability check does not create the library. Replace the example root.

```sh
python3 -B skills/knowledge/recap/scripts/knowledge.py --root /path/to/my-knowledge doctor
```

The report includes `portability.ok` and line-specific errors. This static check covers only explicit UTF-8 `read_text()` calls and resolved Git-root comparisons in `workflow.py`; it does not inspect other files or `bytes.decode()` calls. Such errors exit 2 without initializing or writing the library; a passing static check is not a full health check. Windows paths are compared as resolved paths and knowledge text is read as UTF-8, independently of the locale.

An existing populated directory needs migration review rather than empty-library initialization. See [publication, migration, and recovery](../../skills/knowledge/recap/references/operations.md).

## Maintain routes and locate pending work

```text
$skills:recap
List retained operations and identify missing candidate worktrees.
Update the index.md introduction to cover the current topics.
Prepare a candidate and show its diff before recording my approval.
Preserve unpublished candidates and unrelated local files.
```

`knowledge.py status --all` lists operation records, worktree/branch presence, publication-record presence and interrupted transactions. An old `ready` operation is not automatically abandoned. Cleanup remains limited to matching, successfully published candidates.

For retained work, start with `status --all --summary`. It omits hashes and worktree paths while retaining every operation, per-entry error, review/conflict state and interrupted transaction. Open details with `status OP` and `diff OP`. A new capture starts with `begin OP` instead of listing all historical operations. The summary reduces output volume; it performs the same inventory checks.

The summary retains other operations and recovery information when one operation record is damaged. That entry contains an error and the summary sets `complete: false`; check this field even when the inventory command exits successfully. Library metadata and recovery-journal errors still stop the command. `worktree_exists` reports directory presence only, not valid Git identity or publication readiness.

Guide maintenance changes only the introduction before the generated topic catalog. It uses the same candidate, integration and publication flow as topic changes, with explicit approval of the current candidate hash. Concurrent introduction changes require independent review; a newer generated catalog alone does not. No direct formal-guide edit is necessary. The [guide-maintenance decision](../agents/adr/0005--recap-guide-maintenance.md) explains the boundary.

Initialize a new empty library through [first-capture setup](../../skills/knowledge/recap/references/checklist.md#first-capture). Once coverage, topics and writing guidance are ready, first and repeated captures use the same [publication commands](../../skills/knowledge/recap/references/checklist.md#publication-commands). The input example declares the topic, source and cursor together. Local body links must be root-contained relative paths, not absolute machine paths; [body links](../../skills/knowledge/recap/references/formats.md#body-links) and [capture cursors](../../skills/knowledge/recap/references/formats.md#capture-cursor) define those branches. Failed inspection can leave candidate files dirty without changing the formal library; preserve and investigate that candidate instead of resetting the root.

Use the [command checklist](../../skills/knowledge/recap/references/checklist.md) for ordinary publication. `knowledge.py packet OP --from-dir DIR` computes hashes from the operation base and converts declared topic/source/cursor inputs into a structured packet. Authors still supply reasons, evidence and honest coverage. `reason` is a nonempty single-line string; `evidence` is a nonempty array of distinct nonempty single-line strings, including for one locator. Save redirected JSON as UTF-8 using the [output guidance](../../skills/knowledge/recap/references/operations.md#utf-8-redirected-output). Generation does not run `inspect` or publish the candidate. See [input-directory format](../../skills/knowledge/recap/references/formats.md#packet-input-directory).

Packet generation requires a clean formal root and a clean, existing editing candidate with matching repository and branch identity. It reports problems before reading declared documents and leaves external files intact. A newer clean formal revision does not change the operation's base hashes. Individual input checks do not replace whole-candidate link and source validation by `inspect`.

For OpenCode, use the exact `session_v2.id`, not a workspace directory name. Cutoffs use OpenCode `session_message.seq`, not OpenChamber cache sequences or display turns; map coordinates using a shared message ID or explicit metadata. The [host notes](../../skills/knowledge/recap/references/sessions.md#host-notes) explain this boundary. OpenCode message sequences represent event positions and can begin after 1 or contain gaps. The extractor preserves those positions and records numeric gaps separately. Complete extraction means the supported persisted snapshot was read; it cannot prove the absence of deleted or unsaved host history. Genuine branch, attachment, format or incremental-prefix problems still prevent a complete receipt.

Tool outputs are excluded by default. `--include-tools` reads supported returned content, not tool inputs or external artifacts. Rendered HTML may therefore need a separate authorized read. A small or `complete` extraction is not proof that tool-dependent claims have supporting evidence. See [helper extraction](../../skills/knowledge/recap/references/sessions.md#helper-extraction).

Before review, generated packets and rendered cursor candidates replace `source.locator` with `redacted:local-source` and omit `incremental.prior_receipt`. Raw receipts and inputs stay unchanged; other metadata and coverage checks remain intact. Old and normalized cursors both support verified incremental extraction. This targets two path fields, not arbitrary secrets or historical Git commits. Review other metadata and excerpts separately; the [cursor contract](../../skills/knowledge/recap/references/formats.md#capture-cursor) defines the limits.

For an external research directory, `research_index.py /path/to/research` prints a Markdown inventory to stdout. It does not write an index or edit a knowledge library. Capture status stays unmarked until separately checked; opening excerpts are navigation aids. Saving the inventory and adding external configuration pointers are separate authorized writes. Read [research inventory](../../skills/knowledge/recap/references/operations.md#research-inventory) before replacing an existing annotated index.

## Decide whether useful knowledge was preserved

Open a topic independently. Its question, applicability, and supporting evidence should make sense without the chat. Search for it using different wording and check that it can be found.

A publication commit, index entry, or success message alone is insufficient. A short summary that omits reasons and operating conditions still needs rewriting. A local library is not itself an off-device backup.
