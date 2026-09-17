# Values Travel as Parameters
---
## Slide 1: The name that breaks the page
- A new technician joins: Sam O'Brien
- He types his name into your form
- The page crashes
- Another visitor types something stranger and sees everyone
Speaker notes: Here is a real risk for the app you are building this week. Someone with an apostrophe in their name uses your search, and the page falls over. That one is annoying. The other visitor, the one who typed a quote on purpose, is worse, because nothing crashes for them. Today you learn the one habit that stops both.
Image: A search box containing an apostrophe, with a cracked page behind it, launch red accent.
---
## Slide 2: The f-string you already know
```python
def find_by_name(conn, typed):
    sql = f"SELECT badge, display_name FROM technicians WHERE display_name = '{typed}'"
    return conn.execute(sql).fetchall()


print(find_by_name(conn, "x' OR '1'='1"))
print(find_by_name(conn, "Sam O'Brien"))
```
Speaker notes: This is how most of you would write it, because f-strings are what you know from last year. The table has two invented technicians. Predict what each print does. The first one is an injection string. The second is a real name.
Image: None. This slide is code.
---
## Slide 3: First the injection, then the crash
```
[('T-1041', 'Dana Okafor'), ('T-1057', 'Luis Brennan')]
Traceback (most recent call last):
  File "...\params_wrong.py", line 17, in <module>
    print(find_by_name(conn, "Sam O'Brien"))
          ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "...\params_wrong.py", line 13, in find_by_name
    return conn.execute(sql).fetchall()
           ~~~~~~~~~~~~^^^^^
sqlite3.OperationalError: near "Brien": syntax error
```
Speaker notes: Look at the first line before the traceback. The injection string returned every row, and raised nothing. The quote closed the string early, and one equals one is true for every row. Then the real name crashed, because its apostrophe closed the string after Sam O. The crash is the kind bug. You will find it. The injection is the unkind one. It worked, silently. One fix handles both.
Image: None. This slide is code.
---
## Slide 4: The SQL text is fixed
- The question mark is a slot, not formatting
- Values travel separately, as a tuple
- The database reads the SQL before the values
- Nothing in a value can become SQL
- One value still needs a comma: (typed,)
Speaker notes: This is today's idea. The SQL text never changes. The values go to the database separately, and the driver fills each question mark safely. Because the database has already read the SQL, a quote inside a value is only a character. Watch the comma on a single value. Without it, Python sees a string, not a tuple.
Image: Two separate envelopes labeled SQL and values traveling to a database cylinder, launch blue.
---
## Slide 5: The same search, with parameters
```python
def add_technician(conn, badge, display_name):
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
```
Speaker notes: Two functions. The insert has two question marks and a tuple of two values. RETURNING id hands back the new row's key from the same statement, and it works the same in SQLite and PostgreSQL. The search has one question mark and a one-item tuple. The row factory from the demo lets us write row bracket id.
Image: None. This slide is code.
---
## Slide 6: Only data
```
new id: 3
"Sam O'Brien": [('T-1070', "Sam O'Brien")]
"x' OR '1'='1": []
```
Speaker notes: Sam is stored and found. The injection string matched nobody, because it was compared as a name, and nobody has that name. Same inputs as before, completely different results, and the only change was how the value traveled.
Image: None. This slide is code.
---
## Slide 7: Every query lives in db.py
- Values always travel as parameters
- Every function takes the connection first
- Write functions do not commit
- No other file imports sqlite3
- A test fails if one does
Speaker notes: Open the lab's db.py and read the three rules in its docstring. The routes call functions like create_issue and never see SQL. Why so strict? Next week the app moves to PostgreSQL, and with every query in one file, that move touches one file. Look at add_note. It looks up ids by badge inside the insert. That is your pattern for create_issue today.
Image: A single file icon labeled db.py with arrows from several route boxes pointing into it.
---
## Slide 8: A table name is not a value
```python
conn.execute("SELECT COUNT(*) FROM ?", ("tools",))
# sqlite3.OperationalError: near "?": syntax error

KNOWN_TABLES = {"tools", "checkouts"}

def count_rows(conn, table):
    if table not in KNOWN_TABLES:
        raise ValueError(f"unexpected table {table!r}")
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
```
Speaker notes: A question mark carries a value, never a name. The database must know which table it is reading before it takes any values, so this is a syntax error. When a name has to vary, check it against a list you wrote. That is an allow-list. The lab's table_counts does exactly this, and it is the only place its db.py builds SQL text. Sorting by a column the user picks gets the same answer.
Image: None. This slide is code.
---
## Slide 9: What you are about to build
- Lab U05-01, Part 2: steps 10 through 17
- Write get_issue and create_issue
- Write list_issues with its four filters
- A search for 100% finds only that issue
- Target: 50 of 56 self-checks pass
Speaker notes: Part 2 is the read and create half of CRUD. get_issue returns one issue or None. create_issue follows the add_note pattern and ends with RETURNING id, and it does not commit. list_issues takes four optional filters, and every one of them travels as a parameter. Watch the percent sign in search. It has to be searched as a plain character. In Build 2 you write your tool crib's db.py, seed script, and manage.py init.
Image: A search results page showing one matching issue, navy header, launch blue highlight on the match.
