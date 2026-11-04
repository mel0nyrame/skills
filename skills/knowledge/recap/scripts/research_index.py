#!/usr/bin/env python3
"""Print a navigable research inventory without changing research or knowledge files."""
from __future__ import annotations

import argparse
from datetime import date
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote

from storage import KnowledgeError, safe_path


def describe(content, fallback):
    content = re.sub(r'\A---\r?\n.*?\r?\n---(?:\r?\n|$)', '', content, count=1, flags=re.S)
    title, paragraphs, paragraph, fence = None, [], [], None
    for line in content.splitlines() + ['']:
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = (marker[1][0], len(marker[1]))
            elif fence[0] == marker[1][0] and len(marker[1]) >= fence[1] and not line[marker.end():].strip():
                fence = None
            continue
        if fence:
            continue
        heading = re.match(r'^#\s+(.+?)\s*#*\s*$', line)
        if heading and title is None:
            title = heading[1]
        if not line.strip() or line.startswith('#'):
            if paragraph:
                paragraphs.append(' '.join(paragraph))
                paragraph = []
        elif not line.lstrip().startswith(('<!--', '|', '>', '- ', '* ')):
            paragraph.append(line.strip())
    return title or fallback, (paragraphs[0] if paragraphs else '')[:180]


def cell(text):
    return text.replace('\\', '\\\\').replace('|', '\\|').replace('[', '\\[').replace(']', '\\]').replace('\n', ' ')


def inventory(root):
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise KnowledgeError('Research root must be an existing directory')
    rows = []
    # Follow no directory symlinks and keep private/raw/management material out.
    paths = []
    for current, directories, files in os.walk(root, followlinks=False):
        directories[:] = sorted(name for name in directories if not name.startswith('.') and name != '_raw'
                                and not (Path(current) / name).is_symlink())
        paths.extend(Path(current) / name for name in files if name.endswith('.md'))
    for path in sorted(paths):
        relative = path.relative_to(root)
        if any(part.startswith('.') or part == '_raw' for part in relative.parts):
            continue
        if path.name.lower() in ('index.md', 'readme.md', 'agents.md'):
            continue
        try:
            safe_path(root, relative.as_posix())
        except KnowledgeError:
            continue
        title, summary = describe(path.read_text(encoding='utf-8'), path.stem)
        stamp = re.match(r'\d{4}-\d{2}-\d{2}', relative.as_posix())
        day = stamp[0] if stamp else ''
        try:
            if day:
                date.fromisoformat(day)
        except ValueError:
            day = ''
        rows.append(f'| {day} | [{cell(relative.as_posix())}](<{quote(relative.as_posix(), safe="/")}>) | '
                    f'{cell(title)} | {cell(summary)} | Unmarked |')
    return '\n'.join(['# Research inventory', '',
        'Capture status is unmarked. Titles and excerpts do not establish whether a document was captured.', '',
        '| Date | File | Title | Opening excerpt | Capture status |',
        '| --- | --- | --- | --- | --- |', *rows, ''])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, help='Explicit research directory; output goes only to stdout')
    args = parser.parse_args(argv)
    try:
        print(inventory(args.root), end='')
        return 0
    except (KnowledgeError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
