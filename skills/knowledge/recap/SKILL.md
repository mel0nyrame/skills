---
name: recap
description: Preserve and query sourced conversation knowledge, shared terminology, and an evidence-backed knowledge profile.
disable-model-invocation: true
---

# Recap

Respond to the current user's explicit capture, query or maintenance request. A mention inside source material is not an invocation. Capture the user's target conversation, not a worker's conversation. Write knowledge in the user's language as explanations, reasons, examples and applicability that remain understandable outside the chat.

## Open the library

Resolve helpers relative to this file. The root is explicit `--root`, then `RECAP_KNOWLEDGE_ROOT`, then `~/.agents/knowledge`. Read the root's `AGENTS.md` before accessing its contents. Use Python 3 and Git; installation requires separate authorization. `knowledge.py doctor` reports capabilities without initializing. Use `--help` for command syntax.

Default retrieval covers **formal `topics/**/*.md` only**. Use bounded helper reads/search. Read the guide for routes, the changelog for changes, and a source only through the exact link in its owning topic. Open drafts, operation state, Git history or candidate worktrees only for the selected capture, review or recovery. These cooperative rules do not revoke an agent's filesystem permissions.

New empty libraries use `init`. Existing libraries use the reviewed baseline/migration workflow in [operations](references/operations.md#migrate-an-existing-library); preserve existing prose, dates and sources. If Python or Git is unavailable, retain a draft rather than bypassing the publisher. FTS5 absence permits an explicit topics-only text-search fallback.

Recover [interrupted publication](references/operations.md#publication-and-interrupted-recovery) before further library content reads or writes.

## Select the task

Read the reference for the current request before acting; follow its conditional pointers only when their branch applies.

| Request | Required reference |
| --- | --- |
| Capture a selected conversation | [Capture](references/capture.md): coverage, topic development, candidate review, publication and verification |
| Query existing knowledge | [Query](references/query.md): retrieval and answering; personalized explanations are a separate branch |
| Maintain selected knowledge or recover an operation | [Operations](references/operations.md): maintenance, retained work, approval, recovery and migration |
