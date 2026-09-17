# Gate 2: Adversarial Review · Week 10
## 145065 Object-Oriented Programming · Unit 5 · Week 10, Friday

**Gate 2 is the gate where AI is the opponent.** You did not write this code. You are reviewing it, and
you are scored on what you catch against what you miss.

**35 minutes.** Individual and silent. You may and should run the app and read every file. You may send
requests to your own copy on 127.0.0.1 and to nothing else. You may not ask a model whether the code is
correct, because a model is what is being reviewed.

**This is a generated Flask app that is meant to be deployed. It has one security flaw in how it is
configured, and four other defects.** This week the security defect is not an injection. It is the kind of
mistake that passes every test on your laptop and only bites once the app is live. You review it with the
Five-Dimension Code Review, one planted defect per dimension:

| Dimension | The question to ask |
|---|---|
| **Correctness** | Does every number on the report match the rows it came from? |
| **Security** | Would this be safe once it is on the public internet, not only on your laptop? |
| **Readability** | Would the next person be misled by a name or a comment? |
| **Performance** | Does it repeat work on every request that it could do once? |
| **Requirements Fit** | Did it build what the deployment spec asked for, no more and no less? |

**Exactly five defects, one per dimension. At least one is subtle. One is arguable: defend either side
with a sound reason.** The code runs, every page loads, `/health` says the app is healthy, and a
click-through looks finished. The dangerous design is the one that works today.

**Everything is invented.** Riverside Fabrication is a composite shop. Every machine, event, and rate is
invented.

The code is in `gate2-w10-files/`. It reads its settings from the environment, the way a deployed app
does, and rebuilds a fresh database in your temporary folder each time it starts. Start it the way you
would start it in production, from inside the folder, in PowerShell:

```
$env:APP_ENV = "production"
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
python downtime_app.py --port 8680
```

Open `http://127.0.0.1:8680/`. Read `downtime_app.py`, `schema.sql`, `seed.sql`, `rates.json`, and every
file in `templates/`.

**Where students lose points.** They test the app the way the author did, with everything set up
correctly, and never ask what happens when a setting is missing. They read the report and never check one
number against the seed data. They read a function's name and trust it.

---

## PART A: The requirements spec the code was built from

> Grow the **Line 3 Downtime Log** into an app you can deploy. It reads downtime events from SQLite and
> shows a cost report.
>
> 1. `GET /` shows every **Line 3** downtime event, newest first, with the machine, the reason, the
>    minutes, and whether it is resolved.
> 2. `GET /events/<id>` shows one Line 3 event and its estimated cost. A missing event is a 404.
> 3. `GET /report` lists **every machine** with its **number of downtime events**, its total downtime
>    minutes, and the estimated cost. A machine with no downtime shows **0 events**.
> 4. All settings come from the environment. **In production the app must refuse to start without a
>    `SECRET_KEY` of at least 32 characters.** A secret is never written as a value in any file.
> 5. `GET /health` returns 200 only when the app can read its real data. If the database has no tables,
>    which is what a fresh deploy looks like before it is set up, `/health` must report unhealthy with a
>    503. The host reads `/health` to decide whether the app is ready.
> 6. Debug mode is off in every environment.

---

## What to hand in

For each defect: its **dimension**, the **file and line**, **what is wrong**, **what a person on Line 3,
or the person deploying, would experience**, and the **fix**. Then one line naming the defect you were
least sure about and why.

The security defect is real, and you can prove it without attacking anyone. Run the app the way a careless
deploy would, with a setting missing, and write down what it did instead of refusing.

You may instrument your copy: add a print, count how often a file is read, or point the app at an empty
database file. Write your findings before you change any code.

---

## PART B: The code

In `gate2-w10-files/`. Start with `downtime_app.py`, then the SQL, `rates.json`, and the templates. No
defect is marked.

---

## Scoring · 5 points, double penalty on the security miss

| Found | Points |
|---|---|
| Each defect correctly located and explained | 1 |
| The arguable defect: full point for either side with a sound reason | 1 |
| **Missing the security defect** | **minus 1 on top of the 0 for that defect** |

Five points possible. The security defect is the configuration flaw. Missing it is the worst outcome,
because it is the mistake that only shows up once the app is public, so it costs its point and one more.
Prove it by running the app with the setting missing, and write what happened.
