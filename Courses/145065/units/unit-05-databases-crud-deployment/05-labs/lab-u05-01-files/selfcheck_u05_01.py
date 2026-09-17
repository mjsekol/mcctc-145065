"""
selfcheck_u05_01.py: Lab U05-01, which parts of the lab are done?

Run it from this folder, as often as you like:

    python selfcheck_u05_01.py

It runs the tests in test_app.py and sorts them by lab part. It changes no
files. Every test builds its own database in a temporary folder, never in
instance/.

A part is done when every line under it says PASS.
"""

import contextlib
import io
import os
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).parent
PATTERN = "test_app.py"

PARTS = {
    "Part 1: each fact lives in one place": [
        "test_four_related_tables",
        "test_seed_counts",
        "test_foreign_keys_are_declared",
        "test_a_machine_with_issues_cannot_be_deleted",
        "test_an_issue_cannot_point_at_a_missing_machine",
        "test_the_database_enforces_the_lockout_rule",
        "test_the_database_enforces_closed_at",
        "test_badges_are_unique",
        "test_schema_limits_match_validation",
        "test_no_personal_fields_in_technicians",
        "test_only_db_py_touches_sqlite",
    ],
    "Part 2: values travel as parameters": [
        "test_pages_answer",
        "test_dashboard_lists_open_work_most_urgent_first",
        "test_detail_joins_three_tables",
        "test_closed_issue_shows_time_to_close",
        "test_filters_combine",
        "test_search_is_case_insensitive",
        "test_unknown_filter_values_are_bad_requests",
        "test_missing_things_are_404",
        "test_equipment_counts_come_from_the_database",
        "test_create",
        "test_create_refuses_bad_input_and_writes_nothing",
        "test_an_inactive_badge_cannot_log",
        "test_add_note",
        "test_bad_note_is_refused_with_the_issue_page",
        "test_note_on_a_missing_issue_is_404",
        "test_search_attacks_match_nothing_and_break_nothing",
        "test_a_percent_sign_is_searched_literally",
        "test_sql_in_a_title_is_stored_as_text",
        "test_script_in_a_note_is_escaped",
        "test_the_id_in_the_url_must_be_a_number",
        "test_every_write_needs_the_token",
    ],
    "Part 3: a transaction makes many writes one change": [
        "test_update_changes_the_row",
        "test_closing_stamps_closed_at_once_and_reopening_clears_it",
        "test_update_refuses_critical_without_lockout",
        "test_update_refuses_an_unknown_status",
        "test_edit_form_is_filled_in",
        "test_delete_asks_first_and_get_deletes_nothing",
        "test_delete_removes_the_issue_and_its_notes",
        "test_delete_of_a_missing_issue_is_404",
        "test_a_failed_write_rolls_back",
        "test_good_file_imports_every_row",
        "test_bad_file_imports_nothing_and_names_every_line",
        "test_dry_run_imports_nothing",
        "test_excel_byte_order_mark_is_handled",
        "test_missing_column_is_reported",
        "test_import_row_time_rules",
        "test_manage_refuses_to_overwrite",
        "test_manage_force_rebuilds_empty",
    ],
    "Given: the report you read this week and write in Week 10": [
        "test_by_equipment_matches_hand_calculation",
        "test_labor_does_not_double_count_downtime",
        "test_totals",
        "test_totals_on_an_empty_database",
        "test_open_by_severity",
        "test_report_page",
        "test_csv_export",
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
        suite = unittest.defaultTestLoader.discover(str(HERE), pattern=PATTERN)
        suite.run(Recorder())
        if (HERE / "release_check.py").exists():
            import release_check
            try:
                outcome["release_check.py reports a consistent release"] = release_check.main() == 0
            except Exception:
                outcome["release_check.py reports a consistent release"] = False
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
