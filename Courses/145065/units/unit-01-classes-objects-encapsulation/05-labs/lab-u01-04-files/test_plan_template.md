# Test Plan · Machine and WorkCell

Lab U01-04, Part 2. Copy this file as `test_plan.md` and fill it in **before** you write any test
code. A test you did not plan is usually a test of what the code already does, not of what it
should do.

Read `line3/machine.py` and `line3/cell.py`. Every rule a docstring or comment states is a test
case waiting to be written. Riverside Fabrication is a composite shop.

## Machine

| # | Setup | Action | Expected | Why this matters on the shop floor |
|---|---|---|---|---|
| M1 | a new press | read `is_running` and `temperature_c` | `False` and `None` | a reloaded machine must never look like it is running or reading 0 |
| M2 | | | | |
| M3 | | | | |
| M4 | | | | |
| M5 | | | | |
| M6 | | | | |

Include at least: one refusal at construction, one refused property assignment, one lockout rule,
and one reading the sensor could never produce.

## WorkCell

| # | Setup | Action | Expected | Why this matters on the shop floor |
|---|---|---|---|---|
| C1 | | | | |
| C2 | | | | |
| C3 | | | | |
| C4 | | | | |
| C5 | | | | |

Include at least: a duplicate, a machine that must not be removed, and what a caller can and cannot
do with `cell.machines`.

## The collection the cell keeps

Answer after step 14.

1. What does `WorkCell` keep its machines in, and what question does that collection answer fastest?
2. What did `collection_timer.py` print on your machine?
3. Which of your tests would fail if someone swapped the collection for a list and forgot the
   duplicate check?

## After mutant_check.py

Which mutants did your first run miss, and what test did you add for each?
