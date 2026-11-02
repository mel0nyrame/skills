# Choose a skill by its task and deliverable

English | [简体中文](README.zh.md) · [Installation](../README.md#install)

These skills guide how an AI assistant investigates, performs, and checks a task. Installation makes instructions callable; external connections and file permissions still come from your agent environment.

Start with the result you need. `clarify` provides a focused clarification round. `project-engineering` implements a project change and preserves useful engineering knowledge. `recap` turns conversations into independent topics. Their file outputs and operational effects differ substantially.

## Tasks and actual deliverables

| Skill and detailed guide | Suitable task | Typical result |
| --- | --- | --- |
| [clarify](thinking/clarify.md) | Establish the problem that needs solving | A question and later solution in chat, without a default file |
| [karpathy-guidelines](thinking/karpathy-guidelines.md) | Keep scope, assumptions, and verification under control | The original task's code, documents, or answer, with no fixed artifact directory |
| [project-engineering](engineering/project-engineering.md) | Implement features, fixes, or migrations under project rules | Relevant source and tests, plus engineering knowledge and decision updates when needed |
| [decisions](engineering/decisions.md) | Preserve important choices and maintain existing records | Markdown decisions and links in the project's ADR location |
| [git-ops](engineering/git-ops.md) | Review changes, form commits, and push within authorization | Review findings, local commit hashes, or push results depending on permission |
| [tech-write](engineering/tech-write.md) | Make technical prose understandable without the chat | Updated target prose or read-only review findings |
| [pr](engineering/pr.md) | Write a PR body from actual changes and evidence | A chat draft or an explicitly requested file such as `PR.md` |
| [firecrawl-mcp](research/firecrawl-mcp.md) | Read and extract web information | Sourced answers or structured data, saved locally only when requested |
| [tinyfish-mcp](research/tinyfish-mcp.md) | Read pages and interact with filters or controls when necessary | Extracted data and run status, with optional requested local saving |
| [context7-mcp](research/context7-mcp.md) | Consult matching library documentation | Documentation evidence, code examples, and explanations without default project edits |
| [recap](knowledge/recap.md) | Preserve or query reusable conversation knowledge | Topics, sources, reading routes, and change records in a separate knowledge library |

These are common outcomes, not files generated on every invocation. Individual guides explain actual locations, creation conditions, and acceptance checks.

## Start a task after installation

Complete installation using the linked guide, then choose an example. These names invoke the same bundled skill through different installation surfaces.

| Installation | Example |
| --- | --- |
| Standalone Codex skill | `$clarify` |
| This collection's Codex plugin | `$skills:clarify` |
| This collection's Claude Code plugin | `/skills:clarify` |

Follow the name with the task, input, and permitted actions. Replace example paths with your own. Reading these code blocks does not execute them.

```text
$skills:project-engineering
Add CSV export to this project, reusing existing permission checks. Establish
the editing location, implement the change, and run relevant checks. Report
changed files and useful knowledge preserved. Do not stage, commit, or push.
```

This authorizes implementation and validation while retaining Git-delivery boundaries. Request read-only investigation instead if you only want a proposal.

## Combine skills when the work calls for them

In the export teaching example, `project-engineering` establishes project rules and entry points before modifying functionality and tests. Useful findings go into existing engineering documents first. Only without an appropriate owner do fallback paths such as `docs/engineering/ENGINEERING.md` or `DATA.md` become relevant.

A lasting new choice brings in `decisions` for rationale and replacement relationships. Without target-project conventions, its default directory is `docs/adr/`. This collection's own records use `docs/agents/adr/`; that does not impose the same path on every other project.

Once code and prose are ready, `git-ops` can review them before you separately authorize a commit or push. Use the external `pr` for a review description when needed. A small change does not require every skill in sequence.

## Additional prerequisites for services and knowledge

Firecrawl and TinyFish need their corresponding MCP connections. MCP is the tool connection used by an agent; installed instructions cannot replace it. Reading results can stay in chat. CSV or JSON delivery needs an explicit path and local writing capability.

Context7 and PR come from external projects and require separate installation, described in their guides. This collection contains nine bundled skills. Its two submodules are upstream references using `update = none`, normally leaving complete upstream contents unchecked out. GitHub opens a pinned repository root when a submodule is clicked; the guides retain direct skill-directory links.

`recap` works with a separate knowledge library. Initialization, candidate inspection, and publication can create Git commits. Request an uncommitted draft if you want to inspect content first. Queries can update caches or lock files, so strict read-only tasks need an access-method check.

## Review the delivered result

Open reported files and verify their contents and source links. Check actual commands and outcomes behind test claims. A service job identifier needs a completion check before it represents final data.

Each guide includes outputs and acceptance checks. The corresponding `SKILL.md` owns detailed agent execution rules; these pages explain requests and results. This collection's maintenance rationale lives in [project ADRs](agents/adr/), which ordinary users need not read before trying a skill.
