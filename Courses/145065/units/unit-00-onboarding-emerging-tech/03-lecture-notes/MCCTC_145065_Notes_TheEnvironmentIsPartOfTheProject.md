# Lecture Notes: The Environment Is Part of the Project
## 145065 Object-Oriented Programming · Unit 0 · Week 1, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W01_TheEnvironmentIsPartOfTheProject.md). There is no
exported deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-00-onboarding-emerging-tech/04-slides/MCCTC_145065_Slides_W01_TheEnvironmentIsPartOfTheProject.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and a terminal.

**Competency:** 5.4.1, configure options, preferences, and tools.

---

## Why this exists

This semester your projects grow. In Week 7 you add Flask. In Week 9 you add a database. In Week 11
you add a second language. Each addition is a chance for your machine and the lab machine to
disagree.

"It works on my machine" is one of the most expensive sentences in software. It almost always means
two machines ran different Pythons, or the same Python with different packages, and nobody wrote down
which. This lesson makes your project write that down.

---

## The concept in plain language

A computer can have more than one Python on it. A **virtual environment** is a folder that belongs to
one project. It points at one Python, and it holds that project's packages and no others.

So a package can be installed on the machine and still be missing from your project. Both statements
are true at once.

The question you ask every time something behaves strangely is: **which Python is running this?**

The project records its environment in two small files that you commit:

- `.python-version` says which Python version the project uses.
- `pyproject.toml` lists the packages the project needs.

The `.venv` folder is the built environment. It is large, specific to one machine, and rebuilt from
those two files. It is never committed.

---

## Worked example 1: which Python is running this

```python
# where_am_i.py
# Which Python is running this file, and is it the project's environment?
import sys

print("Interpreter:", sys.executable)
print("Version:", sys.version_info[:2])
print("Inside a virtual environment:", sys.prefix != sys.base_prefix)
```

Run with the machine-wide Python on the build machine:

```
Interpreter: C:\Python313\python.exe
Version: (3, 13)
Inside a virtual environment: False
```

Run with a project environment's Python:

```
Interpreter: C:\...\demo-venv\Scripts\python.exe
Version: (3, 13)
Inside a virtual environment: True
```

The file did not change. The interpreter did. `sys.prefix != sys.base_prefix` is the check the
official `venv` documentation gives: inside an environment, the two point at different folders.

---

## Worked example 2: checking the version correctly

```python
import sys

print(sys.version_info >= (3, 13))
print("3.9" >= "3.13")
print((3, 9) >= (3, 13))
```

Output on Python 3.13.7:

```
True
True
False
```

The middle line is the trap. Strings compare one character at a time, and `"9"` comes after `"1"`,
so the string comparison claims 3.9 is newer than 3.13. `sys.version_info` is numbers in a tuple, and
tuples compare number by number. Always compare versions as numbers.

---

## Worked example 3: setting it up with uv

The lab machines use uv, which manages both the Python version and the packages. These commands are
from the uv documentation. **They were not run on the machine that built this file, so confirm them
on the lab machine [VERIFY].**

```
uv python install 3.14
uv init oop-semester
cd oop-semester
uv python pin 3.14
uv venv
uv run python where_am_i.py
```

What each one does:

| Command | What it does |
|---|---|
| `uv python install 3.14` | downloads Python 3.14 for uv to use |
| `uv init oop-semester` | creates the project folder with a `pyproject.toml` |
| `uv python pin 3.14` | writes `.python-version` so the project always uses 3.14 |
| `uv venv` | builds the `.venv` environment |
| `uv run python where_am_i.py` | runs the file with the project's environment |

**If uv is not available** on a machine you use, the standard library can build an environment:

```
python -m venv .venv
.venv\Scripts\python.exe where_am_i.py
```

That fallback was run on the build machine and produced the second output in example 1.

### Telling VS Code which Python to use

The Run button uses whichever interpreter VS Code was told to use, which may not be the terminal's.
Open the Command Palette and run **Python: Select Interpreter**, then choose the project's `.venv`.
The status bar shows the one in use.

### A Gate 1 profile

Gate 1 reps are done with no autocomplete. VS Code **Profiles** let you keep a separate set of
settings. Create a profile named `Gate 1` from the Profiles editor with **New Profile**, start it
empty, and put these in its settings [VERIFY the setting names on this year's VS Code]:

```json
{
    "editor.quickSuggestions": {"other": "off", "comments": "off", "strings": "off"},
    "editor.suggestOnTriggerCharacters": false,
    "editor.inlineSuggest.enabled": false,
    "editor.parameterHints.enabled": false,
    "editor.wordBasedSuggestions": "off"
}
```

Switch to this profile for every Gate 1 rep. Switch back for everything else. Any AI extension must
be absent from this profile.

---

## The wrong version, and the error it produces

```python
# needs_flask.py
# Week 7 will need Flask. Does this environment have it?
import flask

print("Flask is available in this environment")
```

On the build machine, with the machine-wide Python, which has Flask:

```
Flask is available in this environment
```

With the project environment, which does not:

```
Traceback (most recent call last):
  File "...\needs_flask.py", line 3, in <module>
    import flask
ModuleNotFoundError: No module named 'flask'
```

Same file, same computer, two results. The package is on the machine and not in the project.

The fix is to add the package to the project, which records it in `pyproject.toml`: `uv add flask`
[VERIFY]. You do that in Week 7, not today.

---

## Why the wrong version is tempting

Installing a package machine-wide makes the error go away immediately, and it feels like a fix. It
is not. Your project now depends on something no file in your repository mentions. The next machine
fails, and nothing tells that person why.

The habit that prevents it: add packages to the project, never to the machine, and when something
breaks, check which Python is running before you change anything.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Interpreter** | the program that reads and runs your Python file |
| **Virtual environment** | a project folder holding one Python link and that project's packages |
| **`.venv`** | the usual name for the environment folder. Never committed. |
| **`.python-version`** | a file naming the Python version the project uses. Committed. |
| **`pyproject.toml`** | a file listing the project and its packages. Committed. |
| **uv** | a tool that installs Python versions, builds environments, and manages packages |
| **Profile** | a named set of VS Code settings and extensions you can switch between |
| **Configure** | set the options, preferences, and tools a program uses. Exam code 5.4.1. |

---

## Self-check

**Question 1.** Your program works when you type `python app.py` in the terminal and fails from the
VS Code Run button with `ModuleNotFoundError`. Name the most likely cause.

**Question 2.** Which of these do you commit: `.venv`, `.python-version`, `pyproject.toml`? Why?

**Question 3.** What does `print("3.10" >= "3.9")` print, and why is it a bad way to compare versions?

---

### Answers

**1.** The terminal and the Run button are using different interpreters, and only one of them has the
package. Check `sys.executable` in the terminal and the interpreter in the status bar.

**2.** Commit `.python-version` and `pyproject.toml`, because they are how another machine rebuilds
the same environment. Do not commit `.venv`, because it is large, machine-specific, and rebuilt from
the other two.

**3.** It prints `False`. The strings are compared character by character, and at the third
character `"1"` comes before `"9"`, so the comparison claims 3.10 is older than 3.9. Compare tuples of
numbers instead: `(3, 10) >= (3, 9)` is `True`.
