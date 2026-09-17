"""
db.py · Line 3 Maintenance Log · Lab U05-01 STARTER

Built from the course reference app (stage w09) with the functions you write
in this lab taken out. Every TODO names its lab part. The report functions near
the bottom are complete: read them now. You write your own in Week 10.

The only module that talks to the database. Every SQL statement in the
application is in this file. No other file imports sqlite3; test_app.py checks.

Why one module: when the app moves to PostgreSQL in Week 10, the change lives
here. POSTGRES.md lists every line that changes and why.

Three rules every query below follows:
  1. Values travel as parameters (the ? marks), never pasted into the SQL text.
     Nothing a person types can change what a query does.
  2. Every function takes the connection as its first argument. The web app
     passes one per request; manage.py and import_csv.py open their own.
  3. Write functions do not commit. The caller wraps them in transaction(),
     so a group of writes either all happen or none do.
"""

import pathlib
import sqlite3
from contextlib import contextmanager

from flask import current_app, g

from models import (TIME_FORMAT, Equipment, Issue, Technician, WorkNote,
                    parse_time)

HERE = pathlib.Path(__file__).parent
SCHEMA_PATH = HERE / "schema.sql"
SEED_PATH = HERE / "seed.sql"


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------

def connect(path):
    """Open one connection with the settings this app relies on."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    # TODO Part 1, step 8: SQLite ignores foreign keys unless each connection
    #   turns them on. One line goes here.
    return conn


def get_db():
    """The connection for the current request, opened on first use."""
    if "db" not in g:
        g.db = connect(current_app.config["DATABASE_PATH"])
    return g.db


def close_db(exception=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_app(app):
    app.teardown_appcontext(close_db)


@contextmanager
def transaction(conn):
    """Commit if the block finishes, roll back if it raises."""
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def run_script(conn, path):
    """Run a .sql file such as schema.sql or seed.sql."""
    conn.executescript(pathlib.Path(path).read_text(encoding="utf-8"))
    conn.commit()


def create_database(path, seed=True):
    conn = connect(path)
    try:
        run_script(conn, SCHEMA_PATH)
        if seed:
            run_script(conn, SEED_PATH)
    finally:
        conn.close()


def table_names(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()
    return [row["name"] for row in rows]


KNOWN_TABLES = ("equipment", "issues", "technicians", "work_notes")


def table_counts(conn):
    """Rows per table. A table name cannot be a ? parameter, because
    parameters carry values, not names. So each name is checked against a
    fixed list before it goes into the SQL text."""
    counts = {}
    for name in table_names(conn):
        if name not in KNOWN_TABLES:
            raise ValueError(f"unexpected table {name!r}")
        counts[name] = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    return counts


# ---------------------------------------------------------------------------
# Rows to objects
# ---------------------------------------------------------------------------

ISSUE_COLUMNS = """
    i.id, e.code AS equipment_code, e.name AS equipment_name, i.title, i.description,
    i.severity, i.status, t.badge AS reporter_badge, t.display_name AS reporter_name,
    i.reported_at, i.closed_at, i.downtime_minutes, i.locked_out
"""
ISSUE_FROM = """
    FROM issues AS i
    JOIN equipment AS e ON e.id = i.equipment_id
    JOIN technicians AS t ON t.id = i.reported_by
"""
URGENCY_ORDER = """
    CASE i.severity WHEN 'critical' THEN 4 WHEN 'high' THEN 3 WHEN 'medium' THEN 2 ELSE 1 END DESC,
    i.reported_at DESC
"""


def _issue(row):
    return Issue(
        id=row["id"],
        equipment_code=row["equipment_code"],
        equipment_name=row["equipment_name"],
        title=row["title"],
        description=row["description"],
        severity=row["severity"],
        status=row["status"],
        reporter_badge=row["reporter_badge"],
        reporter_name=row["reporter_name"],
        reported_at=parse_time(row["reported_at"]),
        closed_at=parse_time(row["closed_at"]),
        downtime_minutes=row["downtime_minutes"],
        locked_out=bool(row["locked_out"]),
    )


def _equipment(row):
    return Equipment(id=row["id"], code=row["code"], name=row["name"],
                     cell=row["cell"], kind=row["kind"])


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

def list_equipment(conn):
    rows = conn.execute("SELECT id, code, name, cell, kind FROM equipment ORDER BY code").fetchall()
    return [_equipment(r) for r in rows]


def get_equipment(conn, code):
    row = conn.execute("SELECT id, code, name, cell, kind FROM equipment WHERE code = ?",
                       (code,)).fetchone()
    return _equipment(row) if row else None


def equipment_codes(conn):
    return {r["code"] for r in conn.execute("SELECT code FROM equipment").fetchall()}


def active_badges(conn):
    return {r["badge"] for r in conn.execute(
        "SELECT badge FROM technicians WHERE active = 1").fetchall()}


def get_technician(conn, badge):
    row = conn.execute("SELECT id, badge, display_name, role FROM technicians WHERE badge = ?",
                       (badge,)).fetchone()
    if row is None:
        return None
    return Technician(id=row["id"], badge=row["badge"], display_name=row["display_name"],
                      role=row["role"])


# ---------------------------------------------------------------------------
# Issues: create, read, update, delete
# ---------------------------------------------------------------------------

def list_issues(conn, status=None, equipment=None, search=None, open_only=False):
    """TODO Part 2, steps 13-16. Every filter is optional.

    Build two lists, conditions and params. Each filter that is given adds one
    fixed condition string, such as "i.status = ?" or "e.code = ?", and one
    parameter. open_only adds "i.status <> 'closed'" and no parameter. The
    search matches the title OR the description, ignores case, and treats the
    characters % _ and backslash as plain text. The lab handout gives you the
    escape line for that.

    Then run SELECT {ISSUE_COLUMNS} {ISSUE_FROM} {where} ORDER BY {URGENCY_ORDER}
    with the params, and return [_issue(r) for r in rows].
    Never put a value into the SQL text.
    """
    return []


def get_issue(conn, issue_id):
    """TODO Part 2, step 11: one issue by id, or None. Use ISSUE_COLUMNS and ISSUE_FROM."""
    return None


def create_issue(conn, clean, now):
    """TODO Part 2, step 12. Insert one validated issue and return its new id.

    Read add_note() below first: it is the same pattern. The form gives a
    machine CODE and a BADGE, but the table stores their ids, so the VALUES
    list looks each one up with a subquery. status is clean.get("status", "open"),
    locked_out is stored as int(clean["locked_out"]), reported_at is
    clean.get("reported_at") or now.strftime(TIME_FORMAT), and closed_at is
    clean.get("closed_at"). End the statement with RETURNING id. Do not commit.
    """
    raise NotImplementedError("create_issue is Lab U05-01, Part 2")


def update_issue(conn, issue_id, clean, now):
    """TODO Part 3, steps 19-20. Change an issue. Return True if a row changed.

    Closing an issue stamps closed_at once. Saving a closed issue again keeps
    the first closed_at. Reopening clears it. One UPDATE can do all three with
    CASE WHEN and COALESCE. cursor.rowcount says how many rows changed.
    The reporter never changes.
    """
    raise NotImplementedError("update_issue is Lab U05-01, Part 3")


def delete_issue(conn, issue_id):
    """TODO Part 3, step 21. Delete an issue. Return True if a row was deleted.
    Its work notes must go with it. Which file makes that happen?"""
    raise NotImplementedError("delete_issue is Lab U05-01, Part 3")


# ---------------------------------------------------------------------------
# Work notes
# ---------------------------------------------------------------------------

def list_notes(conn, issue_id):
    rows = conn.execute(
        """
        SELECT n.id, t.badge, t.display_name, n.note, n.minutes_spent, n.created_at
        FROM work_notes AS n
        JOIN technicians AS t ON t.id = n.technician_id
        WHERE n.issue_id = ?
        ORDER BY n.created_at, n.id
        """,
        (issue_id,),
    ).fetchall()
    return [WorkNote(id=r["id"], technician_badge=r["badge"], technician_name=r["display_name"],
                     note=r["note"], minutes_spent=r["minutes_spent"],
                     created_at=parse_time(r["created_at"])) for r in rows]


def add_note(conn, issue_id, clean, now):
    row = conn.execute(
        """
        INSERT INTO work_notes (issue_id, technician_id, note, minutes_spent, created_at)
        VALUES (?, (SELECT id FROM technicians WHERE badge = ?), ?, ?, ?)
        RETURNING id
        """,
        (issue_id, clean["badge"], clean["note"], clean["minutes_spent"],
         now.strftime(TIME_FORMAT)),
    ).fetchone()
    return row["id"]


# ---------------------------------------------------------------------------
# Reports: calculated fields
# ---------------------------------------------------------------------------

def report_by_equipment(conn):
    """One row per machine. Every number after the name is calculated.

    Labor comes from a subquery. Joining work_notes straight into this query
    would repeat each issue once per note and count its downtime twice.
    Dividing by 60.0, not 60, keeps the fraction: 75 / 60 is 1 in integer
    division and 1.25 in decimal division."""
    rows = conn.execute(
        """
        SELECT e.code, e.name,
               COUNT(i.id) AS total_issues,
               SUM(CASE WHEN i.status <> 'closed' THEN 1 ELSE 0 END) AS open_issues,
               COALESCE(SUM(i.downtime_minutes), 0) AS downtime_minutes,
               ROUND(COALESCE(SUM(i.downtime_minutes), 0) / 60.0, 1) AS downtime_hours,
               ROUND(COALESCE(AVG(i.downtime_minutes), 0), 1) AS avg_downtime_minutes,
               ROUND(COALESCE(labor.minutes, 0) / 60.0, 1) AS labor_hours
        FROM equipment AS e
        LEFT JOIN issues AS i ON i.equipment_id = e.id
        LEFT JOIN (
            SELECT i2.equipment_id, SUM(n.minutes_spent) AS minutes
            FROM work_notes AS n
            JOIN issues AS i2 ON i2.id = n.issue_id
            GROUP BY i2.equipment_id
        ) AS labor ON labor.equipment_id = e.id
        GROUP BY e.id, e.code, e.name, labor.minutes
        ORDER BY downtime_minutes DESC, e.code
        """
    ).fetchall()
    return [dict(r) for r in rows]


def report_totals(conn):
    row = conn.execute(
        """
        SELECT COUNT(*) AS total_issues,
               SUM(CASE WHEN status <> 'closed' THEN 1 ELSE 0 END) AS open_issues,
               ROUND(COALESCE(SUM(downtime_minutes), 0) / 60.0, 1) AS downtime_hours,
               ROUND((SELECT COALESCE(SUM(minutes_spent), 0) FROM work_notes) / 60.0, 1)
                   AS labor_hours
        FROM issues
        """
    ).fetchone()
    totals = dict(row)
    totals["open_issues"] = totals["open_issues"] or 0
    return totals


def report_open_by_severity(conn):
    rows = conn.execute(
        """
        SELECT severity, COUNT(*) AS open_count
        FROM issues
        WHERE status <> 'closed'
        GROUP BY severity
        """
    ).fetchall()
    return {r["severity"]: r["open_count"] for r in rows}


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

def import_issues(conn, rows):
    """TODO Part 3, step 23. Insert validated rows and return their new ids.
    All of them, or none of them."""
    raise NotImplementedError("import_issues is Lab U05-01, Part 3")
