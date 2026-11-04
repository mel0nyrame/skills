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

Capture cursors are exact `.state/cursors/NAME.json` files containing a complete `recap-session-receipt/v1`: host, session ID, captured_at, source locator/prefix SHA-256, ordered integer range, and status complete, without unresolved gaps or raw message arrays. Add `represented_by` with nonempty `topics` and `sources` arrays naming related paths authored in this same publication; source session identity must match. They represent only successfully accounted material, not a later unrelated bookkeeping commit. Receipts are caller declarations and do not substitute for inspecting the source.

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
    }
  ]
}
```

Run `packet OP --from-dir DIR`. Save stdout to a separate packet file, then inspect it. The operation must still be `editing`; prepared candidates use `resolve` instead. Optional manifest `risk` is `routine` or `reserved`. Reasons/evidence are required declarations, not generated filler. Paths are explicit; unlisted files are never added and symlinks/traversal are rejected.

- A topic input is Markdown with JSON frontmatter containing the structured `document` fields except `body`; the Markdown body supplies `body`. A full existing `recap-topic/v2` document is also accepted; helper-owned `schema`, `created` and `updated` are removed from the packet input. Other metadata, including aliases and verification scope, is retained. New topic dates still come from the helper at inspection.
- A source or capture cursor contains its complete `content`. The author supplies honest coverage and represented paths. Generation cannot certify source inspection or invent acceptance.
- `index.md` contains only the [guide introduction](#guide-introduction).

The generator computes `expected_sha256` from the operation's frozen base even if the formal library has advanced. It checks item formats but does not create/modify candidate files, validate cross-file links as a batch, or publish. `inspect` owns whole-candidate validation. The generator uses the library lock, which may create a lock file.
