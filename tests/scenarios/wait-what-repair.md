# wait-what: repair scenario plan and execution limits

## Source and attempted execution

Attempt date: 2026-11-16. Harness: pi 1.5.2. Provider/model: `openai/gpt-6.1-sol`. Thinking: `low`.

- Baseline source: `5e607d323e020fb0a41b22eeea0fba802646ebde`.
- Repair instruction source: `bef467f1fccb6607a9a7bf563deb351d180b9670`.
- Supplied file: `skills/thinking/wait-what/SKILL.md`.
- Repair file SHA-256 (UTF-8, LF): `151d7bd5ffed1f85c7c399aa37eee4ebb299f334c550883e085ffb68804ce871`.

The comparison batch prepared both configurations with identical prompts, fixture files, and available tools (`read`, `write`, `edit`, `bash`). Each case/configuration was scheduled for a fresh ephemeral CLI process. Extensions, MCP, discovered skills, prompt templates, context files, and session persistence were disabled. Instructions were supplied directly as the system prompt.

**Outcome: no usable model results.** CLI subprocesses reported `timed out after 240 seconds`. The batch was stopped after repeated timeouts; pending work was cancelled. No completed result was retained for this skill. Preparation and these acceptance criteria are not passed scenarios. The failure does not establish a skill regression or a particular provider/harness cause.

The no-previous-content case has only the `$wait-what` user message; the other cases supply the prior statement in the prompt, not in retained session history.

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
SKILL=skills/thinking/wait-what/SKILL.md
SYSTEM="$(git -C "$REPO" show "$SOURCE:$SKILL"; printf .)"
SYSTEM="${SYSTEM%.}"
pi --no-extensions --no-mcp --no-skills --no-prompt-templates \
  --no-context-files --no-session --offline --tools read,write,edit,bash \
  --model openai/gpt-6.1-sol --thinking low --mode json -p \
  --system-prompt "$SYSTEM" "$PROMPT"
```

The sentinel preserves trailing LF. For the combined case, append the partner text before invoking the CLI. Inspect assistant text and tool events, not process exit alone. Compare all fixture file bytes before and after each run.

## Planned acceptance cases

### Missing connection

```text
上一条解释是：“删除缓存后，下次读取会得到新结果。”我没明白删除缓存怎么导致新结果。请用中文补上中间的联系，最多三句话，只在对话中回答。
```

Acceptance: Explain the cache miss and recomputation/retrieval conditions; at most three sentences; no tools or files.

### Correct a false claim

```text
你上一条说：“HTTP 404 表示服务器内部错误，所以应该重启服务器。”等等，我没明白。请重新解释，保持简短，只在对话中回答。
```

Acceptance: Correct 404 versus 500 and retract the unsupported restart conclusion; no tools or files.

### No previous content

```text
$wait-what
```

Acceptance: Ask which explanation/text to re-explain; do not invent a prior response; no tools or files.

### Format and evidence

```text
上一条说：“没有做行为测试，但链接检查通过，所以已经证明修改后的 skill 在所有模型上可靠。”我没明白。请用中文两条列表重新说明，只在对话里回答，不创建 HTML 或其他文件，也不要执行命令。
```

Acceptance: Correct the unsupported inference: link checks establish structure, not model reliability; exactly two bullets; no tools or files.

## Validation boundaries

Repository checks and independent semantic review are separate evidence recorded in the PR. No new model-behavior pass, automatic invocation, installation discovery, cost reduction, cross-model reliability, or unrestricted authorization guarantee is claimed. Historical thinking-skill observations remain bound to their original sources.
