# Repository Guidelines

## Project Structure

- `skills/<category>/<name>/` contains each skill's `SKILL.md`, `agents/openai.yaml`, and optional `references/` or `scripts/`. Categories are `engineering`, `thinking`, `research`, and `knowledge`.
- `docs/<category>/<name>.md` and `<name>.zh.md` are paired usage guides. Project decisions live in `docs/agents/adr/`.
- `.claude-plugin/`, `.codex-plugin/`, and `.agents/plugins/` expose the same skill sources through plugin manifests and marketplaces. Python regression tests live in `tests/`.

## Development and Validation

There is no build step. Run checks from the repository root:

```sh
python3 -B -m scripts.check_repository
npx skills@latest add . --list
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

These commands run regression tests, validate active decisions and documentation, preview skill discovery without installing, and validate Claude manifests. See [maintenance checks](docs/maintaining.md) for PR-body and forward-fixture commands.

## Style and Naming

Write skill instructions in English. Synchronize English and Chinese READMEs and usage guides. Use kebab-case skill names. Update directory names, frontmatter, UI metadata, invocation prompts, and cross-references together.

Follow existing four-space Python and two-space JSON/YAML indentation. Keep `SKILL.md` focused; link conditional details in supporting references. Preserve invocation policies, including `recap`'s explicit-only settings.

## Testing Expectations

Use Python's standard-library `unittest`; name files `tests/test_*.py` and methods `test_*`. Cover executable changes with behavioral regression tests. ADR checker changes must preserve English/Chinese compatibility, invalid-input rejection, and archive exclusions. Documentation edits require link, anchor, and bilingual-pair checks.

Packaging changes must still discover ten bundled skills. Verify actual Claude/Codex discovery in isolated configuration directories; schema validation alone is insufficient.

## Decision Maintenance

Use this repository's [project-adr skill](skills/engineering/project-adr/SKILL.md) when creating or maintaining decision records, rather than an installed copy. Before proposing or implementing related work, search active decisions and read relevant proposals, choices, rejection reasons, and open questions. During discussion, preserve durable constraints, evaluated alternatives, and substantial proposals in the existing topic owner. Checkpoint progress before pausing, distinguish selection from implementation, and synchronize records as implementation changes. Follow the [decision rules](docs/agents/adr/README.md) for creation criteria, lifecycle, and checks.

## Submodules, Decisions, and Licensing

Before changing manifests or submodule policy, read the [packaging decisions](docs/agents/adr/). Maintain affected records with implementation changes.

For releases, follow [the version policy](docs/agents/adr/0003--repository-release-versions.md). Keep both plugin versions equal and tag the merged `main` commit as `vX.Y.Z`.

Keep external upstream submodules unchecked out under their `update = none` policy. Populating upstream collections can alter recursive discovery. Keep credentials outside repository files. Preserve third-party notices and synchronize original-content license copies with root `LICENSE`.

## Commits and Pull Requests

For reviews, read [review standards](CODING_STANDARDS.md).

Use focused commits and follow the [Git naming defaults](skills/engineering/project-git/references/CONVENTIONS.md) unless explicitly overridden.

Commit, push, and platform publication require explicit authorization. Preserve unrelated staged and unstaged work. PR descriptions should explain behavior, scope, validation actually performed, and remaining limitations. Include representative prompt examples for changed skill behavior and link relevant existing issues.

## Parallel Worktree Preference

- Enabled for this repository. Reuse this task's worktree or create an isolated worktree before implementation.
- Default location: the primary worktree's `.worktree/` directory. Honor an explicit task location.
- Preserve existing changes and task worktrees. Reuse this preference without asking again.
