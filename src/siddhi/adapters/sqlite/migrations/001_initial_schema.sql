-- Schema version 1: goals and their append-only revisions.
-- api-contract.md section 5. Ledger rows are written by the runner, not here.

CREATE TABLE schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT    NOT NULL
);

CREATE TABLE goals (
    id              TEXT    PRIMARY KEY,
    title           TEXT    NOT NULL CHECK (length(trim(title)) BETWEEN 1 AND 200),
    outcome_type    TEXT    NOT NULL CHECK (outcome_type IN
                        ('software','publication','research','internal_investment','other')),
    status          TEXT    NOT NULL CHECK (status IN ('active','archived')),
    description     TEXT,
    rationale       TEXT,
    priority        TEXT CHECK (priority IS NULL OR priority IN ('low','normal','high','critical')),
    target_date     TEXT,
    success_criteria TEXT,
    constraints     TEXT,
    assumptions     TEXT,
    risks           TEXT,
    revision        INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
    created_at      TEXT    NOT NULL,
    updated_at      TEXT    NOT NULL,
    archived_at     TEXT
);

CREATE TABLE goal_revisions (
    goal_id          TEXT    NOT NULL REFERENCES goals(id),
    revision_number  INTEGER NOT NULL,
    changed_at       TEXT    NOT NULL,
    actor            TEXT    NOT NULL,
    reason           TEXT,
    changed_fields   TEXT    NOT NULL,
    prior_state      TEXT    NOT NULL,
    PRIMARY KEY (goal_id, revision_number)
);
