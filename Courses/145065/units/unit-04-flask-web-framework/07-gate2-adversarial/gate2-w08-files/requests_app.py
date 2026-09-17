r"""
requests_app.py · Line 3 Parts Request · Flask

Riverside Fabrication is a composite, an invented shop. Every record is invented.

A technician requests a replacement part on a form. The board shows open
requests. A request writes to a JSON file.

Run it against a copy of the store, stating the port every time:

    set STORE_PATH=%TEMP%\parts_copy.json
    python requests_app.py --port 8685
"""

import argparse
import json
import os
import pathlib
import secrets
import socket
import sys

from flask import (Flask, abort, g, redirect, render_template, request,
                   session, url_for)

HERE = pathlib.Path(__file__).parent
PRIORITIES = ("routine", "soon", "urgent")   # in order of urgency, most urgent first
TITLE_MIN, TITLE_MAX = 5, 60
QTY_MAX = 99

app = Flask(__name__)
app.config["STORE_PATH"] = os.environ.get("STORE_PATH", str(HERE / "data" / "requests.json"))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


def load_store():
    return json.loads(pathlib.Path(app.config["STORE_PATH"]).read_text(encoding="utf-8"))


def parts():
    return {p["number"]: p for p in load_store()["parts"]}


def open_requests():
    return [r for r in load_store()["requests"] if not r["filled"]]


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


def validate(form, part_numbers):
    """Return (clean, errors). errors is a field -> message dict."""
    errors, clean = {}, {}
    number = (form.get("part") or "").strip().upper()
    if number not in part_numbers:
        errors["part"] = "Choose a part from the list."
    clean["part"] = number

    title = (form.get("title") or "").strip()
    if not TITLE_MIN <= len(title) < TITLE_MAX:
        errors["title"] = f"Write a short reason, {TITLE_MIN} to {TITLE_MAX} characters."
    clean["title"] = title

    raw = (form.get("quantity") or "").strip()
    if not raw.isdecimal() or not 1 <= int(raw) <= QTY_MAX:
        errors["quantity"] = f"Enter a quantity from 1 to {QTY_MAX}."
        clean["quantity"] = None
    else:
        clean["quantity"] = int(raw)

    priority = form.get("priority") or ""
    if priority not in PRIORITIES:
        errors["priority"] = "Choose a priority."
    clean["priority"] = priority

    # A note is optional context for the storeroom.
    clean["note"] = (form.get("note") or "").strip()
    return clean, errors


@app.get("/")
def board():
    reqs = open_requests()
    # Show each request with the part's name, looked up from the parts list.
    rows = []
    for req in reqs:
        name = parts().get(req["part"], {}).get("name", "unknown")
        rows.append({"request": req, "part_name": name})
    return render_template("index.html", rows=rows)


@app.get("/requests/new")
def new_request():
    return render_template("form.html", parts=parts().values(), priorities=PRIORITIES,
                           values={}, errors={})


@app.post("/requests/new")
def create_request():
    store = load_store()
    clean, errors = validate(request.form, set(parts()))
    if errors:
        return render_template("form.html", parts=parts().values(), priorities=PRIORITIES,
                               values=request.form, errors=errors), 400
    new_id = max((r["id"] for r in store["requests"]), default=0) + 1
    store["requests"].append({"id": new_id, "part": clean["part"], "title": clean["title"],
                              "quantity": clean["quantity"], "priority": clean["priority"],
                              "note": clean["note"], "filled": False})
    pathlib.Path(app.config["STORE_PATH"]).write_text(json.dumps(store, indent=2), encoding="utf-8")
    return render_template("thanks.html", request_id=new_id)


@app.get("/requests/<int:request_id>")
def request_detail(request_id):
    for req in load_store()["requests"]:
        if req["id"] == request_id:
            return render_template("request.html", req=req,
                                   part=parts().get(req["part"]))
    abort(404)


@app.errorhandler(403)
def forbidden(error):
    return render_template("error.html", code=403, message="That form could not be accepted."), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, message="No page at that address."), 404


def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Line 3 Parts Request")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use.")
        return 1
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
