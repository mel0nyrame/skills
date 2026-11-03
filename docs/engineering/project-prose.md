# Project Prose for documentation other people can use

English | [简体中文](project-prose.zh.md) · [All guides](../README.md)

`project-prose` checks whether technical prose remains understandable without the author's private conversation. It verifies claims against implementation, preserves necessary conditions, checks accessible references, and improves wording. It applies to READMEs, engineering documents, comments, API descriptions, decisions, and agent instructions.

The direct output is usually the document or comment you named. Constraints, failure behavior, and responsibilities must survive the rewrite.

## Name the document and reader

Start with a narrow request. The export feature and path below are teaching examples.

```text
$skills:project-prose
Review docs/export.md for a contributor new to the project. Check claims against
implementation and edit that file directly. Preserve permission constraints,
failure handling, and compatibility requirements. Flag missing evidence rather
than inventing facts. Do not change behavior code or create a separate report.
```

This uses the collection's Codex plugin. Use `$project-prose` standalone or `/skills:project-prose` in Claude Code. Verifying behavior requires relevant source access. With only a prose fragment, the assistant can review expression but must identify unverified facts.

## Follow a claim back to something inspectable

“Handle export errors as agreed in the last review” leaves a new contributor without the actual procedure. Replacing it with “follow the established approach” still omits that information. The assistant needs current implementation or accessible rules before stating the behavior.

If the teaching example really shows retry behavior and retained filters, this wording could be supported.

```text
An export failure displays an error and preserves the current filters.
The user can click Export again.
```

The actual project must provide evidence for that statement. This illustration does not establish that your software behaves this way.

Next, identify which source owns the explanation. Generated API documentation should be changed through source comments or schemas and regenerated. Usage documents explain current behavior; decisions own lasting reasons. Other locations retain only the summary and links their readers need, avoiding conflicting full explanations.

## Files that can change

| Input and authorization | Possible output |
| --- | --- |
| Review a fragment only | Findings and suggestions in chat, without file writes |
| Edit `docs/export.md` directly | The updated named file |
| Text derives from source comments or a schema | Authorized source changes and regenerated documentation |
| Lasting reasons belong to an existing ADR | Necessary maintenance in that record with clear ownership |

There is no default `review.md`, replacement README, or personal glossary. Additional documents need an actual reader purpose and a clear location.

## Check whether the rewrite helps

Read the file alone, without the chat. It should identify the reader, prerequisites, real behavior, and failure handling. Links should lead to actual repository files or declared external sources. Inspect the diff for preserved obligations. A required permission check must not become an optional recommendation.

Relevant, verifiable history and alternatives can remain. Removing every historical word or qualifier is not an accuracy test. The [execution instructions](../../skills/engineering/project-prose/SKILL.md) describe the review method; the [project-adr guide](project-adr.md) explains maintenance of lasting reasons.
