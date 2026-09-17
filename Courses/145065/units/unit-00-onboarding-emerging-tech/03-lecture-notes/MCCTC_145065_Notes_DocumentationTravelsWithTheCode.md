# Lecture Notes: Documentation Travels With the Code
## 145065 Object-Oriented Programming · Unit 0 · Week 1, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W01_DocumentationTravelsWithTheCode.md). There is no
exported deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-00-onboarding-emerging-tech/04-slides/MCCTC_145065_Slides_W01_DocumentationTravelsWithTheCode.md --export pptx`

If you missed class, you can learn this concept from this file alone.

**Competencies:** 5.1.8, describe version control and the relevance of documentation. 1.4.7, use
productivity applications to optimize assigned tasks.

---

## Why this exists

You already commit without thinking. A commit records **what** changed. It does not tell a stranger
how to run your project, or why you built it this way instead of another way.

That is the job of documentation. And documentation has a failure mode code does not: when it goes
wrong, nothing crashes. The README keeps saying the old thing, confidently, until somebody follows it.

This semester, three documents live in your repository from Week 1 to Week 18:

| File | Answers the question |
|---|---|
| `README.md` | What is this, and how do I run it today? |
| `decision-log.md` | Why is it built this way, and what did you reject? |
| the task board | What is left, what is in progress, and what is done? |

---

## The concept in plain language

**Documentation changes in the same commit as the code it describes.**

If a commit renames a file, the same commit updates every document that names that file. If a commit
changes how the program starts, the same commit updates the README's run section. The history then
stays true at every point, not only at the end.

### The decision log format for this course

Every entry names a decision, the option you chose, **the option you rejected**, why, and what the
choice costs you. Naming the rejected option is a syllabus rule for this course. It proves you
considered one.

```
## Week 1, Monday · Project environment
- Decision: how this project gets its Python
- Chosen: uv, with Python 3.14 pinned in .python-version
- Rejected: the machine-wide Python
- Why: the next machine rebuilds the same environment from committed files
- Cost: one more tool to install and learn
```

Date entries by week and day, as above.

### The semester task board

A task board is a productivity tool: cards in columns, usually `To do`, `Doing`, and `Done`. Yours
holds the course milestones for the whole semester, so you can see what is coming before it arrives.

Build it in **GitHub Projects**, which offers a board layout [VERIFY the menu path on your account].
If you cannot use GitHub Projects, use a `TASKBOARD.md` file in your repository with the same three
columns as headings. Either counts. What matters is that you move cards as the work moves.

No card holds anyone's personal information. Milestones and your own tasks only.

---

## Worked example 1: does the README have a run section

```python
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
lines = [line.strip() for line in readme.splitlines()]
print("Has a run section:", "## How to run" in lines)
```

With a README that contains the heading, the output is:

```
Has a run section: True
```

The code compares whole lines, so a sentence that happens to contain "how to run" does not count as
the heading.

---

## Worked example 2: does the README name a file that exists

The README in this example says `python check.py`. The folder holds `env_check.py`.

```python
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
for line in readme.splitlines():
    line = line.strip()
    if line.startswith("python ") and line.endswith(".py"):
        script = line.split()[1]
        found = "exists" if Path(script).is_file() else "MISSING"
        print(script, found)
```

Output:

```
check.py MISSING
```

A program caught what a reader would not: the README points at a file that is no longer there.

---

## Worked example 3: is the decision log entry complete

```python
entry = """## Week 1, Monday · Project environment
- Decision: how this project gets its Python
- Chosen: uv, with Python 3.14 pinned in .python-version
- Rejected: the machine-wide Python
- Why: the next machine rebuilds the same environment from committed files
"""
required = ["Decision:", "Chosen:", "Rejected:", "Why:", "Cost:"]
missing = [field for field in required if field not in entry]
print("Missing fields:", missing)
```

Output:

```
Missing fields: ['Cost:']
```

The entry reads well and is still incomplete. Every choice costs something. Say what.

---

## The wrong version, and the error it produces

Somebody renamed `check.py` to `env_check.py` and committed only the rename. The README still says:

```
## How to run

python check.py
```

A classmate follows it exactly:

```
python.exe: can't open file 'C:\\...\\oop-semester\\check.py': [Errno 2] No such file or directory
```

The code is fine. The documentation is wrong. The commit that renamed the file should have changed
the README too.

---

## Why the wrong version is tempting

When you rename a file, you are thinking about the code. The README is in another tab, and you
already know how to run the program, so you never read your own instructions. Nothing fails for you.
It fails for the next person.

The habit that prevents it: before every commit, ask "does any document name something I changed?"
Then have someone else follow your README literally, out loud. That test takes two minutes.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Version control** | a system that records every change to a set of files, who made it, and when |
| **Documentation** | writing that tells people how to use a system and why it is built as it is |
| **README** | the front page of a repository: what it is and how to run it |
| **Decision log** | a dated record of decisions, including the option rejected and the cost |
| **Task board** | cards in columns showing work to do, in progress, and done |
| **Stale documentation** | documentation that was true once and no longer matches the code |

---

## Self-check

**Question 1.** You change the program so it takes a folder name on the command line. Which document
must change in the same commit, and what must it now say?

**Question 2.** A decision log entry reads "Decision: use uv. Why: it is better." Name two things
missing or weak.

**Question 3.** Why does stale documentation usually go unnoticed by the person who wrote it?

---

### Answers

**1.** The README's run section. It must show the new command with the folder argument, for example
`python env_check.py path/to/folder`, and say what happens with no argument.

**2.** It names no rejected option, and "it is better" is not a reason anybody can check. It also has
no cost. A complete entry says what was rejected, a specific reason, and what the choice costs.

**3.** The author already knows how to run the program and never follows their own instructions, so
nothing fails for them. It fails for the next reader.
