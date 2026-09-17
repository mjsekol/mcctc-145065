# Lab U06-02: Port a Piece of Line 3
## 145065 Object-Oriented Programming · Unit 6 · Week 11

**Gate:** 3 (open tooling). **Duration:** Week 11 Thursday, Build 1 (35 minutes) and Build 2
(40 minutes). **Competencies:** 5.3.12 (classes, objects, and methods), 5.1.4 (object-oriented
programming), 5.5.5 (naming conventions and comments), 5.4.4 and 5.4.5 (test cases), 5.4.6 (correct
syntax errors).

Riverside Fabrication is a composite: an invented small metal fabrication shop.

---

## The scenario

The Line 3 panel will be written in C#, and the model of the line's equipment is in Python. Before
anyone ports the whole model, the team wants two small classes ported exactly, with tests that prove
the C# behaves the same. If the small port goes well, the big one is next Friday, and it is yours.

## What you will build

C# versions of the Python `Sensor`, `Equipment`, and `StorageRack` classes that pass a provided test
suite, plus a new `ToolCart` class you write with no starter.

**This lab is practice for your own port.** Every decision you make here, you will make again for
your Unit 2 hierarchy.

---

## Starter code

The files are in `05-labs/lab-u06-02-files/`. Copy the whole folder.

| Path | What it is |
|---|---|
| `python_original/line3_parts.py` | The Python you are porting. Run it |
| `Line3.Port.sln` | The solution: both projects |
| `Line3.Port/Line3.Port.csproj` | The class library, `net8.0` |
| `Line3.Port/Sensor.cs` | Part A. Every member throws `NotImplementedException` |
| `Line3.Port/Equipment.cs` | Part B. Same |
| `Line3.Port/StorageRack.cs` | Part B. Same |
| `Line3.Port.Tests/SensorTests.cs` | Part A's tests. Do not edit |
| `Line3.Port.Tests/RackTests.cs` | Part B's tests. Do not edit |
| `Line3.Port.Tests/ToolCartTests.cs.txt` | Part C's tests, switched off. Do not edit |

The starter builds. Most tests fail, and that is the point: the tests describe what the Python does,
and your job is to make the C# do it too.

Here is the start of `Sensor.cs`, so you know the shape:

```csharp
public class Sensor
{
    // TODO A1: private fields. Python kept the reading in self._value.
    //          Pick a C# type that can say "no reading" without using zero.

    public Sensor(string id, string kind, string unit, double low, double high)
    {
        // TODO A2: validate every argument the way the Python __init__ does,
        //          then store each one. Throw ArgumentException for bad values.
        throw new NotImplementedException();
    }

    // TODO A3: replace each throw with a get-only property.
    public string Id => throw new NotImplementedException();
```

---

## Part A: Build 1, steps 1 through 7

### Step 1. Run the Python

```
cd python_original
python line3_parts.py
```

**Observable result:** eight lines, ending with `refused: load_kg cannot be negative`. Keep this
output open. It is what the C# must do.

### Step 2. Build and test the starter

From the `lab-u06-02-files` folder:

```
dotnet build Line3.Port.sln
dotnet test Line3.Port.sln
```

In Visual Studio 2026: open `Line3.Port.sln`, Build, Build Solution, then Test, Test Explorer, Run
All. **[VERIFY]** the menu names on your lab machine.

**Observable result:** the build succeeds, and the tests report 21 failed and 5 passed. The 5 that
pass test `IsValidAssetTag`, which is already written for you as an example of a static method.
Commit.

### Step 3. The fields (TODO A1)

Add private fields to `Sensor`. Python used `None` for "no reading." Choose a C# type that can hold a
number or nothing.

**Observable result:** still builds. Nothing passes yet, because the constructor still throws.

### Step 4. The constructor (TODO A2)

Port the Python `__init__`. Keep every check the Python has that the compiler cannot do for you. The
sensor id pattern is `^[a-z][a-z0-9-]{1,31}\z`. Use `\z`, not `$`, because in .NET `$` also matches
before a final newline. Throw `ArgumentException` for a bad id, a blank kind or unit, or limits in the
wrong order.

**Observable result:** tests A06, A07, and A08 pass. Before you move on, write one comment above
the constructor listing the Python checks you **deleted** because the compiler does them now.

### Step 5. The properties (TODO A3 and A4)

Replace each `=> throw new NotImplementedException();` with a get-only property. `Value` returns
your field.

**Observable result:** A01 passes. A02 still fails, because it also calls `Status()`, which still
throws.

### Step 6. `Record` and `Clear` (TODO A5)

`Record` refuses NaN and infinity with `ArgumentOutOfRangeException`. `double.IsFinite` exists.
`Clear` means "no reading," not zero.

**Observable result:** A05 passes. A04 still waits on `Status()`.

### Step 7. `Status` (TODO A6)

Check in the same order as Python: no reading first.

**Observable result:** all 14 Sensor test cases pass. Commit with a message that says what the port
changed.

### Acceptance criteria, Part A

1. All 14 Sensor test cases pass
2. `Value` is `double?`, and no member of `Sensor` is a public field
3. A comment lists the Python checks the compiler made unnecessary

---

## Part B: Build 2, steps 8 through 10

### Step 8. `Equipment` (TODO B1 to B3)

Port the constructor, the two properties, and `Describe`. `Kind` is already declared `abstract`.
`Describe` stays `virtual`, so a subclass may extend it.

**Observable result:** still builds. Apart from the five `IsValidAssetTag` cases, the Rack tests
still fail, because `StorageRack` still throws.

### Step 9. `StorageRack` (TODO B4 to B8)

The constructor already calls `: base(assetTag, name)`. Read that line and find the Python it
replaced. Then port the capacity check, `Kind`, `CapacityKg`, the `LoadKg` property with its
validation, and `Describe`, which adds `, 96% full` to the base description using `Math.Round`.

An overloaded rack is a real, dangerous state, so the setter **records** 1500 kg on a 1200 kg rack.
A negative load is impossible, so the setter **refuses** it and keeps the old load.

**Observable result:** all 12 Rack test cases pass. `dotnet test` reports 26 passed.

### Step 10. Break it once

Delete the `: base(assetTag, name)` line and build.

**Observable result:** error CS7036. Paste it into `LAB_LOG.md` with one sentence saying which
parent constructor the message names and why. Put the line back.

### Acceptance criteria, Part B

1. `dotnet test` reports 26 passed, 0 failed
2. `LoadKg` checks before it assigns, so a refused value never changes the field
3. `LAB_LOG.md` has the CS7036 line and its sentence

---

## Part C: Build 2, steps 11 through 13

### Step 11. Switch on the ToolCart tests before the class exists

Rename `Line3.Port.Tests/ToolCartTests.cs.txt` to `ToolCartTests.cs`. Build the solution.

**Observable result:** the build fails. The first error is:

```
ToolCartTests.cs(15,30): error CS0246: The type or namespace name 'ToolCart' could not be found (are you missing a using directive or an assembly reference?)
```

There are five errors, and one of them, CS0619, talks about `ThrowsAnyAsync`. That one is a side
effect: the compiler could not work out what `new ToolCart(...)` is, so it guessed the wrong version
of `Assert.ThrowsAny`. Paste the first error into `LAB_LOG.md` and say in one sentence why you fix
the first error first.

### Step 12. Write `ToolCart` from nothing

Create `Line3.Port/ToolCart.cs`. Read the four tests in `ToolCartTests.cs` and write the class they
describe:

- a cart is `Equipment` with the kind `"cart"`
- it has a number of slots, at least one, set once
- `ToolsOut` is how many tools are checked out, from 0 to the slot count
- `Describe()` adds `, 3 of 12 tools out` to the base description

Choose the type of `ToolsOut` on purpose. A tool is out or it is not.

**Observable result:** the build succeeds, and `dotnet test` reports 31 passed, 0 failed.

### Step 13. Map it back

In `LAB_LOG.md`, write the Python you would have written for `ToolCart`, as a short sketch, and
list two things C# made you decide that Python would not have.

**Observable result:** a sketch and two decisions. Commit and push.

---

## Acceptance criteria, full lab

- [ ] `dotnet test Line3.Port.sln` reports 31 passed, 0 failed
- [ ] No test file was edited
- [ ] No public fields anywhere in `Line3.Port`
- [ ] `Value` is `double?` and `ToolsOut` is `int`
- [ ] Every property that can be set checks its value before assigning it
- [ ] Names follow C# conventions: `PascalCase` members, `_camelCase` private fields
- [ ] `LAB_LOG.md` has the CS7036 line, the CS0246 line, and the step 13 comparison
- [ ] `bin/` and `obj/` are not committed

---

## If it breaks

These were recorded by making each mistake in the starter.

### 1. The subclass constructor lost its `: base(...)`

```
StorageRack.cs(15,12): error CS7036: There is no argument given that corresponds to the required parameter 'assetTag' of 'Equipment.Equipment(string, string)'
```

**Cause:** without `: base(...)`, C# looks for a parent constructor with no parameters. `Equipment`
has only the one that takes a tag and a name. Put the line back.

### 2. `Kind` without the word `override`

```
StorageRack.cs(23,19): warning CS0114: 'StorageRack.Kind' hides inherited member 'Equipment.Kind'. To make the current member override that implementation, add the override keyword. Otherwise add the new keyword.
StorageRack.cs(9,14): error CS0534: 'StorageRack' does not implement inherited abstract member 'Equipment.Kind.get'
```

**Cause:** a property with the same name is a new property, not the parent's. The parent's abstract
`Kind` is still missing. Write `public override string Kind => "rack";`.

### 3. Doing arithmetic on a reading that may not exist

```
Sensor.cs(32,45): error CS0266: Cannot implicitly convert type 'double?' to 'double'. An explicit conversion exists (are you missing a cast?)
Sensor.cs(32,45): warning CS8629: Nullable value type may be null.
```

**Cause:** `double c = Value;` where `Value` is `double?`. **Do not add the cast the message
suggests.** A cast compiles and then throws on the day the reading is missing. Decide what "no
reading" means first: `if (Value is double c) { ... }`.

### 4. A method that forgets one return

```
Sensor.cs(39,19): error CS0161: 'Sensor.Status()': not all code paths return a value
```

**Cause:** an `if` chain with no final `return`. The compiler does not work out whether your
conditions cover every case. It only sees a path that ends with no value. Add the last `return "ok";`.

### Also likely: the Python word for nothing

```
Sensor.cs(39,43): error CS0103: The name 'None' does not exist in the current context
```

**Cause:** C# spells it `null`, and for a `double?` the clearest test is `Value is null`.

Your line and column numbers will match your own file.

---

## Stretch goal

**Part A.** Add a `ToString()` override to `Sensor` that prints like the Python `__repr__` would.
Nothing tests it. Write one test of your own in a new file.

**Part B.** In `LAB_LOG.md`, answer in three or four sentences: the Python `require_number` helper
checked for text, for booleans, and for NaN. Which of those three checks did your C# keep, and why
are the other two gone?

---

## Submission checklist

- [ ] `dotnet test Line3.Port.sln` reports 31 passed
- [ ] `LAB_LOG.md` complete, with pasted error lines
- [ ] `ToolCartTests.cs` renamed, not edited
- [ ] `git status` shows nothing uncommitted, and `bin/` and `obj/` are not in the repository
- [ ] Pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension
scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| Fewer than 6 Sensor tests passing at minute 25 of Build 1, or confused by `=>` | SCAFFOLDED |
| Tests going green steadily, questions about validation details | STANDARD |
| All 26 passing before Build 2 starts, or asked why `Status` returns a string | EXTENDED |
| Said the plant model has nothing to do with them | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Part A:** the fields and properties (TODO A1, A3, A4) are given complete. The student writes the
  constructor checks, `Record`, `Clear`, and `Status`.
- **Part B:** `Equipment` is given complete. The student writes `StorageRack` only.
- **Part C:** the `ToolCart` class shell is given, with the constructor signature and empty members.
  The student writes the bodies.
- **Step 10 and step 11 stay.** Both deliberate failures are the lesson.
- **Checkpoints:** show you the test count after step 4, after step 7, and after step 9.

**Acceptance criteria:** 31 tests pass; `LAB_LOG.md` has the CS7036 and CS0246 lines.

**Grading:** same 100-point scale, judged against this version's list. A complete SCAFFOLDED
submission earns the same grade as a complete STANDARD one.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus one addition that needs something you have not been taught.

**Added requirement.** A panel should not compare status strings, because `"no readng"` would build.
Add an `enum SensorStatus` with `NoReading`, `Low`, `Ok`, and `High`, and a `StatusCode` property on
`Sensor` that returns it. Then rewrite `Status()` so it turns `StatusCode` into the same four strings.
All 31 existing tests must still pass. Add at least four tests of your own for `StatusCode`.

**Hint, not the answer.** Week 12 teaches the switch expression. Read the C# language reference page
on the switch expression on learn.microsoft.com **[VERIFY]** the page address, and look at the
examples that use relational patterns and `when`.

**Acceptance criteria:** all STANDARD criteria, plus the enum, `StatusCode`, a `Status()` built on it,
and at least four new passing tests.

**Grading:** same scale. An honest, partly working attempt with a clear log entry loses very little.

---

## APPLIED

**For the student who says this does not apply to them.**

**Changed scenario.** Port a class you wrote yourself in Python: a `Room` or `Player` from your
145060 text adventure, or any class from a side quest. Choose one with at least one validated value.

**What you build.** The C# class, a subclass of it with `: base(...)` and one `override`, and a test
project with at least eight tests you wrote, including one for each value that must be refused. Use
`dotnet new xunit -n YourName.Tests -f net8.0` to create the test project.

**The extra requirement that makes it the same lab.** `LAB_LOG.md` lists every check in your Python
and says, for each one, whether the compiler now does it or your code still must.

**Acceptance criteria:** the class, the subclass, eight passing tests, the check list, and the
step 10 and step 11 style failures reproduced on your own code.

**Grading:** same scale. Requirements Fit is judged on whether each type and each kept check fits
the value, which is the same judgment the port project asks for.
