"""Vyasa MCP adapter: contract validation and bounded paging over a scripted process."""

import sys

import pytest

from siddhi.adapters.vyasa.mcp_source import VyasaMcpSource
from siddhi.domain.project import SourceError

SERVER_SCRIPT = '''\
import json
import sys

scenario = sys.argv[1]
marker = sys.argv[2] if len(sys.argv) > 2 else None


def send(message):
    sys.stdout.write(json.dumps(message) + "\\n")
    sys.stdout.flush()


def project(project_id, name):
    return {
        "project_id": project_id,
        "display_name": name,
        "state": "active",
        "identity_status": "resolved",
        "providers": ["github"],
        "languages": ["Python"],
    }


def envelope(projects, page, version="1"):
    return {
        "schema_version": version,
        "data": {"projects": projects, "page": page},
        "meta": {
            "generated_at": "2026-10-29T12:00:00Z",
            "index_version": "11",
            "freshness": "current",
        },
    }


def answer(message):
    arguments = message["params"]["arguments"]
    if scenario == "tool_error":
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": json.dumps({"error": {"code": "unavailable", "message": "no index"}})}
            ],
        }
    if scenario == "unsupported":
        payload = envelope([], {"limit": 100, "next_cursor": None, "has_more": False}, version="2")
    elif scenario == "repeat_cursor":
        payload = envelope(
            [project("a", "Alpha")], {"limit": 100, "next_cursor": "same", "has_more": True}
        )
    elif scenario == "missing_field":
        broken = {"project_id": "a", "state": "active", "identity_status": "resolved"}
        payload = envelope([broken], {"limit": 100, "next_cursor": None, "has_more": False})
    elif scenario in ("two_pages", "text_only") and "cursor" not in arguments:
        payload = envelope(
            [project("a", "Alpha")], {"limit": 100, "next_cursor": "next", "has_more": True}
        )
    elif scenario in ("two_pages", "text_only"):
        payload = envelope([project("b", "Beta")], {"limit": 100, "next_cursor": None, "has_more": False})
    else:
        payload = envelope([], {"limit": 100, "next_cursor": None, "has_more": False})
    result = {"isError": False, "content": [{"type": "text", "text": json.dumps(payload)}]}
    if scenario != "text_only":
        result["structuredContent"] = payload
    return result


try:
    for line in sys.stdin:
        message = json.loads(line)
        if "id" not in message:
            continue
        method = message.get("method")
        if method == "initialize":
            send(
                {
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "result": {
                        "protocolVersion": "2025-06-18",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "fake-vyasa", "version": "1"},
                    },
                }
            )
        elif method == "tools/call":
            if scenario != "silent":
                send({"jsonrpc": "2.0", "id": message["id"], "result": answer(message)})
        else:
            send(
                {
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "error": {"code": -32601, "message": "unknown method"},
                }
            )
finally:
    if marker:
        with open(marker, "w", encoding="utf-8") as handle:
            handle.write("closed")
'''


@pytest.fixture
def command(tmp_path):
    script = tmp_path / "fake_vyasa.py"
    script.write_text(SERVER_SCRIPT, encoding="utf-8")

    def build(*arguments):
        return [sys.executable, "-u", str(script), *arguments]

    return build


def test_two_pages_become_one_inventory(command):
    inventory = VyasaMcpSource(command("two_pages")).fetch_inventory()

    assert [project.project_id for project in inventory.projects] == ["a", "b"]
    assert [project.display_name for project in inventory.projects] == ["Alpha", "Beta"]
    assert (inventory.index_version, inventory.freshness) == ("11", "current")


def test_a_text_only_answer_is_parsed(command):
    inventory = VyasaMcpSource(command("text_only")).fetch_inventory()

    assert [project.project_id for project in inventory.projects] == ["a", "b"]


def test_an_empty_answer_is_a_valid_empty_inventory(command):
    inventory = VyasaMcpSource(command("empty")).fetch_inventory()

    assert inventory.projects == []


def test_the_process_is_closed_after_a_read(command, tmp_path):
    marker = tmp_path / "closed.txt"

    VyasaMcpSource(command("empty", str(marker))).fetch_inventory()

    assert marker.read_text(encoding="utf-8") == "closed"


def test_a_tool_error_stays_a_category_without_the_source_message(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("tool_error")).fetch_inventory()

    assert failed.value.category == "tool_error"
    assert "no index" not in str(failed.value)


def test_an_unsupported_schema_version_fails(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("unsupported")).fetch_inventory()

    assert failed.value.category == "unsupported_contract"


def test_a_project_missing_a_required_field_fails(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("missing_field")).fetch_inventory()

    assert failed.value.category == "unsupported_contract"


def test_a_repeated_cursor_fails_instead_of_looping(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("repeat_cursor")).fetch_inventory()

    assert failed.value.category == "protocol_error"


def test_a_silent_source_times_out(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("silent"), timeout=0.2).fetch_inventory()

    assert failed.value.category == "timeout"


def test_an_executable_that_cannot_start_is_a_connection_failure(tmp_path):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource([str(tmp_path / "absent-vyasa.exe")]).fetch_inventory()

    assert failed.value.category == "connection_failed"
