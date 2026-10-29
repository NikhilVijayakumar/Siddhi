"""Vyasa inventory over its local MCP stdio server.

shortcut: a hand-written newline-delimited JSON-RPC client for one read-only tool;
switch to the official MCP client if more tools or server-initiated requests appear.
"""

from __future__ import annotations

import json
import queue
import subprocess
import threading
import time
from collections.abc import Sequence

from siddhi.domain.project import Inventory, ProjectRecord, SourceError

PROTOCOL_VERSION = "2025-06-18"
SUPPORTED_SCHEMA = "1"
PAGE_LIMIT = 100
MAX_PAGES = 100
MAX_PROJECTS = 10_000
MAX_MESSAGE_BYTES = 1_000_000
CLIENT_INFO = {"name": "siddhi", "version": "0.1.0"}


class VyasaMcpSource:
    """Fetches one complete inventory, or fails with a category and no data."""

    def __init__(self, command: Sequence[str], timeout: float = 60.0) -> None:
        if not command:
            raise ValueError("a Vyasa command is required")
        self._command = list(command)
        self._timeout = timeout

    def fetch_inventory(self) -> Inventory:
        with _Session(self._command, self._timeout) as session:
            projects: list[ProjectRecord] = []
            seen_cursors: set[str | None] = {None}
            cursor: str | None = None
            index_version: str | None = None
            freshness: str | None = None
            for _ in range(MAX_PAGES):
                arguments: dict[str, object] = {"limit": PAGE_LIMIT}
                if cursor is not None:
                    arguments["cursor"] = cursor
                data, meta = session.call_tool("search_projects", arguments)
                index_version = _optional_text(meta, "index_version", index_version)
                freshness = _optional_text(meta, "freshness", freshness)
                projects.extend(_projects(data))
                if len(projects) > MAX_PROJECTS:
                    raise SourceError("unsupported_contract", "the source returned too many projects")
                page = data.get("page")
                if not isinstance(page, dict):
                    raise SourceError("unsupported_contract", "the source answer has no page")
                has_more = page.get("has_more")
                if has_more is False:
                    return Inventory(
                        projects=projects,
                        index_version=index_version,
                        freshness=freshness,
                    )
                if has_more is not True:
                    raise SourceError(
                        "unsupported_contract", "the source answer has no page state"
                    )
                cursor = page.get("next_cursor")
                if not isinstance(cursor, str) or not cursor or cursor in seen_cursors:
                    raise SourceError("protocol_error", "the source cursor did not advance")
                seen_cursors.add(cursor)
        raise SourceError("protocol_error", "the source exceeded the page bound")


class _Session:
    """One child process, one handshake, then request/response pairs."""

    def __init__(self, command: list[str], timeout: float) -> None:
        self._command = command
        self._timeout = timeout
        self._process: subprocess.Popen[str] | None = None
        self._messages: queue.Queue[object] = queue.Queue()
        self._next_id = 0

    def __enter__(self) -> "_Session":
        try:
            self._process = subprocess.Popen(
                self._command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                bufsize=1,
            )
        except OSError:
            raise SourceError("connection_failed", "the source process could not start") from None
        try:
            threading.Thread(target=self._read_stdout, daemon=True).start()
            result = self._request(
                "initialize",
                {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": CLIENT_INFO,
                },
            )
        except BaseException:
            self._close()
            raise
        if not isinstance(result, dict) or not isinstance(result.get("protocolVersion"), str):
            self._close()
            raise SourceError("protocol_error", "the source did not complete the handshake")
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return self

    def __exit__(self, *exc_info: object) -> None:
        self._close()

    def call_tool(self, name: str, arguments: dict[str, object]) -> tuple[dict, dict]:
        result = self._request("tools/call", {"name": name, "arguments": arguments})
        if not isinstance(result, dict):
            raise SourceError("protocol_error", "the tool result is not an object")
        if result.get("isError"):
            raise SourceError(_error_category(result), f"the {name} tool reported an error")
        payload = result.get("structuredContent")
        if not isinstance(payload, dict):
            payload = _text_payload(result)
        if payload.get("schema_version") != SUPPORTED_SCHEMA:
            raise SourceError(
                "unsupported_contract", f"the {name} answer uses an unsupported contract"
            )
        data = payload.get("data")
        if not isinstance(data, dict):
            raise SourceError("unsupported_contract", f"the {name} answer has no data")
        meta = payload.get("meta")
        return data, meta if isinstance(meta, dict) else {}

    def _request(self, method: str, params: dict) -> object:
        self._next_id += 1
        request_id = self._next_id
        self._send(
            {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
        )
        deadline = time.monotonic() + self._timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SourceError("timeout", f"the {method} call timed out")
            try:
                message = self._messages.get(timeout=remaining)
            except queue.Empty:
                raise SourceError("timeout", f"the {method} call timed out") from None
            if message is None:
                category = "connection_failed" if self._exited() else "protocol_error"
                raise SourceError(category, "the source process ended")
            if message is _MALFORMED:
                raise SourceError("protocol_error", "the source sent unreadable output")
            if not isinstance(message, dict) or message.get("id") != request_id:
                continue
            if "error" in message:
                raise SourceError("protocol_error", f"the {method} call failed")
            return message.get("result")

    def _send(self, message: dict) -> None:
        process = self._process
        if process is None or process.stdin is None:
            raise SourceError("connection_failed", "the source process is not running")
        try:
            process.stdin.write(json.dumps(message) + "\n")
            process.stdin.flush()
        except (OSError, ValueError):
            raise SourceError("connection_failed", "the source process is not running") from None

    def _read_stdout(self) -> None:
        process = self._process
        if process is None or process.stdout is None:
            self._messages.put(None)
            return
        while True:
            line = process.stdout.readline(MAX_MESSAGE_BYTES)
            if not line:
                self._messages.put(None)
                return
            if len(line) >= MAX_MESSAGE_BYTES and not line.endswith("\n"):
                self._messages.put(_MALFORMED)
                return
            line = line.strip()
            if not line:
                continue
            try:
                self._messages.put(json.loads(line))
            except Exception:
                # Any unparseable line ends the read; the caller fails fast instead of hanging.
                self._messages.put(_MALFORMED)
                return

    def _exited(self) -> bool:
        return self._process is not None and self._process.poll() is not None

    def _close(self) -> None:
        process = self._process
        if process is None:
            return
        try:
            if process.stdin is not None:
                process.stdin.close()
        except OSError:
            pass
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass


_MALFORMED = object()


def _error_category(result: dict) -> str:
    """A tool-level `unavailable` is a source outage, not a contract problem."""
    payload = result.get("structuredContent")
    if not isinstance(payload, dict):
        content = result.get("content")
        first = content[0] if isinstance(content, list) and content else None
        text = first.get("text") if isinstance(first, dict) else None
        try:
            payload = json.loads(text) if isinstance(text, str) else None
        except ValueError:
            payload = None
    error = payload.get("error") if isinstance(payload, dict) else None
    code = error.get("code") if isinstance(error, dict) else None
    return "unavailable" if code == "unavailable" else "tool_error"


def _text_payload(result: dict) -> dict:
    content = result.get("content")
    if not isinstance(content, list) or not content:
        raise SourceError("protocol_error", "the tool result carries no content")
    first = content[0]
    if not isinstance(first, dict) or not isinstance(first.get("text"), str):
        raise SourceError("protocol_error", "the tool result carries no text")
    try:
        payload = json.loads(first["text"])
    except ValueError:
        raise SourceError("protocol_error", "the tool result text is not JSON") from None
    if not isinstance(payload, dict):
        raise SourceError("protocol_error", "the tool result is not an object")
    return payload


def _projects(data: dict) -> list[ProjectRecord]:
    raw = data.get("projects")
    if not isinstance(raw, list):
        raise SourceError("unsupported_contract", "the source answer has no project list")
    records = []
    for item in raw:
        if not isinstance(item, dict):
            raise SourceError("unsupported_contract", "a project is not an object")
        records.append(
            ProjectRecord(
                project_id=_required_text(item, "project_id"),
                display_name=_required_text(item, "display_name"),
                state=_required_text(item, "state"),
                identity_status=_required_text(item, "identity_status"),
                providers=_labels(item, "providers"),
                languages=_labels(item, "languages"),
            )
        )
    return records


def _required_text(item: dict, key: str) -> str:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SourceError("unsupported_contract", f"a project has no {key}")
    return value


def _labels(item: dict, key: str) -> tuple[str, ...]:
    value = item.get(key, [])
    if not isinstance(value, list) or not all(isinstance(label, str) for label in value):
        raise SourceError("unsupported_contract", f"a project has unusable {key}")
    return tuple(value)


def _optional_text(meta: dict, key: str, fallback: str | None) -> str | None:
    """Keep a usable source scalar as text; otherwise keep the fallback."""
    value = meta.get(key, fallback)
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        return fallback
    return str(value)
