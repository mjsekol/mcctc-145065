# Lecture Notes: Each Fact Lives in One Place
## 145065 Object-Oriented Programming · Unit 5 · Week 9, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W09_EachFactInOnePlace.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-05-databases-crud-deployment/04-slides/MCCTC_145065_Slides_W09_EachFactInOnePlace.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python. The
`sqlite3` module is part of Python, so there is nothing to install.

**Competencies:** 5.6.7 document a design using the appropriate tools (your ER diagram). 1.4.3 verify
compliance with security rules and privacy, including record confidentiality. 5.1.5 describe the
concepts of data management through programming languages.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. Every machine, badge, and name in this file is invented.

---

## Why this exists

Your Unit 4 app saves to a JSON file. It reads the whole file and rewrites the whole file. Its own
docstring admits the problem: two saves at the same moment can each read the old file, and one of them
disappears.

A database fixes that. It also brings three things a file never gave you:

- **Keys** make every row findable and every reference checkable.
- **Constraints** refuse a bad row, even when your application has a bug.
- **Transactions** make a group of writes all-or-nothing. That is Wednesday.

Today is about the design. A database can still lie if you design it like a spreadsheet. The rule that
prevents it has a name: **normalization**. Each fact lives in exactly one place.

Data outlives code. You can rewrite a route in ten minutes. A wrong row, a lost row, or a leaked row
is permanent. Everything in this unit protects the data.

---

## The concept in plain language

A database is several small tables that point at each other. It is not one big sheet.

- Each row has a **primary key**, a number that identifies it and never changes.
- A row that belongs to another row stores that row's key. That column is a **foreign key**.
- A machine's name is stored once, in the `equipment` table. An issue does not copy the name. It
  stores the machine's key.
- Rename the machine, and every issue shows the new name, because no issue ever held a copy.

**Constraints** are rules the database itself enforces:

| Constraint | What it refuses |
|---|---|
| `NOT NULL` | an empty value |
| `UNIQUE` | a second row with the same value, such as a second badge T-1041 |
| `CHECK (...)` | a row that breaks a rule you wrote, such as downtime over 1440 minutes |
| `REFERENCES other (id)` | a key that points at a row that does not exist |

Why put a rule in the database when your form already checks it? Because a bug, a script, or a
teammate's new route can skip your form. The database cannot be skipped.

**The ER diagram** is the drawing of this design. ER stands for entity-relationship. Each box is a
table with its columns and keys. Each line is a relationship, marked with its **cardinality**: one
machine has many issues, and each issue belongs to exactly one machine. That is a **one-to-many**
relationship. Drawing it is 5.6.7: you document the design before anyone argues about the code.

**Record confidentiality (1.4.3)** is a design decision too. The Line 3 `technicians` table holds a
badge and a display name. It holds no address, phone number, birth date, or email, because the app
never needs them. **A table that does not hold personal data cannot leak it.** No password, bug, or
stolen laptop can expose a column that does not exist.

---

## Worked example 1: the table that lies

First the problem. One wide table repeats the machine's name on every row.

```python
# flat_table.py
# One big table repeats the machine's name on every row. Watch what a rename does.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE log (issue TEXT, machine_code TEXT, machine_name TEXT)")
conn.executemany("INSERT INTO log VALUES (?, ?, ?)", [
    ("Zone 2 heater slow", "OV-01", "Powder Coat Cure Oven"),
    ("Exhaust fan belt squeal", "OV-01", "Powder Coat Cure Oven"),
])
# Someone renames the oven, but only on the row they were looking at.
conn.execute("UPDATE log SET machine_name = 'Cure Oven 1' WHERE issue = 'Zone 2 heater slow'")
for row in conn.execute("SELECT DISTINCT machine_code, machine_name FROM log"):
    print(row)
```

Output:

```
('OV-01', 'Cure Oven 1')
('OV-01', 'Powder Coat Cure Oven')
```

One machine, two names. The table now disagrees with itself. No query can tell you which name is true.
`":memory:"` builds the database in memory, so nothing is saved to disk.

---

## Worked example 2: the same facts, normalized

```python
# schema_demo.py
# Each fact lives in one place. Issues point at machines by key.
import sqlite3

SCHEMA = """
CREATE TABLE equipment (
    id   INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
CREATE TABLE issues (
    id           INTEGER PRIMARY KEY,
    equipment_id INTEGER NOT NULL REFERENCES equipment (id),
    title        TEXT    NOT NULL
);
"""

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")    # SQLite ignores foreign keys without this
conn.executescript(SCHEMA)
conn.execute("INSERT INTO equipment (code, name) VALUES ('OV-01', 'Powder Coat Cure Oven')")
conn.execute("INSERT INTO issues (equipment_id, title) VALUES (1, 'Zone 2 heater slow')")
conn.execute("INSERT INTO issues (equipment_id, title) VALUES (1, 'Exhaust fan belt squeal')")
conn.execute("UPDATE equipment SET name = 'Cure Oven 1' WHERE code = 'OV-01'")   # one row changes
for row in conn.execute("""
        SELECT i.title, e.code, e.name
        FROM issues AS i JOIN equipment AS e ON e.id = i.equipment_id"""):
    print(row)
try:
    conn.execute("INSERT INTO issues (equipment_id, title) VALUES (99, 'Machine that is not there')")
except sqlite3.IntegrityError as error:
    print("Refused:", error)
print("issues stored:", conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0])
```

Output:

```
('Zone 2 heater slow', 'OV-01', 'Cure Oven 1')
('Exhaust fan belt squeal', 'OV-01', 'Cure Oven 1')
Refused: FOREIGN KEY constraint failed
issues stored: 2
```

One `UPDATE` changed one row, and both issues show the new name. The `JOIN` puts the name back next
to each issue when you read, so you never had to store it twice. The issue for machine 99 was refused,
because machine 99 does not exist.

---

## Worked example 3: the database refuses bad rows

A different setting: the schedule at a pizza shop where you might work. Three rules, three refusals.

```python
# shift_rules.py
# A pizza shop's schedule. The database refuses bad rows, even when the app has a bug.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript("""
CREATE TABLE crew (
    id         INTEGER PRIMARY KEY,
    crew_code  TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL
);
CREATE TABLE shifts (
    id        INTEGER PRIMARY KEY,
    crew_id   INTEGER NOT NULL REFERENCES crew (id),
    starts_at TEXT NOT NULL,
    ends_at   TEXT NOT NULL,
    CHECK (ends_at > starts_at)
);
""")
conn.execute("INSERT INTO crew (crew_code, first_name) VALUES ('C-07', 'Maya')")

attempts = [
    ("a second C-07",
     "INSERT INTO crew (crew_code, first_name) VALUES ('C-07', 'Jordan')"),
    ("a shift that ends before it starts",
     "INSERT INTO shifts (crew_id, starts_at, ends_at) "
     "VALUES (1, '2026-03-06 17:00', '2026-03-06 16:00')"),
    ("a shift for crew member 42",
     "INSERT INTO shifts (crew_id, starts_at, ends_at) "
     "VALUES (42, '2026-03-06 17:00', '2026-03-06 21:00')"),
    ("a good shift",
     "INSERT INTO shifts (crew_id, starts_at, ends_at) "
     "VALUES (1, '2026-03-06 17:00', '2026-03-06 21:00')"),
]
for label, sql in attempts:
    try:
        conn.execute(sql)
        print(f"{label}: stored")
    except sqlite3.IntegrityError as error:
        print(f"{label}: refused ({error})")
print("crew:", conn.execute("SELECT COUNT(*) FROM crew").fetchone()[0],
      "shifts:", conn.execute("SELECT COUNT(*) FROM shifts").fetchone()[0])
```

Output:

```
a second C-07: refused (UNIQUE constraint failed: crew.crew_code)
a shift that ends before it starts: refused (CHECK constraint failed: ends_at > starts_at)
a shift for crew member 42: refused (FOREIGN KEY constraint failed)
a good shift: stored
crew: 1 shifts: 1
```

The `CHECK` at the bottom of `shifts` is a **table-level** rule. It compares two columns in the same
row. The times are text in the form `YYYY-MM-DD HH:MM`, which sorts in time order, so `>` works on
them. Every value in the SQL above is fixed text in the program. Tomorrow you learn how values a person
types must travel instead.

---

## Worked example 4: foreign keys are a setting on each connection

```python
# pragma_check.py
# Foreign key enforcement is a setting on each connection, not on the file.
import pathlib
import sqlite3
import tempfile

with tempfile.TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "crib.db"

    first = sqlite3.connect(path)
    first.execute("PRAGMA foreign_keys = ON")
    print("first connection: ", first.execute("PRAGMA foreign_keys").fetchone())
    first.close()

    second = sqlite3.connect(path)          # same file, new connection
    print("second connection:", second.execute("PRAGMA foreign_keys").fetchone())
    second.close()
```

Output:

```
first connection:  (1,)
second connection: (0,)
```

The setting did not stay with the file. Every new connection starts with enforcement off. That is why
the lab's `connect()` function turns it on, and why every connection your app opens must go through
that one function. The database file lives in a temporary folder that Python deletes at the end.

---

## Worked example 5: the people table is a privacy decision

```python
# people_table.py
# What a people table stores is a privacy decision. List its columns.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE technicians (
    id           INTEGER PRIMARY KEY,
    badge        TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL
)""")
for column in conn.execute("PRAGMA table_info(technicians)"):
    print(column[1], column[2])
```

Output:

```
id INTEGER
badge TEXT
display_name TEXT
```

`PRAGMA table_info` lists a table's columns. Run it on your own people table and read every line. For
each column, ask one question: does a page in this app need it? If no page needs it, the column goes.
The Lab U05-01 starter has a column that fails this test. You will find it in Part 1.

---

## Before your first database file: the .gitignore

In Build 1 you create `instance/line3.db`. **Before you commit anything**, add these lines to the
`.gitignore` of the repository you work in:

```
# Databases are data, not code. Never commit them.
*.db
*.sqlite3
instance/
.env
```

What each line does:

| Line | Ignores |
|---|---|
| `*.db` | any file ending `.db`, in any folder of the repository, because the pattern has no slash |
| `*.sqlite3` | the other common SQLite file ending |
| `instance/` | any folder named `instance`, where Flask apps keep local data |
| `.env` | a file of local settings and secrets. Week 10 explains why it never goes in Git. |

**Check it with `git status`.** After the database file exists, run `git status`. The file
`instance/line3.db` must not appear in the list. If it appears, your `.gitignore` is in the wrong
folder or has a typo. Fix that before you commit.

**Why this matters beyond tidiness.** A commit is permanent in the history. If you commit a database
and delete it in the next commit, the file is still in the earlier commit. Anyone who can clone the
repository can check out that commit and open every record in it. On a public repository, that is
everyone. Removing a file from history takes special tools and still cannot recall copies other people
already cloned. The only reliable fix is never committing it.

---

## The wrong version, and the output it produces

Delete one line from `schema_demo.py`:

```python
conn.execute("PRAGMA foreign_keys = ON")    # SQLite ignores foreign keys without this
```

Run it again. Output:

```
('Zone 2 heater slow', 'OV-01', 'Cure Oven 1')
('Exhaust fan belt squeal', 'OV-01', 'Cure Oven 1')
issues stored: 3
```

There is no `Refused:` line. No error appeared anywhere. The issue for machine 99 was **stored**. It is
issue 3. The join hides it, because a join only shows issues whose machine exists. Where is issue 3's
machine? Nowhere. That row is an **orphan**.

---

## Why the wrong version is tempting

The schema looks right. The `REFERENCES` clause is there, and SQLite accepts it without a word. Then
SQLite ignores it, because enforcement is off on every new connection unless you turn it on. Your app
works. Your pages load. Orphan rows pile up where no page shows them.

It gets worse in Week 10. PostgreSQL always enforces foreign keys. Data that SQLite accepted all week
can make your app fail on the day you deploy.

The habit that prevents it: open every connection through one function that turns enforcement on, and
write a test that tries to store an orphan and expects a refusal.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Table** | a set of rows that all have the same columns |
| **Primary key** | the column that identifies one row, such as `id` |
| **Foreign key** | a column that holds another table's primary key |
| **Constraint** | a rule the database enforces on every write: `NOT NULL`, `UNIQUE`, `CHECK`, `REFERENCES` |
| **One-to-many** | one row on one side, many on the other: one machine, many issues |
| **Cardinality** | how many rows can be on each side of a relationship |
| **Normalized** | designed so each fact is stored in exactly one place |
| **Join** | a query that combines rows from two tables by matching keys |
| **Orphan** | a row whose foreign key points at a row that does not exist |
| **ER diagram** | a drawing of the tables, their keys, and the relationships between them |
| **Record confidentiality** | keeping records about people private, starting with not storing what you do not need |

---

## Self-check

**Question 1.** A tool crib table has the columns `tool_tag`, `tool_name`, `category_name`,
`checked_out_at`. What goes wrong the day the crib renames the category "Torque tools" to "Torque
wrenches"? What would you change in the design?

**Question 2.** Your schema declares `REFERENCES tools (id)`. A test stores a checkout for tool 500,
which does not exist, and the insert succeeds. Name the most likely cause.

**Question 3.** A teammate wants to add `home_address` to the technicians table "in case we need it
later." Give the strongest reason not to, in one sentence.

---

### Answers

**1.** The category name is copied onto every tool row, so the rename has to change every one of those
rows. Miss one and the table holds two names for one category, with no way to tell which is right.
Move categories into their own table, `categories(id, name UNIQUE)`, and give each tool a
`category_id` foreign key. The rename then changes one row.

**2.** Foreign key enforcement is off on that connection. `PRAGMA foreign_keys = ON` was not run on the
connection the test used, often because the test opened its own connection instead of calling the
app's `connect()` function.

**3.** A table that does not hold personal data cannot leak it, and no page in the app needs an address,
so storing it adds risk and nothing else.
