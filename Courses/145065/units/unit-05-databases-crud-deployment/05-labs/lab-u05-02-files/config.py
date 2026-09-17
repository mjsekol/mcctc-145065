"""
config.py · Line 3 Maintenance Log · Lab U05-02 STARTER

Every setting that changes between your laptop and the live server comes from
the environment, never from the code. Why: the code goes into Git and gets
shared. A secret in the code is a secret you have published.

Environment variables this app reads:

    APP_ENV           development (the default), test, or production
    SECRET_KEY        signs session cookies. REQUIRED in production, 32+ characters.
    DATABASE_URL      a PostgreSQL URL. When set, the app uses PostgreSQL. [VERIFY on Render]
    DATABASE_PATH     a SQLite file, used when DATABASE_URL is not set
    COOKIE_SECURE     1 or 0. Defaults to 1 in production: cookies only travel over HTTPS.
    TRUST_PROXY       1 when a proxy in front of the app (such as Render's) sets
                      X-Forwarded-For and X-Forwarded-Proto. [VERIFY on Render]

Debug mode is never switched on by this file. The Werkzeug debugger lets
anyone who can reach an error page run Python on your server.

Make a strong key with:

    python -c "import secrets; print(secrets.token_hex(32))"
"""

import os
import pathlib
import secrets
import sys

HERE = pathlib.Path(__file__).parent
APP_ENVS = ("development", "test", "production")
MIN_SECRET_LENGTH = 32


class ConfigError(Exception):
    """The environment is not safe or not complete. The app refuses to start."""


def _flag(value, default):
    if value is None or value == "":
        return default
    if value.lower() in ("1", "true", "yes", "on"):
        return True
    if value.lower() in ("0", "false", "no", "off"):
        return False
    raise ConfigError(f"Expected 1 or 0, got {value!r}")


def load_config(environ=None):
    """Build the Flask settings from an environment mapping (os.environ by default)."""
    env = os.environ if environ is None else environ
    app_env = env.get("APP_ENV", "development")
    if app_env not in APP_ENVS:
        raise ConfigError(f"APP_ENV must be one of {', '.join(APP_ENVS)}, not {app_env!r}")
    production = app_env == "production"

    secret = env.get("SECRET_KEY", "")
    # TODO Part 2, steps 8-9. In production, a missing SECRET_KEY must stop the app:
    #   raise ConfigError("SECRET_KEY is not set. Production refuses to start without it.")
    # and a key shorter than MIN_SECRET_LENGTH must stop it too:
    #   raise ConfigError(f"SECRET_KEY is shorter than {MIN_SECRET_LENGTH} characters.")
    # Only outside production may a missing key be replaced by a random one.
    if not secret:
        secret = secrets.token_hex(32)
        print("[config] SECRET_KEY is not set. Using a random key for this run only.",
              file=sys.stderr, flush=True)

    database_url = env.get("DATABASE_URL", "")
    if database_url and not database_url.startswith(("postgres://", "postgresql://")):
        raise ConfigError("DATABASE_URL must start with postgres:// or postgresql://")

    return {
        "APP_ENV": app_env,
        "DEBUG": False,
        "TESTING": app_env == "test",
        "SECRET_KEY": secret,
        "DATABASE_URL": database_url,
        "DATABASE_PATH": env.get("DATABASE_PATH", str(HERE / "instance" / "line3.db")),
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        # TODO Part 2, step 10: in production, cookies travel only over HTTPS unless
        #   COOKIE_SECURE says otherwise. The default below is wrong for production.
        "SESSION_COOKIE_SECURE": _flag(env.get("COOKIE_SECURE"), default=False),
        "PREFERRED_URL_SCHEME": "https" if production else "http",
        "TRUST_PROXY": _flag(env.get("TRUST_PROXY"), default=False),
        # The largest form this app accepts is a few kilobytes. Anything far
        # bigger is refused with 413 before Flask reads it into memory.
        "MAX_CONTENT_LENGTH": 64 * 1024,
    }
