"""
app.py · Line 3 Maintenance Log · Lab U05-02 STARTER · Unit 5, Week 10

Riverside Fabrication is a composite, an invented shop. Every record is invented.

Built from the course reference app (stage w10) with the parts you write in
this lab taken out. Every TODO names its lab part.

Release 1.0.0. This is the baseline: the version deployed, tagged, and
used by someone outside the class. RELEASE.md records it.

What this stage adds to w09_database:
  * create_app(), an application factory: one function builds the app from
    configuration, so tests, the local server, and the live server each get
    the settings they need (config.py)
  * every setting from the environment; SECRET_KEY required in production;
    debug never on
  * GET /health for the hosting platform to poll
  * security headers on every response, a size limit on requests, and error
    pages that never show a traceback
  * the /trace page is gone: a production app does not describe its requests
    to strangers
  * the PostgreSQL switch inside db.py [VERIFY on a lab machine]

Run it three ways:

    python app.py --port 8680            development server, SQLite
    python serve_local.py --port 8681    production-style, SQLite, no new packages
    gunicorn wsgi:app                    on Render, with PostgreSQL [VERIFY]

Why a route table instead of @app.get decorators: the decorators need an app
object when this file is imported, and a factory has no app until
create_app() runs. app.add_url_rule() is what @app.get calls underneath.
Registering from a table keeps every endpoint name the same as in w07-w09.
"""

import argparse
import csv
import io
import logging
import os
import pathlib
import socket
import sys
import time
from datetime import datetime, timezone

from flask import (Flask, Response, abort, current_app, flash, g,
                   get_flashed_messages, jsonify, redirect, render_template,
                   request, url_for)
from werkzeug.middleware.proxy_fix import ProxyFix

import db
from config import load_config
from models import SEVERITIES, STATUS_LABELS, STATUSES
from security import init_security
from validation import (BADGE_PATTERN, DESCRIPTION_MAX, DESCRIPTION_MIN,
                        DOWNTIME_MAX, NOTE_MAX, NOTE_MIN, NOTE_MINUTES_MAX,
                        NOTE_MINUTES_MIN, SEARCH_MAX, TITLE_MAX, TITLE_MIN,
                        validate_issue, validate_note, validate_search)

APP_VERSION = "1.0.0"
HERE = pathlib.Path(__file__).parent
log = logging.getLogger("line3")

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

# Sent with every response. The pages use no inline scripts or styles and load
# nothing from other sites, so the policy can be strict.
SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
        "form-action 'self'; frame-ancestors 'none'; base-uri 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "same-origin",
}


def utc_now():
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Views: read
# ---------------------------------------------------------------------------

def dashboard():
    conn = db.get_db()
    open_issues = db.list_issues(conn, open_only=True)
    critical = [i for i in open_issues if i.severity == "critical"]
    return render_template("index.html", open_issues=open_issues, critical=critical,
                           messages=get_flashed_messages())


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
# Views: create, update, delete
# ---------------------------------------------------------------------------

def render_form(values, errors, issue=None, status=200):
    return render_template("issue_form.html", equipment=db.list_equipment(db.get_db()),
                           severities=SEVERITIES, statuses=STATUSES, values=values,
                           errors=errors, issue=issue), status


def form_values():
    return {name: request.form.get(name, "") for name in
            ["reported_by", "equipment", "title", "description", "severity", "status",
             "downtime_minutes", "locked_out"]}


def new_issue_form():
    return render_form(values={}, errors={})


def create_issue():
    conn = db.get_db()
    clean, errors = validate_issue(request.form, db.equipment_codes(conn), db.active_badges(conn))
    if errors:
        return render_form(form_values(), errors, status=400)
    with db.transaction(conn):
        new_id = db.create_issue(conn, clean, utc_now())
    log.info("issue %s created", new_id)
    flash(f"Issue {new_id} logged.")
    return redirect(url_for("issue_detail", issue_id=new_id), code=303)


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
    log.info("issue %s updated", issue_id)
    flash(f"Issue {issue_id} updated.")
    return redirect(url_for("issue_detail", issue_id=issue_id), code=303)


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


def confirm_delete(issue_id):
    conn = db.get_db()
    issue = db.get_issue(conn, issue_id)
    if issue is None:
        abort(404)
    return render_template("issue_delete.html", issue=issue,
                           note_count=len(db.list_notes(conn, issue_id)))


def delete_issue(issue_id):
    conn = db.get_db()
    with db.transaction(conn):
        deleted = db.delete_issue(conn, issue_id)
    if not deleted:
        abort(404)
    log.info("issue %s deleted", issue_id)
    flash(f"Issue {issue_id} and its work notes were deleted.")
    return redirect(url_for("dashboard"), code=303)


# ---------------------------------------------------------------------------
# Views: equipment, reports, health
# ---------------------------------------------------------------------------

def list_equipment():
    conn = db.get_db()
    counts = {row["code"]: row["open_issues"] for row in db.report_by_equipment(conn)}
    return render_template("equipment.html", equipment=db.list_equipment(conn), counts=counts)


def equipment_detail(code):
    conn = db.get_db()
    machine = db.get_equipment(conn, code)
    if machine is None:
        abort(404)
    return render_template("equipment_detail.html", machine=machine,
                           issues=db.list_issues(conn, equipment=code))


def reports():
    conn = db.get_db()
    return render_template("reports.html", rows=db.report_by_equipment(conn),
                           totals=db.report_totals(conn),
                           by_severity=db.report_open_by_severity(conn),
                           severities=SEVERITIES, closed=db.list_issues(conn, status="closed"))


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


def health():
    """For the hosting platform: 200 when the app can reach its database, 503
    when it cannot. The answer names no hosts, paths, or error text."""
    try:
        db.ping(db.get_db())
    except Exception:
        current_app.logger.exception("health check: database unavailable")
        return jsonify(status="error", database="unavailable", version=APP_VERSION), 503
    return jsonify(status="ok", database="ok", version=APP_VERSION)


ROUTES = [
    # (rule, endpoint and view function, methods)
    ("/", dashboard, ["GET"]),
    ("/issues", list_issues, ["GET"]),
    ("/issues/new", new_issue_form, ["GET"]),
    ("/issues/new", create_issue, ["POST"]),
    ("/issues/<int:issue_id>", issue_detail, ["GET"]),
    ("/issues/<int:issue_id>/edit", edit_issue_form, ["GET"]),
    ("/issues/<int:issue_id>/edit", update_issue, ["POST"]),
    ("/issues/<int:issue_id>/notes", add_note, ["POST"]),
    ("/issues/<int:issue_id>/delete", confirm_delete, ["GET"]),
    ("/issues/<int:issue_id>/delete", delete_issue, ["POST"]),
    ("/equipment", list_equipment, ["GET"]),
    ("/equipment/<code>", equipment_detail, ["GET"]),
    ("/reports", reports, ["GET"]),
    ("/reports/downtime.csv", reports_csv, ["GET"]),
    ("/health", health, ["GET"]),
]


# ---------------------------------------------------------------------------
# Error pages: plain words, no tracebacks, no internals
# ---------------------------------------------------------------------------

def error_page(code, title, message):
    return render_template("error.html", code=code, title=title, message=message), code


def register_error_handlers(app):
    app.register_error_handler(400, lambda e: error_page(
        400, "That request did not make sense", e.description))
    app.register_error_handler(403, lambda e: error_page(
        403, "That form could not be accepted",
        "The form expired or did not come from this site. Open the form again and resend it."))
    app.register_error_handler(404, lambda e: error_page(
        404, "Page not found", "There is no page at that address. Check the issue number."))
    app.register_error_handler(405, lambda e: error_page(
        405, "That address does not take that request", "Use the links and buttons on the page."))
    app.register_error_handler(413, lambda e: error_page(
        413, "That form is too large", "Shorten what you typed and send it again."))
    # Flask logs the real exception before this runs. The visitor sees none of it.
    app.register_error_handler(500, lambda e: error_page(
        500, "Something went wrong on our side",
        "The error was recorded. Try again, and tell your supervisor if it keeps happening."))


# ---------------------------------------------------------------------------
# The factory
# ---------------------------------------------------------------------------

def create_app(overrides=None, environ=None):
    """Build the app. `environ` replaces os.environ (tests use this);
    `overrides` replaces individual settings after that."""
    app = Flask(__name__)
    app.config.update(load_config(environ))
    if overrides:
        app.config.update(overrides)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    db.init_app(app)
    for rule, view, methods in ROUTES:
        app.add_url_rule(rule, view.__name__, view, methods=methods)
    register_error_handlers(app)

    @app.context_processor
    def shared_template_values():
        return {"status_labels": STATUS_LABELS, "rules": RULES, "field_ids": FIELD_IDS,
                "app_version": APP_VERSION}

    @app.before_request
    def start_timer():
        g.started = time.perf_counter()

    # After start_timer, so the timer runs first and a refused POST is still timed.
    init_security(app)

    @app.after_request
    def finish(response):
        for name, value in SECURITY_HEADERS.items():
            response.headers.setdefault(name, value)
        elapsed_ms = (time.perf_counter() - g.get("started", time.perf_counter())) * 1000
        # The path only. A query string can hold whatever a person typed.
        log.info("%s %s -> %s %s (%.1f ms)", request.method, request.path,
                 request.endpoint, response.status_code, elapsed_ms)
        return response

    if app.config["TRUST_PROXY"]:
        # [VERIFY] Render sits one proxy in front of the app. ProxyFix makes
        # request.scheme and request.remote_addr reflect the visitor, not the proxy.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    return app


# ---------------------------------------------------------------------------
# Development server
# ---------------------------------------------------------------------------

def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Line 3 Maintenance Log, development server")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if os.environ.get("APP_ENV") == "production":
        print("APP_ENV is production. The development server is not for production. "
              "Use serve_local.py here, or gunicorn on the server.")
        return 1
    app = create_app()
    if not app.config["DATABASE_URL"] and not pathlib.Path(app.config["DATABASE_PATH"]).exists():
        print(f"No database at {app.config['DATABASE_PATH']}. "
              "Run: python manage.py init --db <path>")
        return 1
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use. Pick another or stop that server.")
        return 1
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
