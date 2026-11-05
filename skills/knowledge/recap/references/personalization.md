# Glossary and profile topic storage

Read this when finding or publishing glossary/profile resources. They are ordinary sourced topics under `topics/`, covered by the existing [document format](formats.md#topic-input) and publication workflow.

| Resource | Type | Discovery alias | New-file example |
| --- | --- | --- | --- |
| Contextual glossary | `concept` | `glossary` | `topics/agent-glossary.md` |
| Knowledge profile | `research` | `knowledge profile` | `topics/knowledge-profile.md` |

Use titles and filenames in the user's language. Find existing resources through the guide and title/alias searches; add short subject terms when useful. Older libraries may use different names, so try their language and known titles before concluding absence. Read relevant current topics at the operation/query revision. Preserve existing aliases and add the role alias to the relevant resource.

Create a resource only when it has a supported entry. Keep entry details in Markdown bodies and include the necessary source contributions in the same candidate. Preserve support for earlier entries and reuse existing source, coverage, approval, and correction rules. Only an explicit capture or selected maintenance publishes updates; ordinary conversation creates no background writes.

## Published files

Resolve all paths below against the selected knowledge-library root, not the skill or current project. Start with one profile topic for the selected user, grouping concepts as sections, and a glossary topic per coherent context. For a Chinese-language library, initial names can be `topics/用户知识画像.md` and `topics/Agent术语表.md`. These are naming examples: reuse the appropriate existing paths on later captures instead of creating a profile per conversation.

| File | Creation or update condition |
| --- | --- |
| The selected `topics/` profile/glossary paths | Candidate-authored sourced Markdown; add on the first supported capture, then update the same resources |
| `sources/<host>-<session-id>.md` | Add or update the selected conversation's source record with coverage and supporting excerpts; topics link to it |
| `index.md` and `CHANGELOG.md` | Publisher updates the generated topic catalog and knowledge-change entries; authored guide-introduction changes retain their approval rules |
| `.state/published/<operation-id>.json` | Publisher creates the operation's publication record |

Capture cursors under `.state/cursors/` are conditional on incremental tracking. Initialization alone does not create empty profile/glossary topics; queries do not create these formal files. Report the exact saved paths and distinguish additions from updates. The existing publication flow owns candidate worktrees and recovery state.
