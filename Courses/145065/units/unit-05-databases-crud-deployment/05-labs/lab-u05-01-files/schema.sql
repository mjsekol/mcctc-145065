-- schema.sql · Line 3 Maintenance Log · Lab U05-01 STARTER · SQLite
--
-- Built from the course reference app (stage w09). This schema WORKS: the app
-- starts and the seed data loads. It is also wrong in several ways. Part 1 fixes them.
--
-- Four tables. Each fact lives in exactly one place:
--   technicians   who can log work (badge and display name only, nothing personal)
--   equipment     the machines on Line 3
--   issues        one problem on one machine, reported by one technician
--   work_notes    what someone did about an issue, and how long it took
--
-- The PostgreSQL version of this file arrives in Week 10. The two will differ
-- only where the databases differ; POSTGRES.md in this folder lists every difference.
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
    home_phone   TEXT,               -- TODO Part 1, step 4: the app never uses this. Should it be here?
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
    equipment_id     INTEGER NOT NULL,     -- TODO Part 1, step 5: holds an equipment id. Declare it.
    reported_by      INTEGER NOT NULL,     -- TODO Part 1, step 5: holds a technician id. Declare it.
    title            TEXT    NOT NULL,
    description      TEXT    NOT NULL,
    severity         TEXT    NOT NULL,     -- TODO Part 1, step 6: low, medium, high, or critical only
    status           TEXT    NOT NULL DEFAULT 'open',   -- TODO Part 1, step 6: open, in_progress, or closed only
    downtime_minutes INTEGER NOT NULL DEFAULT 0,        -- TODO Part 1, step 6: write it as BETWEEN 0 AND 1440
    locked_out       INTEGER NOT NULL DEFAULT 0,        -- TODO Part 1, step 6: 0 or 1 only
    reported_at      TEXT    NOT NULL,     -- UTC, ISO 8601, for example 2025-11-10T07:42:00Z
    closed_at        TEXT                  -- UTC, set when status becomes closed
    -- TODO Part 1, step 7: two table-level CHECK rules that each span two columns.
    --   A critical issue must be locked out.
    --   closed_at is set exactly when status is closed.
);

CREATE TABLE work_notes (
    id            INTEGER PRIMARY KEY,
    issue_id      INTEGER NOT NULL,     -- TODO Part 1, step 5: an issue id. Deleting the issue deletes its notes.
    technician_id INTEGER NOT NULL,     -- TODO Part 1, step 5: a technician id.
    note          TEXT    NOT NULL,
    minutes_spent INTEGER NOT NULL,     -- TODO Part 1, step 6: write it as BETWEEN 1 AND 720
    created_at    TEXT    NOT NULL
);

-- Indexes on the columns the pages filter and join by.
CREATE INDEX idx_issues_equipment ON issues (equipment_id);
CREATE INDEX idx_issues_status ON issues (status);
CREATE INDEX idx_work_notes_issue ON work_notes (issue_id);
