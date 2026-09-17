r"""
downtime_app.py · Line 3 Downtime Log · Flask, SQLite, ready to deploy

Riverside Fabrication is a composite, an invented shop. Every record is invented.

A supervisor logs machine downtime and reads a cost report. This stage is about
deployment: the settings come from the environment, debug is off, and a /health
endpoint tells the host whether the app can serve real data.

Settings read from the environment:

    APP_ENV       development (default), test, or production
    SECRET_KEY    signs session cookies. Required in production, 32+ characters.
    DATABASE_PATH a SQLite file. Defaults to a file in the temporary folder.

Make a real key with:  python -c "import secrets; print(secrets.token_hex(32))"

Run it, stating the port every time:

    set APP_ENV=production
    set SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM%%RANDOM%%RANDOM%
    python downtime_app.py --port 8680
"""

import argparse
import json
import os
import pathlib
import socket
import sqlite3
import tempfile

from flask import Flask, abort, g, jsonify, render_template

HERE = pathlib.Path(__file__).parent
APP_VERSION = "1.0.0"
LINE = 3


def load_config(environ=None):
    """Build the settings from the environment. Production needs a real secret."""
    env = os.environ if environ is None else environ
    app_env = env.get("APP_ENV", "development")
    secret = env.get("SECRET_KEY") or "dev-secret-change-me"
    return {
        "APP_ENV": app_env,
        "DEBUG": False,
        "TESTING": app_env == "test",
        "SECRET_KEY": secret,
        "DATABASE_PATH": env.get(
            "DATABASE_PATH", str(pathlib.Path(tempfile.gettempdir()) / "line3_downtime_w10.db")),
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "MAX_CONTENT_LENGTH": 64 * 1024,
    }


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def connect(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database(path):
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


def load_rates():
    """The dollars-per-hour rate for each machine's downtime, from rates.json."""
    return json.loads((HERE / "rates.json").read_text(encoding="utf-8"))


def cost_for(code, minutes):
    rate = load_rates().get(code, 0)
    return round(minutes / 60.0 * rate, 2)


def recent_events(conn):
    """The Line 3 downtime events, newest first."""
    return conn.execute(
        """SELECT ev.id, ev.reason, ev.minutes, ev.resolved, ev.occurred_at, eq.code, eq.name
           FROM downtime_events AS ev JOIN equipment AS eq ON eq.id = ev.equipment_id
           WHERE ev.line = ? ORDER BY ev.occurred_at DESC""", (LINE,)).fetchall()


def one_event(conn, event_id):
    return conn.execute(
        """SELECT ev.*, eq.code, eq.name FROM downtime_events AS ev
           JOIN equipment AS eq ON eq.id = ev.equipment_id
           WHERE ev.id = ? AND ev.line = ?""", (event_id, LINE)).fetchone()


def downtime_by_machine(conn):
    """Each machine with its event count and total downtime minutes on Line 3."""
    return conn.execute(
        """SELECT eq.code, eq.name,
                  COUNT(*)                             AS events,
                  COALESCE(SUM(ev.minutes), 0)         AS minutes
           FROM equipment AS eq
           LEFT JOIN downtime_events AS ev ON ev.equipment_id = eq.id AND ev.line = ?
           GROUP BY eq.id, eq.code, eq.name
           ORDER BY minutes DESC, eq.code""", (LINE,)).fetchall()


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config.update(load_config())
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(exception=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


@app.get("/")
def dashboard():
    events = recent_events(get_db())
    return render_template("index.html", events=events)


@app.get("/events/<int:event_id>")
def event_detail(event_id):
    event = one_event(get_db(), event_id)
    if event is None:
        abort(404)
    cost = cost_for(event["code"], event["minutes"])
    return render_template("event.html", event=event, cost=cost)


@app.get("/report")
def report():
    conn = get_db()
    rows = []
    for row in downtime_by_machine(conn):
        cost = cost_for(row["code"], row["minutes"])
        rows.append({"row": row, "cost": cost})
    total_cost = round(sum(r["cost"] for r in rows), 2)
    return render_template("report.html", rows=rows, total_cost=total_cost)


@app.get("/health")
def health():
    """For the host: 200 when the app can reach its database, 503 when it cannot."""
    try:
        get_db().execute("SELECT 1")
    except Exception:
        app.logger.exception("health check failed")
        return jsonify(status="error", database="unavailable", version=APP_VERSION), 503
    return jsonify(status="ok", database="ok", version=APP_VERSION)


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, message="No Line 3 record at that address."), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", code=500, message="Something went wrong on our side."), 500


# ---------------------------------------------------------------------------
# Local run
# ---------------------------------------------------------------------------

def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Line 3 Downtime Log")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use.")
        return 1
    create_database(app.config["DATABASE_PATH"])
    print(f"Database rebuilt at {app.config['DATABASE_PATH']} (APP_ENV={app.config['APP_ENV']})")
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
