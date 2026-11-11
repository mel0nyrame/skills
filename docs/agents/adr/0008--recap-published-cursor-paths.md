# Normalize local paths before reviewing published recap cursors

Status: implemented

## Problem

An extraction receipt records the local source path and, for incremental capture, the previous receipt path. Copying that receipt into a published cursor commits machine-specific paths even when the corresponding source record has been sanitized. Rejecting the normal extraction output would leave callers to discover and repair this mismatch manually.

## Decision

Keep original extraction receipts local and unchanged. Normalize a copy when generating a packet and when rendering cursor candidate input, before candidate hashing, inspection or review. Replace `source.locator` with a fixed non-path marker and omit `incremental.prior_receipt`. Preserve all other metadata, including identities, ranges, prefix hashes, warnings and extension fields. Continue rejecting incomplete receipts and unresolved coverage gaps.

Require this published form for cursors authored by the current operation. Do not rewrite unrelated historical cursors. Apply the same transformation in reviewed migration plans; migration may change only these path fields and the existing represented-path declarations, not coverage judgments. The [format contract](../../../skills/knowledge/recap/references/formats.md#capture-cursor) owns the precise published representation.

Incremental continuity remains based on host, session identity, range and prefix hash, not these local paths. Keep both old and normalized receipts usable as checkpoints. Validate and normalize before review; publication must reject an unsafe candidate instead of silently changing approved bytes.

## Alternatives

- Reject absolute paths without normalization: breaks copying ordinary extraction receipts and requires platform-specific path recognition.
- Keep a basename or host-relative suffix: can still disclose private names and is not needed for continuity checks.
- Rebuild receipts from an allowlist: risks dropping warnings, coverage details or future metadata.
- Redact arbitrary strings recursively: can corrupt evidence and coverage data, and cannot guarantee secret removal.
- Rewrite historical commits: requires separate authorization and is outside a forward publication fix.

## Consequences and risks

Published cursors no longer locate the original source on disk. The caller must supply the selected source for incremental extraction. This is a targeted transformation of two known path fields, not general secret scanning. Authors still review other metadata, excerpts and evidence locators. Old Git commits and retained local artifacts can still contain original paths.

Implementation covers generated and direct packets, shared resolution rendering, publication validation, migration, and old/normalized incremental checkpoints. Regression tests preserve gap rejection, duplicate-key rejection and exact metadata other than the two path fields. The local suite passed 114 tests; ADR and documentation checks also passed. These checks do not establish semantic correctness of knowledge, model adherence to the instructions, or automatic privacy of arbitrary caller metadata. Windows execution remains a CI check rather than a local result.
