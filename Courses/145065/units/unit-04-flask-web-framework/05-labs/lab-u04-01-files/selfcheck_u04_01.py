"""
selfcheck_u04_01.py: Lab U04-01, which parts of the lab are done?

Run it from this folder, as often as you like:

    python selfcheck_u04_01.py

It runs the tests in test_app.py and sorts them by lab part, then checks your
LICENSES.md for Part 1. It changes no files. Every test works on a temporary
copy of the store, never data/line3_log.json.

A part is done when every line under it says PASS.
"""

import contextlib
import io
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).parent
PACKAGES = ["flask", "werkzeug", "jinja2", "markupsafe", "itsdangerous", "click", "blinker"]

PARTS = {
    "Part 2: the request cycle": [
        "test_status_filter_uses_the_query_string",
        "test_unknown_status_is_a_bad_request",
        "test_url_variable_selects_the_issue",
        "test_int_converter_refuses_text",
        "test_request_cycle_is_logged",
        "test_dashboard_lists_open_work_most_urgent_first",
        "test_an_edit_to_the_file_shows_on_the_next_request",
        "test_text_from_the_file_is_escaped",
    ],
    "Part 3: templates": [
        "test_equipment_page_counts_open_issues",
        "test_equipment_detail_shows_only_that_machine",
        "test_missing_issue_and_machine_are_404",
        "test_five_or_more_page_routes_answer",
        "test_every_page_extends_the_base_layout",
        "test_trace_shows_the_request",
    ],
    "Part 4: reading the store": [
        "test_a_broken_store_gives_a_503_page_not_a_traceback",
        "test_a_missing_store_gives_a_503_page",
        "test_negative_downtime_is_refused",
        "test_issue_must_point_at_real_equipment",
        "test_the_real_store_loads",
        "test_wrong_version_is_refused",
        "test_missing_field_is_named",
        "test_true_is_not_a_whole_number",
        "test_unknown_severity_is_refused",
        "test_duplicate_ids_are_refused",
        "test_missing_file_has_its_own_error",
    ],
}


def part1():
    """LICENSES.md names every package Flask brought with it, with a license."""
    path = HERE / "LICENSES.md"
    text = path.read_text(encoding="utf-8").lower() if path.exists() else ""
    results = [("LICENSES.md exists", path.exists())]
    for name in PACKAGES:
        lines = [line for line in text.splitlines() if name in line]
        ok = any(("bsd" in line or "mit" in line) for line in lines)
        results.append((f"LICENSES.md has a row for {name} with its license", ok))
    return results


def run_tests():
    """Return {test name: True or False}. A failed sub-test fails its test."""
    sys.path.insert(0, str(HERE))
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_app.py")
    outcome = {}

    class Recorder(unittest.TestResult):
        def addSuccess(self, test):
            outcome.setdefault(test._testMethodName, True)

        def addFailure(self, test, err):
            outcome[test._testMethodName] = False

        def addError(self, test, err):
            outcome[test._testMethodName] = False

        def addSubTest(self, test, subtest, err):
            if err is not None:
                outcome[test._testMethodName] = False

    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        suite.run(Recorder())
    return outcome


def main():
    total = passed = 0
    print("Part 1: someone else's code")
    for label, ok in part1():
        total += 1
        passed += ok
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    outcome = run_tests()
    for part, names in PARTS.items():
        print(part)
        for name in names:
            ok = outcome.get(name, False)
            total += 1
            passed += ok
            print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print(f"\n{passed} of {total} self-checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
