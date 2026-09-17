# Lecture Notes: The Compiler Enforces Who May Touch What
## 145065 Object-Oriented Programming · Unit 6 · Week 12, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W12_AccessModifiers.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W12_AccessModifiers.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK.

**Competencies:** 5.3.12 classes, objects, and methods · 5.5.5 naming conventions and comments.

Every output and error below was printed by a real build: .NET SDK 10.0.401, `net8.0`. Python
outputs are from Python 3.13.7.

---

## Why this exists

In Unit 1 you learned Python's underscore: `_running` means "please do not touch." Python does not
enforce it. `press._running = True` works, and a press can report running with its guard open while
no safety rule ever ran.

That is the dangerous design that works today. Every test passes, because the tests use the class
correctly. The damage comes from the one caller who does not.

C# enforces the request. You decide who may touch each member, and the compiler refuses everyone
else, before the program runs.

---

## The concept in plain language

| Modifier | Who may use it | Python's closest habit |
|---|---|---|
| `public` | Anyone. This is the class's contract | a plain name |
| `private` | This class only. **Subclasses are locked out too** | `_name`, or `__name` |
| `protected` | This class and its subclasses | `_name`, by agreement |
| `internal` | Any code in the same project (assembly) | `_module.py`, by agreement |

A property can have two different levels:

```csharp
public bool IsRunning { get; private set; }
```

Anyone can **read** `IsRunning`. Only code inside the class can **change** it. A property with no
`set` at all can be assigned only in a constructor.

If you write no modifier, a class member is `private`. Write it anyway. The next reader should not
have to remember the default.

---

## Worked example 1: every modifier, chosen on purpose

```csharp
var press = new Press("L3-PRS-01");
press.CloseGuard();
press.Start();
Console.WriteLine($"{press.AssetTag} running: {press.IsRunning}");
press.LockOut("tech-07");
Console.WriteLine($"locked out by {press.LockedOutBy}, running: {press.IsRunning}");

abstract class PoweredEquipment
{
    private string? _lockoutHolder;

    protected PoweredEquipment(string assetTag) => AssetTag = assetTag;

    public string AssetTag { get; }
    public bool IsRunning { get; private set; }
    public string? LockedOutBy => _lockoutHolder;

    public virtual void Start()
    {
        if (_lockoutHolder is not null)
        {
            throw new InvalidOperationException($"{AssetTag} is locked out");
        }
        IsRunning = true;
    }

    public void Stop() => IsRunning = false;

    public void LockOut(string badge)
    {
        Stop();
        _lockoutHolder = badge;
    }

    protected bool CanRun() => _lockoutHolder is null;
}

sealed class Press : PoweredEquipment
{
    public Press(string assetTag) : base(assetTag) { }

    public bool GuardClosed { get; private set; }

    public void CloseGuard() => GuardClosed = true;

    public override void Start()
    {
        if (!GuardClosed)
        {
            throw new InvalidOperationException($"{AssetTag} guard is open");
        }
        base.Start();
    }
}
```

Output:

```
L3-PRS-01 running: True
locked out by tech-07, running: False
```

Say each choice out loud. `_lockoutHolder` is `private`: not even `Press` may clear a lockout.
`IsRunning` has a `private set`: the only ways to change it are `Start()` and `Stop()`, where the
rules live. The constructor is `protected`: only a subclass calls it. `CanRun()` is `protected`: a
helper for subclasses, not part of the public contract.

---

## Worked example 2: four refusals, four messages

Each line below is a separate program, trying to go around the class.

```csharp
press.IsRunning = true;          // setter is private
press.AssetTag = "L3-PRS-99";    // no setter at all
press._lockoutHolder = null;     // private field
press.CanRun();                  // protected method, called from outside
```

```
w12mon_b_private_set_outside.cs(3,1): error CS0272: The property or indexer 'Press.IsRunning' cannot be used in this context because the set accessor is inaccessible
w12mon_c_get_only.cs(3,1): error CS0200: Property or indexer 'Press.AssetTag' cannot be assigned to -- it is read only
w12mon_d_private_field.cs(3,7): error CS0122: 'PoweredEquipment._lockoutHolder' is inaccessible due to its protection level
w12mon_e_protected_outside.cs(3,25): error CS0122: 'PoweredEquipment.CanRun()' is inaccessible due to its protection level
```

And a subclass trying to read its parent's private field:

```csharp
class Press : PoweredEquipment
{
    public string? Holder() => _lockoutHolder;
}
```

```
w12mon_d_private_field.cs(12,32): error CS0122: 'PoweredEquipment._lockoutHolder' is inaccessible due to its protection level
```

Python's name mangling blocked `self.__lockout_holder` in a subclass too, but only the plain name.
`press._PoweredEquipment__lockout_holder = None` still worked. C# has no back door.

---

## Worked example 3: the same line from another project

**This surprises everyone once.** In Lab U06-03, `Intruder` is a separate project that uses the
`Line3.Monitor` library. After `Reading` is locked down with get-only properties:

```
Program.cs(12,1): error CS0200: Property or indexer 'Reading.Value' cannot be assigned to -- it is read only
Program.cs(13,1): error CS0200: Property or indexer 'Reading.SensorId' cannot be assigned to -- it is read only
Program.cs(14,1): error CS0200: Property or indexer 'Reading.Sequence' cannot be assigned to -- it is read only
```

A `private set` also shows up as CS0200 from another project. The compiler reports only what the
caller is allowed to see, and from outside, a property with a private setter looks read only. Inside
the same project, the compiler can see the setter exists, so it says CS0272 instead.

An `internal` class, used from another project:

```csharp
Console.WriteLine(Checks.IsFinite(reading.Value));
```

```
Program.cs(4,19): error CS0122: 'Checks' is inaccessible due to its protection level
```

`Checks` is public to every file in `Line3.Monitor` and invisible to everyone else.

---

## The wrong version, and why it is worse than an error

```csharp
var oven = new LeakyOven();
oven.MaxC = 240;
oven.TemperatureC = double.NaN;
Console.WriteLine($"Over maximum: {oven.IsOverMaximum}");
oven.TemperatureC = 500;
oven.MaxC = 9999;
Console.WriteLine($"Over maximum: {oven.IsOverMaximum}");

class LeakyOven
{
    public double TemperatureC;
    public double MaxC;

    public bool IsOverMaximum => TemperatureC > MaxC;
}
```

Output:

```
Over maximum: False
Over maximum: False
```

It builds with 0 warnings. An oven at 500 degrees reports that it is fine, because somebody raised
the maximum. NaN compares false against everything, so it reports fine too. The Python version of
this class prints the same two lines. **Public fields turn every caller into a co-author of your
rules.**

---

## Why the wrong version is tempting

Public fields are one line each, and every test you write uses the class correctly, so every test
passes. Python taught you that the underscore is enough, because in a small program you are the
only caller.

The habit that prevents it: start every member as `private`, and make it more visible only when a
caller needs it. When you do, write down why.

---

## Naming, and what the modifiers tell a reader (5.5.5)

| Kind | Convention | Example |
|---|---|---|
| Private field | `_camelCase` | `_lockoutHolder` |
| Property, method, class | `PascalCase` | `IsRunning`, `LockOut`, `PoweredEquipment` |
| Parameter, local variable | `camelCase` | `assetTag`, `badge` |
| Interface | `I` plus `PascalCase` | `IReadingSource` |

The underscore in C# is a naming convention that matches the modifier. It is not the protection.
The `private` keyword is.

A comment should say why a member has its access level when the reason is not obvious:

```csharp
// private, not protected: a subclass must not be able to clear a lockout.
private string? _lockoutHolder;
```

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Access modifier** | A keyword that says who may use a member: `public`, `private`, `protected`, `internal` |
| **Encapsulation** | Keeping an object's data and rules together, and letting others in only through the rules |
| **Accessor** | The `get` or `set` part of a property. Each can have its own modifier |
| **Get-only property** | A property with no `set`. Assignable only in a constructor |
| **Assembly** | The `.dll` or `.exe` one project builds. `internal` means "this assembly" |
| **Contract** | The public members of a class. What callers may rely on |

---

## Self-check

**Question 1.** Choose a modifier for each member of a `TipJar` class, and say why: the running
total, a method that adds a tip, a helper that checks an amount is positive, the list of every tip.

**Question 2.** The same assignment gives CS0272 in one program and CS0200 in another. What is
different about where the two lines live?

**Question 3.** A classmate says a private field is pointless because a subclass should be trusted.
Give the strongest reason for `private` using the lockout example, and one situation where
`protected` is the better choice.

---

### Answers

**1.** Total: `public decimal Total { get; private set; }`, so anyone can read it and only the class
can change it. Adding a tip: `public void Add(decimal amount)`, the one way in. The positive check:
`private`, because it is a detail of `Add`. The list: a `private` field, exposed, if at all, as a
read-only view, because a caller who can add to the list can skip the check.

**2.** CS0272 comes from code in the same project as the class, where the compiler can see that a
private setter exists. CS0200 comes from code in another project, where the setter is invisible and
the property looks read only.

**3.** For: `PoweredEquipment` promises that only the badge that locked a machine can release it. If
a subclass could clear `_lockoutHolder`, one careless subclass would break that promise for every
machine of its kind, and no test of the parent would notice. `protected` is better when the parent
is designed for subclasses to extend a step, such as a `protected` helper that every kind of
equipment needs and no outside caller should use.
