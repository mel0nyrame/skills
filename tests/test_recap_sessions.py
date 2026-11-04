"""Exercise supported session snapshots without touching a host's real history."""

from contextlib import closing
import json
from pathlib import Path
import sqlite3
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
        records = [json.loads(line) for line in (self.root / "extract-0/records.jsonl").read_text().splitlines()]
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


if __name__ == "__main__":
    unittest.main()
