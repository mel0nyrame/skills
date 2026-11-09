# Project Prose forward check

## 2026-11-09 instruction refactor

A fresh independent agent received the revised skill and an isolated Python API project. The target Markdown derived from a module docstring through a supplied generator. The source contained draft-review framing and a disclaimer alongside an authentication/permission contract, a 100-row limit, ordered failures, UTF-8 output, and an incident reference. README belonged to another task. The parent supplied no expected answer.

Request:

```text
Rewrite docs/export.md for a new contributor. Remove private review context and
redundant disclaimers; verify facts against implementation. Preserve permissions,
limits, failure ordering, encoding, and useful rationale. Keep executable code and
README unchanged. Do not create a separate report, commit, or push.
```

Observed: the agent changed the source docstring and regenerated Markdown. It retained the contract and incident reason, checked the rendered link, and ran 11 API cases. The parent compared executable ASTs and the unrelated README; both were unchanged. Only source prose and its projection changed.

One scenario passed. This is a finite supplied-skill check, not a measurement of automatic discovery or all document types.

Evaluated `SKILL.md` SHA-256: `a9b27149ac10b0c48749bba3d5e40e769b3b26bad24c152622faf79683a0e246`.
