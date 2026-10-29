"""serve() and `python -m siddhi`: nothing starts until the configuration is accepted."""

import siddhi.__main__ as entrypoint
from siddhi.adapters.sqlite.runner import MigrationFailed
from siddhi.adapters.vyasa.mcp_source import VyasaMcpSource
from siddhi.bootstrap.app import serve
from siddhi.bootstrap.config import Settings


def test_serve_uses_the_validated_address(tmp_path):
    calls = []
    settings = Settings(database_path=tmp_path / "siddhi.db", bind_port=8123)

    serve(settings, run=lambda app, **options: calls.append(options))

    assert calls == [{"host": "127.0.0.1", "port": 8123}]
    assert settings.database_path.exists()


def test_serve_configures_the_vyasa_source_only_when_given(tmp_path):
    apps = []
    configured = Settings(
        database_path=tmp_path / "configured.db",
        vyasa_mcp_command=str(tmp_path / "tools" / "vyasa-mcp.exe"),
    )
    unconfigured = Settings(database_path=tmp_path / "plain.db")

    serve(configured, run=lambda app, **options: apps.append(app))
    serve(unconfigured, run=lambda app, **options: apps.append(app))

    assert isinstance(apps[0].state.project_source, VyasaMcpSource)
    assert apps[1].state.project_source is None


def test_main_runs_the_service(tmp_path, monkeypatch):
    started = []
    monkeypatch.setattr(entrypoint, "serve", started.append)
    monkeypatch.setenv("SIDDHI_SETTINGS_FILE", str(tmp_path / "absent.json"))

    assert entrypoint.main() == 0
    assert started[0].bind_host == "127.0.0.1"


def test_main_refuses_a_non_loopback_bind_before_starting(tmp_path, monkeypatch, capsys):
    started = []
    monkeypatch.setattr(entrypoint, "serve", started.append)
    monkeypatch.setenv("SIDDHI_SETTINGS_FILE", str(tmp_path / "absent.json"))
    monkeypatch.setenv("SIDDHI_BIND_HOST", "0.0.0.0")

    assert entrypoint.main() == 1
    assert started == []
    assert "SIDDHI_BIND_HOST" in capsys.readouterr().err


def test_main_reports_a_failed_migration(tmp_path, monkeypatch, capsys):
    def fail(settings):
        raise MigrationFailed("cannot apply 002")

    monkeypatch.setattr(entrypoint, "serve", fail)
    monkeypatch.setenv("SIDDHI_SETTINGS_FILE", str(tmp_path / "absent.json"))

    assert entrypoint.main() == 1
    assert "cannot apply 002" in capsys.readouterr().err
