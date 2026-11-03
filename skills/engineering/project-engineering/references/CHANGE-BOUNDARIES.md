# Conditional change boundaries

Read the matching section when a change affects generated artifacts or persistent data. Project rules own the actual entry points and validation commands.

## Generated artifacts

For generated OpenAPI, Protobuf, ORM types, database structures, clients, documentation, compiled assets, configuration, or prompts:

```text
Locate owner → edit owner → regenerate → review derived diff
```

By default, change generated or derived artifacts through their owner rather than patching files that regeneration will overwrite. Confirm the source/generated relationship and supported generation command before editing. Completion requires synchronized source and derived outputs, reviewed generated changes, and the applicable generation checks, or an explicit unresolved limitation.

## Persistent data

When adding persistent data or changing its schema, flow, ownership, isolation, lifecycle, deletion, or rebuild strategy, confirm:

- Owner, scope, namespace, and runtime source of truth.
- Schema, migration, and backward compatibility.
- Lifecycle, retention, deletion, and audit.
- Invalidation and rebuild of derived data, caches, and replicas, including propagation of source deletion.

Apply the same checks to agent memory, embeddings, vector indexes, summaries, checkpoints, and context caches. Derived data, caches, and indexes must not become a business source of truth without explicit design, migration, and compatibility policies.

Before implementation, identify affected stores and their authoritative owners, the compatible migration/rebuild approach, and validation. Resolve unknowns that materially change correctness or scope. Before delivery, verify affected data paths and recovery behavior and preserve non-obvious ownership or lifecycle findings through the skill's knowledge-maintenance workflow.
