# Gate 2: Adversarial Review · Week 2
## 145065 Object-Oriented Programming · Unit 1 · Week 2, Friday

**35 minutes.** Individual and silent. You may and should run the code, and write small scripts that
use it. You may not ask an AI tool whether it is correct, because an AI tool is what is being reviewed.

The program is `gate2-w02-files/work_orders.py`. Copy it into a scratch folder and run it.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every order,
badge, and machine here is invented.

---

## What you are looking at

The Line 3 maintenance team handed an AI assistant the spec in Part A and got `work_orders.py`. It
runs. It is formatted well, its docstrings sound sure of themselves, and its sample output is right.

**This course's Gate 2 is different from last semester's.** The defects this week are **design**
defects. Nothing is misspelled and nothing crashes on the sample run. The problems are in where data
lives, who is allowed to change it, and what the classes promise.

**Five defects, one in each dimension of the code review you know:**

| Dimension | What to look for this week |
|---|---|
| **Correctness** | The classes do not keep a promise the spec makes, in a case the sample run never tries |
| **Security** | A rule the spec calls for can be skipped without calling the method that enforces it |
| **Readability** | Behavior that lives somewhere a reader will not look for it |
| **Performance** | Work that grows much faster than the number of orders |
| **Requirements Fit** | Something the spec did not ask for, or asked against |

**One defect does not show up until you use the classes a second way.** The sample run uses one
board.

**One defect is arguable.** Reasonable programmers disagree about it. If you report it, say which
side you take and why, using the question from Wednesday: what data does this need?

---

## PART A: The spec

> Write `work_orders.py` for the Line 3 maintenance team.
>
> 1. `WorkOrder(order_id, asset_tag, description, priority)`. Order ids look like `WO-1001`: `WO-`
>    and four digits. Priority is 1 (urgent), 2 (soon), or 3 (routine). The description is not blank.
>    Refuse anything else.
> 2. A work order is closed only through `close(badge, note)`, which requires a non-blank badge and a
>    non-blank note and records both, because the supervisor audits who closed what and why. **A
>    closed work order is never reopened.** If the fix did not hold, the team writes a new order.
> 3. `WorkOrderBoard(name)` holds one shift's work orders. `add(order)` refuses an order id that is
>    already on the board. `find(order_id)` returns the order, or `None`.
> 4. `open_orders()` returns the open orders, most urgent first.
> 5. Each shift has its own board. **Two boards never share orders.**
> 6. `summary()` returns one line: `<name>: N open (U urgent), M closed`.
> 7. A board holds several thousand orders over a year and must stay quick.

---

## PART B: What the AI produced

```
python work_orders.py
```

A real run:

```
Day shift: 2 open (1 urgent), 1 closed
  WO-1001 [urgent] L3-PRS-02: Vibration above 7 mm/s
  WO-1003 [soon] L3-OVN-01: Door seal worn
```

Read that output against the seven requirements. It is correct. That is the problem with design
defects: the output you are shown is the one case that works.

---

## What to submit

For each defect: **the line number**, **the dimension**, **what goes wrong for a real technician,
supervisor, or shift**, and **the fix**, in a sentence or a few lines of code. Then one last entry:
**what I was unsure about**, naming something specific. That entry is scored, and a blank costs
more than a wrong guess.

Show your evidence. A finding with a command or three lines of code that proves it is worth more
than a finding you only suspect.

### How to spend 35 minutes

- **First 5:** run it. Read the seven requirements and point at the line that meets each one.
- **Next 10:** use the classes the way the whole shop would, not the way the sample run does. Every
  shift, every day.
- **Next 10:** for each rule in the spec, try to break it without calling the method that enforces
  it. Then read every method the spec did not ask for.
- **Last 10:** requirement 7. Then read every function and method and ask where a reader would look
  for it.

---

## Scoring

Five defects, one point each, plus one point for the "unsure about" entry. Your instructor states the
security weighting before you start.

**Four of five is a strong score.**
