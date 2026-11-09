# Project Engineering forward check

## 2026-11-09 instruction refactor

A fresh independent agent received the revised skill, baseline companion skills, and an isolated Python project. Its rules pointed to an existing CSV exporter, a public-field schema, a generator, two tests, and an active privacy decision. The parent supplied no expected answer.

Request:

```text
Add status after id and title in CSV exports, with each row's status value.
Keep export authorization and exclude private_notes. Use the existing engineering
entry points, implement and validate the change, and maintain relevant project
knowledge. Do not commit or push.
```

Observed: the agent edited the schema, regenerated fields, extended the existing test, and updated the engineering owner. Both tests passed, covering ordered values, permission rejection, and private-field exclusion. Regeneration was stable. The existing ADR remained valid. The parent inspected the diff: no parallel exporter, unrelated writes, commits, or pushes.

One scenario passed. This run checks the supplied instructions with baseline companions; it does not measure automatic skill selection or broader reliability.

Evaluated `SKILL.md` SHA-256: `d271a6dc187f5b1838e1633bcd96708589b449978ffb480b7d1145f57ac3beb0`.

## First-decision integration

On 2026-11-09, a fresh independent agent received the revised engineering skill, the baseline `project-adr` companion, and an isolated Git project. Existing `AGENTS.md` pointed to engineering notes but had no decision-maintenance rules. A CI workflow already existed. The parent supplied no expected answer.

Request:

```text
We selected one JSON manifest per report. Reports are imported and deleted
independently, with at most 100 reports and one local writer. A global manifest
was rejected because independent deletion would rewrite the shared manifest.
Save this design progress and discoverable engineering guidance. Implementation
has not started; version compatibility and corrupt-file handling remain open.
Only edit existing AGENTS.md and docs. Do not change code, scripts, hooks, or CI;
do not commit or push.
```

Observed: the agent created one `accepted` decision, a decision-directory contract, and persistent-data notes; it linked them through the existing instructions and engineering entry point. The selected choice, actual rejection reason, unimplemented state, and open questions remained explicit. The supplied ADR checker passed one active record; eight local links and whitespace checks passed.

The parent inspected all five changed documents and confirmed the existing CI bytes, skill files, and commit count were unchanged. No code, script, hook, or CI integration was added. One scenario passed; no baseline behavioral comparison was run.

| Supplied instruction | SHA-256 |
| --- | --- |
| `project-engineering/SKILL.md` | `d271a6dc187f5b1838e1633bcd96708589b449978ffb480b7d1145f57ac3beb0` |
| `project-engineering/references/PROJECT-GOVERNANCE.md` | `66cfd7a6acf4a5af97182e7a1739da17fa16eda7706139f5e01480849307a5c3` |
| `project-adr/SKILL.md` | `e8b8d60ef24c2e243120aff304f24c484fc91ae7318a708c4c152db35c357bbc` |
| `project-adr/references/PROJECT-INTEGRATION.md` | `d1987f9f5074ffacbbd995480d986fe9edb759178ae64ab6533dba81254a1165` |
