# Lab U0-01: Environment Check
## 145065 Object-Oriented Programming · Unit 0 · Week 1

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 2 (Part 1) and Tuesday
Build 1 (Part 2). **Competencies:** 5.4.1 (configure options, preferences, and tools), 5.1.8
(version control and documentation), 5.3.4 (relational operators and compound conditions), 5.3.9
(create and call functions), 5.2.4 (string operations), 5.5.5 (naming conventions and comments).

Files: `lab-u00-01-files/env_check.py` (starter) and `lab-u00-01-files/selfcheck_env.py`.

---

## The scenario

Every semester somebody loses a class period because their machine is set up differently from the
lab's and nobody can tell how. This semester adds Flask, a database, and a second language, so the
chances multiply. Your instructor wants one command that says, in plain words, whether a machine and
a project folder are ready.

## What you will build

A program, `env_check.py`, that runs seven checks on your machine and your project folder and prints
PASS or FAIL for each, with a detail a person can act on.

**Monday you check the machine. Tuesday you check the folder.** Two different problems, two sittings.

---

## Starter code

Copy both files from `lab-u00-01-files/` into your `oop-semester` project folder. Run the starter.

```
python env_check.py
```

It runs and checks nothing:

```
ENVIRONMENT CHECK
-----------------
No checks written yet.
```

Every check function returns `None` for now. When you write one, it must return a tuple of three
things: `(name, passed, detail)`. For example:

```python
("Python version", True, "found 3.14, need 3.13 or newer")
```

One shape for every check means `print_report` can print all of them the same way.

**Why the functions have default arguments.** `check_python_version(version_info=sys.version_info)`
uses the real interpreter when you call it with nothing. `selfcheck_env.py` calls it with a fake
version, such as `(3, 9, 18)`, so it can test a machine you do not have. Keep those parameters and
use them inside the function.

---

## Part 1: Monday, steps 1 through 6

### Step 1. Run the starter and the self-check

```
python env_check.py
python selfcheck_env.py
```

**Observable result:** the checker prints `No checks written yet.` The self-check prints 16 lines
that start with `NOT WRITTEN` and ends `0 of 16 self-checks passed`. Commit the two files.

### Step 2. Write `check_python_version`

Compare the running version with `MINIMUM_PYTHON`. Build a tuple of the first two numbers from
`version_info` and compare tuples. **Do not compare strings.** This morning's bell ringer showed why.

The detail reads like `found 3.14, need 3.13 or newer`.

**Observable result:** `python selfcheck_env.py` shows the first four lines as `PASS`.

### Step 3. Write `check_virtual_environment`

Inside a virtual environment, `prefix` and `base_prefix` are different folders. Outside one, they are
the same. Use the parameters, not `sys.prefix` directly.

If it fails, the detail tells the person what to do.

**Observable result:** self-check lines 5 and 6 show `PASS`.

### Step 4. Write `check_git_available`

`finder("git")` returns the path to git, or `None` if it cannot be found. This searches the same
places your terminal searches. It does not run git.

**Observable result:** self-check lines 7 and 8 show `PASS`.

### Step 5. Run it for real, both ways

Run the checker with the project's environment, then with the machine-wide Python.

```
uv run python env_check.py
```

and, from a terminal where the environment is not active, `python env_check.py`.

**Observable result:** three `PASS` lines with the environment. With the machine-wide Python, the
virtual environment line says `FAIL`, and its detail tells you what to do. If your terminal's
`python` is already the project's, the two runs will match. Say why in your commit message.

### Step 6. Commit

**Observable result:** `git log --oneline` shows a commit whose message says what the checker can
now check.

### Acceptance criteria, Part 1

1. `python selfcheck_env.py` shows the first 8 self-checks as `PASS`.
2. The version check compares tuples, never strings.
3. Every `FAIL` detail tells a person what to do or what was found.
4. Part 1 is committed.

---

## Part 2: Tuesday, steps 7 through 12

### Step 7. Write `check_required_files`

Report every name in `REQUIRED_FILES` that is not a file in `folder`. `folder` is a `Path`, so
`folder / name` builds the path and `.is_file()` answers the question.

**Observable result:** self-check lines 9 and 10 show `PASS`. The detail on a failure names the
missing files.

### Step 8. Write `check_repository`

A folder is a Git repository when it contains a `.git` folder. Check for the folder. Do not run git.

**Observable result:** self-check lines 11 and 12 show `PASS`.

### Step 9. Write `check_gitignore`

Read `.gitignore` and report every entry in `IGNORE_MUST_LIST` it does not list. Treat `.venv/` and
`.venv` as the same entry. If there is no `.gitignore`, fail with a detail that says so rather than
crashing.

**Observable result:** self-check lines 13 and 14 show `PASS`.

### Step 10. Write `check_readme_run_section`

Pass only when `README.md` has a line that reads exactly `## How to run`, ignoring spaces at the ends.
A sentence that mentions "how to run" in passing does not count.

**Observable result:** self-check shows `16 of 16 self-checks passed`.

### Step 11. Add a summary and an exit code

After the checks, print a line such as `5 of 7 checks passed`. Make `main` return `0` when every
check passed and `1` otherwise. Once every check is written, `run_checks` no longer needs to filter
out `None`.

**Observable result:** run it on your own `oop-semester` folder. Read every `FAIL`, fix your folder
(not your checker), and run it again until it prints `7 of 7 checks passed`. In PowerShell,
`echo $LASTEXITCODE` then prints `0`.

### Step 12. Break your README on purpose, then commit

Change the `## How to run` line to `## Running it`. Run the checker.

**Observable result:** `README run section` fails, the summary says `6 of 7`, and the exit code is
`1`. Put the line back, confirm `7 of 7`, and commit the checker and the README together.

### Acceptance criteria, full lab

- [ ] `python selfcheck_env.py` prints `16 of 16 self-checks passed`
- [ ] `python env_check.py` in your project folder prints `7 of 7 checks passed`
- [ ] Exit code is `0` when everything passes and `1` when anything fails
- [ ] No check crashes when a file is missing. It fails with a detail instead.
- [ ] The version check compares numbers
- [ ] No check runs git
- [ ] Names say what things are. Comments say why.
- [ ] Your README's run section is true, and a partner has followed it
- [ ] At least three commits across the two days

---

## The semester milestones, for Tuesday's task board

One card per row. Your instructor confirms external event dates each year.

| Milestone | When |
|---|---|
| Emerging technology brief | Week 1 Fri |
| BPA State pre-submission (competitors) | usually Week 1, confirm the date |
| Refactor project: 145060 code into classes | Week 3 Fri |
| BPA State Leadership Conference (competitors) | usually Week 4, confirm the date |
| Class hierarchy project | Week 5 Fri |
| Problem drop | Week 6 |
| Grading Period 3 exam | Week 9 Thu |
| CRUD web application deployed | Week 10 |
| Python to C# port | Week 12 Fri |
| WPF application | Week 14 Fri |
| BPA National Leadership Conference (qualifiers) | usually Week 14, confirm the date |
| WebXam post-test | Week 16 |
| Final demonstrations and Grading Period 4 exam | Week 18 |

---

## If it breaks

### 1. The self-check cannot find your checker

```
Traceback (most recent call last):
  File "...\selfcheck_env.py", line 15, in <module>
    import env_check
ModuleNotFoundError: No module named 'env_check'
```

**Cause:** `selfcheck_env.py` is not in the same folder as `env_check.py`, or your file has a
different name. Put both files in one folder, named exactly as given.

### 2. Comparing the version string with a tuple

```
TypeError: '>=' not supported between instances of 'str' and 'tuple'
```

**Cause:** you used `sys.version`, which is a string, against `MINIMUM_PYTHON`, which is a tuple.
Use the `version_info` parameter and build a tuple from its first two numbers.

### 3. A check returns the wrong shape

```
TypeError: cannot unpack non-iterable bool object
```

or

```
ValueError: not enough values to unpack (expected 3, got 2)
```

**Cause:** a check returned `True`, or a tuple of two things. `print_report` expects three:
`(name, passed, detail)`. Find the `return` line and add what is missing.

### 4. A missing file crashes the check

```
FileNotFoundError: [Errno 2] No such file or directory: '...\\.gitignore'
```

**Cause:** you read the file before checking it exists. Check `path.is_file()` first, and return a
failing tuple if it does not.

### Not an error, and the most dangerous result: a version check that always passes

If you compare strings, `"3.9" >= "3.13"` is `True`. Your checker passes an old Python and never
complains. That is why the self-check tries 3.9 on purpose.

---

## Stretch goal

Add an eighth check: `check_no_env_file_staged`. It fails when a file named `.env` exists in the
folder **and** `.env` is missing from `.gitignore`. Write the result in your decision log: which
option you chose for combining this with the existing `.gitignore` check, and which you rejected.

---

## Submission checklist

- [ ] `selfcheck_env.py` prints 16 of 16
- [ ] `env_check.py` prints 7 of 7 on your own `oop-semester` folder
- [ ] You ran the step 12 break and saw exit code 1
- [ ] README, `.gitignore`, and `decision-log.md` are committed
- [ ] `git status` shows nothing uncommitted
- [ ] Pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At 15 minutes into Build 2, step 2 still fails, or the student is comparing strings after the bell ringer | SCAFFOLDED |
| Working through the steps, questions are about wording and details | STANDARD |
| Part 1 finished in under 20 minutes with 8 of 8 self-checks | EXTENDED |
| The student asks why anyone would need this, or says their own machine is fine | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** `check_git_available` and `check_repository` are written for the student. Ask
  them to read both aloud before they start. They serve as the pattern for the rest.
- **Steps:** Part 1 is steps 2, 3, and 5 only. Part 2 is steps 7, 9, and 11 only.
- **Checkpoints:** show your instructor the self-check after step 2 and after step 7.
- **Keep step 12.** Breaking the README on purpose is the most valuable minute in the lab.

**Acceptance criteria:** the self-check passes for every check the student wrote. `env_check.py`
reports 7 of 7 on the student's folder. The version check compares tuples.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. A student
who completes this version fully earns the same grade as one who completes STANDARD fully.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a feature that needs a module you have not been taught.

**Added requirement.** Add a `--json` option. `python env_check.py --json` prints the results as a
JSON list of objects with the keys `name`, `passed`, and `detail`, and prints nothing else. Without
the option, the output is unchanged. The folder argument must still work with or without `--json`.

**Hint, not the answer.** Reading options by hand from `sys.argv` gets messy fast. The standard
library has a module built for it. Read the tutorial linked from the top of
`https://docs.python.org/3/library/argparse.html` and find how to declare an option that is either
present or absent. You already know the module that turns a list of dictionaries into JSON text.

**Why this matters.** A person reads the text report. Another program reads the JSON. That is the
difference between output for people and output for machines, and it comes back in Unit 4.

**Acceptance criteria:** all STANDARD criteria, plus `--json` output that `json.loads` can parse, and
a decision log entry naming the option you rejected for reading arguments.

**Grading:** same scale. An attempt documented honestly loses little. Code the student cannot
explain fails the course standard.

---

## APPLIED

**For the student who asks when anyone would use this.** Same skill, different domain.

**Changed scenario.** Your robotics, esports, or band team packs a laptop for a competition, and
every trip somebody discovers the wrong software version on site. Write `trip_check.py` for a folder
your team would actually bring: a match program, a settings file, and a notes file.

**What you build.** At least five checks, each a function returning `(name, passed, detail)`:

- a version number compared as a tuple, such as the version of a game or a tool written in a
  settings file as `version=2.10`
- at least two required files
- a settings file that must list certain keys
- one more check you choose and justify

Each check takes its inputs as parameters, so you can test it with a fake value. Write a small
self-check of your own with at least eight cases, including one version that string comparison would
get wrong.

**Acceptance criteria:** five checks, a summary line, the exit code rule, your own self-check passing,
and a README with a true `## How to run` section.

**Grading:** same scale. Requirements Fit is judged on whether the checks match what the student's
team would really need, which is a harder question than the standard version asks.
