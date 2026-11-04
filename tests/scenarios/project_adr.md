# Manual forward scenarios for decision capture

These scenarios exercise agent behavior, separately from `test_check_adr.py`'s structural checks. Run each producer with a fresh context in a temporary project. Give it only the project instructions, supplied skill files, and the task below. Keep generated documents outside this repository. Use another fresh agent for resumption, without the producer's task or conversation.

For the default fixtures, copy the current [project-adr skill](../../skills/engineering/project-adr/SKILL.md) and its resources into `.agents/skills/project-adr/`. Project `AGENTS.md` links that skill and requires related-topic retrieval, discussion-time capture, one topic owner, and truthful lifecycle states. The fixture has no other format or lifecycle rules and no implementation. Authorize documentation only. The partial-implementation fixture also supplies the current [project-engineering skill](../../skills/engineering/project-engineering/SKILL.md).

## Unresolved discussion and a passing suggestion

Task:

```text
We are designing attachment storage for an offline report viewer. Discuss only;
do not implement. Attachments must open without a network. We rejected remote
object storage alone because it cannot meet that requirement. We rejected
attachment BLOBs in the configuration database because snapshots must be below
20 MiB and an attachment can reach 100 MiB. A separate local directory remains
a candidate. Investigating encryption was suggested, not selected. Pause here;
space quotas and cleanup remain for next time. In passing, the icon might
eventually become blue; we have not discussed that idea.
```

Check that one `proposed` topic preserves the constraints, both actual rejection reasons, the pending local-directory candidate, the unselected encryption suggestion, and the next questions. No implementation or separate icon decision should be created. Run the default checker on the produced record.

## Resume without the original conversation

Give a fresh agent only the preceding fixture's current files. Task:

```text
Continue our attachment-storage design. First explain the current conclusion,
previously rejected approaches and reasons, and what remains undecided. Then
ask the next most important question. Discuss only; do not implement.
```

Check that the answer recovers the actual reasons and constraints, distinguishes a candidate from a selection, and leaves encryption unresolved. It must not manufacture implementation evidence or create a duplicate topic. An unchanged record is appropriate when no new conclusion has been reached.

## Autonomous selection with implementation deferred

Task:

```text
Choose the local report-directory format for the next implementation stage:
one JSON manifest for all reports, or one independent JSON manifest per report.
Reports are imported and deleted independently; there are at most 100 reports
and a single local writer. You may make this internal choice. Evaluate and
select an approach, explain tradeoffs and future verification, but do not
implement or claim measured performance today.
```

Either justified choice is valid. Check that its record is `accepted`, identifies the agent's delegated authority, preserves the real alternative and reasons, and separates remaining verification from evidence already obtained. Run the default checker.

## Synchronize partial implementation

Extend the selection fixture with a minimal implementation of the chosen storage shape and a focused passing test. In the recorded run, `catalog.py` uses one JSON file per report and its test verifies importing two reports and deleting one without affecting the other. It lacks schema/version handling, path validation, malformed-entry isolation, quota enforcement, and recovery behavior required by that fixture's record.

Task:

```text
Use project-engineering to inspect the existing record, catalog.py, and its
test. Run the existing test and synchronize documentation with actual progress.
Separate supported evidence from remaining work. Do not change implementation,
add tests, or guarantee unverified behavior.
```

Check that the existing topic gains implementation paths, actual test evidence, and remaining gaps. It stays `accepted` while required implementation is incomplete. A passing focused test alone must not turn it into a fully implemented claim.

## External interview workflow with project conventions

This scenario additionally requires unmodified `grill-with-docs`, `domain-modeling`, and `grilling` skills from outside this collection. Obtain the matching instructions below and place each skill under the temporary fixture's `.agents/skills/<name>/`, retaining the supporting files beside `domain-modeling/SKILL.md`.

The instruction files supplied to the 2026-11-04 run are byte-identical to the corresponding files in [`mattpocock/skills` at `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`](https://github.com/mattpocock/skills/commit/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d). This is a verified reproduction source, not a claim that the original installation came from that commit; the installation ref was not recorded. SHA-256 values were calculated from the retained test copies and their Git blob identities were checked against the pinned upstream files.

| Instruction file at the pinned source | SHA-256 of supplied file |
| --- | --- |
| [grill-with-docs/SKILL.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/grill-with-docs/SKILL.md) | `7de372c13488f1ee96cc11cd8907b56b6809cc93eef776eeddd37de6b6cbe3fe` |
| [domain-modeling/SKILL.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/domain-modeling/SKILL.md) | `7b925d7b1e341a2eeae33ad68a8a8c0ab889a38ddd22a7598e4c240e5a7556a3` |
| [domain-modeling/ADR-FORMAT.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/domain-modeling/ADR-FORMAT.md) | `944c92aa790e8fbdc9199640b170979abb8a34ba8d0fe18c2a01a63bce140ca0` |
| [domain-modeling/GLOSSARY-FORMAT.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/domain-modeling/GLOSSARY-FORMAT.md) | `21dcc40cdec8e151a829b98ab1517c1867bc444e3665134a98c6983411996801` |
| [grilling/SKILL.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/grilling/SKILL.md) | `a146842ed93ca43d833550fa9adf02e58cb63c83fea9d4b4522995b82242d4e2` |

Before rerunning, verify all five instruction hashes. If a required file is missing or differs from the pinned content, record this scenario as `skipped`, state the missing or mismatched dependency, and exclude it from the passed count. Evaluating another version is a separate run that must record its source and hashes. File identity does not fix the model, harness, or execution environment, so it does not guarantee identical agent behavior.

This fixture's project instructions require `design/decisions/<topic>.md`, a title, a `State` field, and one prose paragraph. Its vocabulary is `evaluating`, `chosen`, `shipped`, and `declined`. An existing `backup-target.md` is evaluating local same-disk copies and remote encrypted copies under the constraint that backups survive failure of the working disk.

Task:

```text
Use grill-with-docs to preserve this completed backup decision. Do not restart
the interview or implement. We selected remote encrypted backups so recovery
remains possible after working-disk failure. Same-disk copies were rejected
because they cannot meet that requirement. The provider and key custody remain
open. Complete the design handoff.
```

Check that the same file becomes `State: chosen`, retaining its short project format, actual rejection reason, open issues, and unimplemented boundary. No parallel default ADR directory, forced default status, glossary without resolved terminology, or edits to external skills are needed. The default checker is not applicable to this custom schema.

## Recorded validation boundary

On 2026-11-04, five isolated forward runs met the checks above: four required only this collection's skills, while external-workflow/custom-format reuse also used the external instructions identified above. The original installation ref for those external skills was not recorded; the retained instruction copies match the pinned reproduction source. The historical external run was executed and passed. The `skipped` rule governs reruns with unavailable or mismatched dependencies and does not change that historical result.

This is a finite manual evaluation, not an automated regression harness or evidence of automatic skill selection inside Claude Code or Codex. Report passed, failed, and skipped counts separately. Re-run the relevant scenarios when their owning instructions change.
