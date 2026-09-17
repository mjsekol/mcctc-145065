"""
board.py · Line 3 Shift Handoff Board · Flask

Riverside Fabrication is a composite, an invented shop. Every record is invented.

Technicians leave notes for the next shift about the machines on Line 3. The
board shows open notes, most urgent first. A supervisor opens one machine to see
its notes.

Run it, stating the port every time:

    python board.py --port 8685
"""

import argparse
import pathlib
import socket
import sys

from flask import Flask, abort, g, render_template, request

HERE = pathlib.Path(__file__).parent
SEVERITIES = ("info", "watch", "urgent")

app = Flask(__name__)
app.config["NOTES_PATH"] = str(HERE / "data" / "notes.json")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


class BoardError(Exception):
    """Anything wrong with the notes file."""


class Board:
    """Reads the shift-note file and answers questions about it."""

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self._machines = {}
        self._notes = {}
        self.load()

    def load(self):
        import json
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise BoardError(f"No notes file at {self.path}") from None
        except json.JSONDecodeError as error:
            raise BoardError(f"Notes file is not valid JSON: {error}") from None
        machines = {m["code"]: m for m in raw["machines"]}
        notes = {}
        for rec in raw["notes"]:
            if rec["machine"] not in machines:
                raise BoardError(f"note {rec['id']} names unknown machine {rec['machine']}")
            notes[rec["id"]] = rec
        self._machines, self._notes = machines, notes

    def all_machines(self):
        return [self._machines[c] for c in sorted(self._machines)]

    def get_machine(self, code):
        return self._machines.get(code)

    def get_note(self, note_id):
        return self._notes.get(note_id)

    def urgent_notes(self):
        """Open notes, most urgent first."""
        notes = [n for n in self._notes.values() if not n["cleared"]]
        # Oldest handoff first within a severity, so nothing waits unseen.
        notes.sort(key=lambda n: n["left_at"])
        notes.sort(key=lambda n: SEVERITIES.index(n["severity"]))
        return notes

    def notes_for(self, code):
        return [n for n in self._notes.values() if n["machine"] == code]


def get_board():
    if "board" not in g:
        g.board = Board(app.config["NOTES_PATH"])
    return g.board


@app.get("/")
def board_page():
    board = get_board()
    notes = board.urgent_notes()
    return render_template("index.html", notes=notes, board=board)


@app.get("/notes/<int:note_id>")
def note_detail(note_id):
    board = get_board()
    note = board.get_note(note_id)
    if note is None:
        abort(404)
    return render_template("note.html", note=note,
                           machine=board.get_machine(note["machine"]))


@app.get("/machines")
def machine_list():
    board = get_board()
    # How many open notes does each machine have?
    counts = {}
    for machine in board.all_machines():
        open_here = [n for n in board.urgent_notes() if n["machine"] == machine["code"]]
        counts[machine["code"]] = len(open_here)
    return render_template("machines.html", machines=board.all_machines(), counts=counts)


@app.get("/machines/<code>")
def machine_detail(code):
    board = get_board()
    machine = board.get_machine(code)
    if machine is None:
        abort(404)
    return render_template("machine.html", machine=machine, notes=board.notes_for(code))


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, message="No page at that address."), 404


@app.errorhandler(BoardError)
def board_unavailable(error):
    return render_template("error.html", code=503, message=str(error)), 503


def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Line 3 Shift Handoff Board")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    if not port_is_free(args.port):
        print(f"Port {args.port} is already in use.")
        return 1
    app.run(host="127.0.0.1", port=args.port, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
