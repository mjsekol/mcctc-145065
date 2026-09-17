# Lab U09-02 · A Change Across Two Machines
## 145065 Object-Oriented Programming · Unit 9 · Week 17, Wednesday

**Files:** `lab-u09-02-files/`
**Time:** Wednesday Build 1, 35 minutes.
**Due:** end of Wednesday Build 1.
**Competencies:** 5.7.1 (interface control), 5.7.2 (baseline), 5.7.3 (impact of changes),
5.5.1 (data validation), 5.3.4 (relational operators and compound conditions).

**No hardware today.** Everything here runs on a lab PC.

---

## The scenario

The Line 3 shift lead wants a yellow warning when the cure oven passes 225 C, five degrees before the
230 C alarm. Maintenance says "that is one line in the limits file." Before anyone edits a file that
two machines and every trained operator depend on, you are going to find out what that one line
actually touches.

**You will predict, then measure, what a version 1.0.0 panel does with five different limits files,
and write the change impact note that decides how the warning should ship.**

Riverside Fabrication and its Line 3 are a composite, an invented shop.

---

## What is in the folder

| Path | What it is |
|---|---|
| `ConfigProbe/PanelConfig.cs` | the limits file loader from the course's Line 3 reference panel, **copied unchanged**. This is exactly what a 1.0.0 panel runs. |
| `ConfigProbe/Program.cs` | loads one file with that loader and prints LOADED or REFUSED, then every key the loader never reads |
| `configs/thresholds.json` | the shipped limits file, `schema_version` 1 |
| `configs/cr-a-extra-key.json` | change A: adds `"warn_high": 225.0` to the oven, keeps `schema_version` 1 |
| `configs/cr-b-schema-2.json` | change B: the same warning, and `schema_version` 2 |
| `configs/cr-c-rename-all.json` | change C: renames `high` to `alarm_high` on every sensor |
| `configs/cr-d-rename-oven.json` | change D: renames `high` to `alarm_high` on the oven only |

Changes C and D are not the shift lead's request. They are the kind of "cleanup" that happens while
someone is in the file anyway.

The starter is finished code. Today's work is prediction, measurement, and judgment.

---

## Steps

**Step 1.** Copy `lab-u09-02-files/` into your repository as `oop-semester/unit-09-change-impact/`.
Open a terminal there.
*You should see* `ConfigProbe/` and `configs/`.

**Step 2.** Before you run anything, copy this table into `unit-09-change-impact/IMPACT.md` and fill in
the **Predicted** column for every row. Commit the file.

| File | Predicted: LOADED or REFUSED? | Predicted: what the operator would see | Actual (step 4) |
|---|---|---|---|
| `thresholds.json` | | | |
| `cr-a-extra-key.json` | | | |
| `cr-b-schema-2.json` | | | |
| `cr-c-rename-all.json` | | | |
| `cr-d-rename-oven.json` | | | |

Read `PanelConfig.cs` to make your predictions. Look for three things: what it does with
`schema_version`, what it does with a key it does not know, and what it requires of every sensor.
*You should see* your commit in `git log --oneline` **before** step 3.

**Step 3.** Run the probe on the shipped file.

```
dotnet run --project ConfigProbe -- configs/thresholds.json
```

*You should see:*

```
File: thresholds.json
LOADED   3 sensors, stale after 5 s
         oven-temp        Limits 190.0 to 230.0 C
         press-vibration  High limit 6.0 mm/s
         coolant-level    Low limit 25 %
Ignored by a 1.0.0 panel: nothing
```

This is the baseline: the file that shipped with 1.0.0.

**Step 4.** Run the probe on each of the four change files, one at a time. Fill in the **Actual**
column of your table from what it prints. Copy each report into `IMPACT.md` under the table.
*You should see* two files LOADED and two REFUSED. Which ones is what you are finding out.

**Step 5.** Mark every row where your prediction was wrong. For each, write one sentence: what in
`PanelConfig.cs` you missed.

**Step 6.** Find the most dangerous result of the four. Write two sentences in `IMPACT.md`: what an
operator would see on the panel, and what would happen on Line 3 if the oven overheated.

**Step 7.** Now the real request. Fill in this impact table for the shift lead's warning, under the
heading `## CR-17-01 · Oven warning at 225 C`.

| Touches | Impact |
|---|---|
| The reading contract with the sensor computer | |
| `thresholds.json` and its `schema_version` | |
| Every 1.0.0 panel already installed | |
| The panel's states (the truth table from Unit 8) | |
| Word, shape, and color on the tile (REQ-01) | |
| Tests | |
| User guide, screen words, training card, pictures | |
| Version of the panel program | |

**Step 8.** Choose how the warning ships, **A** (extra key, `schema_version` stays 1) or **B**
(`schema_version` 2, and a new panel that reads both 1 and 2). Write a decision log entry in this
course's format: decision, chosen, rejected, why, cost. Your "why" must use what step 4 showed you.

**Step 9.** Write the version numbers your choice implies: the new panel program, and the limits file
format. One sentence each, with the reason.

**Step 10.** Commit `IMPACT.md`.

---

## Acceptance criteria

- [ ] The prediction commit comes **before** any probe run in your history. A prediction written after
      the results is not a prediction.
- [ ] All five Actual cells filled from real probe output, with the reports pasted
- [ ] Every wrong prediction has a sentence naming what was missed
- [ ] Step 6 names the dangerous file and describes the operator's view and the consequence
- [ ] The CR-17-01 table has all eight rows, and none says only "none" without a reason
- [ ] The decision log entry has all five fields and cites step 4
- [ ] Two version numbers, each with a reason

---

## If it breaks

**1. `Usage: ConfigProbe <thresholds file>`**
You left out the file. Put it after the two dashes:
`dotnet run --project ConfigProbe -- configs/cr-a-extra-key.json`

**2. `Cannot read configs/nope.json: Could not find file '...\configs\nope.json'.`**
The name is wrong or you are in a different folder. Run `dir configs` and copy the name exactly.

**3. `REFUSED  schema_version is 2; this panel reads version 1.`**
That is not a broken lab. It is the result for change B. Record it.

**4. You edited `PanelConfig.cs` and every result changed.**
The probe is only worth anything while it runs the 1.0.0 loader unchanged. Put the file back from
`lab-u09-02-files/` before step 4. (The EXTENDED option is where you change it, in a copy.)

---

## Stretch goal

Write change **E** yourself: a file that the 1.0.0 loader **loads**, that looks harmless in a code
review, and that changes what an operator sees for the worse. Run it, paste the report, and write the
one-line check you would add to the loader to refuse it.

---

## Submission checklist

- [ ] `unit-09-change-impact/IMPACT.md`, committed twice: predictions first, then everything
- [ ] Decision log entry for CR-17-01, also copied into your project's `docs/DECISION_LOG.md`
- [ ] `ConfigProbe/PanelConfig.cs` unchanged
- [ ] No `bin` or `obj` folders committed

---

# Extended options

All four assess 5.7.1 and 5.7.3 on the same scale: a prediction made before measurement, a correct
reading of the measurements, and a version decision with a reason.

## SCAFFOLDED

**Same target, three files instead of five.** Run only `thresholds.json`, `cr-b-schema-2.json`, and
`cr-d-rename-oven.json`. Your instructor gives you the CR-17-01 table with four of the eight rows
already filled in, and you fill in the other four.

**Checkpoint.** Show your instructor your three predictions before you run anything.

## STANDARD

The lab as written.

## EXTENDED

**Build option B.** In a copy of `ConfigProbe`, change the loader so that it:

1. reads `schema_version` 1 **and** 2,
2. reads an optional `warn_high` per sensor, which must be below `high` and above `low`,
3. **refuses** a version 1 file that contains `warn_high`, because a 1.0.0 panel would ignore it
   without a word.

Add the warning level to `SensorThreshold` **without breaking any code that already builds one**. The
hint is the C# documentation on records and `init` accessors: learn.microsoft.com, search for
"init-only setters" and "positional records" [VERIFY the pages before you start]. Try it the obvious
way first, as a new positional parameter, and read what the compiler says about every place that calls
the constructor. That list is the impact of the change.

Write an xunit test project that loads the lab's own config files. **How you know it works:**
`cr-b-schema-2.json` loads with a warning of 225.0, `cr-a-extra-key.json` is refused with a sentence
that says why, and the shipped file still loads.

## APPLIED

**Same skill, a file you know.** Pick a settings file in something you use: a game's config file, a
Minecraft server's `server.properties`, or your own `oop-semester` project's `pyproject.toml`. Find
out, from the program's documentation, what it does with a key it does not recognize. Then write the
same five-row predict-and-measure table for five edits of your own, and run each one. Write which edit
was most dangerous and why.

**Why this version.** Every program with a settings file has this exact problem. The Line 3 panel is
one example.

---

## Which version, three observable signals

| If you see | Hand them |
|---|---|
| At step 2, the student cannot find `schema_version` or the "no low and no high" check in `PanelConfig.cs` after five minutes | **SCAFFOLDED** |
| The student has all five Actual cells filled and the step 6 answer written with 15 minutes left | **EXTENDED** |
| The student says "this is only a JSON file, why does it need a version?" | **APPLIED**. Their own tools will answer the question. |
