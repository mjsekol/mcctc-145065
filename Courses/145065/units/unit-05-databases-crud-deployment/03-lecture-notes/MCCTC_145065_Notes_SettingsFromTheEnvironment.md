# Lecture Notes: Settings Come from the Environment
## 145065 Object-Oriented Programming · Unit 5 · Week 10, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W10_SettingsFromTheEnvironment.md).
There is no exported deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-05-databases-crud-deployment/04-slides/MCCTC_145065_Slides_W10_SettingsFromTheEnvironment.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and Flask, which
are on the lab machines.

**Competencies:** 9.3.4 implement secure application configuration, including application hardening
and patch management.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. Every key in this file is a stand-in made for the example.
None is used anywhere real.

---

## Why this exists

Your app is about to live in two places: your laptop and a server. The code is the same in both. Some
settings are not.

| Setting | On your laptop | On the server |
|---|---|---|
| where the database is | a file in `instance/` | a database server, or a file the host keeps |
| the secret key | anything, or a random one per run | a long random value that never changes and nobody else knows |
| cookies | sent over plain HTTP to 127.0.0.1 | sent only over HTTPS |

If those settings are written in the code, one of two things happens. Either the server runs with your
laptop's settings, or you edit the code before every deploy and forget once.

Worse, a setting in the code is in Git. **A secret in the code is a secret you have published.** Your
repository is shared with your instructor, maybe with the whole internet, and every old commit keeps
every old value.

The fix: the code is shared. The configuration is not. It comes from the **environment**.

---

## The concept in plain language

Every running program has a set of **environment variables**: names and text values that the
operating system hands it at start. In Python, `os.environ` holds them. The same program started with
different environment variables behaves differently, with no code change.

The lab app reads these:

| Variable | Meaning |
|---|---|
| `APP_ENV` | `development` (the default), `test`, or `production` |
| `SECRET_KEY` | signs the session cookie. Required in production, at least 32 characters. |
| `DATABASE_URL` | a PostgreSQL address. When set, the app uses PostgreSQL. |
| `DATABASE_PATH` | a SQLite file, used when `DATABASE_URL` is not set |
| `COOKIE_SECURE` | whether cookies travel only over HTTPS. On by default in production. |

**Production refuses to start when a setting is missing or unsafe.** No `SECRET_KEY`: refuse. A key
shorter than 32 characters: refuse. A server that will not start is a problem you see in a minute. A
server that starts with a guessable key is a problem you may never see.

**Why the secret key matters.** Flask stores the session in a cookie in the visitor's browser. The key
signs that cookie, so the app can tell whether anyone changed it. The CSRF token from Week 8 lives in
the session. Anyone who knows the key can write a cookie the app believes.

**The application factory.** `create_app()` in the lab's `app.py` builds the app from the
configuration each time it is called. Tests call it with test settings. `serve_local.py` calls it with
production settings. The live server calls it through `wsgi.py`. One function, three sets of settings.
This is why the routes are registered from a table instead of `@app.get` decorators: a decorator needs
an app object when the file is imported, and a factory has none until it runs.

**9.3.4, hardening, in one list.** Each item closes a door:

- **Debug off in every environment.** Flask's debugger lets anyone who can reach an error page run
  Python on your server. The lab's `config.py` never turns it on.
- **The secret required and long,** from the environment, never from a file in Git.
- **`Secure` and `HttpOnly` cookies.** `Secure` means the browser sends the cookie only over HTTPS.
  `HttpOnly` means page scripts cannot read it.
- **Security headers on every response,** such as `Content-Security-Policy` and
  `X-Frame-Options: DENY`, which tell the browser what the page may load and forbid framing it inside
  another site.
- **A request size limit.** The lab refuses any request over 64 KB with a 413 before Flask reads it.
- **Error pages with no tracebacks.** The visitor sees plain words. The traceback goes to the log.
- **The teaching-only `/trace` page removed.** A production app does not describe its requests to
  strangers.
- **Dependencies pinned** in `requirements.txt`, such as `Flask==3.1.3`. A patch is then a deliberate
  change you test, not a surprise on the next deploy. That is patch management.
- **A health route,** `/health`, that tells the host whether the database answers. Tomorrow you make it
  tell the truth.

**A `.env` file** is a common way to keep local settings in one file. If you use one, it is already in
your `.gitignore` from Week 9. It never goes into Git.

---

## Worked example 1: refuse to start

```python
# config_demo.py
# Settings that change between your laptop and the live server come from the
# environment. Production refuses to start without a real secret.

MIN_SECRET_LENGTH = 32


class ConfigError(Exception):
    """The environment is unsafe or incomplete. Refuse to start."""


def load_config(environ):
    app_env = environ.get("APP_ENV", "development")
    secret = environ.get("SECRET_KEY", "")
    if app_env == "production":
        if not secret:
            raise ConfigError("SECRET_KEY is not set. Production refuses to start without it.")
        if len(secret) < MIN_SECRET_LENGTH:
            raise ConfigError(f"SECRET_KEY is shorter than {MIN_SECRET_LENGTH} characters.")
    return {"APP_ENV": app_env, "SECRET_KEY": secret, "DEBUG": False}


for env in [{"APP_ENV": "production"},
            {"APP_ENV": "production", "SECRET_KEY": "password123"},
            {"APP_ENV": "production", "SECRET_KEY": "9f" * 32}]:
    try:
        config = load_config(env)
        print("starts:", config["APP_ENV"], "debug", config["DEBUG"], "key length", len(config["SECRET_KEY"]))
    except ConfigError as error:
        print("Refusing to start:", error)
```

Output:

```
Refusing to start: SECRET_KEY is not set. Production refuses to start without it.
Refusing to start: SECRET_KEY is shorter than 32 characters.
starts: production debug False key length 64
```

`load_config` takes the environment as an argument instead of reading `os.environ` directly. That is
what makes it testable: a test passes in a dictionary and checks the result. The real app passes
`os.environ`.

`"9f" * 32` is a stand-in for a demo only. It is 64 characters and guessable, which is exactly
what a real key must not be.

---

## Worked example 2: one program, two environments

```python
# env_settings.py
# The same code, started twice with two different environments.
import os
import subprocess
import sys

CHILD = """
import os
print("APP_ENV =", os.environ.get("APP_ENV", "development"),
      "| DATABASE_PATH =", os.environ.get("DATABASE_PATH", "instance/toolcrib.db"))
"""

laptop = {k: v for k, v in os.environ.items() if k not in ("APP_ENV", "DATABASE_PATH")}
server = dict(laptop, APP_ENV="production", DATABASE_PATH="/var/data/toolcrib.db")
for name, env in [("laptop", laptop), ("server", server)]:
    result = subprocess.run([sys.executable, "-c", CHILD], env=env,
                            capture_output=True, text=True)
    print(name, "->", result.stdout.strip())
```

Output:

```
laptop -> APP_ENV = development | DATABASE_PATH = instance/toolcrib.db
server -> APP_ENV = production | DATABASE_PATH = /var/data/toolcrib.db
```

`subprocess.run` starts a new Python process with the environment you give it. The child program is
identical both times. Only its environment changed. `os.environ.get(name, default)` returns the default
when the variable is not set, which is why the laptop run shows the development values. The server path
is an invented example.

On a lab machine you set a variable for the current PowerShell window like this, and it disappears when
the window closes:

```
$env:APP_ENV = "production"
```

---

## Worked example 3: make a real key

```python
# make_secret.py
# Make a strong key. Print its length, never the key itself, in anything you share.
import secrets

key = secrets.token_hex(32)
print("characters:", len(key))
print("only hex digits:", all(ch in "0123456789abcdef" for ch in key))
print("same as the next one:", key == secrets.token_hex(32))
```

Output:

```
characters: 64
only hex digits: True
same as the next one: False
```

`secrets.token_hex(32)` makes 32 random bytes and writes each as two hex digits, so the key is 64
characters. The `secrets` module is made for keys. The `random` module is not: it is built for games
and simulations, and its output can be predicted.

For a real deploy you run this once from the command line:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the value into the host's environment settings. Never paste it into a file, a commit, a chat, or
an AI tool.

---

## Worked example 4: what a published key lets a stranger do

This example signs a session cookie the way Flask does, using a key an outsider read in a repository.
It then sends that cookie to two apps.

```python
# forged_cookie.py
# Anyone who knows the secret key can sign a session cookie the app trusts.
from flask import Flask, session
from flask.sessions import SecureCookieSessionInterface


def make_app(secret):
    app = Flask(__name__)
    app.secret_key = secret

    @app.get("/whoami")
    def whoami():
        return session.get("role", "nobody")

    return app


def forge(secret, data):
    """What an outsider does with a key they read in your repository."""
    outsider = Flask("outsider")
    outsider.secret_key = secret
    return SecureCookieSessionInterface().get_signing_serializer(outsider).dumps(data)


cookie = forge("dev-secret-change-me", {"role": "supervisor"})

for label, key in [("app with the published key", "dev-secret-change-me"),
                   ("app with its own long key ", "e3" * 32)]:
    client = make_app(key).test_client()
    client.set_cookie("session", cookie)
    print(label, "->", client.get("/whoami").get_data(as_text=True))
```

Output:

```
app with the published key -> supervisor
app with its own long key  -> nobody
```

The first app accepted a session that it never created, and believed the visitor was a supervisor.
The second app rejected the signature and treated the visitor as nobody. The only difference was the
key. The test client runs the app in memory, so no server starts.

---

## The wrong version, and the output it produces

A fallback secret "so it always starts." Do not copy this.

```python
# config_wrong.py: a fallback secret "so it always starts". Do not copy this.


def load_config(environ):
    return {
        "APP_ENV": environ.get("APP_ENV", "development"),
        "SECRET_KEY": environ.get("SECRET_KEY", "dev-secret-change-me"),
        "DEBUG": environ.get("FLASK_DEBUG", "1") == "1",
    }


config = load_config({"APP_ENV": "production"})
print("starts:", config)
```

Output:

```
starts: {'APP_ENV': 'production', 'SECRET_KEY': 'dev-secret-change-me', 'DEBUG': True}
```

**It starts. That is the problem.** Production is running with a key that is written in the repository,
so anyone who reads the code can sign a cookie the app trusts. Worked example 4 showed exactly that
key being accepted. The second line of the function turns debug on unless someone remembers to set
`FLASK_DEBUG` to something else. No error, no warning, and two open doors.

---

## Why the wrong version is tempting

The fallback makes the app start everywhere with no setup. Your teammate clones the repository and it
runs. Your tests run. The deploy runs. Every one of those is a real convenience.

A default of debug on is tempting for the same reason: on your laptop you want the debugger, and you
never have to type anything to get it.

The trouble is that the convenience does not stay on your laptop. The same line runs on the server.
The safe version gives the convenience only outside production: a random key for this run in
development, and a refusal in production.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Environment variable** | a named text value the operating system gives a program when it starts |
| **Configuration** | the settings that change between places the app runs, kept out of the code |
| **Secret key** | the value that signs session cookies. Anyone who has it can forge them. |
| **Application factory** | a function, `create_app()`, that builds the app from configuration |
| **Hardening** | removing or locking every feature an attacker could use and a user does not need |
| **Debug mode** | Flask's development helper, which can run code from an error page. Never in production. |
| **`Secure` cookie** | a cookie the browser sends only over HTTPS |
| **`HttpOnly` cookie** | a cookie that page scripts cannot read |
| **Pinning** | writing the exact version of each dependency, such as `Flask==3.1.3` |
| **Patch management** | updating dependencies on purpose, testing each update |

---

## Self-check

**Question 1.** Why is a server that refuses to start safer than one that starts with a default key?

**Question 2.** Your teammate's `config.py` has this line. Name two things wrong with it.

```python
SECRET_KEY = os.environ.get("SECRET_KEY", "toolcrib-secret")
```

**Question 3.** Why does `load_config` take the environment as an argument instead of reading
`os.environ` inside the function?

---

### Answers

**1.** A refusal is visible at once, and fixing it takes one setting. A server with a default key runs
normally while anyone who read the code can sign session cookies it trusts, and nothing tells you it is
happening.

**2.** The fallback key is written in the code, so it is published with the repository. It is also
short and guessable, well under 32 characters. And because it is a fallback, production starts with it
whenever the real key is missing, instead of refusing.

**3.** So a test can pass in any environment as a plain dictionary and check the result, without
changing the real environment of the test run. The app passes `os.environ` when it runs for real.
