# Project Git worktree scenarios

These cases validate the instruction contract in isolated Git repositories. They do not authorize writes to a real project's instructions, branches, or remote. A future agent evaluation must receive the skill, raw repository fixture, and user prompt without the expected outcomes below.

## Agent behavior cases

| Fixture and user request | Expected observable result |
| --- | --- |
| No recorded preference; ask the agent to implement a small change | Before implementation, ask once about repository-wide worktrees and describe persistence and the default location; wait for an answer |
| Confirm enabled with no custom path | Save the enabled preference, establish ignore behavior, and create a distinct task worktree under the main checkout's `.worktree/` from the resolved base |
| Decline setup, then start a later session | Save disabled; the later session continues without the same question and preserves unrelated edits |
| Main checkout has enabled policy; old task branch lacks it | Read only the main checkout's dedicated preference as fallback; do not ask again or import its unrelated branch rules |
| Current branch and main checkout record conflicting preferences | Report the conflict and resolve it before setup; do not append competing instructions |
| Already in a host-created linked worktree dedicated to the task | Reuse it and report path/branch/base; do not relocate it or nest `.worktree/` inside it |
| Standing policy uses `.worktree/`; user explicitly supplies another location for one task | Use that location without rewriting the standing preference |
| Source checkout has staged and unstaged edits; new task explicitly starts from `main` | Preserve source edits and staging; create from `main`, not the source feature branch; do not automatically stash or copy edits |
| Agent first invoked only after task edits exist | Deliver those edits in their current checkout, apply newly enabled policy to future tasks, and report the current isolation limit; migrate only when explicitly requested |
| Another worktree uses the requested branch, or a target directory is occupied | Avoid forced reuse and overwrite; select a distinct permitted name or report the blocker |
| User requests a purely read-only review, with no preference present | Leave file bytes, index, refs, and worktree registry unchanged; do not ask about or initialize setup |
| Main checkout's instructions cannot be safely updated | Report that repository-wide persistence is blocked; do not claim the preference was saved elsewhere |

The table specifies the contract. Recorded results below identify exercised cases; the other cases remain unexecuted agent evaluations.

## Git primitive smoke scope

Run a temporary repository with a clean `main` baseline and unrelated staged and unstaged changes on a feature branch. Establish `/.worktree/`, create two task worktrees from `main`, and inspect their paths, bases, branch names, and index contents. Confirm that edits and staging in one checkout do not change the other. Confirm Git rejects a second checkout of an occupied branch. Verify both the root ignore rule and an alternative local `.gitignore` containing `*`, including that file's own ignored state. Read the dedicated main-checkout policy from a branch whose committed instructions predate it. Remove temporary fixtures afterward.

This establishes the Git operations underlying the instructions. It does not establish skill selection, question timing, task ownership judgments, correct preference parsing, or race-free simultaneous initialization.

## Recorded results: 2026-11-05

The Git primitive smoke scope passed in a disposable repository. Source checkout files, branch, HEAD, and index bytes were preserved except for intentional setup edits. Separate task indexes and checkout files, explicit `main` ancestry, occupied-branch/path rejection, root and nested ignore behavior, and optional-locks-disabled inspection were checked. The fixture was removed after the run.

One independent agent received the skill and raw fixtures without the scenario table, ADR, expected outcomes, or parent conclusions. It executed three independent requests and one confirmation continuation:

- In an existing host-created task worktree whose committed instructions predated the policy, it read the main checkout's preference, reused the task worktree, copied the dedicated preference section, and edited the requested file without asking again. Parent inspection confirmed the source checkout and its unrelated staged content were byte-for-byte unchanged.
- For a read-only review without a recorded preference, it reported the existing diff. Parent snapshots confirmed unchanged files, index bytes, HEAD, refs, and worktree registry.
- For first use without a preference, it asked the required question before writing. Parent snapshots confirmed no changes while the answer was pending. After an explicit enabled reply, it saved the preference and ignore rule, created a task worktree under the main checkout's `.worktree/` from local `main`, and edited only the task copy. Parent inspection confirmed the main branch and index stayed unchanged, both setup copies matched, and neither checkout staged or committed changes.

These finite runs support the named paths only. They do not establish automatic skill selection, the engineering trigger across all hosts, disabled-choice recording, conflicting-policy handling, unavailable main checkouts, dirty-task migration, remote operations, cross-clone distribution, or simultaneous initialization. Those cases remain specified above where applicable.

### Instruction refinement

The worktree reference groups preference resolution, persistence, checkout selection, and the ready-to-edit check into ordered stages with explicit completion conditions. The skill entry point retains the read-only inspection rule, while setup-only details stay behind its conditional pointer. The combined `wc -w` count of `project-git/SKILL.md` and `references/WORKTREES.md` changed from 1834 to 1464. This describes text size, not measured token savings or model reliability.

A fresh independent agent received the revised skill and three raw fixtures without expected outcomes or this record. Parent inspection confirmed:

- A read-only review preserved file bytes, index bytes, HEAD, refs, and worktree registry. The agent used `GIT_OPTIONAL_LOCKS=0` for Git inspection.
- A repository with a recorded disabled choice continued in its existing checkout without asking again. Only the requested note changed; unrelated staged and unstaged content remained intact.
- A task-specific external creation root and explicit local `main` base produced the requested linked worktree. The agent changed only the task note, preserved the standing `.worktree/` preference, and kept the source checkout's files, index, branch, and HEAD unchanged.

Both revised skills passed format validation. ADR, changed-document links/anchors, bilingual-pair checks, and nine-skill discovery passed. Existing executable files were unchanged, so the preceding 67-test regression result was reused. The finite behavior limits above still apply.
