# Lecture Notes: A Transaction Makes Many Writes One Change
## 145065 Object-Oriented Programming · Unit 5 · Week 9, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W09_Transactions.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-05-databases-crud-deployment/04-slides/MCCTC_145065_Slides_W09_Transactions.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python. The `sqlite3`,
`csv`, and `contextlib` modules are part of Python.

**Competencies:** 5.3.11 write code to access data repositories, here updates and deletes. 5.5.7 read
inputs, here a CSV data file. 5.3.10 code error handling techniques, here a failed write that undoes
itself.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. Every record in this file is invented.

---

## Why this exists

Purchasing sends a spreadsheet of 40 rows. Your import stops on row 23 because someone typed 5000
minutes of downtime. How many rows are in the table now?

If each row was saved on its own, the answer is 22. Nobody knows which 22 without reading the table
row by row. Fix row 23, run the import again, and rows 1 through 22 go in a second time. Now the table
has duplicates, and nothing tells you which import each row came from.

The job was "load this file." Half of a job is worse than none of it. A **transaction** makes the whole
file one change: every row goes in, or none do.

---

## The concept in plain language

**A transaction groups writes.** If every write in the block succeeds, the database **commits**: the
changes become permanent. If any write fails, it **rolls back**: every change in the block is undone,
and the table is exactly as it was before the block started.

In Python, one small function gives you that behavior with a `with` block:

```python
@contextmanager
def transaction(conn):
    """Commit if the block finishes. Roll back if anything in it raises."""
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
```

- `yield conn` is where your `with` block runs.
- If the block finishes, `conn.commit()` makes every write permanent.
- If anything in the block raises, `conn.rollback()` undoes every write, and `raise` passes the error
  on so the caller still sees it. A rollback that hid the error would be a second bug.

**Updates and deletes report how many rows they changed.** `cursor.rowcount` after an `UPDATE` or a
`DELETE` is that count. An `UPDATE ... WHERE id = ?` for an id that does not exist changes 0 rows and
raises nothing. Your code must check the number. The lab's delete route answers 404 when nothing was
deleted.

**A delete asks first.** `GET /issues/<id>/delete` shows an "are you sure?" page and changes nothing.
Only a `POST` from that page, with the CSRF token, deletes. Why not a delete link? A link can be
followed by a browser that preloads pages, by a search engine's crawler, by a bookmark, or by someone
curious. A form cannot be submitted by accident. On a shop floor, an operator in gloves hits the wrong
button, so a destructive action always gets a confirmation.

**An import checks every row first.** Read the whole file. Check each row with the same rules as the
form. Collect every problem with its line number. If there are any problems, import nothing and print
them all. Only a clean file goes into the transaction.

---

## Worked example 1: the import that undoes itself

```python
# transaction_demo.py
# A transaction groups writes: every one of them happens, or none of them do.
import sqlite3
from contextlib import contextmanager

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE issues (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    downtime_minutes INTEGER NOT NULL CHECK (downtime_minutes BETWEEN 0 AND 1440))""")


@contextmanager
def transaction(conn):
    """Commit if the block finishes. Roll back if anything in it raises."""
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise


ROWS = [("Assist gas pressure drops", 35), ("Roller 14 bearing noise", 0),
        ("Downtime typed wrong", 5000), ("Muting lamp out", 20)]

try:
    with transaction(conn):
        for title, minutes in ROWS:
            conn.execute("INSERT INTO issues (title, downtime_minutes) VALUES (?, ?)",
                         (title, minutes))
except sqlite3.IntegrityError as error:
    print("Import refused:", error)
print("rows in the table:", conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0])
```

Output:

```
Import refused: CHECK constraint failed: downtime_minutes BETWEEN 0 AND 1440
rows in the table: 0
```

The first two inserts worked. The third broke the `CHECK` rule. The rollback undid the first two as
well. Zero rows. That is the whole point: the table is exactly as it was, and you can fix the file and
run it again with nothing to clean up. The 1440 is the number of minutes in a day.

---

## Worked example 2: count what changed

A setting you know: scanning concert tickets at the door.

```python
# ticket_scans.py
# UPDATE and DELETE tell you how many rows they changed. Check the number.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE tickets (id INTEGER PRIMARY KEY, code TEXT UNIQUE, scanned_at TEXT);
INSERT INTO tickets (code) VALUES ('GA-0412'), ('GA-0413');
""")


def scan(conn, code, now):
    cursor = conn.execute(
        "UPDATE tickets SET scanned_at = ? WHERE code = ? AND scanned_at IS NULL",
        (now, code),
    )
    conn.commit()
    return "come in" if cursor.rowcount == 1 else "already used or not a ticket"


def refund(conn, code):
    cursor = conn.execute("DELETE FROM tickets WHERE code = ?", (code,))
    conn.commit()
    return cursor.rowcount


print("GA-0412 at the door:     ", scan(conn, "GA-0412", "19:02"))
print("GA-0412 a screenshot:    ", scan(conn, "GA-0412", "19:40"))
print("GA-9999 made up:         ", scan(conn, "GA-9999", "19:41"))
print("refund GA-0413, rows:    ", refund(conn, "GA-0413"))
print("refund GA-0413 again:    ", refund(conn, "GA-0413"))
print(conn.execute("SELECT code, scanned_at FROM tickets").fetchall())
```

Output:

```
GA-0412 at the door:      come in
GA-0412 a screenshot:     already used or not a ticket
GA-9999 made up:          already used or not a ticket
refund GA-0413, rows:     1
refund GA-0413 again:     0
[('GA-0412', '19:02')]
```

Neither the second scan nor the made-up code raised an error. Each one changed 0 rows, and only the
`rowcount` said so. `AND scanned_at IS NULL` makes the first scan the only one that counts, so a
friend's screenshot of your ticket does not get in. These functions commit on their own to keep the
demo short. In the lab, the route wraps the call in `transaction()`.

---

## Worked example 3: check every row, then import

A playlist file, exported from a spreadsheet. It has two bad rows, and one invisible problem.

```python
# playlist_import.py
# Read every row. Check every row. Import only if every row passed.
import csv
import io
import sqlite3

# What a spreadsheet's "CSV UTF-8" export can start with: an invisible marker.
raw = ("\ufefftitle,seconds\n"
       "Warmup Song,184\n"
       ",201\n"
       "Encore,three minutes\n"
       "Closer,242\n").encode("utf-8")

print("read as utf-8:    ", next(csv.reader(io.StringIO(raw.decode("utf-8")))))
print("read as utf-8-sig:", next(csv.reader(io.StringIO(raw.decode("utf-8-sig")))))

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE songs (id INTEGER PRIMARY KEY, title TEXT NOT NULL, seconds INTEGER NOT NULL)")

clean, problems = [], []
for line, row in enumerate(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))), start=2):
    title = row["title"].strip()
    if not title:
        problems.append(f"line {line}: title: Every song needs a title.")
    if not row["seconds"].strip().isdigit():
        problems.append(f"line {line}: seconds: Enter the length as a whole number of seconds.")
    if title and row["seconds"].strip().isdigit():
        clean.append((title, int(row["seconds"])))

if problems:
    print(f"Nothing imported. {len(problems)} problem(s):")
    for problem in problems:
        print(" ", problem)
else:
    with conn:                        # sqlite3's own block: commit, or roll back on an error
        conn.executemany("INSERT INTO songs (title, seconds) VALUES (?, ?)", clean)
print("songs in the table:", conn.execute("SELECT COUNT(*) FROM songs").fetchone()[0])
```

Output:

```
read as utf-8:     ['\ufefftitle', 'seconds']
read as utf-8-sig: ['title', 'seconds']
Nothing imported. 2 problem(s):
  line 3: title: Every song needs a title.
  line 4: seconds: Enter the length as a whole number of seconds.
songs in the table: 0
```

Three things to notice.

- **The invisible marker.** Some spreadsheet programs start a UTF-8 file with a **byte order mark**.
  Read with `utf-8`, the first column is named `'\ufefftitle'`, not `'title'`, and `row["title"]`
  raises `KeyError: 'title'` on the first row. Read with `utf-8-sig`, the marker is removed. The lab's `import_csv.py` opens
  files with `utf-8-sig` for this reason.
- **Line numbers start at 2.** Line 1 is the header, so the first data row is line 2. The person fixing
  the file sees the same numbers in their spreadsheet.
- **Every problem, not only the first.** A report that stops at the first bad row makes the person
  fix, rerun, fix, rerun. Listing all of them saves every round after the first.

A `sqlite3` connection used as `with conn:` commits when the block finishes and rolls back if it
raises. It does the same job as `transaction()`. The lab uses its own `transaction()` so the same code
works with PostgreSQL in Week 10.

---

## The wrong version, and the output it produces

Move the commit inside the loop and drop the `transaction()` block:

```python
# transaction_wrong.py: commit after every row. Do not copy this.
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE issues (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    downtime_minutes INTEGER NOT NULL CHECK (downtime_minutes BETWEEN 0 AND 1440))""")

ROWS = [("Assist gas pressure drops", 35), ("Roller 14 bearing noise", 0),
        ("Downtime typed wrong", 5000), ("Muting lamp out", 20)]

try:
    for title, minutes in ROWS:
        conn.execute("INSERT INTO issues (title, downtime_minutes) VALUES (?, ?)",
                     (title, minutes))
        conn.commit()
except sqlite3.IntegrityError as error:
    print("Import refused:", error)
print("rows in the table:", conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0])
```

Output:

```
Import refused: CHECK constraint failed: downtime_minutes BETWEEN 0 AND 1440
rows in the table: 2
```

The error message is identical to the good version. The table is not. Two rows made it in and two did
not. The message says "refused," and a person reading it believes nothing was imported. Fix the bad row,
run the import again, and the first two rows are in the table twice.

---

## Why the wrong version is tempting

Committing after each row feels careful. Every row that worked is saved. It also looks like progress:
the table fills as you watch. And on a clean file, the two versions give exactly the same result, so
every test with good data passes.

The difference only shows on a bad file, which is the file you did not test with.

The habit that prevents it: decide what one "change" is before you write the loop. For an import, the
whole file is one change. Put the loop inside one transaction, and write a test that imports a file with
one bad row and expects zero rows afterward.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Transaction** | a group of writes that all happen or none happen |
| **Commit** | make the writes in a transaction permanent |
| **Rollback** | undo every write in a transaction |
| **Context manager** | an object used with `with`, which runs code before and after the block |
| **`cursor.rowcount`** | how many rows the last `UPDATE` or `DELETE` changed |
| **CRUD** | create, read, update, delete: the four things an app does with records |
| **Confirmation page** | a `GET` page that asks "are you sure?" before a `POST` does something permanent |
| **Byte order mark** | an invisible character some programs put at the start of a UTF-8 file |
| **`utf-8-sig`** | the encoding name that reads UTF-8 and removes a byte order mark if one is there |
| **Dry run** | a run that checks everything and changes nothing |

---

## Self-check

**Question 1.** Your import stops on row 23 of 40. With a transaction, how many rows are in the table?
Without one, committing after each row?

**Question 2.** `update_checkout(conn, 999, ...)` runs an `UPDATE ... WHERE id = ?` and raises no
error, but there is no checkout 999. How does your code find out, and what should the route answer?

**Question 3.** A teammate says: "A delete link is fine. My delete route checks the CSRF token on every
POST." What is wrong with that reasoning?

---

### Answers

**1.** With a transaction: 0, because the failure on row 23 rolls back rows 1 through 22. Without one:
22, the rows before the failure, and nothing records which ones they are.

**2.** It reads `cursor.rowcount` after the `UPDATE`. A count of 0 means no row matched. The function
returns `False`, and the route answers 404.

**3.** A link sends a `GET`, and the CSRF check runs only on `POST`. A browser preloading pages, a
crawler, a bookmark, or a person opening the link to look would delete the record with no token and no
confirmation. `GET` must show the "are you sure?" page, and only the `POST` from that page, with the
token, deletes.
