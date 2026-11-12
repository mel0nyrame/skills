# Writing and maintaining decision records

## Write a record

Use the format resolved from project rules or consistent comparable records. Preserve valid short templates and existing representations during maintenance. When no reusable convention exists, use the project's language, one `docs/adr/YYYY-MM-DD-kebab-title.md` per topic, and this structure:

```markdown
# Decision title

Status: proposed

## Problem
## Decision
## Alternatives
## Consequences and risks
```

For default filenames, use the record's first creation date in `YYYY-MM-DD` form and a descriptive kebab-case topic slug, separated by one hyphen. Keep the filename stable through edits, acceptance, implementation, and merge. Different topics may share a date; the complete filename identifies the record. Reuse an existing same-topic owner; if independent topics would have the same filename, make their slugs more specific. Preserve existing numbered filenames and links unless migration is explicitly authorized. Project naming rules still take precedence.

Choose the state through [lifecycle rules](LIFECYCLE.md#default-states). The default checker also supports a complete Chinese schema.

Cover these propositions in the project's permitted structure:

- **Problem:** scope and constraints or conflict requiring a choice.
- **Decision:** current proposal or selected choice, reasons, assumptions, and boundaries. For unfinished topics, distinguish selections from recommendations and state open questions and next steps.
- **Alternatives:** actually evaluated candidates, their outcomes, and actual rejection reasons. Pending candidates stay pending; missing history remains an explicit evidence gap.
- **Consequences and risks:** benefits, costs, limits, relevant failure modes, verification evidence and gaps, and reconsideration conditions.

The default requires four separate nonempty sections. A chosen-technology list alone does not supply alternatives. Add dates, owners, and other fields when required by the project. Put replacement direction, scope, and links near the state.

Engineering documents own current operating details; decisions own the reasons for choices. Link those owners rather than copying their inventories. Maintain affected active records first and preserve unique reasons; cosmetic consistency alone does not justify rewriting historical records.

## Maintain a record

Compare affected records with current code, configuration, tests, documentation, active same-topic records, and inbound links. Classify the change:

| Situation | Action |
| --- | --- |
| Implementation facts change; choice holds | Update paths, names, defaults, owners, and implementation evidence directly |
| Candidates, recommendations, or open questions evolve; a pending choice is selected | Update the existing topic owner |
| An accepted or implemented choice is replaced | Follow project replacement rules; by default create a successor and cross-link both records, preserving the original choice and reasons |
| Partial replacement | Keep each record's unique rationale, constraints, alternatives, and valid scope; cross-link the replaced scope |
| Full replacement | Consolidate only after preserving meaningful reasons, alternatives, consequences, verification, gaps, and reconsideration conditions, and repairing inbound links |
| Nearby topics remain independent | Keep both active |

Reopening evaluation alone does not establish replacement. Review active same-topic records for every new record, including replacement of an accepted but unimplemented choice. Record the resulting relationship or independence. Preserve files and pending actions when consolidation or retirement exceeds authorization.

Archive or deletion additionally requires the [retirement protocol](LIFECYCLE.md#archive-or-delete). Archived bodies remain frozen.
