"""
db.py · Line 3 Maintenance Log · Lab U05-02 STARTER

The only module that talks to the database. What changed since w09: this file
can now open either SQLite (on your machine) or PostgreSQL (on Render). The
rest of the application cannot tell which one it has.

How the switch works:
  * config.py sets DATABASE_URL when the environment has one. If it does,
    connect() opens PostgreSQL through psycopg. If not, SQLite.
  * Every query in this file is written once, with ? placeholders.
    Connection.execute() rewrites them to %s for psycopg, which uses that style.
  * Rows come back as mappings from both drivers, so row["title"] works on both.
    Numbers PostgreSQL returns as Decimal are turned into float for the reports.

[VERIFY] The PostgreSQL branch has never run on this machine: PostgreSQL and
psycopg are not installed here. It follows psycopg 3's documented API. Run the
test suite and the checklist in DEPLOY.md against a real PostgreSQL database on
a lab machine before a class depends on it.

Three rules every query below follows:
  1. Values travel as parameters, never pasted into the SQL text.
  2. Every function takes the connection as its first argument.
  3. Write functions do not commit. The caller wraps them in transaction().
"""

import pathlib
import sqlite3
from contextlib import contextmanager
from decimal import Decimal

from flask import current_app, g

from models import (TIME_FORMAT, Equipment, Issue, Technician, WorkNote,
                    parse_time)

HERE = pathlib.Path(__file__).parent
SCHEMA_PATHS = {"sqlite": HERE / "schema.sql", "postgres": HERE / "schema_postgres.sql"}
SEED_PATH = HERE / "seed.sql"
KNOWN_TABLES = ("equipment", "issues", "technicians", "work_notes")


class DatabaseConfigError(Exception):
    """The configuration asks for a database this machine cannot open."""


def to_pyformat(sql):
    """Rewrite ? placeholders as %s for psycopg.

    A ? inside a quoted SQL string is text, not a placeholder, so it is left
    alone. A literal % must be written %% for psycopg, inside or outside quotes."""
    out, in_quote = [], False
    for ch in sql:
        if ch == "'":
            in_quote = not in_quote
            out.append(ch)
        elif ch == "%":
            out.append("%%")
        elif ch == "?" and not in_quote:
            out.append("%s")
        else:
            out.append(ch)
    if in_quote:
        raise ValueError("unbalanced quote in SQL")
    return "".join(out)


class Connection:
    """A thin wrapper so the rest of this file never checks which database it has."""

    def __init__(self, raw, backend):
        self.raw = raw
        self.backend = backend

    def execute(self, sql, params=()):
        if self.backend == "postgres":
            return self.raw.execute(to_pyformat(sql), params)
        return self.raw.execute(sql, params)

    def run_script(self, text):
        if self.backend == "postgres":
            # [VERIFY] psycopg 3 runs several statements in one execute() only
            # when no parameters are passed. These scripts pass none.
            self.raw.execute(text)
        else:
            self.raw.executescript(text)
        self.raw.commit()

    def commit(self):
        self.raw.commit()

    def rollback(self):
        self.raw.rollback()

    def close(self):
        self.raw.close()


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------

def backend_for(config):
    return "postgres" if config.get("DATABASE_URL") else "sqlite"


def connect(config, create=False):
    """Open one connection. `config` is a mapping with DATABASE_URL and DATABASE_PATH.

    SQLite creates an empty file when a path is wrong, and an app pointed at
    an empty file looks healthy until the first query. So an existing SQLite
    database is opened read-write only (mode=rw), and a missing one is an
    error unless create=True."""
    if backend_for(config) == "postgres":
        try:
            import psycopg  # noqa: PLC0415  (only needed on the server)
            from psycopg.rows import dict_row  # noqa: PLC0415
        except ImportError:
            raise DatabaseConfigError(
                "DATABASE_URL is set, but psycopg is not installed. "
                "Install requirements.txt on the server, or unset DATABASE_URL to use SQLite."
            ) from None
        # [VERIFY] Render's connection string and whether it needs sslmode=require.
        raw = psycopg.connect(config["DATABASE_URL"], row_factory=dict_row)
        return Connection(raw, "postgres")
    mode = "rwc" if create else "rw"
    uri = pathlib.Path(config["DATABASE_PATH"]).resolve().as_uri() + f"?mode={mode}"
    raw = sqlite3.connect(uri, uri=True)
    raw.row_factory = sqlite3.Row
    # SQLite ignores foreign keys unless each connection turns them on.
    # PostgreSQL always enforces them, so this line has no PostgreSQL twin.
    raw.execute("PRAGMA foreign_keys = ON")
    return Connection(raw, "sqlite")


def connect_path(path, create=False):
    """A SQLite connection for tools and tests."""
    return connect({"DATABASE_URL": "", "DATABASE_PATH": str(path)}, create=create)


def get_db():
    if "db" not in g:
        g.db = connect(current_app.config)
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


def create_schema(conn, seed=True):
    conn.run_script(SCHEMA_PATHS[conn.backend].read_text(encoding="utf-8"))
    if seed:
        conn.run_script(SEED_PATH.read_text(encoding="utf-8"))


def create_database(path, seed=True):
    conn = connect_path(path, create=True)
    try:
        create_schema(conn, seed)
    finally:
        conn.close()


def table_names(conn):
    if conn.backend == "postgres":
        sql = ("SELECT table_name AS name FROM information_schema.tables "
               "WHERE table_schema = 'public' ORDER BY table_name")
    else:
        sql = ("SELECT name FROM sqlite_master "
               "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    return [row["name"] for row in conn.execute(sql).fetchall()]


def table_counts(conn):
    """Rows per table. A table name cannot be a parameter, so each name is
    checked against a fixed list before it goes into the SQL text."""
    counts = {}
    for name in table_names(conn):
        if name not in KNOWN_TABLES:
            raise ValueError(f"unexpected table {name!r}")
        counts[name] = conn.execute(f"SELECT COUNT(*) AS n FROM {name}").fetchone()["n"]
    return counts


def ping(conn):
    """Raise if the database cannot answer.

    TODO Part 3, step 14: this answers "ok" for a database with no tables at
    all, which is exactly what a host sees when the build skipped
    init-if-empty. Make it query a real table instead."""
    conn.execute("SELECT 1").fetchone()


def _plain(row):
    """A row as a dict of plain Python values. Decimal becomes float."""
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in dict(row).items()}


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
    conditions, params = [], []
    if status:
        conditions.append("i.status = ?")
        params.append(status)
    if open_only:
        conditions.append("i.status <> 'closed'")
    if equipment:
        conditions.append("e.code = ?")
        params.append(equipment)
    if search:
        term = search.lower().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        conditions.append(
            "(LOWER(i.title) LIKE ? ESCAPE '\\' OR LOWER(i.description) LIKE ? ESCAPE '\\')")
        params.extend([f"%{term}%", f"%{term}%"])
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # The only text joined into this SQL is the fixed condition strings above.
    sql = f"SELECT {ISSUE_COLUMNS} {ISSUE_FROM} {where} ORDER BY {URGENCY_ORDER}"
    return [_issue(r) for r in conn.execute(sql, params).fetchall()]


def get_issue(conn, issue_id):
    row = conn.execute(f"SELECT {ISSUE_COLUMNS} {ISSUE_FROM} WHERE i.id = ?",
                       (issue_id,)).fetchone()
    return _issue(row) if row else None


def create_issue(conn, clean, now):
    """RETURNING id works in SQLite 3.35 and later and in PostgreSQL."""
    row = conn.execute(
        """
        INSERT INTO issues (equipment_id, reported_by, title, description, severity, status,
                            downtime_minutes, locked_out, reported_at, closed_at)
        VALUES ((SELECT id FROM equipment WHERE code = ?),
                (SELECT id FROM technicians WHERE badge = ?),
                ?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """,
        (clean["equipment"], clean["reported_by"], clean["title"], clean["description"],
         clean["severity"], clean.get("status", "open"), clean["downtime_minutes"],
         int(clean["locked_out"]), clean.get("reported_at") or now.strftime(TIME_FORMAT),
         clean.get("closed_at")),
    ).fetchone()
    return row["id"]


def update_issue(conn, issue_id, clean, now):
    cursor = conn.execute(
        """
        UPDATE issues
        SET equipment_id = (SELECT id FROM equipment WHERE code = ?),
            title = ?, description = ?, severity = ?, status = ?,
            downtime_minutes = ?, locked_out = ?,
            closed_at = CASE WHEN ? = 'closed' THEN COALESCE(closed_at, ?) ELSE NULL END
        WHERE id = ?
        """,
        (clean["equipment"], clean["title"], clean["description"], clean["severity"],
         clean["status"], clean["downtime_minutes"], int(clean["locked_out"]),
         clean["status"], now.strftime(TIME_FORMAT), issue_id),
    )
    return cursor.rowcount == 1


def delete_issue(conn, issue_id):
    cursor = conn.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    return cursor.rowcount == 1


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
    """TODO Part 1, steps 2-5. One row per machine, most downtime first, then by code.

    Every machine appears, including one with no issues. Each row is a dict with
    these keys, in this order:
        code, name, total_issues, open_issues, downtime_minutes,
        downtime_hours, avg_downtime_minutes, labor_hours
    Hours and the average are rounded to 1 decimal place. Labor comes from
    work_notes.minutes_spent through a SUBQUERY: read the handout before you
    join work_notes. Return [_plain(r) for r in rows].
    """
    return []


def report_totals(conn):
    """TODO Part 1, step 6. One dict for all of Line 3:
        total_issues, open_issues, downtime_hours, labor_hours
    Hours rounded to 1 place. An empty database gives 0 and 0.0, never None.
    Return it through _plain(), and make open_issues an int."""
    return {"total_issues": 0, "open_issues": 0, "downtime_hours": 0.0, "labor_hours": 0.0}


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
    """Insert validated import rows in one transaction. All or nothing."""
    with transaction(conn):
        return [create_issue(conn, row, now=None) for row in rows]
