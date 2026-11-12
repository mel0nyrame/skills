# Date-based filenames for new decision records

Status: implemented

## Problem

Parallel branches independently allocate the next sequential ADR number. At selection time, main already contains `0007--repository-review-checks.md`, while open PRs #8 and #25 introduce different `0007` records and PR #9 introduces `0008`. Different full filenames can merge without a Git conflict even though their numeric prefixes collide. Reserving or renumbering sequential identifiers would require coordination between otherwise independent topics.

## Decision

The user selected `YYYY-MM-DD-kebab-title.md` for new records and authorized updating `project-adr` and opening a PR. Use the record's first creation date, a single hyphen before the topic slug, and a descriptive kebab-case topic name. Keep filenames stable through later edits, state changes, and merge. Dates are not unique IDs or replacement ordering; the complete filename identifies a record. Distinct topics may share a date. Reuse the existing owner for the same topic; disambiguate independent topics with more specific slugs if their full filenames would collide.

Apply this naming rule to new records in this repository's `docs/agents/adr/` and to the skill's fallback `docs/adr/` convention. Target-project naming rules continue to take precedence. Preserve existing numbered filenames and links. Renaming existing files, modifying other open PRs, and refreshing globally installed skill copies are outside this change.

Same-topic review found no active naming-policy owner. The [discussion-capture decision](0006--capture-decisions-during-design.md) continues to own capture and lifecycle behavior; this record owns filenames and replaces none of its choices.

## Alternatives

- **Sequential numbering with merge-time collision resolution.** Evaluated but not selected. It preserves existing visual ordering but requires coordinating merge order, renaming new records, and repairing their references.
- **A central number reservation list.** Not selected. It adds shared mutable bookkeeping to independent branch work.
- **Date alone or a daily sequence.** Not selected. Dates alone collide for same-day topics; a daily sequence reintroduces allocation coordination.
- **Date plus topic slug.** Selected. It avoids global number allocation while retaining readable, searchable filenames. It still requires same-topic discovery and slug disambiguation.
- **Bulk-renaming historical records.** Not selected. It creates link churn without helping independent new branches.

## Consequences and risks

The implementation updates the skill's fallback filename, detailed writing rules, integration command example, this repository's naming contract, and both usage-guide languages. Existing numbered records remain valid. The checker remains format-agnostic about filenames; it validates structure, status values, and local link paths, not date accuracy, topic uniqueness, or actual agent behavior.

Verification: `PYTHONUTF8=1 python3 -B -m unittest discover -s tests -v` completed successfully (102 tests run, 3 skipped); ADR validation passed all 8 active records; documentation validation passed 76 Markdown files; `git diff --check` passed. The first unrestricted full run reported two subprocess UTF-8 decoding errors on Windows; rerunning with Python UTF-8 mode passed without code changes. Static review covered same-day distinct topics, existing same-topic reuse, target-project naming precedence, stable filenames after status changes, and preservation of numbered history. No new isolated model-behavior run was performed. Representative prompts are: “Record two independent decisions made today,” “Update yesterday's ADR after implementation without renaming it,” and “Record a decision in a project that explicitly requires numbered ADRs.” Mechanical checks cannot establish these model behaviors.

Reconsider if readable slugs still produce frequent conflicts or if consumers require ordered numeric identifiers. Do not infer supersession or chronology from filename ordering; use explicit replacement links and implementation evidence.
