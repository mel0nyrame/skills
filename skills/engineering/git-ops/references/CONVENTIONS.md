# Git Naming and Commit Splitting

Follow explicit target repository conventions. These defaults apply when a project has none.

## Branches

Format:

```text
<type>/<english-kebab-topic>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `perf`, `revert`.

Examples:

- `feat/memory-system`
- `fix/oauth-refresh`
- `docs/agent-workflow`

Use a short, recognizable English kebab-case topic. Rename pushed or shared branches only after explicit coordination.

## Commit titles

Format:

```text
<type>(<scope>): <Chinese description>
```

The optional `scope` uses short English kebab-case. Use an ASCII colon followed by one space. Write the description in Chinese so that a reader unfamiliar with the conversation can understand what the commit delivers. This output-language convention applies even though the skill instructions are in English; explicit repository conventions take precedence.

Examples:

- `feat(memory): 增加分层记忆检索`
- `fix(auth): 修复令牌刷新后会话丢失问题`
- `docs: 补充本地开发环境说明`

## Logical groups

Split by intentions that can be reviewed and reverted independently, rather than by file count or size:

- Split when one title cannot accurately describe the whole staged diff.
- Separate unrelated features, incidental refactors, and independent documentation work.
- Regroup a commit spanning several top-level modules when they share no acceptance criterion.
- Keep tests with the implementation they verify. Independent test infrastructure can have its own commit.
- Keep migrations, dependency upgrades, or generated files together when they are necessary for the feature to work. Explain the coupling in the commit body.

Large file or line counts are review signals. Each resulting commit should remain explainable and, where possible, buildable and verifiable. Preserve an indivisible change rather than creating incomplete commits.
