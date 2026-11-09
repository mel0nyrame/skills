"""Prepare pinned forward-test inputs and verify their source identity."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = {'prose-generated': 'project-prose', 'git-review': 'project-git'}
MANIFEST = '.scenario-source.json'


def git(root, *args):
    return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True).stdout


def sources(root, commit, scenario):
    prefix = f'tests/fixtures/scenarios/{scenario}/'
    skill = f'skills/engineering/{SCENARIOS[scenario]}/'
    names = git(root, 'ls-tree', '-r', '--name-only', '-z', commit, '--', prefix, skill)
    result = {}
    for name in names.decode('utf-8').split('\0'):
        if name:
            destination = (name.removeprefix(prefix) if name.startswith(prefix)
                           else '.agents/skills/' + name.removeprefix('skills/engineering/'))
            result[name] = (destination, git(root, 'show', f'{commit}:{name}'))
    if not any(name.startswith(prefix) for name in result):
        raise ValueError(f'{scenario} has no fixture inputs at {commit}')
    if skill + 'SKILL.md' not in result:
        raise ValueError(f'{SCENARIOS[scenario]} is missing at {commit}')
    return result


def prepare(root, scenario, destination, ref='HEAD'):
    commit = git(root, 'rev-parse', '--verify', f'{ref}^{{commit}}').decode().strip()
    inputs = sources(root, commit, scenario)
    destination.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for source, (target, content) in inputs.items():
        path = destination / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        hashes[source] = hashlib.sha256(content).hexdigest()
    manifest = {'scenario': scenario, 'commit': commit, 'sha256': hashes}
    (destination / MANIFEST).write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    git(destination, 'init', '-b', 'main')
    git(destination, 'add', '.')
    git(destination, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '-m', 'test: initialize forward fixture')
    return manifest


def check_source(root, destination):
    manifest = json.loads((destination / MANIFEST).read_text(encoding='utf-8'))
    if (not isinstance(manifest['commit'], str)
            or not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', manifest['commit'])):
        raise ValueError('Recorded source must be an immutable full commit hash')
    inputs = sources(root, manifest['commit'], manifest['scenario'])
    expected = {source: hashlib.sha256(content).hexdigest()
                for source, (_, content) in inputs.items()}
    errors = []
    if manifest['sha256'] != expected:
        errors.append('Source hashes do not match the recorded commit')
    for _, (target, content) in inputs.items():
        if target.startswith('.agents/skills/'):
            path = destination / target
            if not path.is_file() or path.read_bytes() != content:
                errors.append(f'Supplied instruction changed or missing: {target}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('prepare')
    create.add_argument('scenario', choices=SCENARIOS)
    create.add_argument('destination', type=Path)
    create.add_argument('--ref', default='HEAD', help='Committed fixture and instruction source')
    verify = commands.add_parser('check-source')
    verify.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            manifest = prepare(ROOT, args.scenario, args.destination.resolve(), args.ref)
            print(f"Prepared {args.scenario} at {manifest['commit']}: {args.destination}")
            print('Run the task in a fresh agent; preparation alone is not a passed scenario.')
            return 0
        errors = check_source(ROOT, args.destination.resolve())
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f'Fixture error: {exc}', file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print('Source identity passed against the recorded commit; model behavior was not evaluated.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
