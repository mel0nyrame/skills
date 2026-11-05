# Project Git for parallel worktrees, review, and delivery

English | [简体中文](project-git.zh.md) · [All guides](../README.md)

`project-git` establishes or follows a repository's parallel-worktree preference and handles existing changes. It helps inspect the working tree, form coherent commits, and execute a commit or push only when requested.

A commit saves a version in local Git history. A push sends commits to a remote repository. They are separate decisions. You can use the skill only to review changes without authorizing either action.

## Establish the working context once

Before a task starts modifying files or Git state, the assistant reads the recorded preference in `AGENTS.md`. If none exists, it asks once whether to enable independent worktrees for parallel tasks. It records either choice, so later sessions follow it without repeating the question. Purely read-only reviews do not initialize a preference or change Git state.

When enabled, new tasks use distinct worktrees and branches. An existing worktree dedicated to this task, including one created by the agent's host, is reused. The default location is `.worktree/` under the main checkout; an explicit task location or recorded custom location takes precedence. The assistant verifies ignore rules before creating a project-local checkout. It does not guess agent-specific default directories.

```text
$skills:project-git
Enable independent worktrees for this repository. Use the default .worktree/
location and record the choice in AGENTS.md. Do not commit or push.
```

The main checkout's dedicated preference section is the fallback when an older branch lacks it. Only that preference is reused; other instructions retain their normal scope. Setup preserves unrelated edits and reports where it wrote the preference and ignore rule. Existing edits remain in their original checkout unless migration is explicitly authorized. Independent worktrees do not eliminate later merge conflicts or isolate external services.

The [worktree procedure](../../skills/engineering/project-git/references/WORKTREES.md) orders preference resolution, persistence, checkout selection, and a ready-to-edit check. Implementation starts only after pending choices are resolved and task ownership, base, source preservation, and applicable ignore rules are verified. Read-only Git inspection uses `GIT_OPTIONAL_LOCKS=0` without loading setup details.

## Establish the permitted action

In this teaching example, the working tree contains report-export changes and unrelated login-message edits. Start by reviewing only the export work.

```text
$skills:project-git
Review report-export changes and tests. Identify problems and suggest commit
boundaries. Login-message edits belong to other work. Leave them alone.
For this round, do not edit files, stage, commit, or push.
```

This uses the collection's Codex plugin. Use `$project-git` standalone or `/skills:project-git` in Claude Code. The assistant needs Git and access to applicable repository rules.

It should distinguish this task's changes from other staged and unstaged work. When a push is requested, it additionally checks remotes, the target branch, upstream tracking, and outgoing commits. Existing validation must still cover the current changes.

## Authorize a commit after review

Once you accept the grouping, give a concrete instruction.

```text
Commit only the report-export feature and its tests. Preserve login-message edits.
Follow repository hooks. Report the commit hash and remaining working tree.
Do not push.
```

The assistant stages explicit paths or portions, reviews the staged diff, and commits. Tests, lockfiles, and required generated outputs belong with the implementation they support. Split when intentions are independently explainable and reversible, rather than by file count alone.

Before drafting a commit title, the assistant checks applicable repository instructions, contribution guides, and commit-tool configuration for both format and description language. Where written rules are silent, it checks relevant recent non-merge commits for a consistent, structured convention. Explicit task instructions take precedence.

| Available guidance | Commit-title choice |
| --- | --- |
| Project requires English Conventional Commits | `feat(export): add report export` |
| No written rule, but recent commits consistently use English Conventional Commits | Follow that format and English descriptions |
| Only loose titles such as `fix xxx`, `add xxx`, `修复了xxx`, or `加入xxx` | Use the default `feat(export): 增加报表导出` |
| User explicitly requests English, with no project title format | Keep the default structure and write `feat(export): add report export` |

Format and language are resolved separately; defaults fill only unspecified aspects. Without an established convention or explicit override, the title is `<type>(<scope>): <Chinese description>`, with optional scope. A branch can use `feat/report-export` when no branch naming rule exists. These are teaching examples, not commit results.

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

The external [pr skill](pr.md) helps draft the PR body. Creating or updating a hosted PR is another operation. Consult the [naming conventions](../../skills/engineering/project-git/references/CONVENTIONS.md), [delivery-record rules](../../skills/engineering/project-git/references/TRACKER.md), and [execution instructions](../../skills/engineering/project-git/SKILL.md) for details.
