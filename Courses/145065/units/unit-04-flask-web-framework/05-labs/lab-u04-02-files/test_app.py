"""
test_app.py · stage w08_forms · run from this folder:

    python -m unittest -v

Every test works on a temporary copy of the store, never data/line3_log.json.
Standard library plus Flask's test client.
"""

import contextlib
import io
import json
import os
import pathlib
import re
import shutil
import tempfile
import unittest

os.environ.setdefault("SECRET_KEY", "test-only-not-a-real-secret")

from app import app  # noqa: E402  (the environment must be set first)
from store import IssueStore, StoreFormatError, StoreMissingError  # noqa: E402
from validation import (BADGE_PATTERN, DESCRIPTION_MAX, DOWNTIME_MAX,  # noqa: E402
                        TITLE_MAX, TITLE_MIN, validate_issue)

HERE = pathlib.Path(__file__).parent
REAL_STORE = HERE / "data" / "line3_log.json"
TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')

GOOD = {
    "reported_by": "T-1041",
    "equipment": "PB-02",
    "title": "Ram stalls mid-stroke",
    "description": "The ram stops halfway on thick parts and the pump whines.",
    "severity": "high",
    "downtime_minutes": "30",
}


class StoreCopy(unittest.TestCase):
    """Base class: a fresh copy of the store in a temporary folder for every test."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store_path = pathlib.Path(self.tmp.name) / "line3_log.json"
        shutil.copy(REAL_STORE, self.store_path)
        self.old_path = app.config["STORE_PATH"]
        app.config.update(TESTING=True, STORE_PATH=str(self.store_path))
        self.client = app.test_client()
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

    def token(self):
        return TOKEN.search(self.page("/issues/new")).group(1)

    def submit(self, fields, token=True):
        data = dict(fields)
        if token is True:
            data["csrf_token"] = self.token()
        elif token:
            data["csrf_token"] = token
        return self.client.post("/issues/new", data=data)

    def stored_issue_count(self):
        return len(json.loads(self.store_path.read_text(encoding="utf-8"))["issues"])


# ---------------------------------------------------------------------------
# Carried from w07: routes, templates, reading the store
# ---------------------------------------------------------------------------

class RouteTests(StoreCopy):
    def test_page_routes_answer(self):
        for url in ["/", "/issues", "/issues/new", "/issues/3", "/equipment",
                    "/equipment/OV-01", "/trace"]:
            with self.subTest(url=url):
                self.page(url)

    def test_every_page_extends_the_base_layout(self):
        for url in ["/", "/issues/new", "/issues/3", "/issues/999"]:
            with self.subTest(url=url):
                body = self.client.get(url).get_data(as_text=True)
                self.assertIn('<nav class="site-nav" aria-label="Main">', body)
                self.assertIn("Riverside Fabrication is a composite", body)

    def test_dashboard_lists_open_work_most_urgent_first(self):
        body = self.page("/")
        self.assertIn("5 open issues", body)
        order = [body.index(f'href="/issues/{n}"') for n in (3, 5, 2, 1, 6)]
        self.assertEqual(order, sorted(order))

    def test_unknown_status_is_a_bad_request(self):
        self.page("/issues?status=everything", status=400)

    def test_missing_pages_are_404(self):
        self.page("/issues/999", status=404)
        self.page("/equipment/XX-99", status=404)

    def test_a_broken_store_gives_a_503_page(self):
        self.store_path.write_text("{", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            body = self.page("/", status=503)
        self.assertNotIn("Traceback", body)

    def test_store_validation_still_runs(self):
        self.edit_store(lambda d: d["issues"][0].update(severity="urgent"))
        with self.assertRaises(StoreFormatError):
            IssueStore(self.store_path)
        with self.assertRaises(StoreMissingError):
            IssueStore(pathlib.Path(self.tmp.name) / "nope.json")


# ---------------------------------------------------------------------------
# The form, end to end
# ---------------------------------------------------------------------------

class FormTests(StoreCopy):
    def test_a_good_issue_is_saved_and_redirects(self):
        response = self.submit(GOOD)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.headers["Location"], "/issues/8")
        self.assertEqual(self.stored_issue_count(), 8)
        saved = json.loads(self.store_path.read_text(encoding="utf-8"))["issues"][-1]
        self.assertEqual(saved["status"], "open")
        self.assertEqual(saved["downtime_minutes"], 30)
        self.assertIs(saved["locked_out"], False)
        self.assertRegex(saved["reported_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")

    def test_the_confirmation_shows_once(self):
        response = self.submit(GOOD)
        first = self.page(response.headers["Location"])
        self.assertIn("Issue 8 logged.", first)
        self.assertIn("Ram stalls mid-stroke", first)
        second = self.page(response.headers["Location"])
        self.assertNotIn("Issue 8 logged.", second)

    def test_a_backup_is_kept_before_the_write(self):
        before = self.store_path.read_bytes()
        self.submit(GOOD)
        backup = self.store_path.with_name("line3_log.json.bak")
        self.assertEqual(backup.read_bytes(), before)
        self.assertFalse(self.store_path.with_name("line3_log.json.tmp").exists())

    def test_the_saved_file_still_loads(self):
        self.submit(GOOD)
        self.submit(dict(GOOD, title="Second issue in a row"))
        store = IssueStore(self.store_path)
        self.assertEqual(store.get_issue(9).title, "Second issue in a row")

    def test_bad_input_is_refused_with_400_and_nothing_is_saved(self):
        response = self.submit(dict(GOOD, title="abc", downtime_minutes="-5"))
        self.assertEqual(response.status_code, 400)
        body = response.get_data(as_text=True)
        self.assertIn("<title>Error: Log an issue", body)
        self.assertIn("There are 2 problems", body)
        self.assertIn(f"between {TITLE_MIN} and {TITLE_MAX} characters", body)
        self.assertIn('aria-invalid="true"', body)
        self.assertEqual(self.stored_issue_count(), 7)

    def test_answers_are_kept_on_a_refused_form(self):
        body = self.submit(dict(GOOD, title="abc")).get_data(as_text=True)
        self.assertIn('value="T-1041"', body)
        self.assertIn('<option value="PB-02" selected>', body)
        self.assertIn('value="high" required checked', body)
        self.assertIn("pump whines.</textarea>", body)

    def test_an_empty_form_lists_every_required_field(self):
        response = self.submit({})
        self.assertEqual(response.status_code, 400)
        body = response.get_data(as_text=True)
        self.assertIn("There are 6 problems", body)

    def test_critical_without_lockout_is_refused(self):
        response = self.submit(dict(GOOD, severity="critical"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("needs the machine locked out first", response.get_data(as_text=True))
        ok = self.submit(dict(GOOD, severity="critical", locked_out="yes"))
        self.assertEqual(ok.status_code, 303)

    def test_client_hints_match_the_server_rules(self):
        body = self.page("/issues/new")
        self.assertIn(f'pattern="{BADGE_PATTERN}"', body)
        self.assertIn(f'minlength="{TITLE_MIN}"', body)
        self.assertIn(f'maxlength="{TITLE_MAX}"', body)
        self.assertIn(f'maxlength="{DESCRIPTION_MAX}"', body)
        self.assertIn(f'max="{DOWNTIME_MAX}"', body)
        # Every machine in the store is offered, and only those.
        offered = re.findall(r'<option value="([^"]*)"', body)
        self.assertEqual(offered, ["", "CV-01", "LC-01", "OV-01", "PB-01", "PB-02", "WR-01"])


# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------

class SecurityTests(StoreCopy):
    def test_a_post_without_a_token_is_refused(self):
        response = self.submit(GOOD, token=False)
        self.assertEqual(response.status_code, 403)
        self.assertIn("could not be accepted", response.get_data(as_text=True))
        self.assertEqual(self.stored_issue_count(), 7)

    def test_a_post_with_a_wrong_token_is_refused(self):
        self.token()  # the session now holds a real token
        response = self.submit(GOOD, token="guessed-token")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.stored_issue_count(), 7)

    def test_a_token_from_another_session_is_refused(self):
        other = app.test_client()
        stolen = TOKEN.search(other.get("/issues/new").get_data(as_text=True)).group(1)
        response = self.submit(GOOD, token=stolen)
        self.assertEqual(response.status_code, 403)

    def test_the_token_is_in_the_form(self):
        self.assertRegex(self.page("/issues/new"), TOKEN)

    def test_session_cookie_is_http_only_and_same_site(self):
        response = self.client.get("/issues/new")
        cookie = response.headers["Set-Cookie"]
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)

    def test_a_script_in_a_title_is_stored_as_text_and_shown_escaped(self):
        attack = "<script>alert('pwned')</script>"
        response = self.submit(dict(GOOD, title=attack))
        self.assertEqual(response.status_code, 303)
        stored = json.loads(self.store_path.read_text(encoding="utf-8"))["issues"][-1]
        self.assertEqual(stored["title"], attack)  # stored exactly as typed
        for url in ["/issues/8", "/issues", "/"]:
            body = self.page(url)
            self.assertNotIn(attack, body)
            self.assertIn("&lt;script&gt;alert(&#39;pwned&#39;)&lt;/script&gt;", body)

    def test_a_script_in_a_refused_form_is_escaped_too(self):
        attack = '"><script>alert(1)</script>'
        body = self.submit(dict(GOOD, reported_by=attack)).get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", body)
        self.assertIn("&#34;&gt;&lt;script&gt;", body)

    def test_a_machine_not_in_the_list_is_refused(self):
        response = self.submit(dict(GOOD, equipment="PB-01' OR '1'='1"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("Choose a machine from the list.", response.get_data(as_text=True))

    def test_get_cannot_create_an_issue(self):
        self.client.get("/issues/new?" + "&".join(f"{k}={v}" for k, v in GOOD.items()))
        self.assertEqual(self.stored_issue_count(), 7)

    def test_wrong_method_gets_a_page_not_a_crash(self):
        response = self.client.post("/issues", data={"csrf_token": self.token()})
        self.assertEqual(response.status_code, 405)


# ---------------------------------------------------------------------------
# Every rule in validation.py, without a server
# ---------------------------------------------------------------------------

class ValidationTests(unittest.TestCase):
    CODES = {"PB-01", "PB-02"}
    BADGES = {"T-1041", "S-2003"}

    def check(self, **changes):
        form = dict(GOOD)
        for key, value in changes.items():
            if value is None:
                form.pop(key, None)
            else:
                form[key] = value
        return validate_issue(form, self.CODES, self.BADGES)

    def test_good_input_passes_and_is_converted(self):
        clean, errors = self.check()
        self.assertEqual(errors, {})
        self.assertEqual(clean["downtime_minutes"], 30)
        self.assertIs(clean["locked_out"], False)

    def test_badge_rules(self):
        cases = {
            "": "Enter your badge number.",
            "1041": "Enter a badge like T-1041",
            "T-104": "Enter a badge like T-1041",
            "X-1041": "Enter a badge like T-1041",
            "T-10411": "Enter a badge like T-1041",
            "T-9999": "not on the Line 3 list",
        }
        for badge, message in cases.items():
            with self.subTest(badge=badge):
                _, errors = self.check(reported_by=badge)
                self.assertIn(message, errors["reported_by"])

    def test_badge_is_trimmed_and_upper_cased(self):
        clean, errors = self.check(reported_by="  s-2003 ")
        self.assertEqual(errors, {})
        self.assertEqual(clean["reported_by"], "S-2003")

    def test_title_boundaries(self):
        for title, ok in [("a" * 4, False), ("a" * 5, True), ("a" * 80, True),
                          ("a" * 81, False), ("     ", False), ("Line one\nline two", False)]:
            with self.subTest(length=len(title)):
                _, errors = self.check(title=title)
                self.assertEqual("title" not in errors, ok)

    def test_description_boundaries(self):
        for n, ok in [(9, False), (10, True), (1000, True), (1001, False)]:
            with self.subTest(n=n):
                _, errors = self.check(description="x" * n)
                self.assertEqual("description" not in errors, ok)

    def test_downtime_boundaries_and_formats(self):
        cases = {"0": True, "1440": True, "1441": False, "-1": False, "": False,
                 "12.5": False, "1e3": False, "abc": False, "٣": False, " 45 ": True}
        for raw, ok in cases.items():
            with self.subTest(raw=raw):
                _, errors = self.check(downtime_minutes=raw)
                self.assertEqual("downtime_minutes" not in errors, ok)

    def test_severity_must_be_known(self):
        # critical is a known severity. Its lockout rule reports on locked_out, not here.
        for value, ok in [("low", True), ("critical", True), ("urgent", False), ("", False),
                          (None, False)]:
            with self.subTest(value=value):
                _, errors = self.check(severity=value)
                self.assertEqual("severity" not in errors, ok)

    def test_lockout_rule_truth_table(self):
        # severity critical? | locked out? | accepted?
        rows = [("critical", "yes", True), ("critical", None, False),
                ("high", "yes", True), ("high", None, True)]
        for severity, locked, ok in rows:
            with self.subTest(severity=severity, locked=locked):
                _, errors = self.check(severity=severity, locked_out=locked)
                self.assertEqual(errors == {}, ok)

    def test_any_value_but_yes_is_not_a_lockout(self):
        clean, _ = self.check(locked_out="true")
        self.assertIs(clean["locked_out"], False)

    def test_errors_come_back_in_form_order(self):
        _, errors = validate_issue({}, self.CODES, self.BADGES)
        self.assertEqual(list(errors), ["reported_by", "equipment", "title", "description",
                                        "severity", "downtime_minutes"])


if __name__ == "__main__":
    unittest.main()
