# Lab U0-02: Sensor to Spreadsheet
## 145065 Object-Oriented Programming · Unit 0 · Week 1

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Wednesday Build 1 and Build 2.
**Competencies:** 2.4.2 (architectures of emerging technologies and how they integrate into existing
IT systems), 2.4.4 (describe IoT), 5.1.1 (programs that solve problems), 5.5.7 (read inputs),
5.5.6 (format output for data files), 5.3.5 (conditional control structures), 5.2.3 (arithmetic
operations).

Files: `lab-u00-02-files/line3_pipeline.py` (starter), `lab-u00-02-files/selfcheck_pipeline.py`,
and `lab-u00-02-files/maintenance_log_original.csv`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop used all semester.
Every reading, name, and time in this lab is invented. No hardware is used. The device layer is
simulated.

---

## The scenario

Line 3's supervisor has kept a maintenance log for years, first on paper and now in a spreadsheet,
with temperatures in Fahrenheit. The shop added sensors to the paint cure oven, Press 2, and the
coolant tank, and a Raspberry Pi now sends their readings across the shop network every five seconds.
Nobody has connected those readings to the log the supervisor actually reads, so right now the
sensors change nothing.

## What you will build

The integration layer: the code that turns each sensor message into rows the existing log already
understands, including a row that says plainly when a sensor did not answer.

---

## The architecture you are working in

```
DEVICE  ->  GATEWAY  ->  TRANSPORT  ->  INTEGRATION  ->  EXISTING SYSTEM
reads       packages      carries        YOU WRITE        maintenance_log.csv
sensors     JSON text     the text       THIS LAYER       the supervisor's spreadsheet
```

The device, gateway, and transport layers are written and working. The gateway sends the same JSON
shape the Line 3 sensor service uses all semester:

```json
{
  "device": "line3-pi",
  "sequence": 1043,
  "sampled_at": "2027-01-11T14:03:27Z",
  "sensors": [
    {"id": "oven-temp", "kind": "temperature", "value": 221.5, "unit": "C", "ok": true},
    {"id": "press-vibration", "kind": "vibration", "value": 7.4, "unit": "mm/s", "ok": true},
    {"id": "coolant-level", "kind": "level", "value": null, "unit": "%", "ok": false}
  ]
}
```

The existing log has six columns and looks like this:

```
logged_at,equipment,measurement,value,unit,status
2027-01-11 06:10:00,Paint cure oven,temperature,405.0,F,OK
```

**Every difference between those two shapes is your job.**

---

## Starter code

Copy the three files into a folder in your `oop-semester` repository, then make a working copy of the
log:

```
copy maintenance_log_original.csv maintenance_log.csv
python line3_pipeline.py
```

On macOS or Linux, use `cp` instead of `copy`.

The starter runs. Its last lines are:

```
Wrote 0 rows to maintenance_log.csv
```

Read the starter before you write anything. `to_log_rows` returns an empty list, and
`celsius_to_fahrenheit` hands back the Celsius value unchanged. **The second one is a trap, and step
11 is about it.**

---

## Part 1: Build 1, steps 1 through 6

### Step 1. Run the starter and the self-check

```
python line3_pipeline.py
python selfcheck_pipeline.py
```

**Observable result:** three lines that each end `INTEGRATION 0 rows`, then the last payload printed
as indented JSON. The self-check ends `0 of 4 self-checks passed`. Commit the files.

### Step 2. Fill in the architecture table

Copy this table into your lab README and fill every cell from the running program and the code, not
from memory.

| Layer | Function | Input | Output | On the real line, runs on |
|---|---|---|---|---|
| Device | | | | |
| Gateway | | | | |
| Transport | | | | |
| Integration | | | | |
| Existing system | | | | |

**Observable result:** five complete rows. The Gateway output cell names the JSON keys.

### Step 3. Parse at the boundary

In `to_log_rows`, turn `json_text` into a Python dictionary with `json.loads`. Everything after that
line works with data, not text.

**Observable result:** the program still runs and still writes 0 rows.

### Step 4. Build `logged_at` and one row per sensor

The log's time has no `T` and no `Z`: `2027-01-11T14:03:17Z` becomes `2027-01-11 14:03:17`. Loop over
the sensors and append one row per sensor, in `LOG_COLUMNS` order. Use `EQUIPMENT_NAMES` for the
equipment column and the sensor's `kind` for the measurement column. For now, put the sensor's value
and unit straight in, with status `OK`.

**Observable result:** each tick line now ends `INTEGRATION 3 rows`.

### Step 5. Check sequence 1041 against the log format

Run the self-check.

**Observable result:** sequence 1041 fails **only** on the oven's value, which reads `208.9`, and the
unit, which reads `C`. Every other column matches. If anything else fails, fix it before you go on.

### Step 6. Commit

**Observable result:** a commit whose message says the integration layer now produces rows.

---

## Part 2: Build 2, steps 7 through 12

### Step 7. Convert to the log's unit

Write `celsius_to_fahrenheit`: multiply by 9, divide by 5, add 32. In `to_log_rows`, when a sensor's
unit is `C`, convert the value, round it to one decimal place, and write the unit as `F`.

**Observable result:** the self-check's first line passes, and sequences 1041 and 1042 pass. The oven
at sequence 1041 reads `408.0`.

### Step 8. Mark readings over the limit

`CHECK_ABOVE` holds the shop's limits, **in the log's units**. When a value is above its kind's limit,
the status is `CHECK`. The level has no limit.

Compare **after** converting. A limit written in Fahrenheit means nothing to a Celsius number.

**Observable result:** at sequence 1043 the oven row reads `430.7`, `F`, `CHECK`, and Press 2 reads
`CHECK`.

### Step 9. Say plainly when a sensor did not answer

When a sensor has `ok` set to `false`, its row gets a **blank** value (`""`), its own unit, and status
`NO READING`. Never write `0`. In a level column, `0` means an empty tank, and the sensor never said
that.

**Observable result:** `python selfcheck_pipeline.py` prints `4 of 4 self-checks passed`.

### Step 10. Run the whole pipeline and open the log

Reset the log, run, then open `maintenance_log.csv` in a spreadsheet program.

**Observable result:** `Wrote 9 rows to maintenance_log.csv`. The spreadsheet shows the 3 original
rows and 9 new ones in the same six columns, with one `CHECK` oven row, one `CHECK` press row, and one
`NO READING` row with an empty value cell.

### Step 11. Break it on purpose, and write down what happened

Change `celsius_to_fahrenheit` back to `return celsius`. Reset the log and run the pipeline.

**Observable result:** no error at all. The program writes 9 rows. The oven's last row reads:

```
2027-01-11 14:03:27,Paint cure oven,temperature,221.5,F,OK
```

Copy that row into your README under a heading `## The bug that does not crash`, and write two
sentences: what the supervisor would believe, and what was true. Then restore the conversion and
confirm 4 of 4 again.

### Step 12. Reset, commit, and push

Reset `maintenance_log.csv` from the original, run once, and commit the code, the README, and the
log.

**Observable result:** the committed log has 12 data rows. `git status` shows nothing uncommitted.

### Acceptance criteria, full lab

- [ ] `python selfcheck_pipeline.py` prints `4 of 4 self-checks passed`
- [ ] The architecture table has five complete rows
- [ ] Values are converted before they are compared with a limit
- [ ] A sensor that did not answer produces a blank value and `NO READING`, never `0`
- [ ] The committed log has exactly 12 data rows, in six columns
- [ ] Your README records the step 11 row and your two sentences
- [ ] You did not change the device, gateway, or transport layers
- [ ] Committed and pushed

---

## If it breaks

### 1. You passed data where the function expects text

```
TypeError: the JSON object must be str, bytes or bytearray, not dict
```

**Cause:** `json.loads` was given a dictionary. `to_log_rows` receives **text**, because only text
crosses the network. Call `json.loads` once, on `json_text`.

### 2. A key the payload does not have

```
KeyError: 'value'
```

**Cause:** the key name in your code does not match the payload, or you looked it up on the wrong
dictionary, such as the whole payload instead of one sensor. Print the dictionary you are indexing.

### 3. Comparing a missing value with a limit

```
TypeError: '>' not supported between instances of 'NoneType' and 'float'
```

**Cause:** a sensor with `ok` false has `value` of `None`, and you compared it before checking `ok`.
Handle the missing sensor first, then skip to the next one.

### 4. Long decimals in the log

A value such as `408.02000000000004` in your log. Not an error, and not what the log expects.

**Cause:** floating-point arithmetic. `208.9 * 9 / 5 + 32` really is `408.02000000000004` in Python.
Round to one decimal place after converting.

### Not an error, and the one that matters most: the missing sensor marked OK

If you skip step 9, the coolant row comes out as `Coolant tank,level,,%,OK`. The `csv` module writes
`None` as an empty cell, so the value looks blank, and the status still says `OK`. The supervisor sees
a tank that is fine. The sensor said it did not know.

### Running the pipeline twice

Each run appends 9 more rows, so a second run leaves duplicates. That is how the starter's
`append_rows` works. Reset the log from the original before each run. The EXTENDED option fixes it
properly.

---

## Stretch goal

Add a fourth kind of reading to the simulation: `press-temp`, a temperature on Press 2 in Celsius. You
may change `TICKS`, `SENSORS`, and `EQUIPMENT_NAMES` for this. What else had to change, and what did
not? Write the answer in your README. The answer tells you how well the integration layer was
designed.

---

## Submission checklist

- [ ] Self-check 4 of 4
- [ ] Architecture table complete
- [ ] Step 11 recorded in the README
- [ ] Log reset and 12 data rows committed
- [ ] Your brief's technology choice and the rejected one are in `decision-log.md`
- [ ] Pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Step 4 not reached at the end of Build 1, or the student is editing the gateway to make rows appear | SCAFFOLDED |
| Steady progress, questions about the log format | STANDARD |
| 4 of 4 before Build 2 is half over | EXTENDED |
| The student says they will never work in a factory | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the student receives `to_log_rows` with the loop, `logged_at`, and the equipment
  and measurement columns already written. They write the conversion, the limit check, and the
  missing-sensor branch.
- **Steps:** skip step 2's "On the real line" column.
- **Checkpoints:** show the self-check to the instructor after step 7 and after step 9.
- **Keep step 11.** The silent bug is the lesson.

**Acceptance criteria:** 4 of 4 self-checks, the step 11 row and sentences in the README, 12 data
rows committed.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a real integration problem the lab has not taught.

**Added requirement.** Running the pipeline twice must not add duplicate rows. The existing log has no
ID column. Decide what identifies a row, and have `append_rows` skip any row already in the file. The
starter's behavior for a brand-new log file, which is to write the header first, must still work.

**Hint, not the answer.** You need to read the existing CSV before you append to it. The `csv`
module can read each row as a dictionary keyed by the header line. Read the section on the reader
class that returns dictionaries in `https://docs.python.org/3/library/csv.html`. A `set` of the
values that identify a row makes the "already there?" question fast.

**Acceptance criteria:** all STANDARD criteria; a second run reports `Wrote 0 rows`; deleting the log
and running once writes a header and 9 rows; a decision log entry says what identifies a row and
names the option you rejected.

**Grading:** same scale.

---

## APPLIED

**For the student who will never work in a factory.** The same integration problem, somewhere else.

**Changed scenario.** A gym's new smart treadmills send workout records as JSON: a timestamp in the
same `T` and `Z` format, a machine ID, distance in **kilometers**, and an `ok` flag. The front desk
has kept a member-free usage log in a spreadsheet for years, in **miles**, with columns
`logged_at,machine,distance,unit,status`. Invent at least three moments of data yourself, with no
names or member information, including one machine that did not report.

**What you build.** The same layers, with your own device and gateway, and an integration layer that
converts kilometers to miles (1 kilometer is 0.621371 miles), flags any single workout above a limit
you choose and justify in the README, and writes `NO READING` for the silent machine. Write a
self-check with the expected rows for each of your moments.

**Acceptance criteria:** your self-check passes; the silent machine gets a blank and `NO READING`; the
README has the architecture table and the "bug that does not crash" section for your domain.

**Grading:** same scale. Requirements Fit is judged on whether the student's conversion and limit
choices are defensible.
