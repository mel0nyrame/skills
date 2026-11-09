# Topics, evidence, and reading

## Library shape

Use readable, stable topic names under `topics/`, normally in the user's language. Name the understanding problem, not the chat date. Start shallow; add real subject groups only when they improve navigation. Keep aliases and dates in metadata rather than accumulating filename prefixes. No global document-ID service is required. Update relative links after an approved rename.

The helper builds `index.md` entries from topic summaries. Use those summaries to select topics answering the same understanding question and applicability, then read their bodies before merging. Follow prerequisite links when that background is needed. Write each summary around the reader's question and learning value, with the case scope where needed; keep it consistent with the body. Put useful prerequisite and next-reading links in the topics themselves, with a reason to follow each. Preserve existing guide prose unless the requested maintenance includes its introduction; use the [bounded guide input](formats.md#guide-introduction) and exact user approval. Packets cannot replace the generated catalog or trailing prose. Write `CHANGELOG.md` for substantive knowledge changes, not tool transcripts.

When representative queries miss a relevant topic, consider precise aliases that readers actually use. Preserve existing aliases. Do not assume all topics need additions or infer empty aliases by searching for a YAML-only spelling; topic metadata is JSON frontmatter.

## Built-in writing contract

Choose a structure from the material rather than filling every heading. Start by identifying the subject, question and scope. Explain necessary terms, project identities and chapter labels on first use. Keep essential background in the topic; sources supply provenance. Follow the reader's next questions, preserving reasons and examples. A project-specific explanation is valid when its case and version are explicit.

Conceptual topics often need mechanism, relationships, misconceptions, and applicability. Separate general principles from a particular implementation's names and behavior. Research needs findings, evidence, competing explanations, and gaps. Procedures need target/environment, required starting state, affected paths, ordered actions, visible results, and failure/recovery boundaries; verify local changes before destructive steps. Preserve the conditions behind a past observation when deriving an action rule. Decisions need alternatives and reasons. Combine as needed; tables or diagrams support explanation rather than replacing it.

Use actual source examples or clearly labeled illustrative hypotheticals. Do not invent the user's experience, fabricate supporting cases, or pad prose with restated conclusions. Do not repeat raw questions and answers by default. Split a page for an independently understandable subproblem, not an arbitrary point count. Protect coherent explanations from fragmentation.

Before publication, read each new or substantively changed topic as a standalone page, initially without the chat or sources. Identify unexplained referents, missing conditions and summary/body mismatches; repair them in the candidate. Then follow decisive evidence locators and relevant reading links. The check passes when the page explains its subject, reasons and limits, supports its actions within stated conditions, and makes central evidence locatable. Unresolved defects remain drafts. This is an author check; concurrent merges additionally require independent review.

## Evidence and scope

Distinguish supported claims (inspected primary evidence or actual test, within stated conditions), inferred synthesis, pending assertions, and unresolved disputed evidence. State whether support was inspected during this capture or inherited from an identifiable earlier check. A prior assistant's report alone remains a reported claim; retrieve its decisive evidence or qualify/defer the conclusion. Conversation coverage describes messages read, not factual verification.

Keep significant caveats beside the claim. Cite inspected materials with locators usable from the retained library or an identified external source: repository URL plus commit/path for versioned code, document URL plus section, or a sufficient sanitized excerpt for nonpublic evidence. A filename, line number or another machine's absolute path alone is insufficient. Unavailable supplementary material is labeled optional; central missing evidence limits the claim. Search snippets, unrun commands and plausible recollections do not establish verification. Cite central volatile facts, corrections, contested conclusions and action grounds precisely; section-level citations can cover ordinary explanations without a sentence ledger.

Keep volatile facts when the reasoning needs them; state version, environment, or as-of date. Drop transient status with no lasting explanatory value. Past events can still have incorrect descriptions, numbers, and causal interpretations.

## Time fields

Use the fixed fields and type-specific body contracts in [formats](formats.md). The helper emits canonical frontmatter from structured input.

`created` and `updated` describe the file. `acquired` describes entry into this library; multiple acquisitions belong in sources. Record `verified` only with checked scope and actual evidence, normally beside mixed-status claims. `event_date`, `as_of`, and applicable version are separate and optional. Unknown dates remain unknown. Use the user's current timezone and preserve source timezone/precision. An overdue review is not disproven content.

## Minimal source record

Use `sources/<host>-<exact-session-id>.md` with host, exact session/branch and cutoff; acquisition date; original locator (host-relative where possible); inspected ranges/chunks and counts; gaps and attachment status; receipt/prefix identity; supported topic links; and necessary excerpts with what they establish.

Remove unrelated identities, credentials, and private paths. Receipt metadata enables matching, not transcript archiving. Locators and excerpts can themselves be private. Only retained excerpts remain independently inspectable after deletion of the original chat; do not promise full replay.

Persist successful machine checkpoints in `.state/` with the represented knowledge; the source record explains coverage intelligibly. A script receipt describes extraction, not model inspection: read every included chunk and reconcile identity, cutoff and ranges across receipt, source header and body. Declare message coverage separately from unread attachments/tools and from technical verification. Incremental recaps preserve previous source contributions and acquisition dates rather than replacing them with only the delta.

## Changelog

For each substantive operation, record date, topic link, kind, what changed, why, and supporting evidence. Explain old/new differences for corrections, and linked topics still needing work. Group cosmetic edits. Keep private raw residue out. Git versions and the interrupted-publication journal, not the changelog, provide recovery.
