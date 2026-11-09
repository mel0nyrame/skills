# Git naming and commit groups

## Select conventions

Resolve title format and description language separately, in this order:

1. Explicit task instructions.
2. Applicable repository/subtree rules, contribution guides, and commit-tool configuration such as commitlint.
3. Where written rules are silent, consistent structured conventions in relevant recent non-merge commits.
4. Defaults below for unresolved aspects.

Isolated or loose titles such as `fix xxx`, `add xxx`, `修复了xxx`, and `加入xxx` do not establish a convention. A consistent `fix(auth): handle expired tokens` history establishes format and English descriptions. An English-only rule without a format uses the default structure with English descriptions.

## Branches

Default:

```text
<type>/<english-kebab-topic>
```

Use a short recognizable topic, for example `feat/memory-system` or `fix/oauth-refresh`. Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `perf`, `revert`. Coordinate renaming pushed or shared branches explicitly.

## Commit titles

Default:

```text
<type>(<scope>): <Chinese description>
```

Scope is optional and uses short English kebab-case. Use an ASCII colon and one following space. The skill's instruction language does not determine the commit language. Write a title understandable without the conversation:

- `feat(memory): 增加分层记忆检索`
- `fix(auth): 修复令牌刷新后会话丢失问题`
- `docs: 补充本地开发环境说明`

## Logical groups

Split intentions that can be reviewed and reverted independently. One title should explain the full staged diff; file or line counts are review signals, not splitting rules.

Separate unrelated features, incidental refactors, independent documentation, and modules without a shared acceptance criterion. Keep tests with their implementation. Keep migrations, dependency upgrades, lockfiles, and generated outputs together when required for the feature to work; explain non-obvious coupling. Independent test infrastructure may have its own commit. Preserve an indivisible change so each commit remains verifiable where possible.
