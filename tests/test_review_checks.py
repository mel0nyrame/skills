"""Exercise documentation and PR checks with valid and invalid inputs."""

from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

from scripts import check_docs, check_pr_body


VALID_PR = '''## Summary

```diff
- temporary check
+ repository check
```

## Evidence

- **Before:** Broken links reached review.
  **After:** The checker rejects a missing target and passes a valid link.

## Merge Danger

**Door:** two-way

**Blast Radius:** checks
'''


class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init'], cwd=self.root, check=True, capture_output=True)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def test_encoded_paths_anchors_and_reference_links(self):
        self.write('中文 file.md', '# `Some` API\n\n# 重复\n\n# 重复\n')
        path = self.write('source.md', '[code](%E4%B8%AD%E6%96%87%20file.md#some-api)\n'
                          '[duplicate][ref]\n[ref]: <中文 file.md#重复-1> "Title"\n')
        self.assertEqual(check_docs.check_document(path), [])
        path.write_text('[bad](中文%20file.md#missing)\n[undefined][absent]\n', encoding='utf-8')
        errors = check_docs.check_document(path)
        self.assertTrue(any('missing anchor' in error for error in errors))
        self.assertTrue(any('undefined reference' in error for error in errors))

    def test_fences_comments_inline_code_and_remote_urls(self):
        path = self.write('source.md', '````md\n```\n[example](missing.md)\n````\n'
                          '`[inline](missing.md)`\n<!-- [comment](missing.md) -->\n'
                          '[remote](https://example.invalid/anything#absent)\n')
        self.assertEqual(check_docs.check_document(path), [])

    def test_parentheses_setext_and_explicit_anchors(self):
        self.write('api(v2).md', 'API &amp; Types\n===\n\n<a id="custom"></a>\n')
        path = self.write('source.md', '[api](api(v2).md#api--types)\n'
                          '[html](api(v2).md#custom)\n')
        self.assertEqual(check_docs.check_document(path), [])

    def test_duplicate_heading_collisions(self):
        self.assertEqual(check_docs.anchors('# A\n# A\n# A-1\n# A\n'),
                         {'a', 'a-1', 'a-1-1', 'a-2'})

    def test_heading_formatting_preserves_code_underscores(self):
        self.assertEqual(check_docs.anchors('# **Public** _API_ and `__init__`\n'),
                         {'public-api-and-__init__'})

    def test_repository_scan_pairs_and_fixture_exclusion(self):
        self.write('README.md', '[中文](README.zh.md)\n')
        self.write('README.zh.md', '[English](README.md)\n')
        self.write('docs/guide.md', '[中文](guide.zh.md)\n')
        self.write('docs/guide.zh.md', '[English](guide.md)\n')
        self.write('tests/fixtures/invalid.md', '[deliberate](absent.md)\n')
        self.assertEqual(check_docs.check(self.root)[1], [])
        (self.root / 'docs/guide.zh.md').unlink()
        self.assertTrue(any('missing bilingual pair' in error
                            for error in check_docs.check(self.root)[1]))

    def test_missing_target_and_missing_reciprocal_link(self):
        self.write('README.md', '[中文](README.zh.md)\n[bad](missing.md)\n')
        self.write('README.zh.md', '# 中文\n')
        errors = check_docs.check(self.root)[1]
        self.assertTrue(any('missing target' in error for error in errors))
        self.assertTrue(any('missing reciprocal' in error for error in errors))


class PullRequestTests(unittest.TestCase):
    def test_event_cli_reads_body_as_data_and_rejects_missing_pull_request(self):
        with tempfile.TemporaryDirectory() as directory:
            event = Path(directory) / 'event.json'
            event.write_text(json.dumps({'pull_request': {'body': VALID_PR}}), encoding='utf-8')
            command = [sys.executable, '-B', '-m', 'scripts.check_pr_body', '--event', str(event)]
            root = Path(__file__).resolve().parents[1]
            result = subprocess.run(command, cwd=root, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            event.write_text('{}', encoding='utf-8')
            self.assertNotEqual(subprocess.run(command, cwd=root, capture_output=True).returncode, 0)
    def test_valid_diff_image_and_door_values(self):
        self.assertEqual(check_pr_body.check(VALID_PR), [])
        self.assertEqual(check_pr_body.check(VALID_PR.replace('\n', '\r\n')), [])
        image = VALID_PR.replace('```diff\n- temporary check\n+ repository check\n```',
                                 '![Result](https://example.invalid/result.png)')
        self.assertEqual(check_pr_body.check(image.replace('two-way', 'one-way')), [])

    def test_bad_sections_preamble_and_missing_visual(self):
        for body in (VALID_PR.replace('## Summary', '## Overview'),
                     'Unneeded preamble\n' + VALID_PR,
                     VALID_PR.replace('```diff\n- temporary check\n+ repository check\n```',
                                      'Generic description only.')):
            with self.subTest(body=body):
                self.assertTrue(check_pr_body.check(body))

    def test_fields_in_examples_do_not_count(self):
        body = VALID_PR.replace('- **Before:** Broken links reached review.',
                                '```text\n**Before:** example only\n```')
        self.assertTrue(any('Before' in error for error in check_pr_body.check(body)))

    def test_fake_headings_inside_visual_do_not_split_summary(self):
        body = VALID_PR.replace('- temporary check', '## Evidence\n- temporary check')
        self.assertEqual(check_pr_body.check(body), [])

    def test_empty_placeholder_and_invalid_danger_fields(self):
        for old, new in (('Broken links reached review.', ''),
                         ('Broken links reached review.', '<output>'),
                         ('two-way', 'reversible'), ('checks', 'many checks')):
            with self.subTest(new=new):
                self.assertTrue(check_pr_body.check(VALID_PR.replace(old, new)))


if __name__ == '__main__':
    unittest.main()
