# Project ADR for engineering choices and their reasons

English | [简体中文](project-adr.zh.md) · [All guides](../README.md)

`project-adr` preserves why an engineering choice holds, which alternatives were considered, and when it should be reconsidered. The document is often called an architecture decision record, or ADR. The skill also covers lasting engineering choices outside architecture.

Code may reveal the chosen database without explaining why other options were rejected. A useful record lets a later reader understand the original problem and tradeoffs without recovering the chat.

## Choose something worth recording

Follow the target project's creation criteria first. Without a policy, consider whether future maintainers could reasonably reopen the question or reintroduce a tempting mistake after forgetting the reason. Ordinary wording or local styling changes usually need no ADR.

This collection provides a real example. Its [first packaging decision](../agents/adr/0001--categorized-plugin-layout.md) explains shared categorized sources and the Codex compatibility manifest. The [later submodule decision](../agents/adr/0002--upstream-submodule-references.md) changes external-reference representation while retaining the other packaging choices. Readers can distinguish valid reasons from the replaced scope.

## Give the assistant a maintenance request

Use this in the project whose records need work.

```text
$skills:project-adr
Inspect existing decisions about uploaded-file storage. If the choice changed,
record new reasons and real alternatives, and link old and new records. If only
implementation paths changed, synchronize the existing record's facts. Show the
proposed file changes first. Do not archive or delete other records.
```

Use `$project-adr` standalone or `/skills:project-adr` in Claude Code. An undecided choice can be a `proposed` record; discussion alone does not make it implemented.

## Understand the file output

The assistant locates records and templates before writing. An existing owner of the same choice should normally be maintained. A new choice or replacement may need another record under project policy.

Without repository conventions, one decision occupies one Markdown file.

```text
docs/adr/NNNN--kebab-title.md
```

`docs/adr/0001--upload-storage.md` is an example name, not an automatically generated file. The fallback archive directory is `docs/adr/archive/`. This collection follows its explicit `docs/agents/adr/` location instead.

The default English structure is illustrated below. Actual reasons and alternatives must come from evidence.

```markdown
# Keep skill source in categorized directories

Status: implemented

## Problem
Readers need categories, while three installers need to find the same skills.

## Decision
Keep one source per skill and declare the paths each installer needs.

## Alternatives
A flat layout simplifies discovery but does not provide physical categories.

## Consequences and risks
Adding a category requires checking the installer paths and discovery results.
```

Default states distinguish `proposed`, `implemented`, a still-useful `rejected` choice, fully `superseded` records, and frozen `archived` history. An existing project lifecycle takes precedence.

## Maintain facts without erasing earlier choices

A file move or configuration rename can require a factual update while the decision remains valid. A changed choice needs a clear relationship with the earlier decision. Partial replacement can leave unique reasons in both records; deleting the older record for tidiness would lose them.

Archiving and deletion follow task authorization. Archived bodies remain frozen. Missing historical alternatives remain an evidence gap rather than invented template content.

## Review meaning before structure

Read whether the record explains the choice before relying on a checker. The default script validates structure, state, and local link paths, not truthful rationale. From this collection's root, check its actual records with this command.

```sh
python3 -B skills/engineering/project-adr/scripts/check_adr.py docs/agents/adr
```

It reads files and reports results; it does not generate ADRs. Complete Chinese default templates are also accepted. Use project-specific checks for other valid formats rather than rewriting them to satisfy this script. See the [execution instructions](../../skills/engineering/project-adr/SKILL.md) and [project integration](../../skills/engineering/project-adr/references/PROJECT-INTEGRATION.md).
