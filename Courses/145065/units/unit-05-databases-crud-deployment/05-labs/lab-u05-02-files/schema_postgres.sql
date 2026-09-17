-- schema_postgres.sql · Line 3 Maintenance Log · stage w10_deploy · PostgreSQL
--
-- [VERIFY] This file has not been run on this machine: PostgreSQL is not
-- installed here. Run it against a lab or Render database, then run the
-- checklist in DEPLOY.md, before a class depends on it.
--
-- It matches schema.sql line for line. The only differences:
--   1. id columns: INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY.
--      SQLite fills INTEGER PRIMARY KEY by itself. PostgreSQL needs an identity
--      column (or the older SERIAL) to number new rows.
--   2. DROP TABLE ... CASCADE, so a rebuild does not stop at a dependent object.
--
-- Kept the same on purpose, so db.py does not change:
--   * times stay TEXT in UTC ISO 8601. TIMESTAMPTZ is the better PostgreSQL
--     type; switching means converting in db.py. POSTGRES.md explains the tradeoff.
--   * flags stay INTEGER 0 or 1 rather than BOOLEAN, for the same reason.

DROP TABLE IF EXISTS work_notes CASCADE;
DROP TABLE IF EXISTS issues CASCADE;
DROP TABLE IF EXISTS equipment CASCADE;
DROP TABLE IF EXISTS technicians CASCADE;

CREATE TABLE technicians (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    badge        TEXT    NOT NULL UNIQUE CHECK (length(badge) = 6),
    display_name TEXT    NOT NULL,
    role         TEXT    NOT NULL CHECK (role IN ('technician', 'supervisor')),
    active       INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1))
);

CREATE TABLE equipment (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    cell TEXT NOT NULL,
    kind TEXT NOT NULL
);

CREATE TABLE issues (
    id               INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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
    reported_at      TEXT    NOT NULL,
    closed_at        TEXT,
    CHECK (severity <> 'critical' OR locked_out = 1),
    CHECK ((status = 'closed') = (closed_at IS NOT NULL))
);

CREATE TABLE work_notes (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    issue_id      INTEGER NOT NULL REFERENCES issues (id) ON DELETE CASCADE,
    technician_id INTEGER NOT NULL REFERENCES technicians (id),
    note          TEXT    NOT NULL,
    minutes_spent INTEGER NOT NULL CHECK (minutes_spent BETWEEN 1 AND 720),
    created_at    TEXT    NOT NULL
);

CREATE INDEX idx_issues_equipment ON issues (equipment_id);
CREATE INDEX idx_issues_status ON issues (status);
CREATE INDEX idx_work_notes_issue ON work_notes (issue_id);
