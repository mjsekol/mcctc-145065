# Deploying the Line 3 Maintenance Log

Riverside Fabrication is a composite: an invented shop with invented records.

**Why this page is careful.** A deployment has two halves. The half inside this folder was run
and tested on the build machine. The half on Render was not: the build machine has no Render
account in use for this work, and Render changes its screens, plans, free-tier limits, and
whether it asks for a payment card. **Every Render step is marked [VERIFY].** Check each one
against Render's current documentation before a class depends on it. Students completed a
Render deployment in 145060, so this page covers only what is new: a database and production
settings.

**Students are minors.** Account creation, terms of service, and any payment step are the
instructor's call, made before class. [VERIFY Render's current age requirement and terms.]

## Part 1 · Rehearse locally (tested)

You should see the app start with production settings before you deploy. This uses only the
Python standard library, because neither gunicorn nor waitress is installed on the build machine.

PowerShell, from the folder that holds `app.py`:

```
$env:APP_ENV = "production"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:DATABASE_PATH = "$env:TEMP\line3_rehearsal.db"
python manage.py init --db $env:DATABASE_PATH
python serve_local.py --port 8681
```

What the build machine printed for this copy, on port 8681 (the date and time on log lines are masked):

```
Production-style server on http://127.0.0.1:8681  (APP_ENV=production, debug=False). Ctrl+C stops it.
[date and time] INFO line3: GET /health -> health 200 (2.3 ms)
[date and time] INFO line3: GET / -> dashboard 200 (8.2 ms)
```

And `/health` answered:

```
{"database":"ok","status":"ok","version":"1.0.0"}
```

Things to try, each tested:

| Try this | You should see |
|---|---|
| Start without `SECRET_KEY` | `Refusing to start: SECRET_KEY is not set. Production refuses to start without it.` |
| Start with `SECRET_KEY=password123` | `Refusing to start: SECRET_KEY is shorter than 32 characters.` |
| `python app.py --port 8680` with `APP_ENV=production` | `APP_ENV is production. The development server is not for production. Use serve_local.py here, or gunicorn on the server.` |
| Point `DATABASE_PATH` at a file with no tables, open `/health` | status 503 and `{"database":"unavailable","status":"error","version":"1.0.0"}` |
| Same file, open `/` | status 500, "Something went wrong on our side", no traceback on the page; the traceback is in the terminal |
| Point `DATABASE_PATH` at a file that does not exist | `No database at <path>. Run: python manage.py init --db <path>` and no empty file is created. If the file disappears while the server runs, `/health` answers 503 (`test_health_reports_a_missing_database_without_details`) |

`serve_local.py` sets `COOKIE_SECURE=0` because the rehearsal is plain HTTP on 127.0.0.1. Render
serves HTTPS, so leave `COOKIE_SECURE` unset there and cookies are marked `Secure`.

**On Windows lab machines**, waitress is the usual production server
[VERIFY: not installed on the build machine]:

```
pip install waitress
waitress-serve --listen=127.0.0.1:8681 wsgi:app
```

## Part 2 · Prepare the repository (tested where marked)

1. The app is in a Git repository, with `requirements.txt`, `wsgi.py`, `schema_postgres.sql`,
   and `render.yaml` committed. (Tested: every file exists and `test_deploy.py` checks the pins.)
2. **No secrets and no databases are committed.** Search before you push:
   `git grep -n "SECRET_KEY ="` should find nothing that assigns a real value.
   `.db` files and `instance/` belong in `.gitignore`.
3. The suite passes: `python -m unittest` reports 100 tests, OK. (Tested.)
4. Pin the two production packages. On a machine where they install, run `pip install -r
   requirements.txt`, then `pip freeze`, and copy the exact `gunicorn` and `psycopg` versions
   into `requirements.txt`. [VERIFY]

## Part 3 · Render [VERIFY every step]

Two ways to do the same thing. The Blueprint is faster; the dashboard shows each piece.

### With the Blueprint

1. In Render, create a new Blueprint from the repository. Render reads `render.yaml`. [VERIFY]
2. Review what it will create: one web service, one PostgreSQL database. Choose plans in the
   dashboard. `render.yaml` names none on purpose. [VERIFY]
3. Apply. Render generates `SECRET_KEY` and connects `DATABASE_URL` to the database. [VERIFY]

### With the dashboard

1. Create a PostgreSQL database. Copy its internal connection URL. [VERIFY where Render shows it]
2. Create a web service from the repository. [VERIFY]
   - Root directory: the folder holding `app.py`
   - Build command: `pip install -r requirements.txt && python manage.py init-if-empty`
   - Start command: `gunicorn wsgi:app`
   - Health check path: `/health`
3. Environment variables:

   | Key | Value |
   |---|---|
   | `APP_ENV` | `production` |
   | `SECRET_KEY` | a value from `python -c "import secrets; print(secrets.token_hex(32))"`, pasted once, never committed |
   | `DATABASE_URL` | the database URL from step 1 |
   | `TRUST_PROXY` | `1` [VERIFY that Render sits one proxy in front of the app] |

4. Deploy. Watch the log for `Created the tables` on the first deploy and `already has tables.
   Nothing changed.` on every deploy after it. `init-if-empty` never wipes data.

### Check the live app

1. `https://<your-app>/health` returns `{"database":"ok","status":"ok","version":"1.0.0"}`.
2. The page footer says version 1.0.0.
3. Log an issue, edit it, add a note, delete it. Open `/reports`.
4. In the browser's developer tools, the session cookie shows `Secure`, `HttpOnly`, and
   `SameSite=Lax`. The response headers include `Content-Security-Policy` and
   `X-Frame-Options: DENY`.
5. Visit `/trace`: 404. Visit `/issues/abc`: the site's 404 page, not a traceback.
6. If a page fails, read Render's log. The traceback is there, not on the page.

### If the database connection fails [VERIFY]

- `psycopg is not installed`: the build did not install `requirements.txt`.
- An SSL error: some hosts require `?sslmode=require` on the URL. Check Render's guidance.
- `relation "equipment" does not exist`: the build command did not run `init-if-empty`.

## Part 4 · Tag the baseline

When the live app passes every check above, tag the commit. See `RELEASE.md`.

## Part 5 · The outside user test

Someone outside the class uses the live app for ten minutes with no help. You watch and write
down every place they hesitate or break something. You fix what they broke, bump the version
(1.0.1 for a fix), add a line to `RELEASE.md`, deploy, and check `/health` shows the new
version. That loop is 5.6.17: collect feedback and maintain the application.

Arrange the tester with your instructor. Give them an invented badge from `seed.sql` (for
example T-1041). They type no real personal information into the app.
