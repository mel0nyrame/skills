# Search contract

## Candidates and query terms

The helper indexes current formal topics only. Each topic has separate title, aliases, summary and Markdown-body fields. Frontmatter contributes only the three named reading fields; dates, status, schema and source paths are not search terms. Supported inline Markdown link destinations and reference-definition lines are excluded from the body projection; visible labels remain searchable. A path explicitly written as prose or code remains searchable. This projection is not a complete Markdown renderer.

Spaces separate required query groups. Each group must occur in at least one field. A phrase cannot cross field boundaries. Contiguous CJK characters form a phrase of adjacent character tokens after punctuation and whitespace normalization. Use `并发 写入` for two required fragments, rather than expecting `并发文件` or a complete question to match different wording.

ASCII names joined with `.`, `_` or `::` retain their complete identity, ignoring case. `session.prompt` does not match separate mentions of `session.stop` and `client.prompt`; `foo_bar` does not match `foo bar`. Components remain searchable, so `session` can find `session.prompt`. Other punctuation still separates groups. The helper performs no synonym generation, translation, stemming or semantic search. Try registered aliases and alternative short terms before reporting absence.

FTS5 ranks matching topics with title weight 3, alias and summary weights 2, and body weight 1. These are ranking preferences, not measured relevance guarantees. Without FTS5, the explicit text fallback uses the same fields and token boundaries, but returns path-ordered matches without BM25 ranking.

## Snippets and reading

Snippets come from the Markdown body. The helper chooses a line covering the most query groups, preferring explanation over a heading when coverage ties. It returns up to three lines, bounded to 350 characters. Long lines are cropped near a literal query fragment when one is present. The one-based `line` identifies the original file line where the excerpt starts; a cropped excerpt may begin within that line.

When only a title, alias or summary matches, the snippet starts at the first visible body line. It need not contain the matching alias or establish the answer. Read the current topic using the returned revision before answering. Source reads still require the owning topic's exact link. Search scope, publication locks and revision checks are unchanged.

## Cache ownership and compatibility

Markdown remains authoritative. `.state/index.sqlite` is a disposable local cache, excluded from publication. Index schema 2 stores structured fields and encoded tokens so SQLite cannot reinterpret identifier punctuation or accents. It rebuilds caches with missing or different schema versions from the current allowed topics, including unchanged files. Corruption also triggers reconstruction. This changes neither topic schema nor formal Git history and requires no knowledge migration.

Each search still reads and hashes the topic files before updating changed rows. No embedding models or additional packages are required. Old helper versions can rebuild their own cache schema but retain their own matching behavior; avoid alternating helper versions if repeated cache rebuilds matter.
