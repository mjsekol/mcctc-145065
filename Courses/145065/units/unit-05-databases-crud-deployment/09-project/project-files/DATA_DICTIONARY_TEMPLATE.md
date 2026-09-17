# Data dictionary · toolcrib-web

> **Note, delete before you submit.**
>
> DATA_DICTIONARY_TEMPLATE.md · Unit 5 project, Tool Crib Live (requirement N1)
>
> Copy this file into your toolcrib-web folder as DATA_DICTIONARY.md and fill in every part.
> Delete every note like this one when you are done.
>
> Why this file exists: schema.sql tells the database what to enforce. This file tells a person what
> each column means, where its value comes from, and which rule protects it. Your outside tester, your
> instructor, and the next person to change the app read this page, not your SQL.
>
> The Documentation dimension checks one thing hard: this file matches schema.sql column for column.
> Same tables, same columns, same order, same types. When you change schema.sql, change this file in
> the same commit. A good habit: write a test that builds the database, reads each table's columns
> with PRAGMA table_info, and compares them with the column names in this file.
>
> The most common ways this file goes wrong:
>   * a column added to schema.sql late in Week 10 and never added here
>   * a rule written here that the database does not enforce, with nothing saying the app enforces it
>   * a calculated field with no formula, or a formula that is not the one the code uses
>   * an example value that breaks the column's own rule
>   * a real person's name used as an example. Use your invented seed data.

Riverside Fabrication is a composite: an invented shop with invented tools, badges, and records.

It describes `schema.sql`. [If you have `schema_postgres.sql`, say what differs.] The picture is
`ER_DIAGRAM.___`.

## 1. The tables

Key: **PK** primary key, **FK** foreign key, **UQ** unique. In the Rule column, write "app:" before
a rule that only `validation.py` checks. Everything else, the database enforces.

> **Note, delete before you submit.**
>
> One section per table, in the order schema.sql creates them. One row per column, in schema.sql's
> order. Empty? is "no" for NOT NULL and for a primary key, otherwise "yes". Meaning says what the
> value is for a person, not what type it is. Example is a real value from your seed data.

### technicians

[One sentence on why this table holds nothing personal.]

| Column | Type | Empty? | Key | Rule | Meaning | Example |
|---|---|---|---|---|---|---|
| `id` | INTEGER | no | PK | assigned by the database | | |
| `badge` | | | | | | |
| | | | | | | |

### categories

| Column | Type | Empty? | Key | Rule | Meaning | Example |
|---|---|---|---|---|---|---|
| `id` | INTEGER | no | PK | assigned by the database | | |
| | | | | | | |

### tools

| Column | Type | Empty? | Key | Rule | Meaning | Example |
|---|---|---|---|---|---|---|
| `id` | INTEGER | no | PK | assigned by the database | | |
| | | | FK to `categories.id` | must exist | | |
| | | | | | | |

### checkouts

| Column | Type | Empty? | Key | Rule | Meaning | Example |
|---|---|---|---|---|---|---|
| `id` | INTEGER | no | PK | assigned by the database | | |
| | | | FK to `tools.id` | must exist | | |
| | | | FK to `technicians.id` | must exist | | |
| | | | | | | |

### The rules that span columns or rows

> **Note, delete before you submit.**
>
> Paste each CHECK that uses two columns, and any index that enforces a rule, as it is in schema.sql.
> Then one sentence each on what it stops.
>
> "No tool checked out twice at once" goes here. Say how your database enforces it. If you enforce it
> in db.py instead, inside the transaction, say that, and say what happens when two requests arrive at
> the same moment.

```sql

```

## 2. Relationships in words

> **Note, delete before you submit.**
>
> One line per foreign key: the parent, the child, the cardinality, and the column.

```
categories  1 ──< tools        one category holds zero or more tools          (tools.category_id)
___________ 1 ──< _________    ________________________________________       (________________)
___________ 1 ──< _________    ________________________________________       (________________)
```

[Two or three sentences: why the data is split into these tables, and what the database does when
someone tries to delete a row that another row points at.]

## 3. Calculated fields

> **Note, delete before you submit.**
>
> Every number on /reports that is not stored. The formula is the one your code uses: the SQL
> expression, or the Python line. "Watch for" names the mistake that would give a wrong number
> without an error. Think about tools never checked out, checkouts still out, and division by zero.

| Field | Formula | Watch for |
|---|---|---|
| times checked out | | |
| out now | | |
| returned late | | |
| late share of returns, % | | a tool with no returns |
| [your extra field, R2] | | |
| totals row | | |

**Rounding.** [Where the rounding happens, to how many places, and which way a value exactly halfway
goes. Check it with a real value from your data.]

**Worked from the starting data.** [The hand-calculated table your R5 test compares against. Show
the minutes or counts you started from.]

| Tool | Times out | Out now | Returned late | Late % | [Your field] |
|---|---|---|---|---|---|
| | | | | | |

## 4. The CSV import format

> **Note, delete before you submit.**
>
> Enough that purchasing could make a file that imports on the first try without reading your code.

The header row, exactly:

```

```

| Column | Rule | Example |
|---|---|---|
| | | |

[What happens when any row is wrong. How line numbers are counted. What `--dry-run` does. Which
encodings load, and what the byte order mark is.]
