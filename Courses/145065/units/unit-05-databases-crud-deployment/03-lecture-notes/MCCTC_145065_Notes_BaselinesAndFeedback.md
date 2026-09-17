# Lecture Notes: A Baseline Is the Version Every Change Is Measured Against
## 145065 Object-Oriented Programming · Unit 5 · Week 10, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W10_Baselines.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-05-databases-crud-deployment/04-slides/MCCTC_145065_Slides_W10_Baselines.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python, Flask, Git, and
a copy of `05-labs/lab-u05-02-files/` outside any repository.

**Competencies:** 5.7.2 explain baseline and software lifecycle phases. 5.6.17 collect application
feedback and maintain the application. 5.6.15 train stakeholders, previewed only: watching a tester is
feedback, and Unit 9 teaches training.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. Every badge and record in this file is invented.

---

## Why this exists

Tomorrow, someone who has never seen your app will find a problem in it. You will fix it and deploy
again. Then a question comes that you cannot answer without today's idea: **which version did they
use, and is the fix in the live copy?**

"It worked yesterday" is a guess unless you know exactly what yesterday was. A **baseline** is the
answer. It is the version everyone agreed on, recorded so precisely that every later change can be
measured against it.

5.7 is 5.49 percent of the WebXam, and today is the first time this course teaches any of it.

---

## The concept in plain language

**A baseline is the agreed version that every later change is measured against.** For your app, it is
the first version you deployed for someone outside the class: **v1.0.0**.

**The version is written in three places, and all three must agree:**

1. `APP_VERSION` in `app.py`, which the page footer shows
2. the newest row of the version table in `RELEASE.md`
3. what the live app answers at `/health`

If they disagree, the next person to read any one of them is misled.

**The numbers mean something.** Versions here follow a common pattern called **semantic versioning**,
written `MAJOR.MINOR.PATCH`:

| Part | Goes up when | From 1.0.0 |
|---|---|---|
| **MAJOR** | a change breaks something people rely on, such as a removed page or a changed address | 2.0.0 |
| **MINOR** | a new feature arrives and nothing old breaks | 1.1.0 |
| **PATCH** | a bug is fixed and nothing else changes | 1.0.1 |

When one number goes up, the numbers to its right go back to 0. The outside tester's fix tomorrow is a
PATCH: 1.0.0 becomes 1.0.1.

**A Git tag marks the exact commit you deployed.** A branch moves every time you commit. A tag stays on
one commit. An **annotated** tag, made with `-a`, also records who made it, when, and a message. A
plain tag records none of that.

**The lifecycle, in the order you lived it this unit:** plan (the Week 9 timeline), design (the schema
and ER diagram), build (CRUD, the report, the configuration), test (the suite and the rehearsal),
deploy, and maintain. The baseline marks the moment the app moved from "being built" to "being
maintained." Every change after it is maintenance, and each one gets a version and a row.

**Feedback is part of maintenance (5.6.17).** You cannot see your own app the way a stranger does. You
know where every button is, because you put it there. An outside user test shows you what the app
looks like to someone who does not.

---

## Worked example 1: does every place agree

`release_check.py`, in the Lab U05-02 files, reads all three places and compares them. Run it from the
folder that holds `app.py`:

```
python release_check.py
```

On the finished lab app, with a `RELEASE.md` whose table has one row for 1.0.0, the output was:

```
app.py APP_VERSION       1.0.0
RELEASE.md newest row    1.0.0
GET /health              1.0.0
OK: release 1.0.0 is consistent.
```

It exited with status 0. The third line did not come from a server. The script builds the app with a
throwaway database in a temporary folder and asks `/health` through Flask's test client, so it works
before you deploy.

On the **starter**, before Part 4, `RELEASE.md` has a table heading and no version rows. The output was:

```
app.py APP_VERSION       1.0.0
RELEASE.md newest row    None
GET /health              1.0.0
MISMATCH: fix every place before you deploy or tag.
```

That mismatch is your Part 4 to-do list.

---

## Worked example 2: which number moves

```python
# semver.py
# MAJOR.MINOR.PATCH: which number moves, and how versions compare.


def bump(version, kind):
    major, minor, patch = (int(part) for part in version.split("."))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    if kind == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"unknown kind {kind!r}")


def as_tuple(version):
    return tuple(int(part) for part in version.split("."))


print("a typo fixed on the form:   1.0.0 ->", bump("1.0.0", "patch"))
print("a late-returns column added: 1.0.1 ->", bump("1.0.1", "minor"))
print("every bookmarked URL moved: 1.1.0 ->", bump("1.1.0", "major"))
print("as text,   '1.10.0' > '1.9.0':", "1.10.0" > "1.9.0")
print("as numbers, 1.10.0 > 1.9.0: ", as_tuple("1.10.0") > as_tuple("1.9.0"))
```

Output:

```
a typo fixed on the form:   1.0.0 -> 1.0.1
a late-returns column added: 1.0.1 -> 1.1.0
every bookmarked URL moved: 1.1.0 -> 2.0.0
as text,   '1.10.0' > '1.9.0': False
as numbers, 1.10.0 > 1.9.0:  True
```

- The MINOR bump reset PATCH to 0. The MAJOR bump reset both.
- Moving every address people bookmarked is MAJOR, because it breaks something people rely on, even
  though no code crashed.
- **Versions are not text.** Compared as text, `"1.10.0"` comes before `"1.9.0"`, because the
  character `1` sorts before `9`. Compared as numbers, 10 is greater than 9. Any code that sorts or
  compares versions must split them into numbers first.

---

## Worked example 3: the format is part of the promise

`release_check.py` finds version rows with a pattern. This example uses the same pattern on a table
where one row was typed carelessly.

```python
# newest_row.py
# How release_check.py finds the newest version in RELEASE.md's table.
import re

ROW = re.compile(r"^\| (\d+\.\d+\.\d+) \|", re.MULTILINE)

release_notes = """
| Version | Change | Why | Found by |
|---|---|---|---|
| 1.0.0 | Baseline | First deployment | |
| 1.0.1 | Return button is bigger | Tester missed it twice | outside tester |
|1.0.2| Typo in the footer | Seen in the demo | me |
"""

print("rows found:", ROW.findall(release_notes))
print("newest:", ROW.findall(release_notes)[-1])
```

Output:

```
rows found: ['1.0.0', '1.0.1']
newest: 1.0.1
```

The 1.0.2 row has no spaces around its bars, so the pattern skipped it. The checker now believes 1.0.1
is newest. If `app.py` says 1.0.2, you get a mismatch, and the cause is a missing space. Keep every row
in the exact shape the header shows: `| 1.0.2 | ... |`.

---

## Tagging the baseline

These are standard Git commands. **They were not run on the course build machine**, so no output is
quoted here. Run them in your own project repository after the deploy passes its checklist:

```
git tag -a v1.0.0 -m "Baseline: first deployed release of the tool crib app"
git push origin v1.0.0
git show v1.0.0 --stat
```

- The first line makes an annotated tag named `v1.0.0` on the commit you have checked out. Check that
  it is the commit you deployed before you run it.
- The second line sends the tag to GitHub. A plain `git push` does not send tags.
- The third line shows the tag's message, who made it, when, and the files in that commit. Read it and
  confirm it is the commit you expected.

Why tag at all, when the commit already has an id? Because "v1.0.0" is a name a person can say out
loud, write in `RELEASE.md`, and type a year from now. Nobody remembers a commit id.

---

## The outside user test

Build 2 today. Someone outside the class uses your deployed app for ten minutes. You watch.

**Before they start:**

- Give them an **invented badge** from your seed data, such as T-1041. They type **no real personal
  information** into your app: not their name, email, or phone number. The tester is a real person, and
  a class project never records a real person's data.
- Have `USER_TEST.md` open, and a clock you can see.

**What you say, and nothing more:**

> Please try to check out a tool, return it, and find the report. Think out loud.

**While they work:**

- **Do not help.** Do not point. Do not say "it's up there." Do not explain. The first time you help,
  the test stops measuring your app and starts measuring you.
- If they ask a question, say "What would you try?" and write the question down. A question is a
  finding.
- Write down every pause, every wrong click, every error, and every time they say something like "I
  guess," each with the time.
- Keep your face neutral. A tester who sees you wince starts trying to please you.

**This is the hardest part of the day.** Watching someone struggle with something you built, and saying
nothing, is uncomfortable. It is also the only way to see what they see.

**Afterward, in `USER_TEST.md`:**

- Who tested, as a **role**, never a name: "a teacher from another program."
- What you asked them to do.
- Every problem: what they did, what they expected, and what happened.
- Each problem sorted: **fix now** (goes into 1.0.1), **fix later**, or **not a problem**, with a reason
  for each.

Tomorrow you fix the "fix now" list, change the version to 1.0.1 in every place, add a `RELEASE.md` row,
run `release_check.py`, deploy, and show `/health` answering 1.0.1. That loop, collect feedback and
maintain the app, is 5.6.17.

---

## The wrong version, and the output it produces

Add a `1.0.1` row to `RELEASE.md` and change nothing else:

```
| 1.0.1 | The checkout form names the missing field | The outside tester could not tell what was wrong | outside tester |
```

`release_check.py` printed:

```
app.py APP_VERSION       1.0.0
RELEASE.md newest row    1.0.1
GET /health              1.0.0
MISMATCH: fix every place before you deploy or tag.
```

It exited with status 1.

The release notes say the fix shipped. The app says it did not. The tester's supervisor reads the notes,
believes the problem is solved, and sends the tester back to the same broken form. **A baseline is only
useful when every place agrees.**

---

## Why the wrong version is tempting

Writing the release note feels like finishing the job. It is the part you write last, with the fix
fresh in your mind, and it reads like proof. Changing `APP_VERSION` is one line in a different file, and
nothing breaks if you forget it. Every page still loads. Every test that does not check the version
still passes.

The same trap waits in the other direction: bump `APP_VERSION`, deploy, and never write the row. Then
the live app claims a version nobody can look up.

The habit that prevents it: change the version in every place in the same commit, and run
`release_check.py` before every deploy and every tag.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Baseline** | the agreed version that every later change is measured against |
| **Release** | a named version made available to users |
| **Semantic versioning** | numbering a release `MAJOR.MINOR.PATCH` by what kind of change it holds |
| **Tag** | a name Git keeps on one commit, even after more commits |
| **Annotated tag** | a tag that also records who made it, when, and a message |
| **Release notes** | the record of what each version changed, why, and who found the need |
| **Software lifecycle** | plan, design, build, test, deploy, maintain |
| **Maintenance** | every change after the baseline |
| **Outside user test** | a person who has never seen the app uses it while you watch and do not help |

---

## Self-check

**Question 1.** Your tester's first problem needs a fix to the checkout form. Their second is a request
for a new "tools due today" page. Starting from 1.0.0, what version numbers do the two changes get, if
you ship the fix first?

**Question 2.** Explain "baseline" in one sentence, and say how Git remembers it.

**Question 3.** During the test, your tester stops and asks, "Where do I put the badge?" What do you
say, and what do you write down?

---

### Answers

**1.** The fix is a PATCH: 1.0.0 becomes 1.0.1. The new page is a new feature that breaks nothing, so it
is a MINOR: 1.0.1 becomes 1.1.0, and PATCH goes back to 0.

**2.** A baseline is the agreed version that every later change is measured against. Git remembers it
with an annotated tag, such as `v1.0.0`, on the exact commit that was deployed.

**3.** Say "What would you try?" and nothing that points the way. Write down the question, the time, and
what they did next. The question itself is a finding: the badge field was not where they looked for it.
