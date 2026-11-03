# Git Naming and Commit Splitting

Resolve the target project's conventions first. The defaults below apply only to aspects left unspecified.

## Select conventions

Before drafting commit titles:

1. Apply explicit task instructions about naming format or description language.
2. Read applicable repository and subtree instructions, contribution guides, and commit-tool configuration such as commitlint. Written project requirements take precedence over historical examples.
3. Where written rules are silent, inspect relevant recent non-merge commits. Follow a consistent, structured naming pattern and its description language. Isolated examples or loose titles such as `fix xxx`, `add xxx`, `修复了xxx`, and `加入xxx` do not establish a naming convention.
4. Resolve format and language separately. Keep each requirement found above; use the defaults below only for unspecified aspects.

For example, a documented requirement or consistent history of `fix(auth): handle expired tokens` calls for English descriptions. An explicit English-only requirement with no title format keeps the default `<type>(<scope>):` structure and uses English descriptions. Unstructured history alone leaves the Chinese default in effect.

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

Default format:

```text
<type>(<scope>): <Chinese description>
```

The optional `scope` uses short English kebab-case. Use an ASCII colon followed by one space. When convention selection leaves the description language unspecified, write it in Chinese. Make the title understandable without the conversation. The skill's English instruction language does not determine the commit language.

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
