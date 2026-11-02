# Repository Guidelines

## Project Structure

- `skills/<category>/<name>/` contains each skill's `SKILL.md`, `agents/openai.yaml`, and optional `references/` or `scripts/`. Categories are `engineering`, `thinking`, `research`, and `knowledge`.
- `docs/<category>/<name>.md` and `<name>.zh.md` are paired usage guides. Project decisions live in `docs/agents/adr/`.
- `.claude-plugin/`, `.codex-plugin/`, and `.agents/plugins/` expose the same skill sources through plugin manifests and marketplaces. Python regression tests live in `tests/`.

## Development and Validation

There is no build step. Run checks from the repository root:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B skills/engineering/decisions/scripts/check_adr.py docs/agents/adr
npx skills@latest add . --list
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

These commands run regression tests, validate active decisions, preview skill discovery without installing, and validate Claude manifests.

## Style and Naming

Write skill instructions in English. Synchronize English and Chinese READMEs and usage guides. Use kebab-case skill names. Update directory names, frontmatter, UI metadata, invocation prompts, and cross-references together.

Follow existing four-space Python and two-space JSON/YAML indentation. Keep `SKILL.md` focused; link conditional details in supporting references. Preserve invocation policies, including `recap`'s explicit-only settings.

## Testing Expectations

Use Python's standard-library `unittest`; name files `tests/test_*.py` and methods `test_*`. Cover executable changes with behavioral regression tests. ADR checker changes must preserve English/Chinese compatibility, invalid-input rejection, and archive exclusions. Documentation edits require link, anchor, and bilingual-pair checks.

Packaging changes must still discover nine bundled skills. Verify actual Claude/Codex discovery in isolated configuration directories; schema validation alone is insufficient.

## Submodules, Decisions, and Licensing

Before changing manifests or submodule policy, read the [packaging decisions](docs/agents/adr/). Maintain affected records with implementation changes.

For releases, follow [the version policy](docs/agents/adr/0003--repository-release-versions.md). Keep both plugin versions equal and tag the merged `main` commit as `vX.Y.Z`.

Keep external `pr` and `context7-mcp` submodules unchecked out under their `update = none` policy. Populating upstream collections can alter recursive discovery. Keep credentials outside repository files. Preserve third-party notices and synchronize original-content license copies with root `LICENSE`.

## Commits and Pull Requests

Use focused commits and follow the [Git naming defaults](skills/engineering/git-ops/references/CONVENTIONS.md) unless explicitly overridden.

Commit, push, and platform publication require explicit authorization. Preserve unrelated staged and unstaged work. PR descriptions should explain behavior, scope, validation actually performed, and remaining limitations. Include representative prompt examples for changed skill behavior and link relevant existing issues.
