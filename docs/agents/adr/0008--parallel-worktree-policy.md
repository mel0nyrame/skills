# Persist a repository's parallel worktree preference

Status: implemented

## Problem

Concurrent agent sessions can edit the same checkout and share its index and branch operations. Inspecting unrelated changes before a commit cannot protect earlier edits. The [project-git skill](../../../skills/engineering/project-git/SKILL.md) needs a setup entry point as well as a delivery check, and [project-engineering](../../../skills/engineering/project-engineering/SKILL.md) needs to trigger that setup before implementation mutations.

Repeated worktree prompts add friction. The repository preference must survive a session and remain discoverable when an older branch lacks newly written instructions.

## Decision

The user selected one-time confirmation per repository, with the choice recorded in `AGENTS.md`. Record both enabled and disabled choices. An explicit task override does not silently change the repository preference. Purely read-only reviews perform no initialization.

Dedicated setup and publication owners take precedence over generic initialization. A managed root, such as a recap library, retains its own instruction, ignore-rule, and candidate-worktree contract. The one-time generic confirmation covers setup-only writes in both checkouts, including necessary ignore rules; later tasks reuse that authorization while explicit path restrictions still prevail. Defer optional distribution copies outside scope rather than silently enlarging the task.

Use the main checkout's dedicated `Parallel worktrees` section as the preference fallback for older branches. Read only that section through this fallback; the main checkout's other branch-specific instructions do not gain authority in another checkout. Preserve unrelated instructions and staged changes. Carry the confirmed section into the task checkout within authorization so it can travel through normal Git delivery. Compare the selected target again before copying: matching preferences need no edit; a different choice or root blocks implementation pending resolution. Report setup edits left in the main checkout instead of automatically staging or discarding them.

Default new task worktrees to the main checkout's `.worktree/`, unless the task or recorded preference specifies a different creation root. Reuse an existing linked worktree dedicated to the task, including host-created worktrees. Do not assume agent-specific paths. Verify ignore behavior before project-local creation and use a distinct task branch based on the explicit or verified project default base, rather than the current feature branch.

Keep the procedure in the [worktree reference](../../../skills/engineering/project-git/references/WORKTREES.md). `project-git` owns preference persistence and setup; `project-engineering` triggers resolution before editing. Existing dirty edits keep their checkout and ownership. Setup grants no automatic migration, commit, push, publication, or cleanup permission.

The implementation consists of the skill entry point, its conditional worktree reference, discovery metadata, the engineering workflow's pre-edit trigger, and synchronized English/Chinese guides. The reference owns four ordered stages with completion checks: preference resolution, persistence, checkout selection, and readiness to edit. Read-only Git inspection keeps `GIT_OPTIONAL_LOCKS=0` in the skill entry point because that branch skips the reference.

This record owns the worktree policy and supersedes no active record. The [discussion-capture decision](0006--capture-decisions-during-design.md) continues to own decision persistence.

## Alternatives

- **Ask once per repository and persist both answers.** Selected to avoid repeated confirmation, including after a declined setup.
- **Ask on every new session.** Declined by the user because a standing repository preference should remove repeated questions.
- **Record only a common storage directory.** Insufficient for isolation. Distinct task checkout and branch ownership are still needed.
- **Invoke setup only at delivery.** Not selected. It cannot protect edits made before the Git delivery workflow starts.
- **Read only the current branch's `AGENTS.md`.** Not selected as the complete discovery rule. Older branches may lack the preference and prompt again. The main checkout supplies a narrow fallback without adding a separate configuration store.
- **Use an agent-native location as the universal default.** Not selected. A project-local default is consistent across tools. Explicit locations and existing host-created worktrees remain supported; no particular agent path is assumed.
- **Use only `.worktree/.gitignore` containing `*`.** Supported locally, but it ignores itself. Prefer a tracked root ignore entry for distribution, or preserve the ignore file explicitly when choosing that layout.
- **Add a shared preference database or a session lock service.** Not selected. The requested instruction-based workflow does not justify another persistence mechanism. It cannot promise atomic exactly-once initialization.

## Consequences and risks

Worktree creation is now an early workflow responsibility. Agents must read and follow the rule; a skill cannot force unrelated sessions to do so. Linked worktrees isolate checkout files, indexes, and `HEAD`, while sharing most repository references and objects. Merge conflicts and external resource collisions remain possible. See the [official Git documentation](https://github.com/git/htmldocs/blob/gh-pages/git-worktree.adoc).

The main checkout must be available for repository-wide persistence. Creating or updating its preference leaves visible setup edits even when task implementation is isolated elsewhere. Ordinary delivery distributes the preference to other clones. Re-reading before writes reduces duplicate initialization but does not make simultaneous first sessions atomic.

The [validation scenarios and recorded results](../../../tests/scenarios/project_git_worktrees.md) distinguish Git primitive smoke checks, finite agent behavior evaluations, and cases not yet exercised. On 2026-11-05, 67 repository regression tests, ADR validation, both affected skills' format validation, changed-document link/anchor and bilingual-pair checks, nine-skill discovery, and both Claude manifest checks passed. The plugin check also reported an existing missing-icon warning. These checks do not establish behavior across all models or simultaneous first sessions. No installed skill copy, packaging manifest, or root standing policy is changed by this implementation.
