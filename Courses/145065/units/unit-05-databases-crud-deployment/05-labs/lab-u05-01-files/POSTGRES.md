# Moving from SQLite to PostgreSQL

Riverside Fabrication is a composite: an invented shop with invented records.

**Why two databases.** SQLite is a file. It needs no server, no password, and no install, which
is why you build and test with it in Week 9. Render's web services do not keep files you write
between deploys [VERIFY: check Render's current documentation on persistent disks], so a live
app needs a database server. PostgreSQL is the one Render offers [VERIFY]. This page lists every
difference that touches this app, so the move in Week 10 is a planned change and not a surprise.

**Nothing on this page has been run against PostgreSQL on the build machine.** PostgreSQL and
psycopg are not installed there, and nothing may be installed. Every PostgreSQL-specific line is
marked [VERIFY]. The SQLite side of every comparison was run and tested.

## What `db.py` isolates

Every SQL statement lives in `db.py`, and no other file imports `sqlite3`
(`test_only_db_py_touches_sqlite` checks). So the switch touches one Python file and one schema
file. `w10_deploy/db.py` is the finished switch; this page explains it.

## The differences

| # | Topic | SQLite (tested here) | PostgreSQL [VERIFY] | What this app does |
|---|---|---|---|---|
| 1 | Driver | `import sqlite3`, part of Python | `import psycopg` (psycopg 3), installed with `pip install "psycopg[binary]"` | w10 imports psycopg only when `DATABASE_URL` is set, and gives a clear error if it is missing |
| 2 | Connecting | `sqlite3.connect("instance/line3.db")` | `psycopg.connect(DATABASE_URL)` with a URL such as `postgresql://user:password@host:5432/dbname` | the URL comes from the environment, never from the code |
| 3 | Placeholders | `?` | `%s` | queries are written once with `?`; w10's `to_pyformat()` rewrites them for psycopg |
| 4 | A literal `%` in SQL | fine | must be written `%%` when the query has parameters | `to_pyformat()` doubles it |
| 5 | Rows by column name | `conn.row_factory = sqlite3.Row` | `psycopg.connect(..., row_factory=dict_row)` from `psycopg.rows` | both give `row["title"]` |
| 6 | Auto-numbered ids | `id INTEGER PRIMARY KEY` fills itself | `id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY` (or the older `SERIAL`) | `w10_deploy/schema_postgres.sql` |
| 7 | Getting the new id | `cursor.lastrowid`, or `RETURNING id` (SQLite 3.35 and later; this machine has 3.50.4) | `RETURNING id` | `RETURNING id` everywhere, so the line never changes |
| 8 | Foreign keys | off unless each connection runs `PRAGMA foreign_keys = ON` | always on | `connect()` runs the PRAGMA for SQLite only |
| 9 | Explicit ids in seed data | accepted | refused by `GENERATED ALWAYS`; and inserting ids by hand leaves the sequence behind | `seed.sql` never gives an id; it looks up foreign keys by badge, code, or title |
| 10 | Running a whole `.sql` file | `conn.executescript(text)` | `conn.execute(text)` with no parameters | `Connection.run_script()` in w10 |
| 11 | Listing tables | `sqlite_master` | `information_schema.tables` | `table_names()` branches on the backend |
| 12 | Types are | flexible: a column accepts most values | strict: a text value in an integer column is an error | validation already converts every value |
| 13 | Case in `LIKE` | case-insensitive for ASCII letters | case-sensitive | the search lowers both sides: `LOWER(title) LIKE ?` |
| 14 | `ROUND(x, 1)` | works on floating-point values | defined for `numeric`; `SUM(int) / 60.0` is `numeric`, so it works | results come back as `Decimal`; w10 converts them to `float` |
| 15 | Time columns | no date type; text in ISO 8601 sorts correctly | `TIMESTAMPTZ` is the proper type | **kept as TEXT in both**, a deliberate tradeoff below |
| 16 | True and false | no boolean type; 0 and 1 | `BOOLEAN` | **kept as INTEGER 0 or 1 in both** |
| 17 | Transactions | `sqlite3` opens one before a write | psycopg opens one before the first statement, reads included | `transaction()` commits or rolls back either way; closing without a commit discards |
| 18 | Where the database lives | a file next to the app | a separate server; Render gives its URL [VERIFY] | `DATABASE_URL` in the environment |

## The tradeoff in rows 15 and 16

Keeping times as text and flags as integers means `db.py` and the templates do not change
between databases. The cost is real: PostgreSQL cannot check that `reported_at` is a real time,
and time arithmetic has to happen in Python (`Issue.hours_to_close`). The strongest case for
switching is that the database would then enforce the type and do date math for you. The
strongest case against, for a two-week unit, is that the switch would change every query that
touches a time. This anchor chose the smaller change. A student who argues for `TIMESTAMPTZ`
with a migration plan is making a good argument.

## Workbench and the syllabus tool

The syllabus names MySQL Workbench as the learning tool for this unit. It is not installed on
the build machine. Its menu paths are not written here. [VERIFY on a lab machine: connecting
Workbench to a local MySQL server, and whether a class uses it only to draw the ER diagram.]
The SQL in `schema.sql` is close to portable, but MySQL differs from both databases above in
several ways (for example `AUTO_INCREMENT` and its handling of `CHECK`), so treat it as a third
dialect, not a copy.

## Checklist for a lab machine with PostgreSQL [VERIFY every step]

1. Create an empty database and note its URL.
2. From `w10_deploy/`, install the requirements, then run
   `python manage.py init-if-empty` with `DATABASE_URL` set. Expect "Created the tables".
3. `python manage.py tables` should list equipment 6, issues 7, technicians 4, work_notes 5.
4. Start `python serve_local.py --port 8654` with `APP_ENV=production`, a `SECRET_KEY`, and
   `DATABASE_URL`. Open `/health`: expect `{"database":"ok","status":"ok","version":"1.0.0"}`.
5. Before changing any data, open `/reports` and compare every number with
   `test_by_equipment_matches_hand_calculation` in `test_app.py`. Watch OV-01: 1.3 hours.
6. Search for `100%` and for `O'Brien`. Both must return a page, not an error.
7. Create, edit, note, and delete an issue in the browser.
8. Stop the server, then run `python import_csv.py data/issues_import.csv`. Expect 4 issues imported.
