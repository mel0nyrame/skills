"""Exercise language compatibility and ADR validation boundaries."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" / "engineering"
          / "decisions" / "scripts" / "check_adr.py")
SPEC = importlib.util.spec_from_file_location("check_adr", SCRIPT)
ADR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADR)

SCHEMAS = {
    "en": ("Status", ("Problem", "Decision", "Alternatives", "Consequences and risks")),
    "zh": ("状态", ("问题", "决策", "备选方案", "后果与风险")),
}


def record(language="en", state="implemented"):
    field, sections = SCHEMAS[language]
    return (f"# Storage choice\n\n{field}: {state}\n\n"
            + "\n\n".join(f"## {title}\n\nEvidence and reasoning."
                            for title in sections) + "\n")


class CheckADRTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / "0001--storage.md"

    def tearDown(self):
        self.temp.cleanup()

    def check_text(self, text):
        self.path.write_text(text, encoding="utf-8")
        return ADR.check(self.path)

    def test_both_languages_and_active_states(self):
        for language in ("en", "zh"):
            for state in ("proposed", "implemented", "rejected", "superseded"):
                with self.subTest(language=language, state=state):
                    self.assertEqual(self.check_text(record(language, state)), [])

    def test_existing_chinese_fullwidth_status(self):
        self.assertEqual(self.check_text(record("zh").replace("状态:", "状态：")), [])

    def test_invalid_or_duplicate_statuses(self):
        for status in ("", "Status: unknown", "Status: implemented rejected",
                       "- Status: implemented", "Status: implemented\n状态: implemented",
                       "Status: implemented\nStatus: implemented"):
            with self.subTest(status=status):
                text = record().replace("Status: implemented", status)
                self.assertTrue(self.check_text(text))

    def test_archived_status_is_not_active(self):
        self.assertTrue(self.check_text(record(state="archived")))

    def test_required_title_order_and_contents(self):
        for language in ("en", "zh"):
            text = record(language)
            _, sections = SCHEMAS[language]
            broken = (
                text.replace("# Storage choice", "Storage choice"),
                text.replace(f"## {sections[1]}", "## Extra"),
                text.replace(f"## {sections[1]}", f"## {sections[0]}"),
                text.replace(f"## {sections[0]}\n\nEvidence and reasoning.",
                             f"## {sections[0]}\n\n<!-- only a comment -->"),
                text.replace(sections[0], "TEMP").replace(sections[1], sections[0])
                    .replace("TEMP", sections[1]),
            )
            for candidate in broken:
                with self.subTest(language=language, text=candidate):
                    self.assertTrue(self.check_text(candidate))

    def test_mixed_schema_is_rejected(self):
        self.assertTrue(self.check_text(record().replace("Status:", "状态:")))
        self.assertTrue(self.check_text(record() + "\n## 问题\n\nExtra text.\n"))

    def test_status_must_precede_sections(self):
        text = record().replace("Status: implemented\n", "")
        self.assertTrue(self.check_text(text + "\nStatus: implemented\n"))

    def test_fenced_examples_do_not_create_statuses_headings_or_links(self):
        text = record() + "\n```markdown\nStatus: unknown\n## Problem\n[example](missing.md)\n```\n"
        self.assertEqual(self.check_text(text), [])

    def test_code_can_satisfy_nonempty_section(self):
        text = record().replace("Evidence and reasoning.", "```text\nactual content\n```", 1)
        self.assertEqual(self.check_text(text), [])

    def test_local_links_and_reference_links(self):
        (self.root / "real file.md").write_text("# Linked record\n")
        text = record() + "\n[valid](real%20file.md#section)\n[remote](https://example.com/a)\n"
        self.assertEqual(self.check_text(text), [])
        self.assertTrue(self.check_text(text + "\n[bad][missing]\n[missing]: absent.md\n"))

    def test_directory_excludes_archives_and_entry_files(self):
        self.path.write_text(record())
        for name in ("README.md", "AGENTS.md", "CLAUDE.md"):
            (self.root / name).write_text("Not an ADR")
        for directory in ("archive", "archived"):
            (self.root / directory).mkdir()
            (self.root / directory / "old.md").write_text("Not an active ADR")
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.root)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 active records", result.stdout)
        archived = subprocess.run([sys.executable, "-B", str(SCRIPT),
                                   str(self.root / "archive" / "old.md")],
                                  text=True, capture_output=True)
        self.assertNotEqual(archived.returncode, 0)

    def test_missing_path_fails(self):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.path)],
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
