# Additional Resources · Week 10
## 145065 Object-Oriented Programming · Unit 5 · Week 10
### Topic: report queries and aggregates, configuration from the environment, deployment, PostgreSQL basics, semantic versioning, Git tags, and usability testing

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year. **Every Render page is
marked [VERIFY] even though it loaded,** because Render's plans, free-tier limits, and terms change.

**Three program rules apply to every resource below.**

- **No personal data goes into any AI tool or any website.** Your outside tester uses an invented
  badge from your seed data and types nothing real. `USER_TEST.md` names the tester's role, never
  their name.
- **No secret goes into any file you commit, or into any website except your host's own settings
  page.** Not in a README, not in a screenshot, not in a question you post for help.
- **Nothing here needs a payment or an AI service.** A hosting account is your instructor's decision
  for this year, not yours. Do not sign up for a host on your own.

---

## The week at a glance

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | The Twelve-Factor App: III. Config | Tue | On-level | 15 min |
| 2 | Flask: Configuration Handling | Tue | On-level | 30 min |
| 3 | SQLite: Built-in Aggregate Functions | Mon | On-level | 15 min |
| 4 | Practice: SQLBolt, outer joins and aggregates | Mon | On-level | 30 min |
| 5 | Flask: Deploying to Production, and Security Considerations | Wed | On-level | 25 min |
| 6 | Render: the Flask guide and the free-tier page | Wed | On-level | 20 min |
| 7 | PostgreSQL documentation: the tutorial and data types | Wed | Extension | 40 min |
| 8 | Semantic Versioning, and Pro Git on tagging | Thu | On-level | 25 min |
| 9 | Nielsen Norman Group: thinking aloud | Thu | On-level | 15 min |
| 10 | Video | Any | Remediation | deliberately unfilled |
| 11 | Industry connection: leaked secrets and misconfiguration | Tue, Fri | Extension | 30 min |
| 12 | Side quest: SQ-08 or SQ-24 | Fri | Extension | two blocks to multi-week |

---

## 1. Primary reading: configuration lives in the environment

**The Twelve-Factor App, "III. Config"** · `https://12factor.net/config` · **Opened.**

**What it is.** One short chapter from a widely cited set of principles for building apps that run
on hosting platforms. The whole set is at `https://12factor.net/` · **Confident.**

**Why this one.** It is Tuesday's concept in one page: the code is the same everywhere, and anything
that changes between your laptop and the server, including secrets and the database address, comes
from environment variables.

**A contested point, worth a paragraph in your decision log.** The chapter argues against grouping
settings into named environments such as "development" and "production." Your lab's `config.py` uses
`APP_ENV` to do exactly that, for one reason: production refuses to start without a real key. Read the
chapter's argument. Then write the strongest case for each side, and say which one fits a small app
with one server.

**Time.** 15 minutes. **Level.** On-level.

---

## 2. Official documentation: Flask configuration

**Flask documentation, "Configuration Handling"** · `https://flask.palletsprojects.com/en/stable/config/`
· **Opened.**

**Read these parts:**

| Part | Matches |
|---|---|
| Debug Mode, and the `DEBUG` entry | Tuesday. It says in bold not to enable debug mode in production. |
| The `SECRET_KEY` entry | Tuesday. It says in bold not to reveal the key when posting questions or committing code. |
| `SESSION_COOKIE_SECURE` and `SESSION_COOKIE_SAMESITE` | Tuesday. Why production cookies are `Secure`. |
| Configuring from Environment Variables | Tuesday |
| Configuration Best Practices | Tuesday. Its first point is the application factory, `create_app()`. |

**The failure mode to watch for.** This page shows example secret keys written into code and config
files, to demonstrate the syntax. Your app never does that. Tuesday's deliberate error is a published
key that still signs a cookie the app accepts.

**Time.** 30 minutes. **Level.** On-level.

---

## 3. Official documentation: aggregate functions

**SQLite, "Built-in Aggregate Functions"** · `https://www.sqlite.org/lang_aggfunc.html` · **Opened.**

**What it is.** The reference for `count`, `sum`, `avg`, `min`, `max`, `total`, and the others.

**Why this one.** Monday's two traps are both on this page.

- **`count(X)` against `count(*)`.** One counts rows where `X` is not NULL. The other counts every row
  in the group. After a `LEFT JOIN`, a tool with no checkouts still has one row. Which count gives it
  0?
- **`avg()` always returns a floating point value** when there is at least one input. Division with
  `/` does not promise that. Monday's deliberate error, `/ 60` against `/ 60.0`, lives in that gap.

**Time.** 15 minutes. **Level.** On-level.

---

## 4. Practice: SQLBolt

**SQLBolt, "SQL Lesson 7: OUTER JOINs"** · `https://sqlbolt.com/lesson/select_queries_with_outer_joins`
· **Opened.**

**SQLBolt, "SQL Lesson 10: Queries with aggregates (Pt. 1)"** ·
`https://sqlbolt.com/lesson/select_queries_with_aggregates` · **Opened.**

**What they are.** Free interactive lessons with tasks you run in the browser against sample tables.
Lesson 7 covers `LEFT`, `RIGHT`, and `FULL` joins. Lesson 10 has you find a maximum, an average by
group, and a total by group.

**Why these.** They are Monday's report in miniature. Do lesson 7, then lesson 10, then the lesson
that follows it on aggregates.

**Caution.** The site says its exercises need a recent browser. Check it on the lab browser once.

**Time.** 30 minutes. **Level.** On-level. Remediation for anyone whose Monday report shows a tool with
1 checkout that was never checked out.

---

## 5. Official documentation: deploying Flask

**Flask documentation, "Deploying to Production"** ·
`https://flask.palletsprojects.com/en/stable/deploying/` · **Opened.**

**What it is.** The Flask maintainers' overview of running an app for real users. It says in bold not
to use the development server in production. It lists production WSGI servers, including Gunicorn and
Waitress, and several hosting platforms.

**Why this one.** It is Wednesday's concept from the source: a deploy runs the same code under a
different server. Note its last line, that most hosting platforms need Flask told it is behind a
proxy. That is Wednesday's "ahead" task.

**Flask documentation, "Security Considerations"** ·
`https://flask.palletsprojects.com/en/stable/web-security/` · **Opened.**

You read the top of this page in Week 8. Now read "Security Headers," "Set-Cookie options," and "Host
Header Validation." Tuesday's "ahead" task, the security headers, comes from here.

**Time.** 25 minutes. **Level.** On-level.

---

## 6. Render, if it is this year's target

Your instructor decides this year's deployment target and writes it on the board: Render, a
school-managed host, or the production-style rehearsal on a lab machine. **Read this section only if
the target is Render.**

**Render documentation, "Deploy a Flask App on Render"** · `https://render.com/docs/deploy-flask` ·
**[VERIFY]**.

**What it is.** Render's own guide. When this file was written it set a build command that installs
`requirements.txt` and a start command that runs the app under Gunicorn. The lab was not built with
Gunicorn, so your rehearsal uses the server the lab names. Compare the two in `DEPLOY.md`.

**Render documentation, "Deploy for Free"** · `https://render.com/docs/free` · **[VERIFY]**.

**What it is.** Render's page on what free services can and cannot do. When this file was written it
said free web services spin down after a period with no traffic, free web services lose local files
on restart, and free databases expire after a set number of days. **Read the current numbers
yourself.** Two of those facts change your app: a SQLite file on a free web service will not survive,
and a free database will not last the year.

**The failure mode.** "It deployed, so it works." Open `/health` on the live app and tick every
checklist item from a real check.

**Time.** 20 minutes. **Level.** On-level.

---

## 7. PostgreSQL basics

**PostgreSQL documentation, "Part I. Tutorial"** ·
`https://www.postgresql.org/docs/current/tutorial.html` · **Opened.**

**What it is.** The official PostgreSQL tutorial, for readers with no prior database experience.
Chapter 2, "The SQL Language," covers tables, queries, joins, aggregate functions, updates, and
deletions. Chapter 3 covers foreign keys and transactions.

**Why this one.** The syllabus target is PostgreSQL. The lab uses SQLite, because it needs no server to
install. Reading sections 2.6, 2.7, 3.3, and 3.4 shows you how close the two
are. The lab's `POSTGRES.md` lists the places they differ.

**PostgreSQL documentation, "Chapter 8. Data Types"** ·
`https://www.postgresql.org/docs/current/datatype.html` · **Opened.**

Read 8.1, "Numeric Types," and 8.5, "Date/Time Types." SQLite stores times however you give them.
PostgreSQL has real time types. That difference is the most likely surprise in a PostgreSQL deploy.

**Time.** 40 minutes. **Level.** Extension, unless PostgreSQL is this year's target. Then it is
on-level.

---

## 8. Versions and tags

**Semantic Versioning 2.0.0** · `https://semver.org/` · **Opened.**

**What it is.** The specification behind version numbers like 1.0.1. Its summary gives the rule:
MAJOR for incompatible changes, MINOR for new features that stay compatible, PATCH for compatible bug
fixes.

**Why this one.** Thursday's exit ticket asks what numbers a fix and a new feature get. The summary
paragraph at the top answers it.

**Pro Git, section 2.6, "Git Basics - Tagging"** · `https://git-scm.com/book/en/v2/Git-Basics-Tagging` ·
**Opened.**

**What it is.** The free Git book's section on tags. It shows annotated tags made with `git tag -a`
and `-m`, and it warns that a plain `git push` does not send tags. That warning is why the lab pushes
the tag by name.

**Git reference, "git-tag"** · `https://git-scm.com/docs/git-tag` · **Opened.**

The full reference. Read the entries for `-a` and `-m`, and the note that `-m` alone makes an annotated
tag.

**Time.** 25 minutes. **Level.** On-level.

---

## 9. Usability testing: watching someone think

**Nielsen Norman Group, "Thinking Aloud: The #1 Usability Tool"** ·
`https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/` · **Opened.**

**What it is.** A free article from a user experience research firm on the think-aloud method: give a
representative user real tasks, ask them to say what they are thinking, and do not interrupt.

**Why this one.** It is Thursday's three-minute briefing, with the reasons behind it. The hardest part
is the one the article stresses and the lesson plan repeats: say nothing while the tester works. Your
instinct will be to help. Helping hides the problem you are there to find.

**Time.** 15 minutes. **Level.** On-level.

---

## 10. Video, under 20 minutes

**Deliberately unfilled.** No video on configuration, deployment, or versioning was confirmed while
this file was written, and this file does not list a title or length it could not check. Your
instructor may choose one under 20 minutes on semantic versioning or on environment variables, watch it
first, and share it. **[VERIFY]** whatever is chosen, including its length.

---

## 11. Industry connection: secrets and settings

**GitHub Docs, "About secret scanning"** ·
`https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning` ·
**Opened.**

**What it is.** GitHub's documentation for a feature that scans repositories, including their full
history, for committed credentials such as API keys and passwords, and raises an alert when it finds
one.

**Why this one.** GitHub built a scanner for this, because committed secrets are a
real and repeated problem, not a classroom one. Note the words "Git history." Deleting a key in a later commit
does not remove it from the history. The fix is a new key.

**OWASP Top 10, "Security Misconfiguration"** ·
`https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/` · **Opened.**

**What it is.** The misconfiguration category from the current edition of the OWASP Top 10. Its list
includes default credentials left unchanged, error pages that show stack traces, and missing security
headers.

**Write three sentences.** Pick three items from that list. For each, name the line in your
`config.py` or your error handlers that prevents it.

**Time.** 30 minutes. **Level.** Extension.

---

## 12. Side quests

Both are in `Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`. **Both assume Render's free tier.
Your instructor confirms this year's terms before assigning either.**

**SQ-08 · Deploy Something Nobody Asked For.** ★★, two blocks. Put something on the public internet
at a URL you can send to somebody. It does not have to be impressive. It has to be live. It is done
when the URL loads from a phone on cell data, not school wifi, and your README explains what deployment
did to your code. The catalog's lesson: the gap between "it works on my machine" and "it works" is
larger than it looks.

**Why it fits this week.** This week is SQ-08 for most of you. A student whose tool crib is already
live may take it to a second small app.

**SQ-24 · Ship for a Real Stakeholder.** ★★★, multi-week. Find somebody outside this class who has a
problem, and solve it for them: a club, a teacher, a coach, a family business, a nonprofit. It needs a
written agreement on scope before you start, at least two meetings, a delivered working thing, and a
handoff document they can use without you. It is done when the stakeholder confirms in writing that
they use it, or explains why they do not. Both outcomes complete the quest.

**Why it fits this week.** For a student whose outside tester asked to keep using the app. The catalog
unlocks SQ-24 in the 145010 capstone or with instructor approval, so ask first. The stakeholder's data
follows the same rule as everything else: no real personal data enters any AI tool.

**Level.** Extension, both.
