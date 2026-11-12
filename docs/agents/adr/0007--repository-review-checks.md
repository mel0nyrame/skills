# Keep repository checks executable and semantic review evidence-based

Status: implemented

## Problem

Documentation checks depended on a temporary script while CI checked Python behavior and ADR structure. Reviewers also confused removal of repeated wording with removal of obligations. Historical forward-test hashes identified supplied instructions but the fixture inputs could not be rebuilt from a checkout.

## Decision

The agent selected repository-owned, standard-library checks under the user's authorization to implement the session retrospective. Extend existing CI with local Markdown and bilingual-pair checks and a PR-body structure check. Keep semantic judgments in review-only standards reached from project instructions.

Provide two small, versioned forward fixtures with a preparation command. Record their source commit and byte hashes. Validate historical evidence against that commit rather than current HEAD. Fixture preparation and identity checks do not establish successful model behavior or automatic invocation.

Use the [shared check runner](../../../scripts/check_repository.py) for local and CI regression, ADR, and documentation validation. It retains CI's `PYTHONUTF8=0` coverage while setting `PYTHONIOENCODING=utf-8` for child processes. A local Windows run without the CI environment produced two subprocess decoding errors; enabling UTF-8 mode passed, but making that the permanent default would remove coverage of locale-dependent defaults. Sharing the existing CI environment avoids that tradeoff and duplicate environment configuration. The runner stops at the first failing check and returns its exit code. PR-body checking remains a separate event-specific job.

The repository's `AGENTS.md` directs decision creation and maintenance to the repository-owned `project-adr` skill so changes use the checked-out rules rather than a potentially stale installed copy. This extends the existing check and decision-maintenance contracts; no selected policy is replaced and no successor record is needed.

The [documentation checker](../../../scripts/check_docs.py), [PR-body checker](../../../scripts/check_pr_body.py), and [fixture helper](../../../scripts/scenario_fixture.py) implement the mechanical checks and input preparation. The existing [CI workflow](../../../.github/workflows/tests.yml) runs documentation checks with regression tests and validates PR bodies on creation, synchronization, and metadata edits. [Review standards](../../../CODING_STANDARDS.md) own semantic judgments and bounded tool output; [maintenance instructions](../../maintaining.md) own command usage and limits.

Existing packaging and decision-capture policies remain active; this topic replaces no prior record.

## Alternatives

- Keep ad hoc temporary checks: rejected because another checkout cannot reuse or maintain them.
- Encode semantic equivalence as text-pattern lint: rejected because equivalent instructions can use different wording and an unchanged phrase can still have a changed condition.
- Require historical evidence to match current HEAD: rejected because it would invalidate accurate records of earlier instruction versions.
- Add another CI platform: rejected because the existing GitHub Actions workflow already runs the repository's checks on Ubuntu and Windows.
- Require local users to remember separate encoding exports: rejected because local checks can diverge from CI and produce avoidable decoding failures.
- Enable UTF-8 mode for all tests: not selected as the shared default because CI deliberately exercises locale-dependent defaults. Explicit UTF-8 standard streams address subprocess output without changing that coverage.

## Consequences and risks

Local checks become reproducible and CI can reject structural mistakes before review. [Checker tests](../../../tests/test_review_checks.py) exercise bad links, anchors, guide pairs, example masking, and invalid PR fields. [Fixture tests](../../../tests/test_scenario_fixture.py) exercise reconstruction, historical source identity, changed instructions, output edits, and existing-destination preservation.

The [runner tests](../../../tests/test_check_repository.py) cover command ordering, interpreter and working-directory selection, environment overrides without parent mutation, early failure, and actual UTF-8 child output with UTF-8 mode disabled. Local Windows validation through `python3 -B -m scripts.check_repository` completed successfully: 105 tests run with 3 skips, 8 active ADRs passed, and 76 Markdown files passed documentation checks. Platform CI results remain separate from this local execution evidence.

Review still establishes truthful claims, retained obligations, and whether a visual explains the diff. Markdown syntax outside the checker's documented scope requires separate inspection. The two fixtures specify narrow supplied-skill tasks; preparation tests do not establish model behavior. Reconsider these checks when repository Markdown forms or the PR template change.
