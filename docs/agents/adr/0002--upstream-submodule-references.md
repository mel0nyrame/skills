# Reference external skills with submodules

Status: implemented

Partially supersedes [the packaging decision](0001--categorized-plugin-layout.md) for external-reference representation only. Shared skill sources, categorized directories, and installer manifests remain unchanged.

## Problem

External skill folders should appear as clickable upstream references on GitHub without copying their instructions into this repository. Git submodules point to a whole repository at a fixed commit, while the desired skill lives in a subdirectory. Checking out the whole upstream collection can also expose unrelated skills to recursive discovery.

## Decision

Use standard Git submodules for the external skill references: `skills/engineering/pr`, `skills/engineering/retro`, `skills/engineering/writing-for-agents`, and `skills/research/context7-mcp`. Pin each to a verified upstream commit and set `update = none` in `.gitmodules`. Keep them unchecked out during ordinary collection use. The bilingual usage guides retain exact links to the upstream skill subdirectories.

The `retro` and `writing-for-agents` references reuse `pr`'s upstream repository and pin. Their upstream directories sit in different categories, but this collection places both under `skills/engineering/` to avoid adding a new category.

The gitlinks and `.gitmodules` belong in the Git index together. Adding them does not authorize committing or pushing the collection. Upstream instructions are not stored as parent-repository files.

Human usage guides live in `docs/<category>/<skill>.md` and `<skill>.zh.md`. This repository's own ADRs live in `docs/agents/adr/`, separately from skill source and reader guides.

## Alternatives

- README-only link folders can open exact URLs but do not provide the requested clickable submodule representation.
- A submodule URL containing a GitHub `tree/` subdirectory is not a valid Git repository source. Use the repository URL and keep deep links in guides.
- Normal recursive checkout brings in complete upstream collections and can change local skill discovery. A default no-checkout policy preserves the nine owned install candidates without changing each installer.
- Vendoring upstream instruction bodies makes this repository maintain copies the user wants to reference externally.

## Consequences and risks

GitHub clicks open pinned repository roots, not exact skill subdirectories. Readers use the guides' direct links for those. Normal `git submodule update --init` skips these entries. Explicit checkout overrides can populate upstream trees and affect recursive skill discovery; use a separate upstream checkout when browsing or developing those projects.

When changing a pin, verify the commit exists upstream and check the Git index records mode `160000`. Confirm the Skills CLI still discovers exactly nine bundled skills. Submodule correctness does not establish that an upstream skill has been installed or its service configured.
