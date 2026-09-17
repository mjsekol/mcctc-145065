-- schema.sql · Line 3 Maintenance Log · stage w10_deploy · SQLite
--
-- Four tables. Each fact lives in exactly one place:
--   technicians   who can log work (badge and display name only, nothing personal)
--   equipment     the machines on Line 3
--   issues        one problem on one machine, reported by one technician
--   work_notes    what someone did about an issue, and how long it took
--
-- The PostgreSQL version is schema_postgres.sql. The two differ only where
-- the databases differ; POSTGRES.md lists every difference.
--
-- Running this file deletes every table first. manage.py refuses to run it
-- over an existing database unless you pass --force.

DROP TABLE IF EXISTS work_notes;
DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS technicians;

CREATE TABLE technicians (
    id           INTEGER PRIMARY KEY,
    badge        TEXT    NOT NULL UNIQUE CHECK (length(badge) = 6),
    display_name TEXT    NOT NULL,
    role         TEXT    NOT NULL CHECK (role IN ('technician', 'supervisor')),
    active       INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1))
);

CREATE TABLE equipment (
    id   INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    cell TEXT NOT NULL,
    kind TEXT NOT NULL
);

CREATE TABLE issues (
    id               INTEGER PRIMARY KEY,
    equipment_id     INTEGER NOT NULL REFERENCES equipment (id),
    reported_by      INTEGER NOT NULL REFERENCES technicians (id),
    title            TEXT    NOT NULL,
    description      TEXT    NOT NULL,
    severity         TEXT    NOT NULL
                     CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status           TEXT    NOT NULL DEFAULT 'open'
                     CHECK (status IN ('open', 'in_progress', 'closed')),
    downtime_minutes INTEGER NOT NULL DEFAULT 0
                     CHECK (downtime_minutes BETWEEN 0 AND 1440),
    locked_out       INTEGER NOT NULL DEFAULT 0 CHECK (locked_out IN (0, 1)),
    reported_at      TEXT    NOT NULL,   -- UTC, ISO 8601, for example 2025-11-10T07:42:00Z
    closed_at        TEXT,               -- UTC, set when status becomes closed
    -- The database enforces the two cross-field rules too, so a bug in the
    -- application cannot store a record that breaks them.
    CHECK (severity <> 'critical' OR locked_out = 1),
    CHECK ((status = 'closed') = (closed_at IS NOT NULL))
);

CREATE TABLE work_notes (
    id            INTEGER PRIMARY KEY,
    issue_id      INTEGER NOT NULL REFERENCES issues (id) ON DELETE CASCADE,
    technician_id INTEGER NOT NULL REFERENCES technicians (id),
    note          TEXT    NOT NULL,
    minutes_spent INTEGER NOT NULL CHECK (minutes_spent BETWEEN 1 AND 720),
    created_at    TEXT    NOT NULL
);

-- Indexes on the columns the pages filter and join by.
CREATE INDEX idx_issues_equipment ON issues (equipment_id);
CREATE INDEX idx_issues_status ON issues (status);
CREATE INDEX idx_work_notes_issue ON work_notes (issue_id);
