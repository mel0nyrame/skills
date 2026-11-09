# Share categorized skills across three installation surfaces

Status: implemented

Partially superseded by [upstream submodule references](0002--upstream-submodule-references.md) for the external-reference representation. The shared layout and installer choice remain active.

## Problem

The collection needs physical categories and one maintained source for each skill. The Skills CLI, Claude Code, and Codex use different discovery and plugin metadata conventions. External skills must remain links rather than copied installation candidates.

## Decision

Keep one copy of each skill under `skills/<category>/<name>/`. Use Claude's manifest paths to list category directories. Use Codex's supported `.codex-plugin/plugin.json` compatibility manifest with `skills: "./skills/"` to retain recursive discovery. Each marketplace exposes one complete plugin. The Skills CLI provides individual skill selection.

The original external-reference choice used README-only directories without a `SKILL.md`. Its replacement is owned by the linked submodule decision. Preserve the bundled Karpathy fork's upstream identity and record licensing separately. English and Chinese READMEs describe the same catalog and installation behavior.

The discovery constraint is based on [Codex's manifest-format dispatch](https://github.com/openai/codex/blob/main/codex-rs/core-plugins/src/loader.rs): the compatibility format uses recursive discovery; the portable Agent Plugins format uses direct-child discovery. [Claude's manifest contract](https://code.claude.com/docs/en/plugins/manifest-reference) permits explicit skill directories.

## Alternatives

- A flat `skills/<name>/` layout with README categories simplifies default discovery but does not provide the requested physical categories.
- Separate plugins per category increase metadata and installation choices without serving the requested single-plugin install.
- Copies or symlinks for each platform create extra maintenance or packaging assumptions. Shared source directories are sufficient.
- A root portable `plugin.json` changes Codex discovery to direct children and would miss categorized skill folders. Adopt it only with verified support for this layout or an explicit layout change.
- Git submodules reference repositories and commits rather than arbitrary upstream subfolders. README links meet the external-reference requirement without fetching extra repositories.

## Consequences and risks

Adding a category requires updating Claude's declared paths. Changing Codex manifest format requires rechecking discovery, not merely renaming a file. Validate that all nine bundled skills are discovered and that the external directories are excluded. Schema validity alone does not establish successful runtime discovery.

MCP guidance depends on separately configured services. Plugin installation does not supply service credentials. PR operations depend on the separately installed upstream `pr` skill and retain explicit authorization boundaries.
