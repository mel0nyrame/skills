"""Scoped filesystem, Git and publication-lock primitives (standard library)."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import time


class KnowledgeError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise KnowledgeError(f'Duplicate JSON field: {key}')
        result[key] = value
    return result


def load_json(path):
    try:
        return json.loads(path.read_bytes(), object_pairs_hook=unique_object)
    except (ValueError, UnicodeError) as exc:
        raise KnowledgeError(f'Invalid JSON in {path.name}: {exc}') from exc


def safe_path(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative or any(ord(c) < 32 for c in relative):
        raise KnowledgeError('Use a nonempty root-relative POSIX path without control characters')
    path = PurePosixPath(relative)
    if path.is_absolute() or any(c in ('.', '..') for c in relative.split('/')) or path.as_posix() != relative:
        raise KnowledgeError('Absolute paths, traversal and noncanonical paths are excluded')
    target = root
    for part in path.parts:
        target = target / part
        if target.is_symlink():
            raise KnowledgeError('Symlinks are excluded from knowledge operations')
    if root.resolve() not in target.resolve().parents:
        raise KnowledgeError('Path escapes the selected root')
    return target


def private_mkdir(path):
    missing, current = [], path
    while not current.exists():
        missing.append(current)
        current = current.parent
    for directory in reversed(missing):
        directory.mkdir(mode=0o700, exist_ok=True)


def atomic_write(path, data, mode=0o600):
    private_mkdir(path.parent)
    fd, temporary = tempfile.mkstemp(prefix='.recap-', dir=path.parent)
    try:
        if hasattr(os, 'fchmod'):
            os.fchmod(fd, mode)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        if os.name != 'nt':
            parent = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(parent)
            finally:
                os.close(parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


LOCK_TIMEOUT = 30.0


@contextmanager
def locked(root, timeout=None):
    timeout = LOCK_TIMEOUT if timeout is None else timeout
    if not 0 <= timeout <= 30:
        raise KnowledgeError('Lock timeout must be between 0 and 30 seconds')
    lock = safe_path(root, '.state/write.lock')
    private_mkdir(lock.parent)
    fd = os.open(lock, os.O_RDWR | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, 'a+b') as handle:
        if os.name == 'nt':
            import msvcrt
            handle.seek(0)
            if not handle.read(1):
                handle.write(b'0')
                handle.flush()
            def acquire():
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            def release():
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            def acquire():
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            def release():
                fcntl.flock(handle, fcntl.LOCK_UN)
        deadline = time.monotonic() + timeout
        while True:
            try:
                acquire()
                break
            except (BlockingIOError, OSError) as exc:
                if time.monotonic() >= deadline:
                    raise KnowledgeError('Publication lock timed out; candidate work is retained') from exc
                time.sleep(min(0.1, max(0, deadline - time.monotonic())))
        try:
            yield
        finally:
            release()


def operation_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', value):
        raise KnowledgeError('Operation id must be a unique safe 1-80 character identifier')
    return value


def git(root, *arguments, input=None, check=True):
    executable = shutil.which('git')
    if not executable:
        raise KnowledgeError('Git is unavailable; retain drafts, no software was installed')
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_TERMINAL_PROMPT='0', GIT_OPTIONAL_LOCKS='0')
    command = [executable, '-C', str(root), '-c', 'core.hooksPath=' + os.devnull,
               '-c', 'core.attributesFile=' + os.devnull, '-c', 'core.autocrlf=false',
               '-c', 'core.fsmonitor=false', '-c', 'commit.gpgsign=false',
               '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
               '-c', 'user.name=Recap', '-c', 'user.email=recap@localhost', *arguments]
    result = subprocess.run(command, input=input, capture_output=True, env=environment)
    if check and result.returncode:
        raise KnowledgeError(f'Git {arguments[0]} failed: {result.stderr.decode(errors="replace").strip()}')
    return result


def git_text(root, *arguments):
    return git(root, *arguments).stdout.decode().strip()


def head(root):
    return git_text(root, 'rev-parse', '--verify', 'HEAD')


def git_content(root, commit, path):
    result = git(root, 'show', f'{commit}:{path}', check=False)
    return result.stdout if result.returncode == 0 else None


def allowed_path(path):
    parts = PurePosixPath(path).parts
    if path in ('index.md', 'CHANGELOG.md', 'AGENTS.md', '.gitignore', '.state/library.json'):
        return True
    if len(parts) > 1 and parts[0] in ('topics', 'sources'):
        return path.endswith('.md') and all(not p.startswith('.') for p in parts[1:])
    return len(parts) == 3 and parts[:2] in (('.state', 'cursors'), ('.state', 'published')) and path.endswith('.json')


def library_files(root):
    """Enumerate only publication allowlist material; never walk a whole root."""
    result = {}
    for name in ('index.md', 'CHANGELOG.md', 'AGENTS.md', '.gitignore', '.state/library.json'):
        path = safe_path(root, name)
        if path.is_file():
            result[name] = path.read_bytes()
    for prefix in ('topics', 'sources', '.state/cursors', '.state/published'):
        directory = safe_path(root, prefix)
        if not directory.exists():
            continue
        for current, dirs, names in os.walk(directory, followlinks=False):
            for name in dirs + names:
                if (Path(current) / name).is_symlink():
                    raise KnowledgeError(f'Symlink in formal material: {prefix}')
            dirs[:] = sorted(d for d in dirs if not d.startswith('.')) if prefix in ('topics', 'sources') else []
            for name in sorted(names):
                relative = (Path(current) / name).relative_to(root).as_posix()
                if allowed_path(relative):
                    result[relative] = safe_path(root, relative).read_bytes()
    return result


def assert_clean(root):
    changes = git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all').stdout
    if changes:
        raise KnowledgeError('External/uncommitted changes detected; publication paused without staging or overwriting them')
    tracked = git(root, 'ls-files', '-z').stdout.decode().split('\0')
    for path in filter(None, tracked):
        safe_path(root, path)
        if not allowed_path(path):
            raise KnowledgeError(f'Tracked file is outside the publication allowlist: {path}')


def pending(root, skip=None):
    found = []
    for directory, suffix in (('.state/transactions', '*.json'), ('.history', '*/journal.json')):
        base = safe_path(root, directory)
        if not base.exists():
            continue
        for path in sorted(base.glob(suffix)):
            safe_path(root, path.relative_to(root).as_posix())
            record = load_json(path)
            if not isinstance(record, dict):
                raise KnowledgeError('Malformed operation journal; recovery required')
            if record.get('id') == skip:
                continue
            if record.get('status') not in ('complete', 'rolled-back'):
                found.append(record.get('id', path.name))
    return found


def assert_no_pending(root, skip=None):
    operations = pending(root, skip)
    if operations:
        raise KnowledgeError('Recovery required before reading or publishing: ' + ', '.join(operations))
    migration = safe_path(root, '.state/migration.json')
    if migration.exists() and load_json(migration).get('status') != 'complete' and skip != 'migration':
        raise KnowledgeError('Migration interrupted; resume the exact reviewed migration plan')


def revision(root):
    if (root / '.git').is_dir():
        return head(root)
    return 'legacy-' + digest(json_bytes({p: digest(b) for p, b in library_files(root).items()}))
