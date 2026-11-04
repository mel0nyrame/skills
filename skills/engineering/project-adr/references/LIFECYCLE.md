# Decision lifecycle branches

Project lifecycle rules take precedence. Read default states only when the project lacks a convention; read the retirement protocol before archive or deletion.

## Default states

When no state convention exists and the default structure is used, choose one value:

- **proposed:** still evaluating the choice. Record meaningful constraints, recommendations, pending candidates, and open questions without implying acceptance.
- **accepted:** explicitly selected, with implementation incomplete or not started. State who selected it and the basis: user confirmation or an agent's choice within existing task authorization. A recommendation alone remains `proposed`. Acceptance does not grant execution permission.
- **implemented:** implementation is complete, supported by code, configuration, tests, or other applicable evidence, and the choice still guides future changes. Describe delivered reality and keep references accurate as facts change, preserving the original decision.
- **rejected:** retain only while the wrong approach remains tempting and the record prevents repeated debate. Deletion is allowed when the record is stale, misleading, replaced, or no longer preventive.
- **superseded:** fully replaced, with an explicit replacement-record link. A partly replaced record keeps its still-valid state and identifies the replaced scope.
- **archived:** a frozen historical snapshot. Preserve its wording, facts, and outbound links. It cannot establish current behavior.

A topic's status describes its current choice, not every candidate within it. Rejected candidates may remain in the alternatives of a `proposed`, `accepted`, or `implemented` topic. Use `rejected` for a declined proposal or an independently valuable rejected choice.

Move `proposed` to `accepted` when an authorized choice is made, and to `implemented` only after checking implementation evidence. If the choice is already implemented when first recorded, start at `implemented`; intermediate files are unnecessary. Partial implementation remains `accepted`, with completed scope and remaining work stated. Record reconsideration when changed conditions reopen a choice. Lifecycle labels record facts rather than authorize further actions.

Completion and age do not automatically justify archive. Consider archive when only one-time implementation details, a closed local fix, or low-value history already obvious from current owners remain. When uncertain, preserve the record and state the judgment boundary. Avoid age, length, or count quotas.

## Archive or delete

Follow the repository's complete protocol. Handle language variants, metadata, manifests, signatures, and hashes together. Before moving or deleting:

1. Enumerate unique propositions and confirm an owner for everything that needs preserving.
2. Search filenames, titles, symbols, configuration keys, and links to identify dependents.
3. Repair inbound links from active content so the old path no longer acts as current authority.
4. Use recoverable, reviewable changes permitted by the repository.

An archive operation changes only the state, location, and mechanical metadata permitted by repository protocol. After archive, the body remains permanently frozen.

Completion requires preserved unique reasons, repaired active dependents, and passing project lifecycle/link checks. Report changes, gaps, and actions outside authorization through the skill's validation and reporting step.
