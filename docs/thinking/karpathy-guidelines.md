# Karpathy Guidelines and the way an assistant completes work

English | [简体中文](karpathy-guidelines.zh.md) · [All guides](../README.md)

`karpathy-guidelines` adds working principles to an existing task. It asks the assistant to inspect important assumptions, choose an adequate solution, keep changes within scope, and support conclusions with actual checks. Readers should understand what was completed and how far the evidence reaches.

This collection uses a personally maintained adaptation. The [source and license notice](../../skills/thinking/karpathy-guidelines/NOTICE.md) identifies its origins. Inspiration from Andrej Karpathy's ideas does not imply his authorship or endorsement of the collection.

## When explicit invocation helps

Use it when the assistant tends to refactor unrelated modules during a fix or says something is fixed without explaining verification. It also applies to research and writing, where supported findings need separation from unverified inference.

It can accompany a specialized workflow. `project-engineering` establishes project entry points and preserves engineering knowledge; these broader principles help control scope and explanation throughout the work.

## Give it a real task

This duplicate-save problem is a teaching example.

```text
$skills:karpathy-guidelines
Fix duplicate records caused by repeated Save clicks. Establish the trigger
before editing. Follow the existing structure without unrelated refactoring.
Run checks appropriate to the fix and explain actual checks and unverified scope.
Do not commit or push.
```

This uses the collection's Codex plugin. Use `$karpathy-guidelines` standalone or `/skills:karpathy-guidelines` in Claude Code.

## What should change in the process

The assistant first inspects implementation and constraints to locate the duplicate behavior, which could involve the page, retries, or server handling. Insufficient evidence remains uncertainty, not a prematurely declared root cause.

Each edit should trace to the task. Reuse existing capabilities where adequate. A helper script or visualization can be useful when it serves current understanding or verification, but its purpose should be explicit.

The report separates executed tests from behavior inferred by reading code. One passing failure scenario does not establish that every concurrent case is solved.

## Files depend on the original task

There is no fixed output directory or new policy file created by invoking this skill.

| Original task | Possible result |
| --- | --- |
| Code change | Relevant source and test changes, with verification notes |
| Research question | A source-supported answer and remaining evidence gaps |
| Documentation edit | Updated target documents and necessary references |
| A useful chart or interactive explanation | A task-specific artifact or display, at a location determined by the task |

A conversational explanation normally produces no file. This skill does not automatically create `AGENTS.md`, `CLAUDE.md`, or another personal skill.

## Review the outcome

Look for edits that cannot be traced to your request. Check whether the report identifies executed verification and limitations. Important assumptions should have evidence or remain explicitly unknown.

The principles cannot guarantee an error-free model or replace project testing, review, and authorization. Simple requests can receive direct answers without a long plan. The [execution instructions](../../skills/thinking/karpathy-guidelines/SKILL.md) define the guidance.
