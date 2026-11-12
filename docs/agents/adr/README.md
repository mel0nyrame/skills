# Decision Records for This Collection

This directory owns this repository's decision-recording convention. It is not a record index. The bundled `project-adr` skill uses target-project conventions first; this directory does not prescribe paths for other projects.

## Capture and retrieval

Before proposing or implementing related work, search active records by task topic, capabilities, constraints, paths, and evaluated alternatives. Read matching proposals, choices, rejection reasons, and open questions. If conditions justify reconsideration, state what changed and which earlier reasons still hold.

Capture a meaningful constraint, real tradeoff, or unresolved proposal when it affects future work and forgetting its reasons could reopen the debate or repeat a mistake. Passing suggestions without evaluation and purely local mechanical edits need no record. Preserve meaningful progress during discussion and before pausing, including when implementation is deferred.

Reuse one owner per [decision topic](../../../GLOSSARY.md). Keep its evaluated candidates and outcomes together. A separate rejected record needs independent lasting value. Distinguish selected conclusions, recommendations, missing evidence, and the next open question or investigation. The record is a current synthesis, not a conversation transcript.

## Files and lifecycle

For new records, use `YYYY-MM-DD-kebab-title.md` in this directory, with the first creation date and a descriptive topic slug separated by one hyphen. Keep filenames stable through later edits, state changes, and merge. Dates may repeat; the complete filename identifies a record. Reuse existing same-topic owners and distinguish independent topics with more specific slugs when necessary. Existing numbered records keep their filenames and links; this change does not bulk-rename history. See the [naming decision](2026-11-12-date-based-adr-filenames.md) for rationale and scope. Follow the existing English format: a title, one `Status` field, then `Problem`, `Decision`, `Alternatives`, and `Consequences and risks`. A proposal may have pending candidates; record their actual outcomes without inventing rejection reasons. Put open questions under `Decision` and evidence or verification gaps under `Consequences and risks`.

Use the [default lifecycle](../../../skills/engineering/project-adr/references/LIFECYCLE.md#default-states): `proposed`, `accepted`, `implemented`, `rejected`, `superseded`, or `archived`. An `accepted` choice is selected by the user or by an agent within existing authorization; it is not yet fully implemented. Implementation needs evidence. Acceptance and pending plans do not themselves authorize execution.

Keep unique reasons when decisions change, cross-link full or partial replacements, and update facts when implementation moves. Follow the [retirement protocol](../../../skills/engineering/project-adr/references/LIFECYCLE.md#archive-or-delete) before archiving or deleting. The archive location is `archive/`; archived bodies remain frozen and cannot establish current behavior.

`project-adr` owns record criteria, content, and lifecycle. `project-engineering` reads records during investigation and triggers implementation synchronization. External discussion workflows follow this same directory contract rather than create a second system.

## Validation

From the repository root:

```sh
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
```

The checker validates structure, state values, and local link paths. Review the actual reasons, evidence, open questions, and replacement relationships separately. It does not prove that an implementation exists or that a later agent can resume the discussion.
