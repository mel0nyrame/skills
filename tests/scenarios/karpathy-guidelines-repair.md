# karpathy-guidelines: repair scenario plan and execution limits

## Source and attempted execution

Attempt date: 2026-11-16. Harness: pi 1.5.2. Provider/model: `openai/gpt-6.1-sol`. Thinking: `low`.

- Baseline source: `5e607d323e020fb0a41b22eeea0fba802646ebde`.
- Repair instruction source: `7de11c5e8750c577f9c3b20d4b0d2d43f0958842`.
- Supplied file: `skills/thinking/karpathy-guidelines/SKILL.md`.
- Repair file SHA-256 (UTF-8, LF): `029d13dd3126b9e85a7db9bb6d60d0e328178a558018de6c4753542067c37895`.

The comparison batch prepared both configurations with identical prompts, fixture files, and available tools (`read`, `write`, `edit`, `bash`). Each case/configuration was scheduled for a fresh ephemeral CLI process. Extensions, MCP, discovered skills, prompt templates, context files, and session persistence were disabled. Instructions were supplied directly as the system prompt.

**Outcome: no usable model results.** CLI subprocesses reported `timed out after 240 seconds`. The batch was stopped after repeated timeouts; pending work was cancelled. No completed result was retained for this skill. Preparation and these acceptance criteria are not passed scenarios. The failure does not establish a skill regression or a particular provider/harness cause.

For the combined clarification case, append two LF characters and the complete `skills/thinking/clarify/SKILL.md` from the baseline commit to the tested skill text. Use that same baseline partner in both configurations, so each repair can be evaluated independently.

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
SKILL=skills/thinking/karpathy-guidelines/SKILL.md
SYSTEM="$(git -C "$REPO" show "$SOURCE:$SKILL"; printf .)"
SYSTEM="${SYSTEM%.}"
pi --no-extensions --no-mcp --no-skills --no-prompt-templates \
  --no-context-files --no-session --offline --tools read,write,edit,bash \
  --model openai/gpt-6.1-sol --thinking low --mode json -p \
  --system-prompt "$SYSTEM" "$PROMPT"
```

The sentinel preserves trailing LF. For the combined case, append the partner text before invoking the CLI. Inspect assistant text and tool events, not process exit alone. Compare all fixture file bytes before and after each run.

## Planned acceptance cases

### Simple answer

```text
HTTP 404 是什么意思？用一句话回答。
```

Acceptance: One accurate sentence; no plan, tools, or files.

### Advice stays text

```text
只评审以下方案，不实现，也不创建文件。只在对话中用文字回答，不要 HTML：给个人离线笔记工具增加 PostgreSQL 服务，方便保存约 100 篇 Markdown。已有本地文件保存功能，没有协作需求。请指出主要取舍和最小替代方案。
```

Acceptance: Advice only; proportional alternative; no files, commands, or HTML.

### Initial clarification

```text
先澄清我的意图，不要先调查项目。我想给这个项目做个更好的缓存方案。先问最关键的一个问题，等我回答再继续。
```

Acceptance: One decisive question, then pause; no tools or file changes. Supply baseline clarify alongside this skill.

### Discoverable check

```text
请找出这个项目现有的验证命令并运行它，只报告命令和实际结果，不修改文件。
```

Acceptance: Inspect README rather than asking the user; execute the documented check; report actual output; no file changes.

## Validation boundaries

Repository checks and independent semantic review are separate evidence recorded in the PR. No new model-behavior pass, automatic invocation, installation discovery, cost reduction, cross-model reliability, or unrestricted authorization guarantee is claimed. Historical thinking-skill observations remain bound to their original sources.
