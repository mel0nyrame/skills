# Skills

Personal agent skills for engineering, clarification, research, and knowledge capture. Install individual skills with the Skills CLI or the complete collection as one Claude Code or Codex plugin. All three installation surfaces use the same source files.

English | [简体中文](README.zh.md)

New to the collection? Start with the [usage guides](docs/README.md) for purposes, examples, and limits.

## Catalog

### Engineering

| Skill | Purpose |
| --- | --- |
| [project-engineering](docs/engineering/project-engineering.md) | Implement changes, preserve engineering knowledge, and maintain affected decisions. |
| [project-adr](docs/engineering/project-adr.md) | Capture durable design discussions and maintain choices, rejection reasons, lifecycle, and replacement links. |
| [project-git](docs/engineering/project-git.md) | Review working trees, split commits, and push within user authorization. |
| [project-prose](docs/engineering/project-prose.md) | Write and review self-contained technical prose with complete contracts. |
| [pr ↗](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr) | External recommendation: Matt Pocock's upstream PR skill. [Usage guide](docs/engineering/pr.md) · [Submodule](skills/engineering/pr). |
| [retro ↗](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro) | External recommendation: Matt Pocock's upstream retrospective skill. [Usage guide](docs/engineering/retro.md) · [Submodule](skills/engineering/retro). |
| [writing-for-agents ↗](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) | External recommendation: Matt Pocock's upstream skill for agent-facing documents. [Usage guide](docs/engineering/writing-for-agents.md) · [Submodule](skills/engineering/writing-for-agents). |

The four `project-*` skills form a project-engineering suite: implementation and knowledge maintenance, durable decisions, Git delivery, and technical prose. Each can also be used independently.

### Thinking

| Skill | Purpose |
| --- | --- |
| [clarify](docs/thinking/clarify.md) | Check assumptions, ask one decisive question when needed, or answer directly when context is sufficient. |
| [karpathy-guidelines](docs/thinking/karpathy-guidelines.md) | Keep work focused, verify results, and make outcomes understandable. Maintained fork. |

### Research

| Skill | Purpose |
| --- | --- |
| [firecrawl-mcp](docs/research/firecrawl-mcp.md) | Search, verify, extract, and interact with web sources through Firecrawl MCP. |
| [tinyfish-mcp](docs/research/tinyfish-mcp.md) | Automate web tasks through TinyFish MCP. |
| [context7-mcp ↗](https://github.com/upstash/context7/tree/master/skills/context7-mcp) | External recommendation: Upstash's official Context7 skill. [Usage guide](docs/research/context7-mcp.md) · [Submodule](skills/research/context7-mcp). |

### Knowledge

| Skill | Purpose |
| --- | --- |
| [recap](docs/knowledge/recap.md) | Turn conversations into reusable, traceable topic knowledge. Explicit invocation only. |

The package contains **nine installable skills**. `pr`, `retro`, `writing-for-agents`, and `context7-mcp` are upstream Git submodules left unchecked out by default. They are excluded from the plugin and Skills CLI skill inventory. Their guides provide exact upstream links and separate installation instructions.

## Install

The GitHub commands require this repository to be published at `mel0nyrame/skills`. Use the local-checkout instructions before publication. Choose one installation surface per agent to avoid duplicate copies.

### Skills CLI

Select skills and target agents interactively:

```sh
npx skills@latest add mel0nyrame/skills
```

Install one skill, or inspect the catalog without installing:

```sh
npx skills@latest add mel0nyrame/skills --skill clarify
npx skills@latest add mel0nyrame/skills --list
```

### Claude Code plugin

Run inside Claude Code:

```text
/plugin marketplace add mel0nyrame/skills
/plugin install skills@mel0nyrame-skills
```

The terminal equivalents are `claude plugin marketplace add mel0nyrame/skills` and `claude plugin install skills@mel0nyrame-skills`. Start a new session after installation. Plugin skills use the `skills` namespace, for example `/skills:clarify`.

### Codex plugin

Add the marketplace:

```sh
codex plugin marketplace add mel0nyrame/skills
```

Open Codex, run `/plugins`, and install `skills` from `mel0nyrame-skills`. If your CLI exposes `codex plugin add --help`, you can install directly:

```sh
codex plugin add skills@mel0nyrame-skills
```

The direct CLI command is verified with `codex-cli 0.166.0-alpha.5.1`; availability depends on your version. Start a new session. Plugin skills use the `skills` namespace, such as `$skills:clarify` and `$skills:project-engineering`. A standalone Skills CLI installation uses `$clarify` and `$project-engineering`.

### Local checkout

Run these commands from the repository root. Each install writes to the selected agent's normal configuration.

```sh
# Skills CLI: inspect, then select skills and target agents.
npx skills@latest add . --list
npx skills@latest add .

# Claude Code: register this checkout, then install the plugin.
claude plugin marketplace add .
claude plugin install skills@mel0nyrame-skills

# Codex: register this checkout; install from /plugins or the CLI when available.
codex plugin marketplace add .
codex plugin add skills@mel0nyrame-skills
```

## Behavior and dependencies

- `clarify` asks one decisive question and waits when a key gap remains. When the supplied context is sufficient, it answers in the same reply.
- `recap` is explicitly invoked. It preserves both `disable-model-invocation: true` and the Codex implicit-invocation opt-out.
- `project-git` keeps separate authorization for commits, pushes, and PR/MR operations. It checks project rules and consistent structured commit history before falling back to Chinese commit descriptions. Explicit task instructions take precedence.
- `project-adr` follows project conventions first. Its default checker accepts complete English and Chinese schemas and preserves archive exclusions.
- `project-engineering` and `project-git` use the separately installed upstream `pr` skill for PR/MR descriptions. They report its absence rather than silently installing it.
- Firecrawl and TinyFish guidance requires the corresponding MCP server to be configured separately. This package provides skills and dependency metadata; it does not bundle server configuration or credentials.

## Maintain

### Releases and versions

`main` is the release branch. Keep development on feature branches, update both plugin manifest versions in a release PR, and create the matching `vX.Y.Z` tag on the merged `main` commit. One tag identifies the complete collection; individual skills are not versioned separately. For example, tag `v0.1.0` corresponds to `version: "0.1.0"` in both plugin manifests.

`skills@latest` selects the installer version. The default installation command reads this repository's default branch, not its newest tag. To select a published historical release explicitly, use a tagged source.

```sh
npx skills@latest add https://github.com/mel0nyrame/skills/tree/v0.1.0
```

Keep published tags fixed. Existing installations need a separate update with `npx skills@latest check` and `npx skills@latest update`. See [the release decision](docs/agents/adr/0003--repository-release-versions.md) before changing this policy.

### Repository upkeep

The upstream submodules use `update = none`. Normal initialization leaves them unchecked out; a leading `-` in `git submodule status` is expected. Explicitly populating those directories can expose unrelated upstream skills to recursive discovery. Use their separate installation instructions for the desired skill. The [submodule decision](docs/agents/adr/0002--upstream-submodule-references.md) explains this boundary.

Keep instructions in English. Keep this README and [README.zh.md](README.zh.md) synchronized. Give each skill one source directory. When changing names, update frontmatter, UI metadata, prompts, and cross-skill references together. Adding a category also requires updating Claude's skill paths.

Human usage guides live in `docs/<category>/<skill>.md` with a matching `<skill>.zh.md`. Keep both languages aligned with the owning `SKILL.md`; they explain use rather than define a second execution workflow. Project ADRs live in `docs/agents/adr/`.

Keep Codex's compatibility manifest unless a replacement has been verified to discover categorized skills. See [the packaging decision](docs/agents/adr/0001--categorized-plugin-layout.md) for the discovery constraint and alternatives. Update that record when its decision or supporting facts change. Keep third-party provenance and notices with imported content. The root `LICENSE` owns the license text for original contributions; keep the copies in those skill directories synchronized so standalone installations carry the notice. Karpathy's own license and source notice remain with that skill.

Run focused checks from the repository root:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
npx skills@latest add . --list
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

For packaging changes, also check actual skill discovery in an isolated Claude/Codex installation. A valid manifest alone does not establish that all nine skills load. Remote GitHub installation requires a published repository and separate verification.

Installation contracts: [Skills CLI](https://github.com/vercel-labs/skills), [Claude plugins](https://code.claude.com/docs/en/plugins), [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins).

## License and sources

MIT for mel0nyrame's contributions. The bundled Karpathy fork retains its upstream MIT declaration and attribution. External recommendations remain under their upstream licenses. See [LICENSE](LICENSE), [third-party notices](THIRD_PARTY_NOTICES.md), and [the Karpathy license](skills/thinking/karpathy-guidelines/LICENSE).
