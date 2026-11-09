"""Exercise real candidate workflows under native paths and a GBK default reader."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/knowledge/recap/scripts'
sys.path.insert(0, str(SCRIPTS))
import documents as doc
import knowledge
import workflow
from storage import git, json_bytes


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / 'library with spaces'

    def test_status_candidate_and_migration_accept_native_git_paths(self):
        workflow.initialize(self.root)
        result = workflow.status(self.root)
        self.assertTrue(result['complete'])
        self.assertEqual(result['recovery_required'], [])
        state = workflow.begin(self.root, 'native', 'writer')
        self.assertEqual(workflow.worktree(self.root, state), self.root / '.worktree/native')
        self.assertEqual(workflow.migration_plan(self.root)['schema'], 'recap-migration/v2')

    def chinese_packet(self):
        source = doc.render({'schema': 'recap-source/v2', 'host': 'export', 'session_id': 'fixture',
            'acquired': '2026-11-08', 'locator': 'fixture:1', 'cutoff': 'message 1',
            'coverage': {'status': 'complete', 'scope': 'fixture', 'inspected': ['message 1'], 'gaps': []}},
            '# 来源\n\n已检查的中文来源与适用条件。\n')
        receipt = {'schema': 'recap-session-receipt/v1', 'host': 'export', 'session_id': 'fixture',
            'captured_at': '2026-11-08T00:00:00Z', 'status': 'complete',
            'source': {'locator': 'fixture:1', 'prefix_sha256': '0' * 64},
            'range': {'after': -1, 'through': 1},
            'represented_by': {'topics': ['topics/example.md'], 'sources': ['sources/export-fixture.md']}}
        changes = [
            {'path': 'sources/export-fixture.md', 'content': source},
            {'path': 'topics/example.md', 'document': {'title': '中文知识', 'type': 'concept',
                'acquired': '2026-11-08', 'sources': ['../sources/export-fixture.md'],
                'summary': '说明中文知识的适用条件',
                'body': '# 中文知识\n\n独立可读的中文解释与适用条件。\n\n[来源](../sources/export-fixture.md)\n'}},
            {'path': '.state/cursors/fixture.json', 'content': json.dumps(receipt)}]
        for change in changes:
            change.update(kind='add', expected_sha256=None, reason='Preserve inspected knowledge', evidence=['fixture:1'])
        packet = Path(self.temp.name) / 'packet.json'
        packet.write_bytes(json_bytes({'id': 'chinese', 'writer_id': 'writer', 'changes': changes}))
        return packet

    def test_chinese_candidate_cursor_and_publication_with_gbk_default(self):
        workflow.initialize(self.root)
        packet = self.chinese_packet()
        original = Path.read_text

        def gbk_read(path, encoding=None, errors=None, **kwargs):
            return original(path, encoding=encoding or 'gbk', errors=errors, **kwargs)

        with patch.object(Path, 'read_text', gbk_read):
            result = workflow.inspect(self.root, packet)
            self.assertEqual(result['status'], 'ready')
            workflow.publish(self.root, 'chinese', result['approval_sha256'])
        topic = (self.root / 'topics/example.md').read_text(encoding='utf-8')
        self.assertIn('独立可读的中文解释', topic)
        self.assertIn('已检查的中文来源', (self.root / 'sources/export-fixture.md').read_text(encoding='utf-8'))
        self.assertTrue((self.root / '.state/cursors/fixture.json').is_file())
        self.assertEqual(git(self.root, 'status', '--porcelain').stdout, b'')

    def test_cli_status_and_chinese_inspect_with_utf8_mode_disabled(self):
        workflow.initialize(self.root)
        packet = self.chinese_packet()
        environment = {**os.environ, 'PYTHONUTF8': '0', 'PYTHONIOENCODING': 'utf-8'}
        for arguments in (['status', '--all'], ['inspect', str(packet)]):
            with self.subTest(command=arguments[0]):
                result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'knowledge.py'),
                    '--root', str(self.root), *arguments], env=environment, capture_output=True, encoding='utf-8')
                self.assertEqual(result.returncode, 0, result.stderr)
                data = json.loads(result.stdout)
                if arguments[0] == 'status':
                    self.assertTrue(data['complete'])
                    self.assertEqual(data['recovery_required'], [])
                else:
                    self.assertEqual(data['status'], 'ready')

    def test_documented_first_capture_inputs_generate_valid_candidates(self):
        workflow.initialize(self.root)
        reference = (SCRIPTS.parent / 'references/formats.md').read_text(encoding='utf-8')

        def example(heading, language):
            section = reference.split(heading, 1)[1]
            return re.search(r'```' + language + r'\n(.*?)\n```', section, re.S)[1] + '\n'

        manifest = json.loads(example('### Packet input directory', 'json'))
        topic = example('For `topics/Example.md`', 'markdown')
        source = doc.render(json.loads(example('## Source record', 'json')),
                            '# Source\n\nInspected fixture evidence for the example explanation.\n')
        cursor = example('A minimal illustrative cursor', 'json')
        for stored_header in (False, True):
            with self.subTest(stored_header=stored_header):
                identifier = 'stored' if stored_header else 'minimal'
                workflow.begin(self.root, identifier, 'writer')
                staging = Path(self.temp.name) / identifier
                files = {'topics/Example.md': topic, 'sources/export-exact-id.md': source,
                         '.state/cursors/exact-id.json': cursor}
                if stored_header:
                    metadata, body = doc.split_document(topic)
                    files['topics/Example.md'] = doc.build_topic({**metadata, 'body': body}, '2026-11-08')
                for path, content in files.items():
                    target = staging / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(content, encoding='utf-8')
                (staging / 'changes.json').write_bytes(json_bytes(manifest))
                built = workflow.build_packet(self.root, identifier, staging)
                filename = Path(self.temp.name) / (identifier + '.json')
                filename.write_bytes(json_bytes(built))
                self.assertEqual(workflow.inspect(self.root, filename)['status'], 'ready')

    def test_doctor_checks_portability_without_creating_an_absent_root(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = knowledge.main(['--root', str(self.root), 'doctor'])
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertTrue(result['portability']['ok'])
        self.assertEqual(result['portability']['errors'], [])
        self.assertFalse(result['creates_files'])
        self.assertFalse(self.root.exists())

    def test_doctor_rejects_each_reintroduced_encoding_and_path_bug(self):
        original = (SCRIPTS / 'workflow.py').read_text(encoding='utf-8')
        encoding_pattern = ".read_text(encoding='utf-8')"
        # Each corrected call and each root/candidate/migration comparison is checked independently.
        mutations = []
        for index in range(original.count(encoding_pattern)):
            parts = original.split(encoding_pattern)
            mutated = encoding_pattern.join(parts[:index + 1]) + '.read_text()' + encoding_pattern.join(parts[index + 1:])
            mutations.append(('encoding-' + str(index), mutated))
        for index, match in enumerate(re.finditer(r"Path\(git_text\([^\n]+?'--show-toplevel'\)\)\.resolve\(\)", original)):
            raw_git_text = match[0].removeprefix('Path(').removesuffix(').resolve()')
            mutated = original[:match.start()] + raw_git_text + original[match.end():]
            mutations.append(('path-' + str(index), mutated))
        self.assertEqual(len(mutations), 9)
        copy = Path(self.temp.name) / 'workflow.py'
        for name, mutated in mutations:
            with self.subTest(mutation=name):
                self.assertNotEqual(mutated, original)
                compile(mutated, str(copy), 'exec')
                copy.write_text(mutated, encoding='utf-8')
                output, errors = io.StringIO(), io.StringIO()
                with patch.object(workflow, '__file__', str(copy)), redirect_stdout(output), redirect_stderr(errors):
                    code = knowledge.main(['--root', str(self.root), 'doctor'])
                self.assertEqual(code, 2)
                self.assertFalse(json.loads(output.getvalue())['portability']['ok'])
                self.assertFalse(self.root.exists())


if __name__ == '__main__':
    unittest.main()
