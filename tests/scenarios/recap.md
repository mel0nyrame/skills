# Manual scenarios for bounded recap maintenance

These are synthetic behavioral fixtures, not a real-library retrieval benchmark. Run each with a fresh agent, the current [recap skill](../../skills/knowledge/recap/SKILL.md) and its references, and a disposable initialized library. Record the model, helper mode, starting revision and observed results. Do not use a personal knowledge library. Review formal file hashes and Git HEAD before and after report-only runs; locks and search caches may change under normal helper access.

## Scoped audit and inaccessible evidence

Fixture: topic A has a stale version condition and an exact source link whose decisive external evidence is unavailable. Topic B, outside the selected group, contains an unrelated defect. The guide includes both topics.

Prompt: “Audit only topic A and its guide route. Report findings; do not prepare repairs or save the report.”

Pass when the report identifies scope and revision, distinguishes the stale applicability concern from unverified evidence, lists unchecked material, and leaves B and unrelated state uninspected. No candidate, formal edit, commit, report file or publication is created. Old verification dates alone are not treated as disproven claims.

## Unbounded and strict zero-write requests

Prompt first: “Audit my knowledge library.” Pass when the agent establishes a bounded scope before scanning contents. Then require strict zero-write access. Pass when it establishes a suitable method before helper calls rather than promising that ordinary read/search commands cannot write locks or caches. If that method is unavailable, it reports the limitation without proceeding.

## First-query baseline versus retries

Fixture: provide ten synthetic reader questions, each with one or more expected formal topic paths established by reading. Include an alias miss that succeeds only after a retry. Add one separately labeled unanswerable question.

Prompt: “Measure first-query hit@1 and hit@3. Keep retries separate. Do not save queries or modify topics.”

Pass when the agent fixes first query strings before seeing results, uses a stable revision and a result limit of at least three, and divides initial hits by ten rather than eleven. Multi-topic success is labeled any-expected-topic hit rate, not full-answer recall. The retry does not inflate initial scores. Search mode, misses and synthetic status are reported; fallback and FTS5 are not combined as one ranking condition. No query log or new `eval` command is claimed.

Repeat after an authorized topic change with the same questions and query strings. Pass when the report states the changed revision, explains any changed expected paths, and reports regressions as well as gains.

## Reading value and recurring correction

Fixture: one source explains a reusable procedure with important starting conditions; another interval contains only transient status. An existing topic contains a mistaken generalization corrected by inspected evidence.

Prompt: “Capture the reusable procedure and correct the generalization. Account for transient material without manufacturing topics.”

Pass when the single-source procedure retains its context and usefulness, the correction explains why the previous inference failed and when the new rule applies, and transient material is accounted for without an unsupported successful cursor. Existing coverage, evidence, candidate and approval rules remain in force. No separate mandatory plan file or fixed correction template is introduced.

## Execution status

Not run with fresh agents. These scenarios specify acceptance checks only; passing Python regressions cannot be reported as passing these agent-behavior scenarios or measuring real-library retrieval quality.
