---
name: project-prose
description: Use when writing, editing, or reviewing technical documents, code comments/JSDoc, decision records, agent instructions, prompts, or diagnostics. Verify current facts, explanation ownership, and complete contracts. Remove reliance on private conversation, review, or draft context.
---

# Project Prose

Ground technical prose in the project's current state. Preserve the facts, obligations, constraints, and sources maintainers need. Remove private author workflows, reasoning transcripts, and stale conversational framing. Apply semantic review rather than keyword-based deletion.

## The HEAD-only test

For each questionable passage, ask:

> Can a reader with only the current repository resolve every reference and verify every claim?

If not, restate the facts that remain true from the current project state and remove inaccessible context. Even a resolvable reference may be unsuitable for current-state documentation when it describes the editing process instead of a system guarantee.

## Detect context leakage

Check each category and judge its meaning:

1. **Unstable internal references:** temporary decision numbers, audit codes, draft sections, phase labels, or private design ledgers. Replace them with committed authoritative sources. Remove a reference when the fact stands independently.
2. **Review and commit-stack framing:** “this PR,” “the previous commit,” “a later change,” “the reviewer confirmed,” or draft rounds. Describe the current mechanism, current limitation, or a real issue that owns follow-up work.
3. **Change narratives and stale version language:** “previously,” “no longer,” “legacy,” “this change,” or “now” used to narrate history. State current behavior. When necessary, use a present-tense counterfactual to explain what a constraint protects.
4. **Arguments addressed to an imagined reviewer:** explanations defending a conversion, branch, or implementation. State the constraints, type guarantees, ownership rules, or safety reasons that make it valid. Remove explanations already obvious from the code.
5. **Control-flow and derivation transcripts:** step-by-step restatements of obvious branches, test execution, or code proofs. Keep non-obvious contracts, ordering, races, and failure semantics.
6. **Vague qualifiers and unowned plans:** “maybe,” “should be enough,” “for now,” or work without a marker and owner. Replace them with measurement boundaries, explicit limitations, or a real TODO/issue. Remove unsupported claims.
7. **Writing residue:** language inconsistent with surrounding documents, private separators, or draft markers. Preserve technical tokens and translate or remove the remaining residue.

## Preserve useful context

History and alternatives are not automatically leakage. Keep stable, resolvable references with maintenance value, including:

- Real issues, owners, and follow-up work.
- External standards, specifications, and stable design documents.
- Merged changes or incidents cited in evidence-based documents.
- Reasons required by tools for suppressions, coverage exclusions, or empty error handling.
- Measurement boundaries and their evidence.
- Runtime lifecycle states.
- Alternatives and rejection reasons that prevent repeated debate.

Judge whether a reference helps future maintainers verify or safely change the system, rather than whether its wording refers to the past.

## Preserve complete propositions

Before editing, separate a passage into factual clauses. Preserve every clause expressing:

- Preconditions and postconditions.
- Invariants and compatibility promises.
- Ownership and lifecycle responsibility.
- Timing, cancellation, ordering, and races.
- Security and trust assumptions.
- Failure and recovery behavior.
- Persistence, wire protocols, or user-visible semantics.
- Evidence that calibrates a limitation.

Rewrite with direct present-tense statements, explicit actors, and one main action per sentence. Preserve the strength of obligations, keep assumptions distinct from implemented behavior, and retain sources that make limitations credible.

## Give each explanation one owner

Classify the information, then edit its owning source:

- **Current behavior and implementation details:** code, configuration, tests, and current-state documentation.
- **Consumer contracts:** the README, API documentation, JSDoc, or diagnostic surface consumers actually read.
- **Lasting rationale, tradeoffs, constraints, and rejected alternatives:** the active durable decision record.
- **Incidents and historical narratives:** a postmortem or the project's designated history document.

Elsewhere, repeat only the contract consumers need locally and link to its owner. A README may state a current constraint and link to its decision without copying the full rationale. A decision should leave current directories, data dictionaries, and operating procedures to engineering documentation.

## Edit the owner first

Edit the owning source before generated or derived artifacts. Trace generated directories, copied API descriptions, language variants, snapshots, and rendered pages to their owners. Regenerate through the project's supported process. For example, edit source JSDoc before generating a catalog, edit the schema before generating types, and update canonical documentation before its website projection. Place comments near the code they explain. Put lasting design reasons in an active durable decision.

When `ENGINEERING.md`, `DATA.md`, ADRs, or other architecture documents already own an explanation, update and link that owner first. Keep only the necessary summary and stable links in READMEs, comments, other skills, and PR/MR text. Avoid copying file structures, APIs, or field lists that code already expresses directly. Document reasons, boundaries, ownership, prohibited actions, maintenance entry points, and lasting constraints that code cannot express well.

Respect task scope and exclusions. Modify vendor code, frozen archives, recorded fixtures, and snapshots only when an owning-source change requires regeneration.

## Separate current state from history

READMEs, ordinary docs, JSDoc, and comments describe the current system by default. Durable decisions, postmortems, or dedicated history documents own past design reasons, rejected alternatives, migration narratives, and incidents. Keep brief history in current-state prose only when consumers need it to understand the current contract, and link its owner.

An active durable decision owns rationale, tradeoffs, and lasting constraints; it is not the general authority for current behavior. Support current behavior with code, configuration, tests, and current-state documentation. Archived decisions explain history, cannot establish current behavior, and keep their bodies frozen.

## Verify semantics

After editing:

1. Read the complete updated document without comparing it to the old passage.
2. Search for related leakage patterns and manually review near matches.
3. Confirm every retained reference resolves from the current repository or a declared external source.
4. Run the documentation, generation, translation, lint, and behavior checks that own the affected surface.
5. Review the diff for lost obligations, invented behavior, duplicated reasons, or unsupported claims.

Report the review scope, explicit deletions or rewrites, context deliberately retained, deferred items, and checks actually run. A keyword search with no matches cannot alone establish accuracy or completeness.
