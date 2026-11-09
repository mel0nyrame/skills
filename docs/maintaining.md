# Repository checks and reviews

English | [简体中文](maintaining.zh.md)

## Checks

Run from the repository root with Python 3:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
python3 -B -m scripts.check_docs
python3 -B -m scripts.check_pr_body --body-file /tmp/pr-body.md
```

The [CI workflow](../.github/workflows/tests.yml) runs regression, ADR, and documentation checks on Ubuntu and Windows. PR events also validate the body. Editing the PR title or body reruns its structure check without repeating the full matrix.

The documentation checker reads tracked and unignored Markdown, excluding intentional inputs under `tests/fixtures/`. It checks relative inline and reference-definition targets, local Markdown fragments, duplicate heading slugs, and explicit HTML anchors.

Bilingual pairing covers root `README.md` / `README.zh.md` and every Markdown file under `docs/`. The entire `docs/agents/` subtree is excluded from pairing. Each file in scope needs its language counterpart and a reciprocal link.

Fenced examples, inline code, comments, and remote URLs are excluded from link validation. The checker covers the repository's common Markdown forms; it does not render every Markdown extension, fetch remote links, or establish translation accuracy.

The PR checker requires ordered Summary, Evidence, and Merge Danger sections; a visual in Summary; Before/After values; a one-way or two-way Door; and a one-word Blast Radius. Reviewers assess whether the visual represents the diff and the evidence supports its claims. Follow the [PR guide](engineering/pr.md).

## Review

Read [review standards](../CODING_STANDARDS.md) for semantic changes and bounded tool output. Verify obligations and conditions across the main file, conditional references, metadata, and translations. Use existing tests before claiming a checker behaves differently from its documentation.

Keep large API results and command logs outside the response. Extract the fields needed for the current judgment and expand on failures. A concise projection must retain the reviewed commit and evidence links.

## Forward fixtures

Use [the fixture procedure](../tests/scenarios/README.md) to prepare isolated projects from a committed source version. Source identity is checked against its recorded commit, including historical versions. Record model outcomes separately from preparation and mechanical checks.
