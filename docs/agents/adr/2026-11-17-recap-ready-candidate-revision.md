# Revise unapproved recap candidates within their operation

Status: implemented

## Problem

Candidate inspection is a decision point, but an ordinary `ready` candidate has no supported correction path. Packet generation requires `editing`, while resolution requires conflict or reviewer rejection. [Issue #39](https://github.com/mel0nyrame/skills/issues/39) records a known citation defect published before a separate correction operation. A failed author check must instead keep defective knowledge unpublished.

## Decision

Under the user's authorization to fix issue #39 items 1 and 4, select an explicit `revise OP FILE` command for an ordinary `ready` candidate with no review history, independent-review requirement or recorded user approval. Share resolution's bounded replacement validation, but preserve the operation base, authored paths and review history. Rebuild catalogs, recompute reserved reasons and the candidate fingerprint, and bind packet identity to the revised input. Old packet bytes and candidate hashes must not publish the revised candidate. Return the canonical packet string as `packet_json`, whose exact UTF-8 bytes reproduce the revised packet hash and can be saved for `inspect` replay or `apply`. Keep one packet identity rather than introducing a parallel revision ledger; the original packet is invalidated, not all packet-based publication.

Keep reserved-change user approval separate from independent merge review. Revising an introduction can require user approval without requiring another agent. Candidates with recorded approval or reviews are outside this author-only revision path; conflict and reviewer-rejection resolution retain their existing rules and two-round limit. The [operations contract](../../../skills/knowledge/recap/references/operations.md) owns command details.

Same-topic review found no existing owner for author-only candidate revision. The [guide decision](0005--recap-guide-maintenance.md) continues to require exact-candidate approval and bounded introduction input. The [cursor decision](0008--recap-published-cursor-paths.md) continues to normalize before hashing. Neither is superseded.

## Alternatives

- Open `resolve` to every ready candidate: its unconditional independent-review transition would force another agent for ordinary author corrections, or require silently changing resolution semantics.
- Replace a ready candidate through `inspect`: combines initial preparation with revision and makes packet replay semantics less explicit.
- Publish then correct: puts known defects into formal history. Retaining the candidate and pausing is the safe fallback, not publication.
- Restart under another operation ID: abandons the original candidate and can obscure review bounds; unnecessary for a correction within the same authored scope.

## Consequences and risks

The author can correct inspected prose without publishing it first. This adds a command and an approval boundary: approved or reviewed candidates cannot use the author-only path. It does not provide general cancellation, approval withdrawal or arbitrary scope expansion.

The implementation shares replacement validation with resolution and exposes revision through the CLI. Validate proposed cursor relationships before writing in both paths, so this class of rejected input leaves the candidate clean and retryable. This preflight is not a general transactional rollback guarantee for later I/O failures. State-specific diagnostics distinguish author revision, conflict resolution, independent review and user intervention; a review's `revise` verdict remains distinct from the author command. Disposable-library regression tests cover same-operation revision and publication, stale hash and packet rejection, approval/review guards, reserved reasons, dirty-worktree preservation, conflict resolution and retained review rounds. The Windows repository check passed regression, ADR and documentation validation. These checks do not establish semantic accuracy of authored knowledge or model adherence to the revised instructions; no isolated model-behavior run was performed.

UTF-8 checklist and packet-decode diagnostic fixes are local usability changes, not a separate decision topic. The existing binary-output round-trip test verifies UTF-8 packet generation and inspection with Python UTF-8 mode disabled; it does not establish every shell's redirection behavior. No OpenChamber adapter or citation-checking feature is selected for this change.
