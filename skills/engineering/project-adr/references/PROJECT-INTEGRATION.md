# Integrate Decision Maintenance into a Project

Run all steps when the user requests ongoing maintenance. When writing the first decision in a project with an existing instruction entry point but no maintenance rules, add the standing trigger and directory contract. Wire checks only when governance integration is authorized or the project explicitly requires it. For read-only tasks, report recommendations and gaps while preserving files.

## 1. Establish entry points and the contract

Locate the project's actual `AGENTS.md`, `CLAUDE.md`, or other instruction entry point, decision directory, format template, and check commands. Reuse owners and edit the actual source behind shared or linked instructions. Create a supported instruction file only for an explicitly authorized governance task when no entry point exists.

Establish record conventions through [the skill's discovery rules](../SKILL.md#locate-rules-and-records): creation criteria, location, naming, state representation, template, and checks. Reuse rules in `docs/agents/` or another owner. Rules describe project actions and document locations without requiring an external skill installation.

Without a suitable rule owner, put these conventions in the decision directory's `README.md`, including task-entry retrieval, discussion-time capture, factual synchronization, supersession, and the project's actual archive rules. Base them on the skill and project conventions. Preserve valid short templates and optional states. When formats are mixed, establish allowed formats and existing exceptions for this scope. Finding another installed skill is not a reason to switch systems.

Completion: standing instructions contain a short trigger, one owner holds the detailed contract, and the template and record directory are discoverable from the entry point.

## 2. Add conditional maintenance rules

Adapt this short rule to project paths and language, merging it into existing instructions:

```markdown
## Decision maintenance

Before proposing or implementing related work, search active decisions by task topic, capabilities, constraints, paths, and configuration. Read relevant proposals, selected choices, rejection reasons, and open questions. State changed conditions before reconsidering an earlier choice.

During discussion, preserve meaningful constraints, evaluated rejection reasons, and substantial proposals that meet project creation criteria. Reuse one topic owner and distinguish selected conclusions, recommendations, open questions, and implementation evidence. Checkpoint meaningful progress before pausing or closing, even when no implementation follows.

Synchronize affected active records as implementation facts change. For new choices, check same-topic replacement and maintain links. Before delivery, check required records, state accuracy, and local links, then report update locations or why maintenance is unnecessary. See [decision rules](docs/adr/README.md) for formats, lifecycle, and validation.
```

Use links relative to module-local entry points. Instructions own actions and reading conditions that recur during work. Detailed creation criteria, formats, and lasting reasons remain with their owners. Merge the trigger into existing ADR rules rather than adding parallel thresholds. Preserve project authorization boundaries for read-only work, archive, and deletion.

Completion: future agents can discover when to read, capture, maintain, and check decisions from project instructions even without selecting this skill. `project-adr` owns the record contract; `project-engineering` supplies investigation and implementation triggers when available. External discussion skills reuse existing owners without requiring edits to their instructions.

## 3. Integrate minimal mechanical checks

Reuse project format, link, and lifecycle checks first. If the project uses the default English or Chinese structure and has no checker, copy [check_adr.py](../scripts/check_adr.py) into its existing script directory. It uses only the Python 3 standard library. It checks a title, one state, four ordered nonempty sections, and local Markdown link target paths. Project tools or semantic review own anchors, remote links, truthful reasons, supersession meaning, and omitted decisions.

Check new or maintained files first, for example:

```sh
python3 scripts/check_adr.py docs/adr/0001--storage-choice.md
```

Use directory-wide checks as a stable project command only after every active record uses an accepted default schema:

```sh
python3 scripts/check_adr.py docs/adr
```

Directory mode scans recursively, excluding directory guides, instruction files, and archive subtrees named `archive` or `archived`. Explicit archive paths are rejected. Use a complete English schema (`Status`, `Problem`, `Decision`, `Alternatives`, `Consequences and risks`) or the existing Chinese schema (`状态`, `问题`, `决策`, `备选方案`, `后果与风险`) per record. Both use the same state values. Mixed schemas are rejected.

Use matching project checks for short templates, custom states, or other structures. If none exist, review manually and report scope. Preserve valid formats rather than adding four sections or changing states merely to silence this checker. Migrate old records incrementally within authorization. While unmigrated formats remain, keep the project's changed-file checks instead of bulk rewriting history.

Wire available commands into existing local validation or CI and link them from the directory rules. Without a validation framework, provide an explicit local check using the project's normal mechanism. Creating an entire CI system is outside this default workflow.

Completion: run the integrated command. Valid records pass, and at least one missing-section, invalid-state, or broken-link sample fails. Report check coverage and anything not wired. Semantic review still covers every affected decision.
