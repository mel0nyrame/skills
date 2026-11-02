"""Versioned Markdown contracts; JSON frontmatter is a strict YAML subset."""
from __future__ import annotations

from datetime import date
import json
from pathlib import PurePosixPath
import re
from urllib.parse import unquote, urlsplit


class DocumentError(ValueError):
    pass


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DocumentError('Duplicate frontmatter field: ' + key)
        result[key] = value
    return result


def object_keys(value, required, optional=()):
    if not isinstance(value, dict):
        raise DocumentError("Expected an object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing or extra:
        raise DocumentError(f"Invalid fields: missing={sorted(missing)}, unknown={sorted(extra)}")


def text(value, name):
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise DocumentError(f"{name} must be a nonempty string without NUL")
    return value


def strings(value, name, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise DocumentError(f"{name} must be {'a nonempty' if nonempty else 'an'} array")
    for item in value:
        text(item, name)
    if len(value) != len(set(value)):
        raise DocumentError(f"{name} contains duplicates")
    return value


def day(value, name):
    text(value, name)
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise DocumentError(f"{name} must be an actual YYYY-MM-DD date") from exc
    if parsed.isoformat() != value:
        raise DocumentError(f"{name} must use YYYY-MM-DD")
    return value


def split_document(content, legacy=False):
    text(content, "document")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)\Z", content, re.S)
    if not match:
        raise DocumentError("Document requires frontmatter delimited by ---")
    raw, body = match.groups()
    try:
        metadata = json.loads(raw, object_pairs_hook=unique_fields)
    except json.JSONDecodeError:
        if not legacy:
            raise DocumentError("Use JSON frontmatter; arbitrary YAML is not accepted")
        metadata = legacy_header(raw)
    if not isinstance(metadata, dict):
        raise DocumentError("Frontmatter must be an object")
    return metadata, body


def legacy_header(raw):
    """Read only the old recap flat scalars/lists; reject unsupported YAML."""
    result, active = {}, None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and active:
            result[active].append(legacy_scalar(line[4:]))
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*):(?: (.*))?", line)
        if not match or match[1] in result:
            raise DocumentError("Legacy YAML exceeds the supported flat scalar/list format")
        key, value = match.groups()
        active = key if value is None else None
        result[key] = [] if active else legacy_scalar(value)
    return result


def legacy_scalar(raw):
    if raw.startswith(('"', '[', '{')) or raw in ('true', 'false', 'null'):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise DocumentError("Unsupported legacy scalar; provide an explicit migration override") from exc
    if re.fullmatch(r"-?[0-9]+", raw):
        return int(raw)
    if not raw or raw.startswith(("'", '&', '*', '!', '|', '>')) or ' #' in raw:
        raise DocumentError("Unsupported legacy scalar; provide an explicit migration override")
    return raw


def render(metadata, body):
    return "---\n" + json.dumps(metadata, ensure_ascii=False, indent=2) + "\n---\n" + body


def check_body(body, title=None):
    text(body, "body")
    if re.search(r"^(?:<{7}|={7}|>{7})(?: |$)", body, re.M):
        raise DocumentError("Unresolved merge markers")
    if not re.search(r"^#\s+\S", body, re.M):
        raise DocumentError("Body requires a level-one title")
    prose = re.sub(r"^#{1,6}[^\n]*", "", body, flags=re.M).strip()
    if not prose:
        raise DocumentError("A title alone is not topic knowledge")
    if title and re.search(r"^#\s+(.+)$", body, re.M)[1].strip() != title:
        raise DocumentError("Body title must match metadata.title")


def build_topic(document, today, previous=None, draft=False):
    object_keys(document, ("title", "type", "acquired", "sources", "summary", "body"),
                ("aliases", "status", "verified", "event_date", "as_of", "version"))
    old = split_document(previous)[0] if previous else {}
    metadata = {"schema": "recap-topic/v2", "title": document["title"],
                "type": document["type"], "status": document.get("status", "draft" if draft else "formal"),
                "created": old.get("created", today), "updated": today,
                "acquired": old.get("acquired", document["acquired"]),
                "aliases": document.get("aliases", old.get("aliases", [])), "sources": document["sources"],
                "summary": document["summary"]}
    for key in ("verified", "event_date", "as_of", "version"):
        if key in document:
            metadata[key] = document[key]
        elif key in old:
            metadata[key] = old[key]
    content = render(metadata, document["body"])
    validate_topic(content, draft=draft)
    return content


def validate_topic(content, draft=False):
    meta, body = split_document(content)
    object_keys(meta, ("schema", "title", "type", "status", "created", "updated", "acquired",
                       "aliases", "sources", "summary"), ("verified", "event_date", "as_of", "version"))
    if meta["schema"] != "recap-topic/v2" or meta["type"] not in ("concept", "procedure", "research", "decision"):
        raise DocumentError("Unknown topic schema or type")
    allowed = ("draft",) if draft else ("formal", "archived")
    if meta["status"] not in allowed:
        raise DocumentError(f"Status must be one of {allowed}")
    for key in ("title", "summary"):
        text(meta[key], key)
        if '\n' in meta[key] or '\r' in meta[key]:
            raise DocumentError(f"{key} must be one line")
    if markdown_links(meta['summary']):
        raise DocumentError('summary is plain text; put citations in the body')
    for key in ("created", "updated", "acquired", "event_date", "as_of"):
        if key in meta:
            day(meta[key], key)
    if meta['created'] > meta['updated']:
        raise DocumentError("created is later than updated")
    strings(meta['aliases'], 'aliases')
    strings(meta['sources'], 'sources', nonempty=not draft)
    if 'version' in meta:
        text(meta['version'], 'version')
    if 'verified' in meta:
        object_keys(meta['verified'], ('date', 'scope', 'evidence'))
        day(meta['verified']['date'], 'verified.date')
        text(meta['verified']['scope'], 'verified.scope')
        strings(meta['verified']['evidence'], 'verified.evidence', nonempty=True)
    check_body(body, meta['title'])
    return meta, body


def validate_source(content):
    meta, body = split_document(content)
    object_keys(meta, ('schema', 'host', 'session_id', 'acquired', 'locator', 'cutoff', 'coverage'), ('legacy',))
    if meta['schema'] != 'recap-source/v2':
        raise DocumentError('Unknown source schema')
    for key in ('host', 'session_id', 'locator', 'cutoff'):
        text(meta[key], key)
    day(meta['acquired'], 'acquired')
    coverage = meta['coverage']
    object_keys(coverage, ('status', 'scope', 'inspected', 'gaps'), ('acceptance',))
    if coverage['status'] not in ('complete', 'partial', 'accepted-partial'):
        raise DocumentError('Unknown coverage status')
    text(coverage['scope'], 'coverage.scope')
    strings(coverage['inspected'], 'coverage.inspected', nonempty=True)
    strings(coverage['gaps'], 'coverage.gaps')
    if coverage['status'] == 'complete' and coverage['gaps']:
        raise DocumentError('Complete coverage cannot have declared gaps')
    if coverage['status'] == 'accepted-partial':
        text(coverage.get('acceptance'), 'coverage.acceptance')
    if 'legacy' in meta and not isinstance(meta['legacy'], dict):
        raise DocumentError('legacy must be an object')
    check_body(body)
    return meta, body


def markdown_links(body):
    return re.findall(r"\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)", body)


def local_target(owner, link):
    parsed = urlsplit(link)
    if parsed.scheme:
        if parsed.scheme not in ('http', 'https', 'mailto'):
            raise DocumentError('Unsupported link scheme')
        return None
    if parsed.netloc or parsed.path.startswith('/') or '\\' in parsed.path:
        raise DocumentError('Local links must be root-contained relative paths')
    if not parsed.path:
        return owner
    parts = list(PurePosixPath(owner).parent.parts)
    for component in unquote(parsed.path).split('/'):
        if component in ('', '.'):
            continue
        if component == '..':
            if not parts:
                raise DocumentError('Link escapes the knowledge root')
            parts.pop()
        else:
            if any(ord(c) < 32 for c in component):
                raise DocumentError('Control character in link')
            parts.append(component)
    return '/'.join(parts)


def validate_library(files):
    topics, sources = {}, {}
    for path, content in files.items():
        if path.startswith('sources/'):
            sources[path] = validate_source(content)[0]
        elif path.startswith('topics/'):
            topics[path] = validate_topic(content)[0]
    for path, content in files.items():
        if not (path.endswith('.md') and (path.startswith(('topics/', 'sources/')) or path == 'index.md')):
            continue
        body = split_document(content)[1] if path.startswith(('topics/', 'sources/')) else content
        links = markdown_links(body)
        resolved = set()
        for link in links:
            target = local_target(path, link)
            if target is None:
                continue
            if target not in files:
                raise DocumentError(f'Broken local link in {path}: {link}')
            if path.startswith('topics/') and target not in topics and target not in sources and target != 'index.md':
                raise DocumentError(f'Topic links to management material: {path}: {link}')
            resolved.add(target)
        if path in topics:
            for reference in topics[path]['sources']:
                target = local_target(path, reference)
                if target not in sources or target not in resolved:
                    raise DocumentError(f'{path}: source needs an existing, exact body link: {reference}')
                if sources[target]['coverage']['status'] == 'partial':
                    raise DocumentError('Unaccepted partial coverage cannot support a formal topic')
    return topics


def migrate_topic(content, today, kind='concept'):
    old, body = split_document(content, legacy=True)
    if old.get('schema') == 'recap-topic/v2':
        validate_topic(content)
        return content
    allowed = {'title', 'created', 'updated', 'acquired', 'aliases', 'sources'}
    if old.keys() - allowed:
        raise DocumentError('Legacy topic has unsupported fields; supply a migration override')
    if any(key not in old for key in ('created', 'updated', 'acquired')):
        raise DocumentError('Legacy dates are unknown; migration stopped rather than inventing dates')
    heading = re.search(r'^#\s+(.+)$', body, re.M)
    if not heading:
        raise DocumentError('Legacy topic lacks a body title; provide an explicit reviewed correction')
    title = heading[1].strip()
    aliases = list(old.get('aliases', []))
    if old.get('title') and old['title'] != title and old['title'] not in aliases:
        aliases.append(old['title'])
    paragraphs = [p.strip().replace('\n', ' ') for p in body.split('\n\n') if p.strip() and not p.lstrip().startswith(('#', '-', '|', '```'))]
    meta = {'schema': 'recap-topic/v2', 'title': title, 'type': kind, 'status': 'formal',
            'created': old['created'], 'updated': old['updated'],
            'acquired': old['acquired'], 'aliases': aliases,
            'sources': old.get('sources', []),
            'summary': re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', paragraphs[0]) if paragraphs else title}
    result = render(meta, body)
    validate_topic(result)
    return result
