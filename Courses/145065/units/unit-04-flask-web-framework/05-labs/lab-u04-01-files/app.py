"""
app.py · Line 3 Maintenance Log · Lab U04-01 STARTER · Unit 4, Week 7

Built from the course reference app (Line 3 Maintenance Log, stage w07) with
the parts you write in this lab taken out. Every TODO names its lab part.

Riverside Fabrication is a composite, an invented shop. Every record is invented.

What already works:
  * the request and response cycle, logged for every request (see TRACE.md)
  * the dashboard, the trace page, and the 400 and 404 error pages
  * template inheritance for the pages that exist: they extend base.html

What you write:
  * Part 2: the status filter on /issues, and the rule for /issues/<id>
  * Part 3: the two equipment pages and their templates
  * Part 4: the 503 page for a store that cannot be read, and two store checks

Run it from this folder, stating the port every time:

    python app.py --port 8680

Stop it with Ctrl+C. Point it at another store with the STORE_PATH
environment variable.

Routes:
    GET /                           dashboard: open work, most urgent first
    GET /issues                     every issue; ?status=open filters
    GET /issues/<int:issue_id>      one issue
    GET /equipment                  every machine on Line 3
    GET /equipment/<code>           one machine and its issues
    GET /trace                      what the server received for this request
"""

import argparse
import os
import pathlib
import socket
import sys
import time

from flask import Flask, abort, g, render_template, request

from models import STATUS_LABELS, STATUSES
from store import IssueStore, StoreError

HERE = pathlib.Path(__file__).parent

app = Flask(__name__)
app.config["STORE_PATH"] = os.environ.get("STORE_PATH", str(HERE / "data" / "line3_log.json"))
# Drop the blank lines template tags leave behind, so the HTML stays tidy.
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


def get_store():
    """Read the store once per request. It is small, and reading it fresh
    means an edit to the file shows up on the next page load."""
    if "store" not in g:
        g.store = IssueStore(app.config["STORE_PATH"])
    return g.store


# ---------------------------------------------------------------------------
# The request cycle, made visible
# ---------------------------------------------------------------------------

@app.before_request
def start_timer():
    g.started = time.perf_counter()


@app.after_request
def log_request(response):
    """One line per request: what came in, which function answered, what went out."""
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
    # TODO Part 2, steps 5-6: read "status" from the query string.
    #   A status the program does not know is a bad request (400), not "show nothing".
    #   Use abort(400, description="Unknown status. Use one of: ...") and list STATUSES.
    #   Pass the status to store.issues() and to the template.
    store = get_store()
    return render_template("issues.html", issues=store.issues(),
                           status=None, statuses=STATUSES, store=store)


# TODO Part 2, steps 3-4: this rule answers, but every issue comes back 404.
#   Read the [trace] line, then fix the rule, not the function body.
@app.get("/issues/<issue_id>")
def issue_detail(issue_id):
    store = get_store()
    issue = store.get_issue(issue_id)
    if issue is None:
        abort(404)
    return render_template("issue_detail.html", issue=issue,
                           machine=store.get_equipment(issue.equipment),
                           reporter=store.get_technician(issue.reported_by))


@app.get("/equipment")
def list_equipment():
    # TODO Part 3, steps 7-9: count the OPEN issues for each machine in ONE pass
    #   over store.open_issues(), then render templates/equipment.html with
    #   equipment=store.all_equipment() and counts={code: number}.
    return "The equipment page is not built yet. Lab U04-01, Part 3."


@app.get("/equipment/<code>")
def equipment_detail(code):
    # TODO Part 3, steps 10-11: look the machine up with store.get_equipment(code).
    #   No machine is a 404. Otherwise render templates/equipment_detail.html with
    #   machine, issues=store.issues(equipment=code), and store.
    #   Never put `code` into this return string: it is text the visitor typed.
    return "The machine page is not built yet. Lab U04-01, Part 3."


@app.get("/trace")
def trace():
    """Show the request as Flask sees it. No cookies, no personal data."""
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


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, title="Page not found",
                           message="There is no page at that address. Check the issue number."), 404


# TODO Part 4, steps 13-14: register a handler for StoreError.
#   Print the error type and message to sys.stderr, starting with "[store] ".
#   Answer with templates/error.html, code 503, the title
#   "The maintenance log is unavailable", and a message that tells the user what
#   to do. Never put the error's text on the page.


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
    parser = argparse.ArgumentParser(description="Line 3 Maintenance Log, Lab U04-01")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use. Pick another or stop that server.")
        return 1
    # debug stays off: the debugger lets anyone who reaches the page run code.
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
