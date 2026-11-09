"""Cooperative worktree editing, reviewed integration and recoverable publication."""
from __future__ import annotations

from datetime import date
import difflib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

import documents as doc
from storage import (KnowledgeError, allowed_path, assert_clean, assert_no_pending,
                     atomic_write, digest, git, git_content, git_text, head, json_bytes,
                     library_files, load_json, locked, operation_id, pending, private_mkdir, safe_path,
                     unique_object)


GUIDE = '''# Knowledge reading boundaries

Use index.md for reading routes. Search only formal topics in topics/**/*.md.
Read CHANGELOG.md for changes. Follow a topic's exact source link to sources/.
Open drafts/ only for a selected draft; .history/ for named recovery/comparison.
Open .state/ only for exact operational, capture or review records.
.worktree/ holds unpublished candidates. .git/ holds versions, not current answers.
Use the helper's locked reads and returned revision; refresh related reads if it changes.
Resolve interrupted publication before reading. These are cooperative rules, not OS permissions.
'''

IGNORE = '''# Recap publication allowlist; staging is also explicit in the helper.
*
!*/
!index.md
!CHANGELOG.md
!AGENTS.md
!.gitignore
!topics/**/*.md
!sources/**/*.md
!.state/library.json
!.state/cursors/*.json
!.state/published/*.json
/.worktree/
/drafts/
/.history/
/.state/tmp/
/scripts/
'''


def managed(root, migration=False):
    if not (root / '.git').is_dir() or git_text(root, 'rev-parse', '--show-toplevel') != str(root.resolve()):
        raise KnowledgeError('Initialize/migrate this exact root; linked worktrees are not publication roots')
    marker = safe_path(root, '.state/library.json')
    if not marker.exists():
        raise KnowledgeError('Legacy library requires migration-plan and migrate')
    config = load_json(marker)
    if config.get('schema') != 'recap-library/v2' and not migration:
        raise KnowledgeError('Legacy library requires migration')
    branch = git_text(root, 'symbolic-ref', 'HEAD')
    if config.get('branch') != branch:
        raise KnowledgeError('Publication branch differs from recorded library branch')
    head(root)
    return config


def state_path(root, identifier):
    return safe_path(root, f'.state/operations/{operation_id(identifier)}.json')


def save_state(root, state):
    atomic_write(state_path(root, state['id']), json_bytes(state))


def get_state(root, identifier):
    state = load_json(state_path(root, identifier))
    if not isinstance(state, dict) or state.get('id') != identifier:
        raise KnowledgeError('Invalid operation state')
    return state


def worktree(root, state):
    path = safe_path(root, f'.worktree/{operation_id(state["id"])}')
    if not path.is_dir() or git_text(path, 'rev-parse', '--show-toplevel') != str(path):
        raise KnowledgeError('Candidate worktree is missing; retain operation state for recovery')
    common = Path(git_text(path, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve()
    if common != (root / '.git').resolve():
        raise KnowledgeError('Candidate belongs to a different Git repository')
    if git_text(path, 'symbolic-ref', 'HEAD') != state['branch']:
        raise KnowledgeError('Candidate branch identity changed')
    return path


def begin(root, identifier, writer_id, migration=False):
    operation_id(identifier)
    doc.text(writer_id, 'writer_id')
    with locked(root):
        managed(root, migration)
        assert_no_pending(root, 'migration' if migration else None)
        assert_clean(root)
        filename = state_path(root, identifier)
        if filename.exists():
            state = get_state(root, identifier)
            if state['writer_id'] != writer_id:
                raise KnowledgeError('Operation id belongs to another writer')
            return state
        destination = safe_path(root, f'.worktree/{identifier}')
        if destination.exists():
            raise KnowledgeError('Candidate directory already exists; it was not overwritten')
        private_mkdir(destination.parent)
        base = head(root)
        branch = 'refs/heads/recap-candidate/' + identifier
        if git(root, 'show-ref', '--verify', '--quiet', branch, check=False).returncode == 0:
            raise KnowledgeError('Temporary branch already exists')
        git(root, 'worktree', 'add', '-b', branch.removeprefix('refs/heads/'), str(destination), base)
        state = {'schema': 'recap-operation/v2', 'id': identifier, 'writer_id': writer_id,
                 'branch': branch, 'base': base, 'candidate': base, 'status': 'editing',
                 'authored': [], 'review_required': False, 'reviews': [], 'conflicts': [],
                 'migration': migration}
        save_state(root, state)
        return {**state, 'worktree': str(destination)}


def raw_packet(filename):
    packet = load_json(filename)
    doc.object_keys(packet, ('id', 'writer_id', 'changes'), ('risk',))
    operation_id(packet['id'])
    doc.text(packet['writer_id'], 'writer_id')
    if not isinstance(packet['changes'], list) or not packet['changes']:
        raise KnowledgeError('changes must be a nonempty array')
    if packet.get('risk', 'routine') not in ('routine', 'reserved'):
        raise KnowledgeError('risk must be routine or reserved')
    return packet, digest(filename.read_bytes())


def reserved_ok(state, fingerprint):
    approval = state.get('user_approval')
    return (isinstance(approval, dict) and approval.get('candidate_sha256') == fingerprint
            and bool(approval.get('evidence_locator')))


def approve(root, identifier, filename):
    approval = load_json(filename)
    doc.object_keys(approval, ('candidate_sha256', 'evidence_locator'))
    doc.text(approval['evidence_locator'], 'evidence_locator')
    with locked(root):
        assert_no_pending(root)
        state = get_state(root, identifier)
        ensure_candidate(root, state)
        if approval['candidate_sha256'] != state['fingerprint']:
            raise KnowledgeError('User approval differs from the previewed candidate')
        state['user_approval'] = approval
        save_state(root, state)
        return inspected_result(root, state)


def content_files(path):
    return {p: b.decode('utf-8') for p, b in library_files(path).items() if p.endswith('.md')}


TOPICS_START, TOPICS_END = '<!-- recap:topics:start -->', '<!-- recap:topics:end -->'


def guide_parts(content):
    """Only the prefix is authorable; the catalog and trailing prose retain ownership."""
    if content.count(TOPICS_START) != content.count(TOPICS_END) or content.count(TOPICS_START) > 1:
        raise KnowledgeError('Guide has malformed managed-section markers')
    if TOPICS_START not in content:
        return content, '', ''
    start, end = content.index(TOPICS_START), content.index(TOPICS_END)
    if end < start:
        raise KnowledgeError('Guide has reversed managed-section markers')
    end += len(TOPICS_END)
    return content[:start], content[start:end], content[end:]


def render_item(item, prior, today):
    doc.object_keys(item, ('path', 'expected_sha256', 'kind', 'reason', 'evidence'), ('document', 'content'))
    relative = item['path']
    if not isinstance(relative, str) or not (relative == 'index.md' or
            (relative.startswith(('topics/', 'sources/', '.state/cursors/')) and allowed_path(relative))):
        raise KnowledgeError('Model-authored paths are topics/, sources/, exact capture cursors or the index.md introduction')
    doc.text(item['reason'], 'reason')
    doc.strings(item['evidence'], 'evidence', nonempty=True)
    if any('\n' in value or '\r' in value for value in [item['reason'], *item['evidence']]):
        raise KnowledgeError('Change reasons and evidence locators must be single-line values')
    if item['kind'] not in ('add', 'update', 'correct', 'archive'):
        raise KnowledgeError('Unknown change kind')
    expected = digest(prior) if prior is not None else None
    if item['expected_sha256'] != expected:
        raise KnowledgeError(f'{relative}: expected hash differs from the operation base; reread it')
    if ('document' in item) == ('content' in item):
        raise KnowledgeError('Each change needs exactly one of document or content')
    if relative == 'index.md':
        if prior is None or item['kind'] not in ('update', 'correct') or 'document' not in item:
            raise KnowledgeError('Guide introductions require an existing index.md, update/correct and document.body')
        doc.object_keys(item['document'], ('body',))
        body = item['document']['body']
        doc.check_body(body)
        if '<!-- recap:' in body:
            raise KnowledgeError('Guide introduction cannot contain helper-managed markers')
        _, catalog, suffix = guide_parts(prior.decode())
        result = body.rstrip() + '\n\n' + catalog + suffix
    elif relative.startswith('topics/'):
        if 'document' not in item:
            raise KnowledgeError('Topics require structured document input; helper owns file timestamps')
        result = doc.build_topic(item['document'], today, prior.decode() if prior else None)
    else:
        if 'content' not in item:
            raise KnowledgeError('Sources and cursors require complete content')
        doc.text(item['content'], 'content')
        result = item['content']
        if relative.startswith('sources/'):
            doc.validate_source(result)
        else:
            receipt = json.loads(result)
            validate_cursor(receipt)
    return result.encode()


def validate_cursor(receipt):
    if not isinstance(receipt, dict) or receipt.get('schema') != 'recap-session-receipt/v1' or receipt.get('status') != 'complete':
        raise KnowledgeError('Cursor needs a complete recap-session-receipt/v1 receipt')
    for key in ('host', 'session_id', 'captured_at'):
        doc.text(receipt.get(key), key)
    source, interval = receipt.get('source'), receipt.get('range')
    if not isinstance(source, dict) or not isinstance(interval, dict):
        raise KnowledgeError('Cursor needs source identity and inspected range')
    doc.text(source.get('locator'), 'source.locator')
    if not re.fullmatch(r'[0-9a-f]{64}', str(source.get('prefix_sha256', ''))):
        raise KnowledgeError('Cursor needs the frozen source prefix SHA-256')
    after, through = interval.get('after'), interval.get('through')
    if type(after) is not int or type(through) is not int or after < -1 or through < 0 or through < after:
        raise KnowledgeError('Cursor range requires ordered integer after/through bounds')
    for key in ('missing', 'unread_attachments', 'errors', 'unknown_envelopes'):
        if receipt.get(key, []) != []:
            raise KnowledgeError('Complete cursor contains unresolved coverage gaps')
    represented = receipt.get('represented_by')
    doc.object_keys(represented, ('topics', 'sources'))
    for kind in ('topics', 'sources'):
        doc.strings(represented[kind], 'represented_by.' + kind, nonempty=True)
        if any(not p.startswith(kind + '/') or not allowed_path(p) for p in represented[kind]):
            raise KnowledgeError('Cursor representation paths must name topics and sources')
    def exclude_raw(value):
        if isinstance(value, dict):
            if value.keys() & {'messages', 'records', 'raw_transcript', 'transcript', 'encrypted_content'}:
                raise KnowledgeError('Capture cursors cannot archive raw messages')
            for item in value.values(): exclude_raw(item)
        elif isinstance(value, list):
            for item in value: exclude_raw(item)
    exclude_raw(receipt)


def check_cursors(tree, state, rendered=None):
    rendered = rendered or {}
    authored = set(state['authored'])
    for path in authored:
        if not path.startswith('.state/cursors/'):
            continue
        receipt = (json.loads(rendered[path], object_pairs_hook=unique_object) if path in rendered
                   else load_json(safe_path(tree, path)))
        validate_cursor(receipt)
        represented = receipt['represented_by']
        if not set(represented['topics'] + represented['sources']) <= authored:
            raise KnowledgeError('Capture cursor must publish its represented topics and sources in the same batch')
        matched = False
        used_sources = set()
        for topic in represented['topics']:
            content = rendered[topic].decode() if topic in rendered else safe_path(tree, topic).read_text()
            metadata, _ = doc.validate_topic(content)
            linked = {doc.local_target(topic, reference) for reference in metadata['sources']}
            related = linked & set(represented['sources'])
            if not related:
                raise KnowledgeError('Represented topic must cite a represented source')
            used_sources |= related
        if used_sources != set(represented['sources']):
            raise KnowledgeError('Represented sources must support the represented topics')
        for source in represented['sources']:
            content = rendered[source].decode() if source in rendered else safe_path(tree, source).read_text()
            metadata, _ = doc.validate_source(content)
            matched = matched or (metadata['host'] == receipt['host'] and metadata['session_id'] == receipt['session_id'])
        if not matched:
            raise KnowledgeError('Cursor session identity differs from its represented source records')


def escape_label(value):
    return value.replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]')


def catalogs(tree, state):
    files = content_files(tree)
    topics = {p: doc.validate_topic(c)[0] for p, c in files.items() if p.startswith('topics/')}
    start, end = TOPICS_START, TOPICS_END
    current = files.get('index.md', '# Knowledge\n')
    prefix, _, suffix = guide_parts(current)
    chinese = bool(re.search(r'[\u3400-\u9fff]', current))
    lines = [start, '## 专题' if chinese else '## Topics', '']
    for path, meta in sorted(topics.items()):
        if meta['status'] == 'formal':
            lines.append(f'- [{escape_label(meta["title"])}](<{path}>) — {meta["summary"]}')
    lines += ['', end]
    section = '\n'.join(lines)
    if start in current:
        current = prefix + section + suffix
    else:
        current = current.rstrip() + '\n\n' + section + '\n'
    atomic_write(safe_path(tree, 'index.md'), current.encode())
    changes = safe_path(tree, 'CHANGELOG.md')
    # Rebuild this operation's append from its integration base, never append it twice.
    base_log = git_content(tree, state['base'], 'CHANGELOG.md') or b'# Knowledge changes\n'
    entry = [f'\n\n## {date.today().isoformat()} · {state["id"]}', '']
    for item in state['packet']['changes']:
        path = item['path']
        entry.append(f'- [{escape_label(path)}](<{path}>) · {item["kind"]} · {item["reason"]}')
        entry.append('  ' + ('依据' if chinese else 'Evidence') + ' · ' + '; '.join(item['evidence']))
    atomic_write(changes, base_log.rstrip() + '\n'.join(entry).encode() + b'\n')


def fingerprint(tree, state):
    files = library_files(tree)
    own_record = f'.state/published/{state["id"]}.json'
    return digest(json_bytes({'base': state['base'], 'id': state['id'], 'writer_id': state['writer_id'],
                             'packet_sha256': state['packet_sha256'],
                             'files': {p: digest(b) for p, b in files.items() if p != own_record}}))


def commit_candidate(tree, message):
    changed = git(tree, 'status', '--porcelain=v1', '-z', '--untracked-files=all').stdout
    if not changed:
        return head(tree)
    # Enumerate our allowlist instead of ever staging an entire directory.
    paths = sorted(library_files(tree))
    if paths:
        git(tree, 'add', '--', *paths)
    unexpected = git(tree, 'diff', '--name-only', '-z', '--cached').stdout.decode().split('\0')
    if any(not allowed_path(p) for p in unexpected if p):
        raise KnowledgeError('Candidate stages material outside the publication allowlist')
    git(tree, 'commit', '--allow-empty', '-m', message)
    assert_clean(tree)
    return head(tree)


def check_candidate_scope(tree, state):
    expected = set(state['authored']) | {'index.md', 'CHANGELOG.md', f'.state/published/{state["id"]}.json'}
    if state.get('migration'):
        expected |= {'AGENTS.md', '.state/library.json'}
    for path, data in library_files(tree).items():
        if data != git_content(tree, state['base'], path) and path not in expected:
            raise KnowledgeError(f'Candidate contains an unrelated change: {path}')
    removed = git(tree, 'diff', '--name-only', '--diff-filter=D', state['base']).stdout
    if removed:
        raise KnowledgeError('Candidate removes tracked material; explicit structural work is required')


def reserved_reasons(root, tree, state):
    reasons = []
    if state['packet'].get('risk') == 'reserved':
        reasons.append('writer-declared reserved change')
    for item in state['packet']['changes']:
        path = item['path']
        if path == 'index.md':
            reasons.append('index.md: changes the reading-route introduction')
        if not path.startswith('topics/'):
            continue
        new_meta, new_body = doc.validate_topic(safe_path(tree, path).read_text())
        previous = git_content(root, state['base'], path)
        if item['kind'] == 'archive' or new_meta['status'] == 'archived':
            reasons.append(path + ': archive')
        if previous:
            old_meta, old_body = doc.validate_topic(previous.decode())
            if not set(old_meta['sources']) <= set(new_meta['sources']):
                reasons.append(path + ': removes source contributions')
            # A mechanical trigger for review, not proof of semantic preservation.
            retained = sum(m.size for m in difflib.SequenceMatcher(None, old_body, new_body, autojunk=False).get_matching_blocks())
            if len(old_body) >= 200 and retained < len(old_body) * 0.7:
                reasons.append(path + ': removes or rewrites over 30 percent of prior prose')
    return reasons


def inspected_result(root, state):
    return {'id': state['id'], 'status': state['status'], 'worktree': str(safe_path(root, '.worktree/' + state['id'])),
            'base_revision': state['base'], 'approval_sha256': state.get('fingerprint'),
            'packet_sha256': state.get('packet_sha256'), 'review_required': state['review_required'],
            'review_rounds': len(state['reviews']), 'conflicts': state.get('conflicts', []),
            'candidate_commit': state['candidate'], 'reserved_reasons': state.get('reserved_reasons', [])}


def inspect(root, filename):
    packet, packet_sha = raw_packet(filename)
    state = begin(root, packet['id'], packet['writer_id'])
    with locked(root):
        managed(root)
        assert_no_pending(root)
        assert_clean(root)
        state = get_state(root, packet['id'])
        if state['status'] in ('published', 'cleaned'):
            if state.get('packet_sha256') != packet_sha:
                raise KnowledgeError('Published operation id cannot be reused for different content')
            return inspected_result(root, state)
        if state['status'] != 'editing':
            if state.get('packet_sha256') == packet_sha:
                return inspected_result(root, state)
            raise KnowledgeError('Use resolve for an existing candidate; preserve its review rounds and base')
        tree = worktree(root, state)
        assert_clean(tree)
        seen, rendered = set(), {}
        for item in packet['changes']:
            if not isinstance(item, dict):
                raise KnowledgeError('Every change must be an object')
            relative = item.get('path')
            safe_path(tree, relative)
            if relative in seen:
                raise KnowledgeError('Duplicate changed path')
            seen.add(relative)
            rendered[relative] = render_item(item, git_content(root, state['base'], relative), date.today().isoformat())
        files = content_files(tree)
        files.update({p: b.decode() for p, b in rendered.items() if p.endswith('.md')})
        doc.validate_library(files)
        state.update(packet=packet, packet_sha256=packet_sha, authored=sorted(seen))
        check_cursors(tree, state, rendered)
        for relative, data in rendered.items():
            atomic_write(safe_path(tree, relative), data)
        catalogs(tree, state)
        doc.validate_library(content_files(tree))
        check_cursors(tree, state)
        check_candidate_scope(tree, state)
        state['reserved_reasons'] = reserved_reasons(root, tree, state)
        state['candidate'] = commit_candidate(tree, 'Candidate ' + state['id'])
        state['fingerprint'] = fingerprint(tree, state)
        state['status'] = 'ready'
        save_state(root, state)
        return inspected_result(root, state)


def ensure_candidate(root, state, dirty=False):
    tree = worktree(root, state)
    if head(tree) != state['candidate']:
        raise KnowledgeError('Candidate HEAD changed outside this operation')
    ignored = git(tree, 'ls-files', '--others', '--ignored', '--exclude-standard', '-z').stdout.decode().split('\0')
    ignored = [p for p in ignored if p]
    if ignored:
        raise KnowledgeError('Candidate contains extra ignored files: ' + json.dumps(ignored, ensure_ascii=False) +
                             f'; preserve selected files outside the candidate, e.g. .state/tmp/{state["id"]}/preserved/, then retry. No files were removed')
    if not dirty:
        assert_clean(tree)
        if state.get('fingerprint') and fingerprint(tree, state) != state['fingerprint']:
            raise KnowledgeError('Candidate contents differ from the inspected revision')
    return tree


def integrate(root, identifier):
    with locked(root):
        managed(root)
        assert_no_pending(root)
        assert_clean(root)
        state = get_state(root, identifier)
        if state['status'] not in ('ready', 'needs-review', 'needs-revision'):
            raise KnowledgeError('Prepare or resolve this candidate before integrating')
        tree = ensure_candidate(root, state)
        latest = head(root)
        if latest == state['base']:
            return inspected_result(root, state)
        merged, conflicts, touched = {}, [], []
        latest_guide = None
        for path in state['authored']:
            old = git_content(root, state['base'], path)
            ours = safe_path(tree, path).read_bytes()
            theirs = git_content(root, latest, path)
            if path == 'index.md':
                if old is None or theirs is None:
                    raise KnowledgeError('Guide deletion requires explicit structural maintenance')
                # Generated catalog changes do not constitute concurrent guide authorship.
                latest_guide = guide_parts(theirs.decode())
                old, ours, theirs = (guide_parts(value.decode())[0].encode() for value in (old, ours, theirs))
            if theirs == old or theirs == ours:
                merged[path] = ours
                continue
            if ours == old:
                if theirs is None:
                    raise KnowledgeError('Concurrent deletion requires explicit user maintenance')
                merged[path] = theirs
                continue
            touched.append(path)
            if old is None or theirs is None or not path.endswith('.md'):
                conflicts.append(path)
                merged[path] = ours
                continue
            with tempfile.TemporaryDirectory(prefix='merge-', dir=safe_path(root, '.state')) as temporary:
                temp = Path(temporary)
                for name, data in [('ours', ours), ('base', old), ('theirs', theirs)]:
                    atomic_write(temp / name, data)
                result = git(tree, 'merge-file', '-p', '-L', 'candidate', '-L', 'base', '-L', 'published',
                             str(temp / 'ours'), str(temp / 'base'), str(temp / 'theirs'), check=False)
                # merge-file returns the number of conflicts, capped at 127.
                if result.returncode < 0 or result.returncode >= 128:
                    raise KnowledgeError('Three-way merge failed; candidate retained')
                merged[path] = result.stdout
                if result.returncode:
                    conflicts.append(path)
        if latest_guide is not None:
            merged['index.md'] += (latest_guide[1] + latest_guide[2]).encode()
        # The previous candidate is a clean, committed, operation-owned snapshot.
        # Replace only this disposable worktree's index/files, never the main root.
        git(tree, 'read-tree', '--reset', '-u', latest)
        state['base'] = latest
        state['review_required'] = state['review_required'] or bool(touched)
        state['conflicts'] = conflicts
        for path, data in merged.items():
            atomic_write(safe_path(tree, path), data)
        if not conflicts:
            try:
                catalogs(tree, state)
                doc.validate_library(content_files(tree))
                check_cursors(tree, state)
                check_candidate_scope(tree, state)
                state['reserved_reasons'] = reserved_reasons(root, tree, state)
            except (doc.DocumentError, KnowledgeError) as exc:
                conflicts = state['conflicts'] = list(state['authored'])
                state['integration_error'] = str(exc)
        if conflicts:
            state['status'] = 'conflict'
            state['fingerprint'] = None
        else:
            state['candidate'] = commit_candidate(tree, 'Integrate published changes ' + identifier)
            state['fingerprint'] = fingerprint(tree, state)
            state['status'] = 'needs-review' if state['review_required'] else 'ready'
        save_state(root, state)
        return inspected_result(root, state)


def resolve(root, identifier, filename):
    replacements = load_json(filename)
    doc.object_keys(replacements, ('changes',))
    if not isinstance(replacements['changes'], list) or not replacements['changes']:
        raise KnowledgeError('Resolution needs a nonempty changes array')
    with locked(root):
        managed(root)
        assert_no_pending(root)
        state = get_state(root, identifier)
        if state['status'] not in ('conflict', 'needs-revision'):
            raise KnowledgeError('Only a conflicted or reviewer-rejected candidate can be resolved')
        if len(state['reviews']) >= 2:
            raise KnowledgeError('Two review rounds exhausted; retain worktree and ask the user')
        tree = ensure_candidate(root, state, dirty=state['status'] == 'conflict')
        changes, seen = {}, set()
        for item in replacements['changes']:
            if not isinstance(item, dict):
                raise KnowledgeError('Resolution change must be an object')
            path = item.get('path')
            if path not in state['authored'] or path in seen:
                raise KnowledgeError('Resolution can change each authored path once')
            seen.add(path)
            changes[path] = render_item(item, git_content(root, state['base'], path), date.today().isoformat())
        if not set(state.get('conflicts', [])) <= seen:
            raise KnowledgeError('Resolve every reported conflict in the same resolution')
        files = content_files(tree)
        files.update({p: b.decode() for p, b in changes.items() if p.endswith('.md')})
        doc.validate_library(files)
        for path, data in changes.items():
            atomic_write(safe_path(tree, path), data)
        # Keep audit reasons/evidence synchronized with the resolved input.
        replacement_by_path = {item['path']: item for item in replacements['changes']}
        state['packet']['changes'] = [replacement_by_path.get(item['path'], item) for item in state['packet']['changes']]
        catalogs(tree, state)
        doc.validate_library(content_files(tree))
        check_cursors(tree, state)
        check_candidate_scope(tree, state)
        state['reserved_reasons'] = reserved_reasons(root, tree, state)
        state['candidate'] = commit_candidate(tree, 'Resolve candidate ' + identifier)
        state.update(status='needs-review', conflicts=[], review_required=True)
        state['fingerprint'] = fingerprint(tree, state)
        save_state(root, state)
        return inspected_result(root, state)


def record_review(root, identifier, filename):
    receipt = load_json(filename)
    doc.object_keys(receipt, ('operation', 'candidate_sha256', 'reviewer_id', 'evidence_locator', 'verdict', 'findings'))
    for key in ('reviewer_id', 'evidence_locator'):
        doc.text(receipt[key], key)
    doc.strings(receipt['findings'], 'findings')
    if receipt['verdict'] not in ('approve', 'revise', 'blocked'):
        raise KnowledgeError('Review verdict must be approve, revise or blocked')
    if receipt['verdict'] == 'approve' and receipt['findings']:
        raise KnowledgeError('An approval cannot retain unresolved findings')
    with locked(root):
        assert_no_pending(root)
        state = get_state(root, identifier)
        if not state['review_required'] or state['status'] not in ('needs-review', 'needs-revision'):
            raise KnowledgeError('This candidate is not awaiting independent review')
        ensure_candidate(root, state)
        if receipt['operation'] != identifier or receipt['candidate_sha256'] != state['fingerprint']:
            raise KnowledgeError('Review does not match the exact candidate')
        if receipt['reviewer_id'] == state['writer_id']:
            raise KnowledgeError('Reviewer must be a different host agent identity')
        if len(state['reviews']) >= 2:
            raise KnowledgeError('Two review rounds exhausted; ask the user')
        if any(r['candidate_sha256'] == receipt['candidate_sha256'] for r in state['reviews']):
            raise KnowledgeError('This candidate already has a review; resolve findings before another round')
        state['reviews'].append(receipt)
        state['status'] = {'approve': 'ready', 'revise': 'needs-revision', 'blocked': 'review-blocked'}[receipt['verdict']]
        save_state(root, state)
        return inspected_result(root, state)


def changed_paths(root, old, new):
    raw = git(root, 'diff', '--name-only', '-z', old, new).stdout.decode()
    return sorted(filter(None, raw.split('\0')))


def tx_path(root, identifier):
    return safe_path(root, f'.state/transactions/{operation_id(identifier)}.json')


def save_tx(root, record):
    atomic_write(tx_path(root, record['id']), json_bytes(record))


def remove_backups(root, record):
    for item in record['writes']:
        if item.get('backup'):
            path = safe_path(root, item['backup'])
            if path.exists():
                if digest(path.read_bytes()) != item['old_sha256']:
                    raise KnowledgeError('Backup differs; it was retained')
                path.unlink()


def index_entry(root, commit, path):
    raw = git(root, 'ls-tree', '-z', commit, '--', path).stdout
    if not raw:
        return None
    header = raw.split(b'\t', 1)[0].decode().split()
    return header[0], header[2]


def restore_index(root, commit, paths):
    for path in paths:
        entry = index_entry(root, commit, path)
        if entry:
            git(root, 'update-index', '--add', '--cacheinfo', ','.join((*entry, path)))
        else:
            git(root, 'update-index', '--force-remove', '--', path)


def finish_commit(root, record):
    for item in record['writes']:
        path = safe_path(root, item['path'])
        if not path.is_file() or digest(path.read_bytes()) != item['new_sha256']:
            raise KnowledgeError('Committed files changed externally; retain recovery state')
    if git(root, 'diff', '--cached', '--quiet', record['commit'], check=False).returncode:
        raise KnowledgeError('Index differs from the published commit; recovery needs inspection')
    state = get_state(root, record['id'])
    state.update(status='published', published_commit=record['commit'])
    save_state(root, state)
    # Keep the global barrier until operation state is durably reconstructible.
    record['status'] = 'complete'
    save_tx(root, record)
    reference = 'refs/recap/pending/' + record['id']
    existing = git(root, 'rev-parse', '--verify', reference, check=False)
    if existing.returncode == 0:
        git(root, 'update-ref', '-d', reference, record['commit'])
    remove_backups(root, record)
    return {'id': record['id'], 'status': 'published', 'commit': record['commit'], 'paths': [w['path'] for w in record['writes']]}


def recover(root, identifier):
    with locked(root):
        filename = tx_path(root, identifier)
        if not filename.exists():
            raise KnowledgeError('No v2 transaction for this id; inspect the named legacy journal if applicable')
        record = load_json(filename)
        if record['status'] == 'rolled-back':
            return {'id': identifier, 'status': record['status'], 'changed': False}
        if record['status'] == 'complete':
            state = get_state(root, identifier)
            published = git_content(root, record['commit'], f'.state/published/{identifier}.json')
            if not published or json.loads(published)['candidate_sha256'] != state['fingerprint']:
                raise KnowledgeError('Completed publication evidence does not match the operation')
            if git(root, 'merge-base', '--is-ancestor', record['commit'], head(root), check=False).returncode:
                raise KnowledgeError('Completed commit is no longer in formal history')
            if state['status'] not in ('published', 'cleaned'):
                state.update(status='published', published_commit=record['commit'])
                save_state(root, state)
            reference = 'refs/recap/pending/' + identifier
            if git(root, 'rev-parse', '--verify', reference, check=False).returncode == 0:
                git(root, 'update-ref', '-d', reference, record['commit'])
            remove_backups(root, record)
            return {'id': identifier, 'status': 'complete', 'changed': False}
        current_head = head(root)
        if current_head == record['commit']:
            return finish_commit(root, record)
        if current_head != record['old_head']:
            raise KnowledgeError('Publication HEAD changed; recovery refused to rewrite later history')
        conflicts = []
        for item in record['writes']:
            target = safe_path(root, item['path'])
            actual = digest(target.read_bytes()) if target.exists() else None
            if actual not in (item['old_sha256'], item['new_sha256']):
                conflicts.append(item['path'])
        staged = git(root, 'diff', '--cached', '--name-only', '-z').stdout.decode().split('\0')
        for path in filter(None, staged):
            if path not in [item['path'] for item in record['writes']]:
                conflicts.append('index:' + path)
            else:
                actual = git(root, 'show', ':' + path, check=False)
                target = next(i for i in record['writes'] if i['path'] == path)
                if actual.returncode or digest(actual.stdout) not in (target['old_sha256'], target['new_sha256']):
                    conflicts.append('index:' + path)
        if conflicts:
            record.update(status='recovery-conflict', conflicts=conflicts)
            save_tx(root, record)
            raise KnowledgeError('Recovery preserved external edits: ' + ', '.join(conflicts))
        for item in reversed(record['writes']):
            target = safe_path(root, item['path'])
            if item['old_sha256'] is None:
                if target.exists():
                    target.unlink()
            else:
                data = safe_path(root, item['backup']).read_bytes()
                if digest(data) != item['old_sha256']:
                    raise KnowledgeError('Backup checksum mismatch; recovery stopped')
                atomic_write(target, data, item['mode'])
        restore_index(root, record['old_head'], [i['path'] for i in record['writes']])
        record['status'] = 'rolled-back'
        save_tx(root, record)
        reference = 'refs/recap/pending/' + identifier
        if git(root, 'rev-parse', '--verify', reference, check=False).returncode == 0:
            git(root, 'update-ref', '-d', reference, record['commit'])
        state = get_state(root, identifier)
        state['status'] = 'ready'
        save_state(root, state)
        return {'id': identifier, 'status': 'rolled-back', 'candidate_retained': True}


def publish(root, identifier, approved_sha256, migration=False):
    with locked(root):
        managed(root, migration)
        assert_no_pending(root, 'migration' if migration else None)
        assert_clean(root)
        state = get_state(root, identifier)
        if state['status'] in ('published', 'cleaned'):
            if state.get('fingerprint') != approved_sha256:
                raise KnowledgeError('Approval does not match the published operation')
            return {'id': identifier, 'status': state['status'], 'commit': state['published_commit'], 'changed': False}
        tree = ensure_candidate(root, state)
        if state['status'] != 'ready' or approved_sha256 != state['fingerprint']:
            raise KnowledgeError('Candidate is not ready or exact inspection hash differs')
        if head(root) != state['base']:
            raise KnowledgeError('Published version advanced; run integrate, inspect and review again')
        if state['review_required'] and not any(r['candidate_sha256'] == state['fingerprint'] and r['verdict'] == 'approve' for r in state['reviews']):
            raise KnowledgeError('Independent review unavailable or not approved; candidate retained')
        risk = state['packet'].get('risk', 'routine')
        for item in state['packet']['changes']:
            if item['kind'] == 'archive':
                risk = 'reserved'
        if (risk == 'reserved' or state.get('reserved_reasons')) and not reserved_ok(state, state['fingerprint']):
            raise KnowledgeError('Reserved change needs explicit user approval bound to this candidate')
        doc.validate_library(content_files(tree))
        check_cursors(tree, state)
        check_candidate_scope(tree, state)
        publication_record = {'schema': 'recap-publication/v2', 'id': identifier,
                              'writer_id': state['writer_id'], 'candidate_sha256': state['fingerprint'],
                              'base': state['base'], 'packet_sha256': state['packet_sha256'],
                              'review_required': state['review_required'], 'reviews': state['reviews'],
                              'changes': [{k: i[k] for k in ('path', 'kind', 'reason', 'evidence')} for i in state['packet']['changes']]}
        atomic_write(safe_path(tree, f'.state/published/{identifier}.json'), json_bytes(publication_record))
        state['candidate'] = commit_candidate(tree, 'Publication record ' + identifier)
        save_state(root, state)
        git_tree = git_text(tree, 'rev-parse', 'HEAD^{tree}')
        commit = git(root, 'commit-tree', git_tree, '-p', state['base'], input=('Recap ' + identifier + '\n').encode()).stdout.decode().strip()
        paths = changed_paths(root, state['base'], commit)
        if not paths or any(not allowed_path(p) for p in paths):
            raise KnowledgeError('Publication has no allowed changes')
        record = {'schema': 'recap-transaction/v2', 'id': identifier, 'status': 'prepared',
                  'old_head': state['base'], 'commit': commit, 'branch': managed(root, migration)['branch'], 'writes': []}
        for relative in paths:
            target = safe_path(root, relative)
            data = git_content(root, commit, relative)
            if data is None:
                raise KnowledgeError('Deletion is not a routine publication operation')
            old = target.read_bytes() if target.exists() else None
            item = {'path': relative, 'old_sha256': digest(old) if old is not None else None,
                    'new_sha256': digest(data), 'mode': stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o600}
            if old is not None:
                item['backup'] = f'.history/{identifier}/before/{relative}'
                atomic_write(safe_path(root, item['backup']), old)
            record['writes'].append(item)
        save_tx(root, record)
        try:
            git(root, 'update-ref', 'refs/recap/pending/' + identifier, commit, '0' * len(commit))
            for item in record['writes']:
                target = safe_path(root, item['path'])
                actual = digest(target.read_bytes()) if target.exists() else None
                if actual != item['old_sha256']:
                    raise KnowledgeError('Formal file changed during publication; recover without overwriting it')
                atomic_write(target, git_content(root, commit, item['path']), item['mode'])
            git(root, 'add', '--', *paths)
            # Verify all staged and unstaged formal changes before updating one ref.
            if git(root, 'diff', '--quiet', check=False).returncode or git(root, 'diff', '--cached', '--quiet', commit, check=False).returncode:
                raise KnowledgeError('External changes detected while publishing; recovery required')
            git(root, 'update-ref', record['branch'], commit, record['old_head'])
            return finish_commit(root, record)
        except Exception as exc:
            # Leave an explicit global barrier; recover will prove rollback/roll-forward safety.
            record['error'] = str(exc)
            save_tx(root, record)
            raise KnowledgeError(f'Publication interrupted; run recover {identifier}: {exc}') from exc


def cleanup(root, identifier):
    with locked(root):
        assert_no_pending(root)
        state = get_state(root, identifier)
        if state['status'] == 'cleaned':
            return {'id': identifier, 'status': 'cleaned', 'changed': False}
        if state['status'] != 'published':
            raise KnowledgeError('Only a successfully published candidate can be cleaned automatically')
        record = git_content(root, state['published_commit'], f'.state/published/{identifier}.json')
        if not record or json.loads(record)['candidate_sha256'] != state['fingerprint']:
            raise KnowledgeError('Published provenance does not match this candidate')
        destination = safe_path(root, '.worktree/' + identifier)
        if destination.exists():
            tree = ensure_candidate(root, state)
            git(root, 'worktree', 'remove', str(tree))
        branch = git(root, 'rev-parse', '--verify', state['branch'], check=False)
        if branch.returncode == 0:
            git(root, 'update-ref', '-d', state['branch'], state['candidate'])
        state['status'] = 'cleaned'
        save_state(root, state)
        return {'id': identifier, 'status': 'cleaned', 'changed': True,
                'raw_temporary_area': '.state/tmp/' + identifier,
                'note': 'Temporary raw extraction is not staged; remove only the exact extraction you created.'}


def status(root, identifier=None):
    with locked(root):
        if identifier is not None:
            return inspected_result(root, get_state(root, identifier))
        managed(root)
        recovery_required = pending(root)
        operations = []
        directory = safe_path(root, '.state/operations')
        for path in sorted(directory.glob('*.json')):
            try:
                safe_path(root, path.relative_to(root).as_posix())
                state = get_state(root, operation_id(path.stem))
                result = inspected_result(root, state)
                tree = safe_path(root, '.worktree/' + state['id'])
                result.update(worktree_exists=tree.is_dir(),
                              branch_exists=git(root, 'show-ref', '--verify', '--quiet', state['branch'], check=False).returncode == 0,
                              publication_record_exists=git_content(root, 'HEAD', f'.state/published/{state["id"]}.json') is not None)
            except (KnowledgeError, OSError, ValueError, KeyError, TypeError) as exc:
                result = {'id': path.stem, 'error': f'Cannot inspect operation {path.name}: {exc}'}
            operations.append(result)
        return {'root': str(root), 'operations': operations, 'recovery_required': recovery_required,
                'complete': all('error' not in item for item in operations)}


def build_packet(root, identifier, directory):
    """Fill mechanical fields from an existing base and explicitly declared input files."""
    directory = directory.expanduser().resolve()
    with locked(root):
        managed(root)
        assert_no_pending(root)
        assert_clean(root)
        state = get_state(root, identifier)
        if state['status'] != 'editing':
            raise KnowledgeError('Packet generation requires an editing operation; use resolve for a prepared candidate')
        assert_clean(worktree(root, state))
        manifest = load_json(safe_path(directory, 'changes.json'))
        doc.object_keys(manifest, ('changes',), ('risk',))
        if not isinstance(manifest['changes'], list) or not manifest['changes']:
            raise KnowledgeError('changes must be a nonempty array')
        packet = {'id': identifier, 'writer_id': state['writer_id'], 'changes': []}
        if 'risk' in manifest:
            if manifest['risk'] not in ('routine', 'reserved'):
                raise KnowledgeError('risk must be routine or reserved')
            packet['risk'] = manifest['risk']
        seen = set()
        for declaration in manifest['changes']:
            doc.object_keys(declaration, ('path', 'kind', 'reason', 'evidence'))
            path = declaration['path']
            source = safe_path(directory, path)
            if path in seen:
                raise KnowledgeError('Duplicate changed path')
            seen.add(path)
            prior = git_content(root, state['base'], path)
            item = {**declaration, 'expected_sha256': digest(prior) if prior is not None else None}
            content = source.read_text(encoding='utf-8')
            if path == 'index.md':
                item['document'] = {'body': content}
            elif path.startswith('topics/'):
                metadata, body = doc.split_document(content)
                if 'schema' in metadata:
                    doc.validate_topic(content)
                    metadata = {k: v for k, v in metadata.items() if k not in ('schema', 'created', 'updated')}
                item['document'] = {**metadata, 'body': body}
            else:
                item['content'] = content
            render_item(item, prior, date.today().isoformat())
            packet['changes'].append(item)
        return packet


def diff(root, identifier):
    with locked(root):
        state = get_state(root, identifier)
        tree = worktree(root, state)
        if state['status'] == 'conflict':
            result = git(tree, 'diff', state['base'], '--', *state['authored']).stdout.decode()
        else:
            ensure_candidate(root, state)
            result = git(tree, 'diff', state['base'], state['candidate']).stdout.decode()
        return {'id': identifier, 'candidate_sha256': state.get('fingerprint'), 'diff': result}


def initialize(root, language='en'):
    if root.exists() and library_files(root):
        if (root / '.git').is_dir() and safe_path(root, '.state/library.json').exists():
            with locked(root):
                assert_no_pending(root)
                managed(root)
            return {'root': str(root), 'status': 'already-initialized'}
        raise KnowledgeError('Existing material is preserved; use migration-plan instead of init')
    private_mkdir(root)
    with locked(root):
        assert_no_pending(root)
        if (root / '.git').exists():
            raise KnowledgeError('Existing Git metadata was not overwritten; use migration-plan')
        for prefix in ('topics', 'sources', 'drafts', '.history', '.state', '.worktree'):
            private_mkdir(safe_path(root, prefix))
        git(root, 'init', '-b', 'recap-main')
        initial = {'index.md': '# 知识导读\n' if language == 'zh' else '# Knowledge\n',
                   'CHANGELOG.md': '# 知识变更\n' if language == 'zh' else '# Knowledge changes\n',
                   'AGENTS.md': GUIDE, '.gitignore': IGNORE,
                   '.state/library.json': json_bytes({'schema': 'recap-library/v2', 'branch': 'refs/heads/recap-main', 'language': language}).decode()}
        for path, value in initial.items():
            atomic_write(safe_path(root, path), value.encode())
        git(root, 'add', '--', *initial)
        git(root, 'commit', '-m', 'Initialize recap library')
        return {'root': str(root), 'status': 'initialized', 'revision': head(root)}


def source_migration(content, override=None):
    old, body = doc.split_document(content, legacy=True)
    if old.get('schema') == 'recap-source/v2':
        doc.validate_source(content)
        return content
    if override is None:
        # Coverage judgments are never inferred from a free-form status label.
        raise KnowledgeError('Legacy source needs an explicit v2 metadata override; preserve its original body')
    result = doc.render(override, body)
    doc.validate_source(result)
    return result


def migration_plan(root, overrides_file=None):
    if not root.is_dir():
        raise KnowledgeError('Migration needs an existing library')
    overrides = load_json(overrides_file) if overrides_file else {}
    doc.object_keys(overrides, (), ('topics', 'sources'))
    with locked(root):
        assert_no_pending(root)
        existing = library_files(root)
        if (root / '.git').exists():
            if not (root / '.git').is_dir() or git_text(root, 'rev-parse', '--show-toplevel') != str(root):
                raise KnowledgeError('Migration requires an exact, standalone root')
            if git(root, 'rev-parse', '--verify', 'HEAD', check=False).returncode == 0:
                assert_clean(root)
        today = date.today().isoformat()
        changes = {}
        for path, data in existing.items():
            if path.startswith('topics/'):
                kind = overrides.get('topics', {}).get(path, 'concept')
                changes[path] = doc.migrate_topic(data.decode(), today, kind)
            elif path.startswith('sources/'):
                changes[path] = source_migration(data.decode(), overrides.get('sources', {}).get(path))
        overlay = {p: b.decode() for p, b in existing.items() if p.endswith('.md')}
        overlay.update(changes)
        doc.validate_library(overlay)
        for path, data in existing.items():
            if not path.startswith('.state/cursors/'):
                continue
            receipt = json.loads(data)
            matching_sources = []
            for source_path, content in changes.items():
                if source_path.startswith('sources/'):
                    metadata, _ = doc.validate_source(content)
                    if metadata['host'] == receipt.get('host') and metadata['session_id'] == receipt.get('session_id'):
                        matching_sources.append(source_path)
            matching_topics = [p for p, content in changes.items() if p.startswith('topics/') and
                               any(doc.local_target(p, link) in matching_sources for link in doc.validate_topic(content)[0]['sources'])]
            receipt['represented_by'] = {'topics': sorted(matching_topics), 'sources': sorted(matching_sources)}
            validate_cursor(receipt)
            changes[path] = json_bytes(receipt).decode()
        return {'schema': 'recap-migration/v2', 'id': 'migration',
                'expected_files': {p: digest(b) for p, b in existing.items()}, 'changes': changes,
                'note': 'Review source coverage overrides and topic types; prose and original dates remain unchanged.'}


def migrate(root, filename, approved_sha256):
    plan = load_json(filename)
    if digest(filename.read_bytes()) != approved_sha256:
        raise KnowledgeError('Migration approval does not match exact plan bytes')
    doc.object_keys(plan, ('schema', 'id', 'expected_files', 'changes', 'note'))
    if plan['schema'] != 'recap-migration/v2' or plan['id'] != 'migration':
        raise KnowledgeError('Unsupported migration plan')
    marker = safe_path(root, '.state/migration.json')
    with locked(root):
        assert_no_pending(root, 'migration')
        state = load_json(marker) if marker.exists() else None
        if state:
            if state['plan_sha256'] != approved_sha256:
                raise KnowledgeError('Resume the exact original migration plan')
            if state['status'] == 'complete':
                return {'status': 'already-migrated', 'commit': head(root)}
        else:
            actual = {p: digest(b) for p, b in library_files(root).items()}
            if actual != plan['expected_files']:
                raise KnowledgeError('Library changed since migration preview')
            overlay = content_files(root)
            for path, content in plan['changes'].items():
                safe_path(root, path)
                if not path.startswith(('topics/', 'sources/', '.state/cursors/')) or not allowed_path(path):
                    raise KnowledgeError('Migration can only transform existing topics, sources and capture cursors')
                original = safe_path(root, path).read_text()
                if path.startswith('.state/cursors/'):
                    old_cursor, new_cursor = json.loads(original), json.loads(content)
                    validate_cursor(new_cursor)
                    old_cursor.pop('represented_by', None)
                    compared = dict(new_cursor)
                    compared.pop('represented_by', None)
                    if old_cursor != compared:
                        raise KnowledgeError('Migration must preserve original capture coverage fields')
                    continue
                if doc.split_document(original, legacy=True)[1] != doc.split_document(content)[1]:
                    raise KnowledgeError('Migration must preserve exact original prose')
                if path.startswith('topics/'):
                    old = doc.split_document(original, legacy=True)[0]
                    new = doc.validate_topic(content)[0]
                    if any(k in old and new[k] != old[k] for k in ('created', 'updated', 'acquired', 'sources')):
                        raise KnowledgeError('Migration must preserve existing dates and source contributions')
                overlay[path] = content
            doc.validate_library(overlay)
            state = {'schema': 'recap-migration-state/v2', 'status': 'starting', 'plan_sha256': approved_sha256}
            atomic_write(marker, json_bytes(state))
        if state['status'] == 'starting':
            current_files = library_files(root)
            expected = plan['expected_files']
            if any(p not in current_files or digest(current_files[p]) != checksum for p, checksum in expected.items()):
                raise KnowledgeError('Original material changed during interrupted migration; preserve external edits')
            additions = current_files.keys() - expected.keys() - {'.gitignore', '.state/library.json'}
            if additions:
                raise KnowledgeError('External formal files appeared during interrupted migration')
            if not (root / '.git').exists():
                git(root, 'init', '-b', 'recap-main')
            branch = git_text(root, 'symbolic-ref', 'HEAD')
            if git(root, 'rev-parse', '--verify', 'HEAD', check=False).returncode == 0:
                assert_clean(root)
            # These are migration-owned additions, recorded with the original files as baseline.
            if not safe_path(root, '.gitignore').exists():
                atomic_write(safe_path(root, '.gitignore'), IGNORE.encode())
            config = {'schema': 'recap-library/v1', 'branch': branch}
            atomic_write(safe_path(root, '.state/library.json'), json_bytes(config))
            git(root, 'add', '--', *sorted(library_files(root)))
            git(root, 'commit', '--allow-empty', '-m', 'Baseline before recap format migration')
            state.update(status='baseline', baseline=head(root))
            atomic_write(marker, json_bytes(state))
    # Internal migration uses the same recoverable publication path, with a special source-preserving candidate.
    begin(root, 'migration', 'recap-migrator', migration=True)
    with locked(root):
        op = get_state(root, 'migration')
        if op['status'] == 'editing':
            tree = worktree(root, op)
            changes = []
            for path, content in plan['changes'].items():
                atomic_write(safe_path(tree, path), content.encode())
                changes.append({'path': path, 'kind': 'update', 'reason': 'Migrate metadata; preserve prose and original dates',
                                'evidence': ['reviewed migration plan ' + approved_sha256]})
            config = load_json(safe_path(tree, '.state/library.json'))
            config['schema'] = 'recap-library/v2'
            atomic_write(safe_path(tree, '.state/library.json'), json_bytes(config))
            old_guide = safe_path(tree, 'AGENTS.md').read_text() if safe_path(tree, 'AGENTS.md').exists() else ''
            extension = '''## Publication workflow

Search only formal topics; archived topics are outside ordinary retrieval.
.worktree/ holds unpublished candidates, and .git/ holds historical versions.
Use locked helper reads and their revision checks. Resolve pending publication first.
Capture cursors and generated review records in .state/ remain outside ordinary search.
These are cooperative boundaries, not OS-enforced file permissions.
'''
            guide = old_guide.rstrip() + '\n\n' + extension if old_guide else GUIDE
            atomic_write(safe_path(tree, 'AGENTS.md'), guide.encode())
            op.update(packet={'changes': changes}, packet_sha256=approved_sha256, authored=sorted(plan['changes']))
            catalogs(tree, op)
            doc.validate_library(content_files(tree))
            op['candidate'] = commit_candidate(tree, 'Migrate recap document metadata')
            op['fingerprint'] = fingerprint(tree, op)
            op['status'] = 'ready'
            save_state(root, op)
    result = publish(root, 'migration', get_state(root, 'migration')['fingerprint'], migration=True)
    with locked(root):
        state['status'] = 'complete'
        atomic_write(marker, json_bytes(state))
    cleanup(root, 'migration')
    return result
