# Lecture Notes: Values Travel as Parameters
## 145065 Object-Oriented Programming · Unit 5 · Week 9, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W09_Parameters.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-05-databases-crud-deployment/04-slides/MCCTC_145065_Slides_W09_Parameters.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python. The `sqlite3`
module is part of Python.

**Competencies:** 5.3.11 write code to access data repositories. 9.3.1 identify application
vulnerabilities, here SQL injection.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. Every badge and name in this file is invented.

---

## Why this exists

In 145060 you built strings with f-strings. It is the first tool you reach for. With SQL it is the
wrong one.

A query built with an f-string pastes whatever a person typed into the SQL text. The database cannot
tell your SQL from their typing. Two things follow. A real name with an apostrophe, such as
`Sam O'Brien`, breaks the page. And a person who types SQL on purpose can change what your query does.
That second one is **SQL injection**, and it has leaked real databases for decades.

One habit fixes both: the SQL text never changes, and the values travel separately.

---

## The concept in plain language

**The SQL text is fixed. The values travel separately, as parameters.**

```python
conn.execute("SELECT badge FROM technicians WHERE display_name = ?", (typed,))
```

- The `?` is not a formatting mark. It is a slot.
- The second argument is a tuple of values, one per `?`, in order. A single value still needs the
  comma: `(typed,)`.
- The `sqlite3` driver sends the text and the values to the database separately. The database reads the
  SQL first, then treats each value only as data. Nothing in a value can become SQL.

**Every query lives in `db.py`.** The lab's `db.py` follows three rules, and your project's will too:

1. Values travel as parameters, never pasted into the SQL text.
2. Every function takes the connection as its first argument. The web app passes one per request.
   `manage.py` and `import_csv.py` open their own.
3. Write functions do not commit. The caller wraps them in `transaction()`, which is Wednesday's
   concept.

No other file imports `sqlite3`. The routes call `db.create_issue(conn, clean, now)` and never see SQL.
The lab has a test, `test_only_db_py_touches_sqlite`, that fails if any other file imports it. Why so
strict? In Week 10 the app moves to PostgreSQL. With every query in one file, that move changes one
file. This is 5.1.5 in practice: data management through a language, kept in one place.

**`RETURNING id`** hands back the new row's key from the same `INSERT`. It works in SQLite 3.35 and
later and in PostgreSQL, so the line does not change when the database does.

**A parameter carries a value, never a name.** Table names and column names are part of the SQL text.
When a name must vary, you check it against a fixed list of allowed names first. That list is an
**allow-list**.

---

## Worked example 1: parameters in both directions

```python
# params_demo.py
# Values travel to the database as parameters, never pasted into SQL text.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row                  # rows you can read by column name
conn.executescript("""
CREATE TABLE technicians (id INTEGER PRIMARY KEY, badge TEXT UNIQUE, display_name TEXT);
INSERT INTO technicians (badge, display_name) VALUES ('T-1041', 'Dana Okafor'), ('T-1057', 'Luis Brennan');
""")


def add_technician(conn, badge, display_name):
    # The ? marks are placeholders. sqlite3 sends the values separately.
    row = conn.execute(
        "INSERT INTO technicians (badge, display_name) VALUES (?, ?) RETURNING id",
        (badge, display_name),
    ).fetchone()
    conn.commit()
    return row["id"]


def find_by_name(conn, typed):
    return conn.execute(
        "SELECT badge, display_name FROM technicians WHERE display_name = ?",
        (typed,),
    ).fetchall()


new_id = add_technician(conn, "T-1070", "Sam O'Brien")
print("new id:", new_id)
for typed in ["Sam O'Brien", "x' OR '1'='1"]:
    rows = find_by_name(conn, typed)
    print(f"{typed!r}: {[tuple(r) for r in rows]}")
```

Output:

```
new id: 3
"Sam O'Brien": [('T-1070', "Sam O'Brien")]
"x' OR '1'='1": []
```

The apostrophe in `O'Brien` is stored and found. The injection string matched nothing, because it was
compared as a name, and nobody is named `x' OR '1'='1`. `RETURNING id` gave back 3 without a second
query. `conn.row_factory = sqlite3.Row` lets you write `row["id"]` instead of `row[0]`.

This demo commits inside `add_technician` so it can stand alone. The lab's write functions leave the
commit to the caller.

---

## Worked example 2: a create function in the db.py style

A tool crib checkout. The person at the counter knows a tool tag and a badge, not database ids. The
`INSERT` looks the ids up with small queries inside it.

```python
# crib_create.py
# A create function in the db.py style: connection first, values as parameters,
# the new id back from RETURNING.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.executescript("""
CREATE TABLE technicians (id INTEGER PRIMARY KEY, badge TEXT UNIQUE, display_name TEXT);
CREATE TABLE tools (id INTEGER PRIMARY KEY, tag TEXT UNIQUE, name TEXT);
CREATE TABLE checkouts (id INTEGER PRIMARY KEY,
    tool_id INTEGER REFERENCES tools (id),
    technician_id INTEGER REFERENCES technicians (id),
    note TEXT);
INSERT INTO technicians (badge, display_name) VALUES ('T-1041', 'Dana Okafor');
INSERT INTO tools (tag, name) VALUES ('TW-07', 'Torque wrench 3/8 in'), ('DM-02', 'Digital multimeter');
""")


def create_checkout(conn, tag, badge, note):
    row = conn.execute(
        """
        INSERT INTO checkouts (tool_id, technician_id, note)
        VALUES ((SELECT id FROM tools WHERE tag = ?),
                (SELECT id FROM technicians WHERE badge = ?),
                ?)
        RETURNING id
        """,
        (tag, badge, note),
    ).fetchone()
    return row["id"]


print("checkout", create_checkout(conn, "DM-02", "T-1041", "for the panel on Line 3"))
print("checkout", create_checkout(conn, "TW-07", "T-1041", "100% torque check; don't skip"))
for row in conn.execute("""
        SELECT c.id, t.tag, p.badge, c.note
        FROM checkouts AS c
        JOIN tools AS t ON t.id = c.tool_id
        JOIN technicians AS p ON p.id = c.technician_id"""):
    print(tuple(row))
```

Output:

```
checkout 1
checkout 2
(1, 'DM-02', 'T-1041', 'for the panel on Line 3')
(2, 'TW-07', 'T-1041', "100% torque check; don't skip")
```

Three values, three `?` marks, three items in the tuple, in the same order. The second note holds a
`%`, a `;`, and an apostrophe. All three are stored as plain text. The lab's `add_note()` uses the same
lookup-by-badge pattern. Read it before you write `create_issue`.

---

## Worked example 3: a table name cannot be a parameter

```python
# table_names.py
# A ? carries a value. It cannot carry a table name.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE tools (id INTEGER PRIMARY KEY);
CREATE TABLE checkouts (id INTEGER PRIMARY KEY);
INSERT INTO tools (id) VALUES (1), (2), (3);
""")

try:
    conn.execute("SELECT COUNT(*) FROM ?", ("tools",))
except sqlite3.OperationalError as error:
    print("As a parameter:", error)

KNOWN_TABLES = {"tools", "checkouts"}


def count_rows(conn, table):
    if table not in KNOWN_TABLES:
        raise ValueError(f"unexpected table {table!r}")
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


for asked in ["tools", "checkouts", "tools; DROP TABLE tools"]:
    try:
        print(asked, "->", count_rows(conn, asked))
    except ValueError as error:
        print("Refused:", error)
```

Output:

```
As a parameter: near "?": syntax error
tools -> 3
checkouts -> 0
Refused: unexpected table 'tools; DROP TABLE tools'
```

The database has to know which table a query reads before it can accept any values, so a `?` is not
allowed where a name goes. When a name must vary, the f-string is safe **only after** the name passed
an allow-list that you wrote. The lab's `table_counts()` does exactly this, and it is the one place in
its `db.py` that builds SQL text. The same answer covers "sort by the column the user picked": check
the column against a fixed list first.

---

## The wrong version, and the output it produces

The same search, built with an f-string. Do not copy this.

```python
# params_wrong.py: the same search, built with an f-string. Do not copy this.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE technicians (id INTEGER PRIMARY KEY, badge TEXT UNIQUE, display_name TEXT);
INSERT INTO technicians (badge, display_name) VALUES ('T-1041', 'Dana Okafor'), ('T-1057', 'Luis Brennan');
""")


def find_by_name(conn, typed):
    sql = f"SELECT badge, display_name FROM technicians WHERE display_name = '{typed}'"
    return conn.execute(sql).fetchall()


print(find_by_name(conn, "x' OR '1'='1"))
print(find_by_name(conn, "Sam O'Brien"))
```

**First, the injection.** Output of the first `print`:

```
[('T-1041', 'Dana Okafor'), ('T-1057', 'Luis Brennan')]
```

It returned **every row**, and it raised nothing. Paste the typed text into the SQL and you get
`WHERE display_name = 'x' OR '1'='1'`. The quote in the typing closed the string early, and
`'1'='1'` is true for every row. On a real app, that is every record handed to a stranger.

**Then, the crash.** The second `print`:

```
Traceback (most recent call last):
  File "...\params_wrong.py", line 17, in <module>
    print(find_by_name(conn, "Sam O'Brien"))
          ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "...\params_wrong.py", line 13, in find_by_name
    return conn.execute(sql).fetchall()
           ~~~~~~~~~~~~^^^^^
sqlite3.OperationalError: near "Brien": syntax error
```

The apostrophe in the name closed the string after `Sam O`. The database then read `Brien'` as SQL and
could not make sense of it. The path in the traceback is shortened to `...`. Your line numbers will
match if your file matches.

The crash is the **kind** bug: it stopped the program, and you find it the first time a real person
with an apostrophe uses your page. The injection is the **unkind** bug: it worked, it raised nothing,
and it gave away the table. The same apostrophe is the attacker's first move. One fix handles both:
parameters.

---

## Why the wrong version is tempting

An f-string is the tool you already know, and it works on every name you think to test. `Dana` works.
`Luis` works. The query reads like the sentence you had in your head. The bug waits for a name you did
not think of, or a person who is looking for it.

AI tools can generate f-string SQL too. Read every query an assistant writes for you before you run
it. Friday's Gate 2 exercise gives you generated database code to judge.

The habit that prevents it: **no value ever goes into the SQL text.** If you catch yourself typing an
`f` in front of a SQL string, stop and ask whether the thing inside the braces is a name you checked
against a list. If it is not, it must be a parameter.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Query** | one SQL statement sent to the database |
| **Parameter** | a value sent separately from the SQL text, filling one `?` |
| **Placeholder** | the `?` in the SQL text that a parameter fills |
| **Parameterized query** | a query whose values all travel as parameters |
| **SQL injection** | typed input that changes what a query does, because it was pasted into the SQL text |
| **`RETURNING id`** | a clause that hands back the new row's key from an `INSERT` |
| **`sqlite3.Row`** | a row type you can read by column name |
| **Allow-list** | a fixed list of accepted values, checked before a name goes into SQL text |
| **Data access module** | the one file, `db.py`, that holds every query |

---

## Self-check

**Question 1.** Rewrite this line so the value travels as a parameter:

```python
conn.execute(f"SELECT * FROM tools WHERE tag = '{tag}'")
```

**Question 2.** Why can a table name not be a `?` parameter, and what does the lab's `db.py` do
instead?

**Question 3.** A classmate says, "My f-string query is fine. I tested it with ten names and none of
them broke." Give two inputs that prove otherwise, and what each one does.

---

### Answers

**1.**

```python
conn.execute("SELECT * FROM tools WHERE tag = ?", (tag,))
```

The comma after `tag` makes it a one-item tuple. Without it, `(tag)` is a plain string, and `sqlite3`
treats each character as a separate value. With `tag = "TW-07"`, that fails with
`sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 5 supplied.`

**2.** A parameter carries a value. The database must know which table the query reads before it
accepts any values, so a name has to be part of the SQL text. The lab's `table_counts()` checks each
name against a fixed list of known tables and refuses anything else before the name goes into the
text.

**3.** A name with an apostrophe, such as `Sam O'Brien`, ends the string early and crashes the query
with a syntax error. An injection string such as `x' OR '1'='1` makes the `WHERE` true for every row
and returns the whole table, with no error at all.
