# Lecture Notes: Post/Redirect/Get
## 145065 Object-Oriented Programming · Unit 4 · Week 8, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W08_PostRedirectGet.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W08_PostRedirectGet.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and Flask.

**Competencies:** 5.5.7 read inputs (a submitted form). 5.6.6 design system inputs, outputs, and
processes (what a form sends, what the server does, what the person sees next).

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described. Every record is invented.

---

## Why this exists

Last week your pages only showed data. This week they accept it. A technician on Line 3 should be
able to log a problem from the browser instead of editing a file.

Two things go wrong the first time anyone builds a form.

1. **The refresh problem.** You submit a form, the page appears, and you press refresh. The browser
   asks whether to send the form again. Say yes, and the server saves a second copy. On a maintenance
   log, that is a duplicate issue. On a store, it is a second order.
2. **The missing field problem.** A checkbox that is not ticked sends nothing at all. Not `"no"`. Not
   `False`. Nothing. Code that expects the field crashes.

Today's pattern fixes the first, and one method call fixes the second.

**Today has no validation on purpose.** Tomorrow adds the rules. Keep that in mind while you read.

---

## The concept in plain language

One URL can answer two methods.

- **GET** shows the form. It changes nothing.
- **POST** receives what the person filled in. Flask puts the fields in `request.form`, a
  dictionary-like object keyed by each input's `name`.

After a successful POST, the server does **not** send a page back. It sends a **redirect**: status
**303 See Other**, with a `Location` header that says "now GET this address." The browser follows it
and shows the new record's page with a plain GET.

That is **Post/Redirect/Get**, often shortened to PRG. After it, the last request in the browser's
history is a GET. A refresh repeats the GET. Nothing is saved twice.

For fields that may be missing, use `request.form.get("name")`. It returns `None` when the field was
not sent. `request.form["name"]` fails instead.

---

## Worked example 1: the form and the route

`templates/new_issue.html`, reduced to the parts that matter today:

```html
<form action="{{ url_for('create_issue') }}" method="post">
  <label for="title">Short title</label>
  <input id="title" name="title" type="text" required>
  <input id="locked-out" name="locked_out" type="checkbox" value="yes">
  <label for="locked-out">The machine is locked out</label>
  <button type="submit">Log the issue</button>
</form>
```

The `name` on each input becomes the key in `request.form`. The checkbox's `value` is what it sends
when ticked.

```python
# form_demo.py
# One URL, two methods. GET shows the form. POST reads what came back,
# saves it, and redirects, so a refresh cannot send it twice.
from flask import Flask, abort, redirect, render_template, render_template_string, request, url_for

app = Flask(__name__)
ISSUES = []


@app.get("/issues/new")
def new_issue_form():
    return render_template("new_issue.html")


@app.post("/issues/new")
def create_issue():
    title = request.form.get("title", "").strip()
    # An unticked checkbox sends nothing at all, so .get() with a test.
    locked_out = request.form.get("locked_out") == "yes"
    ISSUES.append({"id": len(ISSUES) + 1, "title": title, "locked_out": locked_out})
    # 303 See Other: "go GET this page now." Post/Redirect/Get.
    return redirect(url_for("issue_detail", issue_id=len(ISSUES)), code=303)


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    if not 1 <= issue_id <= len(ISSUES):
        abort(404)
    # The title is typed text, so it goes through a template, which escapes it.
    return render_template_string(
        "Issue {{ i.id }}: {{ i.title }} (locked out: {{ i.locked_out }})", i=ISSUES[issue_id - 1])
```

Three requests through the test client. `GET /issues/new` answered `200`. A POST with only a title
answered:

```
303 /issues/1
```

That is the status and the `Location` header. The server saved issue 1 and told the browser where to
go. A second POST, titled `Guard <b>interlock</b> trips` with the box ticked, followed to its page:

```
200 Issue 2: Guard &lt;b&gt;interlock&lt;/b&gt; trips (locked out: True)
```

Two things to notice. The ticked box became `True`. The angle brackets in the title were shown as
text, because the page went through a template. That is Wednesday's concept arriving early, and it is
why the view never puts a typed title into an f-string.

In a browser, you can watch the 303 in the developer tools' network panel. The panel's name differs
between browsers.

---

## Worked example 2: what an unticked box sends

```python
# what_came_back.py
# What does the server receive from a form with a checkbox?
from flask import Flask, request

app = Flask(__name__)


@app.post("/order")
def order():
    print("request.form holds:", request.form.to_dict())
    extra_cheese = request.form.get("extra_cheese") == "yes"
    print("extra cheese:", extra_cheese)
    return "ok"


client = app.test_client()
client.post("/order", data={"size": "large", "extra_cheese": "yes"})   # box ticked
client.post("/order", data={"size": "large"})                          # box unticked
```

Output:

```
request.form holds: {'size': 'large', 'extra_cheese': 'yes'}
extra cheese: True
request.form holds: {'size': 'large'}
extra cheese: False
```

The second order has no `extra_cheese` key at all. `request.form.get("extra_cheese")` returned
`None`, `None == "yes"` is `False`, and the order goes through without cheese. That comparison is the
whole fix.

---

## Worked example 3: refresh after a redirect

```python
# refresh_safe.py
# Post/Redirect/Get: after the redirect, a refresh repeats the GET, not the POST.
from flask import Flask, abort, redirect, render_template_string, request, url_for

app = Flask(__name__)
ORDERS = []


@app.post("/orders")
def place_order():
    ORDERS.append(request.form.get("size", "medium"))
    return redirect(url_for("order_page", order_id=len(ORDERS)), code=303)


@app.get("/orders/<int:order_id>")
def order_page(order_id):
    if not 1 <= order_id <= len(ORDERS):
        abort(404)
    return render_template_string("Order {{ n }}: one {{ size }} pizza",
                                  n=order_id, size=ORDERS[order_id - 1])


client = app.test_client()
response = client.post("/orders", data={"size": "large"})
print(response.status_code, response.headers["Location"])

for refresh in range(3):                       # the person presses refresh three times
    page = client.get(response.headers["Location"])
    print(page.status_code, page.get_data(as_text=True))

print(len(ORDERS), "order saved")
```

Output:

```
303 /orders/1
200 Order 1: one large pizza
200 Order 1: one large pizza
200 Order 1: one large pizza
1 order saved
```

Three refreshes, one order. The refreshes repeated the GET, and a GET changes nothing.

### Without the redirect

A version of `form_demo.py` that answered the POST with a page instead of a redirect was sent the
same POST three times. That is what a browser does when the person refreshes and confirms the
resend. Output:

```
200 Saved issue 1
200 Saved issue 2
200 Saved issue 3
3 issues saved
```

Three identical issues. Nothing crashed, and the log is now wrong.

---

## The wrong version, and the error it produces

In `form_demo.py`, change

```python
    locked_out = request.form.get("locked_out") == "yes"
```

to

```python
    locked_out = request.form["locked_out"] == "yes"
```

Submit the form with the box **unticked**. The browser shows:

```
Bad Request
The browser (or proxy) sent a request that this server could not understand.
```

With `debug=False`, the server's terminal shows only the request line:

```
127.0.0.1 - - [date and time] "POST /issues/new HTTP/1.1" 400 -
```

The server prints the real date and time where this copy shows `[date and time]`. **Nothing names the
field.** Flask turns the missing key into a 400 on purpose, so a stranger's bad request
cannot crash your app. The cost is that you get no clue.

To find the field while you develop, add this line after `app = Flask(__name__)`:

```python
app.config["TRAP_BAD_REQUEST_ERRORS"] = True
```

Submit again. The traceback in the terminal ends:

```
werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.
KeyError: 'locked_out'
```

Now the field is named. While the setting is on, the browser gets `Internal Server Error` with status
500 instead of the 400 page, and the request line says 500. The fix is the `.get()` with a comparison
from worked example 1. Remove the `TRAP_BAD_REQUEST_ERRORS` line when you are done.

---

## Why the wrong version is tempting

You tested the form with the box ticked, and it worked. `request.form["locked_out"]` looks like
every dictionary you have used since 145060. The form on the screen shows the checkbox, so it feels
like the checkbox must send something. It does not. **What the browser sends is not what the page
shows.**

The redirect is tempting to skip for a different reason. Returning a page after a POST looks
finished, and the duplicate only appears when someone refreshes, which you never do while testing.

The habits: read fields with `.get()` unless the field is truly required and checked, and end every
successful POST with a 303 redirect.

---

## Vocabulary

| Term | What it means |
|---|---|
| **GET** | the method for asking to see something; it changes nothing |
| **POST** | the method for sending data the server should act on |
| **`request.form`** | the fields a submitted form sent, keyed by each input's `name` |
| **Redirect** | a response that tells the browser to request a different address |
| **303 See Other** | the redirect status that means "now GET this address" |
| **`Location` header** | the part of a redirect that names the address to go to |
| **Post/Redirect/Get (PRG)** | save on POST, answer with a 303, show the result on a GET |
| **400 Bad Request** | the request is missing something the server needs |

---

## Self-check

**Question 1.** A safety form has only two inputs, both checkboxes with `value="yes"`: `wet_floor`
and `guard_off`. The person ticks only `guard_off` and submits. What does
`request.form.to_dict()` hold? Write the line that sets `wet_floor` to `True` or `False` without
failing.

**Question 2.** A student's POST route saves a checkout and returns `render_template("done.html")`.
Describe what happens when the technician refreshes the page and confirms, and how to fix it.

**Question 3.** Your app answers a form with `Bad Request` and the terminal shows only a 400 line.
What setting helps you find the cause, and when should you remove it?

---

### Answers

**1.** `{'guard_off': 'yes'}`. The unticked box sent nothing, so `wet_floor` is not in it at all. The
safe line is `wet_floor = request.form.get("wet_floor") == "yes"`, which gives `False` here. Square
brackets would fail with 400 Bad Request.

**2.** The browser sends the same POST again, so the route saves a second, identical checkout. The
fix is Post/Redirect/Get: after saving, return `redirect(url_for(...), code=303)` to the checkout's
page. A refresh then repeats that GET, which saves nothing.

**3.** `app.config["TRAP_BAD_REQUEST_ERRORS"] = True`. It makes the terminal show the full traceback
with the missing key, such as `KeyError: 'locked_out'`. Remove it once the bug is fixed. It is a
development aid, and while it is on, a bad request gets a 500 instead of a 400.
