# Decision lifecycle

Project lifecycle rules take precedence.

## Default states

When the project lacks a convention and uses the default format, choose:

| State | Meaning |
| --- | --- |
| `proposed` | Choice under evaluation; constraints, recommendations, candidates, and questions may already be recorded |
| `accepted` | Explicitly selected by the user or an agent within task authorization, with implementation incomplete; state who selected it and on what basis |
| `implemented` | Completed with code, configuration, tests, or other applicable evidence; still guides future work |
| `rejected` | Declined proposal or independently useful rejected choice retained to prevent a tempting mistake |
| `superseded` | Fully replaced, with a replacement-record link |
| `archived` | Frozen historical snapshot; current sources establish current behavior |

A topic's state describes its choice, not every candidate. Rejected candidates can remain inside an active topic's alternatives. A recommendation remains `proposed`; acceptance grants no execution permission.

Move to `accepted` on authorized selection and to `implemented` after checking completion evidence. Start at `implemented` when already complete; partial implementation stays `accepted`, with completed and remaining scope stated. Preserve existing project representation, including formats without a state field, and express replacement relationships in that format.

For replacement, follow [record maintenance](RECORDS.md#maintain-a-record). Partial replacement retains the old record's still-valid state and identifies the replaced scope. Reopened evaluation alone does not establish replacement.

Retain rejected records while their reasons prevent repeated mistakes. Consider retirement when only closed local details or low-value history recoverable from current owners remain. Age, completion, length, or count alone does not justify retirement. Preserve uncertain cases and report the judgment boundary.

## Archive or delete

Default archive location: `docs/adr/archive/`. Follow the project's protocol and task authorization. Before moving or deleting:

1. Identify unique propositions and preserve every still-useful reason with an owner.
2. Search filenames, titles, symbols, configuration keys, and links for dependents.
3. Repair active inbound links so the retired path stops acting as current authority.
4. Make recoverable, reviewable changes, handling language variants and required metadata, manifests, signatures, and hashes together.

Archive changes only the state, location, and mechanical metadata permitted by project protocol. Its body, facts, wording, and outbound links then remain frozen.

Complete when unique reasons are preserved, active dependencies are repaired, and lifecycle/link checks pass. Report gaps and pending actions.
