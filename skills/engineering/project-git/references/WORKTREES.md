# Task worktree setup

## 1. Resolve the preference

Inspect the current checkout, branch, staged and unstaged changes, and `git worktree list --porcelain`. Identify the main checkout from Git metadata and read applicable instructions.

Compare the current and main checkouts' root `AGENTS.md` sections named `## Parallel worktrees`, including equivalent existing repository rules. A missing current section falls back to the main checkout's preference only; other branch-specific instructions keep their normal scope. Resolve conflicting preferences before setup.

An explicit task instruction overrides the preference for that task. Change the standing preference only when requested. A host-created worktree alone does not establish a repository-wide choice.

If no repository-wide choice is recorded or explicitly supplied, ask whether to enable independent task worktrees. Explain that either answer is saved in `AGENTS.md`, the default creation root is the main checkout's `.worktree/`, and a custom root is supported. Wait for the answer. Save a declined choice as disabled.

Proceed with the resolved choice and task override; an unanswered question or unresolved conflict blocks setup.

## 2. Save a new or changed choice

For a confirmed repository-wide choice, update the main checkout's root `AGENTS.md`, creating it only if absent. Preserve unrelated content and staged changes. Re-read immediately before writing: reuse a matching choice another session saved; resolve a conflict instead of adding competing rules. If the main checkout cannot be safely read or updated, report the persistence blocker and leave the choice unsaved.

Use a concise dedicated section. For enabled defaults:

```markdown
## Parallel worktrees

Use a distinct worktree and branch for each independent task before modifying files. Reuse a worktree already dedicated to the current task. Create new worktrees under `.worktree/` in the main checkout. Apply this preference without asking again. Explicit task instructions take precedence.
```

Replace the location with its agreed path and anchor for a custom root. For disabled:

```markdown
## Parallel worktrees

Automatic task worktrees are disabled for this repository. Continue in the current checkout without asking again. Preserve unrelated changes. Explicit task instructions take precedence.
```

Proceed when the confirmed choice is saved or an existing choice remains unchanged. Re-reading is not an atomic lock; simultaneous first sessions can still duplicate initialization.

## 3. Select the task checkout

| Resolved context | Action |
| --- | --- |
| Worktrees disabled for this task | Continue in the current checkout; preserve unrelated work and its branch. Shared-checkout writes remain unisolated. |
| Enabled; current linked worktree is dedicated to this task | Reuse it, including a host-created worktree outside the creation root. Confirm ownership from branch and task context, not location alone. |
| Enabled; this task already has edits in an unisolated checkout | Keep delivery there and apply the preference to future tasks. Report the late isolation boundary. Migration needs explicit authorization and clear ownership. |
| Enabled; new task needs isolation | Create a distinct worktree as follows. |

For a new worktree:

1. Resolve the creation root from the task override, recorded preference, then the main checkout's `.worktree/`. Anchor the default `.worktree/` to the main checkout even when invoked in a linked worktree; custom roots keep their agreed anchor. Agent-managed roots require an actual supplied or discoverable path.
2. For a root inside a checkout, establish ignore behavior before creation. Prefer a narrow root `.gitignore` entry such as `/.worktree/`, preserving other rules. A nested `.gitignore` with `*` works locally but ignores itself; distribution requires explicitly tracking it or adding `!.gitignore`. Verify the intended child path with `git check-ignore`. Keep the target outside tracked content and occupied directories.
3. Resolve the base from the task request, project policy, then verified project default branch. Verify the local ref and freshness; fetch when needed and permitted. The current feature branch is not an implicit base. Resolve an unknown base before creation. Choose distinct branch/path names under project conventions and inspect existing registrations; let Git reject an occupied branch rather than forcing reuse.
4. Run `git worktree add -b <task-branch> <task-path> <base-ref>`. Preserve the original checkout's branch, index, and edits except for confirmed preference and necessary ignore setup. Existing edits stay with their owner; automatic stashing, resetting, copying dirty files, or relocation is not part of setup. If isolation is blocked, report the blocker and leave a recoverable state.

Proceed only when the task checkout is identified and its branch and base are verified. Worktree creation alone does not migrate existing edits.

## 4. Ready-to-edit check

In the resolved task checkout, reread applicable instructions. Copy the confirmed preference section into its `AGENTS.md` if missing, along with any agreed root ignore entry into its `.gitignore`; preserve their other content. These copies let normal Git delivery distribute setup to other clones, which cannot rely on the main-checkout fallback.

Before implementation, confirm all of the following:

- No preference question, conflict, or required migration remains unresolved.
- Task path, branch, base, and reused/created/retained state are known; a newly created project-local worktree passed the ignore check.
- Source edits and staging are preserved. Report the working context and all setup paths changed, including copies left in the main checkout.

At delivery, recheck task path and branch before staging. Setup grants no commit, push, PR/MR, or cleanup authorization. Keep main-checkout setup edits and dirty or unmerged worktrees until their delivery or cleanup is authorized.

Linked worktrees isolate files, indexes, and `HEAD`, but share most refs and objects. They cannot prevent merge conflicts or external resource collisions. See the [official Git worktree documentation](https://github.com/git/htmldocs/blob/gh-pages/git-worktree.adoc).
