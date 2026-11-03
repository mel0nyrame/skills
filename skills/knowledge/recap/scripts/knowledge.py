#!/usr/bin/env python3
"""Capture/query knowledge through bounded reads and reviewed Git worktree publication."""
from __future__ import annotations
import argparse
from bisect import bisect_right
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import sys
sys.dont_write_bytecode = True
from urllib.parse import unquote, urlsplit
import documents
import storage
import workflow
from storage import (KnowledgeError, atomic_write, assert_clean, assert_no_pending,
                     digest, git, git_text, head, load_json, locked, private_mkdir, revision, safe_path)


def root_path(value=None):
    return Path(value or os.environ.get('RECAP_KNOWLEDGE_ROOT') or Path.home() / '.agents/knowledge').expanduser().resolve()


def fts_available():
    connection = sqlite3.connect(':memory:')
    try:
        connection.execute('CREATE VIRTUAL TABLE probe USING fts5(text)')
        return True
    except sqlite3.DatabaseError:
        return False
    finally:
        connection.close()


def doctor(root):
    marker = safe_path(root, '.state/library.json')
    migrated = marker.exists() and load_json(marker).get('schema') == 'recap-library/v2'
    return {'root': str(root), 'exists': root.is_dir(), 'fts5': fts_available(),
            'git': shutil.which('git') is not None,
            'migration_required': root.is_dir() and not migrated,
            'default_scope': 'topics/**/*.md', 'creates_files': False}

CJK = r"\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002ffff"
IDENTIFIER = r"[A-Za-z0-9_]+(?:(?:\.|::)[A-Za-z0-9_]+)*"
TOKEN = re.compile(rf"[{CJK}]|{IDENTIFIER}|[^\W_]+", re.UNICODE)
QUERY_GROUP = re.compile(rf"[{CJK}]+|{IDENTIFIER}|[^\W_]+", re.UNICODE)
INDEX_SCHEMA = "3"


def normalized_tokens(text):
    for match in TOKEN.finditer(text):
        token = match[0].casefold()
        # Encode complete tokens so SQLite cannot split punctuation or fold accents.
        yield "t" + token.encode("utf-8").hex(), match.start(), match.end()
        if re.search(r"[_\.:]", token):
            # Keep ordinary component queries useful without loosening full identifiers.
            for part in re.finditer(r"[^_\.:]+", match[0]):
                yield ("t" + part[0].casefold().encode("utf-8").hex(),
                       match.start() + part.start(), match.start() + part.end())


def normalize(text):
    return " ".join(token for token, _, _ in normalized_tokens(text))


def query_groups(query):
    return [normalize(t) for t in QUERY_GROUP.findall(query) if normalize(t)]


def topic_files(root):
    top = safe_path(root, "topics")
    if not top.exists():
        return
    for current, dirs, files in os.walk(top, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and
                         not (Path(current) / d).is_symlink())
        for name in sorted(files):
            path = Path(current) / name
            if name.startswith(".") or path.suffix.lower() != ".md" or path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            safe_path(root, relative)
            content = path.read_text(encoding="utf-8")
            try:
                metadata, _ = documents.split_document(content)
            except documents.DocumentError:
                metadata = {}
                if safe_path(root, '.state/library.json').exists():
                    raise
            if metadata.get('schema') == 'recap-topic/v2':
                metadata, _ = documents.validate_topic(content)
                if metadata['status'] != 'formal':
                    continue
            yield relative, content


def title_for(path, text):
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else PurePosixPath(path).stem


def topic_parts(text):
    try:
        metadata, body = documents.split_document(text, legacy=True)
    except documents.DocumentError:
        return {}, text, 0
    return metadata, body, text[:len(text) - len(body)].count("\n")


def visible_text(text):
    """Mask link metadata while preserving original character and line positions."""
    def blank(value):
        return re.sub(r"[^\r\n]", " ", value)

    def keep_group(match, group):
        start = match.start(group) - match.start()
        end = match.end(group) - match.start()
        return blank(match[0][:start]) + match[group] + blank(match[0][end:])

    def reference_id(value):
        return " ".join(value.split()).casefold()

    definitions = r"(?m)^ {0,3}\[([^]\n]+)\]:[^\n]*"
    references = {reference_id(match[1]) for match in re.finditer(definitions, text)}
    text = re.sub(definitions, lambda match: blank(match[0]), text)
    text = re.sub(r"\[([^]\n]+)\]\[([^]\n]*)\]",
                  lambda match: keep_group(match, 1)
                  if reference_id(match[2] or match[1]) in references else match[0], text)
    text = re.sub(r"\]\(<?[^\s)>]+>?(?:\s+[^)]*)?\)",
                  lambda match: "]" + blank(match[0][1:]), text)
    return re.sub(r"\[\[([^\]|\n]+)(?:\|([^]\n]+))?\]\]",
                  lambda match: keep_group(match, 2 if match[2] is not None else 1), text)


def search_fields(path, text):
    metadata, body, _ = topic_parts(text)
    return (title_for(path, body), "\n".join(metadata.get("aliases", [])),
            metadata.get("summary", ""), visible_text(body))


def contains_group(normalized, group):
    return " " + group + " " in " " + normalized + " "


def matching_spans(text, groups):
    """Locate encoded query groups in the original character coordinates."""
    tokens, bounds, cursor = [], {}, 1
    for token, start, end in normalized_tokens(text):
        bounds[cursor] = start
        tokens.append(token)
        cursor += len(token)
        bounds[cursor] = end
        cursor += 1
    normalized = " " + " ".join(tokens) + " "
    for group_id, group in enumerate(groups):
        position = normalized.find(" " + group + " ")
        while position >= 0:
            yield group_id, bounds[position + 1], bounds[position + 1 + len(group)]
            position = normalized.find(" " + group + " ", position + 1)


def snippet_for(text, query):
    groups = query_groups(query)
    _, body, offset = topic_parts(text)
    lines = body.splitlines(keepends=True)
    projected = visible_text(body)
    projected_lines = projected.splitlines(keepends=True)
    starts, cursor = [], 0
    for line in lines:
        starts.append(cursor)
        cursor += len(line)
    candidates = {}
    for group_id, start, end in matching_spans(projected, groups):
        i = bisect_right(starts, start) - 1
        candidates.setdefault(i, []).append((group_id, start, end))
    if candidates:
        i = max(candidates, key=lambda i: (
            len({match[0] for match in candidates[i]}),
            not re.match(r"^\s*#{1,6}\s", projected_lines[i]), -i))
    else:
        i = next((i for i, line in enumerate(projected_lines) if line.strip()), 0)
    start = 0
    if candidates and len(lines[i]) > 350:
        _, match_start, match_end = min(candidates[i], key=lambda match: match[1])
        context = max(0, min(80, 350 - (match_end - match_start)))
        start = max(0, match_start - starts[i] - context)
    snippet = "".join(lines[i:i + 3]).rstrip("\r\n")
    return offset + i + 1, snippet[start:start + 350]


def plain_search(root, query, limit):
    groups = query_groups(query)
    results = []
    if not groups:
        return []
    for path, text in topic_files(root):
        fields = [normalize(field) for field in search_fields(path, text)]
        if not all(any(contains_group(field, group) for field in fields) for group in groups):
            continue
        line, snippet = snippet_for(text, query)
        results.append({"path": path, "title": title_for(path, text),
                        "line": line, "snippet": snippet, "rank": None})
    return results[:limit]


def open_index(path):
    if not path.exists():
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(fd)
        except FileExistsError:
            pass
    conn = sqlite3.connect(path)
    try:
        if conn.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
            raise sqlite3.DatabaseError("Index integrity check failed")
        conn.execute("CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT)")
        version = conn.execute("SELECT value FROM metadata WHERE key='schema'").fetchone()
        if not version or version[0] != INDEX_SCHEMA:
            conn.execute("DROP TABLE IF EXISTS documents")
            conn.execute("DROP TABLE IF EXISTS search")
        conn.execute("CREATE TABLE IF NOT EXISTS documents (path TEXT PRIMARY KEY, sha TEXT, title TEXT, body TEXT)")
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS search USING fts5(path UNINDEXED, title, aliases, summary, body)")
        conn.execute("INSERT OR REPLACE INTO metadata VALUES ('schema',?)", (INDEX_SCHEMA,))
        return conn
    except Exception:
        conn.close()
        raise


def refresh(conn, root):
    known = dict(conn.execute("SELECT path,sha FROM documents"))
    seen = set()
    changes = {"added": 0, "updated": 0, "removed": 0}
    for path, text in topic_files(root):
        seen.add(path)
        sha = digest(text.encode())
        if known.get(path) == sha:
            continue
        fields = search_fields(path, text)
        title = fields[0]
        conn.execute("DELETE FROM documents WHERE path=?", (path,))
        conn.execute("DELETE FROM search WHERE path=?", (path,))
        conn.execute("INSERT INTO documents VALUES (?,?,?,?)", (path, sha, title, text))
        conn.execute("INSERT INTO search VALUES (?,?,?,?,?)", (path, *(normalize(field) for field in fields)))
        changes["updated" if path in known else "added"] += 1
    for path in known.keys() - seen:
        conn.execute("DELETE FROM documents WHERE path=?", (path,))
        conn.execute("DELETE FROM search WHERE path=?", (path,))
        changes["removed"] += 1
    conn.commit()
    return changes


def _search_unlocked(root, query, limit=8):
    if not root.is_dir():
        raise KnowledgeError("Knowledge root does not exist; search did not create it")
    if limit < 1 or limit > 100:
        raise KnowledgeError("limit must be between 1 and 100")
    groups = query_groups(query)
    if not groups:
        return {"engine": "fts5", "results": []}
    if not fts_available():
        return {"engine": "text-fallback", "scope": "topics/**/*.md",
                "warning": "SQLite FTS5 unavailable; no software installed",
                "results": plain_search(root, query, limit)}
    rebuilt = False
    path = safe_path(root, ".state/index.sqlite")
    conn = None
    try:
        try:
            conn = open_index(path)
            changes = refresh(conn, root)
        except sqlite3.DatabaseError:
            if conn is not None:
                conn.close()
            if path.exists():
                path.unlink()
            conn = open_index(path)
            changes = refresh(conn, root)
            rebuilt = True
        match = " AND ".join('"' + g.replace('"', '""') + '"' for g in groups)
        rows = conn.execute(
            "SELECT documents.path,documents.title,documents.body,bm25(search,0,3,2,2,1) "
            "FROM search JOIN documents ON documents.path=search.path "
            "WHERE search MATCH ? ORDER BY bm25(search,0,3,2,2,1),documents.path LIMIT ?",
            (match, limit)).fetchall()
    finally:
        if conn is not None:
            conn.close()
    results = []
    for path, title, body, rank in rows:
        line, snippet = snippet_for(body, query)
        results.append({"path": path, "title": title, "line": line,
                        "snippet": snippet, "rank": rank})
    return {"engine": "fts5-bm25", "scope": "topics/**/*.md", "refreshed": changes,
            "rebuilt": rebuilt, "results": results}


def _read_document(root, relative, purpose, owner=None):
    path = safe_path(root, relative)
    parts = PurePosixPath(relative).parts
    scopes = {"topic": "topics", "source": "sources", "draft": "drafts",
              "history": ".history", "state": ".state"}
    if purpose == "route":
        allowed = relative in ("index.md", "AGENTS.md")
    elif purpose == "changes":
        allowed = relative == "CHANGELOG.md"
    else:
        allowed = len(parts) > 1 and parts[0] == scopes.get(purpose)
    if not allowed:
        raise KnowledgeError("Path is outside the selected reading purpose")
    if purpose == "topic" and any(p.startswith(".") for p in parts[1:]):
        raise KnowledgeError("Hidden topic files are excluded")
    if purpose == "source":
        if not owner or not owner.startswith("topics/"):
            raise KnowledgeError("Source reads require --owner topics/FILE.md")
        owner_path = safe_path(root, owner)
        text = owner_path.read_text(encoding="utf-8")
        links = re.findall(r"\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)", text)
        links += re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", text)
        found = False
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            local = unquote(parsed.path)
            candidates = [(owner_path.parent / local).resolve(), (root / local).resolve()]
            if path.resolve() in candidates:
                found = True
                break
        if not found:
            raise KnowledgeError("Owner does not reference this exact source record")
    data = path.read_bytes()
    return {"path": relative, "purpose": purpose, "sha256": digest(data),
            "content": data.decode("utf-8")}



def check_read(root, expected_revision=None):
    if not root.is_dir():
        raise KnowledgeError('Knowledge root does not exist')
    assert_no_pending(root)
    if safe_path(root, '.state/library.json').exists():
        workflow.managed(root)
        assert_clean(root)
    current = revision(root)
    if expected_revision and expected_revision != current:
        raise KnowledgeError('Library revision changed; refresh related reads before answering')
    return current


def search(root, query, limit=8, expected_revision=None):
    if not root.is_dir():
        raise KnowledgeError('Knowledge root does not exist; search did not create it')
    with locked(root):
        current = check_read(root, expected_revision)
        result = _search_unlocked(root, query, limit)
        return {**result, 'revision': current}


def read_document(root, relative, purpose, owner=None, expected_revision=None):
    if not root.is_dir():
        raise KnowledgeError('Knowledge root does not exist')
    with locked(root):
        current = check_read(root, expected_revision)
        return {**_read_document(root, relative, purpose, owner), 'revision': current}


def read_version(root, relative, commit, owner=None):
    if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', commit):
        raise KnowledgeError('Historical reads require an exact commit object id')
    with locked(root):
        current = check_read(root)
        safe_path(root, relative)
        if not storage.allowed_path(relative):
            raise KnowledgeError('Historical path is outside publication material')
        if relative.startswith('sources/'):
            if not owner or not owner.startswith('topics/'):
                raise KnowledgeError('Historical source reads require the owning topic at the same commit')
            safe_path(root, owner)
            original = storage.git_content(root, commit, owner)
            if not original or relative not in {documents.local_target(owner, link) for link in documents.markdown_links(original.decode())}:
                raise KnowledgeError('Historical owner does not link to this source')
        data = storage.git_content(root, commit, relative)
        if data is None:
            raise KnowledgeError('Requested path does not exist at this commit')
        return {'path': relative, 'revision': commit, 'current_revision': current,
                'historical': True, 'sha256': digest(data), 'content': data.decode()}


initialize = workflow.initialize
inspect_bundle = workflow.inspect
recover = workflow.recover


def apply_bundle(root, filename, approved_sha256):
    packet, _ = workflow.raw_packet(filename)
    # apply consumes an inspected candidate; it never prepares or changes one implicitly.
    state = workflow.get_state(root, packet['id'])
    if state.get('packet_sha256') != digest(filename.read_bytes()):
        raise KnowledgeError('Packet differs from the inspected candidate')
    return workflow.publish(root, packet['id'], approved_sha256)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', help='Exact library root; otherwise RECAP_KNOWLEDGE_ROOT or ~/.agents/knowledge')
    parser.add_argument('--lock-timeout', type=float, default=30, help='Bounded lock wait, 0–30 seconds')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='Read-only capability report; never initializes')
    p = sub.add_parser('init', help='Explicitly initialize a new empty Git-backed library')
    p.add_argument('--language', choices=['en', 'zh'], default='en')
    p = sub.add_parser('search', help='Search only current formal topics; return a revision')
    p.add_argument('query')
    p.add_argument('--limit', type=int, default=8)
    p.add_argument('--revision')
    p = sub.add_parser('read', help='Read an exact current file for a bounded purpose')
    p.add_argument('path')
    p.add_argument('--purpose', required=True, choices=['topic', 'source', 'route', 'changes', 'draft', 'history', 'state'])
    p.add_argument('--owner')
    p.add_argument('--revision')
    p.add_argument('--at', help='Exact historical commit; requires --purpose history')
    p = sub.add_parser('begin', help='Create one operation-owned candidate worktree')
    p.add_argument('operation')
    p.add_argument('--writer-id', required=True)
    p = sub.add_parser('inspect', help='Validate a v2 change packet, prepare its worktree, return candidate hash')
    p.add_argument('packet')
    p = sub.add_parser('apply', help='Publish the exact inspected packet; alias of publish')
    p.add_argument('packet')
    p.add_argument('--approved-sha256', required=True)
    for name in ['integrate', 'status', 'diff', 'recover', 'cleanup']:
        p = sub.add_parser(name)
        p.add_argument('operation')
    for name in ['resolve', 'review', 'approve']:
        p = sub.add_parser(name)
        p.add_argument('operation')
        p.add_argument('file')
    p = sub.add_parser('publish', help='Publish one ready candidate as one formal commit')
    p.add_argument('operation')
    p.add_argument('--approved-sha256', required=True)
    p = sub.add_parser('migration-plan', help='Return a read-only migration proposal; source coverage needs explicit overrides')
    p.add_argument('--overrides')
    p = sub.add_parser('migrate', help='Create baseline and migrate only the exact reviewed plan')
    p.add_argument('plan')
    p.add_argument('--approved-sha256', required=True)
    args = parser.parse_args(argv)
    root = root_path(args.root)
    try:
        if not 0 <= args.lock_timeout <= 30:
            raise KnowledgeError('Lock timeout must be between 0 and 30 seconds')
        storage.LOCK_TIMEOUT = args.lock_timeout
        if args.command == 'doctor': result = doctor(root)
        elif args.command == 'init': result = initialize(root, args.language)
        elif args.command == 'search': result = search(root, args.query, args.limit, args.revision)
        elif args.command == 'read':
            if args.at and args.purpose != 'history':
                raise KnowledgeError('--at requires an explicit history purpose')
            result = read_version(root, args.path, args.at, args.owner) if args.at else read_document(root, args.path, args.purpose, args.owner, args.revision)
        elif args.command == 'begin': result = workflow.begin(root, args.operation, args.writer_id)
        elif args.command == 'inspect': result = inspect_bundle(root, Path(args.packet))
        elif args.command == 'apply': result = apply_bundle(root, Path(args.packet), args.approved_sha256)
        elif args.command in ('integrate', 'status', 'diff', 'recover', 'cleanup'):
            result = getattr(workflow, args.command)(root, args.operation)
        elif args.command in ('resolve', 'approve'): result = getattr(workflow, args.command)(root, args.operation, Path(args.file))
        elif args.command == 'review': result = workflow.record_review(root, args.operation, Path(args.file))
        elif args.command == 'publish': result = workflow.publish(root, args.operation, args.approved_sha256)
        elif args.command == 'migration-plan': result = workflow.migration_plan(root, Path(args.overrides) if args.overrides else None)
        else: result = workflow.migrate(root, Path(args.plan), args.approved_sha256)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (KnowledgeError, OSError, ValueError, TypeError, sqlite3.DatabaseError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
