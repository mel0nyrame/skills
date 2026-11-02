# Clarify for a question that changes the answer

English | [简体中文](clarify.zh.md) · [All guides](../README.md)

`clarify` is useful when you have an idea but have not established the problem you most need to solve. It identifies assumptions, explains which missing information could affect the answer, and asks one decisive question. After your reply, it delivers the solution.

The first output is a question in the conversation. Stage one calls no tools, creates no files, and does not select a solution before checking your intent.

## Decide whether clarification is useful

“I want a personal knowledge base; recommend tools” leaves several important conditions open. Individual versus shared use, collecting material versus retrieving it, and preserving context can lead to different recommendations. A product list alone may not solve the immediate problem.

An explicit request such as “rename this file to usage.md” usually needs direct action. This skill adds a conversational round, so use it when one answer can materially narrow the task.

## Follow one complete round

This teaching example does not claim any knowledge-base product was tested. After installing the collection's Codex plugin, send this request.

```text
$skills:clarify
I want to build a personal knowledge base. Help identify the actual problem
first. Do not recommend products or modify files in the first round.
```

The first reply should cover hidden assumptions, critical information gaps, one common mistake, and one question that determines the next direction. Depending on context, the final question might resemble this example.

```text
Which problem should we solve first, collecting material or finding what you
have already saved?
```

If you answer “I have saved things but cannot remember why I kept them,” the next response should address context, topic organization, and recovering reasons. It should use your answer rather than repeat a generic list of products.

Use `$clarify` standalone or `/skills:clarify` in Claude Code. `$skills:clarify` is this collection's Codex plugin name.

## Understand the file output

| Stage | Visible result | File effects |
| --- | --- | --- |
| First reply | Assumptions, gaps, one mistake, one question | No tools or file changes |
| After your reply | Explanation, recommendation, or plan addressing the original goal | No default output file |
| A separate request to save the answer | A document at your requested path | Written later within your authorization |

Installing or invoking the skill does not automatically create `requirements.md` or a requirements database. If you want a file after clarification, request a path such as `docs/requirements.md` and specify whether the assistant should only document requirements or proceed to implementation.

## Check whether the question helped

Its answer should change the eventual solution. The assistant should not repeat supplied information or disguise several unrelated questions as one. The second reply should visibly use your clarification.

A full proposal, browser task, or created project file during stage one violates this workflow. Another question is reserved for an ambiguity that prevents a correct or safe response. See the [execution instructions](../../skills/thinking/clarify/SKILL.md). For working principles across the entire task, read [karpathy-guidelines](karpathy-guidelines.md).
