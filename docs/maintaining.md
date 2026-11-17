# Repository checks and reviews

English | [简体中文](maintaining.zh.md)

## Checks

Run from the repository root with Python 3:

```sh
python3 -B -m scripts.check_repository
python3 -B -m scripts.check_pr_body --body-file /tmp/pr-body.md
```

The [shared runner](../scripts/check_repository.py) runs regression tests, ADR validation, and documentation checks in order, stopping at the first nonzero exit code. It uses the invoking Python interpreter and the repository root as each child process's working directory. Each child receives `PYTHONUTF8=0` and `PYTHONIOENCODING=utf-8`: locale-dependent defaults remain covered while Python standard streams use UTF-8. The parent environment is unchanged. Direct checker commands remain available for focused work but do not set this shared environment automatically.

For a focused iteration, use the same runner to retain the shared encoding environment:

```sh
python3 -B -m scripts.check_repository --test-pattern 'test_check_repository.py'
python3 -B -m scripts.check_repository --test-pattern 'test_recap_workflow.py' --test-name revise --test-name resolve
```

`--test-pattern` passes a test-filename glob to unittest discovery (`-p`). Each `--test-name` passes a case-sensitive name substring or glob (`-k`); repeated names match with OR, within the selected files. ADR and documentation checks still run after the selected tests pass, and any failure still stops later checks. Confirm the reported test count; a mistyped selector may select no tests. A filtered run is not full-suite evidence. Without selectors, the runner and CI retain the full existing sequence. Run the unfiltered command before delivery; allow several minutes rather than terminating a healthy run at a short tool timeout.

The [CI workflow](../.github/workflows/tests.yml) uses the same runner on Ubuntu and Windows. PR events also validate the body. Editing the PR title or body reruns its structure check without repeating the full matrix.

The documentation checker reads tracked and unignored Markdown, excluding intentional inputs under `tests/fixtures/`. It checks relative inline and reference-definition targets, local Markdown fragments, duplicate heading slugs, and explicit HTML anchors.

Bilingual pairing covers root `README.md` / `README.zh.md` and every Markdown file under `docs/`. The entire `docs/agents/` subtree is excluded from pairing. Each file in scope needs its language counterpart and a reciprocal link.

Fenced examples, inline code, comments, and remote URLs are excluded from link validation. The checker covers the repository's common Markdown forms; it does not render every Markdown extension, fetch remote links, or establish translation accuracy.

The PR checker requires ordered Summary, Evidence, and Merge Danger sections; a visual in Summary; Before/After values; a one-way or two-way Door; and a one-word Blast Radius. Reviewers assess whether the visual represents the diff and the evidence supports its claims. Follow the [PR guide](engineering/pr.md).

## Review

Read [review standards](../CODING_STANDARDS.md) for semantic changes and bounded tool output. Verify obligations and conditions across the main file, conditional references, metadata, and translations. Use existing tests before claiming a checker behaves differently from its documentation.

Keep large API results and command logs outside the response. Extract the fields needed for the current judgment and expand on failures. A concise projection must retain the reviewed commit and evidence links.

## Forward fixtures

Use [the fixture procedure](../tests/scenarios/README.md) to prepare isolated projects from a committed source version. Source identity is checked against its recorded commit, including historical versions. Record model outcomes separately from preparation and mechanical checks.
