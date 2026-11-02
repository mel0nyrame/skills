# Git Operations for review, commits, and delivery

English | [简体中文](git-ops.zh.md) · [All guides](../README.md)

`git-ops` handles changes already present in a project. It helps inspect the working tree, form coherent commits, and execute a commit or push only when requested.

A commit saves a version in local Git history. A push sends commits to a remote repository. They are separate decisions. You can use the skill only to review changes without authorizing either action.

## Establish the permitted action

In this teaching example, the working tree contains report-export changes and unrelated login-message edits. Start by reviewing only the export work.

```text
$skills:git-ops
Review report-export changes and tests. Identify problems and suggest commit
boundaries. Login-message edits belong to other work. Leave them alone.
For this round, do not edit files, stage, commit, or push.
```

This uses the collection's Codex plugin. Use `$git-ops` standalone or `/skills:git-ops` in Claude Code. The assistant needs Git and access to applicable repository rules.

It should distinguish this task's changes from other staged and unstaged work. When a push is requested, it additionally checks remotes, the target branch, upstream tracking, and outgoing commits. Existing validation must still cover the current changes.

## Authorize a commit after review

Once you accept the grouping, give a concrete instruction.

```text
Commit only the report-export feature and its tests. Preserve login-message edits.
Follow repository hooks. Report the commit hash and remaining working tree.
Do not push.
```

The assistant stages explicit paths or portions, reviews the staged diff, and commits. Tests, lockfiles, and required generated outputs belong with the implementation they support. Split when intentions are independently explainable and reversible, rather than by file count alone.

Without repository naming rules, a branch can use `feat/report-export`. The default commit title is `<type>(<scope>): <Chinese description>`. Established target-project rules take precedence.

## Know what the operation produces

| Authorized stage | Main output | Git-state change |
| --- | --- | --- |
| Read-only review | Findings, grouping suggestions, validation discussion in chat | Files and staging remain unchanged |
| Commit | One or more local commits and their hashes | Selected changes enter history; other work remains |
| Push | Actual remote and branch delivery result | Authorized commits reach the remote |

There is no default `git-report.md`. Request a path if you need a written review record. Commit output primarily belongs to history managed under `.git/`; a Markdown report cannot prove that a commit succeeded.

## Verify the boundary was respected

During review, check that unrelated edits were not absorbed into the proposed commit. After committing, inspect the reported hash and content, then confirm remaining work is intact. After pushing, verify that the remote and branch match your instruction.

Failed validation or hooks should result in an accurate explanation and recoverable state. Hooks are not bypassed to force completion. Force pushes, history rewrites, and remote deletion require explicit authorization matching the scope.

The external [pr skill](pr.md) helps draft the PR body. Creating or updating a hosted PR is another operation. Consult the [naming conventions](../../skills/engineering/git-ops/references/CONVENTIONS.md), [delivery-record rules](../../skills/engineering/git-ops/references/TRACKER.md), and [execution instructions](../../skills/engineering/git-ops/SKILL.md) for details.
