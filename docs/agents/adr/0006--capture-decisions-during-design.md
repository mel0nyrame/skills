# Capture durable decisions during design discussions

Status: implemented

## Problem

A later agent needs to recover meaningful proposals, rejected alternatives, reasons, and unresolved questions without reconstructing a private conversation. Capturing decisions only after implementation loses design work when implementation is deferred or a discussion stops early.

Lifecycle vocabulary alone does not specify when discussion progress must be persisted. Explicit capture and retrieval triggers are needed across the [project-adr skill](../../../skills/engineering/project-adr/SKILL.md), the [project-engineering workflow](../../../skills/engineering/project-engineering/SKILL.md), and project instructions. Actual invocation frequency has not been measured.

The integration must support externally maintained discussion workflows, including `grill-me` and `grill-with-docs`, without assuming that they provide this collection's persistence contract.

## Decision

Capture and resume durable decision topics during design, before implementation is required. The workflow has these boundaries:

- A later agent must be able to identify considered options, important rejection reasons, unresolved questions, and whether a choice has actually been implemented.
- Keep external discussion skills unchanged. This collection owns its decision-recording rules, which also apply to ordinary design discussions without those external skills.
- Organize records by decision topic. Keep related candidates and their rejection reasons together. Give a rejected option its own record only when it has independent lasting value.
- Update a topic's record when discussion establishes a meaningful constraint, rejects a real candidate, or develops a substantial proposal that needs further work. Do not defer all recording until implementation or final delivery.
- Distinguish confirmed conclusions, agent recommendations, and unresolved questions. Review the record before closing a discussion, without requiring a conclusion to every open question.
- Preserve discussion progress only when it has future value: a meaningful constraint, a real tradeoff, or an unresolved question worth continuing must affect subsequent work. A passing suggestion without further evaluation does not require a record. For a recorded topic, preserve the candidates actually evaluated and their outcomes.
- For projects using the default lifecycle, distinguish `proposed` (still evaluating the choice), `accepted` (explicitly selected but not fully implemented), and `implemented` (implementation completed with supporting evidence). Retain rejection, supersession, and archival states. Existing project lifecycle rules take precedence. Accepting a choice does not itself authorize its execution.
- `project-adr` owns the value judgment, topic content, rationale, and lifecycle of records. `project-engineering` reads relevant records during investigation and triggers synchronization as implementation changes. Project instructions expose the shared recording contract to ordinary discussions and external discussion workflows.
- Before starting related work, the agent searches active records by task topic and reads the relevant proposals, selected choices, and rejection reasons. When changed conditions justify reconsideration, state those conditions explicitly and reevaluate the choice with its earlier rationale visible.

The [glossary](../../../GLOSSARY.md) defines the topic, record, and accepted/implemented distinction used here. Acceptance may come from user confirmation or an agent's autonomous engineering choice within existing task authorization. A recommendation alone remains proposed.

The project-level [recording convention](README.md) provides one contract for ordinary discussions and external interview workflows. The skill's [discussion branch](../../../skills/engineering/project-adr/references/DISCUSSIONS.md) owns the capture and resumption procedure.

### Implementation scope

`project-adr` supplies capture and resumption triggers, lifecycle guidance, project-integration instructions, and invocation metadata. `project-engineering` supplies discussion-time capture and task-entry retrieval. The default checker accepts the selected lifecycle vocabulary while preserving existing states. Project-specific formats remain subject to their own checks. The affected English and Chinese usage guides and repository standing rules expose the same responsibilities.

The external discussion skills remain unchanged. Existing records do not require a bulk rewrite merely to adopt the new defaults. Installing or refreshing global skill copies is outside this design's implementation scope.

The existing packaging, submodule, release, and recap-search decisions remain active. This record replaces none of them and owns the discussion-capture policy.

## Alternatives

- **Rely on the external discussion skills for persistence.** Not selected. This would leave the required handoff dependent on externally maintained instructions rather than a collection-owned contract.
- **Create a separate record for every candidate.** Not selected as the default. Keeping candidates under their decision topic preserves the context needed to compare them. Independently useful rejected decisions remain eligible for separate records.
- **Record only at implementation or delivery.** Not selected. It leaves paused or deferred design work unavailable to the next agent.
- **Use `implemented` for a selected but unimplemented choice.** Not selected. It confuses a decision with evidence that the decision has been carried out. `accepted` preserves the distinction without leaving the choice marked as undecided.
- **Record every passing suggestion.** Not selected. The handoff should preserve information that affects future work rather than an unfiltered discussion log.

## Consequences and risks

Earlier capture can preserve design work across sessions and reduce repeated debate. It also adds document maintenance during discussions. The creation threshold must avoid turning transient suggestions into durable decisions or preserving a conversation transcript.

An agent recommendation must not silently become an approved choice. A chosen approach must not be described as implemented without evidence. Multiple participating skills must update one topic owner rather than create duplicate records.

The [checker regression tests](../../../tests/test_check_adr.py) cover acceptance of the new state value in English and Chinese, plus the existing structural checks, invalid-input rejection, and archive exclusions. They do not validate whether a record's prose agrees with its status. The [manual forward scenarios](../../../tests/scenarios/project_adr.md) own the original five isolated runs and the seven-scenario review-follow-up run. The latter also covers replacement of an accepted but unimplemented choice and renewed discovery after a new path and persistence constraint. Its refresh case reused a previously read record, so it does not establish previously unread-record retrieval. The scenario record identifies supplied instruction hashes, results, and limits.

The original external run passed with locally supplied skills whose installation ref was not recorded. Its retained instruction files match the pinned source and hashes in the [external dependency record](../../../tests/scenarios/project_adr.md#external-interview-workflow-with-project-conventions). The review-follow-up run retrieved those pinned files and verified their hashes. A fresh checkout needs matching external files to rerun that scenario; missing or mismatched dependencies make the rerun `skipped`, not passed. This does not alter the historical result.

These are finite evaluations of supplied skills and repository instructions. They do not establish automatic skill selection inside Claude Code or Codex, or reliability across all models and tasks. Format checks establish structure, state values, and local link paths; they do not establish truthful reasons, actual implementation, or successful resumption. Reconsider the capture rules if later agents still miss relevant topics or turn tentative advice into selected choices.
