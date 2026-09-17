# Additional Resources · Week 9
## 145065 Object-Oriented Programming · Unit 5 · Week 9
### Topic: relational design and normalization, keys, ER diagrams, SQL with parameters, sqlite3, transactions, and CSV import

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and it matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

**Two program rules apply to every resource below.**

- **No personal data goes into any AI tool or any website.** The practice sites below run SQL on
  their own sample tables. Do not type real names, phone numbers, or anything about a real person into
  them. Monday's lesson is the same rule inside your own schema: a table that does not hold personal
  data cannot leak it.
- **Nothing here needs an account, a payment, or an AI service.** One site below offers graded
  exercises behind a login. Use those only if your instructor sets them up.

**This week is also the Grading Period 3 exam, Thursday.** Every resource here is on-topic for it.

---

## The week at a glance

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | Python for Everybody, the databases chapter | Mon-Wed | On-level | 60 min |
| 2 | Python `sqlite3` documentation | Tue, Wed | On-level | 25 min |
| 3 | SQLite: foreign keys, and transactions | Mon, Wed | On-level | 25 min |
| 4 | Python `csv` documentation | Wed | On-level | 15 min |
| 5 | Videos: Python for Everybody database lectures | Mon, Tue | Remediation | 4 to 12 min each |
| 6 | Practice: SQLBolt | Mon-Fri | On-level | 30 min a sitting |
| 7 | OWASP: SQL injection and query parameterization | Tue, Fri | Extension | 25 min |
| 8 | Video: Computerphile on SQL injection | Tue | Extension | under 20 min, [VERIFY] length |
| 9 | Industry connection: SQL injection is "unforgivable" | Tue, Fri | Extension | 30 min |
| 10 | BPA 345 SQL Database Fundamentals preparation | Fri | Extension | one block |
| 11 | Side quest: SQ-12 or SQ-17 | Fri | Extension | one to two blocks |

---

## 1. Primary reading: Python for Everybody, databases

**Python for Everybody, "Using Databases and SQL"** · `https://www.py4e.com/html3/15-database` ·
**Opened.**

**What it is.** A free book chapter that teaches databases through SQLite and Python. You met this
book in 145060. Find the chapter by its title, not its number, if the site's numbering has changed.

**Why this one.** It covers Monday and Tuesday in the order this course teaches them, with Python you
can run.

**Read these sections:**

| Section | Matches |
|---|---|
| Database concepts, and Creating a database table | Monday warm-up |
| Multiple tables and basic data modeling | Monday. Why one fact lives in one place. |
| Data model diagrams | Monday. How to draw what you designed. |
| Automatically creating primary keys, and Logical keys for fast lookup | Monday |
| Adding constraints to the database | Monday |
| Sample multi-table application | Tuesday |
| Many to many relationships in databases | Extension. The tool crib does not need one. |

**The failure mode to watch for.** Some of the book's examples build a table fresh each run with
`DROP TABLE IF EXISTS`. That is fine for a teaching script. In your app it would erase every record,
which is the same mistake as `init --force` in a build command, next week's warning.

**Time.** 60 minutes across Monday to Wednesday. **Level.** On-level.

### The other free books

- Automate the Boring Stuff · `https://automatetheboringstuff.com/` · **Confident.**
- Think Python · `https://allendowney.github.io/ThinkPython/` · **Confident.**

Neither is the right source for this week. Use Python for Everybody.

---

## 2. Official documentation: `sqlite3`

**Python documentation, "sqlite3: DB-API 2.0 interface for SQLite databases"** ·
`https://docs.python.org/3/library/sqlite3.html` · **Opened.**

**Read three how-to sections, not the whole page.**

- **"How to use placeholders to bind values in SQL queries."** Tuesday. The page warns against
  building queries with Python's string operations and shows the injection that follows. Find the
  example with `' OR TRUE; --` in it. Then find the two placeholder styles it allows.
- **"How to use the connection context manager."** Wednesday. What happens to the transaction when
  the block ends normally, and when it raises.
- **Transaction control.** Wednesday. The page describes more than one way the module handles
  transactions. Read it with the lab's `transaction()` function open beside it.

**Time.** 25 minutes. **Level.** On-level.

---

## 3. Official documentation: SQLite itself

**SQLite, "SQLite Foreign Key Support"** · `https://www.sqlite.org/foreignkeys.html` · **Opened.**

For Monday. Read section 2, "Enabling Foreign Key Support." It says foreign key checks are off by
default and must be turned on for each connection. That is Monday's deliberate error: delete
`PRAGMA foreign_keys = ON` and a row points at a machine that does not exist.

**SQLite, "Transaction"** · `https://www.sqlite.org/lang_transaction.html` · **Opened.**

For Wednesday. `BEGIN`, `COMMIT`, and `ROLLBACK`, and what SQLite does when you never say `BEGIN`.
Note the line that transactions do not nest.

**Time.** 25 minutes. **Level.** On-level.

---

## 4. Official documentation: `csv`

**Python documentation, "csv: CSV File Reading and Writing"** ·
`https://docs.python.org/3/library/csv.html` · **Opened.**

For Wednesday's import. Read the entry for `csv.DictReader` and its example. Then find the footnote
on why files are opened with `newline=''`. A CSV file with a line break inside a quoted field is
exactly the kind of row that breaks an import that skipped this.

**Time.** 15 minutes. **Level.** On-level.

---

## 5. Videos: Python for Everybody lectures

**Python for Everybody, "Databases" lesson page** · `https://www.py4e.com/lessons/database` ·
**Opened.**

**What it is.** The lesson page for the book chapter in section 1, with ten free lecture videos. The lesson page lists each video's length. Three fit this week and this slot:

| Video, as titled on the lesson page | Length listed | Watch before |
|---|---|---|
| Databases - Complex Models - Part 3 | 8:44 | Monday |
| Databases - Relationships - Part 4 | 4:06 | Monday |
| Databases - Foreign Keys - Part 5 | 11:32 | Monday or Tuesday |

"Databases - JOIN - Part 6" (10:30) is a good fourth for anyone behind on joins before next week's
report.

**Why these.** They explain Monday's concept a second way, from the site of a book you already know.
The videos play from YouTube, which may be blocked at school.

**The quizzes and autograded exercises on the same page need a login.** Skip them unless your
instructor sets them up.

**Level.** Remediation.

---

## 6. Practice: SQLBolt

**SQLBolt** · `https://sqlbolt.com/` · **Opened.**

**What it is.** A free set of interactive SQL lessons. Each lesson explains one idea and then gives you
tasks to run against a sample table in the browser. No account was requested while this file was
written.

**Why this one.** You write real SQL and see the result right away, on tables that are not your
project. Suggested order this week:

| Lessons | For |
|---|---|
| The lessons before lesson 6, on SELECT queries | Remediation, before Tuesday |
| Lesson 6, "Multi-table queries with JOINs" · `https://sqlbolt.com/lesson/select_queries_with_joins` · **Opened.** | Tuesday |
| The INSERT, UPDATE, and DELETE lessons | Wednesday |
| The CREATE TABLE and ALTER TABLE lessons | Monday or Friday |

**Two cautions.** The page says its exercises need a recent browser, so check it on the lab browser
once. And SQLBolt's lessons type values straight into the SQL text, because you are the only user.
Your app never does that. The values in your app travel as parameters.

**Time.** 30 minutes a sitting. **Level.** On-level.

---

## 7. The security community's references

**OWASP, "SQL Injection Prevention Cheat Sheet"** ·
`https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html` ·
**Opened.**

For Tuesday and Friday. Read the introduction and the primary defenses. The first defense is
prepared statements with parameters. Also find the defense it recommends for things a parameter cannot
hold, such as a column name to sort by. That is Tuesday's exit ticket, and the lab's `db.py` does the
same thing.

**OWASP, "Query Parameterization Cheat Sheet"** ·
`https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html` · **Opened.**

A page of parameterized query examples in many languages. **It has no Python example.** Use it to see
that every language you will meet, including C# in Unit 6, solves this the same way.

**Time.** 25 minutes. **Level.** Extension.

---

## 8. Video: SQL injection

**Computerphile, "Running an SQL Injection Attack - Computerphile"** ·
`https://www.youtube.com/watch?v=ciNHn38EyRc` · **[VERIFY]**. The title and channel were confirmed
through YouTube's public embed information while this file was written. The running time was not
confirmed from YouTube. Check that it is under 20 minutes before you assign it.

**What it is.** A university researcher demonstrates an injection against a deliberately weak page,
then explains the fix.

**Why this one.** Tuesday's `params_wrong.py` shows the same failure in a few lines. This shows it at
the scale of a real login page.

**The rule, again.** Watching this is fine. Trying it on any system you do not own is not. Your own app
on 127.0.0.1 is the only target this course allows.

**Level.** Extension. YouTube may be blocked at school.

---

## 9. Industry connection: an "unforgivable" defect

**CISA and FBI, "Secure by Design Alert: Eliminating SQL Injection Vulnerabilities in Software"** ·
`https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-sql-injection-vulnerabilities-software`
· **Opened.**

**What it is.** A public alert from two US government agencies to companies that make software. The
page notes that SQL injection has been documented for more than two decades and has been called an
"unforgivable" vulnerability, yet it keeps appearing in products. The full recommendations are in the
alert document linked from the page.

**Why this one.** It shows that the rule you learn on Tuesday is the rule regulators expect
professionals to follow. Manufacturers in this county buy software too. A defect like this in a
supplier's product becomes their problem.

**Write three sentences.** Open the alert document linked from the page and find the technical fix
it recommends. Say whether your `db.py` already follows it. Point to the line that proves it.

**Time.** 30 minutes. **Level.** Extension.

---

## 10. BPA 345 SQL Database Fundamentals

This week's content is the event's content. **Get the current event guidelines from your BPA advisor.**
This file does not link them, because the event number and its guidelines are confirmed each year.

**A practice plan for Friday, from the lesson plan.** Take the lab's schema and write five queries by
hand, on paper first: a join, a filter, a group with a count, a subquery, and an update. Then run each
one against a copy of the lab database and check it.

**Two free references for it.**

- SQLBolt, from section 6 of this file. Its aggregate lessons are next week's topic, and a competitor
  should do them now.
- **PostgreSQL documentation, "Part I. Tutorial"** ·
  `https://www.postgresql.org/docs/current/tutorial.html` · **Opened.** Chapter 2, "The SQL Language,"
  walks through tables, queries, joins, aggregates, updates, and deletions in order. The SQL is
  standard enough to practice on SQLite, and the lab's `POSTGRES.md` lists where the two differ.

**Time.** One block. **Level.** Extension.

---

## 11. Side quests

Both are in `Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**SQ-12 · Read the Source.** ★★, one block. Find a small open-source Python project on GitHub, under
about 500 lines, and read it. Write a two-page report: what it does, how it is organized, one thing the
author did that you would not have thought of, and one thing you would change. Then check its license
and say what shipping it in your own project would require of you. It is done when your reading is
specific enough to quote line numbers.

**Why it fits this week.** Pick a small project that uses `sqlite3`, and read its queries with section
2 of this file open. Does it use placeholders everywhere? If it does not, that belongs in "one thing
you would change."

**SQ-17 · Unit Tests for Something You Already Wrote.** ★★, one to two blocks, unlocks with this
course. Write a real test suite for an old program: the normal case, the edge cases, and at least three
inputs designed to break it. It is done when the suite runs, at least one test fails and exposes a real
defect you did not know about, and you fixed it. The catalog's rule: if nothing fails, write nastier
tests.

**Why it fits this week.** Your tool crib `db.py` is new and not yet tested hard. Try a name with an
apostrophe, a search for `100%`, a checkout for a tool that does not exist, and a return time before
the checkout time.

**Level.** Extension, both.
