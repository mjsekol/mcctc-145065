# Lecture Notes: Three Interfaces, Three Versions
## 145065 Object-Oriented Programming · Unit 9 · Week 17, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W17_ThreeInterfacesThreeVersions.md). There is no exported
deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-09-ship-document-demonstrate/04-slides/MCCTC_145065_Slides_W17_ThreeInterfacesThreeVersions.md --export pptx`

If you missed class, you can learn this concept from this file alone.

**Competencies:** 5.7.1, version management and interface control. 5.7.2, baseline and lifecycle phases.
5.7.3, analyze the impact of changes. You met all three before: semantic versions and baselines in
145060, the baseline tag on your CRUD app in Week 10, and interface changes the compiler caught in
Week 12. **Today you apply them to a system that spans two machines and a group of people.**

---

## Why this exists

In Week 12 you added a member to a C# interface and the compiler listed every class that broke. That
was interface control at its most comfortable: one program, one compiler, a complete list.

Your panel is not one program. It reads a reply from another machine. It reads a settings file that a
maintenance tech edits. It shows words an operator was trained on. **None of those has a compiler
watching it.** A change to any of them can break something, and nothing will list what.

Today you set a baseline, and you learn to ask one question before every change: **which interface
does this touch?**

---

## The concept in plain language

**A system that spans machines and people has several interfaces, and each one can have its own
version. Classify every change by the interface it touches, and measure it against a baseline.**

The Line 3 panel's interfaces:

| Interface | Who depends on it | Its version |
|---|---|---|
| The reading contract (the JSON the sensor service sends) | the service on the Pi, and every panel | none written in the reply; fixed by agreement |
| `thresholds.json` | every panel, maintenance, the shift lead | `schema_version`, currently 1 |
| The words on the screen | operators, the guide, the training card | the list in `screen-words.txt` |
| The command line | the panel PC's shortcut, the implementation plan | documented in the plan |
| The release | the panel PC, the shift lead | `<Version>` in the project file |

**The baseline** is the release everyone agreed on, tagged so it can always be found. For your panel it
is 1.0.0, the version the shift lead is trained on tomorrow. Every later change is measured against it.
From today, your panel moves from the testing phase into deployment, and after the handoff, into
maintenance, which is the longest phase any used program has.

```
git tag -a v1.0.0 -m "Baseline: the version the shift lead is trained on"
git push origin v1.0.0
```

`git push` alone does not send tags. Push the tag by name, then find it on the repository's tags page
[VERIFY where GitHub lists tags on your account].

---

## Worked example 1: a new key in an old file

The shift lead wants a warning at 225 C, before the 230 C alarm. Maintenance adds one line to the oven's
entry in `thresholds.json` and leaves `schema_version` at 1. Lab U09-02's probe runs the 1.0.0 loader on
that file:

```
dotnet run --project ConfigProbe -- configs/cr-a-extra-key.json
```

```
File: cr-a-extra-key.json
LOADED   3 sensors, stale after 5 s
         oven-temp        Limits 190.0 to 230.0 C
         press-vibration  High limit 6.0 mm/s
         coolant-level    Low limit 25 %
Ignored by a 1.0.0 panel: warn_high (oven-temp)
```

**The 1.0.0 panel starts, and shows no warning, and says nothing.** Its loader asks for the keys it knows
and never looks at the rest. That design lets the file carry notes. It also means a new setting on an
old panel disappears without a word. The last line is the probe telling you. The panel never would.

---

## Worked example 2: the same change with a new schema version

The same file, with `schema_version` raised to 2:

```
File: cr-b-schema-2.json
REFUSED  schema_version is 2; this panel reads version 1.
Ignored by a 1.0.0 panel: warn_high (oven-temp)
```

**The 1.0.0 panel refuses to start, with a sentence.** That is worse for convenience and better for
safety: nobody believes a warning exists on a panel that cannot show one. The file's version made the
change visible. The cost: every panel must be updated to a release that reads version 2 **before** the
new file is installed. That order goes into the implementation plan.

---

## Worked example 3: adding a field without breaking every caller

In C#, the loader builds one limit per sensor. To carry a warning level, the limit type needs a new
field. There are two ways to add it.

```csharp
Limit press = new("press-vibration", null, 6.0) { WarnHigh = 5.5 };
Limit coolant = new("coolant-level", 25.0, null);

Console.WriteLine(press);
Console.WriteLine(coolant);
Console.WriteLine(coolant.WarnHigh is null ? "coolant has no warning level" : "coolant warns");

// Low and High are positional: every caller passes them.
// WarnHigh is init-only: a caller may set it, and old calls still compile.
public sealed record Limit(string Id, double? Low, double? High)
{
    public double? WarnHigh { get; init; }
}
```

Output:

```
Limit { Id = press-vibration, Low = , High = 6, WarnHigh = 5.5 }
Limit { Id = coolant-level, Low = 25, High = , WarnHigh =  }
coolant has no warning level
```

The line that builds `coolant` is exactly the call every existing file already makes. It still
compiles. An `init` property is part of the type's interface, and adding one is a **compatible**
change.

---

## The wrong version, and the error it produces

Add the warning level as a fourth positional parameter instead:

```csharp
Limit press = new("press-vibration", null, 6.0, 5.5);
Limit coolant = new("coolant-level", 25.0, null);

Console.WriteLine(press);
Console.WriteLine(coolant);

// WarnHigh added as a fourth positional parameter.
public sealed record Limit(string Id, double? Low, double? High, double? WarnHigh);
```

```
Program.cs(2,17): error CS7036: There is no argument given that corresponds to the required parameter 'WarnHigh' of 'Limit.Limit(string, double?, double?, double?)'
```

Every existing call is now an error. Inside one program, that is the good kind of wrong: **the compiler's
list of errors is the impact analysis.** You met the same thing in Week 12, when adding a member to an
interface made the compiler name every class that no longer kept it:

```
Program.cs(12,37): error CS0535: 'SimulatedOven' does not implement interface member 'ISensorSource.IsSimulator'
Program.cs(19,36): error CS0535: 'Ds18b20Probe' does not implement interface member 'ISensorSource.IsSimulator'
```

**The real danger is the change the compiler cannot see.** Lab U09-02 has one: rename the oven's `high`
key in the settings file. The 1.0.0 panel loads it, shows `Low limit 190.0 C`, and never alarms on a hot
oven again. No compiler, no error, no warning.

---

## Why the wrong version is tempting

**"It's one line in a file."** Files do not feel like interfaces. They are interfaces, with more readers
than most classes have.

**The compiler trained you to trust silence.** In C#, no errors usually means no problem. Across machines
and files, silence means nobody was checking.

**Versions feel like one number.** Your panel has one release number, and its settings file has its own
format version. A change can be a MINOR release of the program and a breaking change to the file.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Interface control** | changing any interface only on purpose, with a version and a written note |
| **Interface** | anything outside your code that depends on it staying the same: a contract, a file format, a screen word, a command line |
| **Schema version** | a number inside a file that names the file's format |
| **Baseline** | the reviewed, agreed version later changes are measured against |
| **Tag** | a Git name fixed to one commit, such as `v1.0.0` |
| **Compatible change** | a change after which everything that worked still works |
| **Breaking change** | a change that makes something that depended on the old version stop working |
| **Change impact analysis** | listing everything a change touches, before making it |
| **Lifecycle phases** | requirements, design, development, testing, deployment, maintenance |

---

## Self-check

**Question 1.** Maintenance renames `poll_interval_ms` to `poll_ms` in `thresholds.json`, and nothing else.
What does a 1.0.0 panel do with the file, and which interface did the change touch?

**Question 2.** Your team decides the warning ships as `schema_version` 2 with a new panel that reads both
1 and 2. Give a version number for the panel program and say why, then say what the implementation plan
must require about the order of installation.

**Question 3.** Why is a missing key in a settings file more dangerous than a missing argument in a C#
constructor call?

---

### Answers

**1.** It refuses to start: the 1.0.0 loader requires `poll_interval_ms` and reports that it is missing or
not a whole number. The change touched the settings file's format, which is an interface with its own
version, so it should have come with a new `schema_version`, not a silent rename.

**2.** 1.1.0, a MINOR release: a new feature, and every version 1 file still loads. The plan must say
every panel is updated to 1.1.0 before any version 2 file is installed, because a 1.0.0 panel refuses a
version 2 file.

**3.** The compiler checks every constructor call before the program runs and lists each one that is
wrong. Nothing checks a settings file until a panel reads it, and a loader that treats a missing optional
key as "no limit" does not fail at all. It runs, wrongly.
