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

## Replace a selected but unimplemented choice

Provide a default-format `docs/adr/0001--backup-target.md` with `Status: accepted`. It selects encrypted remote backup because backups must survive failure of the working disk. Its alternatives reject same-disk copies for that reason. No implementation exists. The project has no custom replacement rules.

Task:

```text
Our backup policy now requires all backup copies to remain offline. Replace the
selected encrypted remote service with encrypted removable drives kept at a
separate site. This is the selected approach, not a request to compare options.
Preserve why we originally chose remote backup and why same-disk copies failed.
Record the new choice and the changed condition. Key custody and rotation are
still open. Do not implement or delete the original record.
```

Check that a linked successor is `accepted`, the predecessor is `superseded`, and both replacement directions are explicit. Preserve the original choice and reasons. The successor must state the offline constraint, selected removable-drive approach, open questions, and lack of implementation. Merely reopening evaluation without selecting a replacement must not cause supersession. Run the default checker.

## Refresh discovery after a new constraint

Prepare an existing implemented decision about the `runtime_state/` namespace. It requires that namespace to be reconstructed from startup inputs and forbids treating it as authoritative storage. First ask the producer to record a proposal for a user preference file without specifying a path. Keep the same producer for a second turn:

```text
The preference file will be runtime_state/profile.json. User edits must survive
restarts. Reuse the proposal and continue the design; do not implement yet.
```

Check that the producer refreshes relevant-record discovery for the new path and persistence constraint, reads the namespace decision, and preserves the conflict or a justified compatible approach in the existing proposal. The unchanged high-level task scope must not prevent retrieval. Reading all records in the first turn also satisfies retrieval, but does not independently demonstrate second-turn search refresh; report that limitation.

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

### 2026-11-05 review-follow-up run

Seven scenarios passed, none failed, and none were skipped. Producers used fresh independent agent contexts with only the supplied fixture files and task. Resumption used another fresh agent. The discovery-refresh case retained its producer for the second turn. The partial-implementation case used the selected record plus a small storage prototype and one existing test. Outputs were inspected against the checks above; the default checker passed for the default-format fixtures. The custom-format external fixture used a targeted format/content check instead.

| Scenario | Observed result |
| --- | --- |
| Unresolved discussion | One `proposed` record retained both rejection reasons, the local-directory candidate, encryption uncertainty, and quota/cleanup questions; no icon record. |
| Resume without the conversation | A fresh agent recovered the real constraints and rejected approaches, kept encryption unselected, and asked a cleanup-boundary question without duplicating the record. |
| Autonomous selection | The agent selected per-report manifests under delegated authority, recorded `accepted`, and left implementation and measured performance unclaimed. |
| Partial implementation | The existing import/delete test passed; the same record remained `accepted` and distinguished that narrow evidence from missing schema, validation, quota, isolation, and recovery behavior. |
| Selected-choice replacement | The unimplemented predecessor became `superseded`; a successor was `accepted`. Both links, the original rationale, changed offline constraint, and remaining key-management questions were preserved. |
| Discovery refresh | The second turn repeated discovery for `runtime_state/profile.json` and persistence terms, retained the same proposal, and exposed the conflict with startup replacement. |
| External custom format | The existing `design/decisions/backup-target.md` became `State: chosen`, retained one prose paragraph and real rejection reasons, and created no parallel ADR system or glossary. |

The discovery producer had already read the runtime-state record in its first turn. The second turn demonstrates renewed search and correct use of a known record; it does not independently demonstrate finding a previously unread record. No broader retrieval-recall claim follows from this case.

The evaluated `project-adr` instruction hashes are below. These identify the supplied content, not a fixed model or execution environment:

| File | SHA-256 |
| --- | --- |
| `SKILL.md` | `e8b8d60ef24c2e243120aff304f24c484fc91ae7318a708c4c152db35c357bbc` |
| `references/DISCUSSIONS.md` | `2d88da1d8805bdca1de0b87e012d7c3c2bc8b17f6f76041010decc9d03df7c58` |
| `references/LIFECYCLE.md` | `4a1cf3c1cc515abfe60d1456fbd66c310282a5128501511ffa7c9756674b3df7` |
| `references/PROJECT-INTEGRATION.md` | `d1987f9f5074ffacbbd995480d986fe9edb759178ae64ab6533dba81254a1165` |

The partial-implementation fixture also used `project-engineering/SKILL.md` with SHA-256 `75c8cafddcfa6ae50301c882c077920925e4f75fe576301b0b3794eaf29fd2f0`, including the explicit project-rule-precedence clarification. This is a joint fixture using both supplied skills, not an isolated evaluation of either installation. For the external scenario, all five files were retrieved from the pinned reproduction source above and matched its recorded hashes before execution. Fixture directories were not Git repositories; Git status checks were unavailable. No implementation changes by the evaluated agents, real knowledge-library writes, commits, pushes, or external messages were performed.

### 2026-11-09 instruction-refactor run

Four forward scenarios passed with the revised skill in isolated Git fixtures. Each producer received only its project, supplied instructions, and a realistic request; resumption used a separate fresh agent. The parent inspected outputs against the scenarios above.

| Scenario | Observed result |
| --- | --- |
| Unresolved attachment storage | One `proposed` topic retained offline access, the 20 MiB snapshot bound, a possible 100 MiB attachment, both rejection reasons, the pending local directory, unselected encryption, and quota/cleanup questions. No icon record or implementation. |
| Resume from files | A fresh agent recovered those conclusions and reasons, kept the choice unresolved, and asked about the duration of the offline guarantee. No duplicate topic. |
| Replace an accepted choice | The unimplemented remote-backup predecessor became `superseded`; a linked removable-drive successor was `accepted`. Offline-policy change, original reasons, and open key questions were preserved. |
| Custom format | The existing single-paragraph record became `State: chosen` under its custom directory and vocabulary. Actual rejection reasons and open issues remained; no default ADR directory was created. |

Default-format fixtures passed the supplied checker; the custom-format fixture passed a targeted format/content check. Producer tasks authorized documentation only, with no implementation, commits, pushes, or external messages. The custom-format run invoked this collection's skill directly; it did not rerun the pinned external interview workflow.

The supplied instruction hashes are below. This finite run does not measure automatic skill selection or retrieval recall.

| File | SHA-256 |
| --- | --- |
| `SKILL.md` | `e66a2bb7b7564e3da5fe28b7d1bb6e2a624673d1253ec3c9a6bc3aa51b751b7d` |
| `references/RECORDS.md` | `80a4cc3ce2fe2379bf19c12f5b5d39ffe0a57a2d2192472212dc8f71253a77d9` |
| `references/DISCUSSIONS.md` | `ed444d78a73f40e8825d9297fb58f737cb2be9ebb4b24880c5db24aaef695342` |
| `references/LIFECYCLE.md` | `2ba83c2aa20dca7044aff4a5ce3229579c3bdd0a955f196c68816ace22fb1872` |
| `references/PROJECT-INTEGRATION.md` | `8334bce963c5d78729c1d1a0c1e289d5d28a7e75192630b923faa447f539378a` |
