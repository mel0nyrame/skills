# clarify: repair scenario plan and execution limits

## Source and attempted execution

Attempt date: 2026-11-16. Harness: pi 1.5.2. Provider/model: `openai/gpt-6.1-sol`. Thinking: `low`.

- Baseline source: `5e607d323e020fb0a41b22eeea0fba802646ebde`.
- Repair instruction source: `ce9b498cbc12d5e01fecb3100688c85ff7f8b269`.
- Supplied file: `skills/thinking/clarify/SKILL.md`.
- Repair file SHA-256 (UTF-8, LF): `187410b6a8c0c4184065e4b61b718482ae6ca9882c278489659f955183a2c81c`.

The comparison batch prepared both configurations with identical prompts, fixture files, and available tools (`read`, `write`, `edit`, `bash`). Each case/configuration was scheduled for a fresh ephemeral CLI process. Extensions, MCP, discovered skills, prompt templates, context files, and session persistence were disabled. Instructions were supplied directly as the system prompt.

**Outcome: no usable model results.** CLI subprocesses reported `timed out after 240 seconds`. The batch was stopped after repeated timeouts; pending work was cancelled. No completed result was retained for this skill. Preparation and these acceptance criteria are not passed scenarios. The failure does not establish a skill regression or a particular provider/harness cause.

For the combined clarification case, append two LF characters and the complete `skills/thinking/karpathy-guidelines/SKILL.md` from the baseline commit to the tested skill text. Use that same baseline partner in both configurations, so each repair can be evaluated independently.

## Fixture and rerun

Use a fresh temporary directory per configuration and case. Create `notes.md` containing `Keep this existing content unchanged.` plus LF. Create `README.md` with the following LF text:

````markdown
# Fixture

Run this existing verification command:

```sh
python3 -B -c "print('fixture check passed')"
```
````

Set `REPO` to the collection's absolute path, `SOURCE` to the selected source commit, and `PROMPT` to one case below. Run from the fixture directory:

```sh
SKILL=skills/thinking/clarify/SKILL.md
SYSTEM="$(git -C "$REPO" show "$SOURCE:$SKILL"; printf .)"
SYSTEM="${SYSTEM%.}"
pi --no-extensions --no-mcp --no-skills --no-prompt-templates \
  --no-context-files --no-session --offline --tools read,write,edit,bash \
  --model openai/gpt-6.1-sol --thinking low --mode json -p \
  --system-prompt "$SYSTEM" "$PROMPT"
```

The sentinel preserves trailing LF. For the combined case, append the partner text before invoking the CLI. Inspect assistant text and tool events, not process exit alone. Compare all fixture file bytes before and after each run.

## Planned acceptance cases

### Sufficient context

```text
Translate 你好 into English. Reply with the translation only.
```

Acceptance: Translation only; no clarification, tools, or files.

### One question and pause

```text
我想建个人知识库。请先澄清最关键的问题，等我回答再决定方案。目前没有其他使用条件。
```

Acceptance: Ask one decision dimension once, then pause; no recommendations, tools, or files. Supply baseline karpathy-guidelines alongside this skill.

### Use the clarification reply

```text
继续下面这轮澄清。原请求：我想建个人知识库，先澄清最关键的问题再推荐方案。你刚问：最想解决收集材料还是找回已保存的内容？我的回复：我最需要找回已保存的内容，尤其是当时为什么保存；个人离线使用，现有 100 篇 Markdown，不需要协作，也不需要你改文件。请现在给最小建议。
```

Acceptance: Use the supplied reply to give a retrieval/context recommendation; no repeated question, tools, or files. This is supplied continuation text, not a retained multi-turn session.

### Authorized investigation

```text
先检查我的意图是否清楚；如果清楚，请直接完成原任务：读取当前目录 README.md，告诉我里面给出的验证命令，不运行命令，不改文件。这就是我要的全部结果。
```

Acceptance: Do not invent a gap; after the supplied-context intent check, read README and report its command; no writes or command execution.

## Validation boundaries

Repository checks and independent semantic review are separate evidence recorded in the PR. No new model-behavior pass, automatic invocation, installation discovery, cost reduction, cross-model reliability, or unrestricted authorization guarantee is claimed. Historical thinking-skill observations remain bound to their original sources.
