# Maintain recap knowledge profiles and contextual glossaries as sourced topics

Status: implemented

## Problem

Recap preserves sourced knowledge, but a library containing an explanation does not establish that its user understands or can apply it. Repeatedly explaining familiar concepts can also obscure new material. A knowledge profile can help select explanation depth; a contextual glossary can keep terms consistent and reduce repeated definitions.

User contributions in a conversation can provide evidence about recognition, mechanism understanding, and application. Those claims need attribution, context, and inference limits. The existing standalone-reading contract also requires each topic to preserve essential background and reasons regardless of the current user's apparent familiarity.

## Decision

Use existing formal topic types and publication paths rather than add a profile store or extend the helper schema. Implementation consists of agent instructions, discovery summaries, and usage guidance. Helper compatibility is checked separately from the unmeasured accuracy of an agent's competence judgments.

- Store contextual glossaries as `concept` topics and profiles as `research` topics, with the role aliases `glossary` and `knowledge profile`. Keep titles and filenames in the user's language. Start with one profile for the selected user, grouping concept entries as sections, and a glossary per coherent context. Create resources only when there are supported entries, and reuse existing topic owners.
- Maintain relevant entries during explicit capture or selected maintenance. Preserve observations, exact user/source attribution, dates when known, context, inference limits, and the explanation strategy supported by each claim. Recognition, mechanism understanding, and application are separate dimensions. Correctness and independent contribution matter; library coverage or assistant work does not establish user competence.
- Keep definitions separate from profile claims. Glossary entries own contextual meanings and relationships. Profiles link to those concepts and retain evidence. A formula such as `agent = harness + AI` can be local shorthand when supported by its source; it is not a universal identity.
- When a personalized explanation is requested, discover relevant profiles through the guide and title/alias searches, read current evidence at the query revision, and use it to select explanation depth. A topic's linked glossary definition can be followed separately. Ordinary fact lookup does not require profile discovery. Queries do not save new profile claims. Other consumers need an explicit recap query or their own authorized reading instruction.
- Let short local definitions and direct glossary links replace repeated extended definitions. Topics retain essential background, causal reasoning, examples, and operating conditions. Reconcile dependent interpretations when evidence or definitions change, keeping meaningful contradictions and unrelated supported claims.
- Keep entry data in Markdown bodies under existing source, coverage, candidate, approval, and revision rules. No migration, new root-level store, numerical competence score, background updates, or global personalization hook is introduced.

The [storage contract](../../../skills/knowledge/recap/references/personalization.md) owns shared discovery and publication rules. [Glossary](../../../skills/knowledge/recap/references/glossary.md) and [profile](../../../skills/knowledge/recap/references/profile.md) references own their respective entry and use rules. The [writing contract](../../../skills/knowledge/recap/references/knowledge.md#built-in-writing-contract) owns topic readability. The skill entry point routes capture, query, and maintenance to their task files. English/Chinese usage guides and discovery summaries expose the capability.

The storage contract also owns the [published-file description](../../../skills/knowledge/recap/references/personalization.md#published-files): concrete naming examples, authored topic/source files, helper-generated catalog/change/publication records, and conditional cursors. Examples do not introduce fixed schema paths or rename existing resources. Reports identify the actual added/updated paths; initialization alone does not create profile or glossary content.

Existing lexical-search and guide-maintenance decisions remain active. This record supersedes none of them. Role aliases use current lexical search; they do not add synonym expansion or change the search cache contract.

### Conditional loading refinement

Route [capture](../../../skills/knowledge/recap/references/capture.md) and [query](../../../skills/knowledge/recap/references/query.md) through separate reference files, keep glossary and profile rules under their respective branches, and retain shared storage/discovery rules in one small owner. Ordinary queries require neither capture instructions nor profile-maintenance rules. A personalized explanation is an explicit query branch; a linked glossary definition can be followed independently. Compact entries reuse existing source and correction rules instead of adding a second assessment checklist.

The refinement is implemented in the task and resource references, with synchronized usage guidance. Static checks validate branch pointers, unchanged capture steps except resource routing, and distinct required reading paths for ordinary lookup, glossary capture, profile capture, and personalized query. File/word counts describe instruction structure, not measured model token use or inference accuracy.

## Alternatives

- **Keep existing topic explanations only.** Simpler, but cannot retain demonstrated understanding or reuse a contextual vocabulary across explanations. The requested capability warrants explicit capture and consumption rules.
- **Add only a contextual glossary.** Useful for consistency, but does not meet the requested inference of user understanding from conversation contributions.
- **Use a dedicated profile/glossary file type or root-level store.** Not selected. Existing concept/research topics can express definitions and evidence-backed interpretations while retaining supported search, provenance, and publication. A separate store would require new lifecycle and consumer integration without a demonstrated need.
- **Infer mastery directly from library contents or combine mastery into definitions.** Not selected. Coverage and user competence are different claims, and definitions should remain useful when competence judgments change.
- **Shorten all topics according to the current profile.** Not selected. A mistaken or outdated inference could remove prerequisites needed later or by another reader.
- **Load one combined personalization contract before every explanation.** Not selected. Fact lookup and term definition do not require competence assessment. Conditional pointers preserve the relevant rules without making all branches pay for them.

## Consequences and risks

The feature adds agent instructions and discoverable, ordinary topics without changing scripts, schemas, or library rules. Existing libraries need no migration. Profiles and glossaries participate in normal topic search, so queries can return them alongside other formal knowledge.

Incorrect or overly broad profile claims could make answers skip needed explanations. Quoted text, self-report, silence, and assistant-authored material need distinct treatment. Context-specific definitions can be misapplied across subjects, and circular links can hide missing prerequisites. The entry and standalone-reading checks address these cases as agent responsibilities; helper validation cannot establish semantic correctness.

[Manual scenarios](../../../tests/scenarios/recap_personalization.md) specify component recognition, mechanism/application evidence, attribution mistakes, scoped terms, corrections and query behavior, and libraries without personalization resources. They are test specifications, not executed model evaluations.

Validation on 2026-11-05 passed all 67 repository tests with `python3 -B -m unittest discover -s tests -v`. A disposable-library smoke run generated and published glossary/profile inputs using Chinese filenames and the existing concept/research types, discovered their role aliases, read current topics and their source at one revision, and cleaned the published candidate. Queries left the formal revision and tracked bytes unchanged. Link/anchor, bilingual-pair, YAML, and explicit-invocation checks passed. This establishes format and helper compatibility, not model inference accuracy. No personal knowledge library or installed skill copy was changed.

A separate artifact smoke run verified the documented file outputs: initialization produced no profile/glossary topics; first publication changed exactly the two selected topic files, their source, `index.md`, `CHANGELOG.md`, and the operation's publication record. No cursor was produced without tracking. A second publication reused the existing profile path. Naming examples describe authored paths, not files automatically generated by initialization.
