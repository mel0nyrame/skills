# Keep repository checks executable and semantic review evidence-based

Status: implemented

## Problem

Documentation checks depended on a temporary script while CI checked Python behavior and ADR structure. Reviewers also confused removal of repeated wording with removal of obligations. Historical forward-test hashes identified supplied instructions but the fixture inputs could not be rebuilt from a checkout.

## Decision

The agent selected repository-owned, standard-library checks under the user's authorization to implement the session retrospective. Extend existing CI with local Markdown and bilingual-pair checks and a PR-body structure check. Keep semantic judgments in review-only standards reached from project instructions.

Provide two small, versioned forward fixtures with a preparation command. Record their source commit and byte hashes. Validate historical evidence against that commit rather than current HEAD. Fixture preparation and identity checks do not establish successful model behavior or automatic invocation.

The [documentation checker](../../../scripts/check_docs.py), [PR-body checker](../../../scripts/check_pr_body.py), and [fixture helper](../../../scripts/scenario_fixture.py) implement the mechanical checks and input preparation. The existing [CI workflow](../../../.github/workflows/tests.yml) runs documentation checks with regression tests and validates PR bodies on creation, synchronization, and metadata edits. [Review standards](../../../CODING_STANDARDS.md) own semantic judgments and bounded tool output; [maintenance instructions](../../maintaining.md) own command usage and limits.

Existing packaging and decision-capture policies remain active; this topic replaces no prior record.

## Alternatives

- Keep ad hoc temporary checks: rejected because another checkout cannot reuse or maintain them.
- Encode semantic equivalence as text-pattern lint: rejected because equivalent instructions can use different wording and an unchanged phrase can still have a changed condition.
- Require historical evidence to match current HEAD: rejected because it would invalidate accurate records of earlier instruction versions.
- Add another CI platform: rejected because the existing GitHub Actions workflow already runs the repository's checks on Ubuntu and Windows.

## Consequences and risks

Local checks become reproducible and CI can reject structural mistakes before review. [Checker tests](../../../tests/test_review_checks.py) exercise bad links, anchors, guide pairs, example masking, and invalid PR fields. [Fixture tests](../../../tests/test_scenario_fixture.py) exercise reconstruction, historical source identity, changed instructions, output edits, and existing-destination preservation.

Review still establishes truthful claims, retained obligations, and whether a visual explains the diff. Markdown syntax outside the checker's documented scope requires separate inspection. The two fixtures specify narrow supplied-skill tasks; preparation tests do not establish model behavior. Reconsider these checks when repository Markdown forms or the PR template change.
