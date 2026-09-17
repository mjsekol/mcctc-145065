# Gate 2: Adversarial Review · Week 3
## 145065 Object-Oriented Programming · Unit 1 · Week 3, Friday

**35 minutes.** Individual and silent. You may and should run the code and the tests, and write small
scripts that use the class. You may not ask an AI tool whether it is correct, because an AI tool is
what is being reviewed.

The files are `gate2-w03-files/coolant_sensor.py` and `gate2-w03-files/test_coolant_sensor.py`. Copy
both into a scratch folder.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every sensor and
reading here is invented.

---

## What you are looking at

The maintenance team handed an AI assistant the spec in Part A. This time it wrote the class **and
its tests**. Everything runs. Every test passes. The class uses properties, a class method, and a
class attribute, the way this week taught.

**Passing tests are not the same as a correct class.** On Thursday you measured that yourself.

**Five design defects, one in each dimension:**

| Dimension | What to look for this week |
|---|---|
| **Correctness** | A number the class reports that is not the number the spec describes |
| **Security** | A rule the class enforces in one place and skips in another |
| **Readability** | Code whose words and behavior disagree about what kind of method it is |
| **Performance** | Work repeated where it could be done once |
| **Requirements Fit** | A requirement the tests claim to cover and do not |

**One defect is genuinely subtle.** The class has the right check, and the check still does not run
when it matters.

**One defect is arguable.** If you report it, say what you would change it to and why, using
Tuesday's question: what does this method need?

---

## PART A: The spec

> Write `coolant_sensor.py` and its tests for Line 3's coolant tank level sensors.
>
> 1. `CoolantSensor(sensor_id, low_pct, high_pct)`. A sensor id is lowercase words joined by hyphens,
>    such as `coolant-level`. The limits are numbers from 0 to 100, with low below high. Refuse
>    anything else, **when the sensor is built and whenever a limit is changed later.**
> 2. `record(level_pct)` refuses anything that is not a number from 0 to 100, including NaN, and keeps
>    every good reading in order.
> 3. `latest` and `average_pct` are read-only. Before the first reading, both are `None`.
> 4. `status()` returns `"no reading"`, `"low"`, `"high"`, or `"ok"`, from the latest reading.
> 5. `readings_above_average()` returns the readings above the average, in order. A shift records up
>    to 20,000 readings, and the end-of-shift report calls this.
> 6. `CoolantSensor.total_readings()` returns how many readings **all** sensors have recorded this
>    shift.
> 7. `test_coolant_sensor.py` tests every numbered requirement, **including every refusal**.

---

## PART B: What the AI produced

```
python coolant_sensor.py
python -m unittest -v test_coolant_sensor
```

A real run of the program:

```
CoolantSensor('coolant-level', low_pct=20, high_pct=95)
latest 18.0 -> low, average 56.25
above average: [68.5, 67.0, 71.5]
```

And the last lines of the test run:

```
Ran 8 tests in 0.000s

OK
```

---

## What to submit

For each defect: **the file and line**, **the dimension**, **what goes wrong for the maintenance team
or the shift report**, and **the fix**. Then one last entry: **what I was unsure about**, naming
something specific. That entry is scored, and a blank costs more than a wrong guess.

Show your evidence: a command, or a few lines that prove it.

### How to spend 35 minutes

- **First 5:** run both files. Read requirement 7, then count the tests against the requirements.
- **Next 10:** for every rule in requirement 1, find every place a limit gets stored. Try each rule
  at each place.
- **Next 10:** use two sensors the way a whole shift would. Compare what the class reports with what
  you did.
- **Last 10:** read requirement 5 again. Then read every docstring against the line under it.

---

## Scoring

Five defects, one point each, plus one point for the "unsure about" entry. Your instructor states the
security weighting before you start.

**Four of five is a strong score.**
