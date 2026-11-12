# Supplied thinking-skill scenarios

## Source and execution

Run date: 2026-11-12. Harness: pi 1.5.2; provider/model: `openai-codex/gpt-6.1-sol`; thinking: `low`. Each case used a separate ephemeral CLI process. The skill's complete text was supplied as the system prompt. Extensions, MCP, discovered skills, prompt templates, context files, tools, and session persistence were disabled.

Committed source: `d7d1c9406770d4a091c6cb184b3dd6cb96ecbe89`.

| Supplied file | SHA-256 of supplied UTF-8 text, LF |
| --- | --- |
| `skills/thinking/clarify/SKILL.md` | `93ec4ad75186461db0ab0d36d088a712da2da57ff5913e2350942402bdfb164f` |
| `skills/thinking/karpathy-guidelines/SKILL.md` | `3f186b42bcf512b1dde5762420f207896c090a860d3fd8946ee33f173d3a380b` |

Reproduce from that source commit, replacing the skill path and task for each case:

```sh
pi --no-extensions --no-mcp --no-skills --no-prompt-templates \
  --no-context-files --no-tools --no-session --thinking low --mode json -p \
  --system-prompt "$(python -c 'from pathlib import Path; print(Path("skills/thinking/clarify/SKILL.md").read_text(encoding="utf-8"), end="")')" \
  'Translate 你好 into English. Reply with the translation only.'
```

Select the recorded model explicitly if the local default differs. Read assistant text from `message_end` events; do not infer results from process exit alone.

## Actual model observations

### Clarify: sufficient context

Task:

```text
Translate 你好 into English. Reply with the translation only.
```

Final-source output: `Hello`. No sufficiency announcement, clarification headings, or question. Passed this supplied-skill scenario.

A baseline run using `5858cfa`'s clarify text also returned `Hello.`. Its supplied-text SHA-256 was `f59640ab456a64def83ca1815cfa4042e690a3213e79638415dcf58d12e3c256`. This case establishes preserved direct-answer behavior, not a demonstrated before/after improvement. The old requirement for a sufficiency announcement was a static instruction burden; this baseline model did not exhibit it.

### Clarify: decision-changing gap

Task:

```text
我想建个人知识库。先帮我澄清最关键的问题，再决定方案。目前没有给你其他使用条件。
```

The first candidate asked the core-purpose question twice, once before options and once after. That run did not satisfy the one-question criterion. Its supplied-text SHA-256 was `9c92fba28667f88a159b073b72cc255f77171bfb3fb303af41dfc8a88a0dc301`.

The final instruction says to ask the question once and state choices as options. The final-source output explained why purpose matters and asked:

> 你最希望它优先帮你解决哪一个具体问题？

It offered retrieval, producing work, learning, and another concrete use case as choices, then ended with “先选最重要的一项即可。” It contained one question, no product recommendation, and no fixed assumption/gap/risk report. Passed the final supplied-skill scenario. This is one observed correction, not an estimated reliability improvement.

### Karpathy: simple explanation

Task:

```text
HTTP 404 是什么意思？用一句话回答。
```

Output:

> HTTP 404 表示服务器找不到你请求的网页或资源。

One sentence, no plan or ceremony. Passed this supplied-skill scenario.

### Karpathy: advice stays advice

Task:

```text
只评审以下方案，不实现，也不创建文件：给个人离线笔记工具增加 PostgreSQL 服务，方便保存约 100 篇 Markdown。已有本地文件保存功能，没有协作需求。请指出主要取舍和最小替代方案。
```

The response advised against PostgreSQL for the stated scope, compared service/backup/synchronization costs, and recommended retaining Markdown files as the source of truth. It proposed search or SQLite only for demonstrated needs. It did not claim implementation or successful runtime tests. Passed the recommendation-and-reporting criterion.

## Fresh-context semantic review

A separate pi process using the same model received the complete actual diff, both current skill bodies, and `CODING_STANDARDS.md`, with no tools or inherited context. It was asked to identify lost obligations, translation inconsistencies, broad triggers, and unsafe completion rules. Actual output: `No findings.` This was a bounded supplied-material review, not an independent model-family evaluation or automatic discovery test.

## Limits

These finite runs do not establish automatic selection, invocation frequency, lower token cost, or reliability across models. No-tools execution cannot establish that an agent with write tools will honor authorization. The clarification follow-up round, compatibility matrices, executable modifications, and installed Claude/Codex discovery were not exercised. Structural and Python checks are separate evidence. Global steering changes are local user configuration, not part of this repository's source or scenario hashes.
