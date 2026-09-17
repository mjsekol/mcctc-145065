# Lab U8-04: Stale or Missing
## 145065 Object-Oriented Programming · Unit 8 · Week 16, Monday

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Monday Build 1, finishing in the last
25 minutes of Build 2.
**Competencies:** 5.6.6 (design system outputs), 5.6.14 (testing), 5.3.4 (relational operators and
compound conditions), 5.5.6 (format output).

Files: `lab-u08-04-files/StaleOrMissing/`. The given files are copied from the course's HMI anchor:
`PanelConfig.cs`, `Clock.cs`, and `ObservableObject.cs` unchanged; `SensorTileViewModel.cs` with the body
of one `switch` removed; `PanelMonitor.cs` and `AlarmLatch.cs` trimmed to the parts this lab needs.
`StateRules.Truth.cs` is Lab U08-03's answer, given so this lab stands on its own.

**Riverside Fabrication is a composite.** No hardware and no service are used: a scripted clock plays
the scenes.

---

## The scenario

Twice last month (in this invented shop), the Line 3 Pi kept answering after its sensor loop had hung,
and once someone pulled its cable. Each time, an operator had to decide from the panel what was true. A
number the panel can no longer vouch for, and a number the panel does not have, are different facts, and
an operator does different things about each. The panel must never let either one look live.

## What you will build

The freshness rule that decides whether a sample is live, and the display rules that decide what a tile
shows for each of the four states.

---

## The rules you are writing

**Fresh** means both of these are true, with a stale limit of 5 seconds:

1. **By timestamp.** The sample's own `sampled_at` is no more than 5 s older than the panel's clock.
2. **By sequence.** The Pi's sequence number changed no more than 5 s ago, by the **panel's** clock.

A sample stamped **more than 5 s in the future** means the two clocks disagree; the panel cannot tell how
old it is, so it is not live either. A sample exactly at the limit is still fresh.

**What a tile shows:**

| State | `StateText` | `ValueText` (the big number) | `ValueIsLive` | `LastKnownText` |
|---|---|---|---|---|
| Normal | `NORMAL` | the live value, formatted | true | empty |
| Alarm | `ALARM HIGH` or `ALARM LOW` | the live value, formatted | true | empty |
| Stale | `STALE` | `NOT LIVE` | false | `Last value 212.4 C, 12 s old. Not live.` |
| Missing | `NO DATA` | `- - -` | false | empty: **no number anywhere** |

Format a value with the threshold's `Format` method, and an age with `PanelMonitor.FormatAge`.

---

## Starter code

```
StaleOrMissing/
  StaleOrMissing.sln
  Display/
    StateRules.cs                 the state names (given)
    StateRules.Truth.cs           Decide (given)
    StateRules.Freshness.cs       YOU WRITE CheckFreshness
    PanelConfig.cs                SensorThreshold with Check and Format (given)
    PanelMonitor.cs               SensorStatus and FormatAge (given, trimmed)
    AlarmLatch.cs                 the latch states (given, trimmed)
    Clock.cs                      (given)
    ViewModels/
      ObservableObject.cs         (given)
      SensorTileViewModel.cs      YOU WRITE the switch inside Apply
  TileWatch/                      plays four scenes through your code (given)
  Display.SelfCheck/              20 checks (given)
```

The starter's `CheckFreshness` calls every sample fresh: exactly the bug this lab removes. The starter's
`Apply` sets nothing, so every tile says NO DATA while its explanation says "Live. Inside limits." That
contradiction is on purpose.

Use an artifacts folder outside your repository on every `dotnet` command, for example
`--artifacts-path C:\build\lab04` [VERIFY a folder students may write to].

---

## Part 1: freshness

### Step 1. Build, run, check

```
dotnet build StaleOrMissing.sln --artifacts-path C:\build\lab04
dotnet run --project TileWatch --artifacts-path C:\build\lab04
dotnet test Display.SelfCheck --artifacts-path C:\build\lab04
```

**Observable result:** 0 warnings. `TileWatch` prints four scenes of eight lines each, every line
`NO DATA     - - -`. The self-check reports **4 passed, 16 failed**. Read scene 1's last line: the
explanation disagrees with the tile.

### Step 2. Read what is given

Read `SensorStatus` in `PanelMonitor.cs` and the part of `Apply` after the `switch`. Answer in your
README: **which property does the alarm banner follow, and why does that matter when data stops?**

**Observable result:** two sentences in your README.

### Step 3. Fresh by timestamp

In `CheckFreshness`, compute the sample's age, `now - sampledAt`. If it is greater than `staleAfter`,
return `StaleReason.SampleTooOld`. Strictly greater: exactly at the limit is fresh.

**Observable result:** the build succeeds. The freshness rows that expect `SampleTooOld` pass.

### Step 4. Fresh by sequence

If `now - sequenceLastAdvancedAt` is greater than `staleAfter`, return
`StaleReason.SequenceNotAdvancing`.

**Observable result:** F02 passes: a Pi that restamps an old reading with the current time is caught.

### Step 5. The honest limit

If the age is **less than** `-staleAfter`, return `StaleReason.ClockDisagrees`. Put this check
**first**: a large negative age would pass the "too old" test.

**Observable result:** the self-check reports **11 passed, 9 failed**: all ten freshness cases pass,
and only the display checks still fail (D06 passed from the start, by accident).

### Step 6. Break it on purpose, then restore

Delete your sequence check and run `TileWatch`.

**Observable result:** scene 2 shows `NORMAL      212.4` for every second, t=0 through t=7, even though
sample 50 never changed. Copy scene 2 into your README under `## Two checks, not one`, and write one
sentence about what the operator would believe. Restore the check.

---

## Part 2: what the tile shows

### Step 7. Normal

In `Apply`'s `switch`, add `case SensorState.Normal:`. Set `StateText` to `"NORMAL"`, `ValueText` to the
live value formatted by `t.Format(...)`, `ValueIsLive` to `true`, and `LastKnownText` to empty.

**Observable result:** D01 and D02 pass. `D02` shows a coolant level with zero decimals as `68`.

### Step 8. Alarm

`case SensorState.Alarm:` is the same as normal, except `StateText` is `"ALARM LOW"` when
`status.Side` is `AlarmSide.Low` and `"ALARM HIGH"` otherwise.

**Observable result:** D03 passes for both sides.

### Step 9. Stale

`case SensorState.Stale:` sets `StateText` to `"STALE"`, `ValueText` to `NotLiveText`, `ValueIsLive` to
`false`, and `LastKnownText` to
`Last value <value> <unit>, <age> old. Not live.`, using `status.LastKnownValue` and
`PanelMonitor.FormatAge(status.LastKnownAge ?? TimeSpan.Zero)`. If there is no last value, leave
`LastKnownText` empty. Build the string with `string.Create(CultureInfo.InvariantCulture, $"...")`, so a
PC set to a comma decimal still prints `212.4`.

**Observable result:** D04, D05, D07, and D09 pass.

### Step 10. Missing

`default:` sets `StateText` to `"NO DATA"`, `ValueText` to `NoValueText`, `ValueIsLive` to `false`, and
`LastKnownText` to empty. No number, not even an old one.

**Observable result:** `dotnet test Display.SelfCheck` reports **20 passed**. `TileWatch` prints the four
scenes in the table below.

| Scene | t=0 to t=5 | t=6 and t=7 |
|---|---|---|
| 1. the Pi freezes | `NORMAL 212.4` | `STALE NOT LIVE [Last value 212.4 C, 6.0 s old. Not live.]`, then 7.0 s |
| 2. the Pi restamps | `NORMAL 212.4` | the same as scene 1 |
| 3. the cable is pulled at t=3 | `NORMAL` 212.0, 212.1, 212.2, then `NO DATA - - -` from t=3 | `NO DATA - - -` |
| 4. the Pi's clock is 10 min ahead | `STALE NOT LIVE [Last value 212.4 C, 0.0 s old. Not live.]` | the same |

Scene 4 says `0.0 s old` because the sequence moves every second: by the panel's own clock the value is
new, and it still is not live, because the panel cannot trust the Pi's stamp. Write one sentence in your
README about whether that line would confuse an operator, and what you would change.

### Step 11. Move your work into the project

Copy `StateRules.Freshness.cs` into the project's `Line3.Hmi.Core/`, and your `switch` into the project's
`SensorTileViewModel.Apply`. Run the project's tests.

**Observable result:** the project's REQ02, REQ03, REQ05, REQ14, and REQ15 tests pass.

### Step 12. Commit

No `bin` or `obj` in either repository. Commit and push.

---

## Acceptance criteria

- [ ] `dotnet test Display.SelfCheck` reports 20 passed
- [ ] `TileWatch` prints the four scenes above
- [ ] A stale value appears only in `LastKnownText`; a missing value appears nowhere
- [ ] Your README has the banner answer, `## Two checks, not one`, and the scene 4 sentence
- [ ] The project's REQ02, REQ03, REQ05, REQ14, and REQ15 tests pass
- [ ] No `bin` or `obj` committed

---

## If it breaks

### 1. The clock check is missing or in the wrong place

```
Assert.Equal() Failure: Values differ
Expected: ClockDisagrees
Actual:   None
```

**Cause:** no future check, or it comes after the timestamp check. With a sample stamped 10 minutes ahead
and a stuck sequence, the result is `SequenceNotAdvancing` instead: still not live, but the wrong reason,
and the operator gets the wrong explanation.

### 2. Exactly at the limit is stale

```
Assert.Equal() Failure: Values differ
Expected: None
Actual:   SampleTooOld
```

**Cause:** `>=` instead of `>`. Five seconds old is still fresh by the course's rule.

### 3. The stale number is in the big value

```
Assert.Equal() Failure: Strings differ
Expected: "NOT LIVE"
Actual:   "212.4"
```

**Cause:** the stale case formatted the last value into `ValueText`. That is the one thing the display
must never do.

### 4. A stale tile crashes

```
System.InvalidOperationException : Nullable object must have a value.
```

**Cause:** the stale case used `status.LiveValue!.Value`. A stale status has no live value: use
`LastKnownValue`, and check it with `is double last`.

### 5. The window never updates the "last value" box

```
Assert.Contains() Failure: Item not found in collection
Not found:  "LastKnownText"
```

D09 fails, and every other check passes. **Cause:** the stale case set the private field
`lastKnownText` instead of the property `LastKnownText`, so `PropertyChanged` never fired and a window
would keep showing the old box. Set the property.

---

## Stretch goal

Make the stale box also say **when** the last value was taken, in the panel's own time zone:
`Last value 212.4 C at 09:03:22, 12 s old. Not live.`

---

## Submission checklist

- [ ] Self-check 20 of 20
- [ ] README sections complete
- [ ] Project REQ tests passing
- [ ] AI usage log updated if you used a model
- [ ] Pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Step 3 not done 15 minutes into Build 1, or the student is editing `TileWatch` to change its output | SCAFFOLDED |
| Steady progress, questions about which check comes first | STANDARD |
| 20 of 20 before the clinic starts | EXTENDED |
| "Stale versus missing only matters in a factory" | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** `CheckFreshness` arrives with the three `if` statements in the right order and
  empty conditions. `Apply` arrives with the four `case` labels and the `StateText` lines.
- **Steps:** step 6 is kept. Step 9's string is given as a template with blanks.
- **Checkpoints:** show the self-check after step 5 and after step 10.

**Acceptance criteria:** 20 of 20, `## Two checks, not one`, the project tests.

**Grading:** same scale.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus the stretch goal as a requirement.

**Added requirement.** Write `LastValueClock.Describe(threshold, value, sampledAt, age, displayZone)`
that returns the stale sentence with the sample's clock time in the given zone. Add a check with a fixed
zone five hours behind UTC, so the test does not depend on the PC's zone or on daylight saving time.

**Hint, not the answer.** `sampled_at` arrives in UTC. Read about `TimeZoneInfo.ConvertTime` and
`TimeZoneInfo.CreateCustomTimeZone` in the .NET API reference on learn.microsoft.com [VERIFY the exact
pages].

**Acceptance criteria:** all STANDARD criteria; a sample at 14:03:22 UTC reads `at 09:03:22` in the
custom zone; the new check passes.

**Grading:** same scale.

---

## APPLIED

**For the student who thinks this only matters in a factory.** The same skill, somewhere else.

**Changed scenario.** A group chat app shows each friend's location on a map for a meetup. A friend whose
phone stopped sending updates five minutes ago must not appear as "here now"; a friend who turned sharing
off must not appear at all, not even at the last known spot. Use invented names only.

**What you build.** A `Freshness` check with the same two rules (the phone's timestamp, and whether its
update counter moved) and a display function that shows "here now", "last seen 5 min ago at the park,
may have moved", or "location off", with tests for each.

**Acceptance criteria:** tests for all three displays and for a phone whose clock is wrong; no location
shown for "location off".

**Grading:** same scale. Requirements Fit is judged on whether a stale location is ever shown as current.
