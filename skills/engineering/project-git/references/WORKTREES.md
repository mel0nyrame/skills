# Repository worktree preference

Use this procedure before a Git-backed task's first file or Git-state mutation. A purely read-only review leaves the checkout, index, instructions, and worktree registry unchanged. Use `GIT_OPTIONAL_LOCKS=0` for read-only inspection commands that could otherwise refresh the index.

## Resolve the preference

Inspect the current checkout, branch, staged and unstaged changes, and `git worktree list --porcelain`. Identify the main checkout from Git's worktree metadata, not the current directory's parent or a guessed agent path. `.worktree/` is always relative to that main checkout, even when invoked inside a linked worktree.

Read applicable instructions and compare the `## Parallel worktrees` sections in the current and main checkouts' root `AGENTS.md` files. If an older branch lacks the section, use the main checkout's section as the repository preference. This fallback imports only the dedicated preference, not the main checkout's other branch-specific instructions. Honor equivalent existing repository rules without rewriting them merely to match this heading. Conflicting recorded preferences require resolution before setup; do not silently replace one.

An explicit task instruction overrides a standing preference for that task. It does not change the standing preference unless the user requests that. A tool-created worktree does not by itself establish a repository-wide choice.

If no standing choice or explicit repository-wide choice exists, ask once whether to enable independent worktrees for this repository. State that confirmation records the choice in `AGENTS.md`, uses `.worktree/` by default, and accepts a custom location. Treat an unanswered question as pending. Record a declined choice as disabled so later sessions do not ask again. An explicit instruction to keep a task read-only takes precedence over preference initialization.

## Persist a confirmed choice

Store a concise preference in the main checkout's root `AGENTS.md` so sessions on older branches can discover it before the policy is merged. Preserve all unrelated content and staged changes. Create the file only if absent. Re-read the section immediately before writing: reuse a matching choice recorded by another session; resolve a conflicting choice instead of appending competing rules. If the main checkout or its instructions cannot be safely read or updated, report the persistence blocker rather than claim the preference was saved or store it in an unrelated repository.

An enabled default can be expressed as:

```markdown
## Parallel worktrees

Use a distinct worktree and branch for each independent task before modifying files. Reuse a worktree already dedicated to the current task. Create new worktrees under `.worktree/` in the main checkout. Apply this preference without asking again. Explicit task instructions take precedence.
```

For a confirmed custom root, replace the location with the actual agreed path and its anchor. For a disabled choice:

```markdown
## Parallel worktrees

Automatic task worktrees are disabled for this repository. Continue in the current checkout without asking again. Preserve unrelated changes. Explicit task instructions take precedence.
```

Carry the same preference section into the task checkout if its `AGENTS.md` lacks it, preserving that checkout's other instructions. This allows the policy to travel through a normal authorized commit and merge. Report both edited paths when they differ. Do not stage or commit either copy without matching delivery authorization, and do not automatically discard the main checkout's setup edits after a task commit. Explain that other clones and worktrees without access to this main checkout need the policy distributed through normal Git delivery.

This is instruction-level coordination. Re-reading reduces duplicate initialization but is not an atomic lock or a strict exactly-once guarantee for simultaneous first sessions.

## Establish the task checkout

When disabled, continue in the current checkout while preserving other work. This choice does not make concurrent writes to one checkout safe. Do not switch a shared checkout's branch or stage another task's paths.

If this task already has edits in a checkout that was not isolated before editing, keep delivery of those edits in that checkout. Apply a newly enabled preference to future tasks and report the current task's late isolation boundary. Create or move to another checkout for those edits only when migration is explicitly requested and its ownership is clear; opening an empty worktree does not isolate existing work.

When enabled:

1. Reuse the current linked worktree when it is already dedicated to this task, including a host-created worktree at a different location. Do not move it just to enforce the default creation root. Location alone does not prove task ownership; confirm the branch and task context.
2. Otherwise, resolve the creation root from explicit task instructions, then the recorded repository preference, then the main checkout's `.worktree/`. Use an agent-managed location only when actually supplied or discoverable from that tool's current context; do not assume a Codex or OpenCode path.
3. For a root inside a checkout, establish and verify ignore behavior before creating the worktree. Prefer a narrow root `.gitignore` entry such as `/.worktree/`; preserve existing rules. An existing `.worktree/.gitignore` containing `*` is also usable locally, but ignores itself. If that file must be distributed, explicitly track it or use `*` plus `!.gitignore`. Verify with `git check-ignore` against the intended child path. Do not create worktrees under tracked content or overwrite an occupied path.
4. Choose the base from the explicit task request, then project policy, then the verified project default branch. Confirm the local reference and its freshness before creating the task branch; fetch if needed and permitted. Never silently use the current feature branch as the base. If the base cannot be established, resolve it before creating the worktree. Use distinct branch and path names under the project's naming conventions. Inspect existing registrations before creation; let Git reject a branch already checked out elsewhere rather than forcing reuse.
5. Create the task checkout with `git worktree add -b <task-branch> <task-path> <base-ref>`. Preserve the original checkout, branch, index, and edits, apart from the confirmed preference and necessary ignore setup. Existing task edits do not follow a new worktree: keep their checkout and ownership intact, report the late isolation boundary, and resolve any required migration with the user. Do not automatically stash, reset, copy dirty files, or relocate existing edits. If existing work prevents safe isolation, stop setup rather than claiming it succeeded.
6. Continue all task edits and Git operations in the resolved checkout. Carry any newly agreed root ignore entry into the task checkout's `.gitignore` for normal delivery, preserving its existing rules. Verify the branch and base, reread applicable instructions, and report the path, branch, base, reused/created state, and any setup files left in the main checkout. Complete worktree setup before implementation changes.

At delivery, verify the current path and branch still belong to this task. Never stage changes from another checkout merely because the repository metadata is shared. Commits, pushes, PR/MR operations, and worktree removal retain their separate authorization requirements. Leave dirty or unmerged worktrees intact unless cleanup is explicitly authorized.

## Isolation limits

Linked worktrees have separate checkout files, indexes, and `HEAD`, but share most refs and repository objects. They do not eliminate merge conflicts or isolate ports, databases, caches, or other external resources. See the [official Git worktree documentation](https://github.com/git/htmldocs/blob/gh-pages/git-worktree.adoc). This procedure supplies agent instructions, not a process supervisor or mandatory locking service.
