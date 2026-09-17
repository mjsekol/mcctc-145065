# Lecture Notes: Template Inheritance
## 145065 Object-Oriented Programming · Unit 4 · Week 7, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W07_OneLayoutManyPages.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-04-flask-web-framework/04-slides/MCCTC_145065_Slides_W07_OneLayoutManyPages.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python and Flask.
Flask installs Jinja, the template engine, for you.

**Competencies:** 5.5.6 format output (web pages built from templates). 5.5.5 use appropriate
naming conventions and apply comments (template and block names).

**About the setting.** Riverside Fabrication, its Line 3, and its tool crib are a **composite**: an
invented small metal fabrication shop used all semester. No real company is described. Every record
is invented.

---

## Why this exists

A real app has many pages, and every page shares the same header, navigation, and footer. If each
page carries its own copy, then changing the navigation means editing every page. Miss one, and that
page is out of date. The more pages you have, the more certain it is that you will miss one.

**Template inheritance** puts the shared layout in one file. Every page reuses it. Change the layout
once, and every page changes.

You have seen this idea before. In Unit 2, a base class held what every subclass shared, and **a base
class never knows its subclasses**. Today the same rule appears in a second language: **a base
template never knows its pages.**

---

## The concept in plain language

A **template** is a text file, usually HTML, with gaps for values. Flask looks for templates in a
folder named exactly `templates`, next to your app file. A view fills a template with
`render_template("name.html", value=...)`.

Inheritance adds three tags.

| Tag | Where it goes | What it does |
|---|---|---|
| `{% block name %}{% endblock %}` | the base template | marks a named gap a page may fill |
| `{% extends "base.html" %}` | the first line of a page | says "start from this layout" |
| `{% block name %}...{% endblock %}` | the page | fills the gap with that name |

The page fills the blocks the base defines. **The names must match exactly.** The base lists no
pages. Any number of pages can extend it.

A fourth tag shares a smaller piece. `{% include "_table.html" %}` drops the contents of another
template in place. Use it for a table or a card that appears on several pages. A leading underscore
in the file name is a common convention for "this is a piece, not a page."

`{{ value }}` prints a value. `url_for('view_name', ...)` builds a link from a view's name, so a link
never goes stale when an address changes.

---

## Worked example 1: one layout, one page

`templates/base.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}{% endblock %} · Line 3 Maintenance Log</title>
  </head>
  <body>
    <nav><a href="{{ url_for('dashboard') }}">Open work</a></nav>
    <main>
      {% block content %}{% endblock %}
    </main>
    <footer>Riverside Fabrication is a composite.</footer>
  </body>
</html>
```

`templates/issue.html`:

```html
{% extends "base.html" %}
{% block title %}Issue {{ issue.id }}{% endblock %}
{% block content %}
<h1>Issue {{ issue.id }}: {{ issue.title }}</h1>
<p>Machine {{ issue.machine }}, severity {{ issue.severity }}.</p>
{% endblock %}
```

`templates/dashboard.html`:

```html
{% extends "base.html" %}
{% block title %}Open work{% endblock %}
{% block content %}
<h1>Open work</h1>
<ul>
  {% for issue in issues %}
  <li><a href="{{ url_for('issue_detail', issue_id=issue.id) }}">{{ issue.title }}</a></li>
  {% endfor %}
</ul>
{% endblock %}
```

`templates_demo.py`:

```python
# templates_demo.py
# One layout, many pages. Every page extends base.html and fills its blocks.
from flask import Flask, abort, render_template

app = Flask(__name__)

ISSUES = [
    {"id": 1, "machine": "PB-01", "severity": "medium", "title": "Back gauge drifts 2 mm after warm-up"},
    {"id": 3, "machine": "CV-01", "severity": "critical", "title": "Guard interlock trips with the guard closed"},
]


@app.get("/")
def dashboard():
    return render_template("dashboard.html", issues=ISSUES)


@app.get("/issues/<int:issue_id>")
def issue_detail(issue_id):
    for issue in ISSUES:
        if issue["id"] == issue_id:
            return render_template("issue.html", issue=issue)
    abort(404)
```

`GET /issues/3` answered 200 with this HTML:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Issue 3 · Line 3 Maintenance Log</title>
  </head>
  <body>
    <nav><a href="/">Open work</a></nav>
    <main>
      
<h1>Issue 3: Guard interlock trips with the guard closed</h1>
<p>Machine CV-01, severity critical.</p>

    </main>
    <footer>Riverside Fabrication is a composite.</footer>
  </body>
</html>
```

`issue.html` supplied a short title and two lines of content. Every other line came from
`base.html`. The `title` block landed inside `<title>`, and the `content` block landed inside `<main>`. The blank lines
come from the block tags themselves. The lab app tidies them with two Jinja settings, and they do not
change what the browser shows.

---

## Worked example 2: a second page from the same layout

`GET /` rendered `dashboard.html` and answered 200:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Open work · Line 3 Maintenance Log</title>
  </head>
  <body>
    <nav><a href="/">Open work</a></nav>
    <main>
      
<h1>Open work</h1>
<ul>
  
  <li><a href="/issues/1">Back gauge drifts 2 mm after warm-up</a></li>
  
  <li><a href="/issues/3">Guard interlock trips with the guard closed</a></li>
  
</ul>

    </main>
    <footer>Riverside Fabrication is a composite.</footer>
  </body>
</html>
```

Same navigation, same footer, different content. The links were built by
`url_for('issue_detail', issue_id=issue.id)`. If the issue address ever changes in the route, every
link follows without an edit.

---

## Worked example 3: change the base once

This example runs without a server. It uses Jinja directly, the same engine Flask uses, with a
dictionary standing in for the `templates` folder.

```python
# one_layout.py
# Two pages extend one base. Change the base once, and both pages change.
# Flask uses this same Jinja engine; a dictionary stands in for the templates folder.
from jinja2 import DictLoader, Environment

pages = {
    "base.html": "<h1>{% block heading %}{% endblock %}</h1>\n"
                 "{% block content %}{% endblock %}\n"
                 "<footer>Tool crib, Riverside Fabrication (composite)</footer>",
    "tools.html": "{% extends 'base.html' %}"
                  "{% block heading %}All tools{% endblock %}"
                  "{% block content %}<p>{{ count }} tools</p>{% endblock %}",
    "overdue.html": "{% extends 'base.html' %}"
                    "{% block heading %}Overdue{% endblock %}"
                    "{% block content %}<p>{{ count }} overdue</p>{% endblock %}",
}
env = Environment(loader=DictLoader(pages), autoescape=True)
print(env.get_template("tools.html").render(count=8))
print(env.get_template("overdue.html").render(count=1))

print("--- one edit to base.html ---")
pages["base.html"] = pages["base.html"].replace("Tool crib", "Tool crib, second shift")
env = Environment(loader=DictLoader(pages), autoescape=True)
print(env.get_template("tools.html").render(count=8))
print(env.get_template("overdue.html").render(count=1))
```

Output:

```
<h1>All tools</h1>
<p>8 tools</p>
<footer>Tool crib, Riverside Fabrication (composite)</footer>
<h1>Overdue</h1>
<p>1 overdue</p>
<footer>Tool crib, Riverside Fabrication (composite)</footer>
--- one edit to base.html ---
<h1>All tools</h1>
<p>8 tools</p>
<footer>Tool crib, second shift, Riverside Fabrication (composite)</footer>
<h1>Overdue</h1>
<p>1 overdue</p>
<footer>Tool crib, second shift, Riverside Fabrication (composite)</footer>
```

One edit, two pages changed. Neither page file was touched.

---

## Worked example 4: an include shares a piece

```python
# shared_piece.py
# An include shares one piece, here a list of songs, between two pages.
from jinja2 import DictLoader, Environment

pages = {
    "base.html": "<main>{% block content %}{% endblock %}</main>",
    "_song_list.html": "<ul>{% for song in songs %}<li>{{ song }}</li>{% endfor %}</ul>",
    "playlist.html": "{% extends 'base.html' %}{% block content %}"
                     "<h1>Road trip</h1>{% include '_song_list.html' %}{% endblock %}",
    "search.html": "{% extends 'base.html' %}{% block content %}"
                   "<h1>Results</h1>{% include '_song_list.html' %}{% endblock %}",
}
env = Environment(loader=DictLoader(pages), autoescape=True)
print(env.get_template("playlist.html").render(songs=["Track 1", "Track 2"]))
print(env.get_template("search.html").render(songs=["Track 2"]))
```

Output:

```
<main><h1>Road trip</h1><ul><li>Track 1</li><li>Track 2</li></ul></main>
<main><h1>Results</h1><ul><li>Track 2</li></ul></main>
```

`extends` answers "what layout is this page in?" `include` answers "what piece does this page
reuse?" The included piece sees the page's values, here `songs`.

---

## The wrong version, and the output it produces

In `issue.html`, misspell one block name: `{% block content %}` becomes `{% block contnet %}`.
`GET /issues/3` answered **200** and rendered:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Issue 3 · Line 3 Maintenance Log</title>
  </head>
  <body>
    <nav><a href="/">Open work</a></nav>
    <main>
      
    </main>
    <footer>Riverside Fabrication is a composite.</footer>
  </body>
</html>
```

A title, a navigation bar, a footer, and **nothing in between**. No error. No traceback. Status 200.

Jinja accepts a block the parent never defined, and a page that extends a base only shows what lands
in the base's blocks. `contnet` is not one of them, so its content is thrown away. The `title` block
was spelled correctly, which is why the tab still reads `Issue 3`.

The fix: make the page's block name match the base's exactly. When a page is empty between the
header and the footer, compare the block names first.

**The loud version, for comparison.** Name the folder `template` instead of `templates`. Flask cannot
find any page. `GET /` answers 500, and the server prints a traceback that ends:

```
jinja2.exceptions.TemplateNotFound: dashboard.html
```

The loud bug is kinder. It stops you. The quiet one ships.

---

## Why the wrong version is tempting

A misspelled block name is a typo, and typos in Python usually crash. You have learned to trust that
a program which runs without an error is at least wired correctly. Template blocks break that trust:
a page with a wrong block name is perfectly valid to Jinja. It is a page that fills a gap nobody
asked for.

The habit that prevents it: copy block names from the base instead of retyping them, keep the list
of block names in a comment at the top of `base.html`, and look at every new page in the browser
before you commit.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Template** | a text file with gaps that a view fills with values |
| **Base template** | the shared layout that pages extend |
| **Block** | a named gap in the base that a page may fill |
| **`extends`** | the tag on a page's first line that names its layout |
| **`include`** | a tag that drops a shared piece, such as a table, into a page |
| **Template inheritance** | pages reusing one layout by extending it and filling its blocks |
| **`render_template`** | the Flask function that fills a template and returns the page |
| **`url_for`** | builds a link from a view's name, so links follow route changes |

---

## Self-check

**Question 1.** Your app has twelve pages that extend `base.html`. The shop wants a new link in the
navigation bar. How many files do you edit, and which?

**Question 2.** `base.html` defines a block named `content`. A classmate's page fills a block named
`main_content`. What does the browser show for that page, and does Jinja warn anyone?

**Question 3.** Two pages show the same table of overdue tools. Would you put the table in a block of
`base.html`, or in an included file? Explain.

---

### Answers

**1.** One file, `base.html`. Every page that extends it gets the new link, because the navigation
lives only in the base.

**2.** The layout from the base, with an empty space where the content should be, and status 200.
Jinja gives no warning. The base never defined `main_content`, so nothing in the base shows it, and
the page's content is dropped. The fix is to rename the page's block to `content`.

**3.** An included file, such as `_overdue_table.html`. A block in the base would put the table in the
layout of every page, including pages that should not show it. An include places it only on the two
pages that ask for it.
