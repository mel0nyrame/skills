"""Verify reproducible fixture preparation and historical instruction identity."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts import scenario_fixture as fixture


class ScenarioFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        self.destination = self.root.parent / 'project'
        for name, skill in fixture.SCENARIOS.items():
            relative = Path('tests/fixtures/scenarios') / name
            shutil.copytree(fixture.ROOT / relative, self.root / relative)
            relative = Path('skills/engineering') / skill
            shutil.copytree(fixture.ROOT / relative, self.root / relative)
        fixture.git(self.root, 'init', '-b', 'main')
        self.commit('test: source fixtures')

    def commit(self, message):
        fixture.git(self.root, 'add', '.')
        fixture.git(self.root, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                    'commit', '-m', message)

    def test_both_scenarios_have_only_their_selected_skill(self):
        for name, skill in fixture.SCENARIOS.items():
            destination = self.root.parent / name
            fixture.prepare(self.root, name, destination)
            self.assertEqual(fixture.check_source(self.root, destination), [])
            supplied = destination / '.agents/skills'
            self.assertEqual([path.name for path in supplied.iterdir()], [skill])
            self.assertEqual(fixture.git(destination, 'status', '--porcelain'), b'')

    def test_historical_source_stays_valid_after_new_commit(self):
        manifest = fixture.prepare(self.root, 'prose-generated', self.destination)
        source = self.root / 'skills/engineering/project-prose/SKILL.md'
        source.write_text(source.read_text(encoding='utf-8') + '\nNew instructions.\n', encoding='utf-8')
        self.commit('test: revise current instructions')
        self.assertEqual(fixture.check_source(self.root, self.destination), [])
        historical = self.root.parent / 'historical'
        rebuilt = fixture.prepare(self.root, 'prose-generated', historical, manifest['commit'])
        self.assertEqual(rebuilt, manifest)

    def test_generated_fixture_starts_in_sync(self):
        fixture.prepare(self.root, 'prose-generated', self.destination)
        subprocess.run([sys.executable, '-B', 'generate_docs.py'], cwd=self.destination,
                       check=True, capture_output=True)
        self.assertEqual(fixture.git(self.destination, 'status', '--porcelain'), b'')

    def test_edited_project_output_is_allowed_but_changed_skill_fails(self):
        fixture.prepare(self.root, 'prose-generated', self.destination)
        (self.destination / 'docs/export.md').write_text('Rewritten output.\n', encoding='utf-8')
        self.assertEqual(fixture.check_source(self.root, self.destination), [])
        instruction = self.destination / '.agents/skills/project-prose/SKILL.md'
        instruction.write_text('Different instructions.\n', encoding='utf-8')
        self.assertTrue(fixture.check_source(self.root, self.destination))

    def test_incorrect_or_omitted_hashes_fail(self):
        manifest = fixture.prepare(self.root, 'git-review', self.destination)
        manifest['sha256'].pop(next(iter(manifest['sha256'])))
        (self.destination / fixture.MANIFEST).write_text(json.dumps(manifest), encoding='utf-8')
        self.assertTrue(fixture.check_source(self.root, self.destination))

    def test_mutable_source_name_is_rejected(self):
        manifest = fixture.prepare(self.root, 'git-review', self.destination)
        manifest['commit'] = 'HEAD'
        (self.destination / fixture.MANIFEST).write_text(json.dumps(manifest), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'immutable'):
            fixture.check_source(self.root, self.destination)

    def test_existing_destination_is_preserved(self):
        self.destination.mkdir()
        marker = self.destination / 'keep.txt'
        marker.write_text('Keep me.', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            fixture.prepare(self.root, 'git-review', self.destination)
        self.assertEqual(marker.read_text(encoding='utf-8'), 'Keep me.')


if __name__ == '__main__':
    unittest.main()
