# Lab U2-04: Sensors Are Parts
## 145065 Object-Oriented Programming · Unit 2 · Week 5

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Tuesday Build 1.
**Competencies:** 5.1.6 (strengths and weaknesses of different approaches for a specific problem:
inheritance against composition), 5.3.12 (classes, objects, and methods).

Files: `lab-u02-04-files/sensors.py` (starter) and `lab-u02-04-files/selfcheck_sensors.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every tag, name,
and reading is invented. No hardware is used; sensors here are objects in a model.

---

## The scenario

Last year someone added sensor readings to Line 3's model by inheritance: a press with a vibration
reading became one subclass, a press with a coolant reading became another, and Press 1, which has
both, became a third class pasted together from the first two. The shop now wants oil temperature on
some presses, which would double the number of classes again. A press is not a sensor, and the model
has been pretending it is.

## What you will build

Powered equipment that **has** any number of sensors, attached, checked, and asked for their findings,
with the four reading subclasses deleted.

---

## Starter code

Copy both files into one folder and run:

```
python sensors.py
python selfcheck_sensors.py
```

The starter prints:

```
Findings:
  [WARNING] L3-PRS-01: coolant-level reads 14 %, below 20
  [WARNING] L3-PRS-02: press-vibration reads 9.2 mm/s, above 8
  [WARNING] L3-OVN-01: 228 C is 28 C from setpoint 200 C

After the Press 2 cable is pulled:
  [INFO] L3-PRS-02: press-vibration has no reading
```

The self-check ends `1 of 9 self-checks passed`. The one that passes checks that the findings match
the starter's. **It must still pass at the end.** Your refactor changes the design, not the report.

The `Sensor` class at the top of the file is complete, and nothing uses it yet. Do not change it. Read
its `inspect()` and `_mount()` methods before you start.

---

## Steps

### Step 1. Count the explosion

In your README, under `## The class explosion`, answer: the shop has three sensor kinds (vibration,
coolant, oil temperature), and any press may have any mix of them. How many press classes does the
inheritance design need, counting the press with none? Then name the one method that
`VibrationCoolantPress` repeats from two other classes.

**Observable result:** a number and a method name.

### Step 2. Give powered equipment a place for its sensors

In `PoweredEquipment.__init__`, add `self._sensors = {}`, a dictionary from sensor id to sensor. Add
`sensor(self, sensor_id)`, which returns `self._sensors[sensor_id]`, and a `sensors` property that
returns `tuple(self._sensors.values())`.

**Observable result:** the program still runs. The self-check is still `1 of 9`.

### Step 3. Write `attach_sensor()`, the one door in

`attach_sensor(self, sensor)` refuses three things, then mounts and stores the sensor:

1. Anything that is not a `Sensor`: `TypeError`.
2. A second sensor with an id this machine already has: `ValueError`.
3. A sensor already mounted on a different machine: `sensor._mount(self.asset_tag)` refuses it for you.

Then store it by its id and return it.

**Observable result:** `5 of 9`. All four Step 3 checks PASS.

### Step 4. Ask the parts: `common_findings()`

In `PoweredEquipment`, write `common_findings()`: start from `super().common_findings()`, then extend
the list with `sensor.inspect()` for every sensor. `Equipment.inspect()` already puts
`common_findings()` first, so every powered machine now reports its sensors.

**Observable result:** `6 of 9`. The Step 4 check builds a press with an oil temperature sensor and a
vibration sensor, and needs no new class to do it.

### Step 5. The oven reads its own sensor

In `Oven`, write `temperature_sensor()`, which returns the first mounted sensor whose `kind` is
`"temperature"`, or `None`. Rewrite `Oven._kind_findings()`:

- no temperature sensor: a `warning`, `no temperature sensor mounted`
- a sensor with no reading: return an empty list, because the sensor already reported it
- otherwise, the maximum and setpoint checks from `MonitoredOven`, reading `sensor.value`

Delete the "above 240" line: the sensor's own high limit reports that now.

**Observable result:** `7 of 9`.

### Step 6. Rebuild the sample, and delete the four subclasses

Rewrite `build_sample()` so every machine is a plain `Press` or `Oven` with sensors attached:

| Machine | Sensors |
|---|---|
| Press 1 | `press-vibration` (vibration, mm/s, 0 to 8) and `coolant-level` (level, %, 20 to 100) |
| Press 2 | `press-vibration` (vibration, mm/s, 0 to 8) |
| Cure Oven | `oven-temp` (temperature, C, 0 to 240) |

Rewrite `record_sample_readings()` to record through `press1.sensor("press-vibration").record(3.1)`
and so on, and change the cable-pulled line in `main()` to `clear()` the sensor. Then delete
`VibrationPress`, `CoolantPress`, `VibrationCoolantPress`, and `MonitoredOven`.

**Observable result:** `9 of 9 self-checks passed`, and `python sensors.py` prints exactly the starter
output. Commit.

### Step 7. Leak the parts on purpose

Change the `sensors` property to `return self._sensors`. Then run:

```
python -c "import sensors; press1, press2, oven = sensors.build_sample(); sensors.record_sample_readings(press1, press2, oven); print('before:', [str(f) for f in press1.inspect()]); press1.sensors.clear(); print('after: ', [str(f) for f in press1.inspect()])"
```

**Observable result:** no error, and:

```
before: ['[WARNING] L3-PRS-01: coolant-level reads 14 %, below 20']
after:  []
```

The self-check drops to `8 of 9`. Copy the two lines into your README under `## The leak`, with two
sentences: who could run that `clear()`, and what the supervisor would then see. Restore the tuple and
confirm 9 of 9.

### Step 8. Write the analysis paragraph

Under `## Inheritance or composition` in your README, write one paragraph: why a press should have
sensors rather than be one, the strongest argument **for** the inheritance design, and why it loses
for this shop. This paragraph is practice for your project's written analysis.

**Observable result:** a paragraph that names a strength and a weakness of each approach. Commit.

---

## Acceptance criteria

- [ ] `python selfcheck_sensors.py` prints `9 of 9 self-checks passed`
- [ ] `python sensors.py` prints exactly the starter output
- [ ] The four reading subclasses are gone; `Sensor` is unchanged
- [ ] `sensors` returns a copy; `attach_sensor()` is the only way to add a sensor
- [ ] README: the class explosion, the leak, and the analysis paragraph
- [ ] Committed and pushed

---

## If it breaks

### 1. Something that is not a sensor

```
TypeError: expected a Sensor, not str
```

**Cause:** your own `attach_sensor()` doing its job. Pass a `Sensor` object, not its id.

### 2. The same id twice on one machine

```
ValueError: L3-PRS-01 already has a sensor named press-vibration
```

**Cause:** `build_sample()` attached the same id twice to one machine. Two different presses may each
have a `press-vibration` sensor. One press may not have two.

### 3. One sensor object on two machines

```
ValueError: coolant-level is already mounted on L3-PRS-01
```

**Cause:** the same `Sensor` object was attached to two machines. Create a new `Sensor` for each
machine.

### 4. A sensor the machine does not have

```
KeyError: 'oil-temp'
```

**Cause:** `sensor("oil-temp")` asked for an id that was never attached, or was misspelled.

### 5. A findings list that was never started

```
NameError: name 'findings' is not defined. Did you mean: 'Finding'?
```

**Cause:** `common_findings()` uses `findings.extend(...)` without first writing
`findings = super().common_findings()`.

### 6. The subclasses deleted before the sample was rebuilt

```
NameError: name 'VibrationCoolantPress' is not defined
```

**Cause:** step 6 in the wrong order. Rewrite `build_sample()` first, then delete the classes.

**Error wording was captured on Python 3.13.7.** Confirm it on the lab's Python 3.14.

---

## Stretch goal

Batteries on the shop's carts get swapped between carts during a shift. Write a short `Cart` class
that **has** a `Battery` and a `swap_battery(new)` method that returns the old one. In your README,
explain why `class Cart(Battery)` could not model a swap at all.

---

## Submission checklist

- [ ] Self-check 9 of 9
- [ ] Output identical to the starter's
- [ ] README: class explosion, the leak, inheritance or composition
- [ ] Step 7 change restored
- [ ] Committed and pushed
- [ ] AI usage log updated if you used a model

---

# Extended Lab Options

All four versions assess the same competencies (5.1.6, 5.3.12) and grade on the same 100-point
five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| At minute 12 of Build 1, `attach_sensor()` is not started, or the student is editing `Sensor` | SCAFFOLDED |
| Steady progress, questions about where the findings come from | STANDARD |
| 9 of 9 with 10 minutes of Build 1 left | EXTENDED |
| The student says factories are not their thing | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** the instructor hands out a `sensors.py` in which `PoweredEquipment` already has
  `_sensors`, `attach_sensor()`, `sensor()`, and `sensors`. It starts at step 4.
- **Steps:** skip steps 2 and 3. Step 1 and step 8 are unchanged.
- **Checkpoints:** show the instructor the self-check after step 4 and after step 6.
- **Keep step 7.** The leak is the lesson.

**Acceptance criteria:** 9 of 9, the three README sections.

**Grading:** same scale. Full completion earns the same grade as STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one idea the lab has not taught.

**Added requirement.** Callers want to look sensors up by id without calling a method, and to see new
sensors appear as they are attached. Add a `sensor_map` property that gives a **live, read-only**
view of the dictionary: reading works, and every attempt to add, replace, or delete through it is
refused.

**Hint, not the answer.** The standard library's `types` module has a class that wraps a dictionary
in a read-only view. Read its documentation page, `https://docs.python.org/3/library/types.html`.

**Acceptance criteria:** all STANDARD criteria; a demonstration that prints the view's keys before and
after attaching an oil sensor, and shows the error from `del view["coolant-level"]`.

**Grading:** same scale.

---

## APPLIED

**For the student who says factories are not their thing.** The same design in a game.

**Changed scenario.** A game character can carry any mix of gear: a lantern, a shield, a grappling
hook. The first version made `LanternCharacter`, `ShieldCharacter`, and `LanternShieldCharacter`.
Refactor to a `Character` that **has** a collection of `Gear` objects, each able to report on itself
(a lantern low on oil, a cracked shield). Invent every item and rule. No real game's content.

**What you build.** `add_gear()` with the same three refusals as `attach_sensor()`, a `gear` property
that returns a copy, a `status()` that delegates to each piece of gear, and a self-check with at least
six checks.

**Acceptance criteria:** your self-check passes; your README has the class explosion count for your
game and the inheritance or composition paragraph.

**Grading:** same scale.
