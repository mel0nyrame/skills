# Project Engineering Knowledge Governance

Read this reference only when creating or extending repository instructions, engineering documents, indexes, or mechanical gates. Explicit project policy takes precedence over these defaults.

## Owners of current engineering knowledge

Standing instructions own short rules that apply to every change in their scope and link to detailed owners. Engineering documents own current intent that code cannot express well, such as architecture boundaries, reuse entry points, data ownership, and validation. Durable decisions own reasons, alternatives, and consequences. Code, configuration, and tests own current implementation and executable guarantees.

Give each explanation one owner where possible. Elsewhere, retain only the contract consumers need locally and stable links. Keep full rationale, directory inventories, and APIs with their owners.

When establishing ongoing ADR maintenance, use the project-integration workflow in `decisions` for standing triggers, directory contracts, and check commands. Reuse project entry points. On the first decision, fill gaps in existing instructions' maintenance rules. Wire mechanical checks only within the authorized governance scope.

When knowledge needs preserving and the project has neither a suitable owner nor a storage convention, use `docs/engineering/ENGINEERING.md` for relevant architecture, reusable assets, change entry points, validation, known constraints, observed conventions, or open questions. Use `docs/engineering/DATA.md` for persistent-data knowledge. Create only files and sections with actual content. These are fallback entry points, not mandatory filenames for every project.

## Prefer distributed discovery

When directories, metadata, filenames, search, or repository tooling reliably discover records, prefer one file per record or an owner-local structure. Avoid requiring every new record to modify corpus-wide files such as `ADR-INDEX.md`, `NOTES-INDEX.md`, or `DECISIONS-INDEX.md`. Such files create recurring merge conflicts across branches and worktrees.

Follow rules for existing project indexes. Keep indexes fully generated from authoritative metadata with freshness checks. A manually maintained index is justified only when it provides navigation that directories and search cannot express.

## Instruction and document budgets

Continuing growth in root instructions, subtree instructions, `ENGINEERING.md`, `DATA.md`, or other standing documents often signals misplaced ownership. Try these remedies in order:

```text
relocate → condense → split by real owner → raise budget
```

Preserve required consumer contracts when reducing length. Set budgets according to project structure rather than a universal word limit. Mature projects may enforce their own budgets in CI.

## Executable governance

Skills and maintainers own semantic judgments: whether a change needs a lasting record, whether an abstraction is appropriate, or whether an alternative retains value. Where practical, move stable, mechanically decidable invariants into tests, lint, CI, hooks, or repository gates, including:

- Required sections and consistency between paths and lifecycle.
- Synchronization of generated files, schemas, or code generation.
- Links, formatting, prohibited files, and project-specific budgets.

Add gates when the project already has a gate framework, the task explicitly requests them, or a new rule requires mechanical enforcement. Otherwise, record candidate invariants and owners so the project can adopt them as it matures, rather than generating an entire gate system for an unfamiliar project.
