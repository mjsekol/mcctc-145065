"""
test_deploy.py · Lab U05-02, from the reference stage w10 · what makes the app safe to put online

    python -m unittest -v

Covers configuration, the health route, security headers, error pages, the
PostgreSQL switch (as far as it can be tested without PostgreSQL), the
command-line tools, and the release pins. Every test uses a temporary
database. Standard library plus Flask's test client.
"""

import contextlib
import importlib.metadata
import io
import logging
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

import db
import manage
from app import APP_VERSION, create_app
from config import MIN_SECRET_LENGTH, ConfigError, load_config

HERE = pathlib.Path(__file__).parent
STRONG_KEY = "k" * MIN_SECRET_LENGTH
TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')


def psycopg_installed():
    try:
        import psycopg  # noqa: F401
    except ImportError:
        return False
    return True


class TempFolder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db_path = pathlib.Path(self.tmp.name) / "deploy.db"
        db.create_database(self.db_path)

    def make_app(self, **environ):
        env = {"APP_ENV": "test", "SECRET_KEY": STRONG_KEY, "DATABASE_PATH": str(self.db_path)}
        env.update(environ)
        return create_app(environ=env)


# ---------------------------------------------------------------------------
# Configuration comes from the environment
# ---------------------------------------------------------------------------

class ConfigTests(unittest.TestCase):
    def test_production_refuses_to_start_without_a_secret(self):
        with self.assertRaisesRegex(ConfigError, "SECRET_KEY is not set"):
            load_config({"APP_ENV": "production"})

    def test_production_refuses_a_short_secret(self):
        with self.assertRaisesRegex(ConfigError, "shorter than 32"):
            load_config({"APP_ENV": "production", "SECRET_KEY": "password123"})

    def test_production_accepts_a_strong_secret(self):
        config = load_config({"APP_ENV": "production", "SECRET_KEY": STRONG_KEY})
        self.assertEqual(config["SECRET_KEY"], STRONG_KEY)

    def test_debug_is_off_in_every_environment(self):
        for env in ("development", "test", "production"):
            with self.subTest(env=env), contextlib.redirect_stderr(io.StringIO()):
                config = load_config({"APP_ENV": env, "SECRET_KEY": STRONG_KEY})
                self.assertIs(config["DEBUG"], False)

    def test_development_without_a_secret_gets_a_random_one_and_a_warning(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            first = load_config({})["SECRET_KEY"]
            second = load_config({})["SECRET_KEY"]
        self.assertNotEqual(first, second)
        self.assertGreaterEqual(len(first), MIN_SECRET_LENGTH)
        self.assertIn("SECRET_KEY is not set", err.getvalue())

    def test_unknown_app_env_is_refused(self):
        with self.assertRaisesRegex(ConfigError, "APP_ENV must be one of"):
            load_config({"APP_ENV": "prod"})

    def test_cookies_are_secure_by_default_in_production_only(self):
        prod = load_config({"APP_ENV": "production", "SECRET_KEY": STRONG_KEY})
        self.assertIs(prod["SESSION_COOKIE_SECURE"], True)
        with contextlib.redirect_stderr(io.StringIO()):
            dev = load_config({"APP_ENV": "development"})
        self.assertIs(dev["SESSION_COOKIE_SECURE"], False)
        rehearsal = load_config({"APP_ENV": "production", "SECRET_KEY": STRONG_KEY,
                                 "COOKIE_SECURE": "0"})
        self.assertIs(rehearsal["SESSION_COOKIE_SECURE"], False)

    def test_a_bad_flag_is_refused(self):
        with self.assertRaisesRegex(ConfigError, "Expected 1 or 0"):
            load_config({"APP_ENV": "test", "SECRET_KEY": STRONG_KEY, "COOKIE_SECURE": "maybe"})

    def test_database_url_selects_postgres(self):
        config = load_config({"APP_ENV": "test", "SECRET_KEY": STRONG_KEY,
                              "DATABASE_URL": "postgresql://user:pw@db.example.invalid/line3"})
        self.assertEqual(db.backend_for(config), "postgres")
        config["DATABASE_URL"] = ""
        self.assertEqual(db.backend_for(config), "sqlite")

    def test_database_url_must_be_postgres(self):
        with self.assertRaisesRegex(ConfigError, "must start with postgres"):
            load_config({"APP_ENV": "test", "SECRET_KEY": STRONG_KEY,
                         "DATABASE_URL": "mysql://user:pw@db.example.invalid/line3"})

    def test_the_secret_is_not_in_the_code(self):
        for path in HERE.glob("*.py"):
            if path.name.startswith("test_"):
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
                self.assertNotRegex(text, r"SECRET_KEY\"?\]?\s*=\s*['\"][^'\"]+['\"]")

    def test_wsgi_refuses_to_start_in_production_without_a_secret(self):
        result = subprocess.run([sys.executable, "-c", "import wsgi"], cwd=HERE,
                                env=child_env(APP_ENV="production"),
                                capture_output=True, text=True, timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ConfigError: SECRET_KEY is not set", result.stderr)


def child_env(**changes):
    """This machine's environment without any app settings, plus `changes`.
    The child needs the rest (PATH, APPDATA) to find Python's packages."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("APP_ENV", "SECRET_KEY", "DATABASE_URL", "DATABASE_PATH",
                        "COOKIE_SECURE", "TRUST_PROXY")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.update(changes)
    return env


# ---------------------------------------------------------------------------
# The running app
# ---------------------------------------------------------------------------

class AppHardeningTests(TempFolder):
    def test_health_reports_ok(self):
        response = self.make_app().test_client().get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),
                         {"status": "ok", "database": "ok", "version": APP_VERSION})

    def test_health_reports_a_missing_database_without_details(self):
        app = self.make_app(DATABASE_PATH=str(pathlib.Path(self.tmp.name) / "missing.db"))
        with self.assertLogs(app.logger, level="ERROR"):
            response = app.test_client().get("/health")
        self.assertEqual(response.status_code, 503)
        body = response.get_data(as_text=True)
        self.assertEqual(response.get_json()["database"], "unavailable")
        self.assertNotIn("missing.db", body)
        self.assertNotIn("sqlite", body.lower())
        # And the check did not create an empty database file as a side effect.
        self.assertFalse((pathlib.Path(self.tmp.name) / "missing.db").exists())

    def test_health_reports_an_empty_database_as_unavailable(self):
        empty = pathlib.Path(self.tmp.name) / "empty.db"
        db.connect_path(empty, create=True).close()
        app = self.make_app(DATABASE_PATH=str(empty))
        with self.assertLogs(app.logger, level="ERROR"):
            self.assertEqual(app.test_client().get("/health").status_code, 503)

    def test_security_headers_on_every_response(self):
        client = self.make_app().test_client()
        for url in ["/", "/issues/999", "/health", "/reports/downtime.csv"]:
            with self.subTest(url=url):
                headers = client.get(url).headers
                self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
                self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
                self.assertEqual(headers["X-Frame-Options"], "DENY")
                self.assertEqual(headers["Referrer-Policy"], "same-origin")

    def test_the_trace_page_is_gone(self):
        self.assertEqual(self.make_app().test_client().get("/trace").status_code, 404)

    def test_an_unexpected_error_shows_no_traceback(self):
        app = self.make_app()
        app.config.update(TESTING=False, PROPAGATE_EXCEPTIONS=False)

        def explode():
            raise RuntimeError("secret internal detail: C:\\line3\\db")

        app.add_url_rule("/explode", "explode", explode)
        with self.assertLogs(app.logger, level="ERROR") as logs:
            response = app.test_client().get("/explode")
        self.assertEqual(response.status_code, 500)
        body = response.get_data(as_text=True)
        self.assertIn("Something went wrong on our side", body)
        self.assertNotIn("Traceback", body)
        self.assertNotIn("secret internal detail", body)
        self.assertIn("secret internal detail", "\n".join(logs.output))  # the log keeps it

    def test_an_oversized_form_is_refused(self):
        client = self.make_app().test_client()
        token = TOKEN.search(client.get("/issues/new").get_data(as_text=True)).group(1)
        response = client.post("/issues/new", data={"csrf_token": token, "title": "x" * 70000})
        self.assertEqual(response.status_code, 413)
        self.assertIn("That form is too large", response.get_data(as_text=True))

    def test_production_cookie_is_secure(self):
        app = self.make_app(APP_ENV="production")
        response = app.test_client().get("/issues/new", base_url="https://localhost")
        cookie = response.headers["Set-Cookie"]
        for flag in ("Secure", "HttpOnly", "SameSite=Lax"):
            self.assertIn(flag, cookie)

    def test_production_app_is_not_in_debug_mode(self):
        app = self.make_app(APP_ENV="production")
        self.assertFalse(app.debug)
        self.assertFalse(app.testing)

    def test_proxy_fix_is_applied_only_when_asked(self):
        plain = self.make_app()
        proxied = self.make_app(TRUST_PROXY="1")
        self.assertNotEqual(type(plain.wsgi_app).__name__, "ProxyFix")
        self.assertEqual(type(proxied.wsgi_app).__name__, "ProxyFix")

    def test_version_is_in_the_footer(self):
        body = self.make_app().test_client().get("/").get_data(as_text=True)
        self.assertIn(f"Line 3 Maintenance Log version {APP_VERSION}", body)

    def test_request_log_leaves_out_the_query_string(self):
        app = self.make_app()
        with self.assertLogs("line3", level="INFO") as logs:
            app.test_client().get("/issues?q=private+words")
        line = "\n".join(logs.output)
        self.assertIn("GET /issues -> list_issues 200", line)
        self.assertNotIn("private", line)

    def test_endpoint_names_match_earlier_stages(self):
        endpoints = {rule.endpoint for rule in self.make_app().url_map.iter_rules()}
        expected = {"dashboard", "list_issues", "new_issue_form", "create_issue", "issue_detail",
                    "edit_issue_form", "update_issue", "add_note", "confirm_delete",
                    "delete_issue", "list_equipment", "equipment_detail", "reports",
                    "reports_csv", "health", "static"}
        self.assertEqual(endpoints, expected)


# ---------------------------------------------------------------------------
# The database switch
# ---------------------------------------------------------------------------

class DatabaseSwitchTests(TempFolder):
    def test_placeholders_become_pyformat(self):
        self.assertEqual(db.to_pyformat("SELECT * FROM t WHERE a = ? AND b = ?"),
                         "SELECT * FROM t WHERE a = %s AND b = %s")

    def test_a_question_mark_inside_quotes_is_text(self):
        self.assertEqual(db.to_pyformat("SELECT '?' AS q, x FROM t WHERE y = ?"),
                         "SELECT '?' AS q, x FROM t WHERE y = %s")

    def test_a_literal_percent_is_doubled(self):
        self.assertEqual(db.to_pyformat("SELECT name FROM t WHERE name NOT LIKE 'sqlite_%' AND a = ?"),
                         "SELECT name FROM t WHERE name NOT LIKE 'sqlite_%%' AND a = %s")

    def test_the_escape_clause_survives(self):
        sql = "LOWER(i.title) LIKE ? ESCAPE '\\'"
        self.assertEqual(db.to_pyformat(sql), "LOWER(i.title) LIKE %s ESCAPE '\\'")

    def test_unbalanced_quotes_are_refused(self):
        with self.assertRaises(ValueError):
            db.to_pyformat("SELECT 'oops FROM t WHERE a = ?")

    def test_every_query_in_db_py_converts_cleanly(self):
        # Pull every triple-quoted SQL statement out of db.py and convert it.
        source = (HERE / "db.py").read_text(encoding="utf-8")
        statements = re.findall(r'"""\s*((?:SELECT|INSERT|UPDATE|DELETE)[\s\S]*?)"""', source)
        self.assertGreaterEqual(len(statements), 7)
        for sql in statements:
            with self.subTest(sql=sql.split()[0:4]):
                converted = db.to_pyformat(sql)
                self.assertEqual(converted.count("%s"), sql.count("?"))

    @unittest.skipIf(psycopg_installed(), "psycopg is installed on this machine")
    def test_postgres_without_psycopg_gives_a_clear_error(self):
        with self.assertRaisesRegex(db.DatabaseConfigError, "psycopg is not installed"):
            db.connect({"DATABASE_URL": "postgresql://u:p@db.example.invalid/x",
                        "DATABASE_PATH": ""})

    def test_missing_sqlite_file_is_an_error_not_a_new_empty_file(self):
        missing = pathlib.Path(self.tmp.name) / "typo.db"
        import sqlite3
        with self.assertRaises(sqlite3.OperationalError):
            db.connect_path(missing)
        self.assertFalse(missing.exists())

    def test_a_path_with_spaces_works(self):
        spaced = pathlib.Path(self.tmp.name) / "folder with spaces" / "line 3.db"
        spaced.parent.mkdir()
        db.create_database(spaced)
        conn = db.connect_path(spaced)
        self.addCleanup(conn.close)
        self.assertEqual(db.table_counts(conn)["issues"], 7)

    def test_both_schemas_define_the_same_tables_and_checks(self):
        lite = (HERE / "schema.sql").read_text(encoding="utf-8")
        pg = (HERE / "schema_postgres.sql").read_text(encoding="utf-8")
        tables = re.compile(r"CREATE TABLE (\w+)")
        checks = re.compile(r"CHECK \((.+)\),?$", re.M)
        self.assertEqual(tables.findall(lite), tables.findall(pg))
        self.assertEqual(checks.findall(lite), checks.findall(pg))
        identity = re.compile(r"^\s+id\s+INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,$", re.M)
        self.assertEqual(len(identity.findall(pg)), 4)
        self.assertNotIn("AUTOINCREMENT", pg)

    def test_seed_gives_no_ids(self):
        seed = (HERE / "seed.sql").read_text(encoding="utf-8")
        self.assertNotRegex(seed, r"INSERT INTO \w+ \(id")


# ---------------------------------------------------------------------------
# Command-line tools and release files
# ---------------------------------------------------------------------------

class ToolTests(TempFolder):
    def run_manage(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = manage.main(list(args), environ={})
        return code, out.getvalue()

    def test_init_if_empty_builds_a_new_database(self):
        fresh = pathlib.Path(self.tmp.name) / "sub" / "fresh.db"
        code, out = self.run_manage("init-if-empty", "--db", str(fresh))
        self.assertEqual(code, 0)
        self.assertIn("with the starting data", out)
        conn = db.connect_path(fresh)
        self.addCleanup(conn.close)
        self.assertEqual(db.table_counts(conn)["issues"], 7)

    def test_init_if_empty_leaves_existing_data_alone(self):
        conn = db.connect_path(self.db_path)
        with db.transaction(conn):
            db.delete_issue(conn, 1)
        conn.close()
        code, out = self.run_manage("init-if-empty", "--db", str(self.db_path))
        self.assertEqual(code, 0)
        self.assertIn("Nothing changed.", out)
        conn = db.connect_path(self.db_path)
        self.addCleanup(conn.close)
        self.assertEqual(db.table_counts(conn)["issues"], 6)

    def test_init_refuses_without_force(self):
        code, out = self.run_manage("init", "--db", str(self.db_path))
        self.assertEqual(code, 1)
        self.assertIn("--force", out)

    def test_tables_on_a_missing_file(self):
        code, out = self.run_manage("tables", "--db", str(pathlib.Path(self.tmp.name) / "nope.db"))
        self.assertEqual(code, 1)
        self.assertIn("No database", out)

    def test_requirements_pins_match_what_was_tested(self):
        text = (HERE / "requirements.txt").read_text(encoding="utf-8")
        pins = dict(re.findall(r"^([A-Za-z]+)==([\d.]+)$", text, re.M))
        self.assertEqual(set(pins), {"Flask", "Werkzeug"})
        for package, version in pins.items():
            with self.subTest(package=package):
                self.assertEqual(importlib.metadata.version(package), version)
        self.assertIn("gunicorn", text)
        self.assertIn("psycopg[binary]", text)

    def test_release_notes_name_this_version_as_the_baseline(self):
        text = (HERE / "RELEASE.md").read_text(encoding="utf-8")
        self.assertIn(f"v{APP_VERSION}", text)
        self.assertIn("baseline", text)

    def test_serve_local_refuses_without_production_settings(self):
        result = subprocess.run([sys.executable, "serve_local.py", "--port", "8689"], cwd=HERE,
                                env=child_env(), capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Set APP_ENV=production first", result.stdout)
        result = subprocess.run([sys.executable, "serve_local.py", "--port", "8689"], cwd=HERE,
                                env=child_env(APP_ENV="production"),
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Refusing to start: SECRET_KEY is not set", result.stdout)

    def test_dev_server_refuses_production(self):
        result = subprocess.run([sys.executable, "app.py", "--port", "8689"], cwd=HERE,
                                env=child_env(APP_ENV="production"),
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 1)
        self.assertIn("not for production", result.stdout)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    unittest.main()
