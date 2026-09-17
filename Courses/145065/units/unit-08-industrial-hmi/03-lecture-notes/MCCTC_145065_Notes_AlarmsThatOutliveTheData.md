# Lecture Notes: Alarms That Outlive the Data
## 145065 Object-Oriented Programming · Unit 8 · Week 16, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W16_AlarmsThatOutliveTheData.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-08-industrial-hmi/04-slides/MCCTC_145065_Slides_W16_AlarmsThatOutliveTheData.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK for the
examples.

**Competencies:** 5.6.6 design processes: fail-safe alarm behavior · 5.3.5 conditional control
structures · 5.6.1 requirements: confirmation before an action · 5.6.14 testing.

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`.

---

## Why this exists

The oven runs hot. The tile turns red. A minute later a cart clips the Pi's cable, and the tile goes
dark. What should the next person to walk past see?

If your panel decides "alarm" from the current value, the answer is: nothing. No value, so no alarm.
The one moment the operator most needs a warning is the moment it disappears.

An alarm is not a color. It is a **memory**: something happened, and a person has not dealt with it
yet. Memory needs a structure that only the right events can change.

---

## The concept in plain language

**A state machine** is a value that can be in one of a few named states, plus rules for which event
moves it where. Your panel's alarm memory, the **latch**, has four states. Lab U8-05 lists the six rules
that move it.

**Only two kinds of event may move the latch:**

- a **live** value, inside or outside its limits;
- a **person** acknowledging the alarm.

**Stale and missing data move nothing.** "I do not know" is never a reason to change what the panel
remembers.

**Acknowledging is not clearing.** An acknowledged alarm on a value still out of limits is still an
alarm. The banner changes its words and stays.

**Acknowledging takes two steps.** The button opens a question that covers the panel. Only YES acts.
CANCEL, or Escape, changes nothing. A gloved hand that brushes the screen must not dismiss an alarm.

---

## Worked example 1: a memory with three states

A drone controller warns about a low battery. The warning is a memory with three states: **Quiet**,
**Unseen**, and **Seen**. Readings below 10 percent raise it. Readings above 25 percent end it. The pilot
tapping SEEN marks it seen. A lost radio link, "no reading", changes nothing.

```csharp
using System.Globalization;

string warning = "Quiet";
foreach (string happens in new[] { "18%", "9%", "no reading", "no reading", "pilot taps SEEN", "7%", "no reading", "31%" })
{
    string before = warning;
    warning = happens switch
    {
        "pilot taps SEEN" => warning == "Unseen" ? "Seen" : warning,
        "no reading" => warning,
        _ => OnReading(warning, int.Parse(happens.TrimEnd('%'), CultureInfo.InvariantCulture)),
    };
    Console.WriteLine($"{happens,-16} {before,-7} -> {warning}");
}

static string OnReading(string current, int percent) => percent switch
{
    < 10 => current == "Seen" ? "Seen" : "Unseen",
    > 25 => "Quiet",
    _ => current,
};
```

```
18%              Quiet   -> Quiet
9%               Quiet   -> Unseen
no reading       Unseen  -> Unseen
no reading       Unseen  -> Unseen
pilot taps SEEN  Unseen  -> Seen
7%               Seen    -> Seen
no reading       Seen    -> Seen
31%              Seen    -> Quiet
```

Lines 3 and 4 are the lesson. The radio went quiet with the battery at 9 percent, and the warning
stayed. Line 6: a new low reading does not undo the pilot's SEEN. The panel's latch has one more state
than this, for an alarm that ended before anyone saw it, and the same shape.

---

## Worked example 2: write the table before the code

A state machine is clearest to check as a table: one row per current state, one column per event. For
the drone:

| Current | Reading below 10 | Reading above 25 | Reading between | No reading | Pilot taps SEEN |
|---|---|---|---|---|---|
| Quiet | Unseen | Quiet | Quiet | Quiet | Quiet |
| Unseen | Unseen | Quiet | Unseen | Unseen | Seen |
| Seen | Seen | Quiet | Seen | Seen | Seen |

Read the "No reading" column. Every cell equals its row's current state. If any cell in that column
differs, the design forgets on a lost link.

In Lab U8-05 you fill in the panel's version on paper, four rows and four columns, **before** you write
`Next`. Then the `switch` is a copy of the table, and the tests are a copy of its cells.

---

## Worked example 3: the question before the action

Deleting a saved game works the way acknowledging an alarm should: the button asks, and only YES acts.

```csharp
string save = "Slot 2: Chapter 7";
bool questionOpen = false;

Press("DELETE");
Press("CANCEL");
Press("DELETE");
Press("YES");
Press("YES");

void Press(string button)
{
    switch (button)
    {
        case "DELETE" when save != "(empty)":
            questionOpen = true;
            break;
        case "CANCEL":
            questionOpen = false;
            break;
        case "YES" when questionOpen:
            questionOpen = false;
            save = "(empty)";
            break;
    }

    Console.WriteLine($"{button,-7} question {(questionOpen ? "OPEN  " : "closed")}  save {save}");
}
```

```
DELETE  question OPEN    save Slot 2: Chapter 7
CANCEL  question closed  save Slot 2: Chapter 7
DELETE  question OPEN    save Slot 2: Chapter 7
YES     question closed  save (empty)
YES     question closed  save (empty)
```

CANCEL changed nothing. The second YES, with no question open, changed nothing. The question closes
**before** the action, so it can never stay open over something that already changed.

---

## The wrong version: an alarm that is a Boolean

```csharp
using System.Globalization;

double? latest;
foreach (double? reading in new double?[] { 212.0, 236.0, null, null })
{
    latest = reading;
    bool isAlarm = latest > 230.0;
    string shown = latest is double v ? v.ToString("0.0", CultureInfo.InvariantCulture) : "no data";
    Console.WriteLine($"oven {shown,-8} alarm banner: {(isAlarm ? "UP" : "none")}");
}
```

```
oven 212.0    alarm banner: none
oven 236.0    alarm banner: UP
oven no data  alarm banner: none
oven no data  alarm banner: none
```

It compiles with 0 warnings and runs without an error. In C#, comparing a missing `double?` with `>`
gives `false`, so the alarm quietly vanished the moment the data did. The next shift sees a dark tile and
no warning.

The same mistake inside a latch looks like this: a discard arm that returns `Clear` instead of the
current state. In the lab's `ShiftReplay`, the oven goes into alarm at step 2 and the Pi freezes at
step 3:

```
   2  oven reads 236.0, live                    Alarm    ActiveUnacked    UNACKNOWLEDGED ALARM            closed
   3  the Pi freezes                            Stale    Clear            (none)                          closed
```

**A switch with no discard arm at all** is caught earlier. The compiler warns:

```
warning CS8509: The switch expression does not handle all possible values of its input type (it is not exhaustive). For example, the pattern 'Line3.Hmi.Core.SensorState.Stale' is not covered.
```

and, if you ignore it, the first stale reading throws:

```
System.Runtime.CompilerServices.SwitchExpressionException : Non-exhaustive switch expression failed to match its input.
```

---

## Why the wrong version is tempting

A Boolean is one line and it is correct on every screenshot you take while the Pi is healthy. The latch
needs a table, four states, and tests for events that "never happen." They happen on the shift nobody is
watching.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **State machine** | A value with named states and rules for moving between them |
| **Latch** | A state that stays set until a specific event resets it |
| **Transition** | One move from one state to another |
| **Acknowledge** | A person confirming they have seen an alarm; not the same as clearing it |
| **Discard pattern** | `_` in a `switch`: matches anything not matched above |
| **Exhaustive** | A `switch` that handles every possible input |
| **Two-step confirmation** | An action that runs only after a question is answered YES |

---

## Self-check

**Question 1.** In worked example 1, the events are `9%`, `pilot taps SEEN`, `31%`, `8%`. What is the
warning after each?

**Question 2.** Your latch's discard arm returns the current state. A teammate says that is lazy and every
state should be listed. Give one reason the discard arm is the safer choice here.

**Question 3.** The operator presses ACKNOWLEDGE ALARM. While the question is open, the oven returns to
normal. Then the operator presses YES. What should happen, and why must your code check again inside
YES instead of trusting the button?

---

### Answers

**1.** `9%` makes it Unseen. `pilot taps SEEN` makes it Seen. `31%` makes it Quiet. `8%` makes it
Unseen again: after Quiet there is nothing seen to keep, so a new low reading is a new warning.

**2.** A state added later, or an event nobody listed, falls into the discard arm and changes nothing.
"Change nothing" is the safe default for a memory, because it can never hide an alarm. A list with no
discard would throw at run time on the first event nobody thought of.

**3.** Acknowledge whatever the alarm is **now**. It is an alarm that ended and was not yet acknowledged,
so acknowledging it clears it. The code must look at the latch's current state when YES is pressed,
because the data can change between the question and the answer. A button's enabled state can lag by
an instant.
