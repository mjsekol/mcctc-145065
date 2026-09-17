# Gate 2: Adversarial Review · Week 9
## 145065 Object-Oriented Programming · Unit 5 · Week 9, Friday

**Gate 2 is the gate where AI is the opponent.** You did not write this code. You are reviewing it, and
you are scored on what you catch against what you miss.

**35 minutes.** Individual and silent. You may and should run the app and read every file. You may send
requests to your own copy on 127.0.0.1 and to nothing else. You may not ask a model whether the code is
correct, because a model is what is being reviewed.

**This is a generated Flask app with a SQLite database behind it. It has one SQL injection, and four
other defects.** You review it with the Five-Dimension Code Review, one planted defect per dimension:

| Dimension | The question to ask |
|---|---|
| **Correctness** | Does every number and every row match what the spec says, on every input? |
| **Security** | Could a stranger change what a query does, or read rows they should not? |
| **Readability** | Would the next person be misled by a name or a comment? |
| **Performance** | Does it do unnecessary or repeated work, such as a query that runs once per row? |
| **Requirements Fit** | Did it build what the spec asked for, no more and no less? |

**Exactly five defects, one per dimension. At least one is subtle. One is arguable: defend either side
with a sound reason.** The code runs, every page loads, and a quick click-through looks fine. That is the
point. The dangerous design is the one that works today.

**Everything is invented.** Riverside Fabrication is a composite shop. Every part, entry, and reason is
invented.

The code is in `gate2-w09-files/`. The app builds a fresh database in your temporary folder every time it
starts, so you can delete entries and search for anything without breaking a shared copy. From inside the
folder:

```
python scrap_app.py --port 8680
```

Open `http://127.0.0.1:8680/`. Read `scrap_app.py`, `schema.sql`, `seed.sql`, and every file in
`templates/`. Restart the app to get the starting data back.

**Where students lose points.** They read the routes and skip the SQL. They click every page once and
call it done. They find the injection by reading and never prove it. Every one of those costs you.

---

## PART A: The requirements spec the code was built from

> Build a **Line 3 Scrap Review** app in Flask on SQLite. The plant keeps one scrap table for Lines 3 and
> 4. This app is Line 3's view of it.
>
> 1. `GET /` shows every **Line 3** scrap entry, newest first, with the part's number and name, the
>    shift, the pieces, and the reason. **Line 4 entries never appear anywhere in this app.**
> 2. `GET /?q=text` shows only the Line 3 entries whose reason contains that text, ignoring case.
>    Whatever a person types, including an apostrophe, is searched for as text.
> 3. `GET /entries/<id>` shows one Line 3 entry. A missing entry, or a Line 4 entry, is a 404.
> 4. **Deleting asks first.** `GET /entries/<id>/delete` shows an "are you sure?" page with the entry on
>    it. Only a `POST` that carries the CSRF token deletes, and then it redirects to `/`.
> 5. `GET /report` lists **every part**, including parts with no Line 3 scrap, with the pieces scrapped,
>    the rework minutes, and the **rework hours to two decimal places**.
> 6. Every value travels to the database as a `?` parameter. Every connection turns foreign keys on.

---

## What to hand in

For each defect: its **dimension**, the **file and line**, **what is wrong**, **what a person on Line 3
would experience**, and the **fix**. Then one line naming the defect you were least sure about and why.

The injection is real. Prove it on your own copy: write the exact text you typed into the search box and
what the page showed. A finding you describe but did not prove earns less than one you proved.

You may instrument your copy: add a print, count calls, or open the database file with Python's
`sqlite3`. Write your findings before you change any code.

---

## PART B: The code

In `gate2-w09-files/`. Start with `scrap_app.py`, then `schema.sql`, `seed.sql`, and the templates. No
defect is marked.

---

## Scoring · 5 points, double penalty on the security miss

| Found | Points |
|---|---|
| Each defect correctly located and explained | 1 |
| The arguable defect: full point for either side with a sound reason | 1 |
| **Missing the security defect** | **minus 1 on top of the 0 for that defect** |

Five points possible. The security defect is the SQL injection. Missing it is the worst outcome, because
it hands a stranger every row in the table, so it costs its point and one more. Prove it with a search,
do not only describe it.
