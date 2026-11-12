# Clarify for a question that changes the answer

English | [简体中文](clarify.zh.md) · [All guides](../README.md)

`clarify` is useful when you have an idea but have not established the problem you most need to solve. Select it when you want to clarify intent or stress-test the question before receiving a substantive answer. It identifies assumptions and missing information that could affect the answer. If a key gap remains, it asks one decisive question and delivers the solution after your reply.

The initial intent check uses the supplied context without tools or file changes. When a decision-changing gap remains, the first output asks one question and waits. When the context is sufficient, the assistant answers directly in the same reply, without a sufficiency announcement or clarification headings.

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

When clarification is needed, the first reply briefly explains the missing condition and asks one question that determines the next direction. It includes an assumption or risk only when that helps you answer; a fixed multi-section report is unnecessary. Depending on context, the final question might resemble this example.

```text
Which problem should we solve first, collecting material or finding what you
have already saved?
```

If you answer “I have saved things but cannot remember why I kept them,” the next response should address context, topic organization, and recovering reasons. It should use your answer rather than repeat a generic list of products.

Use `$clarify` standalone or `/skills:clarify` in Claude Code. `$skills:clarify` is this collection's Codex plugin name.

## Understand the file output

| Stage | Visible result | File effects |
| --- | --- | --- |
| A key gap remains | A short explanation and one decisive question; relevant assumptions or risks only as needed | No tools or file changes |
| Context is sufficient | The answer directly, without clarification framing | No default output file; later actions follow the task's authorization |
| After your reply | Explanation, recommendation, or plan addressing the original goal | No default output file |
| A separate request to save the answer | A document at your requested path | Written later within your authorization |

Installing or invoking the skill does not automatically create `requirements.md` or a requirements database. If you want a file after clarification, request a path such as `docs/requirements.md` and specify whether the assistant should only document requirements or proceed to implementation.

## Check whether the question helped

Its answer should change the eventual solution. The assistant should not repeat supplied information or disguise several unrelated questions as one. The second reply should visibly use your clarification.

A full proposal, browser task, or created project file while waiting for a necessary clarification violates this workflow. When the context is sufficient, the assistant should proceed without inventing a gap or mistake. Another question is reserved for an ambiguity that prevents a correct or safe response. See the [execution instructions](../../skills/thinking/clarify/SKILL.md). For working principles across the entire task, read [karpathy-guidelines](karpathy-guidelines.md).
