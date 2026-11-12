"""Run repository checks with the same Python encoding environment locally and in CI."""

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


def main():
    env = os.environ.copy()
    # Retain locale-dependent defaults while making subprocess streams UTF-8.
    env.update(PYTHONUTF8='0', PYTHONIOENCODING='utf-8')
    for args in CHECKS:
        command = [sys.executable, '-B', *args]
        print('Running: ' + ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=ROOT, env=env)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
