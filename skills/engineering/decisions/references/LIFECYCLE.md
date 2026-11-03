# Decision lifecycle branches

Project lifecycle rules take precedence. Read default states only when the project lacks a convention; read the retirement protocol before archive or deletion.

## Default states

When no state convention exists and the default structure is used, choose one value:

- **implemented:** delivered and still guides future changes. Keep references accurate as facts change, preserving the original decision.
- **proposed:** genuinely under consideration. After implementation, change it to `implemented` and describe delivered reality rather than a remaining plan.
- **rejected:** retain only while the wrong approach remains tempting and the record prevents repeated debate. Deletion is allowed when the record is stale, misleading, replaced, or no longer preventive.
- **superseded:** fully replaced, with an explicit replacement-record link. A partly replaced record keeps its still-valid state and identifies the replaced scope.
- **archived:** a frozen historical snapshot. Preserve its wording, facts, and outbound links. It cannot establish current behavior.

Completion and age do not automatically justify archive. Consider archive when only one-time implementation details, a closed local fix, or low-value history already obvious from current owners remain. When uncertain, preserve the record and state the judgment boundary. Avoid age, length, or count quotas.

## Archive or delete

Follow the repository's complete protocol. Handle language variants, metadata, manifests, signatures, and hashes together. Before moving or deleting:

1. Enumerate unique propositions and confirm an owner for everything that needs preserving.
2. Search filenames, titles, symbols, configuration keys, and links to identify dependents.
3. Repair inbound links from active content so the old path no longer acts as current authority.
4. Use recoverable, reviewable changes permitted by the repository.

An archive operation changes only the state, location, and mechanical metadata permitted by repository protocol. After archive, the body remains permanently frozen.

Completion requires preserved unique reasons, repaired active dependents, and passing project lifecycle/link checks. Report changes, gaps, and actions outside authorization through the skill's validation and reporting step.
