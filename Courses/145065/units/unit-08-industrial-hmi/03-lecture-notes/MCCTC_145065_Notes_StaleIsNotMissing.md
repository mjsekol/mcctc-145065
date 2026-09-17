# Lecture Notes: Stale Is Not Missing
## 145065 Object-Oriented Programming · Unit 8 · Week 16, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W16_StaleIsNotMissing.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-08-industrial-hmi/04-slides/MCCTC_145065_Slides_W16_StaleIsNotMissing.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK for the
examples.

**Competencies:** 5.6.6 design outputs: stale versus missing · 5.6.14 testing the display rules · 5.5.7
read inputs from a device.

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`.

---

## Why this exists

This is the hardest idea in the unit, and the one the whole panel exists for.

A number on a screen makes a promise: "this is true right now." When the Pi goes quiet, that promise
breaks, but the number does not change. It sits there, steady and calm, looking exactly like a healthy
oven. The course has a name for this: **the dangerous design is the one that works today.**

Your panel has to know two different kinds of "not live" and show them so differently that an operator
can never confuse either one with a live value.

---

## The concept in plain language

**Stale** means the panel has a value it can no longer vouch for. The Pi sent it, but too long ago, or
it keeps sending the same one.

**Missing** means the panel has no value at all. The request failed, the reply was unreadable, or the
sensor said it could not read.

**Fresh takes two checks, and both must pass:**

1. **By timestamp.** The Pi stamps each sample with the time it was taken. If that stamp is more than 5
   seconds before the panel's clock, the sample is old.
2. **By sequence.** The Pi numbers each new sample. The panel remembers, **on its own clock**, when the
   number last changed. If it has not changed for more than 5 seconds, nothing new has been measured,
   whatever the stamp says.

A third case sits in front of both: a stamp far **in the future** means the two clocks disagree, and
the age cannot be known. That is stale too.

**What the operator sees:**

| State | The big value | The box beside it |
|---|---|---|
| Normal or alarm | the live value | nothing |
| Stale | the words NOT LIVE | the old value, with its age, marked not live |
| Missing | no number at all | nothing, not even an old value |

---

## Worked example 1: a check that trusts the timestamp

A delivery app shows where your driver is. Each location update carries the time the driver's phone
stamped it, and an update number. This check trusts the stamp only.

```csharp
using System.Globalization;

DateTimeOffset now = DateTimeOffset.Parse("2027-03-06T18:40:30Z", CultureInfo.InvariantCulture);
TimeSpan limit = TimeSpan.FromSeconds(5);

foreach ((string what, string stamp, int update) in new[]
{
    ("fresh update", "2027-03-06T18:40:29Z", 88),
    ("phone went into a tunnel", "2027-03-06T18:40:21Z", 88),
    ("app re-sends update 88, new stamp", "2027-03-06T18:40:30Z", 88),
})
{
    TimeSpan age = now - DateTimeOffset.Parse(stamp, CultureInfo.InvariantCulture);
    string verdict = age > limit ? "OLD, do not show as live" : "live";
    Console.WriteLine(string.Create(CultureInfo.InvariantCulture,
        $"{what,-36} update {update}  age {age.TotalSeconds,4:0.0} s  {verdict}"));
}
```

```
fresh update                         update 88  age  1.0 s  live
phone went into a tunnel             update 88  age  9.0 s  OLD, do not show as live
app re-sends update 88, new stamp    update 88  age  0.0 s  live
```

The third line is wrong. Update 88 is the same location as before, stamped again. The timestamp check
cannot see that. The update number can: it has not changed. That is the second check, and it uses the
app's own clock to measure how long the number has stood still.

---

## Worked example 2: the panel, four scenes

Lab U8-04's `TileWatch` plays four invented scenes through the panel's rules, one line per second. With
both checks written:

```
1. The Pi freezes: sample 50, taken at t=0, is sent again and again.
  t=0  NORMAL      212.4
  t=1  NORMAL      212.4
  t=2  NORMAL      212.4
  t=3  NORMAL      212.4
  t=4  NORMAL      212.4
  t=5  NORMAL      212.4
  t=6  STALE       NOT LIVE   [Last value 212.4 C, 6.0 s old. Not live.]
  t=7  STALE       NOT LIVE   [Last value 212.4 C, 7.0 s old. Not live.]
  explanation at t=7: Not updated for 7.0 s, so it is not live.

2. The Pi stamps the same sample with the current time every second.
  t=0  NORMAL      212.4
  ...
  t=6  STALE       NOT LIVE   [Last value 212.4 C, 6.0 s old. Not live.]
  t=7  STALE       NOT LIVE   [Last value 212.4 C, 7.0 s old. Not live.]

3. The cable is pulled at t=3.
  t=0  NORMAL      212.0
  t=1  NORMAL      212.1
  t=2  NORMAL      212.2
  t=3  NO DATA     - - -
  ...
  t=7  NO DATA     - - -
  explanation at t=7: No connection to the sensor service. The panel cannot see this value. Check it at the machine.
```

(Lines marked `...` repeat the line above them.)

Read scene 1 at t=5 and t=6. At exactly 5 seconds the value is still fresh, because the rule says
**more than** 5. Read scene 3: the moment the cable goes, the number goes too. There is no old value in
a box, because a pulled cable means the panel knows nothing.

Scene 4, where the Pi's clock runs ten minutes ahead, shows every line as STALE, with the explanation
`The Pi's clock and the panel's clock disagree, so the panel cannot tell how old this value is. It is
not live.`

---

## Worked example 3: three ways to show a value

```csharp
using System.Globalization;

Console.WriteLine(Show("Normal", 212.4, null));
Console.WriteLine(Show("Stale", null, (212.4, 12.0)));
Console.WriteLine(Show("Missing", null, (212.4, 12.0)));

static string Show(string state, double? live, (double Value, double AgeSeconds)? last) => state switch
{
    "Normal" => F($"NORMAL   big: {live:0.0} C   box: (empty)"),
    "Stale" => F($"STALE    big: NOT LIVE   box: Last value {last!.Value.Value:0.0} C, {last.Value.AgeSeconds:0} s old. Not live."),
    _ => "NO DATA  big: - - -      box: (empty)",
};

static string F(FormattableString text) => text.ToString(CultureInfo.InvariantCulture);
```

```
NORMAL   big: 212.4 C   box: (empty)
STALE    big: NOT LIVE   box: Last value 212.4 C, 12 s old. Not live.
NO DATA  big: - - -      box: (empty)
```

Look at the third call. It was handed an old value, and it threw it away. Missing means no number
anywhere. The `_` arm also means any state nobody thought of is shown the safe way.

`InvariantCulture` matters on a shop floor too: a PC set to a language that writes decimals with a comma
would otherwise show `212,4`.

---

## The wrong version: one check instead of two

Delete the sequence check from the panel's freshness rule and run `TileWatch` again. Scene 2, the Pi that
re-stamps an old reading, prints this for all eight seconds:

```
  t=0  NORMAL      212.4
  t=1  NORMAL      212.4
  t=2  NORMAL      212.4
  t=3  NORMAL      212.4
  t=4  NORMAL      212.4
  t=5  NORMAL      212.4
  t=6  NORMAL      212.4
  t=7  NORMAL      212.4
  explanation at t=7: Live. Inside limits.
```

No error. No crash. The panel says "Live" about a reading that is seven seconds old and will never
change. The operator believes the oven is steady at 212.4 C.

**A second wrong version** puts the old value in the big number and adds the word STALE above it. The
test for the display rule fails, and it should. An operator reads the biggest thing on the screen first.

---

## Why the wrong version is tempting

The timestamp is right there in every reply, and it works in every test where the Pi behaves. The
sequence check needs the panel to remember something between polls, which is more code. The failure it
prevents only shows up when a device misbehaves, which is exactly when an operator is relying on the
screen.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Stale** | A value the panel has but can no longer vouch for |
| **Missing** | No value at all |
| **Fresh** | Both checks pass: recent stamp, and a sequence that changed recently |
| **Timestamp** | The time the device says it took the sample |
| **Sequence number** | A counter the device raises for each new sample |
| **Clock skew** | Two clocks that disagree |
| **Fail-safe** | When unsure, show the state that cannot mislead |
| **`InvariantCulture`** | Number and date formatting that does not depend on the PC's language |

---

## Self-check

**Question 1.** The panel's clock reads 10:00:07. The last sample is stamped 10:00:06. Its sequence
number last changed at 10:00:01 by the panel's clock. Fresh or stale? Which check decided it?

**Question 2.** Why is the time the sequence last changed measured on the **panel's** clock, not the
Pi's?

**Question 3.** A teammate says: "When the cable is pulled, show the last value with its age, like
stale. It is more helpful." Give the strongest argument for and the strongest argument against.

---

### Answers

**1.** Stale. The stamp is 1 second old, so the timestamp check passes. The sequence has not changed for
6 seconds, which is more than 5, so the sequence check fails.

**2.** Because the Pi's clock may be the thing that is wrong. The panel's clock is the one the panel can
trust to measure how long it has waited. A Pi that re-stamps old readings, or whose clock drifted, cannot
fool a check made entirely on the panel's side.

**3.** For: the operator gets a hint of where the oven was, which may help a technician decide how fast
to walk. Against: a number on the screen during a disconnect is a number the operator may act on, and
the panel has no idea whether it is still anywhere near true. The course chooses "no number anywhere"
because a missing value that looks missing cannot mislead. A team that argues the other way must show
how its design makes the old value impossible to mistake for live, and test it.
