# Lab U05-02: Ship It
## 145065 Object-Oriented Programming · Unit 5 · Week 10

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Week 10, Monday through Thursday, one
part a day. **Competencies:** 5.5.6 (format output: reports), 5.2.3 (arithmetic operations), 1.4.2
(present information), 9.3.4 (secure application configuration), 5.6.16 (deploy the application), 5.6.8
(create documentation: the data dictionary), 5.6.11 (develop the application), 5.7.2 (baseline and
lifecycle phases), 5.6.17 (collect feedback and maintain the application).

Files: `lab-u05-02-files/`. The app is last week's database app grown for deployment, with four parts
taken out, one per day. Every removed part is marked with a `TODO` that names its lab part.

**Riverside Fabrication is a composite**, an invented shop. Every record is invented.

**PostgreSQL, gunicorn, waitress, and Render are not on this machine.** Every step that needs them is
written for the lab and marked **[VERIFY]**, with a local alternative you run instead. Your instructor
announces this year's deployment target on Monday.

---

## The scenario

Your app works on your machine. On the internet it would run with a guessable secret, a database the
host may not keep, and error pages that assume a friendly visitor. This week adds a report the
supervisor asked for, makes the configuration safe, puts the app where someone else can reach it, and
names the version everyone agrees on.

## What you will build

A report whose every number is calculated, an app that refuses to start in production without a real
secret, a health route that tells the truth, a deploy, and a release tagged as the baseline.

---

## Starter code

Copy `lab-u05-02-files/` into your repository. Build a database and run the tests:

```
python manage.py init --db instance/line3.db
python selfcheck_u05_02.py
```

The self-check reports `85 of 101 self-checks passed`. The Week 9 features still work. Read `db.py`'s
report functions, `config.py`, and `RELEASE.md`. Each `TODO` names its part. **Keep every database file
out of Git**, as in Week 9.

---

## Part 1: a report calculates · Monday

### Step 1. Read the report you must match

Open `db.py` and read `report_by_equipment` and `report_totals`. They are `TODO` now. The comment names
every column and how it is calculated. The anchor's README has the hand-worked table your test checks.

### Step 2. Write `report_by_equipment`

One row per machine, most downtime first. Every machine appears, so use a `LEFT JOIN`. Count issues
with `COUNT(i.id)`, open ones with `SUM(CASE WHEN ...)`, and divide minutes by `60.0`, not `60`, so the
fraction survives. Labor comes from a subquery, so joining work notes does not double-count downtime.
Round hours to one place. Return `[_plain(r) for r in rows]`.

### Step 3. Write `report_totals`

One dictionary for all of Line 3: total issues, open issues, downtime hours, labor hours. An empty
database gives 0 and 0.0, never None.

### Step 4. See the report

```
python app.py --port 8680
```

Open `/reports`.

**Observable result:** the table shows 3.8 hours of downtime for all of Line 3, and OV-01 at 1.3 hours.

### Step 5. Prove the division

Change `/ 60.0` to `/ 60` in `report_by_equipment`, reload, and watch CV-01's 90 minutes become 1.0
hours. Change it back.

**Observable result:** with `/ 60.0`, CV-01 reads 1.5 hours.

### Step 6. Run the self-check

**Observable result:** every "Carried" and Part 1 line is PASS (92 of 101 so far).

**Acceptance criteria, Part 1.** Every Part 1 line is PASS. The report matches the anchor's hand-worked
table.

---

## Part 2: settings come from the environment · Tuesday

### Step 7. Read the plan in `config.py`

Open `config.py`. `load_config` accepts anything right now. Read its `TODO`.

### Step 8. Refuse an unsafe production start

In production, a missing `SECRET_KEY` must raise `ConfigError("SECRET_KEY is not set. Production
refuses to start without it.")`, and a key shorter than `MIN_SECRET_LENGTH` must raise the "shorter
than" error. Only outside production may a missing key be replaced by a random one.

### Step 9. Make cookies secure in production

Fix the `SESSION_COOKIE_SECURE` line so it defaults to True in production and False elsewhere, unless
`COOKIE_SECURE` says otherwise.

### Step 10. Rehearse a production start

PowerShell, in the lab folder:

```
$env:APP_ENV = "production"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:DATABASE_PATH = "$env:TEMP\line3_rehearsal.db"
python manage.py init --db $env:DATABASE_PATH
python serve_local.py --port 8681
```

**Observable result:** the server starts with `APP_ENV=production` and debug off. Open
`http://127.0.0.1:8681/health`: `{"database":"ok","status":"ok","version":"1.0.0"}`.

### Step 11. See the refusals

Stop the server. Start `serve_local.py` again with `$env:SECRET_KEY` cleared.

**Observable result:** `Refusing to start: SECRET_KEY is not set. Production refuses to start without
it.` and no port opens. Set the key again to continue.

### Step 12. Run the self-check

**Observable result:** every Part 2 line is PASS (98 of 101 so far).

**Acceptance criteria, Part 2.** Every Part 2 line is PASS. Production refuses a missing or short key.

---

## Part 3: deploying moves the configuration · Wednesday

### Step 13. Fix the health check

Open `db.py`'s `ping`. It runs `SELECT 1`, which succeeds even on a database with no tables, so the
host would call a broken app healthy. Change it to query a real table.

### Step 14. See it tell the truth

Stop the server. Point `DATABASE_PATH` at a database file with no tables (make one with
`python -c "import sqlite3; sqlite3.connect(r'C:\path\empty.db').close()"`), start `serve_local.py`,
and open `/health`, then `/`.

**Observable result:** `/health` answers 503 with `{"database":"unavailable",...}` and no detail. `/`
answers 500 with "Something went wrong on our side" and no traceback on the page. The traceback is in
the terminal. Point `DATABASE_PATH` back at your real rehearsal database.

### Step 15. Read the deployment steps

Read `DEPLOY.md`. Part 1 is the rehearsal you already ran. Part 3 is the target your instructor named,
every step marked [VERIFY].

### Step 16. Write your deploy notes

Write `DEPLOY_NOTES.md`: this year's target, every environment variable the app needs (with no value
for a secret), and the health-check path. If the target is Render, mark every Render step [VERIFY].

### Step 17. Deploy or record the rehearsal

Deploy to this year's target, or, if it cannot be reached in class, record the production-style
rehearsal an outside tester will use and write the target's steps as a plan.

**Observable result:** the app the tester will reach answers `/health` with status ok.

### Step 18. Run the self-check

**Observable result:** every Part 3 line is PASS (99 of 101 so far).

**Acceptance criteria, Part 3.** Every Part 3 line is PASS. `/health` answers 503 for a database with no
tables, and no page shows a traceback.

---

## Part 4: the baseline · Thursday

### Step 19. Read `RELEASE.md`

Open `RELEASE.md`. It is a `TODO` skeleton. It must name v1.0.0 as the baseline and end with a version
table that `release_check.py` can read.

### Step 20. Write the release notes

Fill in `RELEASE.md`: why a release gets a name, what v1.0.0 contains, the three places the version is
written, the tag commands, and a table with a `1.0.0` row.

### Step 21. Check the version agrees everywhere

```
python release_check.py
```

**Observable result:** `OK: release 1.0.0 is consistent.` If it says MISMATCH, the version in `app.py`,
`RELEASE.md`, and `/health` do not all agree.

### Step 22. See a mismatch

Add a `1.0.1` row to `RELEASE.md` and nothing else. Run `release_check.py` again.

**Observable result:** `MISMATCH: fix every place before you deploy or tag.` and it exits 1. Remove the
row.

### Step 23. Learn the tag commands

`RELEASE.md` gives the commands to tag the deployed commit. You run these in your own project's
repository after the deploy works:

```
git tag -a v1.0.0 -m "Baseline: first deployed release"
git push origin v1.0.0
```

An annotated tag records who tagged it and when. Do not run these on the lab copy.

### Step 24. Run everything

```
python selfcheck_u05_02.py
python -m unittest
```

**Observable result:** `101 of 101 self-checks passed`, and 100 tests OK.

**Acceptance criteria, full lab.**
- [ ] `python selfcheck_u05_02.py` prints `101 of 101 self-checks passed`
- [ ] `python -m unittest` reports 100 tests, OK
- [ ] `release_check.py` reports a consistent release
- [ ] `/health` tells the truth about an empty database
- [ ] No `.db` file in any commit
- [ ] Committed and pushed

---

## If it breaks

### 1. `75 / 60` is 1 in the report

**Cause:** integer division. Divide by `60.0`.

### 2. Downtime doubles when labor is added

**Cause:** work notes joined into the grouped query, repeating each issue once per note. Use a subquery
for labor.

### 3. A tool never checked out shows 1 issue

**Cause:** `COUNT(*)` counts the empty row a `LEFT JOIN` makes. Use `COUNT(i.id)`.

### 4. The app starts in production with no key

**Cause:** the production refusal in `config.py` is not written, or `APP_ENV` is not `production`.

### 5. `/health` says ok but pages fail

**Cause:** `ping` runs `SELECT 1`, which passes on an empty database. It must read a real table.

### 6. Every form fails after a restart

**Cause:** `SECRET_KEY` is random on each start when it is not set, so old form tokens stop matching.
Set it, or let production refuse to start without it.

### 7. `release_check.py` says MISMATCH

**Cause:** the version in `app.py`, the footer, `/health`, and `RELEASE.md` do not all agree. Change all
of them together.

---

## Stretch goal

Add a second report table: open issues by severity, or, in your project, checkouts by category. Read
the SQLite documentation on `GROUP BY` and cite it. Check every number against a hand calculation in a
test.

---

## Submission checklist

- [ ] `101 of 101 self-checks passed`
- [ ] 100 tests OK
- [ ] `release_check.py` consistent
- [ ] `/health` tells the truth about an empty database
- [ ] `DEPLOY_NOTES.md` names the target and every variable, with no secret value
- [ ] No `.db` file in any commit
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Part 1 not finished by the end of Monday, or the student cannot get the report numbers to match | SCAFFOLDED |
| Steady progress, questions about configuration or the deploy | STANDARD |
| 101 of 101 before Thursday's Build 1 is half over | EXTENDED |
| The student says they will never deploy anything | APPLIED |

---

## SCAFFOLDED

**Changed sections:**
- **Part 1:** the student receives `report_by_equipment` written and writes only `report_totals`, then
  checks both against the hand-worked table.
- **Part 3:** the student writes `DEPLOY_NOTES.md` and runs the rehearsal, and the actual deploy is a
  demonstration by the instructor.
- **Checkpoints:** show the self-check after each part.

**Acceptance criteria:** 101 of 101 self-checks, a consistent release, `/health` honest.

**Grading:** same 100-point scale.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus the security headers the lab did not teach.

**Added requirement.** Confirm the app sends `Content-Security-Policy`, `X-Content-Type-Options`,
`X-Frame-Options`, and `Referrer-Policy` on every response (the anchor's `app.py` has them). In your
README, name what each header protects against, and read the OWASP page on secure headers to cite one.

**Acceptance criteria:** all STANDARD criteria; a test checks all four headers on a normal response and
on an error response; the README names what each header does.

**Grading:** same scale.

---

## APPLIED

**For the student who will never deploy anything.** Configuration and versioning, for a program that
stays on one machine.

**Changed scenario.** Take a command-line program you wrote earlier this year. Move every setting it
hard-codes (a file path, a limit, a mode) into environment variables read through a `load_config`
function, with a clear error when a required one is missing. Add a `--version` flag and a `RELEASE.md`
with a version table. Write a `release_check`-style test that the version in the code and in
`RELEASE.md` agree.

**Acceptance criteria:** no setting is hard-coded; a missing required setting gives a clear error, not a
crash; `--version` and `RELEASE.md` agree, and a test proves it.

**Grading:** same scale. Requirements Fit is judged on whether the settings that change between machines
are the ones moved to the environment.
