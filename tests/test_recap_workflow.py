"""Run candidate maintenance through disposable Git libraries."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "skills/knowledge/recap/scripts"
sys.path.insert(0, str(SCRIPTS))
import documents as doc
import knowledge
import workflow
from storage import KnowledgeError, digest, git, head, json_bytes


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "library"
        workflow.initialize(self.root)

    def packet(self, identifier, changes):
        path = Path(self.temp.name) / f"{identifier}.json"
        path.write_bytes(json_bytes({"id": identifier, "writer_id": "writer", "changes": changes}))
        return path

    def guide(self, identifier, body):
        return self.packet(identifier, [{"path": "index.md", "kind": "update",
            "expected_sha256": digest((self.root / "index.md").read_bytes()),
            "reason": "Maintain the reading route", "evidence": ["reviewed route"],
            "document": {"body": body}}])

    def approve(self, identifier, fingerprint):
        path = Path(self.temp.name) / "approval.json"
        path.write_bytes(json_bytes({"candidate_sha256": fingerprint, "evidence_locator": "test user approval"}))
        workflow.approve(self.root, identifier, path)

    def publish_topic(self, identifier):
        source = doc.render({"schema": "recap-source/v2", "host": "export", "session_id": identifier,
            "acquired": "2026-11-04", "locator": "fixture", "cutoff": "message 1",
            "coverage": {"status": "complete", "scope": "fixture", "inspected": ["message 1"], "gaps": []}},
            "# Source\n\nAn inspected fixture.\n")
        changes = [{"path": f"sources/{identifier}.md", "expected_sha256": None, "kind": "add",
            "reason": "Retain fixture evidence", "evidence": ["fixture message 1"], "content": source},
            {"path": f"topics/{identifier}.md", "expected_sha256": None, "kind": "add",
            "reason": "Explain the fixture", "evidence": ["fixture message 1"],
            "document": {"title": identifier, "type": "concept", "acquired": "2026-11-04",
                "sources": [f"../sources/{identifier}.md"], "summary": "Fixture scope and explanation",
                "body": f"# {identifier}\n\nAn independent explanation.\n\n[Source](../sources/{identifier}.md)\n"}}]
        result = workflow.inspect(self.root, self.packet(identifier, changes))
        workflow.publish(self.root, identifier, result["approval_sha256"])
        return result

    def test_guide_update_uses_candidate_and_requires_exact_user_approval(self):
        original = (self.root / "index.md").read_bytes()
        result = workflow.inspect(self.root, self.guide("route", "# Reading route\n\nStart with the current topics.\n\n"))
        self.assertEqual((self.root / "index.md").read_bytes(), original)
        self.assertTrue(result["reserved_reasons"])
        tree = Path(result["worktree"])
        self.assertIn("<!-- recap:topics:start -->", (tree / "index.md").read_text())
        with self.assertRaisesRegex(KnowledgeError, "explicit user approval"):
            workflow.publish(self.root, "route", result["approval_sha256"])
        self.approve("route", result["approval_sha256"])
        workflow.publish(self.root, "route", result["approval_sha256"])
        self.assertIn("Start with the current topics.", (self.root / "index.md").read_text())
        workflow.cleanup(self.root, "route")

    def test_guide_packet_cannot_replace_generated_catalog_or_publisher_rules(self):
        for body in ("# Route\n\n<!-- recap:topics:start -->\nInjected catalog\n<!-- recap:topics:end -->\n",):
            with self.assertRaises((KnowledgeError, doc.DocumentError)):
                workflow.inspect(self.root, self.guide("bad-route", body))
        packet = self.packet("rules", [{"path": "AGENTS.md", "kind": "update",
            "expected_sha256": digest((self.root / "AGENTS.md").read_bytes()),
            "reason": "Replace rules", "evidence": ["test"], "content": "# Replaced\n"}])
        with self.assertRaises(KnowledgeError):
            workflow.inspect(self.root, packet)

    def test_guide_integration_preserves_new_catalog_and_invalidates_old_approval(self):
        self.publish_topic("first")
        result = workflow.inspect(self.root, self.guide("route", "# Route\n\nChoose the newest relevant topic.\n"))
        self.approve("route", result["approval_sha256"])
        self.publish_topic("second")
        integrated = workflow.integrate(self.root, "route")
        self.assertEqual(integrated["status"], "ready")
        self.assertFalse(integrated["review_required"])
        self.assertNotEqual(integrated["approval_sha256"], result["approval_sha256"])
        content = (Path(integrated["worktree"]) / "index.md").read_text()
        self.assertIn("topics/second.md", content)
        self.assertIn("Choose the newest relevant topic.", content)
        with self.assertRaisesRegex(KnowledgeError, "explicit user approval"):
            workflow.publish(self.root, "route", integrated["approval_sha256"])
        self.approve("route", integrated["approval_sha256"])
        workflow.publish(self.root, "route", integrated["approval_sha256"])

    def test_concurrent_guide_changes_require_review_and_keep_conflicting_work(self):
        first = workflow.inspect(self.root, self.guide("one", "# Route\n\nRead the first topic.\n"))
        second = workflow.inspect(self.root, self.guide("two", "# Route\n\nRead the second topic.\n"))
        self.approve("one", first["approval_sha256"])
        workflow.publish(self.root, "one", first["approval_sha256"])
        integrated = workflow.integrate(self.root, "two")
        self.assertEqual(integrated["status"], "conflict")
        self.assertEqual(integrated["conflicts"], ["index.md"])
        self.assertTrue(integrated["review_required"])
        resolution = Path(self.temp.name) / "resolve.json"
        resolution.write_bytes(json_bytes({"changes": [{"path": "index.md", "kind": "update",
            "expected_sha256": digest((self.root / "index.md").read_bytes()),
            "reason": "Reconcile routes", "evidence": ["both topic routes"],
            "document": {"body": "# Route\n\nChoose either relevant topic.\n"}}]}))
        resolved = workflow.resolve(self.root, "two", resolution)
        self.assertEqual(resolved["status"], "needs-review")
        with self.assertRaises(KnowledgeError):
            workflow.publish(self.root, "two", resolved["approval_sha256"])
        self.assertTrue(Path(second["worktree"]).exists())

    def test_conflict_free_concurrent_introduction_edits_still_require_review(self):
        original = '# Route\n\nFirst route.\n\nMiddle route.\n\nLast route.\n'
        seeded = workflow.inspect(self.root, self.guide('seed', original))
        self.approve('seed', seeded['approval_sha256'])
        workflow.publish(self.root, 'seed', seeded['approval_sha256'])
        first = workflow.inspect(self.root, self.guide('one', original.replace('First route.', 'Updated first route.')))
        workflow.inspect(self.root, self.guide('two', original.replace('Last route.', 'Updated last route.')))
        self.approve('one', first['approval_sha256'])
        workflow.publish(self.root, 'one', first['approval_sha256'])
        integrated = workflow.integrate(self.root, 'two')
        self.assertEqual(integrated['status'], 'needs-review')
        self.assertEqual(integrated['conflicts'], [])
        content = (Path(integrated['worktree']) / 'index.md').read_text()
        self.assertIn('Updated first route.', content)
        self.assertIn('Updated last route.', content)
        with self.assertRaises(KnowledgeError):
            workflow.publish(self.root, 'two', integrated['approval_sha256'])

    def test_guide_suffix_is_preserved_and_malformed_markers_are_rejected(self):
        self.publish_topic("first")
        guide = self.root / "index.md"
        guide.write_text(guide.read_text() + "\nKeep this trailing note.\n")
        git(self.root, "add", "--", "index.md")
        git(self.root, "commit", "-m", "Fixture trailing note")
        result = workflow.inspect(self.root, self.guide("route", "# Route\n\nRead a topic.\n"))
        self.assertTrue((Path(result["worktree"]) / "index.md").read_text().endswith("Keep this trailing note.\n"))
        with self.assertRaises(KnowledgeError):
            workflow.guide_parts("<!-- recap:topics:end --><!-- recap:topics:start -->")

    def test_status_all_reports_missing_candidates_without_deleting_state(self):
        workflow.begin(self.root, "retained", "writer")
        workflow.begin(self.root, "missing", "writer")
        git(self.root, "worktree", "remove", str(self.root / ".worktree/missing"))
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(knowledge.main(["--root", str(self.root), "status", "--all"]), 0)
        states = {s["id"]: s for s in json.loads(output.getvalue())["operations"]}
        self.assertTrue(states["retained"]["worktree_exists"])
        self.assertFalse(states["missing"]["worktree_exists"])
        self.assertFalse(states["retained"]["publication_record_exists"])
        self.assertTrue((self.root / ".state/operations/missing.json").exists())
        with self.assertRaisesRegex(KnowledgeError, "successfully published"):
            workflow.cleanup(self.root, "retained")

    def test_status_all_shows_published_records_and_pending_recovery(self):
        self.publish_topic("saved")
        transactions = self.root / ".state/transactions"
        transactions.mkdir(exist_ok=True)
        (transactions / "interrupted.json").write_bytes(json_bytes({"id": "interrupted", "status": "prepared"}))
        result = workflow.status(self.root)
        self.assertEqual(result["recovery_required"], ["interrupted"])
        self.assertTrue(result["operations"][0]["publication_record_exists"])

    def test_packet_generator_uses_operation_base_and_does_not_inspect(self):
        workflow.begin(self.root, "route", "writer")
        staging = Path(self.temp.name) / "staging"
        staging.mkdir()
        (staging / "index.md").write_text("# Reading route\n\nChoose a topic below.\n")
        (staging / "changes.json").write_bytes(json_bytes({"changes": [{"path": "index.md", "kind": "update",
            "reason": "Refresh the route", "evidence": ["reviewed current topics"]}]}))
        base_hash = digest((self.root / "index.md").read_bytes())
        self.publish_topic("newer")
        original_head = head(self.root)
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(knowledge.main(["--root", str(self.root), "packet", "route", "--from-dir", str(staging)]), 0)
        packet = json.loads(output.getvalue())
        self.assertEqual(packet["changes"][0]["expected_sha256"], base_hash)
        self.assertNotEqual(base_hash, digest((self.root / "index.md").read_bytes()))
        self.assertEqual(packet["changes"][0]["document"]["body"], (staging / "index.md").read_text())
        self.assertEqual(workflow.get_state(self.root, "route")["status"], "editing")
        self.assertEqual(head(self.root), original_head)

    def test_packet_builds_topics_and_sources_without_inventing_evidence(self):
        self.publish_topic("first")
        workflow.begin(self.root, "update", "writer")
        staging = Path(self.temp.name) / "staging"
        (staging / "topics").mkdir(parents=True)
        path = "topics/first.md"
        content = (self.root / path).read_text().replace("An independent explanation.", "An expanded explanation.")
        (staging / path).write_text(content)
        declarations = {"changes": [{"path": path, "kind": "update", "reason": "Explain the condition",
                                     "evidence": ["inspected fixture correction"]}]}
        (staging / "sources").mkdir()
        (staging / "sources/first.md").write_bytes((self.root / "sources/first.md").read_bytes())
        declarations['changes'].append({'path': 'sources/first.md', 'kind': 'update',
            'reason': 'Preserve inspected source', 'evidence': ['fixture message 1']})
        (staging / "changes.json").write_bytes(json_bytes(declarations))
        packet = workflow.build_packet(self.root, "update", staging)
        item = packet["changes"][0]
        self.assertNotIn("created", item["document"])
        self.assertNotIn("updated", item["document"])
        self.assertNotIn("content", item)
        self.assertIn("expanded", item["document"]["body"])
        self.assertIn('content', packet['changes'][1])
        self.assertNotIn('document', packet['changes'][1])
        declarations["changes"][0]["evidence"] = []
        (staging / "changes.json").write_bytes(json_bytes(declarations))
        with self.assertRaises(doc.DocumentError):
            workflow.build_packet(self.root, "update", staging)

    def test_packet_rejects_symlinks_duplicate_paths_and_missing_reasons(self):
        workflow.begin(self.root, "route", "writer")
        staging = Path(self.temp.name) / "staging"
        staging.mkdir()
        (staging / "index.md").symlink_to(self.root / "index.md")
        item = {"path": "index.md", "kind": "update", "reason": "Refresh", "evidence": ["reviewed route"]}
        manifest = staging / "changes.json"
        manifest.write_bytes(json_bytes({"changes": [item]}))
        with self.assertRaises(KnowledgeError):
            workflow.build_packet(self.root, "route", staging)
        (staging / "index.md").unlink()
        (staging / "index.md").write_text("# Route\n\nRead a topic.\n")
        manifest.write_bytes(json_bytes({"changes": [item, item]}))
        with self.assertRaisesRegex(KnowledgeError, "Duplicate"):
            workflow.build_packet(self.root, "route", staging)
        del item["reason"]
        manifest.write_bytes(json_bytes({"changes": [item]}))
        with self.assertRaises(doc.DocumentError):
            workflow.build_packet(self.root, "route", staging)

    def test_invalid_edit_purpose_gives_actionable_error_without_creating_library(self):
        absent = Path(self.temp.name) / 'absent'
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'knowledge.py'), '--root', str(absent),
            'read', 'topics/example.md', '--purpose', 'edit'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Use --purpose topic', result.stderr)
        self.assertFalse(absent.exists())

    def test_status_requires_one_selector_and_single_operation_remains_compatible(self):
        workflow.begin(self.root, 'retained', 'writer')
        for arguments in (['status'], ['status', 'retained', '--all']):
            with self.subTest(arguments=arguments):
                result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'knowledge.py'), '--root', str(self.root),
                    *arguments], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(knowledge.main(['--root', str(self.root), 'status', 'retained']), 0)
        self.assertEqual(json.loads(output.getvalue())['id'], 'retained')

    def test_ignored_file_error_names_blocker_and_keeps_bytes(self):
        result = workflow.inspect(self.root, self.guide("route", "# Route\n\nRead the current topics.\n"))
        extra = Path(result["worktree"]) / ".DS_Store"
        extra.write_bytes(b"preserve this")
        with self.assertRaisesRegex(KnowledgeError, r"\.DS_Store"):
            workflow.integrate(self.root, "route")
        self.assertEqual(extra.read_bytes(), b"preserve this")


if __name__ == "__main__":
    unittest.main()
