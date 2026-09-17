# Lecture Notes: Loops, With Types and Braces
## 145065 Object-Oriented Programming · Unit 6 · Week 11, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W11_Loops.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W11_Loops.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK.

**Competency:** 5.3.6 write code that uses repetition control structures (`while`, `for`).

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`. Python outputs are from
Python 3.13.7.

---

## Why this exists

Every summary on an operator panel is a loop: the average of the last hour, the first reading over a
limit, how long the oven has been steady. You have written all of these in Python. Today you write
them in C#, and you meet the two rules Python never had: a loop's condition must be a real `bool`,
and a variable born inside a loop's braces dies at the closing brace.

---

## The concept in plain language

C# has four loops. They are the same ideas you already use.

| Python | C# | Use it when |
|---|---|---|
| `for i in range(n):` | `for (int i = 0; i < n; i++) { }` | You need the position number |
| `for x in items:` | `foreach (double x in items) { }` | You need each item, not its position |
| `while condition:` | `while (condition) { }` | You stop on a condition, not a count |
| no direct equivalent | `do { } while (condition);` | The body must run at least once |

What the compiler checks in every loop: the loop variable has a type, the condition is a `bool`, and
nothing outside the braces uses a variable declared inside them. What it does not check: whether an
index is inside the array.

---

## Worked example 1: four loops over the same readings

```csharp
double[] temps = { 199.2, 212.5, 216.0, 208.1 };

for (int i = 0; i < temps.Length; i++)
{
    Console.WriteLine($"for: minute {i + 1} is {temps[i]}");
}

int over = 0;
foreach (double t in temps)
{
    if (t > 210)
    {
        over++;
    }
}
Console.WriteLine($"foreach: {over} readings above 210");

int minute = 0;
while (minute < temps.Length && temps[minute] < 215)
{
    minute++;
}
Console.WriteLine($"while: first reading at or above 215 is index {minute}");

int tries = 0;
do
{
    tries++;
    Console.WriteLine($"do: attempt {tries}");
} while (tries < 0);
```

Output:

```
for: minute 1 is 199.2
for: minute 2 is 212.5
for: minute 3 is 216
for: minute 4 is 208.1
foreach: 2 readings above 210
while: first reading at or above 215 is index 2
do: attempt 1
```

Three details. `i++` adds one to `i`. `216.0` prints as `216` because a `double` prints its shortest
form. The `do` loop ran once even though `tries < 0` was false from the start.

The `while` condition checks `minute < temps.Length` **first**. `&&` stops as soon as its left side
is false, so the array is never read at an index that does not exist.

---

## Worked example 2: skipping and stopping

A reading can be missing. `double?` holds a number or `null`.

```csharp
double?[] readings = { 201.0, null, 207.5, 243.0, 205.0 };
foreach (double? reading in readings)
{
    if (reading is null)
    {
        Console.WriteLine("missing, skipped");
        continue;
    }
    if (reading > 240)
    {
        Console.WriteLine($"{reading} is above maximum, stop reading");
        break;
    }
    Console.WriteLine($"{reading} ok");
}
```

Output:

```
201 ok
missing, skipped
207.5 ok
243 is above maximum, stop reading
```

`continue` skips to the next reading. `break` leaves the loop, so 205.0 is never printed. Both work
exactly as in Python.

---

## Worked example 3: nested loops

```csharp
string[] cells = { "Forming", "Finishing", "Staging" };
int[] machines = { 2, 0, 3 };
int checks = 0;
for (int c = 0; c < cells.Length; c++)
{
    if (machines[c] == 0)
    {
        continue;
    }
    for (int m = 1; m <= machines[c]; m++)
    {
        checks++;
        if (m == 2)
        {
            break;
        }
    }
    Console.WriteLine($"{cells[c]}: {checks}");
}
Console.WriteLine(checks);
```

Output:

```
Forming: 2
Staging: 4
4
```

`break` leaves only the inner loop. Finishing has no machines, so `continue` skips its whole pass,
including its `WriteLine`. Staging has 3 machines, and the inner loop stops at the second.

---

## The wrong versions, and the errors they produce

**A running total with no starting value.**

```csharp
double[] temps = { 196.5, 198.0, 199.2 };
double total;
foreach (double reading in temps)
{
    total += reading;
}
```

```
lab01_g_unassigned_total.cs(6,5): error CS0165: Use of unassigned local variable 'total'
```

`total += reading` reads `total` before it has a value. Write `double total = 0;`.

**A number where a condition belongs.** The Python habit `while remaining:`:

```csharp
int remaining = 3;
while (remaining)
{
    remaining--;
}
```

```
w11wed_e_condition_not_bool.cs(3,8): error CS0029: Cannot implicitly convert type 'int' to 'bool'
```

C# has no "truthy" numbers. Write `while (remaining > 0)`.

**A variable used after its loop.**

```csharp
foreach (double t in temps)
{
    double fahrenheit = t * 9 / 5 + 32;
}
Console.WriteLine(fahrenheit);
```

```
w11wed_b_loop_scope.cs(7,19): error CS0103: The name 'fahrenheit' does not exist in the current context
```

Python prints `420.8` for the same code, the last value, because Python has no block scope. In C#,
declare the variable before the loop if you need it after.

**The Python `for` loop.**

```csharp
for (int i in range(3))
```

```
w11wed_d_python_range.cs(2,1): error CS1003: Syntax error, 'foreach' expected
```

The compiler saw `in` and guessed you meant `foreach`. It was half right: you meant a counting loop.

**Changing the loop variable of a `foreach`.**

```csharp
foreach (double reading in temps)
{
    reading = reading * 9 / 5 + 32;
}
```

```
lab01_i_foreach_assign.cs(5,5): error CS1656: Cannot assign to 'reading' because it is a 'foreach iteration variable'
```

---

## The wrong version the compiler does not catch

```csharp
double[] temps = { 196.5, 198.0, 199.2 };
for (int i = 0; i <= temps.Length; i++)
{
    Console.WriteLine($"Minute {i + 1}: {temps[i]}");
}
```

It builds with 0 warnings. It prints three lines and then:

```
Minute 1: 196.5
Minute 2: 198
Minute 3: 199.2
Unhandled exception. System.IndexOutOfRangeException: Index was outside the bounds of the array.
```

An array of 3 has indexes 0, 1, and 2. `<=` asks for index 3. Python fails the same way with
`range(len(temps) + 1)`: `IndexError: list index out of range`. Neither language checks array
bounds before running.

---

## Why the wrong versions are tempting

`<=` reads naturally when you think "up to the length." `while remaining:` is correct Python you have
written a hundred times. And Python's loop variables really do survive the loop, so using one
afterward has never failed you before.

The habits that prevent them: write `i < array.Length` every time without thinking, give every
running total a starting value on the line that declares it, and declare a variable at the level
where you need it.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Repetition control structure** | The exam's name for a loop |
| **`for`** | A counting loop: start, condition, step |
| **`foreach`** | A loop over every item in a collection |
| **`while`** | A loop that checks its condition before each pass |
| **`do ... while`** | A loop that checks its condition after each pass, so it runs at least once |
| **Scope** | The part of the program where a name exists. In C#, a pair of braces |
| **Definite assignment** | C#'s rule that a local variable must have a value before it is read |
| **Short-circuit** | `&&` and `\|\|` stop as soon as the answer is known |

---

## Self-check

**Question 1.** Translate to C#, with types:

```python
total = 0
for steps in steps_per_day:
    if steps > 10000:
        total += 1
print(total)
```

**Question 2.** Why does `while (i < temps.Length && temps[i] < 215)` never throw, while
`while (temps[i] < 215 && i < temps.Length)` can?

**Question 3.** A `for` loop builds with 0 warnings and throws `IndexOutOfRangeException` on its last
pass. What is the most likely cause, and why could the compiler not warn you?

---

### Answers

**1.**

```csharp
int total = 0;
foreach (int steps in stepsPerDay)
{
    if (steps > 10000)
    {
        total++;
    }
}
Console.WriteLine(total);
```

`total` is given its starting value where it is declared, the loop variable has a type, and the name
becomes `stepsPerDay` in C# style.

**2.** `&&` evaluates left to right and stops when the left side is false. In the first version, the
index is checked before the array is read. In the second, the array is read first, so when `i`
reaches the length the read throws before the index check can stop it.

**3.** The condition uses `<=` where it needs `<`, so the loop asks for the index equal to the
length. The compiler cannot warn because an array's length is only known when the program runs.
