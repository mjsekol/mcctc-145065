# Unit 4 Project · Tool Crib on the Web
## 145065 Object-Oriented Programming · Unit 4 · Weeks 7-8

**Gate 3.** Full tooling, AI allowed and logged. **Solo.** Due **Week 8, Friday, at the end of the
commit window.** Graded on the 100-point project rubric, in Projects.

**Riverside Fabrication is a composite**: an invented small metal fabrication shop used all semester.
The attendant, the technicians, the badges, and every tool below are invented. No real person or
company is described.

**This app grows in Unit 5.** Week 9 moves its data into a database and Week 10 puts it on a server.
Build it so that the part that reads and writes data lives in one module. You will replace that module,
and nothing else should have to change.

---

## The brief

> **From:** the tool crib attendant, Line 3, Riverside Fabrication
> **About:** getting the tool crib off the clipboard
>
> Right now the crib runs on a clipboard. When a tech takes a torque wrench, they write their badge and
> the time on the sheet. When they bring it back, I cross it off. Mostly.
>
> Here is what goes wrong. I can't tell at a glance what is out. When a supervisor asks where the
> 60-inch-pound torque driver is, I flip pages. Things come back late and nobody notices until the next
> shift needs them. And last month a meter went out on the floor two weeks past its calibration date.
> That one cannot happen again. Quality would have to re-check every part it touched.
>
> What I want is a page on the shop network. I open it and see what is out right now, with the late
> ones first. I can look at the whole crib, or one kind of tool. I can open one tool and see who has had
> it. And when a tech takes something, they check it out on a form instead of the clipboard.
>
> A few things about the crib. Every tool has a tag, like TC-101. They are grouped: torque tools,
> measuring tools, electrical, and so on. Some tools have a calibration due date and some do not need
> one. Techs have badges like T-1041. Supervisors have badges that start with S. A tool goes out for a
> shift, a day, or a weekend. Nothing should be out longer than three days. A tech can leave a short
> note about the tool's condition when they take it.
>
> The badge list and the tool list I can give you as a file for now. I don't want people typing things
> into the page that break it, and I don't want anyone checking a tool out from some other website.
> Our IT person was very clear about that.
>
> Returns can wait until the next version. I mostly need to see what's out, and to stop the clipboard.

**Your first job is to turn that message into requirements.** Some are stated. Some are implied. Some
questions have no answer in the message, and you write those down instead of guessing.

---

## What you are building

A Flask app, `toolcrib-web`, that reads a versioned JSON store and shows the crib on web pages, with a
checkout form that saves good input and refuses bad input.

---

## Technical requirements

Numbered so your tests and your demo can refer to them.

**Routes and templates**

- **T1.** At least **five routes** that answer GET, including at least two with a URL variable and one
  that reads a query string. A suggested set: `/` (what is out now), `/tools` (`?category=`),
  `/tools/<tag>`, `/checkouts` (`?status=`), `/checkouts/<int:checkout_id>`.
- **T2.** A checkout form: `GET /checkouts/new` shows it, `POST /checkouts/new` saves it.
- **T3.** **Template inheritance.** Every page extends one `base.html`. No page repeats the header,
  the navigation, or the footer.
- **T4.** A value the app does not know in a query string answers **400**. A tool or checkout that does
  not exist answers **404**. Both use your own error page, which extends the base.
- **T5.** The footer says that Riverside Fabrication is a composite.

**Data**

- **T6.** One JSON store file with a `format_version`, read through one module, `store.py`, that returns
  objects to the routes. The routes never open the file.
- **T7.** The store checks every field and every reference on load: a checkout that names a tool or
  badge not in the file, a due time before the checkout time, and a wrong version are refused with your
  own exception class. **Never pickle.**
- **T8.** A store that cannot be read gives a **503** page that tells the attendant what to do, and no
  traceback. The details go to the server's terminal.
- **T9.** Saving keeps a backup of the previous file and writes through a temporary file, the Unit 3
  habit.

**The form**

- **T10.** The server refuses bad input with **400**, lists every problem at the top of the form, links
  each message to its field, marks the field invalid, and keeps the person's answers.
- **T11.** Rules the server enforces, at minimum:
  - the badge is `T` or `S`, a hyphen, and four digits, after trimming and upper-casing, **and** it is on
    the list
  - the tool is on the list, **and** it is not already out
  - a tool whose calibration date has passed cannot go out
  - the time allowed is a whole number of hours from 1 to 72
  - the note is optional and at most 200 characters
- **T12.** The form's HTML hints (`required`, `pattern`, `min`, `max`, `maxlength`) come from the same
  constants the server uses.
- **T13.** A good checkout is saved, confirmed once with a flash message, and answered with a **303**
  redirect to the checkout's page. Refreshing that page saves nothing.

**Security**

- **T14.** Every typed value is shown as text. No `| safe` on anything a person typed. No view returns an
  f-string that contains anything a person typed.
- **T15.** Every POST carries a CSRF token that matches the session, or it is refused with **403**.
- **T16.** `SECRET_KEY` comes from the environment. No key is written in any file. Debug is off.
- **T17.** The development server takes an explicit port and refuses a busy one.

**Evidence**

- **T18.** A `unittest` suite with Flask's test client that runs on a temporary copy of the store and
  covers every rule in T11, the 400, 403, 404, and 503 answers, and escaping. At least 15 tests.
- **T19.** `ATTACK_LOG.md`: at least four attacks you sent to your own app on 127.0.0.1, what came back,
  and which line stopped each one.
- **T20.** Every page your app serves, saved and passed through `tools/web-check` (see below), with the
  result in your README.

---

## Required repository structure

```
toolcrib-web/
  README.md             what it is, how to run it, how to test it, what is not finished
  REQUIREMENTS.md       your numbered requirements and your questions for the client
  ROUTES.md             method, path, function, template, and the not-found answer, for each route
  decision-log.md       every design decision, each naming the pattern chosen and the one rejected
  ATTACK_LOG.md         T19
  AI_USAGE.md           every AI use: the tool, what you asked, what you kept, what you checked
  .gitignore            includes .venv/, __pycache__/, *.bak, *.tmp
  app.py
  models.py
  store.py
  validation.py
  security.py
  data/toolcrib.json    invented records only
  templates/            base.html and one template per page
  static/               your stylesheet
  test_app.py
  save_pages.py         copied from project-files/ and edited for your routes
```

`AI_USAGE.md` is required whether or not you used AI. "No AI used this week" is a valid entry.

---

## DMAIC checkpoints

| Phase | What is due | When |
|---|---|---|
| **Define** (M1) | `REQUIREMENTS.md` with at least eight testable requirements and three questions; first decision log entry | Week 7, Monday, end of Build 2 |
| **Measure** (M2) | `data/toolcrib.json` with at least 8 tools in 3 categories, 3 technicians, 5 checkouts (one late, one returned); `ROUTES.md` with the counts your pages must show | Week 7, Tuesday, end of Build 2 |
| **Analyze** (M3) | page sketches naming templates and blocks; a decision log entry naming a chosen and a rejected pattern; `templates/base.html` | Week 7, Wednesday, end of Build 2 |
| **Improve** (M4) | five routes answer, every page extends the base, the store's checks have tests | Week 7, Friday, end of Build 2 |
| **Improve** (M5-M8) | the form posts and redirects (M5, Mon); the rules and their tests (M6, Tue); `ATTACK_LOG.md` with three attacks (M7, Wed); CSRF and a fourth attack (M8, Thu) | Week 8, Monday to Thursday, end of Build 2 |
| **Control** | every test passes, web-check passes, README true, paired demo given | Week 8, Friday, commit window |

Agile ceremonies live inside Improve. Each Improve day starts with a two-line stand-up in your README's
log: what you finished yesterday, what you will finish today.

---

## Constraints, and why each exists

| Constraint | Why |
|---|---|
| Flask and the Python standard library only. No Flask-WTF, no ORM, no front-end framework. | You write every part of the request cycle, the validation, and the token yourself, so you can explain them. Nothing else is installed on the lab image for this unit. |
| No `debug=True`, ever. | The debugger's error page runs Python for anyone who reaches it. |
| No real names, badges, or personal information. Invented records only. | Program rule: no personal data in any project or any AI tool. |
| Attacks go to your own app on 127.0.0.1 and nowhere else. | The Lab Acceptable Use and Safety Agreement. |
| No returns in this version. | The client asked for it later, and Unit 5's update lesson is where it belongs. A return is fine as an EXTENDED feature only after T1-T20 are done. |
| No login. | Out of scope. Say so in your README's "not finished" section. |
| The store is JSON. No database yet. | Week 9 replaces it. Keep all file access in `store.py` so that replacement is one module. |

---

## Milestones

| When | Milestone |
|---|---|
| Week 7 Mon | M1 Define |
| Week 7 Tue | M2 Measure |
| Week 7 Wed | M3 Analyze |
| Week 7 Thu | store module and first two pages |
| Week 7 Fri | M4: five routes |
| Week 8 Mon | M5: the form saves and redirects |
| Week 8 Tue | M6: the rules |
| Week 8 Wed | M7: the attack log |
| Week 8 Thu | M8: CSRF, tests, web-check, README |
| **Week 8 Fri** | **Paired demo in Build 2. Submission at the end of the commit window.** |

---

## Three worked scope examples

Pick your target on Monday and write it in your decision log. You may move up. Moving down after
Wednesday costs Process points.

### Small, and completely finished

Five GET routes: `/`, `/tools`, `/tools/<tag>`, `/checkouts`, `/checkouts/<int:checkout_id>`. The
checkout form with every T11 rule. A plain stylesheet. Fifteen tests. Four attacks logged. Every page
passes web-check.

**What it earns.** Full marks are possible. A small app with every requirement met, true documentation,
and a clean demo beats a large app with gaps.

### Medium, and the one most students should aim for

Everything in Small, plus: the category and status filters combine; the dashboard shows late checkouts
first with how many hours late; a tool's page shows its full history and whether its calibration is due
within 14 days; the flash message names the tool and the due time; 25 or more tests, including a truth
table for the "already out" and "calibration passed" rules.

### Large, and only if Small is finished by Week 8, Tuesday

Everything in Medium, plus one of: a return form as a second POST route with its own rules and tests; a
Content-Security-Policy header with an explanation of what it blocks; a JSON route that returns what is
out now, with its own 400 and 404 answers and tests. Record the choice in your decision log.

### Scope calibration, three signals

- **Too big:** on Week 7, Wednesday, `ROUTES.md` has more than eight routes, or the sketches include a
  login page.
- **Too small:** on Week 7, Friday, the app has five routes but no store checks, or the store is a Python
  dictionary in `app.py`.
- **About right:** on Week 8, Tuesday, the form refuses every T11 rule and the tests say so.

---

## Grading · the 100-point project rubric

| Dimension | Points |
|---|---|
| Functionality | 25 |
| Code Quality | 20 |
| Documentation | 20 |
| Process | 15 |
| Demonstration | 10 |
| Polish | 10 |

### What each dimension means here

**Functionality, 25.** T1 through T17 work on a fresh copy of your store. Every rule in T11 refuses what
it should and accepts what it should. A good checkout redirects and saves once. A broken store gives the
503 page.

**Code Quality, 20.** Scored on the five-dimension standard: Correctness, Security, Readability,
Performance, Requirements Fit. Routes never open the file. Nothing a person typed reaches HTML, a
template's text, or a file without passing through the validator and the escaper. Names say what the
thing does. Comments agree with the code under them. The store is read once per request, not once per
tool.

**Documentation, 20.** README, REQUIREMENTS, ROUTES, decision log, ATTACK_LOG, and AI_USAGE, all present
and all true. The README's run and test commands work when a partner follows them word for word.

**Process, 15.** A commit at the end of every period. M1 through M8 on time. A stand-up line for every
Improve day. Decision log entries that name a chosen and a rejected pattern.

**Demonstration, 10.** The five-minute paired demo below, scored by your partner on the checklist and
spot-checked by the instructor.

**Polish, 10.** The pages are readable by the attendant: high contrast, targets large enough for a
gloved hand, late checkouts marked by words and shape as well as color. Every page passes web-check.
Nothing is left over from the lab.

---

## The five-minute demo script

Five minutes. Your partner times it and scores it.

| Minutes | What you show |
|---|---|
| 0:00-0:30 | The problem, in one sentence, in the attendant's words |
| 0:30-1:30 | The dashboard, a filtered tool list, and one tool's page. Say which requirement each shows. |
| 1:30-2:30 | A good checkout: the form, the redirect, the confirmation, and a refresh that saves nothing |
| 2:30-3:30 | A refused checkout: a tool already out, and a tool past calibration. Show the messages. |
| 3:30-4:30 | One attack from `ATTACK_LOG.md`, sent live to your own app, and the line of code that stopped it |
| 4:30-5:00 | One thing you would change, and the question below |

### The question

Your partner asks one of these, chosen by the instructor, and you answer in under 30 seconds:

1. "Show me the line that stops a tool from going out twice."
2. "What happens if someone deletes the `required` attribute and submits?"
3. "Why does your app redirect after saving?"
4. "What would a broken JSON file look like to the attendant?"

### The ten-point demonstration checklist

Your partner ticks each one. One point each.

- [ ] Finished inside five minutes
- [ ] Stated the problem in the client's terms
- [ ] Named the requirement each screen shows
- [ ] Showed the redirect and the refresh
- [ ] Showed two different refusals with their messages
- [ ] Sent a real attack to their own app
- [ ] Pointed at the line of code that stopped it
- [ ] Every page shown extends the same layout
- [ ] Named one change they would make
- [ ] Answered the question correctly without looking it up

`project-files/DEMO_CHECKLIST.md` is the printable copy.

---

## Saving your pages for web-check

`project-files/save_pages.py` asks your running app for each page and saves the HTML. Edit its `PAGES`
list to match your routes. With your app running on port 8680:

```
python save_pages.py --port 8680
```

Then, from the course repository root on a lab machine:

```
node tools/web-check/check.js <path to your toolcrib-web folder>/saved/*.html
```

Paste the PASS lines into your README.

---

## Submission checklist

- [ ] `python -m unittest` passes, with at least 15 tests
- [ ] `python app.py --port 8680` starts with `SECRET_KEY` set and refuses a busy port
- [ ] Every T1-T20 requirement is met, or your README's "not finished" section says which is not and why
- [ ] Every saved page passes web-check, and your README shows it
- [ ] `ATTACK_LOG.md` has four real attacks
- [ ] `decision-log.md` names at least two design patterns you chose and one you rejected for each
- [ ] `AI_USAGE.md` is filled in
- [ ] No real person's information anywhere, and no secret in any file
- [ ] The last commit is inside the Week 8 Friday commit window, and it is pushed
