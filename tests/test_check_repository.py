"""Check shared validation environment, command ordering, and failure handling."""

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_repository


class RepositoryCheckTests(unittest.TestCase):
    def test_documented_and_ci_entry_points_use_shared_runner(self):
        for name in ('README.md', 'README.zh.md', 'AGENTS.md',
                     'docs/maintaining.md', 'docs/maintaining.zh.md'):
            with self.subTest(path=name):
                text = (check_repository.ROOT / name).read_text(encoding='utf-8')
                blocks = text.split('```sh\n')[1:]
                commands = [block.split('```', 1)[0].splitlines() for block in blocks]
                self.assertTrue(
                    any('python3 -B -m scripts.check_repository' in lines
                        for lines in commands),
                    f'{name}: shell examples must include the shared check command',
                )
        workflow = (check_repository.ROOT / '.github/workflows/tests.yml').read_text(
            encoding='utf-8')
        self.assertIn('      - run: python -B -m scripts.check_repository',
                      workflow.splitlines())

    def test_checks_share_environment_interpreter_and_root(self):
        with patch.dict(os.environ, {'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'ascii',
                                     'CHECK_SENTINEL': 'preserved'}):
            before = os.environ.copy()
            with patch.object(check_repository.subprocess, 'run') as run:
                run.return_value.returncode = 0
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(check_repository.main(), 0)
                self.assertEqual(len(run.call_args_list), 3)
                for call, args in zip(run.call_args_list, check_repository.CHECKS):
                    self.assertEqual(call.args[0], [sys.executable, '-B', *args])
                    self.assertEqual(call.kwargs['cwd'], check_repository.ROOT)
                    env = call.kwargs['env']
                    self.assertEqual(env['PYTHONUTF8'], '0')
                    self.assertEqual(env['PYTHONIOENCODING'], 'utf-8')
                    self.assertEqual(env['CHECK_SENTINEL'], 'preserved')
            self.assertEqual(os.environ.copy(), before)

    def test_failure_stops_later_checks_and_preserves_exit_code(self):
        for failed_index in range(len(check_repository.CHECKS)):
            with self.subTest(failed_index=failed_index):
                results = [subprocess.CompletedProcess([], 0)] * failed_index
                results.append(subprocess.CompletedProcess([], 7))
                with patch.object(check_repository.subprocess, 'run', side_effect=results) as run:
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(check_repository.main(), 7)
                    self.assertEqual(run.call_count, failed_index + 1)

    def test_cli_from_other_directory_sets_child_stream_encoding(self):
        # A tiny stand-in check exercises the real runner without recursive tests.
        runner = Path(check_repository.__file__).resolve()
        probe = ("import sys; print('中文输出'); "
                 "assert sys.flags.utf8_mode == 0; "
                 "assert sys.stdout.encoding.lower() == 'utf-8'")
        code = ('from scripts import check_repository as runner; '
                f'runner.CHECKS = (("-c", {probe!r}),); '
                'raise SystemExit(runner.main())')
        env = os.environ.copy()
        env.update(PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
                   PYTHONPATH=str(runner.parents[1]))
        with tempfile.TemporaryDirectory() as outside:
            result = subprocess.run([sys.executable, '-B', '-c', code], cwd=outside,
                                    env=env, capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('中文输出', result.stdout)


if __name__ == '__main__':
    unittest.main()
