"""
test_app.py · stage w07_routes · run from this folder:

    python -m unittest -v

Every test reads a temporary copy of the store, never data/line3_log.json.
Standard library plus Flask's test client.
"""

import contextlib
import io
import json
import pathlib
import shutil
import tempfile
import unittest

from app import app
from store import IssueStore, StoreFormatError, StoreMissingError

HERE = pathlib.Path(__file__).parent
REAL_STORE = HERE / "data" / "line3_log.json"


class StoreCopy(unittest.TestCase):
    """Base class: a fresh copy of the store in a temporary folder for every test."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store_path = pathlib.Path(self.tmp.name) / "line3_log.json"
        shutil.copy(REAL_STORE, self.store_path)
        self.old_path = app.config["STORE_PATH"]
        app.config.update(TESTING=True, STORE_PATH=str(self.store_path))
        self.client = app.test_client()
        # The trace lines are useful when you run the server, noise in a test run.
        self.quiet = contextlib.redirect_stdout(io.StringIO())
        self.quiet.__enter__()

    def tearDown(self):
        self.quiet.__exit__(None, None, None)
        app.config["STORE_PATH"] = self.old_path
        self.tmp.cleanup()

    def edit_store(self, change):
        data = json.loads(self.store_path.read_text(encoding="utf-8"))
        change(data)
        self.store_path.write_text(json.dumps(data), encoding="utf-8")

    def page(self, url, status=200):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status, url)
        return response.get_data(as_text=True)


class RouteTests(StoreCopy):
    def test_five_or_more_page_routes_answer(self):
        for url in ["/", "/issues", "/issues/3", "/equipment", "/equipment/OV-01", "/trace"]:
            with self.subTest(url=url):
                self.page(url)

    def test_every_page_extends_the_base_layout(self):
        for url in ["/", "/issues", "/issues/3", "/equipment", "/equipment/OV-01", "/trace",
                    "/issues/999"]:
            with self.subTest(url=url):
                body = self.client.get(url).get_data(as_text=True)
                self.assertIn('<nav class="site-nav" aria-label="Main">', body)
                self.assertIn("Riverside Fabrication is a composite", body)

    def test_dashboard_lists_open_work_most_urgent_first(self):
        body = self.page("/")
        self.assertIn("5 open issues", body)
        self.assertIn("1 critical issue open", body)
        # Closed issue 4 is not open work.
        self.assertNotIn("Nozzle camera image is dim", body)
        # Critical (3) before high (5, 2) before medium (1) before low (6).
        order = [body.index(f'href="/issues/{n}"') for n in (3, 5, 2, 1, 6)]
        self.assertEqual(order, sorted(order))

    def test_status_filter_uses_the_query_string(self):
        body = self.page("/issues?status=closed")
        self.assertIn("Exhaust fan belt squeal", body)
        self.assertNotIn("Wire feed stutters", body)
        self.assertIn('aria-current="page">Closed', body)

    def test_unknown_status_is_a_bad_request(self):
        body = self.page("/issues?status=everything", status=400)
        self.assertIn("Unknown status", body)

    def test_url_variable_selects_the_issue(self):
        body = self.page("/issues/2")
        self.assertIn("Zone 2 heater slow to reach setpoint", body)
        self.assertIn("Luis Brennan (T-1057)", body)
        self.assertIn("60 minutes", body)

    def test_int_converter_refuses_text(self):
        self.page("/issues/three", status=404)

    def test_missing_issue_and_machine_are_404(self):
        self.page("/issues/999", status=404)
        self.page("/equipment/XX-99", status=404)
        self.page("/no-such-page", status=404)

    def test_equipment_page_counts_open_issues(self):
        body = self.page("/equipment")
        # OV-01 has one open (2) and one closed (7).
        row = body[body.index('href="/equipment/OV-01"'):]
        row = row[:row.index("</tr>")]
        self.assertIn('<td class="num">1</td>', row)

    def test_equipment_detail_shows_only_that_machine(self):
        body = self.page("/equipment/OV-01")
        self.assertIn("Zone 2 heater", body)
        self.assertIn("Exhaust fan belt squeal", body)
        self.assertNotIn("Back gauge drifts", body)

    def test_trace_shows_the_request(self):
        body = self.page("/trace?machine=PB-01")
        self.assertIn("machine = PB-01", body)
        self.assertIn("<dd>GET</dd>", body)
        self.assertIn("<dd>trace</dd>", body)

    def test_request_cycle_is_logged(self):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            self.client.get("/issues/3")
        line = captured.getvalue()
        self.assertIn("[trace] GET /issues/3 -> issue_detail -> 200 text/html", line)


class StoreThroughRoutesTests(StoreCopy):
    def test_an_edit_to_the_file_shows_on_the_next_request(self):
        self.edit_store(lambda d: d["issues"][0].update(title="Back gauge drifts 3 mm"))
        self.assertIn("Back gauge drifts 3 mm", self.page("/issues/1"))

    def test_text_from_the_file_is_escaped(self):
        self.edit_store(lambda d: d["issues"][0].update(title="<script>alert(1)</script>"))
        body = self.page("/issues/1")
        self.assertNotIn("<script>alert(1)</script>", body)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", body)

    def test_a_broken_store_gives_a_503_page_not_a_traceback(self):
        self.store_path.write_text('{"format_version": 2, "equipment": [', encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()) as err:
            body = self.page("/", status=503)
        self.assertIn("The maintenance log is unavailable", body)
        self.assertNotIn("Traceback", body)
        self.assertIn("StoreFormatError", err.getvalue())

    def test_a_missing_store_gives_a_503_page(self):
        self.store_path.unlink()
        with contextlib.redirect_stderr(io.StringIO()):
            self.page("/issues", status=503)


class StoreValidationTests(StoreCopy):
    def load_after(self, change):
        self.edit_store(change)
        return IssueStore(self.store_path)

    def test_the_real_store_loads(self):
        store = IssueStore(REAL_STORE)
        self.assertEqual(len(store.issues()), 7)
        self.assertEqual(len(store.all_equipment()), 6)

    def test_wrong_version_is_refused(self):
        with self.assertRaisesRegex(StoreFormatError, "format_version is 1"):
            self.load_after(lambda d: d.update(format_version=1))

    def test_missing_field_is_named(self):
        with self.assertRaisesRegex(StoreFormatError, r"issues\[2\]: missing field 'severity'"):
            self.load_after(lambda d: d["issues"][2].pop("severity"))

    def test_true_is_not_a_whole_number(self):
        with self.assertRaisesRegex(StoreFormatError, "whole number"):
            self.load_after(lambda d: d["issues"][0].update(downtime_minutes=True))

    def test_negative_downtime_is_refused(self):
        with self.assertRaisesRegex(StoreFormatError, "negative"):
            self.load_after(lambda d: d["issues"][0].update(downtime_minutes=-5))

    def test_issue_must_point_at_real_equipment(self):
        with self.assertRaisesRegex(StoreFormatError, "unknown equipment 'ZZ-01'"):
            self.load_after(lambda d: d["issues"][0].update(equipment="ZZ-01"))

    def test_unknown_severity_is_refused(self):
        with self.assertRaisesRegex(StoreFormatError, "unknown severity"):
            self.load_after(lambda d: d["issues"][0].update(severity="urgent"))

    def test_duplicate_ids_are_refused(self):
        with self.assertRaisesRegex(StoreFormatError, "duplicate id 1"):
            self.load_after(lambda d: d["issues"][1].update(id=1))

    def test_missing_file_has_its_own_error(self):
        with self.assertRaises(StoreMissingError):
            IssueStore(pathlib.Path(self.tmp.name) / "nope.json")


if __name__ == "__main__":
    unittest.main()
