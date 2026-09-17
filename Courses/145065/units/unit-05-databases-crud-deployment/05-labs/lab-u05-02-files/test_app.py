"""
test_app.py · Lab U05-02, from the reference stage w10 · the w09 suite, carried forward · run from this folder:

    python -m unittest -v

Every test builds a fresh database in a temporary folder from schema.sql and
seed.sql. No test touches instance/line3.db. Deployment checks are in
test_deploy.py. Standard library plus Flask's
test client.
"""

import contextlib
import io
import pathlib
import re
import sqlite3
import tempfile
import unittest

import db
import import_csv
import manage
from app import create_app
from validation import (DOWNTIME_MAX, NOTE_MINUTES_MAX, NOTE_MINUTES_MIN,
                        TITLE_MAX, TITLE_MIN, validate_import_row)

HERE = pathlib.Path(__file__).parent
TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')

GOOD = {
    "reported_by": "T-1041",
    "equipment": "PB-02",
    "title": "Ram stalls mid-stroke",
    "description": "The ram stops halfway on thick parts and the pump whines.",
    "severity": "high",
    "downtime_minutes": "30",
}
HEADER = ("equipment_code,reported_by,title,description,severity,status,"
          "downtime_minutes,locked_out,reported_at,closed_at\n")


class TempDatabase(unittest.TestCase):
    """Base class: a new seeded database for every test."""

    def setUp(self):
        # Cleanups run last-in, first-out. The folder is registered first so it
        # is removed last, after every connection below has closed. Windows
        # refuses to delete a database file that is still open.
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db_path = pathlib.Path(self.tmp.name) / "test.db"
        db.create_database(self.db_path)
        self.app = create_app(
            overrides={"TESTING": True, "DATABASE_PATH": str(self.db_path)},
            environ={"APP_ENV": "test", "SECRET_KEY": "test-only-not-a-real-secret"},
        )
        self.client = self.app.test_client()
        quiet = contextlib.redirect_stdout(io.StringIO())
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)

    def conn(self):
        conn = db.connect_path(self.db_path)
        self.addCleanup(conn.close)
        return conn

    def count(self, table):
        return db.table_counts(self.conn())[table]

    def page(self, url, status=200):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status, url)
        return response.get_data(as_text=True)

    def token(self):
        return TOKEN.search(self.page("/issues/new")).group(1)

    def post(self, url, data, token=True):
        data = dict(data)
        if token:
            data["csrf_token"] = self.token()
        return self.client.post(url, data=data)

    def edit_values(self, **changes):
        values = {"equipment": "PB-01", "title": "Back gauge drifts 2 mm after warm-up",
                  "description": "Parts from the second hour measure long.",
                  "severity": "medium", "status": "open", "downtime_minutes": "25"}
        values.update(changes)
        return values


# ---------------------------------------------------------------------------
# The schema
# ---------------------------------------------------------------------------

class SchemaTests(TempDatabase):
    def test_four_related_tables(self):
        self.assertEqual(db.table_names(self.conn()),
                         ["equipment", "issues", "technicians", "work_notes"])

    def test_seed_counts(self):
        self.assertEqual(db.table_counts(self.conn()),
                         {"equipment": 6, "issues": 7, "technicians": 4, "work_notes": 5})

    def test_foreign_keys_are_declared(self):
        conn = self.conn()
        issues_fk = {(r["from"], r["table"]) for r in conn.execute("PRAGMA foreign_key_list(issues)")}
        notes_fk = {(r["from"], r["table"], r["on_delete"])
                    for r in conn.execute("PRAGMA foreign_key_list(work_notes)")}
        self.assertEqual(issues_fk, {("equipment_id", "equipment"), ("reported_by", "technicians")})
        self.assertIn(("issue_id", "issues", "CASCADE"), notes_fk)

    def test_a_machine_with_issues_cannot_be_deleted(self):
        conn = self.conn()
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("DELETE FROM equipment WHERE code = 'OV-01'")

    def test_an_issue_cannot_point_at_a_missing_machine(self):
        conn = self.conn()
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("UPDATE issues SET equipment_id = 999 WHERE id = 1")

    def test_the_database_enforces_the_lockout_rule(self):
        conn = self.conn()
        with self.assertRaisesRegex(sqlite3.IntegrityError, "CHECK"):
            conn.execute("UPDATE issues SET severity = 'critical', locked_out = 0 WHERE id = 1")

    def test_the_database_enforces_closed_at(self):
        conn = self.conn()
        with self.assertRaisesRegex(sqlite3.IntegrityError, "CHECK"):
            conn.execute("UPDATE issues SET status = 'closed' WHERE id = 1")

    def test_badges_are_unique(self):
        conn = self.conn()
        with self.assertRaisesRegex(sqlite3.IntegrityError, "UNIQUE"):
            conn.execute("INSERT INTO technicians (badge, display_name, role) "
                         "VALUES ('T-1041', 'Someone Else', 'technician')")

    def test_schema_limits_match_validation(self):
        schema = (HERE / "schema.sql").read_text(encoding="utf-8")
        self.assertIn(f"downtime_minutes BETWEEN 0 AND {DOWNTIME_MAX}", schema)
        self.assertIn(f"minutes_spent BETWEEN {NOTE_MINUTES_MIN} AND {NOTE_MINUTES_MAX}", schema)

    def test_no_personal_fields_in_technicians(self):
        cols = [r["name"] for r in self.conn().execute("PRAGMA table_info(technicians)")]
        self.assertEqual(cols, ["id", "badge", "display_name", "role", "active"])

    def test_only_db_py_touches_sqlite(self):
        offenders = []
        for path in HERE.glob("*.py"):
            if path.name == "db.py" or path.name.startswith("test_"):
                continue
            text = path.read_text(encoding="utf-8")
            if "sqlite3" in text or ".execute(" in text:
                offenders.append(path.name)
        self.assertEqual(offenders, [])


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

class ReadTests(TempDatabase):
    def test_pages_answer(self):
        for url in ["/", "/issues", "/issues/new", "/issues/3", "/issues/3/edit",
                    "/issues/3/delete", "/equipment", "/equipment/OV-01", "/reports", "/health"]:
            with self.subTest(url=url):
                self.page(url)

    def test_dashboard_lists_open_work_most_urgent_first(self):
        body = self.page("/")
        self.assertIn("5 open issues", body)
        order = [body.index(f'href="/issues/{n}"') for n in (3, 5, 2, 1, 6)]
        self.assertEqual(order, sorted(order))

    def test_detail_joins_three_tables(self):
        body = self.page("/issues/3")
        self.assertIn("CV-01 Transfer Conveyor", body)
        self.assertIn("Priya Castellano (T-1062)", body)
        self.assertIn("2 notes, 35 minutes of work", body)
        self.assertIn("Morgan Healey (S-2003)", body)

    def test_closed_issue_shows_time_to_close(self):
        self.assertIn("3.5 hours after it was reported", self.page("/issues/7"))

    def test_filters_combine(self):
        body = self.page("/issues?status=closed&equipment=OV-01")
        self.assertIn("1 matching issue", body)
        self.assertIn("Exhaust fan belt squeal", body)

    def test_search_is_case_insensitive(self):
        body = self.page("/issues?q=THERMOCOUPLE")
        self.assertIn("No issues match.", body)  # the word is in a note, not an issue
        body = self.page("/issues?q=GUARD")
        self.assertIn("1 matching issue", body)

    def test_unknown_filter_values_are_bad_requests(self):
        self.page("/issues?status=everything", status=400)
        self.page("/issues?equipment=ZZ-99", status=400)

    def test_missing_things_are_404(self):
        for url in ["/issues/999", "/issues/999/edit", "/issues/999/delete", "/equipment/ZZ-99"]:
            with self.subTest(url=url):
                self.page(url, status=404)

    def test_equipment_counts_come_from_the_database(self):
        body = self.page("/equipment")
        row = body[body.index('href="/equipment/LC-01"'):]
        self.assertIn('<td class="num">0</td>', row[:row.index("</tr>")])


# ---------------------------------------------------------------------------
# Create, update, delete
# ---------------------------------------------------------------------------

class WriteTests(TempDatabase):
    def test_create(self):
        response = self.post("/issues/new", GOOD)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["Location"], "/issues/8")
        body = self.page("/issues/8")
        self.assertIn("Issue 8 logged.", body)
        self.assertIn("Dana Okafor (T-1041)", body)
        self.assertEqual(self.count("issues"), 8)

    def test_create_refuses_bad_input_and_writes_nothing(self):
        response = self.post("/issues/new", dict(GOOD, title="abc", reported_by="T-9999"))
        self.assertEqual(response.status_code, 400)
        body = response.get_data(as_text=True)
        self.assertIn("There are 2 problems", body)
        self.assertIn(f"between {TITLE_MIN} and {TITLE_MAX}", body)
        self.assertIn("not on the Line 3 list", body)
        self.assertEqual(self.count("issues"), 7)

    def test_an_inactive_badge_cannot_log(self):
        conn = self.conn()
        conn.execute("UPDATE technicians SET active = 0 WHERE badge = 'T-1041'")
        conn.commit()
        response = self.post("/issues/new", GOOD)
        self.assertEqual(response.status_code, 400)

    def test_update_changes_the_row(self):
        response = self.post("/issues/1/edit", self.edit_values(title="Back gauge drifts 3 mm",
                                                                 downtime_minutes="40"))
        self.assertEqual(response.status_code, 303)
        issue = db.get_issue(self.conn(), 1)
        self.assertEqual(issue.title, "Back gauge drifts 3 mm")
        self.assertEqual(issue.downtime_minutes, 40)
        self.assertEqual(issue.reporter_badge, "T-1041")  # the reporter never changes

    def test_closing_stamps_closed_at_once_and_reopening_clears_it(self):
        self.post("/issues/1/edit", self.edit_values(status="closed"))
        first = db.get_issue(self.conn(), 1).closed_at
        self.assertIsNotNone(first)
        conn = self.conn()
        conn.execute("UPDATE issues SET closed_at = '2025-11-10T12:00:00Z' WHERE id = 1")
        conn.commit()
        self.post("/issues/1/edit", self.edit_values(status="closed", title="Still closed, renamed"))
        self.assertEqual(db.get_issue(self.conn(), 1).closed_at.isoformat(), "2025-11-10T12:00:00+00:00")
        self.post("/issues/1/edit", self.edit_values(status="open"))
        self.assertIsNone(db.get_issue(self.conn(), 1).closed_at)

    def test_update_refuses_critical_without_lockout(self):
        response = self.post("/issues/1/edit", self.edit_values(severity="critical"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("locked out first", response.get_data(as_text=True))
        self.assertEqual(db.get_issue(self.conn(), 1).severity, "medium")

    def test_update_refuses_an_unknown_status(self):
        response = self.post("/issues/1/edit", self.edit_values(status="done"))
        self.assertEqual(response.status_code, 400)

    def test_edit_form_is_filled_in(self):
        body = self.page("/issues/3/edit")
        self.assertIn('<option value="CV-01" selected>', body)
        self.assertIn('value="critical" required checked', body)
        self.assertIn('name="locked_out" type="checkbox" value="yes" checked', body)
        self.assertNotIn('name="reported_by"', body)

    def test_add_note(self):
        response = self.post("/issues/1/notes", {"badge": "t-1057", "note": "Re-zeroed the gauge.",
                                                 "minutes_spent": "15"})
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["Location"], "/issues/1#notes")
        body = self.page("/issues/1")
        self.assertIn("Re-zeroed the gauge.", body)
        self.assertIn("Luis Brennan (T-1057)", body)

    def test_bad_note_is_refused_with_the_issue_page(self):
        response = self.post("/issues/1/notes", {"badge": "T-1057", "note": "ok",
                                                 "minutes_spent": "0"})
        self.assertEqual(response.status_code, 400)
        body = response.get_data(as_text=True)
        self.assertIn("<title>Error: Issue 1", body)
        self.assertIn("There are 2 problems with this note", body)
        self.assertEqual(self.count("work_notes"), 5)

    def test_note_on_a_missing_issue_is_404(self):
        response = self.post("/issues/999/notes", {"badge": "T-1057", "note": "Nothing here",
                                                   "minutes_spent": "5"})
        self.assertEqual(response.status_code, 404)

    def test_delete_asks_first_and_get_deletes_nothing(self):
        body = self.page("/issues/3/delete")
        self.assertIn("and its 2 work notes", body)
        self.assertIn("This cannot be undone.", body)
        self.assertEqual(self.count("issues"), 7)

    def test_delete_removes_the_issue_and_its_notes(self):
        response = self.post("/issues/3/delete", {})
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["Location"], "/")
        self.assertIn("Issue 3 and its work notes were deleted.", self.page("/"))
        self.assertEqual(self.count("issues"), 6)
        self.assertEqual(self.count("work_notes"), 3)
        self.page("/issues/3", status=404)

    def test_delete_of_a_missing_issue_is_404(self):
        self.assertEqual(self.post("/issues/999/delete", {}).status_code, 404)

    def test_every_write_needs_the_token(self):
        cases = [("/issues/new", GOOD), ("/issues/1/edit", self.edit_values()),
                 ("/issues/1/notes", {"badge": "T-1057", "note": "Forged note", "minutes_spent": "5"}),
                 ("/issues/1/delete", {})]
        for url, data in cases:
            with self.subTest(url=url):
                self.assertEqual(self.post(url, data, token=False).status_code, 403)
        self.assertEqual(db.table_counts(self.conn()),
                         {"equipment": 6, "issues": 7, "technicians": 4, "work_notes": 5})

    def test_a_failed_write_rolls_back(self):
        conn = self.conn()
        with self.assertRaises(sqlite3.IntegrityError):
            with db.transaction(conn):
                db.add_note(conn, 1, {"badge": "T-1041", "note": "first", "minutes_spent": 5},
                            now=db_now())
                db.add_note(conn, 1, {"badge": "T-1041", "note": "second", "minutes_spent": 5000},
                            now=db_now())
        self.assertEqual(self.count("work_notes"), 5)


def db_now():
    from datetime import datetime, timezone
    return datetime(2025, 11, 12, 8, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Injection: typed text is always data
# ---------------------------------------------------------------------------

class InjectionTests(TempDatabase):
    ATTACKS = ["' OR '1'='1", "'; DROP TABLE issues; --", '" OR ""="', "%", "_", "\\"]

    def test_search_attacks_match_nothing_and_break_nothing(self):
        for attack in self.ATTACKS:
            with self.subTest(attack=attack):
                body = self.page("/issues?q=" + attack.replace("%", "%25").replace(";", "%3B")
                                 .replace("'", "%27").replace('"', "%22").replace(" ", "+")
                                 .replace("\\", "%5C"))
                self.assertIn("No issues match.", body)
        self.assertEqual(self.count("issues"), 7)

    def test_a_percent_sign_is_searched_literally(self):
        self.post("/issues/new", dict(GOOD, title="Coolant at 100% on the gauge"))
        body = self.page("/issues?q=100%25")
        self.assertIn("1 matching issue", body)

    def test_sql_in_a_title_is_stored_as_text(self):
        attack = "x'); DELETE FROM issues; --"
        response = self.post("/issues/new", dict(GOOD, title=attack))
        self.assertEqual(response.status_code, 303)
        self.assertEqual(self.count("issues"), 8)
        self.assertEqual(db.get_issue(self.conn(), 8).title, attack)

    def test_script_in_a_note_is_escaped(self):
        self.post("/issues/1/notes", {"badge": "T-1057", "note": "<script>alert(1)</script>",
                                      "minutes_spent": "5"})
        body = self.page("/issues/1")
        self.assertNotIn("<script>alert(1)</script>", body)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", body)

    def test_the_id_in_the_url_must_be_a_number(self):
        self.page("/issues/1%20OR%201=1", status=404)


# ---------------------------------------------------------------------------
# Reports: calculated fields, checked against hand-worked numbers
# ---------------------------------------------------------------------------

class ReportTests(TempDatabase):
    def test_by_equipment_matches_hand_calculation(self):
        rows = [(r["code"], r["total_issues"], r["open_issues"], r["downtime_minutes"],
                 r["downtime_hours"], r["avg_downtime_minutes"], r["labor_hours"])
                for r in db.report_by_equipment(self.conn())]
        self.assertEqual(rows, [
            ("CV-01", 1, 1, 90, 1.5, 90.0, 0.6),   # labor 20 + 15 = 35 min
            ("OV-01", 2, 1, 75, 1.3, 37.5, 1.3),   # 75/60 = 1.25, rounded half away from zero
            ("WR-01", 1, 1, 40, 0.7, 40.0, 0.0),
            ("PB-01", 1, 1, 25, 0.4, 25.0, 0.0),
            ("LC-01", 1, 0, 0, 0.0, 0.0, 0.8),     # labor 45 min
            ("PB-02", 1, 1, 0, 0.0, 0.0, 0.0),
        ])

    def test_labor_does_not_double_count_downtime(self):
        # OV-01 has one note on issue 2 (30 min) and one on issue 7 (50 min).
        # A second note on issue 2 adds labor. Downtime must not change.
        conn = self.conn()
        with db.transaction(conn):
            db.add_note(conn, 2, {"badge": "T-1057", "note": "Checked wiring", "minutes_spent": 40},
                        now=db_now())
        ov = [r for r in db.report_by_equipment(conn) if r["code"] == "OV-01"][0]
        self.assertEqual(ov["downtime_minutes"], 75)
        self.assertEqual(ov["labor_hours"], 2.0)

    def test_totals(self):
        self.assertEqual(db.report_totals(self.conn()),
                         {"total_issues": 7, "open_issues": 5, "downtime_hours": 3.8,
                          "labor_hours": 2.7})

    def test_totals_on_an_empty_database(self):
        empty = pathlib.Path(self.tmp.name) / "empty.db"
        db.create_database(empty, seed=False)
        conn = db.connect_path(empty)
        self.addCleanup(conn.close)
        self.assertEqual(db.report_totals(conn),
                         {"total_issues": 0, "open_issues": 0, "downtime_hours": 0.0,
                          "labor_hours": 0.0})

    def test_open_by_severity(self):
        self.assertEqual(db.report_open_by_severity(self.conn()),
                         {"critical": 1, "high": 2, "medium": 1, "low": 1})

    def test_report_page(self):
        body = self.page("/reports")
        self.assertIn("All of Line 3", body)
        self.assertIn('<td class="num">3.8</td>', body)
        self.assertIn('<td class="num">20.0</td>', body)  # issue 4 closed in 20 hours
        self.assertIn('<td class="num">3.5</td>', body)   # issue 7 in 3.5 hours

    def test_csv_export(self):
        response = self.client.get("/reports/downtime.csv")
        self.assertEqual(response.mimetype, "text/csv")
        self.assertIn("attachment", response.headers["Content-Disposition"])
        lines = response.get_data(as_text=True).splitlines()
        self.assertEqual(lines[0], "code,name,total_issues,open_issues,downtime_minutes,"
                                   "downtime_hours,avg_downtime_minutes,labor_hours")
        self.assertEqual(lines[1], "CV-01,Transfer Conveyor,1,1,90,1.5,90.0,0.6")
        self.assertEqual(len(lines), 7)


# ---------------------------------------------------------------------------
# CSV import and the command-line tools
# ---------------------------------------------------------------------------

class ImportTests(TempDatabase):
    def run_import(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = import_csv.main([*args, "--db", str(self.db_path)])
        return code, out.getvalue()

    def write_csv(self, text, encoding="utf-8"):
        path = pathlib.Path(self.tmp.name) / "import.csv"
        path.write_text(text, encoding=encoding)
        return str(path)

    def test_good_file_imports_every_row(self):
        code, out = self.run_import(str(HERE / "data" / "issues_import.csv"))
        self.assertEqual(code, 0)
        self.assertIn("Imported 4 issue(s): ids 8 to 11.", out)
        self.assertEqual(self.count("issues"), 11)
        closed = db.get_issue(self.conn(), 11)
        self.assertEqual(closed.status, "closed")
        self.assertEqual(closed.hours_to_close, 0.5)

    def test_bad_file_imports_nothing_and_names_every_line(self):
        code, out = self.run_import(str(HERE / "data" / "issues_import_bad.csv"))
        self.assertEqual(code, 1)
        self.assertEqual(self.count("issues"), 7)
        for expected in ["line 3: equipment", "line 4: locked_out", "line 5: closed_at",
                         "line 6: downtime_minutes"]:
            self.assertIn(expected, out)
        self.assertNotIn("line 2:", out)

    def test_dry_run_imports_nothing(self):
        code, out = self.run_import(str(HERE / "data" / "issues_import.csv"), "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("all 4 row(s) are valid", out)
        self.assertEqual(self.count("issues"), 7)

    def test_excel_byte_order_mark_is_handled(self):
        path = self.write_csv(HEADER + "PB-02,T-1041,Guard latch sticks,The guard latch needs "
                              "two hands to open.,low,open,0,no,2025-11-12T10:00:00Z,\n",
                              encoding="utf-8-sig")
        code, _ = self.run_import(path)
        self.assertEqual(code, 0)
        self.assertEqual(self.count("issues"), 8)

    def test_missing_column_is_reported(self):
        path = self.write_csv("equipment_code,title\nPB-01,Something\n")
        code, out = self.run_import(path)
        self.assertEqual(code, 1)
        self.assertIn("missing column(s) reported_by", out)

    def test_import_row_time_rules(self):
        base = {"equipment_code": "PB-01", "reported_by": "T-1041", "title": "Valid title",
                "description": "A valid description.", "severity": "low", "status": "closed",
                "downtime_minutes": "0", "locked_out": "no",
                "reported_at": "2025-11-12T10:00:00Z", "closed_at": "2025-11-12T09:00:00Z"}
        codes, badges = {"PB-01"}, {"T-1041"}
        cases = {
            "closed before reported": ({}, "cannot be before"),
            "not a real date": ({"reported_at": "2025-02-30T10:00:00Z", "closed_at": ""},
                                "not a real date"),
            "wrong shape": ({"reported_at": "11/12/2025"}, "must look like"),
            "open with closed_at": ({"status": "open"}, "Only a closed issue"),
            "locked_out maybe": ({"locked_out": "maybe", "closed_at": "2025-11-12T11:00:00Z"},
                                 "yes or no"),
        }
        for name, (changes, message) in cases.items():
            with self.subTest(name):
                _, errors = validate_import_row({**base, **changes}, codes, badges)
                self.assertTrue(any(message in m for m in errors.values()), errors)

    def test_manage_refuses_to_overwrite(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = manage.main(["init", "--db", str(self.db_path)])
        self.assertEqual(code, 1)
        self.assertIn("--force", out.getvalue())
        self.assertEqual(self.count("issues"), 7)

    def test_manage_force_rebuilds_empty(self):
        with contextlib.redirect_stdout(io.StringIO()):
            code = manage.main(["init", "--db", str(self.db_path), "--force", "--no-seed"])
        self.assertEqual(code, 0)
        self.assertEqual(self.count("issues"), 0)


if __name__ == "__main__":
    unittest.main()
