---
name: wait-what
description: "Stop. That last message did not land: re-pitch it."
disable-model-invocation: true
---

# Wait What

Repair the previous explanation so the user can follow the missing causal or logical connection.

## Re-explain

- Use the user's current language and requested format. If there is no previous content to re-explain, ask what the user wants explained; do not invent it.
- Identify the gap from the user's question and available conversation. If the previous claim is wrong, correct it explicitly rather than just restyling it.
- Give the core answer first. Then add only the context needed to connect the relevant premise or cause to the conclusion or outcome. Make that connection explicit, including conditions and intermediate steps that the previous explanation skipped.
- Add definitions, a concrete example, or limits when they help repair the gap. Choose what is needed rather than giving a fixed four-part lecture. Start with the explanation; no acknowledgment ceremony is required.

## Preserve meaning

- Use direct sentences, one main idea at a time, and consistent terms. Define unfamiliar technical terms when needed. Preserve exact code identifiers, commands, and API names.
- Keep necessary facts, conditions, exceptions, risks, evidence strength, and uncertainty. Distinguish verified facts, inferences, assumptions, and recommendations. Clearer wording must not make an unsupported claim sound verified.

Respond in the conversation by default. Invocation grants no new authorization to write files, run commands, or use external services. This skill is self-contained; it requires no other skill or `GLOSSARY.md`.

Finish when the missing connection is explicit and the necessary conditions remain visible, not merely when the answer is shorter or reworded.
