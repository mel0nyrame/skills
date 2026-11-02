#!/usr/bin/env python3
"""Check default English or Chinese ADR structure and local Markdown link paths."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


SECTIONS = ("Problem", "Decision", "Alternatives", "Consequences and risks")
CHINESE_SECTIONS = ("问题", "决策", "备选方案", "后果与风险")
STATES = {"proposed", "implemented", "rejected", "superseded", "archived"}
ARCHIVES = {"archive", "archived"}
ENTRY_FILES = {"README.md", "AGENTS.md", "CLAUDE.md"}
INLINE_LINK = re.compile(
    r'!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|(?:[^()\s]|\([^()\n]*\))+)'
    r'''(?:\s+["'][^"'\n]*["'])?\s*\)'''
)
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)", re.M)


def visible_lines(text):
    """Hide example syntax while counting substantive fenced code as content."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    fence = None
    result = []
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if (marker and marker[1][0] == fence[0]
                    and len(marker[1]) >= len(fence) and not marker[2].strip()):
                fence = None
            result.append("__code__" if line.strip() and not marker else "")
        elif marker:
            fence = marker[1]
            result.append("")
        else:
            result.append(line)
    return result


def check(path):
    errors = []
    try:
        lines = visible_lines(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        return [f"Cannot read file: {exc}"]
    if not lines or not re.fullmatch(r"#\s+\S.*", lines[0]):
        errors.append("The first line must be a nonempty level-one heading")
    statuses = [(i, line) for i, line in enumerate(lines)
                if re.match(r"^(?:-\s+)?(?:Status|状态)[：:]", line)]
    if len(statuses) != 1:
        errors.append("Exactly one status field is required")
    else:
        state = re.fullmatch(r"(?:Status|状态)[：:]\s*(\S+)\s*", statuses[0][1])
        if state is None or state[1] not in STATES:
            errors.append("Status must be one value from: " + ", ".join(sorted(STATES)))
        elif state[1] == "archived":
            errors.append("Archived records belong in an archive directory, outside active checks")

    headings = [(i, line[3:].strip()) for i, line in enumerate(lines)
                if line.startswith("## ")]
    chinese = bool(statuses and re.match(r"^(?:-\s+)?状态[：:]", statuses[0][1]))
    sections = CHINESE_SECTIONS if chinese else SECTIONS
    other_sections = SECTIONS if chinese else CHINESE_SECTIONS
    required = [(i, title) for i, title in headings if title in sections]
    if [title for _, title in required] != list(sections):
        errors.append("Required sections must occur once in this order: " + ", ".join(sections))
    if any(title in other_sections for _, title in headings):
        errors.append("Use one complete English or Chinese schema per record")
    if statuses and headings and statuses[0][0] >= headings[0][0]:
        errors.append("Status must precede section content")
    for start, title in required:
        end = next((i for i, _ in headings if i > start), len(lines))
        body = [line for line in lines[start + 1:end]
                if line.strip() and not re.match(r"^\s*#+\s", line)]
        if not body:
            errors.append(f"Section must not be empty: {title}")

    prose = "\n".join(lines)
    prose = re.sub(r"`+[^`\n]*`+", "", prose)
    targets = INLINE_LINK.findall(prose) + REFERENCE_LINK.findall(prose)
    for target in sorted(set(targets)):
        target = target.strip("<>")
        try:
            parsed = urlsplit(target)
        except ValueError:
            errors.append(f"Cannot parse link: {target}")
            continue
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        linked = Path(unquote(parsed.path))
        resolved = linked if linked.is_absolute() else path.parent / linked
        if not resolved.exists():
            errors.append(f"Local link target does not exist: {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="ADR files or active-record directories")
    args = parser.parse_args()
    files = set()
    errors = []
    for target in args.paths:
        if not target.exists():
            errors.append(f"{target}: Path does not exist")
        elif any(part in ARCHIVES for part in target.parts):
            errors.append(f"{target}: Archives are outside active-record checks")
        elif target.is_dir():
            files.update(p for p in target.rglob("*.md")
                         if p.name not in ENTRY_FILES
                         and not any(part in ARCHIVES for part in p.relative_to(target).parts))
        elif target.is_file() and target.suffix == ".md" and target.name not in ENTRY_FILES:
            files.add(target)
        else:
            errors.append(f"{target}: Specify an ADR Markdown file or directory")
    for path in sorted(files):
        errors.extend(f"{path}: {error}" for error in check(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"ADR check passed: {len(files)} active records; structure, status, and local link paths.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
