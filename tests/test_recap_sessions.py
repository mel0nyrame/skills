"""Exercise supported session snapshots without touching a host's real history."""

from contextlib import closing
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "skills/knowledge/recap/scripts"
sys.path.insert(0, str(SCRIPTS))
import sessions


class OpenCodeSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.db = self.root / "host.db"
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("CREATE TABLE session_v2 (id TEXT, parent_id TEXT)")
            conn.execute("INSERT INTO session_v2 VALUES ('selected', NULL)")
            conn.execute("CREATE TABLE session_message (id TEXT, session_id TEXT, type TEXT, seq INTEGER, data TEXT)")
        self.add(4, "user", {"text": "Explain the rule."})
        self.add(7, "assistant", {"content": [{"type": "text", "text": "The rule applies to snapshots."}],
                                  "finish": "stop"})

    def add(self, seq, role, data):
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("INSERT INTO session_message VALUES (?, 'selected', ?, ?, ?)",
                         (f"message-{seq}", role, seq, json.dumps(data)))

    def extract(self, **overrides):
        args = dict(host="opencode", session_id="selected", db=str(self.db), input=None,
                    home=None, through=None, after=None, prior_receipt=None,
                    include_tools=False, chunk_chars=1000, knowledge_root=str(self.root / "library"),
                    output=str(self.root / f"extract-{len(list(self.root.glob('extract-*')))}"))
        args.update(overrides)
        return sessions.extract(SimpleNamespace(**args))

    def test_event_sequence_gaps_and_late_start_are_not_missing_messages(self):
        receipt = self.extract()
        self.assertEqual(receipt["status"], "complete", receipt["missing"])
        self.assertEqual(receipt["visible_messages"], 2)
        self.assertEqual(receipt["range"]["through"], 7)
        self.assertEqual(receipt["source"]["first_persisted_seq"], 4)
        self.assertEqual(receipt["source"]["sequence_gaps"]["count"], 1)
        records = [json.loads(line) for line in (self.root / "extract-0/records.jsonl").read_text(encoding='utf-8').splitlines()]
        self.assertEqual([r["locator"] for r in records], ["seq:4", "seq:7"])

    def test_missing_or_future_cutoff_remains_partial(self):
        for cutoff in (0, 5, 8):
            with self.subTest(cutoff=cutoff):
                self.assertEqual(self.extract(through=cutoff)["status"], "partial")

    def test_duplicate_sequences_and_malformed_records_are_not_complete(self):
        self.add(7, "user", {"text": "Duplicate position"})
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("INSERT INTO session_message VALUES ('broken', 'selected', 'user', 12, '{')")
        receipt = self.extract()
        self.assertEqual(receipt["status"], "partial")
        self.assertTrue(receipt["errors"])
        self.assertTrue(any('unique' in gap for gap in receipt["missing"]))

    def test_unverified_branch_streaming_attachments_and_unknown_rows_remain_partial(self):
        self.add(12, "assistant", {"content": [{"type": "text", "text": "Still streaming"}]})
        self.add(20, "user", {"text": "See attachment", "files": [{"name": "image"}]})
        self.add(29, "unsupported-host-record", {})
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("UPDATE session_v2 SET parent_id='parent'")
        receipt = self.extract()
        self.assertEqual(receipt["status"], "partial")
        self.assertTrue(receipt["unread_attachments"])
        self.assertTrue(receipt["unknown_envelopes"])
        self.assertTrue(any("streaming" in gap for gap in receipt["missing"]))
        self.assertTrue(any("branch" in gap for gap in receipt["missing"]))

    def test_incremental_event_positions_require_unchanged_previous_prefix(self):
        prior = self.extract()
        prior_path = self.root / "extract-0/receipt.json"
        self.add(20, "user", {"text": "A correction."})
        delta = self.extract(after=7, prior_receipt=str(prior_path))
        self.assertEqual(delta["status"], "complete")
        self.assertEqual(delta["visible_messages"], 1)
        self.assertTrue(delta["incremental"]["verified_prefix"])
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("UPDATE session_message SET data=? WHERE seq=4", (json.dumps({"text": "Changed"}),))
        changed = self.extract(after=7, prior_receipt=str(prior_path))
        self.assertEqual(changed["status"], "error")
        self.assertTrue(any("changed" in error for error in changed["errors"]))
        self.assertEqual(prior["source"]["persisted_rows"], 2)


    def test_show_chunk_preserves_long_text_and_locators_without_wide_json_lines(self):
        text = 'HEAD ' + '字' * 6000 + ' TAIL_SENTINEL\n\n    indented code\n'
        self.add(12, 'user', {'text': text})
        receipt = self.extract(chunk_chars=24000)
        chunk = self.root / 'extract-0' / receipt['chunks'][0]
        before = {p.name: p.read_bytes() for p in chunk.parent.iterdir()}
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'sessions.py'), 'show', str(chunk)],
            capture_output=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('seq:12', result.stdout)
        self.assertIn('HEAD ', result.stdout)
        self.assertIn(' TAIL_SENTINEL', result.stdout)
        self.assertIn('\n    indented code\n', result.stdout)
        self.assertEqual(result.stdout.count('字'), 6000)
        self.assertLessEqual(max(map(len, result.stdout.splitlines())), 160)
        clipped_json = '\n'.join(line[:2000] for line in chunk.read_text(encoding='utf-8').splitlines())
        clipped_text = '\n'.join(line[:2000] for line in result.stdout.splitlines())
        self.assertNotIn('TAIL_SENTINEL', clipped_json)
        self.assertIn('TAIL_SENTINEL', clipped_text)
        self.assertEqual({p.name: p.read_bytes() for p in chunk.parent.iterdir()}, before)

    def test_show_selected_ordinal_keeps_fragment_offsets(self):
        self.add(12, 'user', {'text': 'x' * 250})
        receipt = self.extract(chunk_chars=100)
        chunks = [self.root / 'extract-0' / name for name in receipt['chunks']]
        fragments = []
        for chunk in chunks:
            for record in map(json.loads, chunk.read_text(encoding='utf-8').splitlines()):
                if record['ordinal'] == 12:
                    fragments.append((chunk, record['text_offset']))
        self.assertEqual([offset for _, offset in fragments], [0, 100, 200])
        for chunk, offset in fragments:
            result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'sessions.py'), 'show', str(chunk),
                '--ordinal', '12'], capture_output=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f'offset={offset}/250', result.stdout)
            self.assertNotIn('Explain the rule.', result.stdout)

    def test_show_rejects_missing_ordinal_and_malformed_records_without_partial_output(self):
        self.extract()
        chunk = self.root / 'extract-0/chunk-0001.jsonl'
        for ordinal, content in [(999, None), (None, chunk.read_text(encoding='utf-8') + '{\n'),
                                 (None, '{"text": "not a chunk record"}\n')]:
            with self.subTest(ordinal=ordinal, content=content):
                if content is not None:
                    chunk.write_text(content, encoding='utf-8')
                args = [sys.executable, '-B', str(SCRIPTS / 'sessions.py'), 'show', str(chunk)]
                if ordinal is not None:
                    args += ['--ordinal', str(ordinal)]
                result = subprocess.run(args, capture_output=True, encoding='utf-8')
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertIn('error', json.loads(result.stderr))


if __name__ == "__main__":
    unittest.main()
