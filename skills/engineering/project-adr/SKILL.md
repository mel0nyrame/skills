---
name: project-adr
description: Use during engineering design discussions to capture durable proposals, choices, and rejection reasons, when resuming related work, when implementation or lifecycle changes affect records, or when establishing project decision maintenance.
---

# Project ADR

Maintain decision memory so another agent can resume a topic without recovering the conversation. The scope extends beyond architecture decision records (ADRs). Follow the target repository's formats, locations, lifecycle, and validation rules.

## Decide whether a record is useful

Follow explicit project creation criteria first. Without them, enter the durable-decision workflow when at least one condition holds. When implementation changes affect an active record, maintain its facts even if there is no new decision:

- A future maintainer could reasonably reopen the question.
- Code and current engineering documentation cannot adequately explain why the choice is necessary.
- Forgetting the reason could reintroduce a tempting wrong approach.

Check architecture boundaries, dependency direction, public protocols/APIs, the security model, critical dependencies, data sources of truth, ownership, flow, isolation, persistent schemas, derived data and rebuilds, retention/deletion, migration/backward compatibility, lasting testing strategy, important process/tooling policy, significant simplifications, key bug lessons, important rejected alternatives, and conditions for reconsideration.

Preserve discussion progress when a meaningful constraint, real tradeoff, or question worth continuing affects future work. Passing suggestions without evaluation, ordinary local bugs, styling, and wording usually need no record. Category labels alone do not establish future value.

When implementation work includes related record maintenance, add records, synchronize facts, and handle supersession in the same change as the code. Read-only reviews report gaps. Archive, deletion, and governance integration actions remain subject to the relevant task authorization.

## Locate rules and records

Read applicable repository and subtree instructions, contribution guides, documentation entry points, and decision configuration. Reuse existing directories, naming, metadata, and lifecycle. A directory name alone does not establish authority.

This skill owns record value, topic content, rationale, and lifecycle. `project-engineering`, when available, reads records during investigation and triggers synchronization as implementation changes. Project instructions expose the same contract to ordinary discussions and external discussion skills. Keep external skills unchanged; their installation does not adopt their default template or creation threshold. All participating workflows reuse one project convention and topic owner.

Use creation criteria, locations, formats, states, and check entry points specified by the current user request and applicable project rules. Without explicit rules, reuse stable, consistent conventions in comparable records. One outlier or mixed samples do not establish a new rule. Use the defaults below for unresolved parts.

Before proposing or implementing related work, search active records by task topic, capabilities, constraints, paths, and rejected alternatives. Read matching proposals, choices, rejection reasons, and open questions, or establish that none match. Keep this topic context for discussion and same-topic review below. Refresh discovery when changes in scope, constraints, capabilities, paths, search terms, evidence, or relevant records could make the earlier search incomplete. Reuse prior reads while those inputs remain valid. If conditions changed, identify them explicitly before reconsidering the choice. Check uncommitted changes before writing and preserve other work. Terminology documents own terms, engineering documents own current facts, and ADRs own reasons.

Without any repository conventions, use one Markdown file per decision topic in `docs/adr/`, named `NNNN--kebab-title.md`. Keep related candidates and their outcomes together; create a separate rejected record only for independent lasting value. Use the project's main language for record titles and prose. The default archive location is `docs/adr/archive/`.

Prefer discovery through directories, metadata, filenames, and search. Avoid adding a central index that every branch must update manually. Follow existing index policy. An index fully generated from authoritative metadata with a freshness check may remain.

Read [project integration](references/PROJECT-INTEGRATION.md) when the user requests ongoing maintenance or the first decision is being written in a project whose existing instruction entry point lacks maintenance rules. It owns standing triggers, directory contracts, and check integration. Installing a skill does not complete project integration.

## Capture discussion progress

When recording or resuming a design discussion, read [discussion capture](references/DISCUSSIONS.md) for capture triggers, topic content, and the checkpoint before pausing. Use the topic context established above. Completion requires meaningful progress to be preserved with an accurate state and enough context for the next agent to resume.

## Check same-topic records before adding one

Before drafting, classify the records already found under “Maintain current facts and decisions.” Reuse the existing topic owner for evolving candidates, recommendations, open questions, and selection of a previously pending choice. Use the discovery refresh rule above when new information could reveal records the earlier search did not cover. When a new record replaces a selected choice, state what it replaces and which constraints remain valid. Maintain replacement links in both directions within the change.

Complete this scope's supersession review for every new record. For fully replaced records needing consolidation, archive, or deletion, perform lifecycle maintenance within authorization. Otherwise, preserve the original file and state relationships and pending actions. Partial replacement preserves each record's unique reasons. Limit review to active same-topic records unless the task requests a full corpus audit.

## Write a complete decision

Use the target repository's template, explicit format rules, or stable conventions among comparable records. A short template may express choice and rationale in one paragraph. Follow project requirements for states and separate sections. Preserve the existing format during maintenance and add genuine tradeoffs needed to understand the choice. The default structure is not a reason to expand or rearrange another valid template.

Without a reusable format, or when old records are mixed and no explicit convention exists, use the default structure. New records need a title, one explicit state, and four sections in this order. Keep titles consistent with the project's main language. The English default is shown below; choose the state under “Choose a lifecycle.” The checker also accepts the complete Chinese schema for existing projects.

```markdown
# Decision title

Status: proposed

## Problem
## Decision
## Alternatives
## Consequences and risks
```

Each default section must meet its completion criterion. For a project template, check its required content and put necessary reasons and tradeoffs where that template permits:

- **Problem:** state the constraints or conflict requiring a choice and the applicable scope.
- **Decision:** state the current choice or proposal, its reasons, assumptions, and boundaries. For unfinished topics, distinguish selected conclusions from recommendations and name unresolved questions and next steps.
- **Alternatives:** record the candidates actually evaluated, their current outcomes, and reasons for rejection where decided. Pending candidates remain pending. When history cannot be reliably recovered, mark it unknown or use the project's allowed missing-value notation. Preserve the evidence gap rather than inventing alternatives or rejection reasons.
- **Consequences and risks:** state benefits, costs, and limits. Include relevant failure modes, validation evidence, known gaps, or conditions for reconsideration. Mark unverified content unknown.

Empty sections, a list containing only the chosen technology, or all four information types mixed into one paragraph do not satisfy the default structure. Add dates, owners, and other fields when the project requires them. For supersession, state its direction, scope, and record links near the state. Current engineering documents explain how the system works. Decisions explain why a choice was made and what was rejected. Link them without copying the full content.

Read-only reviews report format and content gaps. When authorized to maintain older records, prioritize affected active records, preserve unique reasons and genuine gaps, and avoid bulk historical rewrites solely for format consistency. Archive bodies remain frozen.

## Maintain current facts and decisions

Compare the record with current code, configuration, tests, engineering documents, active same-topic records, and inbound links. Distinguish:

- **Implementation facts change; the decision holds:** synchronize paths, packages, configuration keys, defaults, owners, or implementation locations so the record points to current implementation. Update facts directly rather than appending a changelog.
- **The discussion evolves:** update the topic owner for candidate evaluation, recommendations, open questions, or selection of a pending choice. These updates alone do not create a replacement record.
- **A selected choice is replaced:** follow project replacement rules; by default, create a new record with supersession and cross-links. Preserve what the old decision actually chose, including when that choice was accepted but not yet implemented.
- **Partial replacement:** the old record still owns unique rationale, constraints, alternatives, compatibility promises, or reconsideration conditions. Keep both records and cross-link them.
- **Full replacement:** consolidate under repository rules only after the new owner preserves meaningful rationale, alternatives, consequences, required verification, coverage gaps, and reconsideration conditions, and inbound links are repaired.
- **Still valid:** nearby topics own different decisions and both remain active.

Code and configuration own current behavior. Tests own executable guarantees. Generated artifacts derive from upstream owners by default. Current-state documentation owns usage and engineering facts. Active decisions own reasons and tradeoffs.

## Choose a lifecycle

Follow existing project lifecycle rules or stable state conventions, including whether a state is mandatory, whether it lives in YAML or prose, and the vocabulary. Determine meaning from actual implementation and replacement links. A label such as `accepted` does not prove implementation. Preserve existing representation. If a project has no state field, verify the actual lifecycle and express required supersession relationships in its own format.

When the project has no state convention and the default structure is used, read [default states](references/LIFECYCLE.md#default-states) before assigning a state. Confirm the state matches implementation and replacement relationships.

## Archive or delete safely

Before archiving or deleting a record, read [the retirement protocol](references/LIFECYCLE.md#archive-or-delete). Complete its preservation and dependency checks within task authorization. Archived bodies remain frozen.

## Validate and report

Before delivery, review each new or maintained active record. Confirm the selected project convention or default structure, accurate lifecycle facts, complete required content, clear replacement direction and scope, and resolvable links.

Run the repository's focused checks for format, required sections, path/lifecycle consistency, links, metadata, and archive integrity. Run other project checks according to risk. Report added or updated decisions, fact synchronization, full or partial replacement, retained or deleted rejected records, archives, and commands actually run with their results.

For the default English or Chinese structure without a matching project checker, run [the default checker](scripts/check_adr.py) on the affected files or ADR directory. Read project integration for check wiring. Use project-specific checks for short templates, custom states, or other structures. When none exist, review records individually and report scope. Preserve other valid templates rather than rewriting them to satisfy this checker.

Completion requires meaningful discussion progress to be preserved, every affected active record to be synchronized, a same-topic review conclusion for every new record, authorized supersession and lifecycle work to be complete, and passing format, state, and local-link-path checks. A successor must be able to distinguish the current conclusion, evaluated alternatives, open questions, and implementation evidence. Report missing historical evidence, actions outside authorization, and project-integration gaps honestly. A passing checker does not resolve them.

Mechanical checks establish structure, state values, and link consistency. Semantic judgment still establishes content completeness, real alternatives, and the future value of rationale.
