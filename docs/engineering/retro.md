# Retro for reviewing a coding session

English | [简体中文](retro.zh.md) · [All guides](../README.md)

This introduces [Matt Pocock's upstream retro skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro). It reviews a coding session's agent environment and proposes ranked improvements. It does not edit the code under review.

The skill runs only when you explicitly invoke it. It inspects navigation, automated checks, coding standards, global `AGENTS.md`, tool economy, no-ops, and information access. It then offers candidates by severity for you to choose from.

## Install the skill and its writing reference

This external skill is not bundled with this collection. Install it separately.

```sh
npx skills@latest add mattpocock/skills --skill retro
```

Its first step calls the upstream `writing-for-agents` skill for a writing style guide. Install that skill too so the reference resolves:

```sh
npx skills@latest add mattpocock/skills --skill writing-for-agents
```

Select Codex for the standalone `$retro` invocation. This collection's [submodule](../../skills/engineering/retro) is an upstream reference, not evidence of installation.

## Request an inspectable review

```text
$retro
Review the agent environment from this session. Group your findings by the
categories you checked, rank the candidates by severity, and explain why each
matters. Only propose changes; do not edit files, commit, or push.
```

This is an instructional example. Replace the scope with the session you actually want reviewed.

## Deliverables and acceptance

| Your request | Expected artifact |
| --- | --- |
| Explicit `$retro` review | Ranked suggestions in the conversation |
| Explicitly save notes | That local file, reopened to verify the save |
| Apply a suggestion | A separate, explicitly authorized implementation request |

Read the suggestions as someone absent from the session. Each should name the observed problem, its category, and the proposed change. No file should change unless you separately authorize it.

See the [writing-for-agents guide](writing-for-agents.md) for the companion skill, the [upstream instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md) for original rules, and [third-party notices](../../THIRD_PARTY_NOTICES.md) for attribution. This guide does not store a copy of the upstream instruction body.
