# Routine publication checklist

Use `python3 "$SKILL_DIR/scripts/knowledge.py" --root "$ROOT" COMMAND`. Global options precede the command. Resolve these paths from the selected skill and library. Read the root's reader rules first. `doctor` checks capabilities without initialization; `status --all` locates retained operations without deleting them.

| Order | Command | Completion criterion |
| --- | --- | --- |
| 1 | `begin OP --writer-id ID` | One operation-owned candidate and frozen base exist. |
| 2 | `packet OP --from-dir INPUT` | JSON contains base hashes and the author's explicit reasons/evidence. Save stdout outside formal paths. |
| 3 | `inspect PACKET` | Candidate validates; inspect its diff, source coverage and returned `approval_sha256`. |
| 4 | `integrate OP` | Candidate includes newer formal changes. If conflicts or review are required, follow [operations](operations.md#independent-review). |
| 5 | `publish OP --approved-sha256 HASH` | Use the latest candidate hash. Reserved changes also need the user's exact approval through `approve OP FILE`. |
| 6 | `cleanup OP` | Re-read saved knowledge and test retrieval first. Clean only this successfully published operation. |

Inspect substantive prose with the [standalone reading check](knowledge.md#built-in-writing-contract). [Formats](formats.md#packet-input-directory) owns input fields; [operations](operations.md) owns approval, conflicts, recovery and migration. Do not repeatedly load entire references when only one error or field needs checking.

Common corrections:

- Read a topic with `--purpose topic`, including before editing it.
- Updates use hashes from the operation base, not whichever revision is currently published. `packet` computes them.
- Topics use `document`; sources and capture cursors use `content`.
- Guide input is only the introduction before the managed topic catalog. It requires user approval.
- Preserve listed ignored files outside the candidate before retrying; never automatically prune them.
- Never change a partial receipt to complete by clearing its gaps. Re-extract with the supported adapter or disclose unresolved coverage.
