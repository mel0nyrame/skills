"""Check the repository's PR-body structure; semantic review stays with reviewers."""

import argparse
import json
from pathlib import Path
import re
import sys

from scripts.check_docs import without_fences


def check(body):
    body = body.replace('\r\n', '\n').replace('\r', '\n')
    visible = without_fences(body)
    headings = list(re.finditer(r'^## (.+?)[ \t]*$', visible, re.M))
    if [match[1] for match in headings] != ['Summary', 'Evidence', 'Merge Danger']:
        return ['Use exactly these sections in order: Summary, Evidence, Merge Danger']
    sections = {}
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(visible)
        sections[match[1]] = visible[match.end():end]
    errors = []
    if visible[:headings[0].start()].strip():
        errors.append('Start directly with Summary')
    # Locate the raw Summary separately because its visual can be fenced code.
    raw_summary = body[headings[0].end():headings[1].start()]
    if not (re.search(r'^ {0,3}(?:`{3,}|~{3,})', raw_summary, re.M)
            or re.search(r'!\[[^\]]*\]\([^)]+\)', sections['Summary'])):
        errors.append('Summary needs a diagram, diff sketch, tree, or image')
    for field in ('Before', 'After'):
        match = re.search(r'^[ \t]*(?:- )?\*\*' + field + r':\*\*[ \t]*(\S[^\n]*)',
                          sections['Evidence'], re.M)
        if not match or match[1].strip().startswith('<'):
            errors.append(f'Evidence needs a concrete {field} value')
    if not re.search(r'^\*\*Door:\*\*[ \t]+(?:one-way|two-way)[ \t]*$',
                     sections['Merge Danger'], re.M):
        errors.append('Door must be one-way or two-way')
    if not re.search(r'^\*\*Blast Radius:\*\*[ \t]+[\w-]+[ \t]*$',
                     sections['Merge Danger'], re.M):
        errors.append('Blast Radius must be one word')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--body-file', type=Path)
    inputs.add_argument('--event', type=Path, help='GitHub pull_request event JSON')
    args = parser.parse_args()
    try:
        if args.event:
            event = json.loads(args.event.read_text(encoding='utf-8'))
            body = event['pull_request']['body'] or ''
        else:
            body = args.body_file.read_text(encoding='utf-8')
        errors = check(body)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Cannot read PR body: {exc}', file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('PR body structure passed; verify the visual and evidence against the diff during review.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
