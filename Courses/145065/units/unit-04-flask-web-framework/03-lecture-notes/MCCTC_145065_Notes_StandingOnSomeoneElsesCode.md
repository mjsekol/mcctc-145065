# Lecture Notes: Standing on Someone Else's Code
## 145065 Object-Oriented Programming · Unit 4 · Week 7, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W07_SomeoneElsesCode.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W07_SomeoneElsesCode.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and a project
environment with Flask installed.

**Competencies:** 1.7.13 protect intellectual property and knowledge (the licenses on Flask and its
dependencies). 5.5.2 develop programs that use reuse libraries.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described. Every record is invented.

---

## Why this exists

Unit 4 is where your objects go on a web page. You will not write the web server yourself. You will
install Flask, a framework other people wrote, and it will do the hard parts.

That is a good trade, and it comes with two facts you need to know on day one.

1. **You asked for one package, and seven arrived.** Flask needs other packages to work, and they
   need to be on your machine too. Each one is code you did not write and did not choose.
2. **Every one of them came with terms.** A license says what you may do with the code. Using code
   without knowing its terms is how a project, or a company, ends up in trouble later.

There is a third fact, and it causes today's error. **Python finds a library by its name.** You
share that name space with every package you install.

---

## The concept in plain language

A **dependency** is code your program needs that someone else wrote. A **framework** is a special
kind of dependency: it runs the main loop and calls the functions you write. With Flask, you do not
decide when your function runs. A browser asks for a page, and Flask calls your function.

When you install Flask, the installer also installs Flask's own dependencies. These are called
**transitive dependencies**: dependencies of your dependency.

Every package carries a **license**. The packages under Flask use **permissive** licenses, the BSD
family and MIT. At the purpose level, a permissive license says: you may use, change, and share this
code, including inside a company's own tools, as long as you keep the copyright notice and the
license text with it. This is a description of what these licenses are for, not legal advice. For a
class project, the school's policy comes first.

Package metadata usually names the license. Sometimes it names only the family. **"BSD License" with
no number means the metadata does not say which BSD variant.** The package's own LICENSE file does.
The variants differ in how many numbered conditions they carry, so you open the file and read it.

---

## Worked example 1: what came with Flask, and under what terms

```python
# licenses.py
# Flask is code you did not write. What came with it, and under what terms?
from importlib.metadata import metadata, requires, version


def license_of(package):
    """Newer packages state a license expression. Older ones use a classifier."""
    info = metadata(package)
    if info.get("License-Expression"):
        return info["License-Expression"]
    for line in info.get_all("Classifier") or []:
        if line.startswith("License ::"):
            return line.split(" :: ")[-1]
    return "not stated: read the LICENSE file"


print(f"flask {version('flask')}  {license_of('flask')}")
for requirement in requires("flask"):
    if ";" in requirement:          # skip extras and old-Python-only packages
        continue
    name = requirement.split(">")[0].split("=")[0].strip()
    print(f"  needs {name} {version(name)}  {license_of(name)}")
```

Output on the build machine:

```
flask 3.1.3  BSD-3-Clause
  needs blinker 1.9.0  MIT License
  needs click 8.4.2  BSD-3-Clause
  needs itsdangerous 2.2.0  BSD License
  needs jinja2 3.1.6  BSD License
  needs markupsafe 3.0.3  BSD-3-Clause
  needs werkzeug 3.1.8  BSD-3-Clause
```

Your version numbers may differ. The licenses are what matter. Seven packages, one request. Two of
them, `itsdangerous` and `jinja2`, say only "BSD License." That is not enough to fill in a license
table, so the next example goes to the source.

---

## Worked example 2: read the LICENSE file when the metadata is vague

```python
# find_license.py
# "BSD License" with no number? Open the package's own LICENSE file and count
# its numbered conditions.
from importlib.metadata import files

for package in ["jinja2", "itsdangerous"]:
    for f in files(package):
        if "LICENSE" in f.name.upper():
            text = f.read_text(encoding="utf-8")
            conditions = [line for line in text.splitlines()
                          if line.strip()[:2] in ("1.", "2.", "3.", "4.")]
            print(f"{package}: {f}  numbered conditions: {len(conditions)}")
```

Output:

```
jinja2: jinja2-3.1.6.dist-info/licenses/LICENSE.txt  numbered conditions: 3
itsdangerous: itsdangerous-2.2.0.dist-info/LICENSE.txt  numbered conditions: 3
```

The program finds the file and counts. **You still open the file and read it.** A count is a clue,
not a conclusion. The file names the variant in its wording, and the wording is what your
`LICENSES.md` row should rest on.

---

## Worked example 3: the framework calls your function

```python
# hello_line3.py
# The smallest Flask app. Flask calls home() when a browser asks for "/".
from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "Line 3 Maintenance Log is running."


if __name__ == "__main__":
    # State the port every time. Debug stays off: its error page runs code.
    app.run(host="127.0.0.1", port=8680, debug=False)
```

Run `python hello_line3.py`, open `http://127.0.0.1:8680/`, then `http://127.0.0.1:8680/issues`.
The server printed:

```
 * Serving Flask app 'hello_line3'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8680
Press CTRL+C to quit
127.0.0.1 - - [date and time] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [date and time] "GET /issues HTTP/1.1" 404 -
```

The server prints the real date and time where this copy shows `[date and time]`. The page at `/`
showed `Line 3 Maintenance Log is running.` The page at `/issues` answered 404, because no rule
exists for it yet. Tomorrow's lesson is the rule.

**Why `debug=False`.** Flask's debug mode shows an error page with a console that runs Python. Anyone
who can reach that page can run code on your machine. Every lab in this course keeps debug off.

### Who decides when `home()` runs

```python
# who_calls_whom.py
# You write the function. Flask decides when to call it.
from flask import Flask

app = Flask(__name__)
calls = []


@app.get("/")
def home():
    calls.append("home")
    return "Line 3 Maintenance Log is running."


print("after the file loads, home() has run", len(calls), "times")

client = app.test_client()          # pretends to be a browser
for path in ["/", "/", "/issues"]:
    response = client.get(path)
    print(path, response.status_code)

print("after three requests, home() has run", len(calls), "times")
```

Output:

```
after the file loads, home() has run 0 times
/ 200
/ 200
/issues 404
after three requests, home() has run 2 times
```

Your file never calls `home()`. Flask called it twice, once for each request to `/`. The request to
`/issues` matched nothing, so none of your code ran for it. That is what "a framework calls you"
means.

---

## Worked example 4: which `flask` did Python load

```python
# which_flask.py
# Python finds a library by its name. Which file did "import flask" load?
import pathlib

import flask

where = pathlib.Path(flask.__file__)
print("loaded:", where.name)
print("from folder:", where.parent.name)
print("inside:", where.parent.parent.name)
print("has Flask:", hasattr(flask, "Flask"))
```

Output:

```
loaded: __init__.py
from folder: flask
inside: site-packages
has Flask: True
```

`site-packages` is where installed packages live. Keep this example in mind for the next section.

---

## The wrong version, and the error it produces

Save `hello_line3.py` under the name `flask.py`, in an empty folder, and run it. Output, with the
folder path shortened to `...`:

```
Traceback (most recent call last):
  File "...\shadow\flask.py", line 3, in <module>
    from flask import Flask
  File "...\shadow\flask.py", line 3, in <module>
    from flask import Flask
ImportError: cannot import name 'Flask' from 'flask' (consider renaming '...\\shadow\\flask.py' if it has the same name as a library you intended to import)
```

Read it slowly. Python looks in your script's own folder **before** `site-packages`. It found your
file named `flask.py` and imported that. Your file **is** the `flask` module now, and it contains no
`Flask`. The traceback shows the same line twice because your file imported itself.

Python 3.13 added the hint in parentheses, and it tells you the fix: rename your file. The lab
machines run a newer Python, so the wording may differ slightly. The cause is the same.

The fix: rename the file to something that is not a library's name, such as `hello_line3.py`. If a
`__pycache__` folder was created next to it, delete that folder too.

---

## Why the wrong version is tempting

You are learning Flask, so `flask.py` feels like the natural name for your practice file. The same
trap waits for `random.py`, `json.py`, `email.py`, and `test.py`. The name describes what the file is
about, and that is exactly why it collides.

The habit that prevents it: name files after what **your** program does. `hello_line3.py`,
`licenses.py`, `store.py`. When an import fails in a way that makes no sense, check first whether one
of your files has the library's name.

A second temptation, for the license half: "It's open source, so I can do anything with it."
Permissive licenses allow a lot, and they still ask for something. Keeping the notice and the
license text is a condition, not a courtesy.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Dependency** | code your program needs that someone else wrote |
| **Transitive dependency** | a dependency of one of your dependencies, installed along with it |
| **Framework** | a dependency that runs the main loop and calls the functions you write |
| **License** | the terms that say what you may do with a piece of code |
| **Permissive license** | a license, such as BSD or MIT, that allows use, change, and sharing if you keep the notice and license text |
| **Metadata** | the facts a package publishes about itself: name, version, license, dependencies |
| **Shadowing** | your own file having the same name as a library, so Python imports yours instead |
| **Development server** | the server `app.run()` starts, for your own machine only, never for production |

---

## Self-check

**Question 1.** You install one package, and `licenses.py` prints seven lines. Explain where the other
six came from.

**Question 2.** A row in your license table says `jinja2 3.1.6  BSD License`. Why is that row not
finished, and what do you do to finish it?

**Question 3.** A classmate's program fails with `ImportError: cannot import name 'Flask' from
'flask'`, and Flask is installed. What is the most likely cause, and what do they check first?

---

### Answers

**1.** They are Flask's own dependencies, installed because Flask needs them to run. They are called
transitive dependencies. You did not ask for them by name, and they are still part of your project,
with their own licenses.

**2.** "BSD License" names the family, not the variant, so the metadata does not say which terms
apply. You open the package's own LICENSE file, read its conditions, and record the variant you
found there.

**3.** A file in their project folder is named `flask.py`, so Python imported that file instead of
the installed library. They look for a file with a library's name in the folder they ran from, rename
it, and delete any `__pycache__` folder next to it.
