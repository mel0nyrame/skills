# Maintain recap introductions through bounded candidate input

Status: implemented

## Problem

The reading guide combines authored routes and a generated topic catalog. Preserving all authored prose prevents normal maintenance from updating a route as the library grows. Allowing arbitrary guide replacement would let a packet overwrite generated entries and complicate concurrent publication.

## Decision

Permit structured candidate input for only the introduction before the catalog markers. Keep catalog generation and trailing prose under their existing ownership. Require explicit user approval bound to the exact candidate, including after integration changes its hash. Reader and publisher rules remain outside ordinary packet authoring.

Integrate introduction text independently from the catalog. A newer generated entry is not competing route authorship; actual concurrent introduction changes use the existing conflict and independent-review workflow. Keep base hashes and publication journals authoritative for versions. The [format contract](../../../skills/knowledge/recap/references/formats.md#guide-introduction) owns current input details; [operations](../../../skills/knowledge/recap/references/operations.md) owns execution.

## Alternatives

- Directly editing the formal guide bypasses candidate inspection, conflict handling and publication recovery.
- Moving every route to another topic still requires changing the existing guide pointer and creates a second navigation document even for a small library.
- Allowing whole-file guide input lets generated sections compete with authored prose and risks replacing unrelated trailing content.
- Merging generated catalog diffs as authored text creates avoidable conflicts when independent captures add topics.

## Consequences and risks

Existing topic/source packets keep their behavior. Older helpers reject the newly permitted guide input rather than silently accepting it. No knowledge-library migration or direct content rewrite is required. A guide without catalog markers treats its existing text as the introduction. Guide changes require a preview and approval, which adds an intentional maintenance step.

Temporary-library tests cover candidate-only writes, approval invalidation, generated-entry preservation, suffix preservation, concurrent guide conflict and blocked publication pending review. These tests do not establish semantic correctness of a reading route or power-loss durability. The existing lexical-search decision remains active and is not superseded.
