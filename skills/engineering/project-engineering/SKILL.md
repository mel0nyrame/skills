---
name: project-engineering
description: Use when implementing features, fixing defects, refactoring or migrating a project, or organizing its engineering knowledge.
---

# Project Engineering

Change a project as a long-term maintainer: establish how the project permits changes before implementing the goal. Preserve these responsibilities:

- Repository and subtree instructions own standing rules within their scope.
- This skill defines how the agent investigates and changes a project.
- Engineering documents own current engineering intent, boundaries, ownership, and maintenance entry points that code cannot express well.
- Code, configuration, and tests express the current implementation and executable behavior.
- Durable decision records own lasting reasons, alternatives, and consequences.

## 1. Read applicable rules

Identify target files or modules. Read applicable instructions along the path from the repository root to each target. Recognize the mechanisms the project actually uses, including `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, module-local notes, contribution guides, and linked engineering documents. Use the project's filenames rather than requiring a fixed one.

Apply the repository's precedence rules to global and local instructions. Root instructions should contain genuinely global standing orders. Keep module-specific rules with the nearest responsible owner. For work across subtrees, establish each subtree's applicable rules separately.

For a simple local change without architecture or data-boundary effects, stop investigation after identifying the target module, change entry point, nearby reusable implementation, and focused validation. Check the relevant specialized concerns for changes involving multiple modules, infrastructure, generation pipelines, persistent data, or lasting engineering policy.

## 2. Build a just-enough change map

Locate engineering knowledge through rules or documentation entry points. Without an explicit entry point, inspect relevant READMEs, ADRs or decisions, CI, package/build metadata, formatter/lint/type-check configuration, schemas, migrations, code generation, target modules, and tests. Start at entry points and follow dependencies relevant to this task. Stop when the context is sufficient for a safe change.

Search active decisions by affected capabilities, paths, symbols, and configuration keys. Identify which decisions still constrain this change and which facts will change with the implementation. Read the relevant records, or establish that none match the scope, before implementing. Use archives only when historical evidence is explicitly needed.

Classify engineering knowledge for the current task:

- **Complete:** use it and verify that key entry points still match the implementation.
- **Partly missing:** preserve existing owners and identify the knowledge this task needs to add or correct.
- **Absent:** establish minimal context around relevant modules, architecture boundaries, reusable assets, change entry points, data, and validation. Persist findings with future maintenance value under section 7.

Initialize with **Just Enough Engineering Context**. Keep investigation scoped, avoid encyclopedic documentation, and create governance files only when they have actual content.

Classify each engineering claim:

- **Confirmed Rule:** supported by applicable repository rules, an active decision, a configuration contract, or other authoritative evidence. Record its location.
- **Observed Convention:** several relevant implementations share a pattern without an explicit rule. Use it as an investigation lead.
- **Unknown:** based on one example, conflicting evidence, or an unverified claim. Keep it open rather than turning it into a rule.

A single call site does not establish a project rule. A directory does not prove a unique implementation. A shared package does not prove mandatory use. Current implementation does not establish a permanent principle, and one database does not establish the source of truth for all data. Ask the user only when an Unknown materially changes implementation and cannot be verified from the repository.

Before writing, identify relevant modules and layers, existing capabilities and extension points, the **Canonical Change Entry Point**, generated artifacts and generation commands, data effects, validation entry points, and confidence in each conclusion.

## 3. Follow project-specific engineering policy

Prioritize private project rules that materially affect implementation: module responsibilities, dependency direction, Controller/Service/Repository boundaries, HTTP/authentication/logging/configuration/error-model entry points, package creation, shared components, code generation, migrations, test placement, and runtime ownership. Leave mechanical formatting, naming, and whitespace to the project's formatter, lint, type checks, and static analysis.

Persist **Architecture Conventions** before repeating **Style Conventions**.

## 4. Reuse existing capabilities

Start with the capability index in engineering knowledge, then verify implementations, callers, and extension points. Only a Confirmed Rule can make an implementation a mandatory canonical asset. An Observed Convention only raises its investigation priority.

Extend existing assets through their extension points when they can meet the need. Add parallel infrastructure only when existing assets do not own the responsibility or cannot meet a verified requirement. Record the reason where the project requires it. A capability entry contains only:

```text
Capability
Canonical implementation
Use for
Do not
Extension point
```

Source code or its API owner owns API details.

## 5. Change the authoritative entry point

Distinguish the runtime **Source of Truth** from the development **Canonical Change Entry Point**. A production database may own runtime facts, while schema definitions and migrations own manual schema changes.

When the change touches generated or derived artifacts, read [generated artifacts](references/CHANGE-BOUNDARIES.md#generated-artifacts) before editing. Change their owner, regenerate through the supported process, and review the derived diff.

## 6. Govern persistent data

When adding persistent data or changing its schema, flow, ownership, isolation, lifecycle, deletion, or rebuild strategy, read [persistent data](references/CHANGE-BOUNDARIES.md#persistent-data) before implementation. Apply that review to agent memory and derived stores as well as business data. Proceed when affected boundaries and the migration/rebuild approach are established; resolve material unknowns first.

## 7. Implement and persist project knowledge

Make the smallest change within confirmed boundaries and entry points. When engineering documents conflict with implementation, check applicable rules, active decisions, configuration, tests, generation pipelines, and necessary Git history. Then correct implementation that violates a Confirmed Rule, update stale facts, describe a verifiable migration state, or retain an Unknown. History explains change; it cannot alone establish current behavior.

After implementation, inspect each engineering finding introduced or changed by this task. Persist module boundaries, reuse conditions, authoritative change entry points, data ownership and lifecycle, validation limits, or non-obvious constraints when they affect future changes and code, configuration, or tests cannot express them directly. Conversation, plans, and delivery notes do not replace project files. Reuse accurate existing records. Avoid duplicating implementation details that are directly discoverable.

Preserve each finding's single owner: reusable assets own common capabilities, change-entry-point documentation owns source/generated relationships, data-governance documents own current data facts, and architecture documents own module responsibilities. Update gaps in existing owners. Without a suitable owner, create a minimal record under project conventions, or use the defaults in the governance reference. Persist only knowledge within the current scope. The existence of `AGENTS.md` or ADRs does not establish coverage of these topics. Instructions still own standing rules, and decisions still own lasting reasons.

Each record states its scope, engineering conclusion, evidence locations, and confidence, including conditions and limitations that affect use. Confirm future agents can find it through project rules, documentation entry points, or directory searches. Add a conditional link at the nearest module entry point when necessary.

For read-only tasks, report the knowledge to preserve and its intended location while leaving files unchanged. Knowledge writes remain subject to user authorization and applicable project rules.

When creating or extending standing instructions, engineering documents, indexes, or mechanical gates, read [project knowledge governance](references/PROJECT-GOVERNANCE.md). It owns document responsibilities, avoidance of central mutable indexes, instruction budgets, and executable governance. Keep those details there.

## 8. Validate, maintain decisions, and deliver

Run the project's focused validation for this change. Review generated artifacts, migrations, and rollback effects. Report only commands actually executed and their results.

Before delivery, account for every finding that section 7 requires preserving. Confirm a persistent record and discoverable entry point exist, references resolve, and content matches implementation. Report added, updated, or reused knowledge locations, or explain why nothing needs preserving. Reading a skill or finishing code edits does not complete this check.

Compare the active decisions found in section 2 with the actual changes. When paths, symbols, defaults, owners, or mechanisms change, use `project-adr` to update existing records in the same change. Use it for new decisions and same-topic supersession when lasting reasons change or arise. Check affected records' facts even when no new decision is needed.

Follow project conventions for creation criteria, locations, formats, and states. Reuse records already produced by another workflow for the same decision. Delegate maintenance to `project-adr` when available. Otherwise, perform the same factual review and required updates under project rules, and report gaps those rules do not cover. This does not require installing other domain-modeling or ADR skills.

Lasting reasons can concern architecture and dependencies, public protocols, security and critical dependencies, data design and compatibility, testing strategy, important process/tooling policy, important simplifications, and rejected alternatives that remain tempting. For an ordinary local change without affected records or lasting reasons, explain why maintenance is unnecessary. Completion requires synchronized affected decisions, resolved relationships between old and new records, and passing required checks. Report record locations or the exemption reason.

Use `project-prose` to check factual ownership and complete contracts when changing technical prose. Use `project-git` when the user requests commits or pushes. For PR/MR titles, descriptions, creation, or updates, use the external [pr skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr). If it is unavailable, report the dependency. These skills do not expand user authorization.
