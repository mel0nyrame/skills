# Terminology and knowledge profiles

A **contextual glossary** defines terms within a subject or project. A **knowledge profile** records evidence about the selected user's familiarity, understanding, and application of those concepts. Glossary definitions describe concepts; profile claims describe the user's demonstrated relationship to them.

## Capture and maintain

1. Find relevant existing glossary/profile topics through the guide and title/alias searches. Read them before adding entries. Use ordinary formal topics under `topics/`: `type: concept` for glossaries and `type: research` for knowledge profiles. Keep titles and filenames in the user's language, with the discoverable alias `glossary` or `knowledge profile` respectively. These aliases identify the document's role; do not rename or reclassify an unrelated topic merely to obtain them. Create a resource only when there are supported entries to record.
2. Inspect the selected conversation for resolved terminology and contributions attributable to the selected user. Keep other speakers, quoted material, and assistant-authored explanations distinct. Retain necessary excerpts and exact message locators in the owning source records under the existing coverage rules. An inherited profile claim needs identifiable support; unsupported prior assistant judgments remain pending.
3. Develop entries using the contracts below. Separate the user's observed contribution from the agent's interpretation. Check technical correctness within the relevant project/version before using a contribution as positive evidence of understanding. If correctness or attribution is unresolved, preserve that uncertainty instead of promoting the claim.
4. Include supported glossary/profile changes, their source contributions, and affected topic links in the same candidate as the captured knowledge. Use the [existing document fields](formats.md#topic-input) and publication flow; entry details belong in Markdown bodies, not new schema fields or external profile files. Preserve sources supporting earlier entries.
5. Before publication, check every changed entry for attributable evidence, scope, inference limits, and the explanation strategy it supports. Follow glossary links without the chat to check definitions and prerequisites. Reconcile affected profile claims when their definitions or evidence change. Completion requires an intelligible entry and locatable support, or an explicit pending judgment with no assumed competence.

These are ordinary sourced topics, covered by current search, source, revision, candidate, review, and approval rules. Profile updates do not require a new per-entry approval ritual. Changes to the user's non-factual judgment retain the existing preview/approval requirement. Keep recap explicitly invoked; ordinary conversations do not create background profile updates.

## Contextual glossaries

Use one glossary per coherent subject; split only when distinct contexts give the same term different meanings. Keep each entry's canonical term, short definition, applicability, and necessary relationships together. Include useful aliases and source links. Point extended explanations and examples to their owning topics.

A definition such as `agent = harness + AI` is usable as agreed shorthand within a stated context. Preserve what the source establishes about that meaning; a user's preferred local definition does not establish a universal technical identity. Define unfamiliar constituent terms or link directly to their entries. Resolve conflicting definitions by context or retain the disagreement until resolved.

In a knowledge topic, introduce a necessary term with a short local explanation and a direct glossary-entry link. The glossary can own extended definitions. The topic still owns its question, essential background, causal reasoning, examples, and operating conditions. Check that glossary links and prerequisite chains resolve without circular definitions. The current user's profile does not justify removing those elements.

## Knowledge profile evidence

Keep entries specific to a concept and context. Record these together in the body:

| Entry information | Required content |
| --- | --- |
| Concept and scope | Link to its glossary entry or explanatory topic; relevant project, version, or scenario |
| Observation | What the user actually said or did, its source/message locator, and date when known |
| Evidence conditions | Volunteered, prompted, self-reported, repeated, or quoted; enough dialogue context to interpret it |
| Interpretation | Supported familiarity, mechanism understanding, or application; distinguish inference from self-report and retain uncertainty |
| Explanation strategy | What can be used directly and what still needs a prompt or fuller explanation |

Treat familiarity, mechanism understanding, and application as separate dimensions. Use the narrowest claim the contribution supports:

| Conversation contribution, if correct in context | Supported interpretation |
| --- | --- |
| Names tools in a particular harness | Recognizes those components; their scheduling and recovery remain unknown |
| Explains why components interact as they do | Understands the explained mechanism within that scope |
| Selects an approach for a changed scenario and explains why | Provides evidence of application in that scenario |
| Identifies an error and supplies a correct reason | Provides evidence of distinguishing that failure or boundary |

For example, if a user independently names three tools and the inspected tool catalogue confirms them, record recognition of those tools. The explanation strategy can use their names directly while introducing their interactions as needed. Do not extend that observation to competence with every harness.

Independent explanations, new examples, and successful transfer to a changed scenario provide more support than repeating nearby text. Self-report remains self-report. Merely having a topic in the library, an assistant completing a task, a question, silence, or agreement supplies no demonstration of user understanding. Leave unsupported dimensions unknown. Confidence in an inference and breadth of competence are separate; use descriptive limits rather than uncalibrated numerical scores.

Update the same concept entry as evidence accumulates. Keep material counterexamples, contradictions, and context differences visible; recency alone does not resolve them. Correct or qualify a profile claim when its source is corrected, removed, or no longer supports its interpretation. Preserve unrelated supported claims and follow existing publication rules for source removal and substantial rewriting. Source dates describe observations, not permanent competence or automatic expiry.

## Use in answers

Before composing an explanation, use the guide or search `glossary` and `knowledge profile`, adding short subject terms when useful, then read the relevant current topics with the query's revision. Existing libraries may use other titles or aliases; try their language and known names before concluding that a resource is absent. Read only resources relevant to the selected user and question.

Use the contextual definition for terminology and the supported profile interpretation for explanation depth. Introduce terms whose understanding is unknown. Keep new mechanisms, prerequisites, applicability, and consequences explicit even when component names are familiar. When evidence conflicts, explain the needed prerequisite briefly or ask a focused question if it changes the answer. Ordinary conversations need no proficiency test.

With no relevant profile or glossary, use the topic's own definitions and explain necessary prerequisites normally. During a query, apply existing resources without modifying formal knowledge; suggest a separate capture or maintenance only when saving a material new finding would be useful. Other agents need an explicit recap query or their own authorized instruction to read these resources; saving topics does not create a global personalization hook.
