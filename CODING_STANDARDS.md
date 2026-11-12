# Review standards

Read for repository reviews, alongside the diff and applicable project rules.

## Skill and documentation semantics

For each claimed regression, identify the changed trigger, condition, action, obligation, or authorization boundary. Compare both versions and follow relevant references before treating deleted wording as deleted behavior. Distinguish a reproduced failure, a static semantic gap, and an untested risk. Equivalent wording can preserve a rule without repeating it at every step.

For executable claims, trace argument handling, discovery/filtering, validation, and reporting. Inspect existing focused tests and CI evidence. A function excerpt or state constant alone does not establish CLI behavior.

Review descriptions for distinct invocation branches and the body for execution steps. Skill enumeration does not demonstrate correct automatic invocation. Compare translations for the same actor, action, applicability conditions, guarantees, and requirement strength. Bilingual-pair checks establish file pairing and links, not semantic equivalence.

## Evidence and PRs

Run the [repository checks](docs/maintaining.md#checks) for mechanical errors. Review whether the Summary visual explains the actual diff and whether Before/After evidence supports the stated behavior. Use the [PR writing guidance](docs/engineering/pr.md) for the body.

Behavior records identify the supplied source commit and hashes, actual outputs, checks, and uncovered branches. Historical results remain bound to their recorded source. ADRs preserve validation conclusions, decision-relevant evidence, and limitations; prefer PR Evidence or test reports for routine exact counts. If an ADR needs exact counts, identify the validated commit alongside them and describe them as a snapshot rather than current repository totals. Do not refresh historical counts merely because unrelated work changes the totals. New instruction behavior needs its own run; prepared inputs and passing structural tests are not model results. See [forward fixtures](tests/scenarios/README.md).

## Bounded tool output

Keep full tool results in session state. Display only fields needed for the decision: for PR discussion, usually author, body, URL, and reviewed head. Select the normalized text instead of printing both text and HTML. For commands, show a short result and retain full logs for failures. Expand reads when the next decision needs more context.
