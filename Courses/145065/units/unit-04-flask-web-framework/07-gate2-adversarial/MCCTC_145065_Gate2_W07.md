# Gate 2: Adversarial Review · Week 7
## 145065 Object-Oriented Programming · Unit 4 · Week 7, Friday

**Gate 2 is the gate where AI is the opponent.** You did not write this code. You are reviewing it, and
you are scored on what you catch against what you miss.

**35 minutes.** Individual and silent. You may and should run the app and read every file. You may not
ask a model whether the code is correct, because a model is what is being reviewed.

**You review code with the Five-Dimension Code Review**, one planted defect per dimension:

| Dimension | The question to ask |
|---|---|
| **Correctness** | Does it do what the spec says, on every input and boundary? |
| **Security** | Could a stranger read or break something they should not? |
| **Readability** | Would the next person understand it, or be misled by a name or a comment? |
| **Performance** | Does it do unnecessary or repeated work? |
| **Requirements Fit** | Did it build what the spec asked for, no more and no less? |

**There are exactly five defects, one per dimension. At least one is subtle, and you will probably
miss it. One is arguable: a reasonable reviewer could defend it, and you are scored on your reasoning,
not on which side you pick.** The code runs and looks finished. That is the point.

**Everything is invented.** Riverside Fabrication is a composite shop. Every note and machine is
invented.

The code is in `gate2-w07-files/`. Run it:

```
python board.py --port 8680
```

Open `http://127.0.0.1:8680/`. Read `board.py` and every file in `templates/`.

---

## PART A: The requirements spec the code was built from

> Build a **Line 3 Shift Handoff Board** in Flask. Technicians leave notes about machines for the next
> shift.
>
> 1. `GET /` shows every **open** note (a note that has not been cleared), **most urgent first**.
>    Severity is `info`, `watch`, or `urgent`.
> 2. `GET /notes/<id>` shows one note in full. A missing note is a 404.
> 3. `GET /machines` lists every machine with a count of its open notes.
> 4. `GET /machines/<code>` shows one machine and its notes. A missing machine is a 404.
> 5. **Every page uses the same layout** through template inheritance: the same header, navigation, and
>    footer. The footer says Riverside Fabrication is a composite.
> 6. The notes come from a JSON file, read through one class. If the file cannot be read, the page says
>    the board is unavailable **without showing any internal detail**, and the detail goes to the
>    server's log.

---

## What to hand in

For each defect you find: its **dimension**, the **file and line**, **what is wrong**, **what a real
person on Line 3 would experience**, and the **fix**. Then one line naming the defect you were least
sure about and why.

You may run the app, add a note to `data/notes.json`, break the file on purpose, and instrument the
code. Change nothing in `templates/` until you have written your findings.

---

## PART B: The code

In `gate2-w07-files/`. Start with `board.py`, then the templates. No defect is marked.

---

## Scoring · 5 points, double penalty on the security miss

| Found | Points |
|---|---|
| Each defect correctly located and explained | 1 |
| The arguable defect: full point for either side with a sound reason | 1 |
| **Missing the security defect** | **minus 1 on top of the 0 for that defect** |

Five points possible. Missing the security defect alone drops you to 3 of the other 4 at most, because
its consequence is the worst on a shop network. The subtle defect is not required for full marks if you
find the other four and reason well about the arguable one.
