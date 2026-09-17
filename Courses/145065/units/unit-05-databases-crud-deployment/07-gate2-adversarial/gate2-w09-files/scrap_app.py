r"""
scrap_app.py · Line 3 Scrap Review · Flask and SQLite

Riverside Fabrication is a composite, an invented shop. Every record is invented.

The plant keeps one scrap table for Lines 3 and 4. This app is Line 3's view of
it: the entries, a search, one entry, a delete, and a rework report.

Every start rebuilds the database from schema.sql and seed.sql in your
temporary folder, so you can delete entries freely. State the port every time:

    python scrap_app.py --port 8680
"""

import argparse
import os
import pathlib
import secrets
import socket
import sqlite3
import tempfile

from flask import (Flask, abort, g, redirect, render_template, request,
                   session, url_for)

HERE = pathlib.Path(__file__).parent
LINE = 3

app = Flask(__name__)
app.config["DATABASE_PATH"] = os.environ.get(
    "DATABASE_PATH", str(pathlib.Path(tempfile.gettempdir()) / "line3_scrap_w09.db"))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def connect(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database(path):
    """Build a fresh database from the schema and the seed."""
    pathlib.Path(path).unlink(missing_ok=True)
    conn = connect(path)
    for name in ("schema.sql", "seed.sql"):
        conn.executescript((HERE / name).read_text(encoding="utf-8"))
    conn.commit()
    conn.close()


def get_db():
    if "db" not in g:
        g.db = connect(app.config["DATABASE_PATH"])
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def list_entries(conn, q=""):
    """Line 3 entries, newest first. q narrows them to reasons containing q."""
    sql = "SELECT id, part_id, shift, quantity, reason, rework_minutes FROM scrap_entries WHERE line = 3"
    if q:
        sql += f" AND lower(reason) LIKE '%{q.lower()}%'"
    sql += " ORDER BY logged_at DESC"
    return conn.execute(sql).fetchall()


def part_label(conn, part_id):
    return conn.execute("SELECT number, name FROM parts WHERE id = ?", (part_id,)).fetchone()


def get_entry(conn, entry_id):
    return conn.execute(
        """SELECT s.*, p.number, p.name FROM scrap_entries AS s
           JOIN parts AS p ON p.id = s.part_id
           WHERE s.id = ? AND s.line = ?""", (entry_id, LINE)).fetchone()


def delete_entry(conn, entry_id):
    cursor = conn.execute("DELETE FROM scrap_entries WHERE id = ? AND line = ?", (entry_id, LINE))
    conn.commit()
    return cursor.rowcount == 1


def parts_with_scrap(conn):
    """The rework report: pieces, minutes, and hours for each part on Line 3."""
    return conn.execute(
        """SELECT p.number, p.name,
                  COALESCE(SUM(s.quantity), 0)                          AS pieces,
                  COALESCE(SUM(s.rework_minutes), 0)                    AS minutes,
                  ROUND(COALESCE(SUM(s.rework_minutes), 0) / 60, 2)     AS hours
           FROM parts AS p
           LEFT JOIN scrap_entries AS s ON s.part_id = p.id AND s.line = ?
           GROUP BY p.id, p.number, p.name
           ORDER BY minutes DESC, p.number""", (LINE,)).fetchall()


# ---------------------------------------------------------------------------
# CSRF: every POST carries the token from the session
# ---------------------------------------------------------------------------

def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


@app.before_request
def check_csrf():
    if request.method == "POST":
        sent = request.form.get("csrf_token", "")
        expected = session.get("csrf_token", "")
        if not expected or not secrets.compare_digest(sent, expected):
            abort(403)


app.jinja_env.globals["csrf_token"] = csrf_token


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    conn = get_db()
    q = request.args.get("q", "").strip()
    rows = []
    for entry in list_entries(conn, q):
        part = part_label(conn, entry["part_id"])
        rows.append({"entry": entry, "number": part["number"], "name": part["name"]})
    return render_template("index.html", rows=rows, q=q)


@app.get("/entries/<int:entry_id>")
def entry_detail(entry_id):
    entry = get_entry(get_db(), entry_id)
    if entry is None:
        abort(404)
    return render_template("entry.html", entry=entry)


@app.route("/entries/<int:entry_id>/delete", methods=["GET", "POST"])
def delete(entry_id):
    if not delete_entry(get_db(), entry_id):
        abort(404)
    return redirect(url_for("index"), code=303)


@app.get("/report")
def report():
    rows = parts_with_scrap(get_db())
    totals = {"pieces": sum(r["pieces"] for r in rows),
              "minutes": sum(r["minutes"] for r in rows)}
    return render_template("report.html", rows=rows, totals=totals)


@app.errorhandler(403)
def forbidden(error):
    return render_template("error.html", code=403, message="That form could not be accepted."), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, message="No Line 3 record at that address."), 404


def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Line 3 Scrap Review")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use.")
        return 1
    create_database(app.config["DATABASE_PATH"])
    print(f"Database rebuilt at {app.config['DATABASE_PATH']}")
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
