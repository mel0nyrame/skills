# Karpathy Guidelines and the way an assistant completes work

English | [简体中文](karpathy-guidelines.zh.md) · [All guides](../README.md)

`karpathy-guidelines` adds working principles to an existing task. It asks the assistant to inspect important assumptions, choose an adequate solution, keep changes within scope, and support conclusions with actual checks. Readers should understand what was completed and how far the evidence reaches.

This collection uses a personally maintained adaptation. The [source and license notice](../../skills/thinking/karpathy-guidelines/NOTICE.md) identifies its origins. Inspiration from Andrej Karpathy's ideas does not imply his authorship or endorsement of the collection.

## When explicit invocation helps

Use it when the assistant tends to refactor unrelated modules during a fix or says something is fixed without explaining verification. Automatic selection targets consequential tradeoffs, unclear requirements, scope creep, or verification gaps, rather than every explanation or writing task. You can still invoke it explicitly for research and writing, where supported findings need separation from unverified inference.

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

If you or an active workflow request an initial intent check or a no-tools stage, the assistant first uses only the supplied context. It honors any required pause, including `clarify`'s question-and-wait rule, before environmental investigation or independent work. Otherwise, it inspects discoverable facts instead of asking you for them. For this fix, it inspects implementation and constraints to locate the duplicate behavior, which could involve the page, retries, or server handling. Insufficient evidence remains uncertainty, not a prematurely declared root cause. It states material assumptions and tradeoffs and presents a supported default for remaining choices.

Each edit should trace to the task and provide only the minimum sufficient behavior. Reuse existing capabilities where adequate. Avoid speculative features, unrequested configuration, and error handling for impossible cases. A disposable helper script or visualization can serve current understanding or verification without needing a reusable abstraction. Remove residue introduced or made unused by the change; preserve unrelated pre-existing work and dead code unless removal is requested.

The report accounts for each requirement and separates executed tests from behavior inferred by reading code. Compatibility work distinguishes required behavior, accepted limitations, and user-approved deferrals. One passing failure scenario does not establish that every concurrent case is solved.

For agent instructions, use representative fresh-context behavior scenarios when possible; format and link checks do not establish model behavior. Disclose scenarios that were not run. State a plan only when dependencies or verification points need coordination, not merely because a task has several actions. For nontrivial work, briefly identify the deliverable and change boundary without turning advice or planning into implementation.

## Files depend on the original task

There is no fixed output directory or new policy file created by invoking this skill.

| Original task | Possible result |
| --- | --- |
| Code change | Relevant source and test changes, with verification notes |
| Research question | A source-supported answer and remaining evidence gaps |
| Documentation edit | Updated target documents and necessary references |
| A useful chart or interactive explanation | A task-specific artifact or display, at a location determined by the task |

Conversation defaults to text and normally produces no file. Follow the requested format; a useful inline visual is allowed when it fits that format. Creating files, calling services, or using tools requires task authorization, not merely a preference for a format. Advice or planning does not authorize implementation, and HTML must not replace a requested format. This skill does not automatically create `AGENTS.md`, `CLAUDE.md`, or another personal skill.

Within those boundaries, diagrams or images can explain relationships; editable diagrams help with precise technical structure. Interactive HTML can help users change parameters or compare scenarios. An authorized HTML artifact should use only necessary interactions and dependencies, follow workspace placement conventions, and have its key behavior checked. If a format is unavailable, explain the limitation and offer a useful supported alternative. Video production is outside this skill.

Writing uses clarity principles inspired by ASD-STE100 and adapted to the user's language. Preserve necessary facts, conditions, exceptions, and uncertainty. This is not a claim of full compliance; strict vocabulary, tense, and word-count rules apply only when requested and checked against the specification.

## Review the outcome

Look for edits that cannot be traced to your request. Check whether the report identifies executed verification and limitations. Important assumptions should have evidence or remain explicitly unknown.

The principles cannot guarantee an error-free model or replace project testing, review, and authorization. Simple requests can receive direct answers without a long plan. The [execution instructions](../../skills/thinking/karpathy-guidelines/SKILL.md) define the guidance.
