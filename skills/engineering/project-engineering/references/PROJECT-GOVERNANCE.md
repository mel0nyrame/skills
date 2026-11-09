# Project knowledge governance

Read when creating or extending instructions, engineering documents, capability entries, indexes, or gates. Project policy takes precedence.

## Information owners

- Standing instructions hold short recurring rules and conditional links.
- Engineering documents explain current boundaries, reuse entry points, ownership, and validation that implementation does not express well.
- Decision records preserve reasons, alternatives, and consequences.
- Code, configuration, and tests establish implementation and executable guarantees.

Give an explanation one owner; retain only necessary consumer contracts and links elsewhere. Document architecture conventions before mechanical style.

For requested ongoing decision maintenance, or the first decision in a project whose existing instruction entry point lacks maintenance rules, read [project integration](../../project-adr/references/PROJECT-INTEGRATION.md). It owns standing triggers, directory contracts, and the authorization boundary for wiring checks.

When no existing owner or project storage convention fits useful findings, use `docs/engineering/ENGINEERING.md` for architecture, reusable capabilities, editing entry points, checks, and open questions. Use `docs/engineering/DATA.md` for persistent-data knowledge. Create only files and sections with actual content.

## Capability entries

Keep reusable-capability entries bounded:

```text
Capability
Canonical implementation
Use for
Do not
Extension point
```

Verify canonical authority from project rules before requiring an implementation. Observed patterns guide investigation. API owners retain API details.

## Discovery and document growth

Prefer directories, metadata, filenames, search, and owner-local records. Follow existing index policy. A new manual central index needs navigation value that existing discovery cannot provide; generated indexes need authoritative metadata and freshness checks.

For growing instructions or engineering documents, try:

```text
relocate → condense → split by real owner → raise budget
```

Preserve required consumer contracts. Set budgets from project needs rather than a universal word limit.

## Mechanical gates

Use tests, lint, CI, or hooks for decidable invariants such as required sections, links, generated-output synchronization, and project budgets. Semantic judgments remain with maintainers.

Add gates through an existing framework, explicit task authorization, or a new rule requiring enforcement. Otherwise, record candidate invariants and their owners for later adoption. Keep integration proportional to the project.
