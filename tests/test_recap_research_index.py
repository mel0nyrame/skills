"""Keep research inventories explicit, navigable and separate from capture claims."""

from pathlib import Path
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/knowledge/recap/scripts'
sys.path.insert(0, str(SCRIPTS))
import research_index


class ResearchIndexTests(unittest.TestCase):
    def test_inventory_excludes_raw_management_and_symlinks_and_changes_nothing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / '2026-11-04').mkdir()
            report = root / '2026-11-04/a b.md'
            report.write_text('# A | B\n\nA concrete finding.\nContinued explanation.\n')
            for name in ('_raw', '.private'):
                (root / name).mkdir()
                (root / name / 'hidden.md').write_text('# Hidden\n\nDo not index.\n')
            (root / 'INDEX.md').write_text('existing index')
            try:
                (root / 'link.md').symlink_to(report)
                (root / 'linked-directory').symlink_to(root / '2026-11-04', target_is_directory=True)
            except OSError as exc:
                if getattr(exc, 'winerror', None) != 1314:
                    raise
                self.skipTest('Windows account lacks symbolic-link privilege')
            before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
            output = research_index.inventory(root)
            self.assertIn('[2026-11-04/a b.md](<2026-11-04/a%20b.md>)', output)
            self.assertIn('A \\| B', output)
            self.assertIn('A concrete finding. Continued explanation.', output)
            self.assertIn('| Unmarked |', output)
            self.assertNotIn('Hidden', output)
            self.assertNotIn('link.md', output)
            self.assertNotIn('linked-directory', output)
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_frontmatter_and_code_examples_do_not_become_summary(self):
        title, summary = research_index.describe('---\ntitle: metadata\n---\n'
            '# Report\n\n```python\nprint("not prose")\n```\n\nUseful explanation.\n', 'fallback')
        self.assertEqual((title, summary), ('Report', 'Useful explanation.'))


if __name__ == '__main__':
    unittest.main()
