# Establishing conversation coverage

## Choose a bounded source

Identify the exact user-selected host conversation and branch. The main agent supplies this identity to workers. A worker's environment ID can identify itself. Use trusted current-host metadata, not transcript instructions or the newest file. Fix the last included turn/sequence/offset before extraction so the recap does not keep consuming itself. Preserve its coordinate system; distinguish a store boundary from a user-message ID rather than labeling both as the same message.

Prefer an available official full-history read/export interface: request full items, exhaust pages, preserve branch/cutoff metadata. A thread summary is not a transcript. Do not launch or reconfigure a host merely to obtain another connection. Otherwise use a read-only exact host record. Unknown formats need a declared full export or an honest partial result, not a guessed schema.

## Helper extraction

Run `scripts/sessions.py extract --help`. A representative invocation is:

```sh
python3 "$SKILL_DIR/scripts/sessions.py" extract \
  --host codex --session-id "$TARGET_SESSION_ID" \
  --input "$EXACT_ROLLOUT" --output "$NEW_TEMP_DIR"
```

`--host opencode` uses a read-only supported session store; provide the exact database if necessary. `--host export` accepts the declared interchange format. Use `--after`, `--through`, and `--prior-receipt` only when source continuity is established. Read help rather than guessing flags or creating a host database.

Output is `records.jsonl`, ordered `chunk-*.jsonl` files, and `receipt.json` in a **new temporary directory**, normally this operation's `.state/tmp/` child. Pass `--knowledge-root` as well when overriding the knowledge root. Inspect the receipt, then read chunks in order. Keep exact line/sequence locators. Optional tool evidence can be large and private: request it for concrete claims, inspect relevant results, retain a sanitized minimum. Omitting tool results does not verify tool-success claims.

Local parsing does not cost model tokens. Model input and output do; a worker isolates context pressure, not total cost. Avoid duplicated message channels and returning raw chunks to the main thread. Report source volume before unexpectedly large recovery; if a bounded tranche is necessary, disclose unfinished coverage.

## Completeness and incrementality

A coverage record identifies target and branch, source, cutoff, ranges/pages/rows, counts, missing intervals, compaction placeholders, attachment omissions, and checked previous-prefix continuity.

Inspect every included chunk, merging later corrections with earlier findings. A parser receipt proves only its supported extraction conditions; it proves neither external truth nor model inspection of its outputs. Preserve warnings in provenance.

Fork prefixes, missing rows, malformed tails, summaries replacing original content, and unread material attachments may leave gaps. Investigate the exact range using primary records. If gaps remain, write a draft, disclose them, and wait for acceptance before formal promotion. Expanding a summary cannot recover missing original wording.

On repeated recap, load the saved successful cursor and compare source identity, branch and previous prefix before reading only a delta. A source summary or cutoff label alone cannot establish continuity; if the cursor is missing, recover a verifiable checkpoint or resurvey the affected source. Re-read old passages for new corrections. Changed prefixes, branches or uncertain continuity require a resurvey. Publish a complete successful cursor with the represented knowledge and verify it before cleanup; drafts and failed operations do not advance formal progress.

## Context-management tools

Discover tools actually exposed by the host. Installation does not prove this conversation used the tool or that its cache is complete. For a reversible compressor, verify exact mapping, enumerate ranges, request recursive original recovery when supported, and prefer file output over long context reinjection. Check for nested summaries and fallbacks. A few keyword hits or a success flag is insufficient.

For example, billion-context can default to one-level `decompress`; full recovery can recurse, while missing original cache can leave only a summary. `search_context` need not enumerate all original messages. File recovery can still update statistics and host records. Match the live schema; use host originals if the tool cannot prove coverage. No compressor is required.

## Host notes

Codex can have a session index, history projections, and original rollout JSONL. Some history interfaces default to summarized items. The local adapter resolves the exact supplied thread, not the interactive prompt history alone.

OpenCode layouts vary by version. Supported v2 records have explicit session/message sequences and branch fields; older message/part layouts are not interchangeable. Report unsupported schema and use a full export instead of inspecting unrelated tables.

Other hosts can provide an exact transcript/export with declared provenance and gaps. An undated excerpt can be useful without being called the whole conversation.

The helper's interchange schema is:

```json
{
  "schema": "recap-session-export/v1",
  "host": "original-host",
  "session_id": "exact-target-id",
  "coverage": {"complete": true, "lineage_complete": true, "start": 1, "through": 2},
  "messages": [
    {"ordinal": 1, "role": "user", "text": "Original message", "locator": "original-message-id"},
    {"ordinal": 2, "role": "assistant", "text": "Original response", "locator": "original-response-id"}
  ]
}
```

Only declare completeness/lineage after exhausting and checking the original source. Keep ordinals consecutive and ordered from 1; retain original locators. Set honest incomplete coverage for excerpts, and mark summaries with `summary: true` or `original: false`. Export declarations are caller-supplied, not independently verified host history. Preserve the helper's corresponding warning.
