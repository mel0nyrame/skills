---
name: decisions
description: Use when adding or changing lasting engineering decisions, implementation changes affect existing ADRs, or reviewing, superseding, archiving, deleting records, or establishing project ADR maintenance. Synchronize active records with implementation, preserve lasting reasons and real alternatives, and check same-topic supersession.
---

# Durable Engineering Decisions

Maintain decision memory that prevents repeated mistakes or debates. The scope extends beyond architecture decision records (ADRs). Follow the target repository's formats, locations, lifecycle, and validation rules.

## Decide whether a record is useful

Follow explicit project creation criteria first. Without them, enter the durable-decision workflow when at least one condition holds. When implementation changes affect an active record, maintain its facts even if there is no new decision:

- A future maintainer could reasonably reopen the question.
- Code and current engineering documentation cannot adequately explain why the choice is necessary.
- Forgetting the reason could reintroduce a tempting wrong approach.

Check architecture boundaries, dependency direction, public protocols/APIs, the security model, critical dependencies, data sources of truth, ownership, flow, isolation, persistent schemas, derived data and rebuilds, retention/deletion, migration/backward compatibility, lasting testing strategy, important process/tooling policy, significant simplifications, key bug lessons, important rejected alternatives, and conditions for reconsideration.

Ordinary local bugs, styling, wording, and changes without these lasting constraints usually need no record. Category labels do not establish future value: not every feature, bug fix, or process change merits preservation.

When implementation work includes related record maintenance, add records, synchronize facts, and handle supersession in the same change as the code. Read-only reviews report gaps. Archive, deletion, and governance integration actions remain subject to the relevant task authorization.

## Locate rules and records

Read applicable repository and subtree instructions, contribution guides, documentation entry points, and decision configuration. Reuse existing directories, naming, metadata, and lifecycle. A directory name alone does not establish authority.

This skill maintains records independently of other domain-modeling, discussion, or ADR skills. When multiple skills participate, establish one project record convention and use it throughout. Installing another skill does not adopt its default template or creation threshold. Assign writers according to the actual task's division of work rather than a fixed skill name.

Use creation criteria, locations, formats, states, and check entry points specified by the current user request and applicable project rules. Without explicit rules, reuse stable, consistent conventions in comparable records. One outlier or mixed samples do not establish a new rule. Use the defaults below for unresolved parts.

Before writing, check existing same-topic records and uncommitted changes. Maintain an existing draft or delivered record that already owns the decision within task authorization. Preserve other work. Multiple skill triggers must not create duplicate records for one decision. Terminology documents own terms, engineering documents own current facts, and ADRs own reasons.

Without any repository conventions, use one Markdown file per decision in `docs/adr/`, named `NNNN--kebab-title.md`. Use the project's main language for record titles and prose. The default archive location is `docs/adr/archive/`.

Prefer discovery through directories, metadata, filenames, and search. Avoid adding a central index that every branch must update manually. Follow existing index policy. An index fully generated from authoritative metadata with a freshness check may remain.

Read [project integration](references/PROJECT-INTEGRATION.md) when the user requests ongoing maintenance or the first decision is being written in a project whose existing instruction entry point lacks maintenance rules. It owns standing triggers, directory contracts, and check integration. Installing a skill does not complete project integration.

## Check same-topic records before adding one

Before drafting, search active records for the same capabilities, mechanisms, constraints, and rejected alternatives. Classify them under “Maintain current facts and decisions.” Update the existing owner of the same decision. A new decision states what it replaces and which constraints remain valid. Maintain links in both directions within the change.

Complete this scope's supersession review for every new record. For fully replaced records needing consolidation, archive, or deletion, perform lifecycle maintenance within authorization. Otherwise, preserve the original file and state relationships and pending actions. Partial replacement preserves each record's unique reasons. Limit review to active same-topic records unless the task requests a full corpus audit.

## Write a complete decision

Use the target repository's template, explicit format rules, or stable conventions among comparable records. A short template may express choice and rationale in one paragraph. Follow project requirements for states and separate sections. Preserve the existing format during maintenance and add genuine tradeoffs needed to understand the choice. The default structure is not a reason to expand or rearrange another valid template.

Without a reusable format, or when old records are mixed and no explicit convention exists, use the default structure. New records need a title, one explicit state, and four sections in this order. Keep titles consistent with the project's main language. The English default is shown below; choose the state under “Choose a lifecycle.” The checker also accepts the complete Chinese schema for existing projects.

```markdown
# Decision title

Status: implemented

## Problem
## Decision
## Alternatives
## Consequences and risks
```

Each default section must meet its completion criterion. For a project template, check its required content and put necessary reasons and tradeoffs where that template permits:

- **Problem:** state the constraints or conflict requiring a choice and the applicable scope.
- **Decision:** state the choice or proposal, its reasons, and the assumptions and boundaries under which it holds.
- **Alternatives:** record every real candidate and why it lost, so future readers can see which plausible paths were evaluated. When history cannot be reliably recovered, mark it unknown or use the project's allowed missing-value notation. Preserve the evidence gap rather than inventing alternatives.
- **Consequences and risks:** state benefits, costs, and limits. Include relevant failure modes, validation evidence, known gaps, or conditions for reconsideration. Mark unverified content unknown.

Empty sections, a list containing only the chosen technology, or all four information types mixed into one paragraph do not satisfy the default structure. Add dates, owners, and other fields when the project requires them. For supersession, state its direction, scope, and record links near the state. Current engineering documents explain how the system works. Decisions explain why a choice was made and what was rejected. Link them without copying the full content.

Read-only reviews report format and content gaps. When authorized to maintain older records, prioritize affected active records, preserve unique reasons and genuine gaps, and avoid bulk historical rewrites solely for format consistency. Archive bodies remain frozen.

## Maintain current facts and decisions

Compare the record with current code, configuration, tests, engineering documents, active same-topic records, and inbound links. Distinguish:

- **Implementation facts change; the decision holds:** synchronize paths, packages, configuration keys, defaults, owners, or implementation locations so the record points to current implementation. Update facts directly rather than appending a changelog.
- **The decision changes:** create a new record with supersession and cross-links. Preserve what the old decision actually chose.
- **Partial replacement:** the old record still owns unique rationale, constraints, alternatives, compatibility promises, or reconsideration conditions. Keep both records and cross-link them.
- **Full replacement:** consolidate under repository rules only after the new owner preserves meaningful rationale, alternatives, consequences, required verification, coverage gaps, and reconsideration conditions, and inbound links are repaired.
- **Still valid:** nearby topics own different decisions and both remain active.

Code and configuration own current behavior. Tests own executable guarantees. Generated artifacts derive from upstream owners by default. Current-state documentation owns usage and engineering facts. Active decisions own reasons and tradeoffs.

## Choose a lifecycle

Follow existing project lifecycle rules or stable state conventions, including whether a state is mandatory, whether it lives in YAML or prose, and the vocabulary. Determine meaning from actual implementation and replacement links. A label such as `accepted` does not prove implementation. Preserve existing representation. If a project has no state field, verify the actual lifecycle and express required supersession relationships in its own format.

When no state convention exists and the default structure is used, choose one value:

- **implemented:** delivered and still guides future changes. Keep references accurate as facts change, preserving the original decision.
- **proposed:** genuinely under consideration. After implementation, change it to `implemented` and describe delivered reality rather than a remaining plan.
- **rejected:** retain only while the wrong approach remains tempting and the record prevents repeated debate. Deletion is allowed when the record is stale, misleading, replaced, or no longer preventive.
- **superseded:** fully replaced, with an explicit replacement-record link. A partly replaced record keeps its still-valid state and identifies the replaced scope.
- **archived:** a frozen historical snapshot. Preserve its wording, facts, and outbound links. It cannot establish current behavior.

Completion and age do not automatically justify archive. Consider archive when only one-time implementation details, a closed local fix, or low-value history already obvious from current owners remain. When uncertain, preserve the record and state the judgment boundary. Avoid age, length, or count quotas.

## Archive or delete safely

Follow the repository's complete protocol. Handle language variants, metadata, manifests, signatures, and hashes together. Before moving or deleting:

1. Enumerate unique propositions and confirm an owner for everything that needs preserving.
2. Search filenames, titles, symbols, configuration keys, and links to identify dependents.
3. Repair inbound links from active content so the old path no longer acts as current authority.
4. Use recoverable, reviewable changes permitted by the repository.

An archive operation changes only the state, location, and mechanical metadata permitted by repository protocol. After archive, the body remains permanently frozen.

## Validate and report

Before delivery, review each new or maintained active record. Confirm the selected project convention or default structure, accurate lifecycle facts, complete required content, clear replacement direction and scope, and resolvable links.

Run the repository's focused checks for format, required sections, path/lifecycle consistency, links, metadata, and archive integrity. Run other project checks according to risk. Report added or updated decisions, fact synchronization, full or partial replacement, retained or deleted rejected records, archives, and commands actually run with their results.

For the default English or Chinese structure without a matching project checker, run [the default checker](scripts/check_adr.py) on the affected files or ADR directory. Read project integration for check wiring. Use project-specific checks for short templates, custom states, or other structures. When none exist, review records individually and report scope. Preserve other valid templates rather than rewriting them to satisfy this checker.

Completion requires every affected active record to be synchronized in the same change, a same-topic review conclusion for every new record, authorized supersession and lifecycle work to be complete, and passing format, state, and local-link-path checks. Report missing historical evidence, actions outside authorization, and project-integration gaps honestly. A passing checker does not resolve them.

Mechanical checks establish structure, state values, and link consistency. Semantic judgment still establishes content completeness, real alternatives, and the future value of rationale.
