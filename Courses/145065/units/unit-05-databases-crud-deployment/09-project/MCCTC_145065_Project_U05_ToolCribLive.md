# Unit 5 Project · Tool Crib Live
## 145065 Object-Oriented Programming · Unit 5 · Weeks 9-10

**Gate 3.** Full tooling, AI allowed and logged. **Solo.** Due **Week 10, Friday, at the end of the
commit window**, deployed. Graded on the 100-point project rubric, in Projects. **The Process
dimension, 15 points, is scored at the end of Week 9 and entered in Grading Period 3.** The other 85
points are scored in Week 10 and entered in Grading Period 4.

**Riverside Fabrication is a composite**: an invented small metal fabrication shop. Every person,
badge, tool, and record in this project is invented. Your outside tester is a real person, so they
type nothing real into your app.

**You start from your Unit 4 app, `toolcrib-web`.** If your Unit 4 app is not in a state you can build
on, talk to your instructor on Week 9, Monday. You may start from the Unit 4 lab's structure instead,
and you record that in your decision log.

---

## The brief

> **From:** the tool crib attendant, Line 3, Riverside Fabrication
> **About:** the tool crib page, version two
>
> The page works. The clipboard is gone. Now for the next round.
>
> Two of us tried to check tools out at the same moment on Tuesday and one checkout vanished. IT says
> the file the page saves to cannot handle that, and it needs a real database. Fine by me, as long as
> nothing I already have is lost.
>
> Things I need now. When a tool comes back, I mark it returned, with a word about its condition. If I
> type a checkout wrong, I fix it. If someone checks out a tool by mistake, I void it, but I want the
> page to make me confirm, because I will be wearing gloves and I will hit the wrong button.
>
> Purchasing sends me the tool list as a spreadsheet when we get new tools. I want to load that file
> instead of typing forty tools. If any line in it is wrong, load nothing and tell me which line.
>
> My supervisor wants a report. For each tool: how many times it went out, whether it is out now, how
> many times it came back late, and how long it usually stays out. The same report as a file she can
> open in a spreadsheet would be nice.
>
> And it needs to be on the shop network for real, not on your laptop. IT will want to know it is safe
> to leave running. Before we rely on it, somebody who has never seen it should try it, and you fix what
> trips them up.
>
> One more thing from IT: the badge list holds badges and the names on the screen, nothing else. They
> do not want anybody's phone number or address in there.

---

## What you are building

`toolcrib-web` version 1.0: the same app on a normalized SQLite database behind one `db.py` module, with
full create, read, update, and delete for checkouts, a CSV import for tools, a report with calculated
fields, safe production settings, and a deploy that someone outside the class has used. Then version
1.0.1, with their problems fixed.

---

## Technical requirements

Every Unit 4 requirement still holds, except T6 through T9, which the database replaces.

**The schema (Define and Measure)**

- **D1.** At least **three related tables** with primary keys and declared foreign keys. The suggested
  design has four: `technicians`, `categories`, `tools`, `checkouts`.
- **D2.** Each fact lives in one place. A category name, a tool name, and a technician name are each
  stored once.
- **D3.** **Record confidentiality.** The technicians table holds a badge, a display name, a role, and
  whether the badge is active. Nothing personal. Your design says why in one sentence.
- **D4.** The database enforces: a due time after the checkout time, a return time never before the
  checkout time, **no tool checked out twice at once**, unique badges, unique tool tags, and the allowed
  values of every fixed-list column. SQLite needs `PRAGMA foreign_keys = ON` on every connection.
- **D5.** `schema.sql` builds the tables. `seed.sql` loads your invented starting records without
  writing any id by hand. `manage.py init` builds and seeds, and refuses to overwrite without `--force`.
- **D6.** An **ER diagram** showing every table, key, and relationship with its cardinality.
- **D7.** `*.db`, `*.sqlite3`, `instance/`, and `.env` are in `.gitignore`. No database file is ever
  committed.

**CRUD (Improve)**

- **C1.** Every query lives in `db.py`, which is the only file that imports `sqlite3`. A test checks it.
- **C2.** Every value travels as a parameter. No value is ever joined into SQL text.
- **C3.** **Create:** the checkout form saves through `db.py` inside a transaction.
- **C4.** **Read:** the Unit 4 pages, now from the database, plus a search or filter that treats `%`,
  `_`, and `'` as plain text.
- **C5.** **Update:** return a tool (stamps `returned_at` once and records a condition), and edit a
  checkout's due time or note. Both use the Unit 4 validation habits and answer 400 with messages.
- **C6.** **Delete:** void a checkout. `GET` shows an "are you sure?" page and changes nothing. Only a
  `POST` with the CSRF token deletes. A missing checkout answers 404.
- **C7.** **Import:** `import_csv.py` loads tools from a CSV file with a header row. Every row is checked
  with the same rules as a form. If any row fails, nothing is imported, and every problem is printed
  with its line number. It handles the byte order mark Excel writes. `--dry-run` checks without
  importing.

**The report (Improve)**

- **R1.** A `/reports` page with one row per tool, including tools never checked out, and at least these
  **calculated fields**: times checked out, out now (yes or no), returned late, and the share of returns
  that were late as a percentage, rounded to one place. A tool with no returns shows no percentage, not
  a division error.
- **R2.** At least one more calculated field of your choice, such as average hours out.
- **R3.** A totals row for the whole crib.
- **R4.** A CSV export of the report as a download.
- **R5.** A test that compares every cell of the report with a table you worked out by hand from your
  seed data.

**Configuration and deployment (Improve and Control)**

- **P1.** `config.py` reads `APP_ENV`, `SECRET_KEY`, and the database location from the environment.
  Production refuses to start without a `SECRET_KEY` of at least 32 characters. Debug is off in every
  environment. Cookies are `Secure` in production.
- **P2.** An application factory, `create_app()`.
- **P3.** `GET /health` answers 200 with the version when the database has its tables, and 503 with no
  detail when it does not.
- **P4.** `requirements.txt` pins Flask and Werkzeug to the versions you tested with.
- **P5.** A production-style start that is not Flask's development server: the lab's `serve_local.py`
  for the rehearsal, and the server this year's target uses [VERIFY].
- **P6.** The app is deployed to **this year's target**, which your instructor announces on Week 10,
  Monday. It is one of:
  - **Render** with a PostgreSQL database [VERIFY every step]. `db.py` switches on `DATABASE_URL`, as the
    lab's does, and the PostgreSQL schema is in `schema_postgres.sql`.
  - **A school-managed host** your instructor names [VERIFY the host's steps].
  - **The production-style rehearsal** on a lab machine, which your outside tester reaches, with your
    Render or host steps written in `DEPLOY.md` as a plan.
- **P7.** `DEPLOY.md`: rehearse, prepare, deploy, check. Every step you could not run is marked
  [VERIFY].

**Baseline and maintenance (Control)**

- **B1.** `RELEASE.md` names **v1.0.0** as the baseline, lists what it contains, and has a version table.
- **B2.** The deployed commit is tagged `v1.0.0` and the tag is pushed.
- **B3.** `APP_VERSION`, the page footer, `/health`, and `RELEASE.md` agree. `release_check.py`, adapted
  from the lab, says so.
- **B4.** `USER_TEST.md`: someone outside the class used the deployed app for ten minutes with no help.
  Record their role, never their name, the tasks you gave them, and every problem: what they did, what
  they expected, and what happened. Sort each problem into fix now, fix later, or not a problem, with a
  reason.
- **B5.** Every "fix now" problem is fixed in **v1.0.1**: a new row in `RELEASE.md`, the version changed
  everywhere, deployed, and `/health` showing 1.0.1.

**Documentation (throughout)**

- **N1.** `DATA_DICTIONARY.md`: every table and every column with its type, whether it may be empty, its
  key, its rule, its meaning, and an example; the relationships in words; the calculated fields and
  their formulas; the CSV import format. `project-files/DATA_DICTIONARY_TEMPLATE.md` is the outline.
- **N2.** `TIMELINE.md` and the sprint paragraph (Week 9, Thursday).
- **N3.** `decision-log.md` with a Week 9 and a Week 10 entry, each naming a design pattern chosen and
  one rejected.
- **N4.** `AI_USAGE.md`, as in Unit 4.
- **N5.** A `unittest` suite, on a temporary database, that covers every requirement above that a test
  can check. At least 35 tests.

---

## Required repository structure

```
toolcrib-web/
  README.md                what it is, how to run, test, deploy, and what is not finished
  REQUIREMENTS.md          updated with the version two requirements
  ER_DIAGRAM.svg (or .png, or .md in the "relationships in words" form)
  DATA_DICTIONARY.md
  TIMELINE.md
  DEPLOY.md
  RELEASE.md
  USER_TEST.md
  decision-log.md
  ATTACK_LOG.md            carried from Unit 4, with at least one SQL injection attempt added
  AI_USAGE.md
  .gitignore               includes *.db, *.sqlite3, instance/, .env
  app.py                   create_app() and the routes
  config.py
  db.py                    the only file with SQL
  models.py
  validation.py
  security.py
  schema.sql
  schema_postgres.sql      only if Render with PostgreSQL is this year's target
  seed.sql
  manage.py
  import_csv.py
  data/tools_import.csv    a good file, invented
  data/tools_import_bad.csv  a file with at least three bad rows, invented
  wsgi.py
  serve_local.py
  release_check.py
  requirements.txt
  templates/  static/
  test_app.py  test_deploy.py
  save_pages.py
```

---

## DMAIC checkpoints

| Phase | What is due | When | Scored in |
|---|---|---|---|
| **Define** (D1) | the version two requirements; `schema.sql`; the ER diagram; the `.gitignore` | Week 9, Monday, end of Build 2 | GP3 Process |
| **Measure** (D2) | `seed.sql` and `manage.py init`; `db.py` create and read; the Unit 4 routes on the database | Week 9, Tuesday, end of Build 2 | GP3 Process |
| **Analyze** (D3) | update, void, and import working, with tests; a decision log entry | Week 9, Wednesday, end of Build 2 | GP3 Process |
| **Analyze** (D4) | `TIMELINE.md` and the sprint paragraph | Week 9, Thursday, end of Build 2 | GP3 Process |
| **Improve** (D5-D7) | the report (Mon), configuration and `/health` (Tue), deployed with `DEPLOY.md` and `DATA_DICTIONARY.md` (Wed) | Week 10, Monday to Wednesday | GP4 |
| **Control** (D8) | v1.0.0 tagged, `USER_TEST.md` | Week 10, Thursday, end of Build 2 | GP4 |
| **Control** | v1.0.1 deployed, demo recorded, everything true | Week 10, Friday, commit window | GP4 |

### The GP3 Process checkpoint, scored Week 9, Friday

| Evidence | Points |
|---|---|
| A commit at the end of every period, Week 9 Monday to Friday | 3 |
| D1 on time and complete | 3 |
| D2 on time and complete | 3 |
| D3 on time and complete | 2 |
| D4: a timeline you can keep, and a sprint paragraph that names a strength of each approach | 2 |
| Decision log: a Week 9 entry naming a chosen and a rejected design pattern | 2 |
| **Process, total** | **15** |

Agile ceremonies live inside Improve. Each Improve day in Week 10 starts with a stand-up line in your
README's log.

---

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| Flask and the Python standard library. No ORM. `psycopg` and a production server only if the deployment target needs them, installed on the target, not the lab image. | You write every query, so you can explain every query. |
| No SQL outside `db.py`, and no value joined into SQL text. | One place to review, one place to change for PostgreSQL, and no injection. |
| No `debug=True`, no secret in any file, no database file in Git. | Each one has leaked real data in real projects. |
| No real person's information, in the app or in `USER_TEST.md`. | Program rule. Your tester is a real person, so you record a role. |
| Account creation, terms, and any payment step for a host are your instructor's decision. | You are a minor, and host terms change [VERIFY]. |
| No login. | Out of scope. Your README's "not finished" section says anyone who can reach the app can change it. |

---

## Milestones

| When | Milestone |
|---|---|
| Week 9 Mon | D1 Define |
| Week 9 Tue | D2 Measure |
| Week 9 Wed | D3 Analyze |
| Week 9 Thu | GP3 exam, then D4 |
| **Week 9 Fri** | **GP3 Process checkpoint scored. Grading Period 3 closes.** |
| Week 10 Mon | D5: the report |
| Week 10 Tue | D6: configuration and `/health` |
| Week 10 Wed | D7: deployed, `DEPLOY.md`, `DATA_DICTIONARY.md` |
| Week 10 Thu | D8: v1.0.0 tagged, the outside user test |
| **Week 10 Fri** | **v1.0.1 deployed, demo recorded, submitted at the end of the commit window** |

---

## Three worked scope examples

### Small, and completely finished

Four tables. Checkouts get create, read, return, and void. The import loads tools. The report has the
four R1 fields and a totals row, and no CSV export. Deployed to this year's target. One outside test,
two fixes, v1.0.1. 35 tests.

**What it earns.** Full marks are possible, except the missing R4 costs Functionality points. Every
requirement met except one, and the README says so.

### Medium, and the one most students should aim for

Everything in Small, plus: the CSV export; editing a checkout's due time and note; a search that
matches tool names and notes; average hours out in the report; the import's `--dry-run`; 50 or more
tests, including the report's hand-calculated table.

### Large, and only if Medium is deployed by Week 10, Wednesday

Everything in Medium, plus one of: retiring a tool (a soft delete, so its history stays in the report)
with the reason in the decision log; checkouts by category as a second report; a PostgreSQL deployment
with the lab's `POSTGRES.md` checklist completed and recorded [VERIFY]. Record the choice.

### Scope calibration, three signals

- **Too big:** on Week 9, Monday, the schema has more than six tables, or includes users and passwords.
- **Too small:** on Week 9, Wednesday, there is no void, or the import commits row by row.
- **About right:** on Week 10, Tuesday, the rehearsal refuses to start without a key and `/health`
  answers.

---

## Grading · the 100-point project rubric

| Dimension | Points |
|---|---|
| Functionality | 25 |
| Code Quality | 20 |
| Documentation | 20 |
| Process | 15 |
| Demonstration | 10 |
| Polish | 10 |

### What each dimension means here

**Functionality, 25.** D4, C1 through C7, R1 through R4, P1 through P6, and B5 work on the deployed app
and on a fresh local database. Every number in the report matches your hand calculation.

**Code Quality, 20.** Scored on the five-dimension standard: Correctness, Security, Readability,
Performance, Requirements Fit. Parameterized queries only. Transactions around every write. No N+1
query on the report or the tool list. Names and comments that are true.

**Documentation, 20.** The ER diagram, `DATA_DICTIONARY.md`, `DEPLOY.md`, `RELEASE.md`,
`USER_TEST.md`, `TIMELINE.md`, the README, and `AI_USAGE.md`, all present and all true. The data
dictionary matches `schema.sql` column for column.

**Process, 15.** Scored at the end of Week 9 from the checkpoint table above, and entered in GP3.

**Demonstration, 10.** The five-minute recording below, and the live URL, spot-checked.

**Polish, 10.** The pages work for a gloved hand and a glance: large targets, high contrast, late and
out-now shown by words and shape as well as color, a confirmation before a void. Every page passes
web-check. The outside tester's "fix now" problems are gone.

---

## The five-minute demo recording

Record your screen and your voice [VERIFY the recorder on the lab image]. Five minutes or less. Commit
the file to your repository if it is under the size your instructor sets, or commit a link to where your
instructor told you to put it.

| Minutes | What you show |
|---|---|
| 0:00-0:30 | The live URL, and `/health` showing 1.0.1 |
| 0:30-1:30 | A checkout, a return, and a void with its confirmation |
| 1:30-2:15 | The import: the bad file refused with line numbers, then the good file loaded |
| 2:15-3:00 | The report, and one number checked against your hand calculation |
| 3:00-3:45 | `schema.sql` and your ER diagram: point at one foreign key and one constraint the database enforces |
| 3:45-4:30 | `USER_TEST.md`: the problem your tester found that you fixed, and the fix |
| 4:30-5:00 | What you would change for version 1.1, and why it is a MINOR version |

### The ten-point demonstration checklist

- [ ] Five minutes or less, with the live URL shown first
- [ ] `/health` shows the submitted version
- [ ] Create, update, and delete shown, with the delete confirmed
- [ ] The import refused a bad file and named the lines
- [ ] One report number checked against a hand calculation
- [ ] A foreign key and a database constraint named
- [ ] The tester's problem and the fix shown
- [ ] The version change explained with MAJOR, MINOR, PATCH
- [ ] Nothing real typed into the app on screen
- [ ] Voice and screen both clear

`project-files/DEMO_CHECKLIST.md` is the printable copy.

---

## Submission checklist

- [ ] `python -m unittest` passes, with at least 35 tests
- [ ] The deployed app answers `/health` with the version in your last commit
- [ ] `release_check.py` reports a consistent release
- [ ] The tags `v1.0.0` and `v1.0.1` are pushed
- [ ] Every page passes web-check, and your README shows it
- [ ] `git status` shows no database file, and `git log` never had one
- [ ] No secret and no real person's information in any file
- [ ] The demo recording is committed or linked
- [ ] The last commit is inside the Week 10 Friday commit window, and it is pushed
