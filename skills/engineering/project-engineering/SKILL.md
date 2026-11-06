---
name: project-engineering
description: Use when investigating or implementing features, fixes, refactors, or migrations, or organizing project engineering knowledge. Read related decisions before choosing an approach and preserve durable design progress as it develops.
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

Before the first file mutation in a Git repository, follow a dedicated workflow when it owns this task's setup or publication. Otherwise use `project-git` for worktree setup when available; it owns preference resolution and the ready-to-edit check within task authorization. If unavailable, follow repository policy and resolve any missing working-context choice before editing. Read-only investigation skips setup.

## 2. Build a just-enough change map

Locate engineering knowledge through rules or documentation entry points. Without an explicit entry point, inspect relevant READMEs, ADRs or decisions, CI, package/build metadata, formatter/lint/type-check configuration, schemas, migrations, code generation, target modules, and tests. Start at entry points and follow dependencies relevant to this task. Stop when the context is sufficient for a safe change.

Before proposing or implementing an approach, search active decisions by affected capabilities, constraints, paths, symbols, and configuration keys. Read related proposals, selected choices, rejection reasons, and open questions, or establish that none match. Identify constraints and facts that may change. When changed conditions justify reconsideration, state them explicitly and reevaluate with the earlier rationale visible. Existing plans do not authorize execution. Use archives only when historical evidence is explicitly needed.

During investigation and design, use `project-adr` when meaningful constraints, evaluated rejection reasons, or substantial proposals need preserving. It owns record criteria, topic content, lifecycle, and discussion checkpoints; this workflow triggers it as progress occurs. When it is unavailable, follow the project's decision rules directly. External discussion skills reuse those rules and need no modification.

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

Extend existing assets through their extension points when they can meet the need. Add parallel infrastructure only when existing assets do not own the responsibility or cannot meet a verified requirement. Record the reason where the project requires it. When writing capability entries, read [capability entries](references/PROJECT-GOVERNANCE.md#capability-entries) for their content boundary.

## 5. Change the authoritative entry point

Distinguish the runtime **Source of Truth** from the development **Canonical Change Entry Point**. A production database may own runtime facts, while schema definitions and migrations own manual schema changes.

When the change touches generated or derived artifacts, read [generated artifacts](references/CHANGE-BOUNDARIES.md#generated-artifacts) before editing. Change their owner, regenerate through the supported process, and review the derived diff.

## 6. Govern persistent data

When adding persistent data or changing its schema, flow, ownership, isolation, lifecycle, deletion, or rebuild strategy, read [persistent data](references/CHANGE-BOUNDARIES.md#persistent-data) before implementation. Apply that review to agent memory and derived stores as well as business data. Proceed when affected boundaries and the migration/rebuild approach are established; resolve material unknowns first.

## 7. Implement and persist project knowledge

Make the smallest change within confirmed boundaries and entry points. When engineering documents conflict with implementation, check applicable rules, active decisions, configuration, tests, generation pipelines, and necessary Git history. Then correct implementation that violates a Confirmed Rule, update stale facts, describe a verifiable migration state, or retain an Unknown. History explains change; it cannot alone establish current behavior.

Preserve durable decision progress during design under section 2. After implementation, inspect each engineering finding introduced or changed by this task. Persist module boundaries, reuse conditions, authoritative change entry points, data ownership and lifecycle, validation limits, or non-obvious constraints when they affect future changes and code, configuration, or tests cannot express them directly. Conversation, plans, and delivery notes do not replace project files. Reuse accurate existing records. Avoid duplicating implementation details that are directly discoverable.

Preserve each finding's single owner: reusable assets own common capabilities, change-entry-point documentation owns source/generated relationships, data-governance documents own current data facts, and architecture documents own module responsibilities. Update gaps in existing owners. Without a suitable owner, create a minimal record under project conventions, or use the defaults in the governance reference. Persist only knowledge within the current scope. The existence of `AGENTS.md` or ADRs does not establish coverage of these topics. Instructions still own standing rules, and decisions still own lasting reasons.

Each record states its scope, engineering conclusion, evidence locations, and confidence, including conditions and limitations that affect use. Confirm future agents can find it through project rules, documentation entry points, or directory searches. Add a conditional link at the nearest module entry point when necessary.

For read-only tasks, report the knowledge to preserve and its intended location while leaving files unchanged. Knowledge writes remain subject to user authorization and applicable project rules.

When creating or extending standing instructions, engineering documents, indexes, or mechanical gates, read [project knowledge governance](references/PROJECT-GOVERNANCE.md). It owns document responsibilities, avoidance of central mutable indexes, instruction budgets, and executable governance. Keep those details there.

## 8. Validate, maintain decisions, and deliver

Run the project's focused validation for this change. Review generated artifacts, migrations, and rollback effects. Report only commands actually executed and their results.

Before delivery, account for design progress under section 2 and every finding that section 7 requires preserving. Confirm a persistent record and discoverable entry point exist, references resolve, and implementation claims match evidence. Selected but unfinished work retains its applicable pre-implementation state and remaining questions. Report added, updated, or reused knowledge locations, or explain why nothing needs preserving. Reading a skill or finishing code edits does not complete this check.

Compare the active decisions read in section 2 with the actual changes. Use `project-adr` to synchronize affected facts in the same change, even when no new decision is needed, and to handle new choices or replacement relationships. Reuse records already produced by another workflow. When the skill is unavailable, complete the same factual review and required maintenance under project rules; report gaps without requiring another skill installation.

Complete delivery only when affected records are synchronized, replacement relationships are resolved, and required checks pass. Report record locations, remaining limits, or why this change needs no decision maintenance. The project's decision rules take precedence over skill defaults. Use `project-adr` for record criteria, content, and lifecycle within those rules.

Use `project-prose` to check factual ownership and complete contracts when changing technical prose. Use `project-git` when the user requests commits or pushes. Use the external [pr skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr) for PR/MR bodies; report the dependency if unavailable. Follow project conventions for titles. Create or update hosted requests through the available platform tools only within user authorization, and verify the platform result. A completed body alone does not complete a publication request.
