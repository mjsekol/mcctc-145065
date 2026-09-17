"""
selfcheck_u04_02.py: Lab U04-02, which parts of the lab are done?

Run it from this folder, as often as you like:

    python selfcheck_u04_02.py

It runs the tests in test_app.py and sorts them by lab part. It changes no
files. Every test works on a temporary copy of the store.

A part is done when every line under it says PASS.
"""

import contextlib
import io
import os
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).parent

PARTS = {
    "Carried from Week 7, already passing": [
        "test_dashboard_lists_open_work_most_urgent_first",
        "test_unknown_status_is_a_bad_request",
        "test_missing_pages_are_404",
        "test_a_broken_store_gives_a_503_page",
        "test_store_validation_still_runs",
        "test_page_routes_answer",
        "test_every_page_extends_the_base_layout",
    ],
    "Part 1: the form posts, saves, and redirects": [
        "test_a_good_issue_is_saved_and_redirects",
        "test_the_confirmation_shows_once",
        "test_a_backup_is_kept_before_the_write",
        "test_the_saved_file_still_loads",
        "test_get_cannot_create_an_issue",
        "test_wrong_method_gets_a_page_not_a_crash",
    ],
    "Part 2: the server's rules": [
        "test_good_input_passes_and_is_converted",
        "test_badge_rules",
        "test_badge_is_trimmed_and_upper_cased",
        "test_title_boundaries",
        "test_description_boundaries",
        "test_downtime_boundaries_and_formats",
        "test_severity_must_be_known",
        "test_lockout_rule_truth_table",
        "test_any_value_but_yes_is_not_a_lockout",
        "test_errors_come_back_in_form_order",
        "test_bad_input_is_refused_with_400_and_nothing_is_saved",
        "test_answers_are_kept_on_a_refused_form",
        "test_an_empty_form_lists_every_required_field",
        "test_critical_without_lockout_is_refused",
        "test_client_hints_match_the_server_rules",
        "test_a_machine_not_in_the_list_is_refused",
    ],
    "Part 3: input is data, never code": [
        "test_a_script_in_a_title_is_stored_as_text_and_shown_escaped",
        "test_a_script_in_a_refused_form_is_escaped_too",
    ],
    "Part 4: forms prove where they came from": [
        "test_a_post_without_a_token_is_refused",
        "test_a_post_with_a_wrong_token_is_refused",
        "test_a_token_from_another_session_is_refused",
        "test_the_token_is_in_the_form",
        "test_session_cookie_is_http_only_and_same_site",
    ],
}


def run_tests():
    """Return {test name: True or False}. A failed sub-test fails its test."""
    os.environ.setdefault("SECRET_KEY", "selfcheck-only-not-a-real-secret")
    sys.path.insert(0, str(HERE))
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
        suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_app.py")
        suite.run(Recorder())
    return outcome


def main():
    outcome = run_tests()
    total = passed = 0
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
