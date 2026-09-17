# Lecture Notes: Input Is Data, Never Code
## 145065 Object-Oriented Programming · Unit 4 · Week 8, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W08_InputIsData.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W08_InputIsData.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and Flask.

**Competencies:** 9.3.1 identify application vulnerabilities (cross-site scripting, injection).
9.3.3 implement secure coding concepts (output escaping, input validation).

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described. Every record is invented.

**The rule for every attack in this unit.** You send attacks only to your own app, running on
`127.0.0.1`, and to nothing else. That is in the Lab Acceptable Use and Safety Agreement.

---

## Why this exists

Yesterday you made sure a title is the right length. Today's question is different: **what happens
when a perfectly allowed title contains something that looks like code?**

A title such as `<script>...</script>` is text. If your page pastes it into the HTML as it is, the
browser does not see text. It sees a script, and it runs it, for every person who opens that issue.
The person who typed it does not need access to anyone's computer. Your page delivers the script for
them.

That is **cross-site scripting**, usually shortened to XSS. It is the first vulnerability named in
competency 9.3.1, and it is the most common one in small web apps.

---

## The concept in plain language

**An injection is text that should have been a value, pasted into text that is code.**

Every language your app writes has this risk: HTML for pages, Jinja for templates, and SQL for
databases in Week 9. The shape of the mistake is the same each time. You build code by joining
strings, and a person's typed text becomes part of the code.

The defense is the same shape too: **pass the text as a value**, and let the tool that understands
the language keep it as a value.

For HTML, Jinja does this for you. **Every `{{ value }}` in a template is escaped by default.**
Escaping replaces the characters that mean something in HTML with codes that only display them:

| Character | Escaped as |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&#34;` |
| `'` | `&#39;` |

The browser shows `&lt;` as `<` on the screen, but never treats it as the start of a tag.

So your job is mostly to **not turn escaping off**. The two ways people turn it off:

1. adding `| safe` to a value in a template
2. building HTML, or template text, by joining strings in Python

### The three shapes of one mistake

| Code language | Pasted, dangerous | Passed as a value, safe |
|---|---|---|
| HTML | `f"<h1>{title}</h1>"` returned from a view, or `{{ title \| safe }}` | `{{ title }}` in a template |
| A Jinja template | `render_template_string(f"No results for {q}")` | `render_template_string("No results for {{ q }}", q=q)` |
| SQL (Week 9) | `f"... WHERE name = '{typed}'"` | `"... WHERE name = ?", (typed,)` |

The middle row has its own name: **server-side template injection**. When typed text becomes part of
the template itself, Jinja treats any template syntax inside it as instructions to run on the server,
which is worse than a script in one person's browser.

### Escaping and validation are different jobs

**Escaping protects display. Validation protects meaning.** You need both.

- Validation decides whether a value is allowed at all. A severity of `apocalyptic` is refused.
- Escaping decides how an allowed value is shown. A title about a `<b>` tag in a laser program is
  legitimate text. It is stored exactly as typed and shown escaped.

---

## Worked example 1: Jinja escapes a typed title

`templates/issue.html`:

```html
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Issue {{ issue.id }}</title></head>
<body>
<h1>Issue {{ issue.id }}: {{ issue.title }}</h1>
</body>
</html>
```

```python
# escape_demo.py
# A title is whatever a person typed. Jinja escapes it when it is shown.
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)
ISSUES = {9: {"id": 9, "title": "<script>document.title='owned'</script>"}}


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    return render_template("issue.html", issue=ISSUES[issue_id])


print(escape("Bracket <b> & \"quotes\" 'too'"))
```

The `print` runs when the file loads. Then `GET /issues/9` was requested, and a check looked for a
raw `<script>` tag in the page. Output, with the heading line of the page in the middle:

```
Bracket &lt;b&gt; &amp; &#34;quotes&#34; &#39;too&#39;
<h1>Issue 9: &lt;script&gt;document.title=&#39;owned&#39;&lt;/script&gt;</h1>
raw script tag in page: False
```

`escape()` from `markupsafe` is the same function Jinja uses. Every character from the table above
was replaced. In the page, the title is shown to the reader as it was typed, angle brackets and all,
and the browser runs nothing. The tab title stays `Issue 9`.

---

## Worked example 2: pasted into HTML, or passed as a value

```python
# pasted_or_passed.py
# The same typed text, pasted into HTML, then passed to a template as a value.
from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.get("/pasted")
def pasted():
    name = request.args.get("name", "")
    return f"<p>Welcome back, {name}</p>"               # WRONG: text becomes HTML


@app.get("/passed")
def passed():
    name = request.args.get("name", "")
    return render_template_string("<p>Welcome back, {{ name }}</p>", name=name)


client = app.test_client()
typed = "<img src=x onerror=alert(1)>"
for route in ["/pasted", "/passed"]:
    body = client.get(route, query_string={"name": typed}).get_data(as_text=True)
    print(f"{route:8} {body}")
```

Output:

```
/pasted  <p>Welcome back, <img src=x onerror=alert(1)></p>
/passed  <p>Welcome back, &lt;img src=x onerror=alert(1)&gt;</p>
```

The first page contains a real image tag whose error handler runs JavaScript. The second contains
text. The only difference is where the name went: into an f-string, or into a template as a value.

Look at the template text in `/passed`. It is a fixed string written by the programmer. The typed
name is handed over separately, as `name=name`. That is the safe row of the table. **The template text
never contains anything a person typed.**

This is also why no view in this course returns an f-string that contains typed text, even a short
one.

---

## Worked example 3: display and meaning

```python
# display_and_meaning.py
# Escaping decides how an allowed value is shown.
# Validation decides whether a value is allowed at all.
from markupsafe import escape

SEVERITIES = ("low", "medium", "high", "critical")

submissions = [
    {"title": "Laser skips the <b> tag in program 12", "severity": "high"},
    {"title": "Belt squeal", "severity": "apocalyptic"},
]
for issue in submissions:
    allowed = issue["severity"] in SEVERITIES
    print("allowed:", allowed, "| shown as:", escape(issue["title"]), "|", escape(issue["severity"]))
```

Output:

```
allowed: True | shown as: Laser skips the &lt;b&gt; tag in program 12 | high
allowed: False | shown as: Belt squeal | apocalyptic
```

The first issue is legitimate. A technician really is reporting a problem with a `<b>` tag in a
laser program. Refusing it would be wrong. Escaping lets it be shown safely.

The second issue escapes perfectly and is still wrong. `apocalyptic` contains no dangerous
characters, and it is not a severity. Only validation catches it.

---

## The wrong version, and the output it produces

In `templates/issue.html`, change `{{ issue.title }}` to `{{ issue.title | safe }}`. The heading line
of `GET /issues/9` becomes:

```
<h1>Issue 9: <script>document.title='owned'</script></h1>
raw script tag in page: True
```

The script tag is in the page, unescaped. Opened in a browser, the script ran: the tab title changed
from `Issue 9` to `owned`. This one only renames a tab. A real attacker's script could do anything
the page itself can do, for every person who opens the issue.

Because the script was saved in the data and runs for everyone who views it later, this is called
**stored cross-site scripting**.

The fix: remove `| safe`. Jinja's default was already right.

---

## Why the wrong version is tempting

`| safe` sounds like a good thing to add. It reads as "make this safe." It means the opposite: **"I
promise this is already HTML I trust, so do not escape it."** A title typed by a person is never that.

It usually appears for a reason that feels harmless. Someone wants bold text in a description, types
`<b>`, sees the tags printed on the page, and adds `| safe` to make the bold work. It works. It also
makes every script work.

The second temptation is the f-string. `f"<p>Saved: {title}</p>"` is shorter than a template, and it
looks fine with every title you test, because you never type a script into your own form.

The habits:

- Jinja already escapes. Your job is to not turn it off.
- Search your templates for `| safe` before every commit. If you find one, the value must be text your
  program built itself, and a comment must say so.
- Never return an f-string that contains anything a person typed. Never build template text or SQL
  text by joining strings.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Injection** | typed text that becomes part of code because it was pasted into code |
| **Cross-site scripting (XSS)** | an injection where typed text becomes a script that runs in other people's browsers |
| **Stored XSS** | XSS saved in the data, so it runs for everyone who views the record |
| **Escaping** | replacing characters that mean something in a language with codes that only display them |
| **Autoescaping** | Jinja escaping every `{{ value }}` without being asked |
| **`\| safe`** | a Jinja filter that turns escaping off for one value |
| **Server-side template injection** | typed text pasted into template text, so the server runs template syntax inside it |
| **Parameter (SQL)** | a value passed separately from the SQL text, with `?`, so it is never read as SQL |

---

## Self-check

**Question 1.** Which of these is dangerous, and why, in one sentence each?
(a) `return render_template("tool.html", note=note)` with `{{ note }}` in the template
(b) `return f"<p>Checked out: {tool_name}</p>"`, where `tool_name` was typed into the form
(c) `return f"Checkout {checkout_id} saved"`, where `checkout_id` is a number the program computed

**Question 2.** A teammate adds `| safe` to the condition note so that `<i>` shows as italics. What
can now happen, and to whom?

**Question 3.** A condition note reads `Handle is <loose>`. Should the validator refuse it? Explain,
using the difference between escaping and validation.

---

### Answers

**1.** (a) is safe: the note is passed as a value, and Jinja escapes it. (b) is dangerous: the typed
tool name is pasted into HTML, so any tags in it become real tags in the page. (c) is safe: the
number was computed by the program, not typed by a person, so it cannot carry HTML.

**2.** Any note containing a script now runs that script in the browser of every person who opens the
checkout, including people who never saw the form. It is stored cross-site scripting. Italics are not
worth that; show the note as plain text.

**3.** No. It is a legitimate note, and it breaks no rule about length or content. Validation is for
whether a value is allowed. Escaping is for how it is shown, and Jinja will display `<loose>` as text
without running anything.
