"""
selfcheck_u05_02.py: Lab U05-02, which parts of the lab are done?

Run it from this folder, as often as you like:

    python selfcheck_u05_02.py

It runs the tests in test_*.py and sorts them by lab part. It changes no
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
PATTERN = "test_*.py"

PARTS = {
    "Carried from Week 9, already passing": [
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
        "test_pages_answer",
        "test_dashboard_lists_open_work_most_urgent_first",
        "test_detail_joins_three_tables",
        "test_closed_issue_shows_time_to_close",
        "test_filters_combine",
        "test_search_is_case_insensitive",
        "test_unknown_filter_values_are_bad_requests",
        "test_missing_things_are_404",
        "test_create",
        "test_create_refuses_bad_input_and_writes_nothing",
        "test_an_inactive_badge_cannot_log",
        "test_update_changes_the_row",
        "test_closing_stamps_closed_at_once_and_reopening_clears_it",
        "test_update_refuses_critical_without_lockout",
        "test_update_refuses_an_unknown_status",
        "test_edit_form_is_filled_in",
        "test_add_note",
        "test_bad_note_is_refused_with_the_issue_page",
        "test_note_on_a_missing_issue_is_404",
        "test_delete_asks_first_and_get_deletes_nothing",
        "test_delete_removes_the_issue_and_its_notes",
        "test_delete_of_a_missing_issue_is_404",
        "test_every_write_needs_the_token",
        "test_a_failed_write_rolls_back",
        "test_search_attacks_match_nothing_and_break_nothing",
        "test_a_percent_sign_is_searched_literally",
        "test_sql_in_a_title_is_stored_as_text",
        "test_script_in_a_note_is_escaped",
        "test_the_id_in_the_url_must_be_a_number",
        "test_good_file_imports_every_row",
        "test_bad_file_imports_nothing_and_names_every_line",
        "test_dry_run_imports_nothing",
        "test_excel_byte_order_mark_is_handled",
        "test_missing_column_is_reported",
        "test_import_row_time_rules",
        "test_manage_refuses_to_overwrite",
        "test_manage_force_rebuilds_empty",
    ],
    "Part 1: a report calculates": [
        "test_by_equipment_matches_hand_calculation",
        "test_labor_does_not_double_count_downtime",
        "test_totals",
        "test_totals_on_an_empty_database",
        "test_open_by_severity",
        "test_report_page",
        "test_csv_export",
        "test_equipment_counts_come_from_the_database",
        "test_every_query_in_db_py_converts_cleanly",
    ],
    "Part 2: settings come from the environment": [
        "test_production_refuses_to_start_without_a_secret",
        "test_production_refuses_a_short_secret",
        "test_production_accepts_a_strong_secret",
        "test_debug_is_off_in_every_environment",
        "test_development_without_a_secret_gets_a_random_one_and_a_warning",
        "test_unknown_app_env_is_refused",
        "test_cookies_are_secure_by_default_in_production_only",
        "test_a_bad_flag_is_refused",
        "test_database_url_selects_postgres",
        "test_database_url_must_be_postgres",
        "test_the_secret_is_not_in_the_code",
        "test_wsgi_refuses_to_start_in_production_without_a_secret",
        "test_production_cookie_is_secure",
        "test_production_app_is_not_in_debug_mode",
        "test_serve_local_refuses_without_production_settings",
        "test_dev_server_refuses_production",
    ],
    "Part 3: deploying moves the configuration": [
        "test_health_reports_ok",
        "test_health_reports_a_missing_database_without_details",
        "test_health_reports_an_empty_database_as_unavailable",
        "test_security_headers_on_every_response",
        "test_the_trace_page_is_gone",
        "test_an_unexpected_error_shows_no_traceback",
        "test_an_oversized_form_is_refused",
        "test_proxy_fix_is_applied_only_when_asked",
        "test_request_log_leaves_out_the_query_string",
        "test_endpoint_names_match_earlier_stages",
        "test_placeholders_become_pyformat",
        "test_a_question_mark_inside_quotes_is_text",
        "test_a_literal_percent_is_doubled",
        "test_the_escape_clause_survives",
        "test_unbalanced_quotes_are_refused",
        "test_postgres_without_psycopg_gives_a_clear_error",
        "test_missing_sqlite_file_is_an_error_not_a_new_empty_file",
        "test_a_path_with_spaces_works",
        "test_both_schemas_define_the_same_tables_and_checks",
        "test_seed_gives_no_ids",
        "test_init_if_empty_builds_a_new_database",
        "test_init_if_empty_leaves_existing_data_alone",
        "test_init_refuses_without_force",
        "test_tables_on_a_missing_file",
    ],
    "Part 4: the baseline": [
        "test_release_notes_name_this_version_as_the_baseline",
        "test_requirements_pins_match_what_was_tested",
        "test_version_is_in_the_footer",
        "release_check.py reports a consistent release",
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
