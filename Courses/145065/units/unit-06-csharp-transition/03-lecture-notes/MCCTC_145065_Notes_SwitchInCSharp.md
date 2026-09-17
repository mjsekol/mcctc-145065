# Lecture Notes: `switch`, and Why Arm Order Matters
## 145065 Object-Oriented Programming · Unit 6 · Week 12, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W12_Switch.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W12_Switch.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK.

**Competency:** 5.3.7 write code that uses selection control structures (case, switch).

Every output and error below was printed by a real build: .NET SDK 10.0.401, `net8.0`. Python
outputs are from Python 3.13.7.

---

## Why this exists

An operator panel spends its life turning one value into one decision: this temperature is normal,
warning, or alarm; this level means "call the lead" or "watch it." You wrote those decisions in
Python with `if` and `elif`, and maybe with `match`. C# has `switch`, in two forms, and it checks
some of your decisions before the program runs. Not all of them. Today is about which.

---

## The concept in plain language

**The switch statement** runs a block of code for the case that matches. Each case must end with
`break`, `return`, or `throw`. C# does not let one case fall into the next.

**The switch expression** turns one value into one value. Its arms are tried top to bottom, and
**the first arm that matches wins**, not the best one.

| Python | C# statement | C# expression |
|---|---|---|
| `match level:` | `switch (level) { ... }` | `level switch { ... }` |
| `case "alarm":` | `case Level.Alarm:` | `Level.Alarm => ...,` |
| `case _:` | `default:` | `_ => ...,` |
| `case 1 \| 2:` | `case 1: case 2:` | `1 or 2 => ...,` |
| `if t >= 240:` | inside a case | `>= 240 => ...,` a relational pattern |
| nothing happens if no case matches | nothing happens if no case matches | a warning at build time, an exception at run time |

---

## Worked example 1: the same decision, both forms

```csharp
foreach (double? reading in new double?[] { 198.0, 222.5, 247.0, null })
{
    Console.WriteLine($"{Show(reading),6}  {Classify(reading),-8} {Advice(Classify(reading))}");
}

static string Show(double? value) => value?.ToString() ?? "--";

static Level Classify(double? tempC) => tempC switch
{
    null => Level.Missing,
    >= 240 => Level.Alarm,
    >= 215 => Level.Warning,
    _ => Level.Normal,
};

static string Advice(Level level)
{
    switch (level)
    {
        case Level.Alarm:
            return "call the lead now";
        case Level.Warning:
            return "watch it";
        case Level.Missing:
            return "check the sensor";
        default:
            return "no action";
    }
}

enum Level
{
    Missing,
    Normal,
    Warning,
    Alarm,
}
```

Output:

```
   198  Normal   no action
 222.5  Warning  watch it
   247  Alarm    call the lead now
    --  Missing  check the sensor
```

`Classify` checks `null` first, because a missing reading is not a number to compare. Then the most
urgent test, then the next. An `enum` is a named set of values, and `Level.Alarm` cannot be
misspelled without a compiler error, which a string like `"alram"` could.

`value?.ToString() ?? "--"` means: if `value` is null, use `"--"`. `{x,6}` pads to six characters,
right-aligned, and `{x,-8}` pads to eight, left-aligned.

---

## Worked example 2: stacked labels and `or`

```csharp
foreach (string day in new[] { "Sat", "Tue", "Sun" })
{
    switch (day)
    {
        case "Sat":
        case "Sun":
            Console.WriteLine($"{day}: line down");
            break;
        default:
            Console.WriteLine($"{day}: line running");
            break;
    }
    string kind = day switch
    {
        "Sat" or "Sun" => "weekend",
        _ => "weekday",
    };
    Console.WriteLine(kind);
}
```

Output:

```
Sat: line down
weekend
Tue: line running
weekday
Sun: line down
weekend
```

Two labels on one block are allowed, because the first label has no code of its own. What C#
forbids is code under one label that runs on into the next.

---

## Worked example 3: when there is no default

```csharp
static string ShiftName(int shift) => shift switch
{
    1 => "first",
    2 => "second",
    3 => "third",
};

Console.WriteLine(ShiftName(2));
Console.WriteLine(ShiftName(4));
```

The build succeeds with a warning:

```
w12wed_e_not_exhaustive.cs(3,45): warning CS8509: The switch expression does not handle all possible values of its input type (it is not exhaustive). For example, the pattern '0' is not covered.
```

It prints `second`, then throws:

```
Unhandled exception. System.Runtime.CompilerServices.SwitchExpressionException: Non-exhaustive switch expression failed to match its input.
```

A switch expression must produce a value, so it cannot quietly do nothing. Python's `match` with no
matching case does exactly that: it skips to the next line with no error. Add a `_` arm and decide
what an unknown shift means.

---

## The wrong version, and the error it produces

Arms in the wrong order, with constant limits:

```csharp
static string Classify(double tempC) => tempC switch
{
    >= 215 => "warning",
    >= 240 => "alarm",
    _ => "normal",
};
```

```
w12wed_b_arm_order_constant.cs(5,5): error CS8510: The pattern is unreachable. It has already been handled by a previous arm of the switch expression or it is impossible to match.
```

Every value at or above 240 is also at or above 215, so the second arm can never win. The compiler
can prove it, because both limits are constants.

Two habits from other languages:

```
w12wed_d_fall_through.cs(5,5): error CS0163: Control cannot fall through from one case label ('case 1:') to another
w12wed_f_python_match.cs(3,14): error CS1002: ; expected
w12wed_f_python_match.cs(4,2): error CS1003: Syntax error, 'switch' expected
w12wed_f_python_match.cs(7,2): error CS1513: } expected
```

The first is a case with code and no `break`. The second is Python's `match (shift)`, which C# reads
as a call to a method named `match`, and then gets lost.

---

## The wrong version the compiler cannot catch

**This is the most important example in the lesson.** The same wrong order, with limits read from
settings:

```csharp
double warnAtC = 215;
double alarmAtC = 240;

string Classify(double tempC) => tempC switch
{
    var t when t >= warnAtC => "warning",
    var t when t >= alarmAtC => "alarm",
    _ => "normal",
};

Console.WriteLine(Classify(250));
Console.WriteLine(Classify(220));
```

It builds with 0 warnings. Output:

```
warning
warning
```

250 degrees is an alarm, and the panel says warning. The limits are variables, so the compiler cannot
prove the second arm unreachable: somebody could set `alarmAtC` below `warnAtC`. Python's `if` and
`elif` in the same order prints `warning` too.

The fix is the order: the most urgent test first.

---

## Why the wrong version is tempting

Thresholds are usually written smallest first, the way you would list them in a table. Reading down
the arms, each one looks correct on its own. And a real panel reads its thresholds from a settings
file, which is exactly the case the compiler cannot check.

The habit that prevents it: read the arms top to bottom with the most extreme value in hand, and
write a test for a value above the highest limit.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Selection control structure** | The exam's name for `if`, `switch`, and `case` |
| **Switch statement** | Runs the block for the matching case |
| **Switch expression** | Produces a value from the first matching arm |
| **Arm** | One `pattern => result` line in a switch expression |
| **Relational pattern** | `>= 240`, `< 20`: a comparison used as a pattern |
| **`when` clause** | An extra condition on an arm, which can use variables |
| **Discard `_`** | The arm that matches anything left |
| **Exhaustive** | Covers every possible input. The compiler warns when it is not |
| **`enum`** | A type with a fixed set of named values |

---

## Self-check

**Question 1.** Write a switch expression that turns a battery percent into `"error"` below 0 or above
100, `"full"` above 80, `"ok"` from 20 to 80, `"low"` above 0, and `"empty"` otherwise.

**Question 2.** Why does the compiler refuse the wrong arm order with `>= 215` and `>= 240`, but
accept it with `when t >= warnAtC` and `when t >= alarmAtC`?

**Question 3.** A classmate's switch statement puts `Console.WriteLine` under `case 1:` with no
`break`, and the build fails. They say C# is being fussy. What bug does the rule prevent?

---

### Answers

**1.**

```csharp
static string BatteryIcon(int percent) => percent switch
{
    < 0 or > 100 => "error",
    > 80 => "full",
    >= 20 => "ok",
    > 0 => "low",
    _ => "empty",
};
```

Verified as Gate 1 Rep 18: 100 and 81 are full, 80 and 20 are ok, 19 and 1 are low, 0 is empty, and
-5 and 130 are errors. The error arm comes first so no later arm can claim 130.

**2.** With constants, the compiler can prove every value at or above 240 was already taken by the
first arm. With variables, the limits are only known when the program runs, and the compiler cannot
rule out a settings file where the alarm limit is lower than the warning limit.

**3.** Accidental fall-through: in languages that allow it, forgetting one `break` runs the next
case's code too, which is a bug that builds, runs, and looks almost right. C# makes every case end
on purpose.
