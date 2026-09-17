# One Layout, Many Pages
---
## Slide 1: Forty pages, one new link
- The club website has forty pages
- Every page has its own menu copy
- The club adds one new page
- How many files do you edit
Speaker notes: Picture a club website where every page carries its own copy of the menu. The club adds a page, and now the menu needs a new link. That is forty edits, and you will miss one. Somebody will click the old menu on the page you missed. Today you fix that for good.
Image: A grid of forty small page thumbnails, one with an outdated menu circled in launch red.
---
## Slide 2: One layout, many pages
- The base template holds the shared layout
- It marks named gaps called blocks
- Each page extends the base and fills blocks
- The base never names its pages
Speaker notes: Here is the idea. The layout lives in one file. Each page says which layout it extends and fills the gaps. You met this rule in Unit 2. A base class never knows its subclasses. A base template never knows its pages. Same design, second language.
Image: One wide layout frame at the top with arrows down to three different page cards.
---
## Slide 3: The base
```html
<title>{% block title %}{% endblock %} · Line 3 Maintenance Log</title>
<nav><a href="{{ url_for('dashboard') }}">Open work</a></nav>
<main>
  {% block content %}{% endblock %}
</main>
<footer>Riverside Fabrication is a composite.</footer>
```
Speaker notes: This is base dot html, trimmed to the lines that matter. Two blocks, title and content. The navigation link is built with url for, from the view's name, so it never goes stale. Riverside Fabrication is our composite shop, and the footer says so on every page.
Image: None. This slide is code.
---
## Slide 4: A page
```html
{% extends "base.html" %}
{% block title %}Issue {{ issue.id }}{% endblock %}
{% block content %}
<h1>Issue {{ issue.id }}: {{ issue.title }}</h1>
<p>Machine {{ issue.machine }}, severity {{ issue.severity }}.</p>
{% endblock %}
```
Speaker notes: This is issue dot html, the whole file. The first line names the layout. Then it fills the two blocks, with names that match the base exactly. There is no navigation and no footer in this file. Watch where they come from.
Image: None. This slide is code.
---
## Slide 5: What the browser receives
```html
    <title>Issue 3 · Line 3 Maintenance Log</title>
    <nav><a href="/">Open work</a></nav>
    <main>
<h1>Issue 3: Guard interlock trips with the guard closed</h1>
<p>Machine CV-01, severity critical.</p>
    </main>
    <footer>Riverside Fabrication is a composite.</footer>
```
Speaker notes: These are the key lines of the real page for issue 3, status 200. The title block landed inside the title tag. The content block landed inside main. The navigation and footer came from the base. Now I change the footer text in base dot html and reload two different pages. Both change.
Image: None. This slide is code.
---
## Slide 6: Include shares a piece
- extends: which layout is this page in
- include: which piece does this page reuse
- Use include for a shared table
- Underscore names mark pieces, not pages
Speaker notes: One more tag. Extends picks the layout. Include drops a smaller piece, like a table of issues, into any page that asks for it. The lab puts the issue table in an included file, so two pages share it. A leading underscore in the file name tells a reader it is a piece, not a page.
Image: Two page cards each containing the same small table, linked to one file labeled _table.html.
---
## Slide 7: One letter off
```html
{% extends "base.html" %}
{% block title %}Issue {{ issue.id }}{% endblock %}
{% block contnet %}
<h1>Issue {{ issue.id }}: {{ issue.title }}</h1>
<p>Machine {{ issue.machine }}, severity {{ issue.severity }}.</p>
{% endblock %}
```
Speaker notes: I misspell content. Two letters swapped. Predict: does the page crash, show an error, or something else?
Image: None. This slide is code.
---
## Slide 8: Status 200, empty page
```html
    <title>Issue 3 · Line 3 Maintenance Log</title>
    <nav><a href="/">Open work</a></nav>
    <main>
      
    </main>
    <footer>Riverside Fabrication is a composite.</footer>
```
Speaker notes: Status 200. A title, a navigation bar, a footer, and nothing in the middle. Why did Jinja not complain? A page may define any block it likes. The base only shows the blocks it defined. Contnet is not one of them, so its content is thrown away. The quiet bug is the dangerous one, because it ships.
Image: None. This slide is code.
---
## Slide 9: The loud one, for comparison
- Folder named template instead of templates
- `GET /` answers 500
- TemplateNotFound: dashboard.html
- Loud bugs stop you; quiet bugs ship
Speaker notes: Here is the loud version. Name the folder template, singular, and Flask finds no pages at all. You get a 500 and a traceback ending in TemplateNotFound. That one is kind. It stops you. When a page is empty between header and footer, compare block names first.
Image: A red error banner next to a calm empty page, labeled loud and quiet.
---
## Slide 10: What you are about to build
- Lab U04-01 Part 3, steps 7 to 12
- The equipment list with a one-pass count
- The machine page for one piece of equipment
- Both pages extend base.html, issue table included
Speaker notes: Build 1 is Lab U04-01 Part 3. You build the equipment list, counting open issues in one pass, then the page for one machine. Both templates extend the base, and both include the shared issue table. When you are done, the equipment page shows OV-01 with 1 open issue, and no template repeats the header or footer.
Image: An equipment table with six machines and an open-issue count column, navy header.
