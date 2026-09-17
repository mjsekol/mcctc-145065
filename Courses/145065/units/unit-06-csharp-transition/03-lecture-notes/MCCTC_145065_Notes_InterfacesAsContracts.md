# Lecture Notes: An Interface Is a Contract the Compiler Checks
## 145065 Object-Oriented Programming · Unit 6 · Week 12, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W12_Interfaces.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W12_Interfaces.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK.

**Competencies:** 5.3.12 classes, objects, and methods · 5.1.4 object-oriented programming ·
5.1.6 strengths and weaknesses of different approaches and languages.

Every output and error below was printed by a real build: .NET SDK 10.0.401, `net8.0`. Python
outputs are from Python 3.13.7.

---

## Why this exists

In Unit 2, the line inspected every machine with one loop: `for item in line: item.inspect()`. That
worked because every class happened to have an `inspect()` method. Nothing guaranteed it. A new
class without one worked fine until the loop reached it, and then it crashed, sometimes after half
the line was already done.

The HMI panel in Unit 8 reads readings from a simulator today and a real Raspberry Pi later. The
panel code should not care which. An interface is how you write code that works with "anything that
provides readings," and get the compiler to guarantee that everything you hand it really does.

---

## The concept in plain language

An **interface** is a list of members with no code inside them:

```csharp
interface IReadingSource
{
    string Name { get; }
    double? Next();
}
```

A class that names the interface **promises** to supply every member, with the same types:

```csharp
sealed class ScriptedSource : IReadingSource
```

If it misses one, or gets a type wrong, the build fails.

Code written against the interface works with **any** class that keeps the promise, including one
written next year. Through a variable of the interface type, you see only what the interface lists.

| Python, Unit 2 | C# | What changed |
|---|---|---|
| "Every class has `inspect()`," a habit | `interface IInspectable { ... }` | The promise has a name and a checker |
| A missing method fails when the loop reaches it | CS0535 at build time | Found before any machine starts |
| One base class for shared code and shared promise | An interface for the promise, a base class only if code is shared | A class can keep several promises, and have only one parent |

---

## Worked example 1: one contract, two very different implementations

```csharp
IReadingSource[] sources =
{
    new ScriptedSource("bench script", new double?[] { 201.5, null, 214.0 }),
    new TextLineSource("pasted log", "oven-temp,212.4\noven-temp,oops\noven-temp,219.0"),
};

foreach (IReadingSource source in sources)
{
    Console.WriteLine(source.Name);
    for (int i = 0; i < 3; i++)
    {
        double? value = source.Next();
        Console.WriteLine(value is double v ? $"  {v}" : "  missing");
    }
}

interface IReadingSource
{
    string Name { get; }
    double? Next();
}

sealed class ScriptedSource : IReadingSource
{
    private readonly double?[] _values;
    private int _index;

    public ScriptedSource(string name, double?[] values)
    {
        Name = name;
        _values = values;
    }

    public string Name { get; }

    public double? Next() => _index < _values.Length ? _values[_index++] : null;
}

sealed class TextLineSource : IReadingSource
{
    private readonly string[] _lines;
    private int _index;

    public TextLineSource(string name, string text)
    {
        Name = name;
        _lines = text.Split('\n');
    }

    public string Name { get; }

    public double? Next()
    {
        if (_index >= _lines.Length)
        {
            return null;
        }
        string[] parts = _lines[_index++].Split(',');
        return parts.Length == 2 && double.TryParse(parts[1], out double value) ? value : null;
    }
}
```

Output:

```
bench script
  201.5
  missing
  214
pasted log
  212.4
  missing
  219
```

The loop never asks what kind of source it has. One replays a list. The other parses text and turns
a line it cannot read into a missing value, never a zero. `value is double v` checks for a value and
unwraps it in one step.

(Lab U06-03 builds the full version, where `Next()` returns a `Reading` object, parses with
`CultureInfo.InvariantCulture`, and refuses NaN and infinity. This example keeps the idea small.)

---

## Worked example 2: what you can see through the interface

`ScriptedSource` has an extra method, `Rewind()`. Through the interface, it does not exist.

```csharp
IReadingSource source = new ScriptedSource();
source.Rewind();
```

```
w12tue_c_interface_hides_extras.cs(3,8): error CS1061: 'IReadingSource' does not contain a definition for 'Rewind' and no accessible extension method 'Rewind' accepting a first argument of type 'IReadingSource' could be found (are you missing a using directive or an assembly reference?)
```

That is a feature. Code that holds an `IReadingSource` can only use what every source promised, so it
keeps working when someone swaps in a source that cannot rewind, such as a live sensor.

---

## Worked example 3: an interface is not an object

```csharp
IReadingSource source = new IReadingSource();
```

```
w12tue_d_new_interface.cs(2,25): error CS0144: Cannot create an instance of the abstract type or interface 'IReadingSource'
```

An interface has no code to run. You always build a class that keeps it.

---

## The wrong versions, and the errors they produce

**A class that promises and skips a member.**

```csharp
sealed class ScriptedSource : IReadingSource
{
    public string Name => "bench script";
}
```

```
w12tue_b_missing_member.cs(9,31): error CS0535: 'ScriptedSource' does not implement interface member 'IReadingSource.Next()'
```

Python, for the same mistake, runs until the loop reaches that object:

```
bench script
AttributeError: 'ScriptedSource' object has no attribute 'next'
```

**A class that promises less than the contract says.**

```csharp
sealed class ScriptedSource : IReadingSource
{
    public double Next() => 201.5;
}
```

```
w12tue_e_wrong_return_type.cs(8,31): error CS0738: 'ScriptedSource' does not implement interface member 'IReadingSource.Next()'. 'ScriptedSource.Next()' cannot implement 'IReadingSource.Next()' because it does not have the matching return type of 'double?'.
```

The contract said "a reading that may be missing." A `double` cannot say "missing," so it does not
keep the promise, even though every value it returns is a valid `double?`.

---

## Why the wrong versions are tempting

The class you are writing today only needs some of the members, so the rest feel optional. And
`double` looks like it should be close enough to `double?`, because in Python `None` and a float
travel through the same variable.

The habit that prevents it: write the class declaration line with the interface first, build, and
let the CS0535 list tell you exactly what is left to write.

---

## Designing a good interface

An interface should promise **only what every implementation can keep.** A panel's reading source
can say its name and give its next reading. A scripted source also knows how many readings remain.
A live sensor does not. If `Remaining` goes into the interface, the live sensor has two bad choices:
invent a number, or throw `NotSupportedException` at run time, which is the crash the interface was
supposed to prevent.

**The strengths and the costs (5.1.6).**

| | Interface | Base class |
|---|---|---|
| Shares a promise | yes | yes |
| Shares code | no | yes |
| How many per class | as many as you like | one |
| When it is the right tool | unrelated classes that answer the same question | a real "is a" with shared code |

Python can say something similar with `typing.Protocol` or `abc.ABC`. The difference is when the
check happens: C# checks every class at build time, whether or not the code that uses it ever runs.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Interface** | A named list of members with no code. A contract |
| **Implement** | To supply every member an interface lists: `class X : IName` |
| **Contract** | What callers may rely on. An interface makes it explicit and checked |
| **Polymorphism** | One call, many implementations. The loop above calls `Next()` on both sources |
| **`is` pattern** | `value is double v` tests a type and names the result in one step |
| **Program to the interface** | Declare variables and parameters as the interface type, not a class |

---

## Self-check

**Question 1.** Write an interface `IFare` with a `Name` and a method that returns the price for a
number of rides, then write two classes that implement it with different prices.

**Question 2.** Why does `double Next()` not implement `double? Next()`, when every `double` can be
stored in a `double?`?

**Question 3.** A teammate wants to add `void Reset()` to `IReadingSource` so the scripted source can
start over. Give the strongest argument against, and a way to get the feature without changing the
interface.

---

### Answers

**1.**

```csharp
interface IFare
{
    string Name { get; }
    decimal PriceFor(int rides);
}

sealed class StudentFare : IFare
{
    public string Name => "student";
    public decimal PriceFor(int rides) => rides * 1.00m;
}

sealed class AdultFare : IFare
{
    public string Name => "adult";
    public decimal PriceFor(int rides) => rides * 2.25m;
}
```

For 3 rides, these print `student: 3.00` and `adult: 6.75`. This is Gate 1 Rep 19.

**2.** The interface promises callers a type that can say "missing." A method that returns `double`
never can, so a caller who checks for `null` would be checking a promise the class does not make.
C# requires the return type to match exactly.

**3.** A live sensor cannot start over, so it would have to throw at run time, and every existing
class that implements the interface stops building until someone adds a `Reset` it may not be able
to keep. Put `Reset()` on `ScriptedSource` alone, where the code that builds a scripted source can
call it, or define a separate, narrower interface that only rewindable sources implement.
