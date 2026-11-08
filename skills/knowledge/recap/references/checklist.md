# Routine publication checklist

Use `python3 "$SKILL_DIR/scripts/knowledge.py" --root "$ROOT" COMMAND`. Global options precede the command. Resolve these paths from the selected skill and library. Read the root's reader rules first. `doctor` checks capabilities and statically checks `workflow.py` for explicit UTF-8 reads and resolved Git path comparisons without initialization. `portability.ok: false` includes line-specific errors and exits 2; success is not an end-to-end library health guarantee. `status --all` locates retained operations without deleting them.

## First capture

Confirm required capabilities with `doctor`. Initialize only a new empty root with `init`, then read its generated `AGENTS.md`. Existing populated roots require [migration](operations.md#migrate-an-existing-library).

Complete when the library is initialized and its reader rules have been read.

## Publication commands

Start after source coverage and topic development are complete and writing guidance is selected. First and repeated captures use the same sequence. Set a unique `OP`, the actual writer `ID`, a separate `INPUT` directory and a `PACKET` file outside formal paths. The [input-directory example](formats.md#packet-input-directory) supplies the initial topic/source/cursor batch.

| Order | Command | Completion criterion |
| --- | --- | --- |
| 1 | `begin OP --writer-id ID` | One operation-owned candidate and frozen base exist. |
| 2 | `packet OP --from-dir INPUT` | Formal root and matching editing candidate are clean. JSON contains base hashes and the author's explicit reasons/evidence. Save stdout outside formal paths. |
| 3 | `inspect PACKET` | Candidate validates; inspect its diff, source coverage and returned `approval_sha256`. |
| 4 | `integrate OP` | Candidate includes newer formal changes. If conflicts or review are required, follow [operations](operations.md#independent-review). |
| 5 | `publish OP --approved-sha256 HASH` | Use the latest candidate hash. Reserved changes also need the user's exact approval through `approve OP FILE`. |
| 6 | `cleanup OP` | Re-read saved knowledge and test retrieval first. Clean only this successfully published operation. |

Inspect substantive prose with the [standalone reading check](knowledge.md#built-in-writing-contract). [Formats](formats.md#packet-input-directory) owns input fields; [operations](operations.md) owns approval, conflicts, recovery and migration. Do not repeatedly load entire references when only one error or field needs checking.

## Common corrections

If `inspect` fails after writing candidate material, retain that operation and inspect its status/diff before retrying. The candidate may be dirty even though nothing was published. Do not reset or clean the formal root to repair a candidate.

- Read a topic with `--purpose topic`, including before editing it.
- Check `complete` and per-entry errors in `status --all`; directory presence does not prove candidate validity.
- Updates use hashes from the operation base, not whichever revision is currently published. `packet` computes them.
- Topics use `document`; sources and capture cursors use `content`.
- Guide input is only the introduction before the managed topic catalog. It requires user approval.
- Preserve listed ignored files outside the candidate before retrying; never automatically prune them.
- Never change a partial receipt to complete by clearing its gaps. Re-extract with the supported adapter or disclose unresolved coverage.
