# PR for a description reviewers can use

English | [简体中文](pr.zh.md) · [All guides](../README.md)

This introduces [Matt Pocock's upstream pr skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr). It mainly writes pull-request bodies explaining the change, validation, and merge risk. GitLab commonly calls the corresponding request an MR.

Its direct output is text. Upstream instructions do not require automatic hosted-request creation or a fixed local file on every invocation.

## Prepare the evidence

Give the assistant access to the actual diff and real validation results, or permission to obtain them. Identify project terminology, PR templates, and contribution rules when relevant.

If only the changed code is available, the assistant cannot invent a before screenshot or failing test. The description should distinguish what the evidence supports from what is missing.

Install this external skill separately; it is not one of this collection's nine bundled skills.

```sh
npx skills@latest add mattpocock/skills --skill pr
```

Select Codex for the standalone `$pr` invocation. Use upstream naming if installing its plugin. This collection's [submodule](../../skills/engineering/pr) is an upstream reference, not evidence of installation.

## Request an inspectable draft

This teaching example explicitly chooses the save location.

```text
$pr
Draft a PR body from the current diff and available test results. Save PR.md.
Make the important change understandable and explain evidence, reversibility,
and affected scope. State missing before evidence instead of inventing it.
Write only the draft. Do not create or update a hosted PR, commit, or push.
```

For copyable text without a file, request the draft in chat instead. Invoking `$pr` alone does not authorize platform publication.

## Understand the body

The upstream structure uses `Summary`, `Evidence`, and `Merge Danger` for its three sections. A compact tree, diff, or diagram can expose relationships that matter to a reviewer. A small change does not need a large diagram just to fill a template.

Evidence comes from actual test output, execution, or screenshots. Merge risk should explain reversibility and affected modules or consumers. Hard-to-reverse actions such as deleting data need a concrete account rather than a vague low-risk label.

For illustration, moving an export function from a page to a shared service can be explained with a shallow responsibility tree. That helps locate the change but cannot replace permission tests. It is a teaching example, not a claim that this collection implements export functionality.

## Deliverables and acceptance

| Your request | Expected artifact |
| --- | --- |
| Draft text only | A body in the conversation |
| Explicitly save `PR.md` | That local file, reopened to verify the save |
| Explicitly create a hosted PR | Additional platform tools and authorization; a real URL only after success |

Read the draft as someone absent from the chat. It should explain what changed, why, actual checks, and remaining risks. Filenames must match the diff, and evidence and links should be inspectable.

[git-ops](git-ops.md) handles commits and pushes. See the [upstream instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/pr/SKILL.md) and [third-party notices](../../THIRD_PARTY_NOTICES.md) for original rules and attribution. This guide does not store a copy of the upstream instruction body.
