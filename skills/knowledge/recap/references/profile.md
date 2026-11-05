# Knowledge profiles

A knowledge profile records the selected user's demonstrated familiarity, understanding, and application of concepts. For finding and publishing profile topics, read [resource storage](personalization.md).

## Capture and maintain

Retain useful contributions attributable to the selected user. Keep each concept entry compact: a scoped interpretation and its supporting observation/source locator, with the date when known. Link its glossary entry or explanatory topic when available. Note an explanation strategy only when it helps future answers; these details can be a sentence rather than a fixed form.

Separate the observed contribution from the agent's inference. Preserve conditions that affect its strength, such as self-report, prompting, quotation, or repetition of nearby assistant text. Check technical correctness in context before treating a contribution as positive understanding evidence. Unresolved attribution or correctness leaves the interpretation pending.

| Correct contribution in context | Supported scope |
| --- | --- |
| Names tools in a harness | Recognizes those components; mechanism understanding remains unknown |
| Explains component interactions | Understands the explained mechanism |
| Chooses an approach for a changed scenario and explains why | Provides evidence of application in that scenario |
| Identifies an error and supplies a correct reason | Distinguishes that failure or boundary |

These are separate dimensions, not a competence score. Independent explanations and transfer provide more support than repetition. Library contents, assistant work, questions, silence, and agreement do not demonstrate user understanding; leave unsupported dimensions unknown.

Update the same entry as evidence accumulates. Reconcile corrections or source removal without erasing unrelated supported claims. Keep meaningful counterexamples and context differences; recency alone does not resolve them. Use the existing evidence, source and approval rules rather than a separate assessment workflow. The entry is ready when its scope follows from locatable evidence or is explicitly pending. Source dates describe observations rather than permanent competence or automatic expiry.

## Use in answers

For a requested personalized explanation, find relevant current profile topics through [resource discovery](personalization.md), retaining the query's revision. Read only evidence relevant to the selected user and question. Use familiar terms directly within their supported scope; explain new mechanisms, prerequisites, applicability, and consequences. With missing or conflicting evidence, give a brief prerequisite explanation or ask a focused question if it changes the answer.

Queries consume these records without updating them. Ordinary conversation needs no proficiency test or background capture. Other agents need an explicit recap query or their own authorized reading instruction; saving a profile does not create a global personalization hook.
