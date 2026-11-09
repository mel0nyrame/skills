# Rebuildable forward fixtures

These fixtures supply project inputs for fresh-agent runs. They complement the historical scenario records in this directory. Run from a committed checkout with Python 3 and Git. The helper refuses an existing destination.

## Prepare and identify the inputs

```sh
python3 -B -m scripts.scenario_fixture prepare prose-generated /tmp/skills-prose-run --ref HEAD
python3 -B -m scripts.scenario_fixture check-source /tmp/skills-prose-run
python3 -B -m scripts.scenario_fixture prepare git-review /tmp/skills-git-run --ref HEAD
python3 -B -m scripts.scenario_fixture check-source /tmp/skills-git-run
```

Preparation copies the named fixture and only its selected skill, initializes a local Git repository, and commits the baseline. `.scenario-source.json` records the source commit and SHA-256 of every supplied file. `check-source` compares those hashes with that commit and checks that supplied skill bytes remain unchanged. Authored project outputs may change. Later changes to this collection's HEAD do not invalidate an earlier record. Generated fixture documentation uses UTF-8 and LF on every host.

The source commit must contain these fixtures. In a shallow checkout, fetch the recorded commit before checking historical evidence. Missing or changed dependencies make that attempted run `skipped`; preparation and source validation alone never count as a passed agent scenario.

Give a fresh producer only the prepared project and the task below. Keep the acceptance observations with the evaluator. Record the model/harness, source manifest, actual checks, outcome, and uncovered branches beside the historical runs. Leave outputs outside this repository. These supplied-skill tasks do not measure automatic invocation.

## Generated prose

Producer task:

```text
Rewrite docs/export.md for a new contributor. Remove private review framing and
redundant disclaimers. Verify the contract against implementation and preserve
permissions, limits, error ordering, encoding, and useful reasons. Keep executable
behavior and README unchanged. Do not commit, push, or create a separate report.
```

Acceptance observations: edit the source docstring and regenerate the Markdown; preserve authentication, `export:read`, 100 rows, authentication-before-permission-before-size ordering, UTF-8, and the reason for that ordering. Compare executable ASTs with docstrings removed and compare README bytes with the baseline. Inspect generated output against the source; review meaning rather than keyword count.

## Git review without companion skills

Producer task:

```text
Review the export contract and its decision record before delivery. Report factual
or reference problems and checks actually run. Keep files, staging, and history
unchanged. Do not commit, push, or write to any platform.
```

Acceptance observations: identify the documented 500-row limit, missing permission requirement, UTF-16 claim, and obsolete implementation path. Preserve the valid permission-before-size rationale. Verify no file, staging, history, or platform changes. The fixture supplies `project-git` without `project-prose` or `project-adr`; the review must still check the facts.
