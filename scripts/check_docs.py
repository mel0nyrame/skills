"""Check local Markdown targets, anchors, and English/Chinese guide pairs."""

import argparse
from html import unescape
from pathlib import Path
import re
import subprocess
import unicodedata
from urllib.parse import unquote, urlsplit


INLINE_LINK = re.compile(
    r'!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|(?:[^()\s]|\([^()\n]*\))+)'
    r'''(?:\s+["'][^"'\n]*["'])?\s*\)'''
)
REFERENCE = re.compile(r'^ {0,3}\[([^\]\n]+)\]:\s*(<[^>\n]+>|\S+)', re.M)


def without_fences(text):
    """Keep line positions; hide comments and fenced examples."""
    text = re.sub(r'<!--.*?-->', lambda m: re.sub(r'[^\n]', ' ', m[0]), text, flags=re.S)
    fence = None
    lines = []
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if (marker and marker[1][0] == fence[0]
                    and len(marker[1]) >= len(fence) and not marker[2].strip()):
                fence = None
            lines.append(' ' * len(line))
        elif marker:
            fence = marker[1]
            lines.append(' ' * len(line))
        else:
            lines.append(line)
    return '\n'.join(lines)


def anchors(text):
    text = without_fences(text)
    titles = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        heading = re.match(r'^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
        if heading:
            titles.append(heading[1])
        elif (index and re.fullmatch(r' {0,3}(?:=+|-+)\s*', line)
              and lines[index - 1].strip()):
            titles.append(lines[index - 1].strip())
    found = set()
    for title in titles:
        title = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', title)
        code = []

        def hold_code(match):
            code.append(match[2])
            return f'CODETOKEN{len(code) - 1}END'

        title = re.sub(r'(`+)(.*?)\1', hold_code, title)
        title = re.sub(r'(\*\*|__)(.+?)\1', r'\2', title)
        title = re.sub(r'(?<!\w)(\*|_)(\S(?:.*?\S)?)\1(?!\w)', r'\2', title)
        for index, content in enumerate(code):
            title = title.replace(f'CODETOKEN{index}END', content)
        title = unescape(re.sub(r'<[^>]+>', '', title)).lower()
        slug = ''.join(c for c in title
                       if c in '-_ ' or unicodedata.category(c)[0] in 'LNM')
        slug = slug.replace(' ', '-')
        candidate, suffix = slug, 0
        while candidate in found:
            suffix += 1
            candidate = f'{slug}-{suffix}'
        found.add(candidate)
    found.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text, re.I))
    return found


def check_document(path):
    errors = []
    text = without_fences(path.read_text(encoding='utf-8'))
    text = re.sub(r'(`+).*?\1', '', text, flags=re.S)
    definitions = {key.casefold(): target for key, target in REFERENCE.findall(text)}
    for key in re.findall(r'\[[^\]\n]+\]\[([^\]\n]+)\]', text):
        if key.casefold() not in definitions:
            errors.append(f'{path}: undefined reference [{key}]')
    targets = INLINE_LINK.findall(text) + list(definitions.values())
    for target in sorted(set(targets)):
        target = target.strip('<>')
        try:
            url = urlsplit(target)
        except ValueError:
            errors.append(f'{path}: invalid link {target}')
            continue
        if url.scheme or url.netloc:
            continue
        dest = path.parent / unquote(url.path) if url.path else path
        if not dest.exists():
            errors.append(f'{path}: missing target {target}')
        elif url.fragment and dest.is_file() and dest.suffix == '.md':
            if unquote(url.fragment) not in anchors(dest.read_text(encoding='utf-8')):
                errors.append(f'{path}: missing anchor {target}')
    return errors


def check_pairs(root, files):
    errors = []
    guides = {p for p in files
              if (p.name in ('README.md', 'README.zh.md') and p.parent == root)
              or (p.is_relative_to(root / 'docs')
                  and not p.is_relative_to(root / 'docs/agents'))}
    for path in sorted(guides):
        other = path.with_name(path.name.replace('.zh.md', '.md')
                               if path.name.endswith('.zh.md')
                               else path.stem + '.zh.md')
        if other not in guides:
            errors.append(f'{path}: missing bilingual pair {other.name}')
        elif f']({other.name})' not in path.read_text(encoding='utf-8'):
            errors.append(f'{path}: missing reciprocal guide link to {other.name}')
    return errors


def check(root):
    result = subprocess.run(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', '*.md'],
        cwd=root, check=True, capture_output=True,
    )
    files = [root / name for name in sorted(set(result.stdout.decode('utf-8').split('\0')))
             if name and not name.startswith('tests/fixtures/')]
    errors = []
    for path in files:
        if path.is_file():
            errors.extend(check_document(path))
        else:
            errors.append(f'{path}: missing Markdown file')
    errors.extend(check_pairs(root, files))
    return files, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    files, errors = check(args.root.resolve())
    for error in errors:
        print(error)
    if not errors:
        print(f'Documentation check passed: {len(files)} Markdown files; local links, anchors, guide pairs.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
