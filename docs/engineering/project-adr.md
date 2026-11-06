# Project ADR for engineering choices and their reasons

English | [简体中文](project-adr.zh.md) · [All guides](../README.md)

`project-adr` captures durable design proposals, selected choices, rejection reasons, and open questions so another agent can resume the topic. It also maintains implementation facts and replacement relationships. The document is often called an architecture decision record, or ADR; its scope includes lasting choices outside architecture.

Code may reveal the chosen database without explaining why other options were rejected. A useful record lets a later reader understand the original problem and tradeoffs without recovering the chat.

## Choose something worth recording

Follow the target project's creation criteria first. Without a policy, consider whether future maintainers could reasonably reopen the question or reintroduce a tempting mistake after forgetting the reason. Ordinary wording or local styling changes usually need no ADR.

This collection provides a real example. Its [first packaging decision](../agents/adr/0001--categorized-plugin-layout.md) explains shared categorized sources and the Codex compatibility manifest. The [later submodule decision](../agents/adr/0002--upstream-submodule-references.md) changes external-reference representation while retaining the other packaging choices. Readers can distinguish valid reasons from the replaced scope.

## Start a discussion or maintain a record

Capture a design discussion before implementation in the target project:

```text
$skills:project-adr
We are comparing local and object storage for uploads. Preserve meaningful
constraints, evaluated alternatives, rejection reasons, and open questions as
we discuss them. Reuse this topic's existing record. No choice has been made;
do not implement storage changes.
```

When the user or an authorized agent selects a choice but implementation is deferred, the default state is `accepted`. A recommendation alone remains `proposed`. For example: "We have selected object storage, but will implement it later. Record the choice, reasons, and remaining work."

Use a maintenance request when an existing record or implementation changes:

```text
$skills:project-adr
Inspect existing decisions about uploaded-file storage. If the choice changed,
record new reasons and real alternatives, and link old and new records. If only
implementation paths changed, synchronize the existing record's facts. Show the
proposed file changes first. Do not archive or delete other records.
```

Use `$project-adr` standalone or `/skills:project-adr` in Claude Code. Ordinary discussions and external interview skills use the same project rules and topic owner; neither requires editing the external skill.

Before proposing or implementing related work, the assistant searches active records and reads relevant choices, rejection reasons, and unresolved questions. Changed conditions can justify reconsideration, with the earlier reasons still visible. `project-adr` owns records; `project-engineering` supplies investigation and implementation-synchronization triggers. Ongoing behavior requires [project integration](../../skills/engineering/project-adr/references/PROJECT-INTEGRATION.md), not just installation.

## Understand the file output

The assistant locates records and templates before writing, then reuses the topic context while the search inputs remain valid. New scope, constraints, capabilities, paths, terms, evidence, or changed records can require another search. Candidate evaluation, open questions, and selection of a pending choice stay in the existing topic record. Replacing a previously selected choice follows project replacement rules; by default it creates a linked successor, even when the earlier choice was not implemented.

Without repository conventions, one decision topic occupies one Markdown file, with related candidates and their outcomes together. A separate rejected record needs independent lasting value.

```text
docs/adr/NNNN--kebab-title.md
```

`docs/adr/0001--upload-storage.md` is an example name, not an automatically generated file. The fallback archive directory is `docs/adr/archive/`. This collection follows its explicit `docs/agents/adr/` location instead.

The default English structure below uses a hypothetical unresolved storage discussion. Actual reasons and alternatives must come from evidence; pending candidates need no invented rejection reason.

```markdown
# Upload storage

Status: proposed

## Problem
Uploads need durable retention and a clear deletion owner.

## Decision
Local and object storage remain under evaluation. Deletion ownership is open.

## Alternatives
Local storage needs a backup assessment. Object storage needs a cost assessment.
Both candidates remain pending.

## Consequences and risks
Retention, deletion behavior, and operating costs still need verification.
```

Default states distinguish `proposed` (evaluating), `accepted` (selected but not fully implemented), `implemented` (completed with evidence), a still-useful `rejected` proposal, fully `superseded` records, and frozen `archived` history. A topic can contain rejected candidates without itself being rejected. Acceptance does not grant execution permission. An existing project lifecycle takes precedence.

The assistant reads [default-state definitions](../../skills/engineering/project-adr/references/LIFECYCLE.md#default-states) when the project lacks a lifecycle convention. Before archiving or deleting records, it reads the separate [preservation and dependency checks](../../skills/engineering/project-adr/references/LIFECYCLE.md#archive-or-delete).

## Maintain facts without erasing earlier choices

A file move or configuration rename can require a factual update while the decision remains valid. A changed choice needs a clear relationship with the earlier decision. Partial replacement can leave unique reasons in both records; deleting the older record for tidiness would lose them.

Archiving and deletion follow task authorization. Archived bodies remain frozen. Missing historical alternatives remain an evidence gap rather than invented template content.

## Review meaning before structure

Read whether the record explains the choice before relying on a checker. The default script validates structure, state, and local link paths, not truthful rationale. From this collection's root, check its actual records with this command.

```sh
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
```

It reads files and reports results; it does not generate ADRs. Complete Chinese default templates are also accepted. Use project-specific checks for other valid formats rather than rewriting them to satisfy this script. See the [execution instructions](../../skills/engineering/project-adr/SKILL.md) and [project integration](../../skills/engineering/project-adr/references/PROJECT-INTEGRATION.md).

For a discussion handoff, check that another agent can find the topic, recover actual rejection reasons, distinguish selected conclusions from recommendations, and identify the next open question without the original chat. A passing format check does not prove this behavior.
