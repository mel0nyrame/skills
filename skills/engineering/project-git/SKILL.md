---
name: project-git
description: Use when reviewing a Git working tree, splitting or creating commits, pushing branches, or recording Git delivery. Check changes and validation against repository rules, and execute only the authorized delivery stage. Use the external pr skill for PR/MR titles, descriptions, and publication.
---

# Project Git

Handle the working tree, commits, and pushes within the user's authorization. A commit request does not authorize a push. A push request does not authorize creating or updating a PR/MR or changing an external tracker. Route PR/MR requests to the external [pr skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr). If it is unavailable, report that dependency rather than treating a push as a completed PR/MR.

## Confirm scope

- Read repository and subtree instructions, contribution rules, and Git rules for the current stage. Before drafting commit titles, resolve the project's format and language using [the convention selection rules](references/CONVENTIONS.md#select-conventions).
- Inspect `git status --short --branch`, unstaged changes, and staged changes. Separate this task's changes from other work. Check remotes, upstream tracking, and outgoing commits when a push is requested.
- Identify required validation and existing results. Reuse checks from the current task that still cover the same changes. Run focused checks when evidence is missing or invalidated by later edits. Report only commands actually run and their results.
- For changes to technical prose, confirm that facts and references make sense from the current repository. For lasting engineering decisions, check affected records and their reasons. Use `project-prose` or `project-adr` for deeper review when available. Required repository checks still apply when those skills are absent.

## Create commits

Split changes by intentions that can be explained and reverted independently. Keep tests, lockfiles, and generated files with the source changes they verify or derive from. Use the resolved project naming conventions, with [defaults](references/CONVENTIONS.md) for unspecified aspects. In an ordinary project, switch to a compliant work branch before committing on the default branch. Rename pushed or shared branches only after explicit coordination.

For each logical group:

1. Stage explicit paths or interactive hunks, preserving unrelated changes.
2. Review `git diff --cached --stat` and `git diff --cached`. Confirm one intention and check for sensitive information, debugging leftovers, conflict markers, and accidental artifacts. Verify that the commit title matches the selected format and language.
3. Commit without bypassing hooks. Inspect the commit summary and remaining working tree.

When repository delivery rules require local issues, specifications, or changelogs, commit them with the implementation they describe. Create records for actual delivery needs, rather than solely to hold a link. Read [the recording conventions](references/TRACKER.md) when linking delivery records or external trackers. If the user requested only a commit, report the commit, validation results, and remaining changes, then stop.

## Push

Push only when the user explicitly requests it. Read and follow the repository's pre-push policy. Confirm the remote, target branch, upstream, and outgoing commits. Establish a normal upstream on the first push. Reuse validation that still covers the outgoing diff unless project policy requires another run.

Preserve hooks. Force pushes, history rewrites, and remote ref deletion require explicit authorization matching the target and scope. On failure, leave a recoverable state and report completed actions, sanitized errors, and the smallest repair recommendation.

Use the external `pr` skill for PR/MR descriptions and platform operations. A successful push does not mean a PR/MR has been created.
