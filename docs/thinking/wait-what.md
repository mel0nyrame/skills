# Wait What for an explanation that did not land

English | [简体中文](wait-what.zh.md) · [All guides](../README.md)

`wait-what` asks the assistant to re-explain its previous response with the missing context, clearer logic, and consistent terminology. Use it when you did not understand an explanation, rather than when you need to clarify the task before an answer.

This collection bundles a maintained adaptation of Matt Pocock's skill. The [source and license notice](../../skills/thinking/wait-what/NOTICE.md) records its provenance; the [MIT license](../../skills/thinking/wait-what/LICENSE) remains with the skill.

## Invoke it after an unclear response

The skill is manual-only. With this collection's Codex plugin, send:

```text
$skills:wait-what
I didn't follow how cache invalidation leads to a fresh result.
Explain that connection again, including the assumptions and a concrete example.
```

Use `$wait-what` for a standalone installation or `/skills:wait-what` in Claude Code. You can also invoke it without naming a specific gap to request a re-explanation of the previous response.

## What to expect

- The core answer first, then the minimum context and intermediate steps needed to explain the missing causal or logical connection.
- A response in your current language and requested format, without a required acknowledgment before the explanation.
- Direct wording and consistent terms. Definitions, examples, and limits appear as needed, not as a fixed four-part lecture.
- Necessary facts, conditions, exceptions, risks, evidence strength, uncertainty, and exact technical identifiers preserved.
- A distinction between verified facts, inferences, assumptions, and recommendations. If the previous claim is wrong, the assistant corrects it explicitly rather than just restyling it.

If there is no previous content, the assistant asks what to re-explain instead of inventing an explanation.

The explanation stays in the conversation by default. Invoking the skill grants no new authorization to write files, run commands, or use external services. It requires no other skill, `GLOSSARY.md`, project-specific documentation, or external service.

## Check the result

Check whether the new response makes the missing connection explicit, not merely shorter or differently worded. Necessary prerequisites, terms, assumptions, and limits should remain visible. Clearer wording does not verify the underlying technical claims; check those against the relevant evidence.

The [skill instructions](../../skills/thinking/wait-what/SKILL.md) own the behavior. Use [clarify](clarify.md) when the task itself needs clarification before an answer.
