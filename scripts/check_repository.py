"""Run repository checks with the same Python encoding environment locally and in CI."""

import argparse
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ('-m', 'unittest', 'discover', '-s', 'tests', '-v'),
    ('skills/engineering/project-adr/scripts/check_adr.py', 'docs/agents/adr'),
    ('-m', 'scripts.check_docs'),
)


def test_selector(value):
    if not value.strip():
        raise argparse.ArgumentTypeError('Test selectors must be nonempty')
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--test-pattern', type=test_selector,
                        help='Discover only matching test filenames (unittest -p glob)')
    parser.add_argument('--test-name', action='append', type=test_selector, default=[],
                        help='Select test names (unittest -k substring/glob); repeat for OR matching')
    options = parser.parse_args(argv)
    test_args = []
    if options.test_pattern is not None:
        test_args.extend(('-p', options.test_pattern))
    for name in options.test_name:
        test_args.extend(('-k', name))
    env = os.environ.copy()
    # Retain locale-dependent defaults while making subprocess streams UTF-8.
    env.update(PYTHONUTF8='0', PYTHONIOENCODING='utf-8')
    for index, args in enumerate(CHECKS):
        command = [sys.executable, '-B', *args, *(test_args if index == 0 else [])]
        print('Running: ' + ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=ROOT, env=env)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
