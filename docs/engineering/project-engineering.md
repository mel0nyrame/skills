# Project Engineering for implementation and useful project knowledge

English | [简体中文](project-engineering.zh.md) · [All guides](../README.md)

`project-engineering` helps an assistant complete a bounded implementation task in an existing project. It establishes the rules, reusable implementation, authoritative editing location, and validation before making changes. Knowledge that future maintainers need should remain in the project after the conversation ends.

This guide follows the [execution instructions](../../skills/engineering/project-engineering/SKILL.md) and [knowledge-governance reference](../../skills/engineering/project-engineering/references/PROJECT-GOVERNANCE.md). The export feature below is a teaching example. Replace its paths with your project's paths.

## Start with a concrete task

Suppose you want CSV export on a reports page. “Add an export button” does not establish whether an export service already exists, which fields may be exported, or whether the client is generated. Those details affect both the editing location and verification.

In the target project, send this request using the collection's Codex plugin.

```text
$skills:project-engineering
Add CSV export to the reports page, matching current list fields and preserving
permission checks. Inspect repository rules and existing export code before
choosing the editing location. Implement and validate the change. Report affected
files and knowledge worth preserving. Do not stage, commit, or push.
```

Use `$project-engineering` standalone or `/skills:project-engineering` in Claude Code. The assistant needs project-file access and, for implementation, editing and validation tools.

## Follow the work through

The assistant first reads instructions applying to the target paths, contribution guidance, and relevant documents. Before choosing an approach, it searches active decision topics and reads related proposals, selected choices, rejection reasons, and open questions. Changed conditions must be stated when reopening an earlier choice. Investigation scales with the task. One component change should not automatically become a whole-project audit.

During design, it uses `project-adr` to preserve meaningful constraints, evaluated rejection reasons, and substantial proposals as they arise, including when implementation is deferred. The same topic owner serves ordinary discussions and external interview skills. `project-adr` owns record content and lifecycle; `project-engineering` supplies reading and synchronization triggers under project instructions.

It then follows relevant calls to find the change entry point. An existing shared export service needs a suitability check. A generated client normally requires changing its schema and regenerating. One example of a coding pattern is a lead for investigation, not evidence of a repository-wide rule.

Persistent-data changes require understanding ownership, retention, deletion, and rebuild behavior. A page-only button does not by itself justify new database-governance documents.

For generated artifacts or persistent-data changes, the assistant reads the matching [change-boundary checklist](../../skills/engineering/project-engineering/references/CHANGE-BOUNDARIES.md) before editing. The main workflow retains the reading conditions and completion checks; detailed branch rules are loaded when applicable.

After implementation, the assistant runs focused checks, inspects actual results, and synchronizes affected documentation and decision facts. A verification claim should identify the check and outcome.

## Files you may receive

There is no fixed bundle generated on every invocation. The task determines implementation paths. Engineering knowledge goes into an existing owner first. These paths are fallbacks when no suitable owner exists.

| File or directory | When it is used | What it contains |
| --- | --- | --- |
| Target modules, tests, necessary generated artifacts | Required by implementation | Delivered behavior and executable verification |
| `docs/engineering/ENGINEERING.md` | Useful findings need preserving and no suitable document owns them | Module boundaries, reuse conditions, editing entry points, validation limits |
| `docs/engineering/DATA.md` | Relevant lasting data rules have no existing owner | Ownership, lifecycle, deletion, and rebuild constraints |
| The project's ADR directory | A durable design topic or implementation change needs recording | Proposals, selected choices, rejection reasons, open questions, evidence, and replacement relationships |

In the teaching example, routing exports through a shared permission service could affect future export features and merit documentation. A function's current line number is directly discoverable and usually needs no separate record.

When a target project has no decision convention, the `project-adr` fallback is `docs/adr/`. This collection itself uses `docs/agents/adr/`. Those paths apply to different projects.

## Check the actual result

Expect an inspectable diff, commands actually run with results, and locations of knowledge added, updated, or reused. No new knowledge file is necessary when nothing useful needs preserving; the report should explain that conclusion.

For the CSV example, verify the requested fields and permissions, relevant tests, and synchronized generated artifacts. Open any reported engineering document. It should explain useful constraints and evidence rather than repeat a directory listing.

A read-only investigation leaves files unchanged and reports findings in chat. Commits, pushes, and PR publication require their own authorization. Continue with [project-adr](project-adr.md), [technical writing](project-prose.md), or [Git operations](project-git.md) for those responsibilities.
