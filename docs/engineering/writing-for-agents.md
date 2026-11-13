# Writing for agents

English | [简体中文](writing-for-agents.zh.md) · [All guides](../README.md)

This introduces [Matt Pocock's upstream writing-for-agents skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents). It guides documents written for agents: skills, `AGENTS.md`, `CLAUDE.md`, and similar instruction files. It favors context pointers, an information hierarchy, explicit completion criteria, and pruning over long prose.

The upstream directory lives under `skills/productivity/`. This collection keeps its [submodule](../../skills/engineering/writing-for-agents) under `skills/engineering/` to avoid adding a new category. The link above opens the exact upstream directory.

## Install the skill

This external skill is not bundled with this collection. Install it separately.

```sh
npx skills@latest add mattpocock/skills --skill writing-for-agents
```

Select your target agent and use upstream naming for the invocation. The submodule records a pinned upstream repository and remains unchecked out normally; it is not an installed skill. When this skill is used to write a skill, it reads its own `SKILL-MECHANICS.md` for the detailed rules.

## Ask for a document edit

```text
$writing-for-agents
Rewrite the completion criteria in this skill's SKILL.md. Keep the existing
scope and invocation policy. Replace vague instructions with observable checks,
remove duplicated caveats, and report what you removed. Do not publish or commit.
```

This is an instructional example. Name the file, the intended behavior, and the parts that must stay unchanged.

## Expected results and file effects

The example should return a revised document or a read-only review, depending on your request. It normally creates no files unless you name a save location. The skill supplies writing rules; it does not install services, run a project's test suite, or authorize Git delivery.

The [retro guide](retro.md) calls this skill for its writing style guide. Install both when you plan to use retro.

## Review the result

Check that every instruction has a clear action, object, and completion condition. Confirm required limits, exceptions, and invocation policies remain. A shorter document is not automatically correct if it drops a condition.

See the [upstream instructions](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md) and [third-party notices](../../THIRD_PARTY_NOTICES.md) for original rules and attribution. This guide does not store a copy of the upstream instruction body.
