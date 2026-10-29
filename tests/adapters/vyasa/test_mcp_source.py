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


def get_answer(requested):
    if scenario == "get_unsupported":
        payload = envelope([], {"limit": 100, "next_cursor": None, "has_more": False}, version="2")
        return {"isError": False, "content": [{"type": "text", "text": json.dumps(payload)}], "structuredContent": payload}
    if scenario == "get_error":
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": json.dumps({"error": {"code": "internal_error", "message": "no index"}})}
            ],
        }
    if scenario == "get_other":
        detail = {
            "project_id": "zzz",
            "aliases": [],
            "checkouts": [],
            "languages": [],
            "markers": [],
            "frameworks": [],
        }
        payload = {
            "schema_version": "1",
            "data": detail,
            "meta": {"generated_at": "2026-10-29T12:00:00Z", "index_version": "11", "freshness": "current"},
        }
        return {"isError": False, "content": [{"type": "text", "text": json.dumps(payload)}], "structuredContent": payload}
    detail = {
        "project_id": requested,
        "aliases": ["siddhi"],
        "checkouts": [
            {"remote": "https://github.com/owner/repo", "status": "clean", "observed_at": "2026-10-29T12:00:00Z"}
        ],
        "languages": ["Python"],
        "markers": ["implementation:complete"],
        "frameworks": ["fastapi"],
    }
    payload = {
        "schema_version": "1",
        "data": detail,
        "meta": {"generated_at": "2026-10-29T12:00:00Z", "index_version": "11", "freshness": "current"},
    }
    return {"isError": False, "content": [{"type": "text", "text": json.dumps(payload)}], "structuredContent": payload}


def answer(message):
    arguments = message["params"]["arguments"]
    if "project_id" in arguments:
        return get_answer(arguments["project_id"])
    if scenario in ("tool_error", "tool_unavailable"):
        code = "unavailable" if scenario == "tool_unavailable" else "internal_error"
        return {
            "isError": True,
            "content": [
                {"type": "text", "text": json.dumps({"error": {"code": code, "message": "no index"}})}
            ],
        }
    if scenario == "unsupported":
        payload = envelope([], {"limit": 100, "next_cursor": None, "has_more": False}, version="2")
    elif scenario == "no_has_more":
        payload = envelope([], {"limit": 100, "next_cursor": None})
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
    if scenario == "numeric_version":
        payload["meta"]["index_version"] = 11
        result["content"][0]["text"] = json.dumps(payload)
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
            if scenario == "silent_init":
                continue
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
            if scenario == "oversized":
                sys.stdout.write("x" * 1050000 + "\\n")
                sys.stdout.flush()
            elif scenario != "silent":
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


def test_a_numeric_index_version_is_kept_as_text(command):
    inventory = VyasaMcpSource(command("numeric_version")).fetch_inventory()

    assert inventory.index_version == "11"


def test_the_process_is_closed_after_a_read(command, tmp_path):
    marker = tmp_path / "closed.txt"

    VyasaMcpSource(command("empty", str(marker))).fetch_inventory()

    assert marker.read_text(encoding="utf-8") == "closed"


def test_a_failed_handshake_closes_the_process(command, tmp_path):
    marker = tmp_path / "closed.txt"

    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("silent_init", str(marker)), timeout=0.2).fetch_inventory()

    assert failed.value.category == "timeout"
    assert marker.read_text(encoding="utf-8") == "closed"


def test_a_page_without_a_page_state_is_unsupported(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("no_has_more")).fetch_inventory()

    assert failed.value.category == "unsupported_contract"


def test_a_tool_level_unavailable_is_an_outage(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("tool_unavailable")).fetch_inventory()

    assert failed.value.category == "unavailable"


def test_an_oversized_message_is_refused_without_buffering_it(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("oversized")).fetch_inventory()

    assert failed.value.category == "protocol_error"


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


def test_a_get_project_returns_the_detail(command):
    detail = VyasaMcpSource(command("get_ok")).get_project("a")

    assert detail["project_id"] == "a"
    assert detail["aliases"] == ["siddhi"]
    assert detail["checkouts"][0]["status"] == "clean"


def test_a_get_project_with_an_unsupported_version_fails(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("get_unsupported")).get_project("a")

    assert failed.value.category == "unsupported_contract"


def test_a_get_project_propagating_a_tool_error_maps_a_category(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("get_error")).get_project("a")

    assert failed.value.category == "tool_error"


def test_a_get_project_for_a_different_identifier_fails(command):
    with pytest.raises(SourceError) as failed:
        VyasaMcpSource(command("get_other")).get_project("a")

    assert failed.value.category == "protocol_error"
