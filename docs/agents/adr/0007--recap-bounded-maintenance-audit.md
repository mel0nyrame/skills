# Keep recap maintenance audits bounded and report-only

Status: implemented

## Problem

Recap can publish corrections and maintain reading routes, but its maintenance entry point does not describe how to discover content problems without preparing changes. Agent-memory designs suggest broader consolidation, query logging and injected-context budgets. Applying these mechanisms directly would conflate recap's explicitly requested, sourced explanations with an automatically managed memory store.

## Decision

Add an explicitly requested, scoped, report-only agent workflow. The [audit contract](../../../skills/knowledge/recap/references/operations.md#bounded-maintenance-audit) owns scope selection, evidence checks, navigation checks, access limits and report completion. Formal repairs remain separate authorized candidates. Ordinary helper locks/caches are permitted only under their existing access contract; report-only does not promise zero filesystem writes.

Keep the implementation at the instruction layer. No new CLI, schema, persistent notes layer or automatic query log is needed to try this workflow. Topic development judges future reading value without requiring a separate plan artifact; useful single-source explanations remain valid. Recurring corrections retain causal reasoning and applicability rather than a mandatory field template.

The [retrieval baseline](../../../skills/knowledge/recap/references/search.md#retrieval-baseline) uses selected questions and expected topics, distinguishes first-query hits from retries, and reports search mode and revision. It is an optional diagnostic, not a publication gate. Representative real-library results are still missing; the next investigation is to run it on a user-selected library and question set before changing retrieval scope or ranking.

Same-topic review: [ADR 0004](0004--recap-lexical-search-contract.md) continues to own lexical matching and topics-only retrieval; this workflow supplies an evaluation method without replacing that choice. [ADR 0005](0005--recap-guide-maintenance.md) continues to own guide candidate authoring and approval. This record owns discovery/reporting, not guide publication, and supersedes neither record.

## Alternatives

- Automatically repairing or publishing audit findings would bypass the existing separation between inspection, authorization and publication. Keep findings as a report until repair is requested.
- A whole-library scan on every maintenance request increases cost and exposes unrelated material. Select a bounded scope and disclose unchecked items instead.
- A persistent notes layer, source search and source-only successful cursors would change storage, privacy and coverage invariants without demonstrated need. Defer those designs rather than introduce them through audit.
- A fixed 200-line/25-KB guide budget copies an injected-memory limit from another product. Recap's guide is read on demand; size alone does not establish a defect.
- Default query logging would retain potentially private questions. Use explicitly selected evaluation questions without automatic persistence.
- Rejecting every topic answerable from one source would discard useful explanations. Judge reading value, not source count.

## Consequences and risks

The skill and paired usage guides now expose bounded audit and manual retrieval evaluation without runtime or library migration changes. Audit quality still depends on the agent, available evidence and an honest statement of scope; structural validity cannot establish truth. Reports can miss issues outside their selected material. Hit@1/hit@3 measure whether any expected topic appears, not full-answer recall or factual accuracy.

[Manual scenarios](../../../tests/scenarios/recap.md) define behavioral checks; they have not been run with fresh agents. Existing executable regression tests do not validate adherence to these new instructions. Reconsider automation only after bounded audits or representative evaluations reveal recurring work that justifies it.
