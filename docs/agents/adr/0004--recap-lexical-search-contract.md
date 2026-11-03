# Keep recap retrieval local with a shared lexical contract

Status: implemented

## Problem

Recap must retrieve readable topics with Python's standard library and optional SQLite FTS5. Identifier punctuation, metadata and raw source paths can produce unrelated candidates or unhelpful excerpts. FTS5's tokenizer and text fallback can also disagree. Improving retrieval must preserve formal-topic boundaries and leave knowledge content and publication history authoritative.

## Decision

Keep FTS5 as the default cache and share a structured lexical projection with the fallback. Preserve complete identifiers while retaining component queries. Encode tokens before SQLite indexing so the database cannot introduce different token boundaries. Map those token matches to original character positions for body excerpts and file line numbers. Mask link metadata in place so excluding it does not invalidate those positions. The [search contract](../../../skills/knowledge/recap/references/search.md) owns the current consumer behavior and cache compatibility.

Treat index schema changes as disposable-cache rebuilds, not knowledge migrations. Projection changes require an index schema version change even if topic bytes are unchanged; otherwise a warm cache retains the previous search terms. Preserve the existing locks, revision checks and allowed-topic enumeration. This retains low installation cost and keeps every candidate traceable to current Markdown.

The existing packaging, submodule and release decisions remain active. This record does not supersede them or change installation and release policy.

## Alternatives

- Keeping whole-file indexing is simpler but lets schema, status and source-path tokens select unrelated topics and show frontmatter as evidence.
- Adding a separate exact-match filter after SQLite candidate selection retains two token interpretations. Sharing token boundaries also makes the explicit fallback predictable.
- Replacing the tokenizer with trigram loses short CJK `MATCH` queries without a second route and does not add synonym understanding.
- Adding embeddings, fusion or model reranking may help paraphrases and cross-language questions, but requires model and runtime management. No representative query evaluation yet justifies that cost. Reconsider when important literal-retrieval failures persist after keyword and alias retries.

## Consequences and risks

Stored caches rebuild when helper schema versions differ; alternating versions can cause repeated rebuilds. Encoded tokens and identifier components increase cache size and alter BM25 term statistics. Field weights express preferences and have not been tuned on real user queries.

The Markdown projection handles supported link forms rather than full rendering. Search still reads and hashes the corpus and does not infer synonyms. Regression tests in `tests/test_recap_search.py` cover matching, fallback agreement, scope exclusions, original line locations and cache reconstruction; they do not establish real-library retrieval quality or large-corpus performance.
