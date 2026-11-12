# Integrate decision maintenance

For requested ongoing maintenance, complete this workflow. On the first decision, fill missing maintenance rules in an existing instruction entry point. New instruction files and check wiring require authorized governance scope or explicit project policy. Read-only tasks report gaps.

## 1. Establish the contract

Locate the actual instruction source, decision directory, template, lifecycle, and checks. Use [discovery](../SKILL.md#locate-rules-and-records) to resolve conventions. Preserve valid short formats, optional states, and existing exceptions.

Reuse a detailed rule owner; otherwise place the contract in the decision directory's `README.md`. Cover creation criteria, naming, format, retrieval, capture, synchronization, replacement, and archival. Use project actions and paths so the contract works without an external skill installation.

Complete when standing instructions point to one discoverable contract and record directory.

## 2. Add the standing trigger

Merge a short rule into the existing instructions, adapting paths and language:

```markdown
## Decision maintenance

Before related design or implementation, read relevant active decisions and their
reasons. Preserve meaningful constraints, evaluated alternatives, and substantial
proposals in one topic owner during discussion and before pausing. Distinguish
recommendations, selections, and implementation evidence. Synchronize affected
facts and replacement links with implementation; validate before delivery.
See [decision rules](docs/adr/README.md) for criteria, format, lifecycle, and checks.
```

Use paths relative to the actual entry point. Keep detailed criteria with the contract owner and preserve authorization boundaries. All workflows reuse it; external discussion skills remain unchanged. `project-adr` owns record content and lifecycle; `project-engineering` supplies investigation and implementation triggers.

Complete when future agents can discover retrieval, capture, and maintenance rules from project instructions.

## 3. Integrate focused checks

Reuse project checks. For the default schema without a checker, copy [check_adr.py](../scripts/check_adr.py) to the project's script directory. It requires Python 3's standard library. Check affected files first:

```sh
python3 scripts/check_adr.py docs/adr/2026-11-12-storage-choice.md
```

Use directory-wide checks only after all active records use accepted default schemas:

```sh
python3 scripts/check_adr.py docs/adr
```

The checker requires a title, one state, four ordered nonempty sections, and valid local link target paths. Each record uses either complete English headings (`Status`, `Problem`, `Decision`, `Alternatives`, `Consequences and risks`) or Chinese headings (`状态`, `问题`, `决策`, `备选方案`, `后果与风险`). Mixed schemas fail. Directory mode excludes guides, instructions, and `archive`/`archived` subtrees; explicit archive paths fail.

Custom states or templates use matching checks or manual review. Migrate incrementally within authorization; preserve valid formats. Wire into existing validation rather than adding a whole CI system. Until directory-wide compatibility is established, retain changed-file checks.

Complete when the integrated command passes valid records and rejects at least one missing-section, invalid-state, or broken-link sample. Report coverage and unwired checks. Semantic review covers reasons, anchors, remote references, replacements, and omitted decisions.
