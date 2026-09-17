-- schema.sql · Line 3 Scrap Review
-- Riverside Fabrication is a composite. The plant keeps one scrap table for
-- Lines 3 and 4. Each part's number and name live once, in parts.

CREATE TABLE parts (
    id     INTEGER PRIMARY KEY,
    number TEXT    NOT NULL UNIQUE,
    name   TEXT    NOT NULL
);

CREATE TABLE scrap_entries (
    id             INTEGER PRIMARY KEY,
    part_id        INTEGER NOT NULL REFERENCES parts (id),
    line           INTEGER NOT NULL CHECK (line IN (3, 4)),
    shift          TEXT    NOT NULL CHECK (shift IN ('first', 'second')),
    quantity       INTEGER NOT NULL CHECK (quantity BETWEEN 1 AND 500),
    reason         TEXT    NOT NULL CHECK (length(reason) BETWEEN 5 AND 120),
    rework_minutes INTEGER NOT NULL CHECK (rework_minutes BETWEEN 0 AND 1440),
    logged_at      TEXT    NOT NULL
);
