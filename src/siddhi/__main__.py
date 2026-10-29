"""Start Siddhi locally: `python -m siddhi`."""

import sys

from siddhi.adapters.sqlite.runner import MigrationFailed, SchemaTooNew
from siddhi.bootstrap.app import serve
from siddhi.bootstrap.config import ConfigError, load_settings


def main() -> int:
    """Exit non-zero with the reason when startup cannot proceed."""
    try:
        serve(load_settings())
    except (ConfigError, MigrationFailed, SchemaTooNew) as error:
        print(f"siddhi: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
