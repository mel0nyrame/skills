# Context7 MCP for documentation-backed code guidance

English | [简体中文](context7-mcp.zh.md) · [All guides](../README.md)

This introduces [Upstash's official Context7 skill](https://github.com/upstash/context7/tree/master/skills/context7-mcp). It helps with libraries, frameworks, APIs, and configuration by retrieving relevant documentation before explaining use. Specific versions and focused questions make that material more useful.

A library can change interfaces between versions. A memory-based example may not reveal which version it assumes. Context7 supplies a documentation step; compilation and tests still belong to the actual project.

## Install the skill and connect the tools

This external skill is not bundled with this collection. Install it separately.

```sh
npx skills@latest add upstash/context7 --skill context7-mcp
```

Select your target agent and configure Context7 MCP using upstream setup instructions. Instructions and a working tool connection are separate prerequisites. This collection's [submodule directory](../../skills/research/context7-mcp) records a pinned upstream repository and remains unchecked out normally; it is not an installed skill.

## Ask a focused question

This Prisma pagination example is instructional and makes no claim about a particular version's API syntax.

```text
$context7-mcp
Establish the Prisma version used by this project. Consult matching official
documentation and explain cursor pagination and ordering requirements. Return
code examples, version evidence, and documentation links in chat without editing
files. State explicitly if matching-version material cannot be found.
```

This is the standalone Codex name from a Skills CLI installation, without this collection's `skills` prefix. Follow upstream naming for an upstream plugin installation.

The assistant identifies the requested library, chooses the appropriate documentation source, and retrieves material relevant to the question. Separate unrelated questions so one search does not spread its results across several topics.

## Expected results and file effects

The example should return an explanation, sample code, and source links in chat. It normally creates no files. Retrieving documentation does not upgrade project dependencies or install an SDK.

A separate request to implement pagination moves the task into project editing. Source files, tests, and configuration then depend on that project's structure. Actual behavior still needs project validation.

You can explicitly request notes at `docs/pagination-notes.md`. That location comes from your request; Context7 has no fixed notes output file.

## Review the evidence

Check that the suggestion identifies the library and version. Follow documentation links to see whether they support the suggested API use. A version mismatch, a similarly named community project, or missing material should remain a stated limitation. Finding an interface cannot establish that your implementation passed runtime tests.

This explanation follows the [official instructions](https://github.com/upstash/context7/blob/master/skills/context7-mcp/SKILL.md) without copying their full body. The first link opens the exact skill directory. On GitHub, the submodule opens the whole pinned repository instead.
