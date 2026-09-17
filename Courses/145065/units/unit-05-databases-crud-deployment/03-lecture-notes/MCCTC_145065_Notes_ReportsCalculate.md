# Lecture Notes: A Report Calculates; It Never Stores
## 145065 Object-Oriented Programming · Unit 5 · Week 10, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W10_ReportsCalculate.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-05-databases-crud-deployment/04-slides/MCCTC_145065_Slides_W10_ReportsCalculate.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python. The `sqlite3`
module is part of Python.

**Competencies:** 5.5.6 format output, here a report. 5.2.3 write code that uses arithmetic
operations. 1.4.2 use software applications to locate, record, analyze, and present information, here a
report and its spreadsheet export for a supervisor.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. Every machine and record in this file is invented.

---

## Why this exists

A supervisor plans Monday's shift from the downtime report. If the report says the oven lost 1 hour
when it lost 1 hour and 15 minutes, the plan is wrong, and nobody knows why.

Numbers on a report go wrong in two ways. The first is a **stored total** that drifts: a column
someone forgot to update when a record was edited or deleted. The second is **arithmetic** that looks
right and is not: division that throws away the fraction, rounding that differs between two
languages, a count that counts the wrong thing.

Today fixes both. A report calculates every number from the rows, every time it runs, and you check
each calculation against a hand-worked answer.

---

## The concept in plain language

**A calculated field is computed from the rows each time the report runs.** It is never stored. So it
can never disagree with the rows.

The tools, one line each:

| SQL | What it does |
|---|---|
| `GROUP BY e.id` | makes one output row per machine |
| `COUNT(i.id)` | counts the issues in the group, skipping empty values |
| `COUNT(*)` | counts rows in the group, whatever they hold |
| `SUM(i.downtime_minutes)` | adds the values in the group |
| `AVG(...)` | the average of the values in the group, skipping empty values |
| `ROUND(x, 2)` | rounds to 2 decimal places |
| `COALESCE(x, 0)` | gives `x`, or `0` when `x` is empty |
| `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` | counts only the rows that match a condition |
| `LEFT JOIN` | keeps every row on the left, even one with nothing to join |

**`LEFT JOIN` versus `JOIN`.** A plain `JOIN` keeps only machines that have issues. A report of every
machine must show a machine with none, so it uses `LEFT JOIN`. For that machine, the issue columns come
back empty. In SQL, an empty value is `NULL`.

**Three arithmetic traps**, each verified below:

1. **Integer division.** In SQLite, an integer divided by an integer throws away the fraction:
   `75 / 60` is `1`. Divide by `60.0` to keep it: `1.25`. Python 3 does the opposite: `75 / 60` is
   `1.25`, and you ask for the whole number with `75 // 60`.
2. **Rounding differs.** SQLite's `ROUND(1.25, 1)` gives `1.3`. Python's `round(1.25, 1)` gives `1.2`.
   Python rounds an exact half to the even neighbor. SQLite rounds it away from zero. If your report
   and your hand calculation disagree by 0.1, check this first.
3. **`COUNT(*)` with a `LEFT JOIN`.** A machine with no issues still produces one joined row, with empty
   issue columns. `COUNT(*)` counts that row and reports 1. `COUNT(i.id)` skips the empty value and
   reports 0.

---

## Worked example 1: the downtime report

```python
# report_demo.py
# A report calculates its numbers from the rows every time. It stores none of them.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript("""
CREATE TABLE equipment (id INTEGER PRIMARY KEY, code TEXT UNIQUE);
CREATE TABLE issues (id INTEGER PRIMARY KEY, equipment_id INTEGER REFERENCES equipment (id),
                     status TEXT, downtime_minutes INTEGER);
INSERT INTO equipment (code) VALUES ('CV-01'), ('OV-01'), ('PB-02'), ('LC-02');
INSERT INTO issues (equipment_id, status, downtime_minutes) VALUES
    (1, 'open', 90), (2, 'in_progress', 60), (2, 'closed', 15), (3, 'open', 0);
""")

REPORT = """
SELECT e.code,
       COUNT(i.id)                                              AS issues,
       SUM(CASE WHEN i.status <> 'closed' THEN 1 ELSE 0 END)     AS open_issues,
       COALESCE(SUM(i.downtime_minutes), 0)                     AS minutes,
       ROUND(COALESCE(SUM(i.downtime_minutes), 0) / 60.0, 2)    AS hours
FROM equipment AS e
LEFT JOIN issues AS i ON i.equipment_id = e.id
GROUP BY e.id, e.code
ORDER BY minutes DESC, e.code
"""

print(f"{'machine':8} {'issues':>6} {'open':>5} {'minutes':>8} {'hours':>6}")
for row in conn.execute(REPORT):
    print(f"{row['code']:8} {row['issues']:>6} {row['open_issues'] or 0:>5} "
          f"{row['minutes']:>8} {row['hours']:>6}")
```

`LC-02` is an invented laser with no issues yet. It is there to show what a `LEFT JOIN` keeps.
Output:

```
machine  issues  open  minutes  hours
CV-01         1     1       90    1.5
OV-01         2     1       75   1.25
LC-02         0     0        0    0.0
PB-02         1     1        0    0.0
```

Read each column.

- `issues`: `COUNT(i.id)` counts issues, so LC-02 shows 0.
- `open`: `SUM(CASE ...)` adds 1 for each issue that is not closed. OV-01 has one open and one closed.
  For LC-02 the sum is empty, so Python prints `row['open_issues'] or 0`.
- `minutes`: `COALESCE` turns "no issues" into 0 instead of an empty value.
- `hours`: `/ 60.0` keeps the fraction. 75 minutes is 1.25 hours.
- The order: most downtime first, then by code. LC-02 and PB-02 both have 0 minutes, so the code
  decides, and `LC` comes before `PB`.

**Check it by hand.** OV-01 has two issues, 60 and 15 minutes. 60 + 15 = 75. 75 / 60 = 1.25. The
report agrees. A test that compares every cell with a table you worked out by hand is how you prove a
report is right. Lab U05-02 checks yours against such a table.

---

## Worked example 2: the same arithmetic, two languages

```python
# arithmetic_two_ways.py
# The same arithmetic in SQL and in Python. They do not always agree.
import sqlite3

conn = sqlite3.connect(":memory:")
print("SQL    75 / 60, 75 / 60.0, 75 % 60:",
      conn.execute("SELECT 75 / 60, 75 / 60.0, 75 % 60").fetchone())
print("Python 75 / 60, 75 // 60, 75 % 60: ", (75 / 60, 75 // 60, 75 % 60))
print("SQL    ROUND(1.25, 1):", conn.execute("SELECT ROUND(1.25, 1)").fetchone()[0])
print("Python round(1.25, 1):", round(1.25, 1))
print("SQL    ROUND(2.5), Python round(2.5):",
      conn.execute("SELECT ROUND(2.5)").fetchone()[0], round(2.5))
```

Output:

```
SQL    75 / 60, 75 / 60.0, 75 % 60: (1, 1.25, 15)
Python 75 / 60, 75 // 60, 75 % 60:  (1.25, 1, 15)
SQL    ROUND(1.25, 1): 1.3
Python round(1.25, 1): 1.2
SQL    ROUND(2.5), Python round(2.5): 3.0 2
```

- The `/` sign means different things. In SQLite, integer `/` integer is whole-number division. In
  Python 3, `/` always keeps the fraction.
- `%` is the remainder in both: 75 minutes is 1 hour and 15 minutes.
- On an exact half, the two languages round differently. The OV-01 row above has 1.25 hours. Rounded
  to one place by SQLite, it shows 1.3. Rounded by Python, it would show 1.2. Decide where your report
  rounds, and round in one place only.

---

## Worked example 3: a practice log, and why nothing is stored

A setting from your own week: minutes practiced on each song for a band's next show.

```python
# practice_report.py
# Practice time per song, calculated from the session rows every time.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript("""
CREATE TABLE songs (id INTEGER PRIMARY KEY, title TEXT UNIQUE);
CREATE TABLE sessions (id INTEGER PRIMARY KEY, song_id INTEGER REFERENCES songs (id),
                       minutes INTEGER);
INSERT INTO songs (title) VALUES ('Warmup Song'), ('Encore'), ('Closer');
INSERT INTO sessions (song_id, minutes) VALUES (1, 45), (1, 50), (2, 200);
""")

REPORT = """
SELECT s.title,
       COUNT(p.id)                                  AS sessions,
       ROUND(COALESCE(SUM(p.minutes), 0) / 60.0, 1) AS hours,
       ROUND(AVG(p.minutes) / 60.0, 1)              AS avg_hours
FROM songs AS s
LEFT JOIN sessions AS p ON p.song_id = s.id
GROUP BY s.id, s.title
ORDER BY hours DESC, s.title
"""
for row in conn.execute(REPORT):
    print(dict(row))

conn.execute("DELETE FROM sessions WHERE id = 3")      # a session logged by mistake
print("after deleting session 3:")
for row in conn.execute(REPORT):
    print(dict(row))
```

Output:

```
{'title': 'Encore', 'sessions': 1, 'hours': 3.3, 'avg_hours': 3.3}
{'title': 'Warmup Song', 'sessions': 2, 'hours': 1.6, 'avg_hours': 0.8}
{'title': 'Closer', 'sessions': 0, 'hours': 0.0, 'avg_hours': None}
after deleting session 3:
{'title': 'Warmup Song', 'sessions': 2, 'hours': 1.6, 'avg_hours': 0.8}
{'title': 'Closer', 'sessions': 0, 'hours': 0.0, 'avg_hours': None}
{'title': 'Encore', 'sessions': 0, 'hours': 0.0, 'avg_hours': None}
```

Check two cells by hand. Warmup Song: 45 + 50 = 95 minutes, and 95 / 60 = 1.583, which rounds to 1.6.
The average session is 95 / 2 = 47.5 minutes, and 47.5 / 60 = 0.79, which rounds to 0.8.

Two lessons in this output.

- **The delete fixed the report with no extra code.** Encore dropped to 0 the moment its session was
  deleted, because the report recalculated. A stored `total_hours` column on `songs` would still say
  3.3 until someone remembered to update it.
- **`AVG` of nothing is `None`.** Closer has no sessions, so its average is empty, not 0. That is
  honest: there is no average of nothing. Your page must decide what to show, such as a dash, instead
  of printing `None`. `COALESCE` would turn it into 0, which would claim an average that does not
  exist.

---

## The wrong version, and the output it produces

Change `/ 60.0` to `/ 60` in `report_demo.py`:

```python
       ROUND(COALESCE(SUM(i.downtime_minutes), 0) / 60, 2)      AS hours
```

Output:

```
machine  issues  open  minutes  hours
CV-01         1     1       90    1.0
OV-01         2     1       75    1.0
LC-02         0     0        0    0.0
PB-02         1     1        0    0.0
```

No error. A plausible number. And wrong: 90 minutes became 1 hour, and 75 minutes became 1 hour. A
supervisor who plans a shift around this report loses half an hour on the conveyor without knowing why.

**A second trap.** Put `/ 60.0` back and change `COUNT(i.id)` to `COUNT(*)`:

```
machine  issues  open  minutes  hours
CV-01         1     1       90    1.5
OV-01         2     1       75   1.25
LC-02         1     0        0    0.0
PB-02         1     1        0    0.0
```

LC-02 now claims 1 issue. It has none. The `LEFT JOIN` produced one row for it with empty issue
columns, and `COUNT(*)` counted that row.

---

## Why the wrong version is tempting

You have written Python for a year, and in Python 3, `75 / 60` is `1.25`. It is natural to assume SQL
shares the rule. It does not. And the wrong answer is a whole number of hours, which looks like a
reasonable report.

`COUNT(*)` is tempting because it is the count you learned first, and it gives the right answer for
every machine that has at least one issue. The bug shows only on the machine with none.

The stored total is tempting because it looks faster. At the size of a shop's maintenance log,
calculating takes milliseconds. A stored total is a real technique for very large tables, and it comes
with a plan for keeping it true on every insert, edit, and delete. Without that plan, it drifts.

The habit that prevents all three: work one row of the report out by hand before you trust the query,
and include a row with nothing to count.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Calculated field** | a report value computed from the rows each time the report runs |
| **Aggregate function** | a function that turns many rows into one value: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |
| **`GROUP BY`** | splits the rows into groups, one output row per group |
| **`LEFT JOIN`** | a join that keeps every row of the left table, even with no match |
| **`NULL`** | SQL's empty value. Python receives it as `None`. |
| **`COALESCE`** | returns the first value that is not `NULL` |
| **Integer division** | division that throws away the fraction |
| **Round half to even** | Python's rule for exact halves: 1.25 rounds to 1.2, 2.5 rounds to 2 |
| **Hand calculation** | the answer you work out yourself, used as the test's expected value |

---

## Self-check

**Question 1.** Write the exact output:

```python
import sqlite3
c = sqlite3.connect(":memory:")
c.execute("CREATE TABLE t (m INTEGER)")
c.executemany("INSERT INTO t VALUES (?)", [(45,), (50,)])
print(c.execute("SELECT SUM(m) / 60, SUM(m) / 60.0, ROUND(AVG(m), 1) FROM t").fetchone())
```

**Question 2.** Your tool crib report shows 1 checkout for a tool that has never been checked out. Name
the likely cause in one phrase.

**Question 3.** A teammate wants to add a `total_hours_out` column to the `tools` table "so the report
is faster." What question should you ask them, and what is the strongest case on each side?

---

### Answers

**1.**

```
(1, 1.5833333333333333, 47.5)
```

45 + 50 = 95. Integer division gives 1. Decimal division gives 1.5833333333333333. The average of 45
and 50 is 47.5.

**2.** `COUNT(*)` with a `LEFT JOIN`, counting the one empty joined row. Use `COUNT(c.id)`.

**3.** Ask: "What updates it when a checkout is edited or voided?" For the stored column: a report on a
very large table reads one value per tool instead of adding up every checkout. Against it: every
insert, edit, and delete must also update the total, one missed update makes the report wrong until
someone notices, and at the size of a tool crib the calculation takes milliseconds.
