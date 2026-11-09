# Document and packet contracts

The helper validates structure; agents establish support, coverage and meaning. There is no automatic truth score. Runtime validation uses the standard library. Canonical frontmatter is a JSON object between `---` lines: a deliberately strict subset of YAML, without YAML tags, aliases or arbitrary indentation. Supply structured input rather than hand-formatting topic headers. The helper emits the header.

## Topic input

A packet contains a `document` object with these required fields:

| Field | Contract |
|---|---|
| `title` | Nonempty single-line title, matching the body's `#` title |
| `type` | `concept`, `procedure`, `research` or `decision` |
| `acquired` | Actual acquisition date, `YYYY-MM-DD`; existing acquisition is preserved |
| `sources` | Nonempty array of topic-relative source paths; each also has an exact body link |
| `summary` | Single-line plain-text reading purpose and necessary case scope, consistent with the body |
| `body` | Nonempty Markdown explanation with a matching level-one title |

Optional fields are `aliases` (unique string array), `status` (`formal` or `archived`; draft files use `draft`), `event_date`, `as_of`, `version`, and `verified`. Verification is an object with `date`, `scope` and a nonempty `evidence` array. A timestamp records only the stated scope; it is not a whole-document truth label. Existing optional applicability/verification fields are preserved when omitted, and alias defaults are preserved. Keep supporting sources and prior acquisition contributions when extending a topic.

Stored headers additionally contain `schema: recap-topic/v2`, `created` and `updated`. The helper preserves creation/acquisition and sets the edit date; a format-only migration preserves all original dates. Status controls document lifecycle, not factual certainty. Archived topics leave the default index. Partial capture drafts stay under `drafts/`, outside publication; preserve them without a formal publish/cursor update until the user accepts the gap or it is repaired.

## Body links

Local body links must be relative to their owning document, use forward slashes and remain inside the knowledge root. Absolute local paths (including Windows drive paths and `file:` URLs), backslashes and root-escaping `..` are rejected. Link fragments are allowed; the helper checks the target file, not its heading anchor. Topic links may target only topics, sources or `index.md`, not management material. External link schemes are limited to `http`, `https` and `mailto`. A path needed as an operational example can appear as code rather than as a clickable local link.

## Body templates

Select a type from the reader's question. These specify information to cover, not mandatory literal headings:

| Type | Information the reader needs |
|---|---|
| `concept` | Question, mechanism/relationships, useful example, applicability and limitations, evidence |
| `procedure` | Target/environment and starting state, affected paths, ordered actions, visible results, failure/recovery boundaries, evidence |
| `research` | Question and scope, findings and primary evidence, competing explanations, remaining gaps |
| `decision` | Problem/conditions, chosen option and reasons, real alternatives, consequences and reconsideration triggers |

Apply the [built-in writing contract and standalone reading check](knowledge.md#built-in-writing-contract). These templates specify information, not fixed headings or point counts. The helper checks nonempty bodies, titles and merge markers; it does not establish readability, evidence accessibility or factual correctness.

## Source record

Use `sources/<host>-<exact-session-id>.md`. The canonical header has:

```json
{
  "schema": "recap-source/v2",
  "host": "export",
  "session_id": "exact-id",
  "acquired": "2026-10-28",
  "locator": "host-relative original locator",
  "cutoff": "message 12",
  "coverage": {
    "status": "complete",
    "scope": "user-visible messages on the selected branch",
    "inspected": ["messages 1-12"],
    "gaps": []
  }
}
```

These are illustrative values, not defaults. Coverage status is `complete`, `partial` or `accepted-partial`, relative to an explicit `scope`; complete sources have no gaps within that scope. Record unread attachments/tools and their effect on claims in the body; a message-only scope does not verify them. Accepted partial sources require `coverage.acceptance`, locating the user's informed acceptance; acceptance does not verify facts. Plain `partial` cannot support formal topics. Source bodies explain ranges/chunks/counts, branch, exact claim/test locators and necessary excerpts; keep identity, cutoff and ranges consistent with the header/checkpoint and preserve earlier contributions. Migration may retain metadata in `legacy` without treating old labels as verification.

Remove unrelated identities, secrets, private paths and raw chat residue. Prefix hashes and locators aid matching, not full replay. After the original is deleted, only retained excerpts remain independently inspectable.

## Change packet

```json
{
  "id": "capture-example",
  "writer_id": "actual host agent identity",
  "changes": [
    {
      "path": "topics/Example.md",
      "expected_sha256": null,
      "kind": "add",
      "reason": "Explain the mechanism and its limits",
      "evidence": ["exact inspected source locator"],
      "document": {
        "title": "Example",
        "type": "concept",
        "acquired": "2026-10-28",
        "sources": ["../sources/export-exact-id.md"],
        "summary": "What this explanation helps the reader understand",
        "body": "# Example\n\nA supported explanation with conditions.\n\n[Source](../sources/export-exact-id.md)\n"
      }
    }
  ]
}
```

This illustrates one item, not a complete first capture: the referenced source must exist in the candidate or be supplied in the same packet. For sources and capture cursors, use `content` instead of `document`. Each item has the same `path`, `expected_sha256`, `kind`, `reason`, `evidence` envelope. Reasons/evidence are nonempty single-line values. Kinds are `add`, `update`, `correct`, `archive`. `null` expects a new path; updates require the hash from the operation's base. No delete operation is provided. Metadata, source and local-link checks run before formal publication.

### Capture cursor

Capture cursors are exact `.state/cursors/NAME.json` files containing a complete `recap-session-receipt/v1`: host, session ID, captured_at, source locator/prefix SHA-256, ordered integer range, and status complete, without unresolved gaps or raw message arrays. Add `represented_by` with nonempty `topics` and `sources` arrays naming related paths authored in this same publication; source session identity must match. They represent only successfully accounted material, not a later unrelated bookkeeping commit. Receipts are caller declarations and do not substitute for inspecting the source.

- Every represented topic must cite at least one represented source; every represented source must be cited by a represented topic.
- At least one represented source must match the cursor's host and exact session ID. Keep all declared identities, cutoffs and ranges consistent with the inspected material.
- Range bounds are integers: `after >= -1`, `through >= 0`, and `through >= after`. Prefix hashes are 64 lowercase hexadecimal characters.

A minimal illustrative cursor for `.state/cursors/exact-id.json` is:

```json
{
  "schema": "recap-session-receipt/v1",
  "host": "export",
  "session_id": "exact-id",
  "captured_at": "2026-10-28T00:00:00Z",
  "status": "complete",
  "source": {"locator": "host-relative original locator", "prefix_sha256": "0000000000000000000000000000000000000000000000000000000000000000"},
  "range": {"after": -1, "through": 12},
  "represented_by": {"topics": ["topics/Example.md"], "sources": ["sources/export-exact-id.md"]}
}
```

Replace the illustrative identity, timestamp, locator, hash and range with the inspected extraction receipt. Preserve its gaps/warnings rather than inventing completeness. Copy a complete receipt into the input directory and add its represented paths only after those source intervals have been accounted for.

### Risk and resolution

Optional packet `risk: reserved` requests explicit user preview/approval; routine is the default. Mechanical checks do not discover every judgment-changing edit, so the writer must classify those correctly.

A resolution file has `{"changes": [...]}` with the same item envelope, hashes from the operation's new integration base, and replacements for every reported conflict. It may alter only that operation's authored paths. The helper rebuilds shared entries and invalidates old review approval. Inspect the returned candidate hash after each integration/resolution.

### Guide introduction

An `index.md` change uses `kind: update` or `correct`, its full file hash from the operation base, and `document: {"body": "# Reading route\n\nChoose a relevant topic below.\n"}`. The body replaces only the introduction before `<!-- recap:topics:start -->`; do not include helper markers or the generated catalog. The helper preserves trailing prose and regenerates the catalog from current topics. In a guide without markers, the existing text is the introduction. A guide update always needs explicit user approval of the candidate hash. Reader/publisher rules remain outside packet authoring.

### Packet input directory

After `begin OP --writer-id ID`, prepare a separate input directory containing `changes.json` and only the intended files at their root-relative paths. The manifest contains author-supplied declarations:

```json
{
  "changes": [
    {
      "path": "topics/Example.md",
      "kind": "add",
      "reason": "Explain the mechanism and its limits",
      "evidence": ["exact inspected source locator"]
    },
    {
      "path": "sources/export-exact-id.md",
      "kind": "add",
      "reason": "Preserve inspected evidence",
      "evidence": ["exact inspected source locator"]
    },
    {
      "path": ".state/cursors/exact-id.json",
      "kind": "add",
      "reason": "Record the represented capture range",
      "evidence": ["inspected extraction receipt"]
    }
  ]
}
```

This first-capture example declares a topic, its source and its successful cursor together. Omit the cursor only when not claiming a saved incremental checkpoint. Repeated capture updates existing paths instead of reusing these `add` declarations.

Run `packet OP --from-dir DIR`. Save stdout to a separate packet file, then inspect it. The operation must still be `editing`; prepared candidates use `resolve` instead. Optional manifest `risk` is `routine` or `reserved`. Reasons/evidence are required declarations, not generated filler. Paths are explicit; unlisted files are never added and symlinks/traversal are rejected.

- A topic input follows [topic fields](#topic-input), [body templates](#body-templates) and [body links](#body-links). It is Markdown with JSON frontmatter containing the structured `document` fields except `body`; the Markdown body supplies `body`. A full existing `recap-topic/v2` document is also accepted; helper-owned `schema`, `created` and `updated` are removed from the packet input. Other metadata, including aliases and verification scope, is retained. New topic dates still come from the helper at inspection.
- A source contains its complete [source record](#source-record): JSON frontmatter including `schema: recap-source/v2`, then a nonempty Markdown body with a level-one title, inspected ranges and evidence. A cursor contains complete JSON following [capture cursor](#capture-cursor), including `represented_by`. Generation cannot certify source inspection or invent acceptance.
- `index.md` contains only the [guide introduction](#guide-introduction).

For `topics/Example.md`, a minimal input file is:

```markdown
---
{
  "title": "Example",
  "type": "concept",
  "acquired": "2026-10-28",
  "sources": ["../sources/export-exact-id.md"],
  "summary": "What this explanation helps the reader understand"
}
---
# Example

A supported explanation with conditions.

[Source](../sources/export-exact-id.md)
```

These are format examples, not evidence or default acquisition dates. Supply the source header/body and cursor described above; writing only this topic file leaves a broken source link.

The generator checks preparation conditions under the library lock before reading declared documents: no unfinished publication, a clean formal root, an editing operation, and an existing clean candidate with matching repository/branch identity. It preserves external edits and fails without repairing or adopting them. A newer clean formal revision is permitted; `expected_sha256` still comes from the operation's frozen base.

Generation checks individual item formats without creating/modifying candidate files or publishing. `inspect` owns whole-candidate validation, including cross-file links and source/cursor relationships; publication retains its final checks. The lock may create a lock file.
