"""
app.py · Line 3 Maintenance Log · Lab U05-01 starter, unchanged from the reference stage w09 · Unit 5, Week 9

Riverside Fabrication is a composite, an invented shop. Every record is invented.

What this stage adds to w08_forms:
  * a normalized SQLite database: four related tables with keys (schema.sql)
  * full CRUD through parameterized queries, all inside db.py
  * search and filters that treat every typed character as data
  * a delete that asks for confirmation first
  * work notes, a second form on the issue page
  * a report with calculated fields, and a CSV export of it
  * CSV import (import_csv.py) and a SQL seed script (seed.sql)

First, create the database (once):

    python manage.py init --db instance/line3.db

Then run, stating the port every time:

    python app.py --port 8680

DATABASE_PATH in the environment points at a different database file.
SECRET_KEY in the environment signs the session cookie (see w08_forms).

Routes:
    GET  /                              dashboard: open work, most urgent first
    GET  /issues                        every issue; ?status= &equipment= &q= filter
    GET  /issues/new                    the blank form
    POST /issues/new                    create
    GET  /issues/<id>                   read one issue with its work notes
    GET  /issues/<id>/edit              the form, filled in
    POST /issues/<id>/edit              update
    POST /issues/<id>/notes             add a work note
    GET  /issues/<id>/delete            "are you sure?"
    POST /issues/<id>/delete            delete
    GET  /equipment                     every machine
    GET  /equipment/<code>              one machine and its issues
    GET  /reports                       downtime and labor by machine
    GET  /reports/downtime.csv          the same report as a CSV file
    GET  /trace                         what the server received for this request
"""

import argparse
import csv
import io
import os
import pathlib
import secrets
import socket
import sys
import time
from datetime import datetime, timezone

from flask import (Flask, Response, abort, flash, g, get_flashed_messages,
                   redirect, render_template, request, url_for)

import db
from models import SEVERITIES, STATUS_LABELS, STATUSES
from security import init_security
from validation import (BADGE_PATTERN, DESCRIPTION_MAX, DESCRIPTION_MIN,
                        DOWNTIME_MAX, NOTE_MAX, NOTE_MIN, NOTE_MINUTES_MAX,
                        NOTE_MINUTES_MIN, SEARCH_MAX, TITLE_MAX, TITLE_MIN,
                        validate_issue, validate_note, validate_search)

HERE = pathlib.Path(__file__).parent

app = Flask(__name__)
app.config["DATABASE_PATH"] = os.environ.get("DATABASE_PATH", str(HERE / "instance" / "line3.db"))
if os.environ.get("SECRET_KEY"):
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
else:
    app.config["SECRET_KEY"] = secrets.token_hex(32)
    print("[config] SECRET_KEY is not set. Using a random key for this run only.",
          file=sys.stderr, flush=True)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
db.init_app(app)

FIELD_IDS = {
    "reported_by": "reported-by",
    "equipment": "equipment",
    "title": "title",
    "description": "description",
    "severity": "severity-low",
    "status": "status",
    "downtime_minutes": "downtime-minutes",
    "locked_out": "locked-out",
    "badge": "note-badge",
    "note": "note-text",
    "minutes_spent": "note-minutes",
}

RULES = {
    "badge_pattern": BADGE_PATTERN,
    "title_min": TITLE_MIN, "title_max": TITLE_MAX,
    "description_min": DESCRIPTION_MIN, "description_max": DESCRIPTION_MAX,
    "downtime_max": DOWNTIME_MAX,
    "note_min": NOTE_MIN, "note_max": NOTE_MAX,
    "note_minutes_min": NOTE_MINUTES_MIN, "note_minutes_max": NOTE_MINUTES_MAX,
    "search_max": SEARCH_MAX,
}


def utc_now():
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# The request cycle, made visible
# ---------------------------------------------------------------------------

@app.before_request
def start_timer():
    g.started = time.perf_counter()


# Registered after start_timer, so the timer runs first and a refused POST is still timed.
init_security(app)


@app.after_request
def log_request(response):
    elapsed_ms = (time.perf_counter() - g.get("started", time.perf_counter())) * 1000
    query = f"?{request.query_string.decode('utf-8', 'replace')}" if request.query_string else ""
    print(
        f"[trace] {request.method} {request.path}{query} -> {request.endpoint} -> "
        f"{response.status_code} {response.mimetype} "
        f"({response.calculate_content_length() or 0} bytes, {elapsed_ms:.1f} ms)",
        flush=True,
    )
    return response


@app.context_processor
def shared_template_values():
    return {"status_labels": STATUS_LABELS, "rules": RULES, "field_ids": FIELD_IDS}


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

@app.get("/")
def dashboard():
    conn = db.get_db()
    open_issues = db.list_issues(conn, open_only=True)
    critical = [i for i in open_issues if i.severity == "critical"]
    return render_template("index.html", open_issues=open_issues, critical=critical,
                           messages=get_flashed_messages())


@app.get("/issues")
def list_issues():
    conn = db.get_db()
    status = request.args.get("status") or None
    equipment = request.args.get("equipment") or None
    search = validate_search(request.args.get("q"))
    if status is not None and status not in STATUSES:
        abort(400, description=f"Unknown status. Use one of: {', '.join(STATUSES)}.")
    machines = db.list_equipment(conn)
    if equipment is not None and equipment not in {m.code for m in machines}:
        abort(400, description="Unknown machine code.")
    issues = db.list_issues(conn, status=status, equipment=equipment, search=search)
    return render_template("issues.html", issues=issues, status=status, statuses=STATUSES,
                           equipment=machines, chosen_equipment=equipment, search=search,
                           filtered=bool(status or equipment or search))


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    return render_detail(issue_id)


def render_detail(issue_id, note_values=None, note_errors=None, status=200):
    conn = db.get_db()
    issue = db.get_issue(conn, issue_id)
    if issue is None:
        abort(404)
    return render_template("issue_detail.html", issue=issue, notes=db.list_notes(conn, issue_id),
                           messages=get_flashed_messages(), values=note_values or {},
                           errors=note_errors or {}), status


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def render_form(values, errors, issue=None, status=200):
    return render_template("issue_form.html", equipment=db.list_equipment(db.get_db()),
                           severities=SEVERITIES, statuses=STATUSES, values=values,
                           errors=errors, issue=issue), status


def form_values():
    return {name: request.form.get(name, "") for name in
            ["reported_by", "equipment", "title", "description", "severity", "status",
             "downtime_minutes", "locked_out"]}


@app.get("/issues/new")
def new_issue_form():
    return render_form(values={}, errors={})


@app.post("/issues/new")
def create_issue():
    conn = db.get_db()
    clean, errors = validate_issue(request.form, db.equipment_codes(conn), db.active_badges(conn))
    if errors:
        return render_form(form_values(), errors, status=400)
    with db.transaction(conn):
        new_id = db.create_issue(conn, clean, utc_now())
    flash(f"Issue {new_id} logged.")
    return redirect(url_for("issue_detail", issue_id=new_id), code=303)


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

@app.get("/issues/<int:issue_id>/edit")
def edit_issue_form(issue_id):
    issue = db.get_issue(db.get_db(), issue_id)
    if issue is None:
        abort(404)
    values = {
        "equipment": issue.equipment_code, "title": issue.title,
        "description": issue.description, "severity": issue.severity,
        "status": issue.status, "downtime_minutes": str(issue.downtime_minutes),
        "locked_out": "yes" if issue.locked_out else "",
    }
    return render_form(values, {}, issue=issue)


@app.post("/issues/<int:issue_id>/edit")
def update_issue(issue_id):
    conn = db.get_db()
    issue = db.get_issue(conn, issue_id)
    if issue is None:
        abort(404)
    clean, errors = validate_issue(request.form, db.equipment_codes(conn),
                                   db.active_badges(conn), editing=True)
    if errors:
        return render_form(form_values(), errors, issue=issue, status=400)
    with db.transaction(conn):
        db.update_issue(conn, issue_id, clean, utc_now())
    flash(f"Issue {issue_id} updated.")
    return redirect(url_for("issue_detail", issue_id=issue_id), code=303)


@app.post("/issues/<int:issue_id>/notes")
def add_note(issue_id):
    conn = db.get_db()
    if db.get_issue(conn, issue_id) is None:
        abort(404)
    clean, errors = validate_note(request.form, db.active_badges(conn))
    if errors:
        values = {name: request.form.get(name, "") for name in ["badge", "note", "minutes_spent"]}
        return render_detail(issue_id, values, errors, status=400)
    with db.transaction(conn):
        db.add_note(conn, issue_id, clean, utc_now())
    flash("Work note added.")
    return redirect(url_for("issue_detail", issue_id=issue_id, _anchor="notes"), code=303)


# ---------------------------------------------------------------------------
# Delete: a confirmation page first, then a POST
# ---------------------------------------------------------------------------

@app.get("/issues/<int:issue_id>/delete")
def confirm_delete(issue_id):
    conn = db.get_db()
    issue = db.get_issue(conn, issue_id)
    if issue is None:
        abort(404)
    return render_template("issue_delete.html", issue=issue,
                           note_count=len(db.list_notes(conn, issue_id)))


@app.post("/issues/<int:issue_id>/delete")
def delete_issue(issue_id):
    conn = db.get_db()
    with db.transaction(conn):
        deleted = db.delete_issue(conn, issue_id)
    if not deleted:
        abort(404)
    flash(f"Issue {issue_id} and its work notes were deleted.")
    return redirect(url_for("dashboard"), code=303)


# ---------------------------------------------------------------------------
# Equipment and reports
# ---------------------------------------------------------------------------

@app.get("/equipment")
def list_equipment():
    conn = db.get_db()
    counts = {row["code"]: row["open_issues"] for row in db.report_by_equipment(conn)}
    return render_template("equipment.html", equipment=db.list_equipment(conn), counts=counts)


@app.get("/equipment/<code>")
def equipment_detail(code):
    conn = db.get_db()
    machine = db.get_equipment(conn, code)
    if machine is None:
        abort(404)
    return render_template("equipment_detail.html", machine=machine,
                           issues=db.list_issues(conn, equipment=code))


@app.get("/reports")
def reports():
    conn = db.get_db()
    closed = db.list_issues(conn, status="closed")
    return render_template("reports.html", rows=db.report_by_equipment(conn),
                           totals=db.report_totals(conn),
                           by_severity=db.report_open_by_severity(conn),
                           severities=SEVERITIES, closed=closed)


@app.get("/reports/downtime.csv")
def reports_csv():
    rows = db.report_by_equipment(db.get_db())
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\r\n")
    columns = ["code", "name", "total_issues", "open_issues", "downtime_minutes",
               "downtime_hours", "avg_downtime_minutes", "labor_hours"]
    writer.writerow(columns)
    for row in rows:
        writer.writerow([row[c] for c in columns])
    return Response(out.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=line3_downtime.csv"})


@app.get("/trace")
def trace():
    shown_headers = ["Host", "User-Agent", "Accept"]
    headers = [(name, request.headers.get(name, "(not sent)")) for name in shown_headers]
    return render_template(
        "trace.html", method=request.method, path=request.path,
        args=list(request.args.items(multi=True)), endpoint=request.endpoint,
        rule=str(request.url_rule), headers=headers,
    )


# ---------------------------------------------------------------------------
# Error pages
# ---------------------------------------------------------------------------

@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", code=400, title="That request did not make sense",
                           message=error.description), 400


@app.errorhandler(403)
def forbidden(error):
    return render_template(
        "error.html", code=403, title="That form could not be accepted",
        message="The form expired or did not come from this site. Open the form again and resend it.",
    ), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, title="Page not found",
                           message="There is no page at that address. Check the issue number."), 404


@app.errorhandler(405)
def wrong_method(error):
    return render_template("error.html", code=405, title="That address does not take that request",
                           message="Use the links and buttons on the page."), 405


# ---------------------------------------------------------------------------
# Start
# ---------------------------------------------------------------------------

def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Line 3 Maintenance Log, stage w09")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if not pathlib.Path(app.config["DATABASE_PATH"]).exists():
        print(f"No database at {app.config['DATABASE_PATH']}. "
              "Run: python manage.py init --db <path>")
        return 1
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use. Pick another or stop that server.")
        return 1
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
