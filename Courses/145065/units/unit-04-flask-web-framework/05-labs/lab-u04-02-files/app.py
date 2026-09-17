"""
app.py · Line 3 Maintenance Log · Lab U04-02 STARTER · Unit 4, Week 8

Built from the course reference app (Line 3 Maintenance Log, stage w08) with
the parts you write in this lab taken out. Every TODO names its lab part.

Riverside Fabrication is a composite, an invented shop. Every record is invented.

What already works: every Week 7 page, the blank form at GET /issues/new,
the store's add_issue() with a backup before every write, and the error pages.

What you write:
  * Part 1: create_issue, the POST half of the form, with Post/Redirect/Get
  * Part 2: every rule in validation.py
  * Part 3: find the template that shows typed text without escaping
  * Part 4: check_csrf in security.py

Run it from this folder, stating the port every time:

    python app.py --port 8680

The form writes to the store. To keep the canonical data/line3_log.json
unchanged, point the server at a copy:

    set STORE_PATH=C:\\path\\to\\copy\\line3_log.json        (Command Prompt)
    $env:STORE_PATH = "C:\\path\\to\\copy\\line3_log.json"   (PowerShell)

SECRET_KEY signs the session cookie. Set it in the environment. If it is
missing, this stage makes a random one for this run and says so; every session
ends when the server stops. Week 10 makes it required in production.

Routes:
    GET  /                          dashboard: open work, most urgent first
    GET  /issues                    every issue; ?status=open filters
    GET  /issues/new                the blank form
    POST /issues/new                check, save, redirect; or the form again with errors
    GET  /issues/<int:issue_id>     one issue
    GET  /equipment                 every machine on Line 3
    GET  /equipment/<code>          one machine and its issues
    GET  /trace                     what the server received for this request
"""

import argparse
import os
import pathlib
import secrets
import socket
import sys
import time

from flask import (Flask, abort, flash, g, get_flashed_messages, redirect,
                   render_template, request, url_for)

from models import SEVERITIES, STATUS_LABELS, STATUSES
from security import init_security
from store import IssueStore, StoreError
from validation import (BADGE_PATTERN, DESCRIPTION_MAX, DESCRIPTION_MIN,
                        DOWNTIME_MAX, TITLE_MAX, TITLE_MIN, validate_issue)

HERE = pathlib.Path(__file__).parent

app = Flask(__name__)
app.config["STORE_PATH"] = os.environ.get("STORE_PATH", str(HERE / "data" / "line3_log.json"))
if os.environ.get("SECRET_KEY"):
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
else:
    app.config["SECRET_KEY"] = secrets.token_hex(32)
    print("[config] SECRET_KEY is not set. Using a random key for this run only.",
          file=sys.stderr, flush=True)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Which element each error message links to.
FIELD_IDS = {
    "reported_by": "reported-by",
    "equipment": "equipment",
    "title": "title",
    "description": "description",
    "severity": "severity-low",
    "downtime_minutes": "downtime-minutes",
    "locked_out": "locked-out",
}

# The rule values the form's hints are built from. Same numbers as the server.
FORM_RULES = {
    "badge_pattern": BADGE_PATTERN,
    "title_min": TITLE_MIN, "title_max": TITLE_MAX,
    "description_min": DESCRIPTION_MIN, "description_max": DESCRIPTION_MAX,
    "downtime_max": DOWNTIME_MAX,
}


def get_store():
    if "store" not in g:
        g.store = IssueStore(app.config["STORE_PATH"])
    return g.store


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
    return {"status_labels": STATUS_LABELS}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def dashboard():
    store = get_store()
    open_issues = store.open_issues()
    critical = [i for i in open_issues if i.severity == "critical"]
    return render_template("index.html", open_issues=open_issues, critical=critical,
                           store=store)


@app.get("/issues")
def list_issues():
    status = request.args.get("status")
    if status is not None and status not in STATUSES:
        abort(400, description=f"Unknown status. Use one of: {', '.join(STATUSES)}.")
    store = get_store()
    return render_template("issues.html", issues=store.issues(status=status),
                           status=status, statuses=STATUSES, store=store)


def render_form(values, errors, status=200):
    return render_template("issue_form.html", equipment=get_store().all_equipment(),
                           severities=SEVERITIES, values=values, errors=errors,
                           field_ids=FIELD_IDS, rules=FORM_RULES), status


@app.get("/issues/new")
def new_issue_form():
    return render_form(values={}, errors={})


@app.post("/issues/new")
def create_issue():
    # TODO Part 1, steps 3-7. In this order:
    #   1. store = get_store()
    #   2. clean, errors = validate_issue(request.form, store.equipment_codes(), store.badges())
    #   3. If there are errors, answer render_form(values, errors, status=400), where
    #      values = {name: request.form.get(name, "") for name in FIELD_IDS}
    #      so the person gets their answers back.
    #   4. Otherwise new_id = store.add_issue(clean)
    #   5. flash(f"Issue {new_id} logged. Thank you.")
    #   6. Redirect to the new issue's page with code 303 (Post/Redirect/Get).
    return render_form(values={}, errors={}, status=501)


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    store = get_store()
    issue = store.get_issue(issue_id)
    if issue is None:
        abort(404)
    return render_template("issue_detail.html", issue=issue,
                           machine=store.get_equipment(issue.equipment),
                           reporter=store.get_technician(issue.reported_by),
                           messages=get_flashed_messages())


@app.get("/equipment")
def list_equipment():
    store = get_store()
    # One pass over the open issues, not one pass per machine.
    counts = {e.code: 0 for e in store.all_equipment()}
    for issue in store.open_issues():
        counts[issue.equipment] += 1
    return render_template("equipment.html", equipment=store.all_equipment(), counts=counts)


@app.get("/equipment/<code>")
def equipment_detail(code):
    store = get_store()
    machine = store.get_equipment(code)
    if machine is None:
        abort(404)
    return render_template("equipment_detail.html", machine=machine,
                           issues=store.issues(equipment=code), store=store)


@app.get("/trace")
def trace():
    shown_headers = ["Host", "User-Agent", "Accept"]
    headers = [(name, request.headers.get(name, "(not sent)")) for name in shown_headers]
    return render_template(
        "trace.html",
        method=request.method,
        path=request.path,
        args=list(request.args.items(multi=True)),
        endpoint=request.endpoint,
        rule=str(request.url_rule),
        headers=headers,
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


@app.errorhandler(StoreError)
def store_unavailable(error):
    print(f"[store] {type(error).__name__}: {error}", file=sys.stderr, flush=True)
    return render_template("error.html", code=503, title="The maintenance log is unavailable",
                           message="The log file could not be read. Tell your supervisor."), 503


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
    parser = argparse.ArgumentParser(description="Line 3 Maintenance Log, Lab U04-02")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use. Pick another or stop that server.")
        return 1
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
