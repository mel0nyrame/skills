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

- A reset from the confusing explanation, with missing prerequisites, the current problem state, and assumptions made explicit.
- A response in the language you are currently using.
- Direct wording, explicit conditions and outcomes, consistent terms, and brief definitions of technical terms.
- The core answer first, followed by the background and examples needed to understand it, without dropping necessary details or risks.
- A distinction between verified facts, inferences, assumptions, and recommendations.

The explanation stays in the conversation; the skill has no default file output. It requires no `GLOSSARY.md`, project-specific documentation, or external service.

## Check the result

Check whether the new response explains the missing connection instead of repeating the same wording. Necessary prerequisites, terms, assumptions, and limits should be visible. Clearer wording does not verify the underlying technical claims; check those against the relevant evidence.

The [skill instructions](../../skills/thinking/wait-what/SKILL.md) own the behavior. Use [clarify](clarify.md) when the task itself needs clarification before an answer.
