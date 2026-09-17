# Lab U8-01: Bench Check
## 145065 Object-Oriented Programming · Unit 8 · Week 15

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 2, finishing Tuesday for
homework if needed.
**Competencies:** 2.10.2 (processor, memory, storage, power, and environmental requirements), 1.8.2
(select and organize resources), 5.5.7 (read inputs from a device), 5.6.5 (input and output
requirements), 5.5.1 (data validation).

Files: `lab-u08-01-files/bench_check.py` (starter) and `lab-u08-01-files/selfcheck_bench.py`, plus the
sensor service in `sensor-service/`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every reading here is
invented or simulated.

---

## Safety brief · read it aloud with your partner before anything else

- **ESD strap on**, clipped to the mat, before you touch the Pi, the probe, or a jumper wire.
- **Power the Pi off** before you connect or disconnect any wire on its pins.
- **No mains voltage, ever.** The Pi's power supply is the only thing that plugs into the wall.
- **Your signed Lab Acceptable Use and Safety Agreement is on file.** No agreement, no bench kit: you do
  this lab on the simulator only, and that earns full credit.
- **The software monitors. It never switches equipment on or off.** Nothing in this lab or this unit
  controls a machine.
- Wiring and powering the Pi happen **only with your instructor present**.

Parts 1 and 2 of this lab touch no hardware.

---

## The scenario

Line 3's new operator panel will trust whatever the Pi on the line tells it. Before anyone builds that
panel, the maintenance lead wants proof that the Pi's sensor service keeps its promise, and a list of
exactly what the Pi needs to run in a hot, dirty cell. If the service can freeze or send garbage without
anyone noticing, the panel will show an operator numbers that are not true.

## What you will build

A bench checker that asks a sensor service five questions and says PASS or FAIL for each, plus the
hardware requirements and parts list for your panel's bench.

---

## The contract you are checking

`GET /api/readings` returns:

```json
{
  "device": "line3-pi",
  "sequence": 1042,
  "sampled_at": "2027-01-11T14:03:22Z",
  "sensors": [
    {"id": "oven-temp", "kind": "temperature", "value": 212.4, "unit": "C", "ok": true},
    {"id": "press-vibration", "kind": "vibration", "value": 3.1, "unit": "mm/s", "ok": true},
    {"id": "coolant-level", "kind": "level", "value": 68.0, "unit": "%", "ok": true}
  ]
}
```

`sequence` goes up by one for each new sample. `sampled_at` is when the sample was taken, in UTC, ending
in `Z`. A sensor that failed reports `"value": null, "ok": false`. **`ok` true always has a number.
`ok` false always has `null`.**

---

## Starter code

`bench_check.py` runs, reaches the service, and prints the five checks. Checks 3 and 4 always fail,
because `contract_problems()` and `sequence_advanced()` are not written yet. Read the whole file first:
`fetch()`, `health_ok()`, and `every_sensor_reported()` are given, and they show the style to follow.

---

## Part 1: the checker

### Step 1. Read the safety brief, then copy the files

Copy `lab-u08-01-files/` and `sensor-service/` into your `hmi-panel` repository. Set
`PYTHONDONTWRITEBYTECODE=1` in your terminal, or delete `__pycache__` before every commit.

**Observable result:** both folders are in your repository and committed.

### Step 2. Start the simulator and read one reply

Check the port is free (no output means free), then start the service in one terminal:

```
netstat -ano | findstr :8700
python sensor_service.py --port 8700
```

In a second terminal, in `sensor-service/`:

```
python sim_control.py --port 8700 read
```

**Observable result:** `200` followed by one reply in the contract's shape. Your sequence number, time,
and values will differ from the example.

### Step 3. Run the starter checker

In a third terminal, in `lab-u08-01-files/`:

```
python bench_check.py --port 8700
```

**Observable result:** checks 1, 2, and 5 pass. Check 3 prints
`contract_problems() is not written yet`. The last line is `3 of 5 checks passed.`

### Step 4. Run the self-check

```
python selfcheck_bench.py
```

**Observable result:** `2 of 12 self-checks passed.` Two checks pass by accident: a function that always
answers `False` passes every test that expects `False`. Read the canned replies at the top of the file.

### Step 5. Parse at the boundary

In `contract_problems`, turn the text into data with `json.loads`. If that fails, return one problem
that says the reply is not valid JSON, and stop. If the result is not a dictionary, say so and stop.

**Observable result:** self-check 2 passes.

### Step 6. The four reply keys

Report each missing key. Then check that `device` is a non-empty string, `sequence` is a whole number of
zero or more, and `sampled_at` is a string ending in `Z`.

**The trap:** in Python, `True` is an `int`. `isinstance(True, int)` is `True`. Refuse a `bool` sequence
first.

**Observable result:** self-checks 3, 4, and 5 pass.

### Step 7. The sensors

Check that `sensors` is a list, and that each sensor is a dictionary with all five keys.

**Observable result:** nothing new passes yet. The next step needs this one.

### Step 8. `ok` and `value` agree, and no id repeats

For each sensor: `ok` is `true` or `false`; `ok` true with a `null` value is a problem; `ok` false with a
value is a problem; a value that is present is a number; no `id` appears twice. Name the sensor in every
problem.

**Observable result:** self-checks 1, 6, 7, and 8 pass. Check 1 passes because a failed sensor that says
so is **not** a contract problem.

### Step 9. `sequence_advanced`

Return `True` when the two replies carry different sequence numbers, `False` when they are the same, and
`False` when either reply is unreadable. Any change counts, including a smaller number: a Pi that
restarted counts from 1 again.

**Observable result:** `12 of 12 self-checks passed.` Then `python bench_check.py --port 8700` ends with
`5 of 5 checks passed.` Commit.

---

## Part 2: what each mode looks like, and what the Pi needs

### Step 10. Run the checker in every mode

In the control terminal, switch the mode, wait two seconds, then run the checker. Fill this table from
your runs, not from the mode descriptions.

```
python sim_control.py --port 8700 mode drift
```

| Mode | Check 1 | Check 2 | Check 3 | Check 4 | Check 5 | Checks passed |
|---|---|---|---|---|---|---|
| normal | | | | | | |
| drift | | | | | | |
| freeze | | | | | | |
| drop-sensor | | | | | | |
| silent | | | | | | |
| garbage | | | | | | |
| service stopped (Ctrl+C) | | | | | | |

Put the simulator back to `normal` when you are done.

**Observable result:** seven complete rows. Write one sentence under the table: **which mode passes all
five checks even though the panel must raise an alarm, and why is that correct for a contract check?**

### Step 11. Hardware requirements for the Pi side

Measure the service while it runs. On Windows, find its process number from `netstat -ano | findstr :8700`
(the last column), then:

```
tasklist /FI "PID eq <that number>"
```

Read the `Mem Usage` column. Use check 2's time from your runs for the response time.

Copy this table into `docs/HARDWARE.md` in your repository and fill every row. Write where each number
came from.

| Resource | What the sensor service needs | How you know |
|---|---|---|
| Processor | | |
| Memory | | |
| Storage | | |
| Software | | |
| Power | | |
| Environment (heat, coolant mist, metal chips) | | |
| Clock | | |
| Network | | |

For any row you could not measure here, write what must be confirmed on the lab Pi and mark it [VERIFY].

**Observable result:** eight rows, each with a source.

### Step 12. The parts and resources list

In the same file, list everything a bench needs: hardware, software, safety equipment, paperwork, and
time. Include a quantity and a note for each.

**Observable result:** at least ten rows, including the ESD strap and mat, the signed agreement, and the
time the build takes, by week.

### Step 13. On the lab Pi, with your instructor present [VERIFY every step on the hardware]

Only with a signed agreement on file, after reading the safety brief again.

1. **Power off.** Wire the DS18B20 probe to the Pi as the lab's wiring sheet shows, with its pull-up
   resistor. [VERIFY] the pins and the resistor value against the sheet and the part's datasheet.
2. **Power on.** Confirm 1-Wire is enabled and the probe appears:

   ```
   ls /sys/bus/w1/devices/
   cat /sys/bus/w1/devices/28-*/w1_slave
   ```

   The second line should end in `t=` and a number of thousandths of a degree. [VERIFY]
3. Start the service on the Pi's lab address (your instructor gives you the address; never use an
   address outside the lab network):

   ```
   python3 sensor_service.py --port 8700 --backend hardware --host <pi address>
   ```

4. From the lab PC: `python bench_check.py --port 8700 --host <pi address>`. Add a row to your step 10
   table for the lab Pi. Expect check 5 to fail: the kit has one real sensor, and the other two report
   `ok: false` on purpose.
5. Ctrl+C on the Pi. **Power off before you unwire anything.**

**Observable result:** a lab Pi row in your table, and a note in `docs/HARDWARE.md` with the room
temperature the probe read.

### Step 14. Stop everything and commit

Ctrl+C in the service terminal. It prints `Stopped.` Confirm `netstat -ano | findstr :8700` prints
nothing. Delete any `__pycache__`. Commit.

**Observable result:** the port is free and `git status` shows nothing uncommitted.

---

## Acceptance criteria

- [ ] `python selfcheck_bench.py` prints `12 of 12 self-checks passed.`
- [ ] `python bench_check.py --port 8700` prints `5 of 5 checks passed.` in normal mode
- [ ] The mode table has seven rows from real runs, and the sentence under it
- [ ] `docs/HARDWARE.md` has the eight-row hardware table with a source for every row, and the parts list
- [ ] Every Pi fact you could not measure is marked [VERIFY]
- [ ] The service is stopped and port 8700 is free
- [ ] No `__pycache__` committed

---

## If it breaks

### 1. The checker refuses to start

```
usage: bench_check.py [-h] --port PORT [--host HOST]
bench_check.py: error: the following arguments are required: --port
```

**Cause:** there is no default port, on purpose. Add `--port 8700`.

### 2. The service refuses to start

```
Cannot start: port 8700 is already in use on 127.0.0.1; choose another or stop that program
```

**Cause:** another service, maybe yours from earlier, still holds the port. Find it with
`netstat -ano | findstr :8700` and stop it, or run on `--port 8701` and pass the same port to the checker.

### 3. Every check fails with "no answer"

```
  2. /api/readings answers in time .... FAIL  (no answer, 1.50 s)
```

**Cause:** nothing is answering on that port: the service is not running, or it runs on another port, or
the simulator is in `silent` mode. `python sim_control.py --port 8700 read` tells you which: a refused
connection prints `No answer from http://127.0.0.1:8700: [WinError 10061] No connection could be made
because the target machine actively refused it`, and silent mode prints `timed out`.

### 4. A self-check says your code raised an exception

```
FAIL   3. a reply with no sequence says so  (raised KeyError: 'sequence')
```

**Cause:** you indexed a key that the reply does not have, `reply["sequence"]`, before checking that it
is there. Check with `in` or use `.get()`. A contract checker must never crash on a bad reply: a bad reply
is exactly what it exists to find.

### 5. On the Pi, the hardware backend will not start

```
No DS18B20 found under /sys/bus/w1/devices. Check that 1-Wire is enabled and the sensor is wired, then try again. Or run the simulator: --backend sim
```

**Cause:** 1-Wire is not enabled on the Pi's image, or the probe is not wired or not seated. **Power off
before you touch the wiring.** This message was captured on the build PC, which has no 1-Wire bus; on
the Pi, confirm step 13.2 first [VERIFY].

### Not an error: drift passes every check

The oven is out of limits, and the contract is still perfectly kept. Deciding what is an alarm is the
panel's job, with your team's limits, on Wednesday.

---

## Stretch goal

Add a sixth check: **the sample is fresh by its own timestamp**. It passes when `sampled_at` is within
5 seconds of this PC's clock, either side. Run it in freeze mode after waiting seven seconds. Then write
two sentences: what does a timestamp check catch, and what can it miss?

---

## Submission checklist

- [ ] Self-check 12 of 12, committed
- [ ] Mode table and sentence in your lab README
- [ ] `docs/HARDWARE.md` with both tables
- [ ] Port free, no `__pycache__`
- [ ] AI usage log updated if you used a model
- [ ] Pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Step 5 not done 15 minutes into Build 2, or the student is editing `fetch()` to make checks pass | SCAFFOLDED |
| Steady progress, questions about the contract's rules | STANDARD |
| 12 of 12 before Build 2 is half over | EXTENDED |
| "I'm never going to work in a factory" | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** `contract_problems` arrives with steps 5 and 7 written. The student writes step 6's
  three field checks and step 8's `ok` and `value` rule.
- **Steps:** step 10's table needs four modes: normal, freeze, drop-sensor, silent.
- **Checkpoints:** show the self-check to the instructor after step 6 and after step 9.
- **Keep step 11.** The hardware table is the competency.

**Acceptance criteria:** 12 of 12 self-checks, the four-row mode table, the hardware table.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus the stretch goal as a requirement: check 6, **the sample is fresh**, with a
5-second limit either side.

**Hint, not the answer.** You need to turn `2027-01-11T14:03:22Z` into a time you can subtract from
now. Read the section on `datetime.fromisoformat()` in the Python documentation for the `datetime`
module, `https://docs.python.org/3/library/datetime.html`, and check what it does with a trailing `Z` in
the version you run. Compare with a time that knows it is UTC: `datetime.now(timezone.utc)`.

**Acceptance criteria:** all STANDARD criteria; check 6 passes in normal mode and fails in freeze mode
after seven seconds; an unreadable timestamp fails check 6 instead of crashing; your README has the two
sentences from the stretch goal.

**Grading:** same scale.

---

## APPLIED

**For the student who will not work in a factory.** The same contract check, somewhere else.

**Changed scenario.** A school's new smart lockers report, over the building network, whether each locker
is open, closed, or unknown, with a sequence number and a UTC timestamp, in the same shape as the Line 3
contract. The front office will trust whatever the lockers say. Write a checker for that contract. Invent
three canned replies (no student names, no locker assignments, nothing personal) including one that
breaks the contract, and a self-check with at least eight checks.

**What you build.** `contract_problems` and `sequence_advanced` for the locker contract, with the same
rules: an `ok` flag that agrees with the value, unique ids, a whole-number sequence, a timestamp ending
in `Z`. Replace step 11 with a requirements table for the device that would report the lockers: what it
needs for power, network, and environment, each row with how you would find out.

**Acceptance criteria:** your self-check passes; a reply that breaks the contract is reported with the
locker's id; the requirements table has a source for every row.

**Grading:** same scale. Requirements Fit is judged on whether the student's contract rules match the
Line 3 rules.
