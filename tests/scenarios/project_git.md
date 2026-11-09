# Project Git forward check

## 2026-11-09 instruction refactor

A fresh independent agent received the revised skill and an isolated Git project. Project rules required English Conventional Commits and a focused Python test. The export implementation and test were untracked; an unrelated notes update was already staged. No remote was configured. The parent supplied no expected answer.

Request:

```text
Commit only report-export.py and its test. Follow project naming and run required
checks. Preserve notes.txt content and staging. Do not push or create a PR.
```

Observed: the agent created a feature branch, passed the test, and committed exactly the two export files with `feat(export): add report title export`. The parent checked the commit file list and notes index blob; unrelated content and staging remained intact. No push or PR was attempted. Hooks were not disabled; this fixture did not test custom-hook execution.

One scenario passed. Remote delivery and actual platform publication are outside this fixture's coverage.

Evaluated `SKILL.md` SHA-256: `e3df3edd745a9f8975e663ee3ac16f758c006f7665ea0711dd072f2691506f40`.
