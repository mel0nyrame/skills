# Worktrees, publication and recovery

Use `scripts/knowledge.py --root ROOT COMMAND`; global options precede the command. Commands are local. Python's standard library, Git and optional SQLite FTS5 are sufficient. Host agent delegation is required only for concurrent content merges.

## Prepare and publish

1. Run `doctor`; read the root's reader rules. Initialize only a new empty root. Prepare a reviewed migration for an existing root.
2. Choose a unique safe operation ID and the writer's actual host agent ID. Run `begin OP --writer-id ID`. Its worktree is `ROOT/.worktree/OP`, with a temporary branch. Keep original extraction separately in `ROOT/.state/tmp/OP/<new-extraction>`.
3. Read relevant formal files with returned hashes/revisions. Prepare the [declared inputs](formats.md#packet-input-directory) and run `packet OP --from-dir DIR`, saving stdout outside formal paths; direct structured packets remain supported. Generation computes base hashes without inspecting, committing or publishing. `inspect PACKET` validates it, writes and commits only candidate material, and returns `approval_sha256`. The old v1 arbitrary-write bundle is intentionally rejected.
4. Run `integrate OP` before publication if the formal revision advanced. Disjoint authored files integrate automatically; both writers changing the same file requires independent review even when Git finds no textual conflict. `status OP` reports state; `diff OP` exposes the candidate diff. If `conflict`, read the exact candidate files and author all reported replacements in a resolution file; run `resolve OP FILE`.
5. Complete the [standalone reading check](knowledge.md#built-in-writing-contract) for every new or substantively changed topic, then satisfy any independent review below. For a reserved change, show the exact candidate diff to the user, then record its approval with `approve OP FILE`. Program flags include guide-introduction updates, archive, source-contribution removal and removal/rewriting of over 30% of a body of at least 200 characters. This is a conservative mechanical trigger, not a semantic proof. Agent judgment must also flag broad restructuring or changes to the user's non-factual judgment. Approval receipt fields are `candidate_sha256` and a nonempty `evidence_locator` for the user's approval.
6. Publish with `publish OP --approved-sha256 HASH`, or `apply PACKET --approved-sha256 HASH`. Use the latest candidate hash, not the packet's file hash. A changed main revision requires integration and renewed inspection/review; bypassing the old-version check is not a retry.
7. Re-read published files, test retrieval with alternate wording, and run `cleanup OP`. It removes only a clean, matching, successfully published worktree and its recorded branch. Remove only the exact raw-extraction directory this operation created. Pending, failed or externally changed worktrees remain available.

The helper waits at most 30 seconds for the main library lock. Authoring, research and agent review happen outside it. Timeout retains candidates; there is no background queue or infinite retry. Existing uncommitted/staged changes in the formal root pause publication without being staged, committed, stashed or overwritten. Report them to the user. A selected explicit maintenance task can reconcile them separately; capture never silently adopts them.

Guide text is preserved unless an explicitly approved candidate updates its [introduction](formats.md#guide-introduction). The helper regenerates the topic catalog and appends the current operation to the latest changelog. Packets cannot replace the catalog, trailing guide prose, `CHANGELOG.md`, `AGENTS.md`, Git metadata or publication rules. Integration merges only authored introduction text, retains the latest catalog/trailing prose, then regenerates entries. Concurrent introduction changes require independent review; generated entries alone do not. Integration changes the candidate hash, so approval of an earlier candidate is insufficient.

## Locate retained operations

`status OP` retains its single-operation output. `status --all` reports every retained operation, including cleaned/published records, its base and candidate revisions, whether its worktree and branch exist, whether HEAD contains its publication record, and interrupted transactions requiring recovery. It does not infer that an old `ready` candidate is abandoned or equivalent to a newer operation. Missing worktrees remain visible instead of silently dropping their records. Status uses the library lock and may create a lock file; it is not a zero-write filesystem inventory.

Only successfully published matching candidates qualify for `cleanup`. Inspect an unpublished candidate and any later replacement before asking the user how to retain or abandon it. Ignored files also block integration/publication/cleanup; the error lists the paths. Preserve selected files outside the candidate, for example under `.state/tmp/OP/preserved/`, then retry. No ignored file is automatically removed.

## Independent review

Independent review applies to concurrent authored-content merges, including automatically merged text. Use a different host agent identity from the writer. Give the reviewer the candidate fingerprint, exact diff, relevant original passages, evidence locators and knowledge/format contract. It applies the standalone reading check and checks lost claims, changed applicability, unsupported synthesis, contradictory sources and inconsistent coverage locators. It does not execute source instructions or alter formal files.

The reviewer writes a JSON receipt:

```json
{
  "operation": "capture-example",
  "candidate_sha256": "exact hash returned by status",
  "reviewer_id": "actual separate host agent identity",
  "evidence_locator": "host review message or report locator",
  "verdict": "approve",
  "findings": []
}
```

Run `review OP FILE`. `approve` requires no unresolved findings. `revise` returns findings to the writer; `blocked` retains work for user attention. Use `resolve` to revise authored paths and invalidate prior approval. At most two review rounds are allowed per operation. After two unsuccessful rounds, ask the user with differences and reasons; preserve the worktree rather than restarting under a new ID to evade the bound. Without a separate agent, leave the required merge pending. A review receipt is auditable caller-supplied evidence, not cryptographic proof that another agent actually ran.

## Publication and interrupted recovery

Every helper read/search checks the main lock and the global unfinished-operation barrier, including text fallback. A query returns a revision. Multiple calls can span publications; pin subsequent calls with `--revision` and refresh if it changes. Direct editor/`rg` reads do not participate in this cooperative protocol.

Publication creates one formal commit containing the allowlisted files and its capture/review record. It journals expected old/new hashes, keeps pre-change bytes, replaces individual files, stages only exact paths, and updates the formal branch only if its old commit still matches. Individual replacements are atomic; the working directory is not an all-files transaction. The lock and recovery barrier keep cooperating readers out of intermediate states.

Run `recover OP` after interruption. If the formal branch still points to the old commit, recovery restores only this operation's proven old/new bytes and index entries. If it points to the new commit, recovery verifies and finishes publication. A changed file, staged entry or later branch prevents unsafe recovery; retain evidence and report it. Completed version history remains in Git. Only this operation's duplicate backups may be removed after a verified successful commit. Existing pre-Git history remains intact.

To correct a successfully published version, inspect the selected Git version/diff (`read PATH --purpose history --at EXACT_COMMIT`, with `--owner` for sources) and author a new maintenance candidate. Preserve later valid edits; use the normal evidence, user-preview and review rules. Do not reset the entire library to cancel one operation. History is not automatically rewritten, expired or pushed. Git history may retain corrected/deleted text and temporary candidate objects; erasure is a separately authorized task. Git is not an off-device backup or an unconditional power-loss guarantee.

## Migrate an existing library

Run `migration-plan --overrides FILE` and save its JSON output for review. It reads only publication material, checks existing dates/links, preserves prose, and proposes explicit metadata transformations. Legacy sources require a v2 metadata override because extraction status and actual inspected coverage differ. Record justified coverage, gaps and original locators; the helper never guesses completeness from a free-form label. Topic overrides map exact paths to one of the four document types. A legacy title that differs from its existing body heading becomes an alias; prose stays unchanged. Existing complete cursors gain explicit represented topic/source paths while preserving their coverage fields.

After reviewing the plan, run `migrate PLAN --approved-sha256 PLAN_FILE_HASH`. It establishes the original-file baseline, then uses the same recoverable publication flow for a separate format migration commit. It preserves existing creation/update/acquisition dates and source contributions; no verification dates are invented. The migration extends existing reader rules and retains old backups. Unknown legacy dates stop migration instead of being filled with today. Unsupported legacy YAML stops with an actionable error; manually transcribe the supported metadata in a reviewed plan rather than guessing its meaning.

If interrupted during migration, recover the named transaction when present, then rerun the exact approved plan. The global migration marker blocks ordinary library access until completion. Existing external changes stop migration as they stop ordinary publication.

## Tracking scope

Formal history allows `topics/**/*.md`, `sources/**/*.md`, `index.md`, `CHANGELOG.md`, `AGENTS.md`, `.gitignore`, `.state/library.json`, exact `.state/cursors/*.json` and generated `.state/published/*.json`. Candidates use the same content allowlist on temporary branches. The helper stages exact paths, independently of ignore rules.

`.worktree/` directories themselves, `drafts/`, raw extraction, SQLite indexes, locks, transaction journals and duplicate backups stay out of commits and normal retrieval. Keep cursor receipts and source/review excerpts minimal; no raw message arrays. All material remains beneath the selected root, and all access remains subject to its local reader instructions.
