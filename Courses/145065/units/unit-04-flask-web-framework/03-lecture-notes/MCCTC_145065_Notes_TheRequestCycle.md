# Lecture Notes: The Request Cycle
## 145065 Object-Oriented Programming · Unit 4 · Week 7, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W07_TheRequestCycle.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W07_TheRequestCycle.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and Flask.

**Competencies:** 5.5.7 read inputs (the URL and the query string). 5.3.5 write code that uses
conditional control structures (the checks inside a view).

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described. Every record is invented.

---

## Why this exists

Every bug you meet in Weeks 7 through 10 lives at one step of a request's trip through your app. If
you can name the step, you know which file to open. If you cannot, a 404 looks like one mystery when
it is really two different problems.

Today's question: **when a browser asks for an address, which of your functions answers, and did it
run at all?**

---

## The concept in plain language

A **route** is a rule with three parts:

1. a URL pattern, such as `/issues/<int:issue_id>`
2. the methods it accepts, such as GET
3. the one function Flask calls when a request matches

The decorator `@app.get(...)` runs **once**, when your file loads. It does not call your function. It
adds an entry to a lookup table. The URL pattern is the key. Your function is the value. That
function is called a **view function**.

When a request arrives, Flask compares its path with every rule in the table.

- If a rule matches, Flask **converts** the variable parts. `<int:issue_id>` turns the text `"3"` into
  the number `3`. Then Flask calls the view with that value.
- If no rule matches, Flask answers 404 itself. **Your code never runs.**

A view can still answer 404 on purpose, with `abort(404)`. That means the rule matched, your code
ran, and the record was not there. Same status, different cause. The **endpoint** tells them apart:
it is the name of the view that ran, or `None` when nothing matched.

A view also reads the **query string**, the part after `?`, from `request.args`. A value you do not
recognize is a bad request, so the view answers 400.

---

## Worked example 1: six requests, six trace lines

```python
# routes_demo.py
# A route is a rule: a URL pattern, the methods it accepts, and the function
# Flask calls when a request matches. Riverside Fabrication is a composite.
from flask import Flask, abort, request

app = Flask(__name__)

ISSUES = {
    1: "Back gauge drifts 2 mm after warm-up",
    3: "Guard interlock trips with the guard closed",
}
STATUSES = ("open", "in_progress", "closed")


@app.get("/issues/<int:issue_id>")        # <int:...> turns "3" into 3
def issue_detail(issue_id):
    title = ISSUES.get(issue_id)
    if title is None:
        abort(404)                         # the rule matched; the record did not
    return f"Issue {issue_id}: {title}"


@app.get("/issues")
def list_issues():
    status = request.args.get("status")    # ?status=open, or None
    if status is not None and status not in STATUSES:
        abort(400)                         # a value you do not know is a bad request
    return f"Listing issues, status: {status or 'any'}"


@app.after_request
def trace(response):
    print(f"[trace] {request.method} {request.full_path.rstrip('?')} "
          f"-> {request.endpoint} -> {response.status_code}")
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8681, debug=False)
```

The titles come from a fixed dictionary inside the program, so returning them in an f-string is safe
here. Tomorrow, pages move into templates, which are safer for anything a person typed.

Six requests sent through Flask's test client (`app.test_client().get(path)`) printed:

```
[trace] GET /issues/3 -> issue_detail -> 200
[trace] GET /issues/2 -> issue_detail -> 404
[trace] GET /issues/three -> None -> 404
[trace] GET /issues -> list_issues -> 200
[trace] GET /issues?status=open -> list_issues -> 200
[trace] GET /issues?status=everything -> list_issues -> 400
```

Read lines two and three slowly.

- `/issues/2` reached `issue_detail`. The function looked for issue 2, found nothing, and called
  `abort(404)`. **Your code answered.**
- `/issues/three` reached **no function**. The endpoint is `None`. The `int` converter refused
  `three`, so no rule matched. **Your code never ran.**

The last line is the query string at work. `everything` is not a status, so `list_issues` refused it.

---

## Worked example 2: the lookup table is real

```python
# rule_table.py
# The decorators run once, when the file loads, and fill a lookup table.
from flask import Flask

app = Flask(__name__)
print("registering rules...")


@app.get("/tools/<tag>")
def tool_detail(tag):
    return "One tool"                 # never paste the URL text into HTML


@app.get("/checkouts/<int:checkout_id>")
def checkout_detail(checkout_id):
    return f"Checkout {checkout_id}"  # a number, so this is safe


print("done. The table now holds:")
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
    print(f"  {methods:4} {rule.rule:32} -> {rule.endpoint}")
```

Output:

```
registering rules...
done. The table now holds:
  GET  /checkouts/<int:checkout_id>     -> checkout_detail
  GET  /static/<path:filename>          -> static
  GET  /tools/<tag>                     -> tool_detail
```

No request was sent, and the table is already full. The `static` rule is one Flask adds for you, to
serve files such as a stylesheet. `app.url_map` is the table Flask searches for every request.

This is the fix for the most common wrong idea about Flask: **"my program runs from top to bottom."**
It does, once, to fill the table. After that, Flask calls your functions in whatever order requests
arrive.

---

## Worked example 3: which function would answer

You can ask the table a question without running any view.

```python
# match_only.py
# Ask the lookup table which function a URL would reach, without running it.
from flask import Flask
from werkzeug.exceptions import NotFound

app = Flask(__name__)


@app.get("/playlists/<int:playlist_id>")
def playlist(playlist_id):
    return f"Playlist {playlist_id}"


@app.get("/playlists")
def all_playlists():
    return "All playlists"


adapter = app.url_map.bind("127.0.0.1")
for path in ["/playlists/12", "/playlists/road-trip", "/playlists", "/songs"]:
    try:
        endpoint, values = adapter.match(path, method="GET")
        print(f"{path:22} -> {endpoint}, {values}")
    except NotFound:
        print(f"{path:22} -> no rule matched: 404 before your code runs")
```

Output:

```
/playlists/12          -> playlist, {'playlist_id': 12}
/playlists/road-trip   -> no rule matched: 404 before your code runs
/playlists             -> all_playlists, {}
/songs                 -> no rule matched: 404 before your code runs
```

Look at `{'playlist_id': 12}`. The 12 has no quotes. It is already a number when your function
receives it. That is the converter's job. `road-trip` is not a whole number, so the rule does not
match at all.

---

## The wrong version, and the output it produces

Remove the converter. Change `@app.get("/issues/<int:issue_id>")` in `routes_demo.py` to
`@app.get("/issues/<issue_id>")` and send the same six requests:

```
[trace] GET /issues/3 -> issue_detail -> 404
[trace] GET /issues/2 -> issue_detail -> 404
[trace] GET /issues/three -> issue_detail -> 404
[trace] GET /issues -> list_issues -> 200
[trace] GET /issues?status=open -> list_issues -> 200
[trace] GET /issues?status=everything -> list_issues -> 400
```

**Issue 3 exists, and it answers 404.** No crash. No traceback. Without a converter, `issue_id`
arrives as the text `"3"`. The dictionary's key is the number `3`. Text and numbers are never equal in
Python, so `ISSUES.get("3")` finds nothing and the view calls `abort(404)`.

Compare the third line with worked example 1. Before, `/issues/three` reached `None`. Now it reaches
`issue_detail`, because a rule with no converter accepts any text. The trace line is the evidence.

The fix: put `int:` back. The converter is not decoration. It is the line that turns URL text into
the type your data uses.

---

## Why the wrong version is tempting

`<issue_id>` looks complete. The page loads. The route matches. Every piece you can see is working,
and nothing prints an error. The mismatch is between the **type** of the value and the type of the
key, and types are invisible in a URL, because every URL is text.

The habit that prevents it: when a route answers 404 for a record you know exists, read the trace
line. If the endpoint is your view, print the type of the value your view received.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Route** | a rule: a URL pattern, the methods it accepts, and one view function |
| **View function** | the function Flask calls when a request matches a route |
| **Decorator** | the `@app.get(...)` line above a function; here it registers the route once, when the file loads |
| **Converter** | the part of a pattern such as `int:` that checks and converts a URL piece |
| **Endpoint** | the name Flask uses for a view; `None` in the trace means no rule matched |
| **Query string** | the part of a URL after `?`, read with `request.args` |
| **404 Not Found** | no such page, either because no rule matched or because the view said so |
| **400 Bad Request** | the request asked for something the view does not accept |

---

## Self-check

**Question 1.** A trace line reads `[trace] GET /tools/HX-07 -> tool_detail -> 404`. Did any of your
code run? Where do you look first?

**Question 2.** Using `routes_demo.py`, what status does `GET /issues?status=closed` get, and which
line decides it?

**Question 3.** A student's rule is `@app.get("/checkouts/<checkout_id>")` and the data uses whole
numbers as keys. Every checkout page answers 404. Explain why, and give the one-word fix.

---

### Answers

**1.** Yes. The endpoint is `tool_detail`, so the rule matched and that view ran. The view decided the
tool does not exist and called `abort(404)`. Look inside `tool_detail`: how it looks the tag up, and
whether `HX-07` is really in the data with exactly that spelling.

**2.** 200. `closed` is in `STATUSES`, so the `if status is not None and status not in STATUSES`
test is false, `abort(400)` is skipped, and the view returns `Listing issues, status: closed`.

**3.** Without a converter, `checkout_id` arrives as text such as `"4"`, and a text key never equals
the number `4`, so the lookup finds nothing and the view answers 404. The fix is the converter:
`<int:checkout_id>`.
