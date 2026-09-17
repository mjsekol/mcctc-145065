# Lecture Notes: Every Value Has a Type, and Arithmetic Follows the Types
## 145065 Object-Oriented Programming · Unit 6 · Week 11, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W11_StaticTypes.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W11_StaticTypes.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK.

**Competencies:** 5.2.1 primitive numeric and nonnumeric types · 5.2.3 arithmetic operations ·
2.3.2 convert between binary, hexadecimal, and decimal.

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`. Python outputs are from
Python 3.13.7.

---

## Why this exists

In Python, a name can point at a number today and a string tomorrow. You checked types by hand when
it mattered, with `isinstance`. The plant model in Unit 2 had a whole helper, `require_number`, for
that job.

In C#, the compiler does that job. Every variable has one type, fixed when the program is compiled.
That removes a whole family of bugs. It also creates one you have never met: arithmetic that happens
in the wrong type and gives a wrong answer with no error at all. This lesson is about both.

---

## The concept in plain language

**A C# variable has one type, forever.** You write it, or you write `var` and the compiler works it
out from the first value. Either way, it never changes.

**Arithmetic is done in the types of the values, not the type of the variable you store it in.**
`int / int` is integer division, which throws the fraction away. Storing the answer in a `double`
happens after the division, so it is too late to help.

### The types you will use

| C# type | Holds | Python equivalent | Example |
|---|---|---|---|
| `int` | whole numbers, about plus or minus 2.1 billion | `int` (no limit) | `int strokes = 1250;` |
| `long` | much larger whole numbers | `int` | `long total = 9_000_000_000;` |
| `double` | numbers with fractions, approximately | `float` | `double tempC = 212.4;` |
| `decimal` | exact decimal fractions, for money | `decimal.Decimal` | `decimal rate = 18.50m;` |
| `bool` | `true` or `false` | `bool` | `bool running = true;` |
| `char` | exactly one character, single quotes | a one-letter `str` | `char shift = 'B';` |
| `string` | text, double quotes | `str` | `string tag = "L3-PRS-01";` |
| `double?` | a `double`, or `null` for "no value" | `float` or `None` | `double? reading = null;` |

---

## Worked example 1: the same digits, different answers

```csharp
Console.WriteLine(7 / 2);
Console.WriteLine(7 / 2.0);
Console.WriteLine(7 % 2);
Console.WriteLine(-7 / 2);
Console.WriteLine(0.1 + 0.2);
Console.WriteLine(0.1m + 0.2m);
Console.WriteLine((int)212.9);
Console.WriteLine(Math.Round(212.5));
Console.WriteLine(Math.Round(213.5));
```

Output:

```
3
3.5
1
-3
0.30000000000000004
0.3
212
212
214
```

Line by line: two `int`s divide as integers. One `double` makes the whole division a `double`. `%` is
the remainder. `-7 / 2` is `-3` because C# truncates toward zero, where Python's `-7 // 2` is `-4`.
`double` is approximate, `decimal` (the `m` suffix) is exact. A cast to `int` chops the fraction off.
`Math.Round` sends a half to the nearest even number, the same as Python's `round()`.

---

## Worked example 2: one value, three spellings (2.3.2)

You converted bases by hand in 145060. C# writes the same value three ways.

```csharp
int statusWord = 0x2C;
int alsoStatus = 0b0010_1100;
Console.WriteLine(statusWord);
Console.WriteLine(statusWord == alsoStatus);
Console.WriteLine(statusWord.ToString("X"));
Console.WriteLine(statusWord.ToString("X4"));
Console.WriteLine(Convert.ToString(statusWord, 2));
Console.WriteLine(Convert.ToString(statusWord, 2).PadLeft(8, '0'));
Console.WriteLine(Convert.ToInt32("2C", 16));
Console.WriteLine(Convert.ToInt32("101100", 2));
```

Output:

```
44
True
2C
002C
101100
00101100
44
44
```

`0x` starts a hexadecimal literal and `0b` a binary one, exactly as in Python. The underscore is
only for your eyes. The value is 44 however it is written: 2 sixteens plus 12 is 44, and
32 + 8 + 4 is 44.

---

## Worked example 3: an int has a top

Python integers grow as large as memory allows. A C# `int` stops at 2,147,483,647.

```csharp
int strokes = int.MaxValue;
Console.WriteLine(strokes);
strokes = strokes + 1;
Console.WriteLine(strokes);
long bigStrokes = int.MaxValue;
bigStrokes = bigStrokes + 1;
Console.WriteLine(bigStrokes);
int checkedStrokes = int.MaxValue;
checkedStrokes = checked(checkedStrokes + 1);
```

Output:

```
2147483647
-2147483648
2147483648
Unhandled exception. System.OverflowException: Arithmetic operation resulted in an overflow.
```

Adding one wrapped around to the most negative `int`, silently. `long` has room. `checked` turns
the silent wrap into an exception you can see. A press stroke counter that wraps to a negative
number would report the press as brand new.

---

## The wrong version, and the error it produces

The Python habit: a name that changes type.

```csharp
var partsMade = 1250;
partsMade = "twelve hundred fifty";
```

```
w11tue_a_type_is_forever.cs(3,13): error CS0029: Cannot implicitly convert type 'string' to 'int'
```

`var` made `partsMade` an `int` on the first line. Python runs the same two lines without a word.

Two more the compiler refuses:

```csharp
bool running = 1;
char shift = "B";
```

```
w11tue_c_bool_is_not_int.cs(2,16): error CS0029: Cannot implicitly convert type 'int' to 'bool'
w11tue_c_bool_is_not_int.cs(3,14): error CS0029: Cannot implicitly convert type 'string' to 'char'
```

And the one with a hint you should not always take:

```csharp
double total = 6184.6;
int average = total / 30;
```

```
lab01_f_double_into_int.cs(3,15): error CS0266: Cannot implicitly convert type 'double' to 'int'. An explicit conversion exists (are you missing a cast?)
```

The compiler suggests a cast. A cast chops the fraction off. Most of the time the right fix is to
make `average` a `double`, not to throw the fraction away.

---

## The wrong version that the compiler does not catch

**This is the most important example in the lesson.**

```csharp
int runMinutes = 437;
int scheduledMinutes = 480;
double uptimePercent = runMinutes / scheduledMinutes * 100;
Console.WriteLine(uptimePercent);
```

Output:

```
0
```

No error. No warning. The same line in Python:

```python
run_minutes = 437
scheduled_minutes = 480
print(run_minutes / scheduled_minutes * 100)
```

```
91.04166666666667
```

In Python 3, `/` always gives a float. In C#, `437 / 480` is integer division, which is `0`. Then
`0 * 100` is `0`, and only then is `0` stored in the `double`.

The fix: make the arithmetic a `double` before the division happens.

```csharp
double fixedPercent = runMinutes * 100.0 / scheduledMinutes;
Console.WriteLine(fixedPercent);
```

```
91.04166666666667
```

---

## Why the wrong version is tempting

Your Python was correct. `run / scheduled * 100` is the right formula, and you have written it
correctly for a year. Nothing about the line looks wrong, and declaring the result as `double`
feels like it should be enough. It is a correct habit carried into a language with different rules,
and the compiler cannot tell that you meant a fraction.

The habit that prevents it: whenever you divide, say the types of both sides out loud. If both are
whole numbers, ask whether you want a whole-number answer.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Static typing** | Every variable's type is fixed when the program is compiled |
| **`var`** | "Compiler, work out the type from the first value." Still one type forever |
| **Integer division** | Division of two whole-number types. The fraction is thrown away |
| **Implicit conversion** | A conversion C# does for you because nothing can be lost, such as `int` to `double` |
| **Cast** | An explicit conversion you ask for, such as `(int)212.9`. It can lose information |
| **Overflow** | A result too big for its type. An `int` wraps around unless the code says `checked` |
| **Literal** | A value written in the code: `44`, `0x2C`, `0b0010_1100`, `18.50m`, `'B'`, `"B"` |
| **Nullable value type** | `double?`, `int?`: the type plus `null` for "no value" |

---

## Self-check

**Question 1.** What does each line print?

```csharp
Console.WriteLine(1250 / 48);
Console.WriteLine(1250 % 48);
Console.WriteLine(1250 / 48.0 > 26);
```

**Question 2.** `double averageMinutesLate = totalMinutes / days;` where both are `int`, total is 9
and days is 4. What is stored, why, and what is the fix?

**Question 3.** Convert `0b1111_0000` to decimal and to hexadecimal, then write the C# line that
prints it in hexadecimal.

---

### Answers

**1.** `26`, then `2`, then `True`. 48 times 26 is 1,248, so the remainder is 2. With `48.0` the
division is a `double`, about 26.04, which is more than 26.

**2.** `2` is stored. `9 / 4` is integer division, which is `2`, and the `double` receives `2` after
the division is over. Fix: `double averageMinutesLate = (double)totalMinutes / days;` or
`totalMinutes * 1.0 / days`, which gives `2.25`.

**3.** 128 + 64 + 32 + 16 is 240. In hexadecimal, `1111` is F and `0000` is 0, so `F0`.
`Console.WriteLine(0b1111_0000.ToString("X"));` prints `F0`.
