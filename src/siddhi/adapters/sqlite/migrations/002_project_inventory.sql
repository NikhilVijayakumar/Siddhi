-- Project inventory: one row per refresh attempt and one projection row per project.
CREATE TABLE ingestion_runs (
    id             TEXT    PRIMARY KEY,
    source         TEXT    NOT NULL CHECK (source = 'vyasa'),
    started_at     TEXT    NOT NULL,
    finished_at    TEXT    NOT NULL,
    outcome        TEXT    NOT NULL CHECK (outcome IN ('completed', 'failed')),
    failure        TEXT,
    index_version  TEXT,
    freshness      TEXT,
    projects_total INTEGER NOT NULL DEFAULT 0 CHECK (projects_total >= 0),
    added          INTEGER NOT NULL DEFAULT 0 CHECK (added >= 0),
    updated        INTEGER NOT NULL DEFAULT 0 CHECK (updated >= 0),
    removed        INTEGER NOT NULL DEFAULT 0 CHECK (removed >= 0),
    unchanged      INTEGER NOT NULL DEFAULT 0 CHECK (unchanged >= 0),
    CHECK ((outcome = 'completed' AND failure IS NULL)
        OR (outcome = 'failed' AND failure IS NOT NULL))
);

CREATE TABLE projects (
    project_id        TEXT PRIMARY KEY,
    display_name      TEXT NOT NULL,
    state             TEXT NOT NULL CHECK (state IN ('active', 'missing', 'inaccessible')),
    identity_status   TEXT NOT NULL,
    providers         TEXT NOT NULL,
    languages         TEXT NOT NULL,
    first_observed_at TEXT NOT NULL,
    last_observed_at  TEXT NOT NULL,
    last_run_id       TEXT NOT NULL REFERENCES ingestion_runs(id)
);

CREATE INDEX projects_by_name ON projects (display_name, project_id);
