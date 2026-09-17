# Lab U05-01: Line 3 Gets a Database
## 145065 Object-Oriented Programming · Unit 5 · Week 9

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Week 9, Monday through Wednesday, one
part a day. **Competencies:** 5.6.7 (document a design: the ER diagram), 1.4.3 (record confidentiality
in the schema), 5.1.5 (data management through a language), 5.3.11 (access data repositories), 9.3.1
(SQL injection), 5.5.7 (read a CSV file), 5.3.10 (a failed write that undoes itself).

Files: `lab-u05-01-files/`. The app is last week's app with the JSON store replaced by SQLite, and with
the schema and the write functions taken out, one part a day. Every removed part is marked with a
`TODO` that names its lab part. The report functions are complete; you read them this week and write
your own next week.

**Riverside Fabrication is a composite**, an invented shop. Every record is invented.

**Before anything: keep the database out of Git.** A database file is data, not code, and a committed
one is public in the history forever. Work in a folder whose `.gitignore` lists `*.db`, `*.sqlite3`,
`instance/`, and `.env` before you build the database.

---

## The scenario

Two technicians saved an issue at the same moment last week, and one issue vanished. The JSON store
cannot handle two writers. A database can, and it brings rules the file could not enforce: keys that
make every reference checkable, constraints that refuse bad rows, and transactions that make a group of
writes all-or-nothing.

## What you will build

The maintenance log on a normalized SQLite database with four related tables, full create, read,
update, and delete through parameterized queries in one module, and a CSV import that is all-or-nothing.

---

## Starter code

Copy `lab-u05-01-files/` into a folder in your repository **whose `.gitignore` already lists the
database patterns above.** Then:

```
python -m unittest
python selfcheck_u05_01.py
```

The self-check reports `25 of 56 self-checks passed`. Read `schema.sql` and `db.py`. Each `TODO` names
its part. Do not run the app yet: the schema is not finished.

---

## Part 1: each fact lives in one place · Monday

### Step 1. Read the broken schema

Open `schema.sql`. It works: the app starts and the seed loads. It is also wrong in several ways, each
marked with a `TODO`.

### Step 2. Add the .gitignore lines

If your folder's `.gitignore` does not already have them, add:

```
*.db
*.sqlite3
instance/
.env
```

**Observable result:** you will build a database in step 8 and `git status` will not list it.

### Step 3. See the flat-table problem

Read the comment at the top of `schema.sql` about where each fact lives. A single table would repeat a
machine's name on every row.

### Step 4. Decide the personal-data column

The starter's `technicians` table has a `home_phone` column. The app never uses it. Decide whether it
belongs, and write your decision and its reason in your lab README. Then remove it, because a table
that does not hold personal data cannot leak it.

### Step 5. Declare the foreign keys

Two columns in `issues` and two in `work_notes` hold ids from other tables. Declare each as
`REFERENCES <table> (id)`. The `work_notes` to `issues` reference gets `ON DELETE CASCADE`, so deleting
an issue deletes its notes.

### Step 6. Add the value rules

Add the `CHECK` constraints the `TODO` lines name: severity, status, downtime between 0 and 1440,
locked_out 0 or 1, and minutes_spent between 1 and 720.

### Step 7. Add the two cross-field rules

Two table-level `CHECK` rules each span two columns: a critical issue must be locked out, and
`closed_at` is set exactly when the status is closed.

### Step 8. Turn foreign keys on and build the database

In `db.py`'s `connect`, add `conn.execute("PRAGMA foreign_keys = ON")`. Then:

```
python manage.py init --db instance/line3.db
git status
```

**Observable result:** the database is created and seeded. `git status` does not list
`instance/line3.db`. Every Part 1 line in the self-check is PASS (33 of 56 so far).

### Step 9. Draw the ER diagram

Draw the four tables, their keys, and the four relationships, with cardinality. Use a drawing tool,
an SVG, or the "relationships in words" text style from the data dictionary [MySQL Workbench if your
lab has it: VERIFY]. Save it in the lab folder.

**Acceptance criteria, Part 1.** Every Part 1 line is PASS. `git status` does not list the database.
Your README says why `home_phone` was removed. The ER diagram shows every table, key, and relationship.

---

## Part 2: values travel as parameters · Tuesday

### Step 10. Start the app

```
python app.py --port 8680
```

The read pages are broken: `list_issues` returns nothing and `get_issue` returns None. Stop the app.

### Step 11. Write `get_issue`

One issue by id, or None. Use `ISSUE_COLUMNS` and `ISSUE_FROM` and a `?` parameter.

### Step 12. Write `create_issue`

Read `add_note` below it first: same pattern. The form gives a machine code and a badge; the table
stores ids, so the `VALUES` list looks each one up with a subquery. End with `RETURNING id`. Do not
commit inside the function; the caller wraps it in a transaction.

### Step 13. Write `list_issues`

Build a `conditions` list and a `params` list. Each filter that is given adds one fixed condition
string and, when it has a value, one parameter. `open_only` adds a condition and no parameter.

### Step 14. Handle the search safely

The search matches the title or the description, ignores case, and treats `%`, `_`, and `\` as plain
text. The lab gives you the escape line in `db.py`'s `TODO`. Copy it exactly. The value goes in as a
parameter, never in the SQL text.

### Step 15. See an injection do nothing

Start the app. Search for `' OR '1'='1`.

**Observable result:** no issues match. The string was compared as text.

### Step 16. Search for a percent sign

Add an issue whose title contains `100%`, then search `100%`.

**Observable result:** only that issue matches.

### Step 17. Run the self-check

**Observable result:** every Part 2 line is PASS (50 of 56 so far).

**Acceptance criteria, Part 2.** Every Part 2 line is PASS. A search for an apostrophe or an injection
string returns a page, never an error.

---

## Part 3: a transaction makes many writes one change · Wednesday

### Step 18. Write `update_issue`

Change an issue and return True if a row changed. Closing it stamps `closed_at` once; saving a closed
issue again keeps the first time; reopening clears it. One `UPDATE` with `CASE WHEN` and `COALESCE`
does all three. The reporter never changes.

### Step 19. Write `delete_issue`

Delete an issue and return True if a row was deleted. Its work notes go with it, because of the
`ON DELETE CASCADE` you declared in Part 1.

### Step 20. See the delete confirmation

Start the app. Open an issue and click delete.

**Observable result:** an "are you sure?" page. The issue is still there. Only the confirm button, a
POST, deletes it.

### Step 21. Write `import_issues`

Insert the validated rows and return their ids, all inside one transaction, so a failure on any row
leaves the table as it was.

### Step 22. Import a bad file

```
python import_csv.py data/issues_import_bad.csv --db instance/line3.db
```

**Observable result:** `Nothing imported.` and four problem lines, each with its line number. The table
is unchanged.

### Step 23. Import the good file

```
python import_csv.py data/issues_import.csv --db instance/line3.db --dry-run
python import_csv.py data/issues_import.csv --db instance/line3.db
python manage.py tables --db instance/line3.db
```

**Observable result:** the dry run reports all rows valid and imports nothing. The real run imports
four issues. `manage.py tables` shows the new counts.

### Step 24. Run everything

```
python selfcheck_u05_01.py
python -m unittest
```

**Observable result:** `56 of 56 self-checks passed`, and 56 tests OK.

### Step 25. Commit

**Observable result:** the database file is not in the commit. `git status` is clean of it.

**Acceptance criteria, full lab.**
- [ ] `python selfcheck_u05_01.py` prints `56 of 56 self-checks passed`
- [ ] `python -m unittest` reports 56 tests, OK
- [ ] `git status` never lists a `.db` file
- [ ] A delete asks first; a GET deletes nothing
- [ ] A bad CSV file imports nothing and names every bad line
- [ ] The ER diagram is committed
- [ ] Committed and pushed

---

## If it breaks

### 1. Foreign keys "do not work": a bad reference is accepted

**Cause:** SQLite ignores foreign keys unless each connection runs `PRAGMA foreign_keys = ON`. Check
`connect` in `db.py`.

### 2. `sqlite3.OperationalError: no such table`

**Cause:** you have not run `manage.py init`, or you are pointing at a different database file.

### 3. `sqlite3.IntegrityError: CHECK constraint failed`

**Cause:** a value broke a rule you wrote in the schema. Read which constraint. That is the database
protecting the data, working as designed.

### 4. `database is locked`

**Cause:** another program has the file open with an unfinished write: a database browser, or a forgotten
Python shell. Close it.

### 5. Tests fail on Windows with "being used by another process"

**Cause:** a connection was still open when the temporary folder was deleted. The tests close
connections first; if your own code leaves one open, close it.

### 6. The search box breaks on an apostrophe

**Cause:** the query was built with an f-string somewhere. Every value goes in as a `?` parameter.

---

## Stretch goal

Add an index to the column your issue list filters by most, and write in your README one sentence on
what an index buys and what it costs. Read the SQLite `CREATE INDEX` documentation and cite it.

---

## Submission checklist

- [ ] `56 of 56 self-checks passed`
- [ ] 56 tests OK
- [ ] No `.db` file in any commit, ever
- [ ] The ER diagram committed
- [ ] Bad-file import refused with line numbers
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Part 1 not finished by the end of Monday, or the student is editing the tests to pass | SCAFFOLDED |
| Steady progress, questions about queries or transactions | STANDARD |
| 56 of 56 before Wednesday's Build 1 is half over | EXTENDED |
| The student says they will never touch a database | APPLIED |

---

## SCAFFOLDED

**Changed sections:**
- **Part 1:** the student receives the finished `issues` table and writes only the `work_notes` table
  and the `PRAGMA` line.
- **Part 2:** the student receives `get_issue` and `create_issue` written and writes `list_issues` with
  its filters.
- **Checkpoints:** show the self-check after each part.

**Acceptance criteria:** 56 of 56 self-checks, no `.db` in a commit, the ER diagram.

**Grading:** same 100-point scale.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a query the lab did not teach.

**Added requirement.** Add a sort the user picks: `/issues?sort=downtime` or `?sort=reported`. A column
name cannot be a `?` parameter, so map the allowed values to fixed column names with an allow-list, and
refuse anything else with 400. Write in your README why an allow-list is the only safe way to sort by a
user's choice.

**Acceptance criteria:** all STANDARD criteria; the two sorts work; an unknown sort value answers 400; a
test for each; the README explains the allow-list.

**Grading:** same scale.

---

## APPLIED

**For the student who will never touch a database.** The same design, for their own data.

**Changed scenario.** Design and build a small SQLite database for something the student actually
tracks: a game backlog, a car's maintenance, a team roster. At least three related tables with keys and
constraints, a seed script, and three queries: one join, one filtered list, and one count grouped by a
category. Every value goes in as a parameter. Draw the ER diagram.

**Acceptance criteria:** three related tables with real foreign keys and at least two `CHECK` rules; the
three queries run and return the right rows; the ER diagram matches the schema; no value is ever joined
into SQL text.

**Grading:** same scale. Requirements Fit is judged on whether the schema is normalized: no fact stored
twice.
