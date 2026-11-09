"""Check recap retrieval against disposable topics, caches and Git libraries."""

from contextlib import closing
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "skills/knowledge/recap/scripts"
sys.path.insert(0, str(SCRIPTS))
import knowledge
import documents


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "topics").mkdir()
        (self.root / ".state").mkdir()
        # Exercise UTF-8 fixtures under a non-UTF-8 file default on every runner.
        original_read, original_write = Path.read_text, Path.write_text

        def gbk_read(path, encoding=None, errors=None, **kwargs):
            return original_read(path, encoding=encoding or 'gbk', errors=errors, **kwargs)

        def gbk_write(path, data, encoding=None, errors=None, **kwargs):
            return original_write(path, data, encoding=encoding or 'gbk', errors=errors, **kwargs)

        for method, replacement in (('read_text', gbk_read), ('write_text', gbk_write)):
            patcher = patch.object(Path, method, replacement)
            patcher.start()
            self.addCleanup(patcher.stop)

    def topic(self, name, title, body, aliases=None, summary=None, status="formal"):
        meta = {
            "schema": "recap-topic/v2", "title": title, "type": "concept",
            "status": status, "created": "2026-11-02", "updated": "2026-11-02",
            "acquired": "2026-11-02", "aliases": aliases or [],
            "sources": ["../sources/session-concurrency.md"],
            "summary": summary or title,
        }
        content = documents.render(meta, f"# {title}\n\n{body}\n")
        documents.validate_topic(content)
        path = self.root / "topics" / name
        path.write_text(content, encoding="utf-8")
        return path

    def results(self, query, fallback=False):
        if fallback:
            with patch.object(knowledge, "fts_available", return_value=False):
                return knowledge._search_unlocked(self.root, query, 100)["results"]
        if not knowledge.fts_available():
            self.skipTest("SQLite FTS5 unavailable")
        return knowledge._search_unlocked(self.root, query, 100)["results"]

    def paths(self, query, fallback=False):
        return [result["path"] for result in self.results(query, fallback)]

    def test_complete_identifiers_do_not_match_unrelated_members(self):
        self.topic("split.md", "Other calls", "Use session.stop and client.prompt.")
        self.topic("exact.md", "Selected call", "Use session.prompt to send input.")
        for fallback in (False, True):
            with self.subTest(fallback=fallback):
                self.assertEqual(self.paths("session.prompt", fallback), ["topics/exact.md"])
                self.assertEqual(set(self.paths("session", fallback)),
                                 {"topics/split.md", "topics/exact.md"})

    def test_underscores_and_namespaces_preserve_identifier_boundaries(self):
        self.topic("split.md", "Separate names", "foo bar and std vector")
        self.topic("exact.md", "Joined names", "foo_bar and std::vector")
        for query in ("foo_bar", "std::vector"):
            for fallback in (False, True):
                with self.subTest(query=query, fallback=fallback):
                    self.assertEqual(self.paths(query, fallback), ["topics/exact.md"])

    def test_metadata_and_link_destinations_do_not_create_candidates(self):
        self.topic("garden.md", "Garden", "Grow trees. [Source](../sources/session-concurrency.md)")
        for query in ("concurrency", "recap-topic", "formal", "2026-11-02"):
            for fallback in (False, True):
                with self.subTest(query=query, fallback=fallback):
                    self.assertEqual(self.paths(query, fallback), [])

    def test_searchable_fields_and_visible_link_labels_remain_available(self):
        self.topic("scope.md", "并发写入", "[排他锁](../sources/session-concurrency.md)",
                   aliases=["Atomicity"], summary="说明文件更新的适用条件")
        for query in ("并发", "Atomicity", "适用条件", "排他锁"):
            for fallback in (False, True):
                with self.subTest(query=query, fallback=fallback):
                    self.assertEqual(self.paths(query, fallback), ["topics/scope.md"])

    def test_phrase_must_not_cross_structured_fields(self):
        self.topic("scope.md", "更新规则", "取得锁。", aliases=["并发"], summary="安全")
        for fallback in (False, True):
            self.assertEqual(self.paths("并发安全", fallback), [])
            self.assertEqual(self.paths("并发 安全", fallback), ["topics/scope.md"])

    def test_snippet_prefers_explanation_and_preserves_original_line_number(self):
        path = self.topic("scope.md", "并发控制", "## 原理\n\n并发控制需要取得锁。\n锁可防止同时覆盖。")
        original_lines = path.read_text(encoding='utf-8').splitlines()
        for fallback in (False, True):
            result = self.results("并发控制", fallback)[0]
            self.assertTrue(result["snippet"].startswith("并发控制需要取得锁。"))
            self.assertEqual(original_lines[result["line"] - 1], "并发控制需要取得锁。")

    def test_alias_only_snippet_uses_body_instead_of_frontmatter(self):
        path = self.topic("scope.md", "更新规则", "写入前取得锁。", aliases=["Atomicity"])
        for fallback in (False, True):
            result = self.results("Atomicity", fallback)[0]
            self.assertNotIn('"aliases"', result["snippet"])
            self.assertIn(result["snippet"].splitlines()[0], path.read_text(encoding='utf-8').splitlines())
            self.assertGreaterEqual(result["line"], path.read_text(encoding='utf-8').splitlines().index("# 更新规则") + 1)

    def test_long_snippet_keeps_match_in_view(self):
        for prefix in ("x ", "ß "):
            self.topic("scope.md", "Long example", prefix * 400 + "session.prompt sends input.")
            for fallback in (False, True):
                with self.subTest(prefix=prefix, fallback=fallback):
                    result = self.results("session.prompt", fallback)[0]
                    self.assertLessEqual(len(result["snippet"]), 350)
                    self.assertIn("session.prompt", result["snippet"])

    def test_short_cjk_and_required_groups_keep_their_contract(self):
        self.topic("scope.md", "并发写入", "写入前取得锁。")
        for fallback in (False, True):
            for query in ("锁", "并发", "并发 写入"):
                self.assertEqual(self.paths(query, fallback), ["topics/scope.md"])
            for query in ("并发文件", "并发 不存在", "多个进程同时改文件怎么办", "原子性", "!!!"):
                self.assertEqual(self.paths(query, fallback), [])

    def test_fallback_and_fts_agree_on_case_accents_and_identifiers(self):
        self.topic("scope.md", "Tokens", "CAFÉ session.prompt foo_bar naïve")
        for query in ("café", "CAFÉ", "cafe", "session.prompt", "SESSION.PROMPT", "foo_bar", "naïve"):
            with self.subTest(query=query):
                self.assertEqual(self.paths(query), self.paths(query, True))

    def test_management_archives_hidden_files_and_symlinks_are_excluded(self):
        self.topic("scope.md", "Current", "retrievalmarker")
        self.topic("archive.md", "Old", "excludedmarker", status="archived")
        self.topic(".hidden.md", "Hidden", "excludedmarker")
        for name in ("sources", "drafts", ".history"):
            (self.root / name).mkdir()
            (self.root / name / "secret.md").write_text("excludedmarker", encoding='utf-8')
        try:
            (self.root / "topics/link.md").symlink_to(self.root / "sources/secret.md")
        except OSError as exc:
            if getattr(exc, 'winerror', None) != 1314:
                raise
            self.skipTest('Windows account lacks symbolic-link privilege')
        for fallback in (False, True):
            self.assertEqual(self.paths("excludedmarker", fallback), [])
            self.assertEqual(self.paths("retrievalmarker", fallback), ["topics/scope.md"])

    def test_cache_updates_rename_delete_archive_and_corruption(self):
        path = self.topic("scope.md", "当前专题", "firstmarker")
        self.assertEqual(self.paths("firstmarker"), ["topics/scope.md"])
        path.write_text(path.read_text(encoding='utf-8').replace("firstmarker", "secondmarker"), encoding='utf-8')
        self.assertEqual(self.paths("firstmarker"), [])
        self.assertEqual(self.paths("secondmarker"), ["topics/scope.md"])
        renamed = path.with_name("renamed.md")
        path.rename(renamed)
        self.assertEqual(self.paths("secondmarker"), ["topics/renamed.md"])
        renamed.write_text(renamed.read_text(encoding='utf-8').replace('"formal"', '"archived"'), encoding='utf-8')
        self.assertEqual(self.paths("secondmarker"), [])
        renamed.unlink()
        (self.root / ".state/index.sqlite").write_bytes(b"corrupt cache")
        result = knowledge._search_unlocked(self.root, "secondmarker")
        self.assertTrue(result["rebuilt"])
        self.assertEqual(result["results"], [])

    def test_existing_v1_cache_is_rebuilt_from_unchanged_topics(self):
        if not knowledge.fts_available():
            self.skipTest("SQLite FTS5 unavailable")
        path = self.topic("scope.md", "Garden", "Grow trees.")
        original = path.read_bytes()
        cache = self.root / ".state/index.sqlite"
        with closing(sqlite3.connect(cache)) as conn, conn:
            conn.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT)")
            conn.execute("INSERT INTO metadata VALUES ('schema','1')")
            conn.execute("CREATE TABLE documents (path TEXT PRIMARY KEY, sha TEXT, title TEXT, body TEXT)")
            conn.execute("CREATE VIRTUAL TABLE search USING fts5(path UNINDEXED, title, body)")
            conn.execute("INSERT INTO documents VALUES (?,?,?,?)", ("topics/scope.md", knowledge.digest(original), "Garden", original.decode()))
            conn.execute("INSERT INTO search VALUES (?,?,?)", ("topics/scope.md", "garden", "concurrency"))
        self.assertEqual(self.paths("concurrency"), [])
        self.assertEqual(self.paths("trees"), ["topics/scope.md"])
        self.assertEqual(path.read_bytes(), original)

    def test_title_hits_outrank_body_only_hits(self):
        self.topic("a-body.md", "Other", "needle")
        self.topic("z-title.md", "needle", "Other")
        self.assertEqual(self.paths("needle")[0], "topics/z-title.md")

    def test_plain_markdown_and_reference_links_remain_searchable(self):
        (self.root / "topics/plain.md").write_text(
            "# Older note\n\nUse session.prompt. [Visible label][ref]\n\n"
            "[ref]: ../sources/destinationmarker.md\n", encoding='utf-8'
        )
        for fallback in (False, True):
            for query in ("session.prompt", "Visible"):
                self.assertEqual(self.paths(query, fallback), ["topics/plain.md"])
            self.assertEqual(self.paths("destinationmarker", fallback), [])

    def test_reference_keys_are_excluded_but_labels_remain_searchable(self):
        self.topic("references.md", "References",
                   "[Visible label][ HiddenRefKey ] and [Collapsed label][]\n\n"
                   "[hiddenrefkey]: ../sources/example.md\n"
                   "[Collapsed label]: ../sources/example.md")
        for fallback in (False, True):
            with self.subTest(fallback=fallback):
                self.assertEqual(self.paths("hiddenrefkey", fallback), [])
                for query in ("Visible", "Collapsed"):
                    self.assertEqual(self.paths(query, fallback), ["topics/references.md"])

    def test_undefined_reference_syntax_remains_literal_text(self):
        self.topic("literal.md", "Literal text", "[Visible label][undefinedkey]")
        for fallback in (False, True):
            self.assertEqual(self.paths("undefinedkey", fallback), ["topics/literal.md"])

    def test_normalized_phrase_stays_visible_in_long_line_snippet(self):
        for phrase in ("并发，安全", "并发  安全"):
            path = self.topic("long.md", "Long example", "x " * 400 + phrase + "需要锁。")
            for fallback in (False, True):
                with self.subTest(phrase=phrase, fallback=fallback):
                    hit = self.results("并发安全", fallback)[0]
                    self.assertIn(phrase, hit["snippet"])
                    self.assertLessEqual(len(hit["snippet"]), 350)
                    self.assertIn(phrase, path.read_text(encoding='utf-8').splitlines()[hit["line"] - 1])

    def test_snippet_anchors_actual_identifier_after_a_similar_prefix(self):
        self.topic("long.md", "Long example",
                   "session.prompting " + "x " * 400 + "session.prompt sends input.")
        for fallback in (False, True):
            hit = self.results("session.prompt", fallback)[0]
            self.assertIn("session.prompt sends input.", hit["snippet"])

    def test_phrase_across_lines_keeps_original_start_line(self):
        path = self.topic("multiline.md", "Multiple lines", "说明文字。\n\n并发\n安全需要锁。")
        for fallback in (False, True):
            hit = self.results("并发安全", fallback)[0]
            self.assertIn("并发\n安全", hit["snippet"])
            self.assertEqual(path.read_text(encoding='utf-8').splitlines()[hit["line"] - 1], "并发")

    def test_link_projection_keeps_long_snippet_source_offsets(self):
        self.topic("long.md", "Long example",
                   "[Visible](../sources/" + "destination" * 50 + ".md) "
                   + "x " * 400 + "并发，安全需要锁。")
        for fallback in (False, True):
            hit = self.results("并发安全", fallback)[0]
            self.assertIn("并发，安全", hit["snippet"])

    def test_schema2_cache_rebuilds_changed_reference_projection(self):
        if not knowledge.fts_available():
            self.skipTest("SQLite FTS5 unavailable")
        path = self.topic("references.md", "References",
                          "[Visible label][hiddenrefkey]\n\n"
                          "[hiddenrefkey]: ../sources/example.md")
        original = path.read_bytes()
        cache = self.root / ".state/index.sqlite"
        with closing(sqlite3.connect(cache)) as conn, conn:
            conn.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT)")
            conn.execute("INSERT INTO metadata VALUES ('schema','2')")
            conn.execute("CREATE TABLE documents (path TEXT PRIMARY KEY, sha TEXT, title TEXT, body TEXT)")
            conn.execute("CREATE VIRTUAL TABLE search USING fts5(path UNINDEXED,title,aliases,summary,body)")
            conn.execute("INSERT INTO documents VALUES (?,?,?,?)",
                         ("topics/references.md", knowledge.digest(original), "References", original.decode()))
            conn.execute("INSERT INTO search VALUES (?,?,?,?,?)",
                         ("topics/references.md", "", "", "", knowledge.normalize("Visible label hiddenrefkey")))
        self.assertEqual(self.paths("hiddenrefkey"), [])
        self.assertEqual(self.paths("Visible"), ["topics/references.md"])
        self.assertEqual(path.read_bytes(), original)

    def test_public_search_and_read_keep_revision_checks(self):
        knowledge.initialize(self.root)
        path = self.topic("scope.md", "当前专题", "session.prompt sends input.")
        knowledge.git(self.root, "add", "--", "topics/scope.md")
        knowledge.git(self.root, "commit", "-m", "Add search fixture")
        available = knowledge.fts_available()
        for fallback in (False, True):
            if not fallback and not available:
                continue
            with patch.object(knowledge, "fts_available", return_value=not fallback):
                result = knowledge.search(self.root, "session.prompt")
            saved = knowledge.read_document(self.root, "topics/scope.md", "topic",
                                            expected_revision=result["revision"])
            self.assertIn("session.prompt", saved["content"])
        revision = result["revision"]
        path.write_text(path.read_text(encoding='utf-8').replace("sends input", "sends another input"), encoding='utf-8')
        knowledge.git(self.root, "add", "--", "topics/scope.md")
        knowledge.git(self.root, "commit", "-m", "Update search fixture")
        with self.assertRaisesRegex(knowledge.KnowledgeError, "revision changed"):
            knowledge.search(self.root, "session.prompt", expected_revision=revision)
        with self.assertRaisesRegex(knowledge.KnowledgeError, "revision changed"):
            knowledge.read_document(self.root, "topics/scope.md", "topic", expected_revision=revision)

    def test_pending_recovery_blocks_both_public_search_engines(self):
        transactions = self.root / ".state/transactions"
        transactions.mkdir()
        (transactions / "pending.json").write_text(json.dumps({"id": "pending", "status": "prepared"}), encoding='utf-8')
        for fallback in (False, True):
            with patch.object(knowledge, "fts_available", return_value=not fallback):
                with self.assertRaisesRegex(knowledge.KnowledgeError, "Recovery required"):
                    knowledge.search(self.root, "anything")

    def test_command_line_search_returns_body_location_and_revision(self):
        path = self.topic("scope.md", "选定调用", "session.prompt sends input.")
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "knowledge.py"), "--root", str(self.root),
             "search", "session.prompt"], capture_output=True, encoding='utf-8'
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("revision", payload)
        hit = payload["results"][0]
        self.assertEqual(hit["path"], "topics/scope.md")
        self.assertEqual(hit["title"], "选定调用")
        self.assertEqual(path.read_text(encoding='utf-8').splitlines()[hit["line"] - 1], "session.prompt sends input.")


if __name__ == "__main__":
    unittest.main()
