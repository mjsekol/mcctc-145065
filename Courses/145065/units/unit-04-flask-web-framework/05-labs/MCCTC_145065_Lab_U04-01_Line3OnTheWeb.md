# Lab U04-01: Line 3 on the Web
## 145065 Object-Oriented Programming · Unit 4 · Week 7

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Week 7, Monday through Thursday, one
part a day. **Competencies:** 1.7.13 (protect intellectual property, the licenses on Flask and its
dependencies), 5.5.2 (reuse libraries), 5.5.7 (read inputs: the URL and query string), 5.3.5
(conditional structures in a view), 5.5.6 (format output), 5.5.5 (naming and comments), 5.3.11 (access
a data repository from routes), 5.5.1 (validate loaded data), 5.3.10 (error handling).

Files: `lab-u04-01-files/`. The app is a copy of the course's Line 3 Maintenance Log with four parts
taken out, one per day. Every removed part is marked with a `TODO` that names its lab part.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop used all semester.
Every machine, badge, and record in the store is invented. No hardware is used.

---

## The scenario

The Line 3 supervisor keeps a maintenance log. Right now it is a JSON file that a program on your
machine reads. This week you put it on a web page, so the supervisor opens it in a browser instead of
reading the file. Nobody types into it yet. That is next week.

## What you will build

A Flask app with six routes, one layout that every page extends, and a store that is read and checked
on every request, so a broken file gives a clear page instead of a crash.

---

## Starter code

Copy `lab-u04-01-files/` into a folder in your `oop-semester` repository. Then, from that folder, in a
project environment that has Flask:

```
python -m unittest
python selfcheck_u04_01.py
```

The tests fail and the self-check reports `10 of 33 self-checks passed`. That is correct: the four
parts are not written yet. Read `app.py` and `store.py` top to bottom before you write anything. Every
`TODO` names its part.

Run the app to see what already works:

```
python app.py --port 8680
```

Open `http://127.0.0.1:8680/`. The dashboard and the request trace work. `/issues/1` answers 404,
because you have not fixed the rule yet. Stop the server with Ctrl+C.

---

## Part 1: someone else's code · Monday

Flask is code you did not write. Before you build on it, find out what it is and what its license lets
you do.

### Step 1. See what came with Flask

```
python licenses.py
```

**Observable result:** seven lines, Flask and the six packages it installed, each with a version and a
license. Two say only "BSD License" with no number.

### Step 2. Write the license record

Open each package's `LICENSE` file. It is inside that package's `.dist-info` folder in your
environment (for example `jinja2-3.1.6.dist-info`). A BSD file with three numbered conditions, the
third beginning "Neither the name," is the 3-clause BSD license.

Write `LICENSES.md` with a row for each of the seven packages: the package, its version, its license,
where you confirmed it, and what the license lets this project do. For the two that said only "BSD
License," name the variant after you read the file.

**Observable result:** `python selfcheck_u04_01.py` shows all eight Part 1 lines as PASS.

**Acceptance criteria, Part 1.**
- [ ] Flask is in your project environment (`python -c "import flask"` prints nothing and exits 0).
- [ ] `LICENSES.md` has a row for all seven packages with a real license each.
- [ ] The two "BSD License" rows name the variant, confirmed from the file.

---

## Part 2: the request cycle · Tuesday

Read `lab-u04-01-files/TRACE.md` first. It walks one request through ten steps with real server output.

### Step 3. Fix the issue rule

`GET /issues/1` answers 404, but issue 1 exists. Start the app, request `/issues/1`, and read the
`[trace]` line the server prints. Then open `app.py` and find the `issue_detail` rule. The bug is in
the rule, not the function body.

**Observable result:** `/issues/3` shows issue 3. `/issues/three` still answers 404, and its trace line
shows the endpoint as `None`.

### Step 4. Refuse an unknown status

In `list_issues`, read `status` from the query string. A status the program does not know is a bad
request. Use `abort(400, description="Unknown status. Use one of: ...")` and list the statuses. Pass
the status to `store.issues()` and to the template.

**Observable result:** `/issues?status=closed` shows only closed issues. `/issues?status=everything`
shows the 400 page with "Unknown status."

### Step 5. Check sequence against the tests

```
python selfcheck_u04_01.py
```

**Observable result:** every Part 2 line is PASS.

### Step 6. Commit

**Observable result:** a commit whose message says the request cycle is working.

**Acceptance criteria, Part 2.** Every Part 2 line in the self-check is PASS.

---

## Part 3: templates · Wednesday

### Step 7. Count open issues in one pass

In `list_equipment`, count the open issues for each machine. Do it in one pass over
`store.open_issues()`, not one pass per machine. Build a dictionary from machine code to a number.

**Observable result:** the program runs. The equipment page is still a placeholder.

### Step 8. Build the equipment page

Write `templates/equipment.html`. It extends `base.html`, fills the `title`, `heading`, and `content`
blocks, and shows every machine with its open count. Then render it from `list_equipment`.

**Observable result:** `/equipment` shows six machines. OV-01 shows 1 open issue.

### Step 9. Build the machine page

Write `templates/equipment_detail.html` and finish `equipment_detail`. Look the machine up with
`store.get_equipment(code)`. No machine is a 404. Otherwise show the machine and its issues, using the
shared `_issue_table.html` include. **Never put `code` into a return string:** it is text the visitor
typed, and it belongs in a template, which escapes it.

**Observable result:** `/equipment/OV-01` shows the oven and its two issues. `/equipment/XX-99` answers
404.

### Step 10. Check every page extends the base

**Observable result:** no template has its own `<header>` or `<footer>`. Every Part 3 line in the
self-check is PASS.

### Step 11. See the layout change once, everywhere

Change the footer text in `templates/base.html`. Reload two different pages.

**Observable result:** both pages show the new footer. Change it back so the composite note stays
correct.

### Step 12. Commit

**Acceptance criteria, Part 3.** Every Part 3 line in the self-check is PASS. No page repeats the
header or footer.

---

## Part 4: reading the store · Thursday

### Step 13. Turn a store error into a page

The store raises `StoreError` when the file is wrong. Right now that becomes a 500 and a traceback.
Register `@app.errorhandler(StoreError)`. Print the error type and message to `sys.stderr`, starting
with `[store] `. Answer with `error.html`, code 503, the title "The maintenance log is unavailable,"
and a message that tells the user what to do. **Do not put the error's text on the page.**

**Observable result:** with a broken store, the page says the log is unavailable and the terminal
shows the `[store]` line.

### Step 14. See both versions

Copy `data/line3_log.json` somewhere safe. Add a second comma after one `"downtime_minutes": 90,` in
the working copy. Start the app and open `/`.

**Observable result:** the 503 page, and a `[store]` line in the terminal naming the JSON error. If
your handler is not written yet, you get a 500 and a traceback instead. Restore the file from your copy.

### Step 15. Add two store checks

Open `store.py`. Two checks are missing, each marked with a `TODO`: an issue must point at a machine
that exists, and downtime cannot be negative. Write both, raising `StoreFormatError` with the message
the `TODO` gives.

**Observable result:** every Part 4 line in the self-check is PASS.

### Step 16. Run everything

```
python selfcheck_u04_01.py
python -m unittest
```

**Observable result:** `33 of 33 self-checks passed`, and 25 tests OK.

**Acceptance criteria, full lab.**
- [ ] `python selfcheck_u04_01.py` prints `33 of 33 self-checks passed`
- [ ] `python -m unittest` reports 25 tests, OK
- [ ] `LICENSES.md` names all seven packages with confirmed licenses
- [ ] A broken store gives a 503 page, never a traceback on the page
- [ ] You did not change `models.py`, `test_app.py`, or the templates you were not asked to write
- [ ] Committed and pushed

---

## If it breaks

### 1. `ImportError: cannot import name 'Flask' from 'flask'`

```
ImportError: cannot import name 'Flask' from 'flask' (consider renaming '...\flask.py' ...)
```

**Cause:** you named a file `flask.py`, so Python imports your file instead of the library. Rename it.
Python looks in your own folder first.

### 2. A page you wrote answers 404

Read the trace line. `-> None -> 404` means no rule matched: check the rule text and its converter.
`-> issue_detail -> 404` means your function ran and called `abort(404)`: check the id or the lookup.

### 3. `jinja2.exceptions.TemplateNotFound: equipment.html`

**Cause:** the file is missing or misnamed, or it is not in the `templates` folder next to `app.py`.

### 4. The page renders with status 200 and nothing in the middle

**Cause:** a block name is misspelled, so Jinja threw the content away. Check `{% block content %}`
against `base.html`. This one does not raise an error.

### 5. `TypeError: 'NoneType' object is not ...` in `equipment_detail`

**Cause:** the machine was not found and you used it anyway. Check for `None` and `abort(404)` first.

---

## Stretch goal

Extend `licenses.py` so it also prints, for each package, the path to its `LICENSE` file and how many
numbered conditions the file contains. Then your `LICENSES.md` "where I confirmed it" column can name
the exact file. Write in your README what you found for the two "BSD License" packages.

---

## Submission checklist

- [ ] `33 of 33 self-checks passed`
- [ ] 25 tests OK
- [ ] `LICENSES.md` complete
- [ ] Broken-store 503 confirmed and the store restored
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Part 2 not reached by the end of Tuesday, or the student is editing `models.py` or the tests to make the checks pass | SCAFFOLDED |
| Steady progress, questions about the store or the templates | STANDARD |
| 33 of 33 before Thursday's Build 1 is half over | EXTENDED |
| The student says they will never build a web app | APPLIED |

---

## SCAFFOLDED

**Changed sections:**
- **Part 3:** the student receives `templates/equipment.html` already written and writes only
  `templates/equipment_detail.html` and the two view functions.
- **Checkpoints:** show the self-check to the instructor after Part 2 and after Part 3.
- **Keep Part 4.** The broken-store lesson is the point of the week.

**Acceptance criteria:** 33 of 33 self-checks, `LICENSES.md` complete, the store restored.

**Grading:** same 100-point scale. Full completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a route the lab did not teach.

**Added requirement.** Add `GET /health` that returns JSON: whether the store loaded, and how many
issues and machines it holds, and nothing else. A broken store answers 503 with `{"store": "unavailable"}`
and no error text. Do not use Flask's `jsonify` from memory: read the "APIs with JSON" section of the
Flask documentation at `https://flask.palletsprojects.com/` and cite it in your README.

**Acceptance criteria:** all STANDARD criteria; `/health` answers 200 with the counts on a good store
and 503 with no detail on a broken one; a test for each.

**Grading:** same scale.

---

## APPLIED

**For the student who will never build a web app.** The same request cycle, as a command-line tool.

**Changed scenario.** Write a command-line program `log.py` that reads the same
`data/line3_log.json` through `store.py` and answers "routes" typed as commands: `issue 3`,
`issues open`, `equipment OV-01`, `equipment`. An unknown command or a missing record prints a clear
message and exits with a non-zero code, the way a 400 or 404 answers on the web. Reuse `store.py`
unchanged.

**Acceptance criteria:** each command prints the right records; an unknown status prints an "unknown"
message and exits non-zero; a broken store prints the "unavailable" message, not a traceback; you
reused `store.py` without editing it.

**Grading:** same scale. Requirements Fit is judged on whether the command-line answers match the
web answers for the same data.
