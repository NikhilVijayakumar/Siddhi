"""Launch configuration: defaults, a machine-local file, then environment wins."""

import ipaddress
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

ENV_PREFIX = "SIDDHI_"
DEFAULT_DIRECTORY = Path.home() / ".siddhi"
DEFAULT_DATABASE_FILE = DEFAULT_DIRECTORY / "siddhi.db"
DEFAULT_SETTINGS_FILE = DEFAULT_DIRECTORY / "settings.json"
DEFAULT_BIND_HOST = "127.0.0.1"
DEFAULT_BIND_PORT = 8000
DEFAULT_LOG_LEVEL = "INFO"
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class ConfigError(Exception):
    """A configured value is unusable. Names the setting, never the submitted value."""

    def __init__(self, setting: str, message: str) -> None:
        super().__init__(f"{setting}: {message}")
        self.setting = setting


@dataclass(frozen=True)
class Settings:
    database_path: Path
    bind_host: str = DEFAULT_BIND_HOST
    bind_port: int = DEFAULT_BIND_PORT
    log_level: str = DEFAULT_LOG_LEVEL
    vyasa_mcp_command: str | None = None


def load_settings(
    environ: Mapping[str, str] | None = None, settings_file: Path | None = None
) -> Settings:
    """Resolve every setting, refusing anything unsafe before a socket is opened."""
    env = os.environ if environ is None else environ
    path = settings_file or Path(env.get(f"{ENV_PREFIX}SETTINGS_FILE", DEFAULT_SETTINGS_FILE))
    from_file = _read_settings_file(path)

    def resolve(name: str, default: object) -> object:
        env_key = f"{ENV_PREFIX}{name.upper()}"
        if env_key in env:
            return env[env_key]
        return from_file.get(name, default)

    bind_host = str(resolve("bind_host", DEFAULT_BIND_HOST))
    if not _is_loopback(bind_host):
        # Loopback only: this service has no authentication and no transport security.
        raise ConfigError(
            f"{ENV_PREFIX}BIND_HOST", "must be a loopback address (127.0.0.1 or localhost)"
        )

    log_level = str(resolve("log_level", DEFAULT_LOG_LEVEL)).upper()
    if log_level not in LOG_LEVELS:
        raise ConfigError(f"{ENV_PREFIX}LOG_LEVEL", f"must be one of {', '.join(LOG_LEVELS)}")

    return Settings(
        database_path=Path(
            str(resolve("database_path", str(DEFAULT_DATABASE_FILE)))
        ).expanduser(),
        bind_host=bind_host,
        bind_port=_port(resolve("bind_port", DEFAULT_BIND_PORT)),
        log_level=log_level,
        vyasa_mcp_command=_command(resolve("vyasa_mcp_command", None)),
    )


def _is_loopback(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _command(value: object) -> str | None:
    """A path kept verbatim; unset turns the integration off, blank is a mistake."""
    if value is None:
        return None
    command = str(value).strip()
    if not command:
        raise ConfigError(
            f"{ENV_PREFIX}VYASA_MCP_COMMAND", "must be an executable path or unset"
        )
    return command


def _port(value: object) -> int:
    try:
        port = int(str(value), 10)
    except ValueError:
        port = 0
    if not 1 <= port <= 65535:
        raise ConfigError(f"{ENV_PREFIX}BIND_PORT", "must be a whole number from 1 to 65535")
    return port


def _read_settings_file(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    try:
        values = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ConfigError(f"{ENV_PREFIX}SETTINGS_FILE", "must be readable JSON") from None
    if not isinstance(values, dict):
        raise ConfigError(f"{ENV_PREFIX}SETTINGS_FILE", "must be a JSON object")
    return values
