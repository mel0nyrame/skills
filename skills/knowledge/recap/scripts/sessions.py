#!/usr/bin/env python3
"""Read an explicitly selected session into temporary, provenance-bearing chunks.

Python standard library only. Source databases use read-only SQLite connections.
This is a record reader, not a summarizer or a context-window bypass.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from typing import Any, Iterator


class SessionError(Exception):
    pass


def dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@contextmanager
def readonly(path: Path) -> Iterator[sqlite3.Connection]:
    if not path.is_file():
        raise SessionError("Source database does not exist")
    connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA query_only=ON")
        yield connection
    finally:
        connection.close()


def columns(connection: sqlite3.Connection, table: str) -> set[str]:
    # Table names here are constants, never user-provided SQL identifiers.
    return {row["name"] for row in connection.execute("PRAGMA table_info(" + table + ")")}


def locate_codex(session_id: str, home: Path, database: Path | None) -> Path:
    candidates = [database] if database else sorted(home.glob("state_*.sqlite"))
    matches: set[Path] = set()
    for candidate in candidates:
        try:
            with readonly(candidate) as connection:
                if not {"id", "rollout_path"} <= columns(connection, "threads"):
                    continue
                rows = connection.execute(
                    "SELECT rollout_path FROM threads WHERE id = ?", (session_id,)
                ).fetchall()
                for row in rows:
                    value = row["rollout_path"]
                    if value:
                        path = Path(value).expanduser()
                        matches.add((candidate.parent / path).resolve() if not path.is_absolute() else path.resolve())
        except (sqlite3.Error, SessionError) as exc:
            if database:
                raise SessionError("Cannot read the selected Codex index: " + str(exc)) from exc
    if len(matches) != 1:
        raise SessionError("Exact session lookup found %d rollout paths; supply --input explicitly" % len(matches))
    result = matches.pop()
    if not result.is_file():
        raise SessionError("The indexed rollout file is missing; use a complete host export")
    return result


class JsonlSnapshot:
    def __init__(self, path: Path):
        self.path = path.resolve()
        if not self.path.is_file():
            raise SessionError("Input file does not exist")
        stat = self.path.stat()
        self.bytes = stat.st_size
        self.identity = (stat.st_dev, stat.st_ino)
        self.cutoff_bytes = 0
        self.tail_bytes = 0
        self.sha256 = ""
        self.prefixes: dict[int, str] = {}
        self.errors: list[str] = []

    def rows(self, remember_prefixes: set[int] | None = None) -> Iterator[tuple[int, dict[str, Any]]]:
        remember_prefixes = remember_prefixes or set()
        digest = hashlib.sha256()
        ordinal = 0
        offset = 0
        errors: list[str] = []
        with self.path.open("rb") as handle:
            stat = os.fstat(handle.fileno())
            if (stat.st_dev, stat.st_ino) != self.identity or stat.st_size < self.bytes:
                raise SessionError("Input was replaced or truncated during extraction")
            while offset < self.bytes:
                raw = handle.readline(self.bytes - offset)
                if not raw:
                    break
                if not raw.endswith(b"\n"):
                    self.tail_bytes = len(raw)
                    break  # The active final row is not a stable JSONL boundary.
                offset += len(raw)
                ordinal += 1
                digest.update(raw)
                if ordinal in remember_prefixes:
                    self.prefixes[ordinal] = digest.hexdigest()
                try:
                    item = json.loads(raw)
                    if not isinstance(item, dict):
                        raise ValueError("record is not an object")
                except (ValueError, UnicodeDecodeError):
                    errors.append("Unreadable JSON object at line %d" % ordinal)
                    continue
                yield ordinal, item
        self.cutoff_bytes = offset
        self.sha256 = digest.hexdigest()
        self.prefixes.setdefault(0, hashlib.sha256(b"").hexdigest())
        self.errors = errors


def text_content(value: Any) -> tuple[str, int, int]:
    """Return display text, unrepresented attachments, unknown content parts."""
    if isinstance(value, str):
        return value, 0, 0
    if value is None:
        return "", 0, 0
    if not isinstance(value, list):
        return "", 0, 1
    texts: list[str] = []
    attachments = 0
    unknown = 0
    for part in value:
        if isinstance(part, str):
            texts.append(part)
            continue
        if not isinstance(part, dict):
            unknown += 1
            continue
        kind = part.get("type")
        if kind in {"input_text", "output_text", "text"} and isinstance(part.get("text"), str):
            texts.append(part["text"])
        elif kind in {"image", "input_image", "output_image", "audio", "input_audio", "file", "input_file", "video"}:
            attachments += 1
        elif kind in {"reasoning", "thinking", "redacted_thinking"}:
            continue
        else:
            unknown += 1
    return "\n".join(texts), attachments, unknown


def normalize_codex(item: dict[str, Any], ordinal: int, receipt: dict[str, Any], include_tools: bool) -> list[dict[str, Any]]:
    kind = item.get("type")
    payload = item.get("payload") or {}
    if not isinstance(payload, dict):
        receipt["missing"].append("Unsupported payload at line %d" % ordinal)
        return []
    locator = "line:%d" % ordinal
    if kind == "compacted":
        receipt["compaction"]["markers"].append(ordinal)
        return []
    if kind in {"session_meta", "turn_context", "world_state"}:
        receipt["skipped_noise"][kind] += 1
        return []
    if kind == "event_msg":
        event = payload.get("type", "unknown")
        if event in {"context_compacted", "compaction", "compacted"}:
            receipt["compaction"]["markers"].append(ordinal)
        elif event in {"user_message", "agent_message"}:
            receipt["event_message_count"] += 1
        receipt["skipped_noise"]["event_msg"] += 1
        return []
    if kind != "response_item":
        receipt["unknown_envelopes"].append({"ordinal": ordinal, "type": str(kind)})
        return []
    response_type = payload.get("type")
    if response_type == "message":
        role = payload.get("role")
        if role in {"system", "developer"} or payload.get("channel") == "analysis":
            receipt["skipped_noise"]["nonvisible_role_or_analysis"] += 1
            return []
        if role not in {"user", "assistant"}:
            receipt["missing"].append("Unsupported message role at " + locator)
            return []
        text, attachments, unknown = text_content(payload.get("content"))
        if attachments:
            receipt["unread_attachments"].append({"locator": locator, "count": attachments})
        if unknown:
            receipt["missing"].append("Unsupported message content at " + locator)
        if payload.get("summary") is True or payload.get("synthetic") is True:
            receipt["compaction"]["summary_placeholders"].append(ordinal)
            return []
        if not text:
            return []
        receipt["visible_messages"] += 1
        return [{"ordinal": ordinal, "role": role, "text": text, "locator": locator,
                 "message_id": payload.get("id"), "timestamp": item.get("timestamp")}]
    if response_type in {"function_call_output", "custom_tool_call_output", "tool_result"}:
        if not include_tools:
            receipt["skipped_noise"]["tool_output"] += 1
            return []
        value = payload.get("output", payload.get("content", ""))
        text, attachments, unknown = text_content(value)
        if attachments:
            receipt["unread_attachments"].append({"locator": locator, "count": attachments})
        if unknown:
            receipt["missing"].append("Unsupported tool evidence at " + locator)
        if text:
            return [{"ordinal": ordinal, "role": "evidence", "text": text, "locator": locator,
                     "message_id": payload.get("call_id"), "timestamp": item.get("timestamp")}]
        return []
    if response_type in {"function_call", "custom_tool_call", "reasoning", "web_search_call", "local_shell_call"}:
        receipt["skipped_noise"][str(response_type)] += 1
        return []
    receipt["missing"].append("Unsupported response item %r at %s" % (response_type, locator))
    return []


def normalize_opencode(kind: str, data: dict[str, Any], ordinal: int, message_id: str,
                       receipt: dict[str, Any], include_tools: bool) -> list[dict[str, Any]]:
    locator = "seq:%d" % ordinal
    result: list[dict[str, Any]] = []
    timestamp = data.get("time") or {}
    if not isinstance(timestamp, dict):
        receipt["missing"].append("Unsupported message time at " + locator)
        timestamp = {}
    if kind == "user":
        text = data.get("text", "")
        if not isinstance(text, str):
            receipt["missing"].append("Unsupported user text at " + locator)
            return []
        files = data.get("files") or []
        if not isinstance(files, list):
            receipt["missing"].append("Unsupported attachment metadata at " + locator)
            files = [files]
        if files:
            receipt["unread_attachments"].append({"locator": locator, "count": len(files)})
        if text:
            receipt["visible_messages"] += 1
            result.append({"role": "user", "text": text})
    elif kind == "assistant":
        content = data.get("content")
        if not isinstance(content, list):
            receipt["missing"].append("Unsupported assistant content at " + locator)
            return []
        texts: list[str] = []
        for part in content:
            if not isinstance(part, dict):
                receipt["missing"].append("Unsupported assistant part at " + locator)
                continue
            part_type = part.get("type")
            if part_type == "text" and isinstance(part.get("text"), str):
                texts.append(part["text"])
            elif part_type == "tool":
                if include_tools:
                    state = part.get("state") or {}
                    if not isinstance(state, dict):
                        receipt["missing"].append("Unsupported tool state at " + locator)
                        continue
                    evidence, attachments, unknown = text_content(state.get("content"))
                    if attachments:
                        receipt["unread_attachments"].append({"locator": locator, "count": attachments})
                    if unknown:
                        receipt["missing"].append("Unsupported tool evidence at " + locator)
                    if evidence:
                        result.append({"role": "evidence", "text": evidence, "tool_name": part.get("name")})
                else:
                    receipt["skipped_noise"]["tool_output"] += 1
            elif part_type != "reasoning":
                receipt["missing"].append("Unsupported assistant part at " + locator)
        if texts:
            receipt["visible_messages"] += 1
            result.insert(0, {"role": "assistant", "text": "\n".join(texts)})
        if not data.get("finish") and not timestamp.get("completed"):
            receipt["missing"].append("Assistant message may still be streaming at " + locator)
    elif kind == "compaction":
        receipt["compaction"]["markers"].append(ordinal)
    elif kind == "shell" and include_tools:
        output = data.get("output", "")
        if isinstance(output, str) and output:
            result.append({"role": "evidence", "text": output})
        elif output:
            receipt["missing"].append("Unsupported shell evidence at " + locator)
    elif kind in {"agent-switched", "model-switched", "location-switched", "synthetic", "system", "skill", "shell", "idle"}:
        receipt["skipped_noise"][kind] += 1
    else:
        receipt["unknown_envelopes"].append({"ordinal": ordinal, "type": str(kind)})
    for record in result:
        record.update({"ordinal": ordinal, "locator": locator, "message_id": message_id,
                       "timestamp": timestamp.get("created")})
    return result


def base_receipt(host: str, session_id: str) -> dict[str, Any]:
    return {"schema": "recap-session-receipt/v1", "host": host, "session_id": session_id,
            "captured_at": datetime.now(timezone.utc).isoformat(), "status": "partial",
            "source": {}, "range": {}, "branch": {}, "visible_messages": 0,
            "event_message_count": 0, "records_emitted": 0, "characters_emitted": 0,
            "chunks": [], "skipped_noise": Counter(), "unknown_envelopes": [],
            "compaction": {"markers": [], "summary_placeholders": []},
            "unread_attachments": [], "missing": [], "warnings": [], "errors": [],
            "incremental": {"requested": False, "verified_prefix": False},
            "boundary": "Coverage describes this frozen source snapshot, not unsaved or deleted host history."}


class ChunkWriter:
    def __init__(self, directory: Path, size: int, receipt: dict[str, Any]):
        if directory.exists():
            raise SessionError("Output must be a new temporary directory; refusing to overwrite")
        directory.mkdir(parents=True, mode=0o700)
        self.directory, self.size, self.receipt = directory, size, receipt
        self.records = self.open_private("records.jsonl")
        self.chunk = None
        self.chunk_size = 0

    def open_private(self, name: str):
        descriptor = os.open(self.directory / name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        return os.fdopen(descriptor, "w", encoding="utf-8")

    def add(self, record: dict[str, Any]):
        text = record["text"]
        for offset in range(0, len(text), self.size):
            fragment = dict(record, text=text[offset:offset + self.size], text_offset=offset,
                            text_length=len(text))
            if self.chunk is None or self.chunk_size + len(fragment["text"]) > self.size:
                if self.chunk:
                    self.chunk.close()
                name = "chunk-%04d.jsonl" % (len(self.receipt["chunks"]) + 1)
                self.chunk = self.open_private(name)
                self.receipt["chunks"].append(name)
                self.chunk_size = 0
            line = dump(fragment) + "\n"
            self.records.write(line)
            self.chunk.write(line)
            self.chunk_size += len(fragment["text"])
            self.receipt["records_emitted"] += 1
            self.receipt["characters_emitted"] += len(fragment["text"])

    def close(self):
        self.records.close()
        if self.chunk:
            self.chunk.close()

    def write_receipt(self):
        with self.open_private("receipt.json") as handle:
            json.dump(self.receipt, handle, ensure_ascii=False, indent=2)
            handle.write("\n")


def read_prior(args, host: str, cutoff: int, prefix: str | None, receipt: dict[str, Any]):
    if args.after is None:
        if args.prior_receipt:
            raise SessionError("--prior-receipt requires --after")
        return
    receipt["incremental"]["requested"] = True
    if not args.prior_receipt:
        receipt["missing"].append("Incremental range has no prior coverage receipt")
        return
    try:
        prior = json.loads(Path(args.prior_receipt).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SessionError("Cannot read prior coverage receipt") from exc
    if prior.get("host") != host or prior.get("session_id") != args.session_id:
        raise SessionError("Prior receipt belongs to a different host or session")
    if prior.get("range", {}).get("through") != args.after or args.after > cutoff:
        raise SessionError("Prior cutoff does not match --after or the source was truncated")
    expected = prior.get("source", {}).get("prefix_sha256")
    if not prefix or prefix != expected:
        raise SessionError("Earlier source records changed; re-read the affected range instead of appending")
    receipt["incremental"]["verified_prefix"] = True
    receipt["incremental"]["prior_receipt"] = str(Path(args.prior_receipt).resolve())
    if prior.get("status") != "complete":
        receipt["missing"].append("Prior receipt was incomplete; delta cannot repair its missing history")


def extract_codex(args, receipt: dict[str, Any], writer: ChunkWriter):
    home = Path(args.home).expanduser() if args.home else Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    path = Path(args.input).expanduser() if args.input else locate_codex(args.session_id, home, Path(args.db) if args.db else None)
    snapshot = JsonlSnapshot(path)
    # Read metadata before emitting content, and freeze a stable line/byte boundary.
    first_meta = None
    ids = set()
    max_ordinal = 0
    for ordinal, item in snapshot.rows({args.after or 0, args.through or -1}):
        max_ordinal = ordinal
        if item.get("type") == "session_meta":
            metadata = item.get("payload") or {}
            if first_meta is None:
                first_meta = metadata
            if isinstance(metadata, dict) and metadata.get("id"):
                ids.add(metadata["id"])
    first_hash = snapshot.sha256
    stable_bytes = snapshot.cutoff_bytes
    if not isinstance(first_meta, dict) or first_meta.get("id") != args.session_id:
        raise SessionError("The rollout's first session_meta does not match the explicit session ID")
    if ids != {args.session_id}:
        receipt["missing"].append("Multiple session identities or inherited history require lineage verification")
    branch_fields = {key: first_meta[key] for key in ("parent_thread_id", "parent_id", "forked_from_id", "forked_from", "fork_point", "fork_boundary", "fork_session_id", "subagent_history_start_ordinal") if first_meta.get(key) is not None}
    receipt["branch"] = {"observed_session_ids": sorted(ids), "metadata": branch_fields}
    if branch_fields:
        receipt["missing"].append("Fork or parent lineage has not been verified by this adapter")
    cutoff = min(args.through, max_ordinal) if args.through is not None else max_ordinal
    if args.through is not None and args.through > max_ordinal:
        receipt["missing"].append("Requested cutoff exceeds available source lines")
    if snapshot.tail_bytes:
        receipt["missing"].append("Active final JSONL row was incomplete and was not read")
    receipt["errors"].extend(snapshot.errors)
    receipt["source"] = {"kind": "codex_rollout", "locator": str(snapshot.path), "snapshot_bytes": snapshot.bytes,
                         "stable_bytes": stable_bytes, "incomplete_tail_bytes": snapshot.tail_bytes,
                         "snapshot_sha256": first_hash, "prefix_sha256": snapshot.prefixes.get(cutoff)}
    if args.after is not None and args.after > cutoff:
        raise SessionError("--after exceeds the frozen cutoff")
    read_prior(args, "codex", cutoff, snapshot.prefixes.get(args.after or 0), receipt)
    receipt["range"] = {"unit": "one-based JSONL line", "after": args.after or 0, "through": cutoff,
                        "available_through": max_ordinal, "full_source_snapshot": args.through is None}
    for ordinal, item in snapshot.rows({cutoff}):
        if ordinal > cutoff:
            continue
        if args.after is not None and ordinal <= args.after:
            continue
        for record in normalize_codex(item, ordinal, receipt, args.include_tools):
            writer.add(record)
    if snapshot.sha256 != first_hash or snapshot.cutoff_bytes != stable_bytes:
        receipt["errors"].append("Source prefix changed between inventory and extraction")
    receipt["source"]["prefix_sha256"] = snapshot.prefixes.get(cutoff)


def extract_opencode(args, receipt: dict[str, Any], writer: ChunkWriter):
    path = Path(args.db or args.input).expanduser() if (args.db or args.input) else (
        Path(args.home).expanduser() / "opencode.db" if args.home else
        Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share"))) / "opencode/opencode.db")
    with readonly(path) as connection:
        connection.execute("BEGIN")  # Freeze all statements to one read snapshot, including active WAL data.
        if not {"id", "session_id", "type", "seq", "data"} <= columns(connection, "session_message"):
            raise SessionError("Unsupported OpenCode message schema; supply a verified export")
        session_columns = columns(connection, "session_v2")
        if "id" not in session_columns:
            raise SessionError("Unsupported OpenCode session schema; supply a verified export")
        keys = [name for name in ("id", "parent_id", "fork_session_id", "fork_boundary", "revert") if name in session_columns]
        meta = connection.execute("SELECT " + ",".join(keys) + " FROM session_v2 WHERE id = ?", (args.session_id,)).fetchone()
        if meta is None:
            raise SessionError("Explicit session ID was not found")
        receipt["branch"] = dict(meta)
        if any(meta[key] is not None for key in keys if key != "id"):
            receipt["missing"].append("Parent, fork or reverted session requires explicit branch verification")
        bounds = connection.execute("SELECT MIN(seq),MAX(seq),COUNT(*) FROM session_message WHERE session_id = ?", (args.session_id,)).fetchone()
        available = bounds[1]
        if available is None:
            raise SessionError("The selected session has no persisted messages")
        cutoff = min(args.through, available) if args.through is not None else available
        if args.through is not None and args.through > available:
            receipt["missing"].append("Requested cutoff exceeds available sequence")
        if args.after is not None and args.after > cutoff:
            raise SessionError("--after exceeds the frozen cutoff")
        digest = hashlib.sha256()
        prior_hash = hashlib.sha256(b"").hexdigest() if args.after == -1 else None
        prefix_hash = None
        first = None
        last = None
        sequence_gaps = {"count": 0, "examples": []}
        cursor = connection.execute("SELECT id,type,seq,data FROM session_message WHERE session_id = ? AND seq <= ? ORDER BY seq", (args.session_id, cutoff))
        while True:
            batch = cursor.fetchmany(256)
            if not batch:
                break
            for row in batch:
                ordinal = row["seq"]
                if last is not None and ordinal <= last:
                    receipt["missing"].append("Persisted message sequences are not unique and increasing")
                elif last is not None and ordinal > last + 1:
                    sequence_gaps["count"] += 1
                    if len(sequence_gaps["examples"]) < 20:
                        sequence_gaps["examples"].append({"after": last, "before": ordinal})
                first = ordinal if first is None else first
                last = ordinal
                digest.update((dump([row["id"], row["type"], ordinal, row["data"]]) + "\n").encode("utf-8"))
                if ordinal == args.after:
                    prior_hash = digest.hexdigest()
                if args.after is not None and ordinal <= args.after:
                    continue
                try:
                    data = json.loads(row["data"])
                    if not isinstance(data, dict):
                        raise ValueError("not an object")
                except (ValueError, TypeError):
                    receipt["errors"].append("Unreadable data at seq:%d" % ordinal)
                    continue
                for record in normalize_opencode(row["type"], data, ordinal, row["id"], receipt, args.include_tools):
                    writer.add(record)
        prefix_hash = digest.hexdigest()
        # OpenCode projects message creation from a shared durable-event sequence.
        # Other events consume positions without creating session_message rows.
        receipt["warnings"].append("Coverage is the persisted message snapshot; event-sequence gaps do not prove missing messages or exclude deleted history")
        if last != cutoff:
            receipt["missing"].append("Requested cutoff is not an available sequence")
        receipt["source"] = {"kind": "opencode_v2_read_snapshot", "locator": str(path.resolve()),
                             "prefix_sha256": prefix_hash, "persisted_rows": bounds[2],
                             "first_persisted_seq": first, "sequence_gaps": sequence_gaps}
        receipt["range"] = {"unit": "session_message.seq", "after": args.after if args.after is not None else (first - 1 if first is not None else -1),
                            "through": cutoff, "available_through": available,
                            "full_source_snapshot": args.through is None}
        read_prior(args, "opencode", cutoff, prior_hash, receipt)


def extract_export(args, receipt: dict[str, Any], writer: ChunkWriter):
    if not args.input:
        raise SessionError("--host export requires --input")
    path = Path(args.input).expanduser().resolve()
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != "recap-session-export/v1" or value.get("session_id") != args.session_id:
        raise SessionError("Export requires recap-session-export/v1 and the exact session_id")
    messages = value.get("messages")
    coverage = value.get("coverage") or {}
    if not isinstance(messages, list) or not isinstance(coverage, dict):
        raise SessionError("Invalid export messages or coverage")
    if coverage.get("complete") is not True or coverage.get("lineage_complete") is not True:
        receipt["missing"].append("Export does not declare complete original coverage and lineage")
    receipt["warnings"].append("Export coverage is caller-declared; not independently compared with the host")
    receipt["branch"] = value.get("branch", {})
    digest = hashlib.sha256()
    prefix_hash = None
    prior_hash = None
    ordinals: list[int] = []
    available = max((record["ordinal"] for record in messages
                     if isinstance(record, dict) and type(record.get("ordinal")) is int), default=0)
    cutoff = min(args.through, available) if args.through is not None else available
    for message in messages:
        if not isinstance(message, dict) or type(message.get("ordinal")) is not int:
            receipt["missing"].append("Export contains unsupported message records")
            continue
        ordinal = message["ordinal"]
        ordinals.append(ordinal)
        if ordinal > cutoff:
            continue
        digest.update((dump(message) + "\n").encode("utf-8"))
        if ordinal == args.after:
            prior_hash = digest.hexdigest()
        if args.after is not None and ordinal <= args.after:
            continue
        role = message.get("role")
        if message.get("summary") or message.get("original") is False:
            receipt["compaction"]["summary_placeholders"].append(ordinal)
            continue
        if role not in {"user", "assistant", "evidence"}:
            receipt["skipped_noise"]["nonvisible_role"] += 1
            continue
        if role == "evidence" and not args.include_tools:
            receipt["skipped_noise"]["tool_output"] += 1
            continue
        text = message.get("text")
        if not isinstance(text, str):
            receipt["missing"].append("Export record has no original text")
            continue
        if message.get("attachments"):
            attachments = message["attachments"]
            receipt["unread_attachments"].append({"locator": "ordinal:%d" % ordinal,
                                                "count": len(attachments) if isinstance(attachments, list) else 1})
        if role != "evidence":
            receipt["visible_messages"] += 1
        writer.add({"ordinal": ordinal, "role": role, "text": text,
                    "locator": message.get("locator", "ordinal:%d" % ordinal),
                    "message_id": message.get("id"), "timestamp": message.get("timestamp")})
    if ordinals != list(range(1, available + 1)):
        receipt["missing"].append("Export ordinals are not an ordered full prefix beginning at 1")
    if coverage.get("through") != available or coverage.get("start") != 1:
        receipt["missing"].append("Export coverage bounds do not match its original message records")
    if args.through is not None and args.through > available:
        receipt["missing"].append("Requested cutoff exceeds export coverage")
    prefix_hash = digest.hexdigest()
    receipt["source"] = {"kind": "declared_export", "locator": str(path), "prefix_sha256": prefix_hash,
                         "declared_host": value.get("host"), "declaration": coverage}
    receipt["range"] = {"unit": "export.ordinal", "after": args.after or 0, "through": cutoff,
                        "available_through": available, "full_source_snapshot": args.through is None}
    read_prior(args, "export", cutoff, prior_hash, receipt)


def extract(args) -> dict[str, Any]:
    if not args.session_id.strip() or args.chunk_chars < 100:
        raise SessionError("Use a nonempty exact session ID and --chunk-chars >= 100")
    if args.after is not None and args.after < -1:
        raise SessionError("--after must be >= -1")
    if args.through is not None and args.through < 0:
        raise SessionError("--through must be >= 0")
    output_lexical = Path(os.path.abspath(Path(args.output).expanduser()))
    knowledge_lexical = Path(os.path.abspath(Path(args.knowledge_root or os.environ.get(
        "RECAP_KNOWLEDGE_ROOT", str(Path.home() / ".agents/knowledge"))).expanduser()))
    output = output_lexical.resolve()
    knowledge = knowledge_lexical.resolve()
    lexical_base = next((base for base in (knowledge_lexical, knowledge)
                         if output_lexical == base or base in output_lexical.parents), None)
    if lexical_base is not None:
        current = lexical_base
        for component in output_lexical.relative_to(lexical_base).parts:
            current = current / component
            if current.is_symlink():
                raise SessionError("Temporary extraction paths inside the knowledge root may not cross symlinks")
    if lexical_base is not None or output == knowledge or knowledge in output.parents:
        temporary = knowledge / ".state/tmp"
        if temporary not in output.parents:
            raise SessionError("Inside the knowledge root, original-text extraction is allowed only in .state/tmp/<new-operation>")
    receipt = base_receipt(args.host, args.session_id)
    writer = ChunkWriter(output, args.chunk_chars, receipt)
    try:
        {"codex": extract_codex, "opencode": extract_opencode, "export": extract_export}[args.host](args, receipt, writer)
        if receipt["compaction"]["markers"] and receipt["visible_messages"] == 0:
            receipt["missing"].append("Compaction is present without original visible messages in the selected range")
        if receipt["compaction"]["summary_placeholders"]:
            receipt["missing"].append("Summary placeholders are not recovered original messages")
        if receipt["event_message_count"] and receipt["visible_messages"] == 0:
            receipt["missing"].append("Only event-message mirrors are available; original response items were not extracted")
        if not receipt["visible_messages"] and not receipt["incremental"]["verified_prefix"]:
            receipt["missing"].append("No original visible messages were extracted")
        if args.through is not None:
            receipt["warnings"].append("Caller selected an explicit historical cutoff; later source rows were intentionally excluded")
        if not receipt["missing"] and not receipt["unread_attachments"] and not receipt["unknown_envelopes"] and not receipt["errors"]:
            receipt["status"] = "complete"
    except (SessionError, OSError, ValueError, sqlite3.Error) as exc:
        receipt["errors"].append(str(exc))
        receipt["status"] = "error"
    finally:
        writer.close()
        writer.write_receipt()
    return receipt


def show_chunk(path: Path, ordinal: int | None = None) -> str:
    """Render one selected extraction chunk; inserted wraps are display-only."""
    lines = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            record = json.loads(raw)
        except ValueError as exc:
            raise SessionError(f"Invalid chunk JSON at line {number}") from exc
        if (not isinstance(record, dict) or record.get("role") not in ("user", "assistant", "evidence")
                or not isinstance(record.get("text"), str) or not isinstance(record.get("locator"), str)
                or not record["locator"] or type(record.get("ordinal")) is not int
                or type(record.get("text_offset")) is not int or type(record.get("text_length")) is not int
                or not 0 <= record["text_offset"] <= record["text_length"] - len(record["text"])):
            raise SessionError(f"Invalid chunk record at line {number}")
        if ordinal is not None and record["ordinal"] != ordinal:
            continue
        lines.append(f'--- {record["role"]} | locator={dump(record["locator"])} | ordinal={record["ordinal"]}'
                     f' | offset={record["text_offset"]}/{record["text_length"]} ---')
        for line in record["text"].split("\n"):
            if line:
                lines.extend(line[start:start + 160] for start in range(0, len(line), 160))
            else:
                lines.append("")
        lines.append("")
    if not lines:
        raise SessionError("No chunk fragments match the selected ordinal" if ordinal is not None else "Chunk is empty")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("extract", help="Read an exact source snapshot into a new temporary directory")
    command.add_argument("--host", required=True, choices=("codex", "opencode", "export"))
    command.add_argument("--session-id", required=True, help="Explicit target user session; never inferred from this process")
    command.add_argument("--output", required=True, help="New temporary directory outside the knowledge root or strictly below its .state/tmp/")
    command.add_argument("--input", help="Exact Codex rollout JSONL, OpenCode DB, or declared JSON export")
    command.add_argument("--db", help="Exact Codex index or OpenCode source database")
    command.add_argument("--home", help="Codex data directory or OpenCode data directory containing opencode.db")
    command.add_argument("--after", type=int, help="Exclusive prior line/sequence cutoff, with --prior-receipt for a verified delta")
    command.add_argument("--through", type=int, help="Inclusive fixed source line/sequence cutoff")
    command.add_argument("--chunk-chars", type=int, default=24000, help="Maximum text characters per chunk, default 24000; JSON framing is additional")
    command.add_argument("--prior-receipt", help="Previous receipt used to verify unchanged prefix before a delta")
    command.add_argument("--include-tools", action="store_true", help="Include original tool-output evidence; examine it only when relevant")
    command.add_argument("--knowledge-root", help="Knowledge root whose only raw-text temporary area is .state/tmp/<new-operation>")
    command = sub.add_parser("show", help="Display one extracted JSONL chunk as wrapped text with original locators")
    command.add_argument("chunk", help="Exact extracted chunk file; display does not establish source coverage")
    command.add_argument("--ordinal", type=int, help="Show only this original ordinal within the selected chunk")
    args = parser.parse_args()
    try:
        if args.command == "show":
            print(show_chunk(Path(args.chunk).expanduser(), args.ordinal), end="")
            return 0
        receipt = extract(args)
    except (SessionError, OSError, UnicodeError) as exc:
        print(dump({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2
    print(dump({"status": receipt["status"], "receipt": str(Path(args.output).resolve() / "receipt.json"),
                "chunks": len(receipt["chunks"]), "visible_messages": receipt["visible_messages"],
                "characters_emitted": receipt["characters_emitted"], "missing_count": len(receipt["missing"]),
                "errors": receipt["errors"]}))
    return 2 if receipt["status"] == "error" else 0


if __name__ == "__main__":
    raise SystemExit(main())
