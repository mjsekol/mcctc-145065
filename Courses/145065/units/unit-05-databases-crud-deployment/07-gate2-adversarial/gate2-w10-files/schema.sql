-- schema.sql · Line 3 Downtime Log. Riverside Fabrication is a composite.

CREATE TABLE equipment (
    id   INTEGER PRIMARY KEY,
    code TEXT    NOT NULL UNIQUE,
    name TEXT    NOT NULL
);

CREATE TABLE downtime_events (
    id           INTEGER PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES equipment (id),
    line         INTEGER NOT NULL CHECK (line IN (3, 4)),
    reason       TEXT    NOT NULL CHECK (length(reason) BETWEEN 5 AND 120),
    minutes      INTEGER NOT NULL CHECK (minutes BETWEEN 1 AND 1440),
    resolved     INTEGER NOT NULL CHECK (resolved IN (0, 1)),
    occurred_at  TEXT    NOT NULL
);
