# Additional Resources · Week 7
## 145065 Object-Oriented Programming · Unit 4 · Week 7
### Topic: Flask as a dependency and its licenses, the request cycle, routes, templates, and reading a data store

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**Two program rules apply to every resource below.**

- **No personal data goes into any AI tool or any website.** Not yours, not a classmate's, not a
  tester's. Every name, badge, and record you type anywhere is invented.
- **Nothing here needs an account, a payment, or an AI service.** If a page asks you to sign up, stop
  and ask your instructor.

---

## The week at a glance

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | Flask Quickstart | Mon-Thu | On-level | 40 min |
| 2 | Flask: Templates, and the Template Inheritance pattern | Wed | On-level | 20 min |
| 3 | Jinja Template Designer Documentation | Wed | Extension | 25 min |
| 4 | Flask: Handling Application Errors | Thu | On-level | 20 min |
| 5 | Licenses: Flask's own license and choosealicense.com | Mon | On-level | 20 min |
| 6 | Video: Corey Schafer, Flask tutorial Part 1 | Mon, Tue | Remediation | under 20 min, [VERIFY] length |
| 7 | Practice: the official Flask tutorial, on your own machine | Any | Extension | one to three blocks |
| 8 | Industry connection: software supply chains | Mon, Fri | Extension | 30 min |
| 9 | Side quest: SQ-12 or SQ-21 | Fri | Extension | one to two blocks |

---

## 1. Primary reading: the Flask Quickstart

**Flask documentation, "Quickstart"** · `https://flask.palletsprojects.com/en/stable/quickstart/` ·
**Opened.**

**What it is.** The official tour of Flask, from the people who maintain it. Flask's documentation is
free to read and is the primary source for every Flask call in this unit.

**Why this one.** It covers the whole week in one page. Read these sections, in this order:

| Section | Matches |
|---|---|
| A Minimal Application | Monday. Find the sentence that tells you not to name your file `flask.py`. That is Monday's deliberate error. |
| Routing, with Variable Rules and its converter table | Tuesday. The `int` converter is why `/issues/three` never reaches your function. |
| URL Building | Tuesday and Wednesday |
| Rendering Templates | Wednesday |
| Redirects and Errors | Thursday |

**Skip for now:** File Uploads, Cookies, and Sessions. Sessions come in Week 8.

**Two things on this page this course does differently.** Name them before they trip you.

- The Quickstart runs the server with `flask --app hello run` on port 5000. The lab runs
  `python app.py --port 8680`, because a Flask development server can start silently on a busy port
  on the lab machines.
- The Quickstart shows debug mode. This course never turns it on. The same page's warning says why:
  the debugger lets someone run code on your computer from a browser.

**Time.** 40 minutes, split across the week. **Level.** On-level. Remediation for anyone whose Tuesday
exit ticket missed.

### Free books you already know

- Automate the Boring Stuff · `https://automatetheboringstuff.com/` · **Confident.**
- Think Python · `https://allendowney.github.io/ThinkPython/` · **Confident.**
- Python for Everybody · `https://www.py4e.com/` · **Confident.**

None of them teaches Flask. Use them to refresh the Unit 3 habits this week's store
depends on: reading JSON and raising your own exceptions.

---

## 2. Official documentation: templates

**Flask documentation, "Templates"** · `https://flask.palletsprojects.com/en/stable/templating/` ·
**Opened.**

**What it is.** How Flask sets up Jinja. Its "Jinja Setup" list says which template file extensions
get automatic escaping. Its "Controlling Autoescaping" section names the three ways to turn escaping
off. Read that section now and remember it. Week 8, Wednesday is about why you do not.

**Flask documentation, "Template Inheritance"** ·
`https://flask.palletsprojects.com/en/stable/patterns/templateinheritance/` · **Opened.**

**What it is.** A two-section page: one base template with blocks, one child that extends it. It is
Wednesday's concept on one screen. Note the sentence that says the `extends` tag must be the first tag
in the template.

**Give yourself one question, not the pages:** "If I misspell a block name in the child, what does the
page show, and why does nothing complain?"

**Time.** 20 minutes. **Level.** On-level.

---

## 3. Jinja Template Designer Documentation

`https://jinja.palletsprojects.com/en/stable/templates/` · **Opened.**

**What it is.** The full reference for the template language: template inheritance, `include`,
macros, filters, and HTML escaping.

**Why this one.** It is where to go when Wednesday's "ahead" task asks you to turn the severity badge
into a macro. It also explains `include` and how an included template sees the current variables.

**Skip for now:** the sections on extensions, sandboxing, and anything about writing your own
filters. They are not this unit.

**Time.** 25 minutes. **Level.** Extension.

---

## 4. Official documentation: errors that never show a traceback

**Flask documentation, "Handling Application Errors"** ·
`https://flask.palletsprojects.com/en/stable/errorhandling/` · **Opened.**

**What it is.** How Flask picks an error handler: by status code first, then by exception class,
most specific first.

**Why this one.** Thursday's `StoreError` handler is this page applied to your own exception. Read
"Error Handlers" and "Custom Error Pages." Find the sentence that says a handler does not set the
status code for you. That is the most common Thursday bug.

**Skip:** "Error Logging Tools." It recommends a hosted error service, which would need an account.
This course does not use one.

**Time.** 20 minutes. **Level.** On-level.

---

## 5. Licenses: what "open source" lets you do

**Flask's license page** · `https://flask.palletsprojects.com/en/stable/license/` · **Opened.**

**What it is.** The full text of Flask's license, the BSD-3-Clause License. It is short. Count its
three numbered conditions.

**choosealicense.com, "BSD 3-Clause" License** ·
`https://choosealicense.com/licenses/bsd-3-clause/` · **Opened.**

**choosealicense.com, "Licenses"** · `https://choosealicense.com/licenses/` · **Opened.**

**What they are.** A plain-language site that sorts each license into permissions, conditions, and
limitations. The BSD 3-Clause page lists commercial use, distribution, modification, and private use
as permissions, and keeping the license and copyright notice as the condition.

**Why these.** Monday's `LICENSES.md` needs a row for each package Flask brought with it. Two of them
report only "BSD License." That label does not say which BSD. Open the package's own LICENSE file,
count the numbered conditions, and then compare with the BSD 3-Clause page here.

**The failure mode.** "It's open source, so I can do anything." Every license on the list page has at
least one condition. The most permissive ones still ask you to keep a notice.

**Time.** 20 minutes. **Level.** On-level.

---

## 6. Video, under 20 minutes

**Corey Schafer, "Python Flask Tutorial: Full-Featured Web App Part 1 - Getting Started"** ·
`https://www.youtube.com/watch?v=MwZwr5Tvyxo` · **[VERIFY]**. The title and channel were confirmed
through YouTube's public embed information while this file was written. The running time was not.
Check that it is under 20 minutes before you assign it.

**What it is.** A screen-recorded walkthrough of installing Flask and serving a first page.

**Why this one.** For a student who missed Monday or Tuesday and wants to watch a first route being
written. It uses its own setup commands, not the lab's. Follow the lab for anything you type.

**Do not go on to Part 2 as a class assignment.** It is a good video, but a search result lists it at
over 30 minutes, so it is outside this slot.

**Level.** Remediation. YouTube may be blocked on the school network. Watch it at home.

---

## 7. Practice: the official Flask tutorial

**Flask documentation, "Tutorial"** · `https://flask.palletsprojects.com/en/stable/tutorial/` ·
**Opened.**

**What it is.** A step-by-step build of a small blog called Flaskr, in eleven chapters from "Project
Layout" to "Deploy to Production." It is not a browser exercise. You build it on your own machine,
which is the practice.

**Why this one.** It is the same framework, written by the same people, with a different app. After
the lab, it shows you how much of Flask you already recognize.

**Rules for doing it here.**

- Build it in a scratch folder, not inside your `oop-semester` or `toolcrib-web` repository.
- Run it on 127.0.0.1 on a port you choose. Do not use debug mode.
- The app has user registration. Every username and password you type is invented, and none is a
  password you use anywhere else.
- It uses a SQLite database from chapter 3. That is Week 9's topic, so it is fine to read that chapter
  now and come back to it.

**Time.** One to three blocks. **Level.** Extension.

---

## 8. Industry connection: the software you did not write

**OWASP Top 10, "Software Supply Chain Failures"** ·
`https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/` · **Opened.**

**What it is.** One category from the current edition of the OWASP Top 10, the most widely cited list
of web application security risks. This category is about the components your software depends on.
It tells teams to track the versions of every component they use, including the ones their
dependencies pulled in.

**CISA, "Software Bill of Materials (SBOM)"** · `https://www.cisa.gov/sbom` · **Opened.**

**What it is.** The US Cybersecurity and Infrastructure Security Agency's page on software bills of
materials. It describes an SBOM as a nested list of the ingredients that make up a piece of software.

**Why these.** Your Monday `LICENSES.md` is a tiny bill of materials: every package, its version, and
its license. Companies that sell software to manufacturers are increasingly asked for exactly this
list.

**Write two sentences.** What is in your `LICENSES.md` that an SBOM also needs? What would an SBOM need
that your file does not have?

**Time.** 30 minutes. **Level.** Extension.

### The current article slot

**Deliberately unfilled.** No news article about a specific supply chain incident was confirmed while
this file was written, and this file does not name an incident it could not check. If you want one,
pick a current piece from a trade or news outlet the week you teach this, confirm the incident in a
second source, and use it with the OWASP page above. **[VERIFY]** whatever you choose.

---

## 9. Side quests

Both are in `Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**SQ-12 · Read the Source.** ★★, one block, unlocks any time after Unit 4. Find a small open-source
Python project on GitHub, under about 500 lines. Read it. Write a two-page report: what it does, how
it is organized, one thing the author did that you would not have thought of, and one thing you would
change. Then check its license and say what shipping it in your own project would require of you.
It is done when your reading is specific enough to quote line numbers.

**Why it fits this week.** It is Monday's license question applied to code you read closely. If you
asked how Werkzeug parses a request, you may read one of its functions for curiosity. Werkzeug is far
larger than the catalog's 500-line limit, though, so the report needs a small project.

**SQ-21 · The Accessibility Pass.** ★★, one to two blocks. Take a page you built and navigate it using
only the keyboard. Then use a screen reader with your eyes closed. It is done when you can complete
every task on the page without a mouse and without looking, and your README lists what you fixed and
what you could not.

**Why it fits this week.** Your lab app now has real pages. The catalog lists SQ-21 under 145010, so
your instructor offers it here only to students who have finished Project M4.

**Level.** Extension, both.
