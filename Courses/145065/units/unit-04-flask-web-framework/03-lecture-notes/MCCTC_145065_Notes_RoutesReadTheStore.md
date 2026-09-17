# Lecture Notes: Routes Read the Store
## 145065 Object-Oriented Programming · Unit 4 · Week 7, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W07_RoutesReadTheStore.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W07_RoutesReadTheStore.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python, Flask, and the
lab files `store.py`, `models.py`, and `data/line3_log.json` from Lab U04-01.

**Competencies:** 5.3.11 write code to access data repositories (a JSON store read from routes).
5.5.1 develop programs using data validation techniques (every field checked on load). 5.3.10 code
error handling techniques (one handler turns a broken store into a safe page).

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described. Every record is invented.

---

## Why this exists

Until today, the pages read a dictionary typed into the program. Real pages read data that lives
outside the program, in a file or a database. Anything outside your program can change without
asking you.

A person edits the file by hand and leaves a stray comma. A save gets cut off halfway. An old copy
comes back from a backup in an old format. If a route trusts the file, one of two things happens.
The user sees a traceback, which also shows them how your program works. Or, worse, the page shows
wrong data and nothing looks broken.

In Unit 3 you built a store that checks every field when it loads. Today that store moves behind
your routes. **A route asks the store for clean objects, and never trusts the file.**

---

## The concept in plain language

Four pieces work together.

1. **The store class** (`IssueStore` in `store.py`) reads the file, checks the version, checks every
   field's type, and checks that every reference points at something that exists. It hands out
   objects, never raw dictionaries. If anything is wrong, it raises its own exception, a kind of
   `StoreError`. It never uses `pickle`, because loading a pickle file can run code hidden inside it.
2. **`get_store()`** creates the store for the current request and keeps it in `g`. `g` is Flask's
   per-request scratch space. It starts empty on every request, so every request reads the file
   fresh. A fix to the file shows on the next page load.
3. **The route** calls `get_store()` and asks for what it needs. It only ever sees clean objects.
4. **One error handler**, `@app.errorhandler(StoreError)`, catches every store problem from every
   route. It writes the details to the server's log and sends the user a short page with status
   **503 Service Unavailable**: something the user can act on, and nothing about how the program
   works.

---

## Worked example 1: a route reads the store

Put this file next to the lab's `store.py`, `models.py`, and `data/line3_log.json`.

```python
# store_demo.py
# A route reads the Unit 3-style JSON store through IssueStore, and a broken
# file becomes a 503 page, never a traceback in front of the user.
import sys

from flask import Flask, abort, g

from store import IssueStore, StoreError

app = Flask(__name__)
app.config["STORE_PATH"] = "data/line3_log.json"


def get_store():
    """Read the store once per request, so a change to the file shows next time."""
    if "store" not in g:
        g.store = IssueStore(app.config["STORE_PATH"])
    return g.store


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    issue = get_store().get_issue(issue_id)
    if issue is None:
        abort(404)
    return f"Issue {issue.id} on {issue.equipment}: {issue.severity}, {issue.status_label}"


@app.errorhandler(StoreError)
def store_unavailable(error):
    print(f"[store] {type(error).__name__}: {error}", file=sys.stderr)
    return "The maintenance log is unavailable. Tell your supervisor.", 503
```

Two requests through the test client:

```
200 Issue 3 on CV-01: critical, Open
404
```

The first line is `GET /issues/3`. The second is `GET /issues/99`, which does not exist. Every value
in the returned text is one the store already checked against a fixed list, so the f-string is safe
here. A title a person typed would go through a template instead.

`Open` is `status_label`, a property of the `Issue` object. The file stores `open`. The object knows
how to show it. That is the Unit 1 idea of an object carrying the behavior that belongs to its data.

---

## Worked example 2: one handler for every kind of broken file

The store's exceptions form a small hierarchy from Unit 3: `StoreMissingError` and
`StoreFormatError` are both kinds of `StoreError`. So one `except`, or one handler, catches all of
them.

**A warning before you run it.** The output below came from the finished store. The lab's starter
`store.py` leaves the negative-downtime check for you to write in Part 4, step 15. Until you write it,
the third line of your output reads `data/negative.json: loaded, 5 open issues`. A store that loads a
negative downtime is a store that trusts the file. That is the point of step 15.

This example runs in the same folder, with two extra files: `data/negative.json` is a copy of
the store with issue 3's downtime changed from `90` to `-90`, and `data/gone.json` does not exist.

```python
# one_handler.py
# One except clause, many kinds of broken file, because every store
# exception is a kind of StoreError (the Unit 3 hierarchy).
from store import IssueStore, StoreError

for path in ["data/line3_log.json", "data/gone.json", "data/negative.json"]:
    try:
        store = IssueStore(path)
        print(f"{path}: loaded, {len(store.open_issues())} open issues")
    except StoreError as error:
        print(f"{path}: {type(error).__name__}: {error}")
```

Output on Windows:

```
data/line3_log.json: loaded, 5 open issues
data/gone.json: StoreMissingError: No store at data\gone.json
data/negative.json: StoreFormatError: issues[2]: downtime_minutes cannot be negative
```

On a Mac or Linux machine the second path prints with `/`. Look at the third line. The JSON is
perfectly valid. The value is not. `issues[2]` is the third issue in the file, counting from zero.
The store checked meaning, not only shape, and it named exactly where the problem is.

---

## Worked example 3: read fresh on every request

`g` starts empty on every request. This example proves it with a cafeteria menu file that changes
between two page loads.

```python
# menu_store.py
# The lunch menu lives in a file the cafeteria edits. The route reads it
# fresh on every request, through a class that checks it first.
import json
import pathlib
import sys

from flask import Flask, g, render_template_string

MENU_FILE = pathlib.Path("menu.json")


class MenuError(Exception):
    """Anything wrong with the menu file."""


class MenuStore:
    def __init__(self, path):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as error:
            raise MenuError(f"cannot read {path.name}: {error}") from None
        items = raw.get("items") if isinstance(raw, dict) else None
        if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
            raise MenuError("'items' must be a list of text")
        self.items = items


app = Flask(__name__)


def get_menu():
    if "menu" not in g:                 # g starts empty on every request
        print("  (reading menu.json)")
        g.menu = MenuStore(MENU_FILE)
    return g.menu


@app.get("/menu")
def menu():
    return render_template_string("{{ items | join(', ') }}", items=get_menu().items)


@app.errorhandler(MenuError)
def menu_unavailable(error):
    print(f"  [menu] {error}", file=sys.stdout)
    return "The menu is not available right now.", 503


client = app.test_client()
MENU_FILE.write_text('{"items": ["pizza", "salad"]}', encoding="utf-8")
print(client.get("/menu").get_data(as_text=True))

MENU_FILE.write_text('{"items": ["pizza", "salad", "tacos"]}', encoding="utf-8")
print(client.get("/menu").get_data(as_text=True))

MENU_FILE.write_text('{"items": "tacos"}', encoding="utf-8")
response = client.get("/menu")
print(response.status_code, response.get_data(as_text=True))
MENU_FILE.unlink()
```

Output:

```
  (reading menu.json)
pizza, salad
  (reading menu.json)
pizza, salad, tacos
  (reading menu.json)
  [menu] 'items' must be a list of text
503 The menu is not available right now.
```

Three requests, three reads. The second page showed tacos without a restart. The third file was valid
JSON with the wrong shape, and the class refused it. The user got a sentence, and the detail went to
the log.

**The tradeoff.** Reading on every request is right for a small shop log that people edit and that
must always be current. It would be wrong for a large file on a busy site, where reading it thousands
of times a minute wastes time. Week 9 replaces the file with a database, which is built for that.

---

## The wrong version, and the output it produces

Make a copy of the store file. In the copy, add a second comma after `"downtime_minutes": 90,`, which
is line 52 of the lab's file. Point `STORE_PATH` at the copy and request `/issues/3`.

**With the handler**, the server log shows:

```
[store] StoreFormatError: Not valid JSON: Expecting property name enclosed in double quotes: line 52 column 30 (char 2221)
```

and the user sees:

```
503 The maintenance log is unavailable. Tell your supervisor.
```

**Now the wrong version.** Comment out the whole `@app.errorhandler(StoreError)` function and request
the page again. The status is **500**, and the server prints a traceback that starts:

```
[date and time] ERROR in app: Exception on /issues/3 [GET]
Traceback (most recent call last):
```

and ends:

```
store.StoreFormatError: Not valid JSON: Expecting property name enclosed in double quotes: line 52 column 30 (char 2221)
```

The user sees Flask's generic `Internal Server Error` page. Both versions refused the broken file.
Only one told the user what to do, and only one kept the file's details in the log where they
belong. With debug mode on, the user could have seen the whole traceback, which is one more reason
debug stays off.

Restore the clean file when you finish. Keep a clean copy before you break anything on purpose.

---

## Why the wrong version is tempting

"I wrote the JSON myself, so it is fine." You did write it. You are not the only thing that touches
it. A classmate edits it by hand. A save is cut off. An old backup is restored. The Unit 3 question
still applies: **what else can touch that file?**

The second temptation is to catch the error inside every route. That means the same `try` in fifteen
places, and one forgotten route shows a traceback. One handler, registered once, covers every route,
including the ones you have not written yet.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Data store** | where the app's data lives outside the program; here, a JSON file |
| **Validation on load** | checking every field, type, and reference before any route sees the data |
| **`g`** | Flask's scratch space for one request; empty at the start of each request |
| **Error handler** | a function registered with `@app.errorhandler(...)` that answers when that exception is raised |
| **Exception hierarchy** | related exception classes that share a base, so one handler catches them all |
| **503 Service Unavailable** | the server is working, but something it needs is not |
| **500 Internal Server Error** | the server hit an error nobody handled |
| **Server log** | the output the server writes for the people who run it, not for users |

---

## Self-check

**Question 1.** The lab app answers every page with 503 after a classmate edited the store file. Where
do you look to find out what is wrong, and why is the answer not on the page?

**Question 2.** The handler is registered for `StoreError`. Why does it also catch a
`StoreMissingError` when the file is deleted?

**Question 3.** A store file is valid JSON, but one issue names equipment `ZZ-99`, which is not in
the equipment list. What should happen when a route asks for that issue, and which piece of code
makes it happen?

---

### Answers

**1.** In the server's log, the terminal running the app. The handler prints a `[store]` line with
the exception type and the exact problem there. The page shows only a short message, because details
about the file and the program are for the people who run it, not for users.

**2.** `StoreMissingError` is a subclass of `StoreError`. A handler registered for a class also
handles every subclass of it, the same way `except StoreError` catches both kinds in worked example 2.
That is why one handler covers every kind of broken store.

**3.** The store refuses the whole file when it loads, with a `StoreFormatError` that names the issue
and the unknown equipment. The reference check in `IssueStore.load()` raises it, and the
`StoreError` handler turns it into the 503 page. The route never receives an issue that points at
nothing.
