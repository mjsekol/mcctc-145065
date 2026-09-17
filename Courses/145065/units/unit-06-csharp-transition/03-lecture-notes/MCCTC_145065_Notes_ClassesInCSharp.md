# Lecture Notes: A C# Class Declares Its Whole Shape Up Front
## 145065 Object-Oriented Programming · Unit 6 · Week 11, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W11_Classes.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W11_Classes.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK.

**Competencies:** 5.3.12 write code that creates classes, objects, and methods · 5.1.4 object-oriented
programming · 5.5.5 naming conventions and comments.

Every output and error below was printed by a real build: .NET SDK 10.0.401, `net8.0`.

---

## Why this exists

In Unit 2 you built a class hierarchy in Python: a base class, a middle class, concrete classes, and
one method every class answers its own way. Next Friday you hand in that hierarchy, ported to C#.
Today is the translation table you need to do it, and the reason C# asks you to write more of it
down.

---

## The concept in plain language

A Python object gets its attributes as `__init__` runs. Nothing lists them anywhere else. A C# class
**declares** everything first: its fields, its properties, its constructors, its methods, and its
parent. Then the compiler checks every use of the class against that declaration, before anything
runs.

### Side by side

| Python | C# | What changed |
|---|---|---|
| `class StorageRack(Equipment):` | `class StorageRack : Equipment` | Same idea |
| `def __init__(self, tag, name):` | `public StorageRack(string tag, string name)` | A constructor has the class's name and no return type |
| `super().__init__(tag, name)` | `: base(tag, name)` after the constructor's parameters | Checked: the parent's parameters must match |
| `self._load_kg = 0.0` | `private double _loadKg;` declared in the class | Declared once, with a type |
| `@property` with no setter | `public string Name { get; }` | Only a constructor can set it |
| `@property` plus `@load_kg.setter` | `public double LoadKg { get => ...; set { ... } }` | Validation goes in the `set` block |
| `class Equipment(ABC)` | `abstract class Equipment` | `new Equipment(...)` does not build |
| `@abstractmethod` | `public abstract string Kind { get; }` | A concrete subclass that skips it does not build |
| overriding by writing the same name | `virtual` in the parent, `override` in the child | Both sides must agree |
| `self.x` | `x`, or `this.x` when a parameter has the same name | No `self` parameter |
| `snake_case` | `PascalCase` for classes, methods, and properties; `camelCase` for parameters; `_camelCase` for private fields | 5.5.5, the C# naming conventions |

---

## Worked example 1: a two-level hierarchy

```csharp
var rack = new StorageRack("L3-RCK-01", "Finished Goods Rack", 1200);
rack.LoadKg = 1150;
Equipment item = rack;
Console.WriteLine(item.Describe());
Console.WriteLine(item.Kind);
rack.LoadKg = -5;

abstract class Equipment
{
    protected Equipment(string assetTag, string name)
    {
        AssetTag = assetTag;
        Name = name;
    }

    public string AssetTag { get; }
    public string Name { get; }
    public abstract string Kind { get; }

    public virtual string Describe() => $"{AssetTag} {Name} ({Kind})";
}

sealed class StorageRack : Equipment
{
    private double _loadKg;

    public StorageRack(string assetTag, string name, double capacityKg)
        : base(assetTag, name)
    {
        CapacityKg = capacityKg;
    }

    public double CapacityKg { get; }

    public double LoadKg
    {
        get => _loadKg;
        set
        {
            if (value < 0)
            {
                throw new ArgumentOutOfRangeException(nameof(LoadKg), "load cannot be negative");
            }
            _loadKg = value;
        }
    }

    public override string Kind => "rack";

    public override string Describe() => $"{base.Describe()}, {LoadKg * 100 / CapacityKg:F0}% full";
}
```

Output:

```
L3-RCK-01 Finished Goods Rack (rack), 96% full
rack
Unhandled exception. System.ArgumentOutOfRangeException: load cannot be negative (Parameter 'LoadKg')
```

Read it in Python terms. `item` is typed as `Equipment`, and `item.Describe()` still runs the rack's
version, because `Describe` is `virtual` and the rack overrides it. `base.Describe()` is
`super().describe()`. Inside `set`, the word `value` is whatever was assigned. The last line of the
program assigns `-5`, and the setter refuses it.

`=>` is a short way to write a method or property whose whole body is one expression.
`protected` means "this class and its subclasses." Monday of Week 12 is the whole story of access
modifiers. For today: `public` is anyone, `private` is this class only.

---

## Worked example 2: a Python class, ported line by line

The Python, from Lab U06-02:

```python
class Sensor:
    def __init__(self, sensor_id, kind, unit, low, high):
        self._sensor_id = sensor_id
        self._low = require_number(low, "low limit")
        self._high = require_number(high, "high limit")
        self._value = None

    @property
    def value(self):
        return self._value

    def record(self, value):
        self._value = require_number(value, f"{self._sensor_id} reading")

    def clear(self):
        self._value = None
```

The C# shape, trimmed to the same members:

```csharp
public class Sensor
{
    private double? _value;

    public Sensor(string id, double low, double high)
    {
        Id = id;
        Low = low;
        High = high;
    }

    public string Id { get; }
    public double Low { get; }
    public double High { get; }
    public double? Value => _value;

    public void Record(double value)
    {
        if (!double.IsFinite(value))
        {
            throw new ArgumentOutOfRangeException(nameof(value), value, "a reading must be a finite number");
        }
        _value = value;
    }

    public void Clear() => _value = null;
}
```

Three things disappeared: the `require_number` type check (the parameter is a `double`, so the
compiler already refuses text), `self`, and the separate `@property` decorator. One check stayed:
NaN and infinity are perfectly good `double` values, so `Record` still refuses them by hand.

---

## Worked example 3: what the compiler checks in a hierarchy

A subclass that forgets the abstract member:

```csharp
abstract class Equipment
{
    public abstract string Kind { get; }
}

sealed class Grinder : Equipment
{
}
```

```
w11thu_c_missing_abstract.cs(8,14): error CS0534: 'Grinder' does not implement inherited abstract member 'Equipment.Kind.get'
```

Building the abstract parent:

```
w11thu_e_new_abstract.cs(2,13): error CS0144: Cannot create an instance of the abstract type or interface 'Equipment'
```

Overriding a method the parent did not mark `virtual`:

```
w11thu_d_override_not_virtual.cs(10,28): error CS0506: 'Grinder.Describe()': cannot override inherited member 'Equipment.Describe()' because it is not marked virtual, abstract, or override
```

The parent's author decides what a subclass may change. In Python, any subclass could replace any
method, including one the parent's rules depended on.

---

## The wrong version, and the error it produces

The subclass constructor forgets `: base(...)`:

```csharp
sealed class StorageRack : Equipment
{
    public StorageRack(string assetTag, string name, double capacityKg)
    {
        CapacityKg = capacityKg;
    }

    public double CapacityKg { get; }
}
```

```
w11thu_b_missing_base.cs(17,12): error CS7036: There is no argument given that corresponds to the required parameter 'assetTag' of 'Equipment.Equipment(string, string)'
```

Read the message slowly. Without `: base(...)`, C# tries to call a parent constructor with no
arguments. `Equipment` has only the one that takes two strings, and the compiler names its first
parameter. The fix is the line you left out: `: base(assetTag, name)`.

The Python habits, each refused:

```
w11thu_h_self.cs(7,9): error CS0103: The name 'self' does not exist in the current context
w11thu_f_python_init.cs(9,9): error CS0200: Property or indexer 'Sensor.Id' cannot be assigned to -- it is read only
```

The second one comes from a method named `__init__`. C# builds it as an ordinary method. It is not
a constructor, so it may not set a get-only property.

---

## The wrong version the compiler only warns about

```csharp
var sensor = new Sensor();
Console.WriteLine(sensor.Id.ToUpper());

class Sensor
{
    public string Id { get; }
}
```

```
w11thu_g_property_never_set.cs(8,19): warning CS8618: Non-nullable property 'Id' must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring the property as nullable.
```

A warning, so it builds. It then throws `System.NullReferenceException` when it runs. Read your
warnings. Week 12, Thursday is about what a team does with them.

---

## Why the wrong versions are tempting

Python never needed `: base(...)` to be on a particular line, and forgetting `super().__init__()`
only failed later, somewhere else. `self.` is in your fingers. And a warning in yellow looks
optional, because in Python there was nothing between "works" and "crashes."

The habit that prevents them: write the constructor's first line as the `: base(...)` line whenever
the class has a parent, and build before you write the body.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Field** | A variable that belongs to an object. Private by convention: `_loadKg` |
| **Property** | A member that looks like a field from outside and runs `get` and `set` code |
| **Auto-property** | A property with no body: `public string Name { get; }` |
| **Constructor** | The method that builds an object. Same name as the class, no return type |
| **`: base(...)`** | Calls the parent class's constructor first |
| **`abstract`** | On a class: cannot be built. On a member: every concrete subclass must supply it |
| **`virtual` / `override`** | The parent allows a replacement; the child supplies one |
| **`sealed`** | Nothing may inherit from this class |
| **PascalCase / camelCase** | `StorageRack`, `LoadKg` / `capacityKg`, `_loadKg` |

---

## Self-check

**Question 1.** Rewrite this Python property pair as one C# property, with the check.

```python
@property
def tools_out(self):
    return self._tools_out

@tools_out.setter
def tools_out(self, value):
    if value < 0 or value > self._slots:
        raise ValueError("tools out must be from 0 to slots")
    self._tools_out = value
```

**Question 2.** What does CS7036 mean in a subclass constructor, and what line fixes it?

**Question 3.** `Equipment item = new StorageRack(...)`, then `item.Describe()`. Which `Describe`
runs, and which two keywords make that happen?

---

### Answers

**1.**

```csharp
public int ToolsOut
{
    get => _toolsOut;
    set
    {
        if (value < 0 || value > Slots)
        {
            throw new ArgumentOutOfRangeException(nameof(ToolsOut), value, $"tools out must be from 0 to {Slots}");
        }
        _toolsOut = value;
    }
}
```

`_toolsOut` is a `private int` field, and `Slots` is a get-only `int` property set in the
constructor. Lab U06-02's `ToolCart` is this exact code.

**2.** The subclass constructor did not say which parent constructor to call, so C# looked for one
with no parameters and found none. The fix is `: base(...)` after the constructor's parameter list,
passing the arguments the parent needs.

**3.** The rack's `Describe` runs. `virtual` on the parent's method allows a replacement, and
`override` on the rack's method supplies it. The variable's type decides which members you may call.
The object's real type decides which version runs.
