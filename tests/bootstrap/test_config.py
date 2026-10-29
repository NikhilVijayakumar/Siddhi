"""Launch configuration: defaults, a machine-local file, then environment wins."""

import json

import pytest

from siddhi.bootstrap.config import ConfigError, load_settings


def settings_file(tmp_path, values):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps(values), encoding="utf-8")
    return path


def test_defaults_bind_loopback_only(tmp_path):
    settings = load_settings(environ={}, settings_file=tmp_path / "absent.json")

    assert settings.bind_host == "127.0.0.1"
    assert settings.bind_port == 8000
    assert settings.log_level == "INFO"
    assert settings.database_path.name.endswith(".db")


def test_environment_overrides_the_settings_file(tmp_path):
    path = settings_file(
        tmp_path, {"bind_port": 8100, "log_level": "warning", "database_path": "from-file.db"}
    )

    settings = load_settings(
        environ={"SIDDHI_BIND_PORT": "9100", "SIDDHI_LOG_LEVEL": "debug"},
        settings_file=path,
    )

    assert settings.bind_port == 9100
    assert settings.log_level == "DEBUG"
    assert settings.database_path.name == "from-file.db"


def test_settings_file_supplies_values_without_environment(tmp_path):
    path = settings_file(tmp_path, {"bind_port": 8100, "database_path": "local.db"})

    settings = load_settings(environ={}, settings_file=path)

    assert settings.bind_port == 8100
    assert settings.database_path.name == "local.db"


@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.1.20", "::"])
def test_non_loopback_bind_is_refused_without_naming_the_value(tmp_path, host):
    with pytest.raises(ConfigError) as refused:
        load_settings(environ={"SIDDHI_BIND_HOST": host}, settings_file=tmp_path / "absent.json")

    assert refused.value.setting == "SIDDHI_BIND_HOST"
    assert host not in str(refused.value)
    assert "127.0.0.1" in str(refused.value)


@pytest.mark.parametrize("host", ["127.0.0.1", "::1", "localhost"])
def test_loopback_bind_is_accepted(tmp_path, host):
    settings = load_settings(
        environ={"SIDDHI_BIND_HOST": host}, settings_file=tmp_path / "absent.json"
    )

    assert settings.bind_host == host


@pytest.mark.parametrize(
    "environ,setting",
    [
        ({"SIDDHI_BIND_PORT": "0"}, "SIDDHI_BIND_PORT"),
        ({"SIDDHI_BIND_PORT": "http"}, "SIDDHI_BIND_PORT"),
        ({"SIDDHI_LOG_LEVEL": "verbose"}, "SIDDHI_LOG_LEVEL"),
    ],
)
def test_unusable_values_name_the_setting(tmp_path, environ, setting):
    with pytest.raises(ConfigError) as refused:
        load_settings(environ=environ, settings_file=tmp_path / "absent.json")

    assert refused.value.setting == setting


def test_vyasa_command_is_optional_and_blank_is_refused(tmp_path):
    command = str(tmp_path / "tools" / "vyasa-mcp.exe")
    unset = load_settings(environ={}, settings_file=tmp_path / "absent.json")
    assert unset.vyasa_mcp_command is None

    configured = load_settings(
        environ={"SIDDHI_VYASA_MCP_COMMAND": command},
        settings_file=tmp_path / "absent.json",
    )
    assert configured.vyasa_mcp_command == command

    with pytest.raises(ConfigError) as refused:
        load_settings(
            environ={"SIDDHI_VYASA_MCP_COMMAND": "   "},
            settings_file=tmp_path / "absent.json",
        )
    assert refused.value.setting == "SIDDHI_VYASA_MCP_COMMAND"


def test_a_malformed_settings_file_is_reported_by_setting(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(ConfigError) as refused:
        load_settings(environ={}, settings_file=path)

    assert refused.value.setting == "SIDDHI_SETTINGS_FILE"
