# Lecture Notes: Deploying Moves the Configuration, Not the Laptop
## 145065 Object-Oriented Programming · Unit 5 · Week 10, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W10_Deploying.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-05-databases-crud-deployment/04-slides/MCCTC_145065_Slides_W10_Deploying.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python, Flask, and a
copy of `05-labs/lab-u05-02-files/` in a folder outside any repository.

**Competencies:** 5.6.16 deploy the application. 5.6.8 create documentation, here the data dictionary.
5.6.11 develop the application.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. Every record in this file is invented.

**What was run, and what was not.** The production-style rehearsal in this file was run on the course
build machine, and its output is quoted with the date and time masked. PostgreSQL, gunicorn, and Render
were **not** available there. Every statement about them is marked **[VERIFY]**. Render changes its
plans, prices, free-tier limits, and terms, so nothing here describes them. Your instructor announces
this year's deployment target on Week 10, Monday.

---

## Why this exists

In 145060 you deployed an app. This one is harder, and it is worth saying why.

This app has a **database** and a **secret**. Your laptop has a SQLite file and whatever key you set
this morning. The server has neither until you give them to it. It may also throw away any file the app
writes when you redeploy [VERIFY for this year's host]. So the database has to live somewhere the
redeploy does not touch, and the tables have to exist before the first visitor arrives.

Copying your laptop to the internet does not work. The code is the same. **Everything around the code
changes.** A deploy is the same code, started with different configuration, and then proven to work.

---

## The concept in plain language

A deploy changes three things and keeps one:

| | On your laptop | On the server |
|---|---|---|
| **the code** | your repository | **the same commit** |
| the web server | Flask's development server | a production WSGI server, such as gunicorn [VERIFY] |
| the database | a SQLite file | a database server such as PostgreSQL, reached through `DATABASE_URL` [VERIFY] |
| the settings | your terminal's environment | the host's environment settings |

**A production WSGI server.** WSGI is the standard way a Python web app and a web server talk. Flask's
development server is built for one person testing. When it starts, it says so itself:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
```

A production server is built for real traffic and never shows the debugger. `wsgi.py` in the lab
builds the app once, from the environment, for that server to call.

**The build command** runs once per deploy, before the app starts. For the lab app it is written in
`DEPLOY.md` as:

```
pip install -r requirements.txt && python manage.py init-if-empty
```

That line is **[VERIFY]** against this year's host. Its two halves are the idea: install the pinned
requirements, then create the tables **only if they do not exist**.

**Three ways to start the database, and only one is safe on every deploy:**

| Command | On a new, empty database | On a database with records |
|---|---|---|
| `manage.py init` | creates and seeds the tables | refuses, and changes nothing |
| `manage.py init --force` | creates and seeds the tables | **deletes every record** and rebuilds |
| `manage.py init-if-empty` | creates and seeds the tables | "already has tables. Nothing changed." |

`init-if-empty` is the one that belongs in a build command. It builds on the first deploy and leaves the
data alone on every deploy after.

**Proof that it worked** comes from two places. The **health route**, `/health`, answers 200 when the
database answers and 503 when it does not, with no detail a stranger could use. The host can check it
on a schedule without a person [VERIFY how this year's host uses it]. And a **written checklist** in
`DEPLOY.md`, where every item is ticked from a real check, not from memory.

**The rehearsal comes first.** Before you deploy, you start the app on your own machine exactly the way
the server will: production settings, a real secret, debug off, and no Flask development server. The
lab's `serve_local.py` does this with Python's standard library, so it needs no new package. Be honest
about what it is: a reference server with no worker processes and no timeouts. It is fine on
127.0.0.1. It is not for the internet.

---

## Worked example 1: the rehearsal

In a copy of `lab-u05-02-files/`, outside any repository, in PowerShell:

```
$env:APP_ENV = "production"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:DATABASE_PATH = "$env:TEMP\line3_rehearsal.db"
python manage.py init --db $env:DATABASE_PATH
python serve_local.py --port 8688
```

This run used port 8688. Use the port your lab handout names. The database goes in your `TEMP` folder,
never inside a repository.

`manage.py init` printed (the folder is shortened to `...`):

```
Created the tables in ...\line3_rehearsal.db with the starting data.
```

The server printed its start line. Then four pages were opened: `/health`, `/`, `/issues/abc`, and
`/trace`. The terminal showed:

```
Production-style server on http://127.0.0.1:8688  (APP_ENV=production, debug=False). Ctrl+C stops it.
[date and time] INFO line3: GET /health -> health 200 (1.0 ms)
[date and time] INFO line3: GET / -> dashboard 200 (14.2 ms)
[date and time] INFO line3: GET /issues/abc -> None 404 (2.0 ms)
[date and time] INFO line3: GET /trace -> None 404 (0.2 ms)
```

And `/health` answered:

```
{"database":"ok","status":"ok","version":"1.0.0"}
```

Read each line.

- `APP_ENV=production, debug=False`: the settings came from the environment, and debug is off.
- `/health` 200: the database answered.
- `/issues/abc` 404: a bad address gets the site's own "not found" page, not a traceback.
- `/trace` 404: the teaching page from Unit 4 is gone.

`serve_local.py` sets `COOKIE_SECURE=0` for this run, because the rehearsal is plain HTTP on
127.0.0.1 and a `Secure` cookie would never come back. On a host that serves HTTPS, leave
`COOKIE_SECURE` unset, and cookies are marked `Secure`.

**Your starter will not refuse yet.** In the Lab U05-02 starter, Part 2 is not done, so the same
commands with no `SECRET_KEY` start anyway. The server printed
`[config] SECRET_KEY is not set. Using a random key for this run only.` and started. The finished
app, with Part 2 done, printed this and opened no port:

```
Refusing to start: SECRET_KEY is not set. Production refuses to start without it.
```

---

## Worked example 2: init-if-empty is safe to run twice

With `DATABASE_PATH` still set from example 1:

```
python manage.py init-if-empty
python manage.py init --db $env:DATABASE_PATH
```

Output, one line each (the folder is shortened to `...`):

```
...\line3_rehearsal.db already has tables. Nothing changed.
...\line3_rehearsal.db already has tables. Add --force to delete every record and rebuild it.
```

The first command is what a build runs on every deploy after the first. It changed nothing. The second
refused, and exited with status 1, which a build treats as a failure. That refusal is the design: the
only command that destroys records needs a flag you have to type on purpose.

**The worse mistake.** A build command with `init --force` passes every deploy. It also deletes every
record the shop entered since the last one, every single time, and prints a cheerful
`Created the tables` while it does.

---

## Worked example 3: SQLite now, PostgreSQL on the server

Nothing in the right-hand column was run on the build machine. The lab's `POSTGRES.md` lists eighteen
differences. These are the five you will hit first.

| SQLite (tested) | PostgreSQL [VERIFY] |
|---|---|
| `?` placeholders | `%s` placeholders, and a literal `%` written `%%` |
| `id INTEGER PRIMARY KEY` fills itself | `id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY` |
| foreign keys only with `PRAGMA foreign_keys = ON` | always enforced |
| `LIKE` ignores case for ASCII letters | `LIKE` is case-sensitive; the lab lowers both sides |
| a file next to the app | a separate server, reached through `DATABASE_URL` |

Why the lab's switch touches one Python file: every query is in `db.py`. When `DATABASE_URL` is set,
the lab's `db.py` opens PostgreSQL through the psycopg driver and rewrites each `?` as `%s` before it
sends a query [VERIFY on a machine with PostgreSQL]. The routes never know which database they use.

The honest cost of testing on SQLite: it accepts some things PostgreSQL refuses. The third row is the
one from Week 9. An orphan row that SQLite stored all week can break the deploy. Test on the real
database before you trust it.

**The host steps [VERIFY every one].** The lab's `DEPLOY.md` Part 3 describes the Render steps two ways,
from `render.yaml` or through the dashboard. Its build command is the one above, its start command is
`gunicorn wsgi:app`, its health check path is `/health`, and its environment variables are `APP_ENV`,
`SECRET_KEY`, `DATABASE_URL`, and `TRUST_PROXY`. None of that was run on the build machine. Your
instructor decides whether your class deploys there, to a school-managed host, or to the rehearsal on a
lab machine that your outside tester reaches. Account creation and terms are your instructor's call,
not yours.

---

## The wrong version, and the output it produces

Point the rehearsal at an **empty** database file: a file that exists and has no tables. That is what a
live app sees when the build command left out `init-if-empty`. Make one in `TEMP`:

```
python -c "import sqlite3; sqlite3.connect(r'$env:TEMP\line3_empty.db').close()"
$env:DATABASE_PATH = "$env:TEMP\line3_empty.db"
```

Start the finished lab app with `serve_local.py`, then open `/health` and `/`. The pages answered:

```
503 /health {"database":"unavailable","status":"error","version":"1.0.0"}
500 /
```

The page for `/` said "Something went wrong on our side," with no traceback on the page. The traceback
was in the terminal. Here are its first and last lines for each request, with the frames in between
replaced by `...`:

```
[date and time] ERROR app: health check: database unavailable
Traceback (most recent call last):
  ...
sqlite3.OperationalError: no such table: equipment
[date and time] INFO line3: GET /health -> health 503 (4.0 ms)
[date and time] ERROR app: Exception on / [GET]
Traceback (most recent call last):
  ...
sqlite3.OperationalError: no such table: issues
[date and time] INFO line3: GET / -> dashboard 500 (6.7 ms)
```

**The app did everything right.** The visitor saw no internals. The health check told the host the
truth. The **configuration** was wrong. On a real host, the traceback is in the host's log, not on the
page [VERIFY where this year's host shows it]. The message to look for on PostgreSQL is
`relation "equipment" does not exist` [VERIFY], which means the same thing.

**What your starter does here.** The Lab U05-02 starter's health check runs a query that needs no table,
so on the same empty file it answered `200` and `{"database":"ok","status":"ok","version":"1.0.0"}`,
while `/` answered 500. A health check that says "ok" for a database with no tables is the bug you fix
in Part 3.

---

## Why the wrong version is tempting

The build command without `init-if-empty` is shorter, and it is the build command from 145060, where the
app had no database. The deploy succeeds. The host shows a green status. The first person to open a page
gets an error.

A health check that returns "ok" without touching a real table is tempting for the same reason. It
always passes. It passes on your laptop, where the tables exist, so every test you think of agrees with
it.

And `init --force` is tempting after a bad deploy, because it makes the error go away. It makes the data
go away too.

The habits that prevent all three: rehearse against an empty database on purpose, make the health check
touch a real table, and put only `init-if-empty` in a build command.

---

## Build 2 today: the data dictionary (5.6.8)

Your outside tester reads your `DATA_DICTIONARY.md` tomorrow, and so will anyone who maintains the app
after you. For every table and every column, write its type, whether it may be empty, its key, its rule,
its meaning, and an example. Then the relationships in words, the calculated fields with their
formulas, and the CSV import format. The project spec names the template to start from.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Deploy** | put a specific version of the app on a server and start it with that server's configuration |
| **Rehearsal** | a production-style start on your own machine, before the real deploy |
| **WSGI** | the standard interface between a Python web app and a web server |
| **Production server** | a web server built for real traffic, such as gunicorn [VERIFY on the host] |
| **Build command** | the command a host runs before starting the app, once per deploy |
| **Start command** | the command a host runs to start the app |
| **`init-if-empty`** | create the tables only when the database has none |
| **Health check** | a route the host calls to learn whether the app and its database answer |
| **`DATABASE_URL`** | the environment variable that holds the database server's address |
| **Data dictionary** | a document that describes every table and column: type, rule, meaning, example |

---

## Self-check

**Question 1.** Your app works on your machine. On the server, every page fails with "no such table" or
"relation does not exist." What did the build skip, and where do you look first?

**Question 2.** A classmate puts `python manage.py init --force` in the build command "so the tables
always exist." What happens on the second deploy?

**Question 3.** Why does the rehearsal matter, if the real server is different anyway? Give the
strongest reason, and one thing the rehearsal cannot prove.

---

### Answers

**1.** The build did not create the tables: `init-if-empty` was left out of the build command, or it ran
against a different database. Look at the build command in the host's settings, then at the build log
for `Created the tables` [VERIFY where this year's host shows it].

**2.** Every record entered since the first deploy is deleted, and the starting data is loaded again.
The deploy reports success, so nobody notices until someone looks for a record.

**3.** The strongest reason: it proves the app starts with production settings, refuses a missing
secret, shows no tracebacks, and answers `/health`, before a stranger ever sees it, on a machine where
you can read every error. What it cannot prove: that the host's database, environment variables, and
start command are right. Only the real deploy and the checklist can.
