# Gate 2: Adversarial Review · Week 4
## 145065 Object-Oriented Programming · Unit 2 · Week 4, Friday

**35 minutes.** Individual and silent. You may and should run the code, and write your own small
tests. You may not ask an AI tool whether the code is correct, because AI-written code is what is
being reviewed.

The program is `gate2-w04-files/weld_cell.py`. Copy it into a folder of your own and run it.

**Riverside Fabrication is a composite**, an invented shop. Every tag and badge id is invented.

---

## What you are looking at

A developer handed an AI assistant the requirements in Part A and got the program in
`weld_cell.py`. It runs with no errors. It uses `abc`, type hints, and docstrings, and it looks like
the Week 4 lecture notes.

**In this course, Gate 2 plants design defects, not typos.** Every defect below is a decision. The
code compiles, runs, and passes a quick look.

**Five defects, one in each dimension:**

| Dimension | What to look for this week |
|---|---|
| **Correctness** | An override that breaks what its parent promised |
| **Security** | A safety rule the model is supposed to enforce and does not |
| **Readability** | A class that knows too much about other classes, or a comment the code contradicts |
| **Performance** | Work repeated inside a loop that only needs doing once |
| **Requirements Fit** | Something the requirements asked for that the design cannot deliver |

**One of the five is genuinely arguable.** Reasonable people could defend it. If you think a finding
is arguable, say so, and argue both sides. That earns its own point.

**One of the five does not show up in the sample run at all.** You have to call methods the sample
run never calls, in an order it never uses.

---

## Part A: The requirements

> Riverside is adding a weld cell to Line 3. Write `weld_cell.py`.
>
> 1. An abstract base `Asset`, using `abc`. Every asset has an asset tag matching `L3-ABC-00` and a
>    name. Creating a bare `Asset` must fail.
> 2. `PoweredAsset(Asset)` can `start()`, `stop()`, `lock_out(badge)`, and `release_lockout(badge)`.
>    Locking out stops the asset. A locked-out asset refuses to start. **Only the badge that applied a
>    lockout may release it.**
> 3. `Welder(PoweredAsset)` has an arc that is on only while the welder runs. `stop()` turns the arc
>    off.
> 4. `FumeExtractor(PoweredAsset)` has an airflow in cubic meters per hour.
> 5. `WeldCart(Asset)` carries filler wire and gas bottles. **A cart has no power. Code must not be
>    able to start a cart.**
> 6. `WeldCell` holds assets and smaller cells, to any depth. `count_assets()` counts every asset at
>    every depth. `find(tag)` finds an asset at any depth. `start_all(tags)` starts the listed assets
>    and returns the tags it started. The cell will grow to hundreds of assets.
> 7. `describe()` on every asset returns one line: tag, name, and kind, plus each kind's own details,
>    and for powered assets whether they are running.

---

## Part B: What the AI produced

The code is in `gate2-w04-files/weld_cell.py`. Run it:

```
python weld_cell.py
```

A real run:

```
Started: L3-FEX-01, L3-WLD-01, L3-CRT-01
Assets in cell: 3
L3-WLD-01 MIG Welder A (welder), arc on, running
L3-FEX-01 Extractor A (extractor), 1200 m3/h, running
L3-CRT-01 Wire Cart (cart)
```

**Read that output against the seven requirements before you read the code.** One requirement is
already visibly unmet.

---

## What to submit

For each defect, write:

1. **File and line**, or the method name
2. **Dimension**
3. **What goes wrong**, for a real person on Line 3
4. **How you proved it**: the command or test you ran, and what it printed
5. **The fix**, in a sentence or a few lines of code

Then two more entries:

- **The arguable one:** which finding it is, the strongest case that it is a defect, and the
  strongest case that it is acceptable.
- **What I was unsure about:** something specific. This entry is scored, and a blank costs more than
  a wrong guess.

### How to spend 35 minutes

- **First 5:** run it. Check the output against all seven requirements.
- **Next 10:** call what the sample run never calls. Lock something out. Release it with a
  different badge. Lock out a running welder and look at every attribute.
- **Next 10:** read each class for one question: does this class know about classes it should not?
  Read each comment against the code under it.
- **Last 10:** think about requirement 6's last sentence. Count how often the code walks the whole
  cell. Write up.

---

## Scoring

Five defects, one point each, plus one point for the arguable entry argued both ways, plus one point
for the unsure-about entry. A finding scores only with a location, a consequence, and a fix. Your
instructor states the Security weighting before you start.

**Four of five is a strong score.**
