# Routine publication checklist

Use `python3 "$SKILL_DIR/scripts/knowledge.py" --root "$ROOT" COMMAND`. Global options precede the command. Resolve these paths from the selected skill and library. Read the root's reader rules, then run `doctor` once to check capabilities. A new capture starts with `begin`; query `status OP` when its state is needed. Use the [inventory](operations.md#locate-retained-operations) when locating retained work or recovery journals.

| Order | Command | Completion criterion |
| --- | --- | --- |
| 1 | `begin OP --writer-id ID` | One operation-owned candidate and frozen base exist. |
| 2 | `packet OP --from-dir INPUT` | Formal root and matching editing candidate are clean. JSON contains base hashes and the author's explicit reasons/evidence. Save stdout outside formal paths. |
| 3 | `inspect PACKET` | Candidate validates; inspect its diff, source coverage and returned `approval_sha256`. |
| 4 | `integrate OP` | Candidate includes newer formal changes. If conflicts or review are required, follow [operations](operations.md#independent-review). |
| 5 | `publish OP --approved-sha256 HASH` | Use the latest candidate hash. Reserved changes also need the user's exact approval through `approve OP FILE`. |
| 6 | `cleanup OP` | Re-read saved knowledge and test retrieval first. Clean only this successfully published operation. |

Inspect substantive prose with the [standalone reading check](knowledge.md#built-in-writing-contract). Use the contract for the current step:

| Step or condition | Read |
| --- | --- |
| Recover a local source | [Extraction](sessions.md#helper-extraction), then [chunk display](sessions.md#read-extracted-chunks) |
| Resume a previous capture | [Continuity and gaps](sessions.md#completeness-and-incrementality) |
| Recover compressor-held originals | [Context-management tools](sessions.md#context-management-tools) |
| Write a topic | [Topic fields](formats.md#topic-input) and [body types](formats.md#body-templates) |
| Write a source or cursor | [Source record](formats.md#source-record) and [change packet](formats.md#change-packet) |
| Prepare `packet` inputs | [Input directory](formats.md#packet-input-directory) |
| Review the candidate or publish | [Approval and publication](operations.md#prepare-and-publish) |
| Integrate concurrent same-file edits | [Independent review](operations.md#independent-review) |
| Resume interrupted publication | [Recovery](operations.md#publication-and-interrupted-recovery) |

Group independent reads of these selected sections, the extraction receipt and current topic summaries in one host tool request. Keep source inspection, candidate review and publication as decision points. After a context summary, reopen only material whose required details were lost. Small sources use the same coverage, evidence and publication checks; their size does not determine merge complexity.

Common corrections:

- Read a topic with `--purpose topic`, including before editing it.
- Check `complete` and per-entry errors in `status --all`; directory presence does not prove candidate validity.
- Updates use hashes from the operation base, not whichever revision is currently published. `packet` computes them.
- Topics use `document`; sources and capture cursors use `content`.
- Guide input is only the introduction before the managed topic catalog. It requires user approval.
- Preserve listed ignored files outside the candidate before retrying; never automatically prune them.
- Never change a partial receipt to complete by clearing its gaps. Re-extract with the supported adapter or disclose unresolved coverage.
