# Lecture Notes: A Release You Can Install
## 145065 Object-Oriented Programming · Unit 9 · Week 17, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W17_AReleaseYouCanInstall.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-09-ship-document-demonstrate/04-slides/MCCTC_145065_Slides_W17_AReleaseYouCanInstall.md --export pptx`

If you missed class, you can learn this concept from this file alone. Run the commands on a lab PC.

**Competencies:** 5.6.8, create documentation such as an implementation plan. 5.7.1, explain version
management. 5.4.3, compile a working program.

---

## Why this exists

In 145060 you deployed a web app. The host built it from your repository. Nobody had to carry a
program to a machine.

An operator panel is different. It runs on one PC beside a machine. Somebody has to build it, carry
it there, start it, and prove it is the right one. That somebody might be you on a Friday afternoon,
or a maintenance tech a year from now who has never met you.

Until today your panel ran with `dotnet run`, from source, on your own PC. **That is not a release.**
It needs the SDK, your source folder, and you.

---

## The concept in plain language

**A release is a built program with one version number, installed by written steps that anyone can
follow and check.**

Three parts, and you need all three.

| Part | What it means for your panel |
|---|---|
| **A built program** | a release folder made by `dotnet publish`: the `.exe`, the `.dll` files beside it, and your settings files |
| **One version number** | written once, as `<Version>` in the WPF project file. The build stamps it into the program. The screen shows it. |
| **Written steps** | an implementation plan in which every step says what you should see, including how to go back |

You met the implementation plan in 145060, with its data dictionary and rollback. Today it gets a job
it did not have before: carrying a program to a different machine.

### Where the version lives

```xml
<PropertyGroup>
  <OutputType>WinExe</OutputType>
  <TargetFramework>net8.0-windows</TargetFramework>
  <UseWPF>true</UseWPF>
  <Version>1.0.0</Version>
</PropertyGroup>
```

When you build, the SDK writes that number into the program file in several places. The one that
matters most is the **informational version**, which your code can read and which Windows shows as the
file's "Product version."

---

## Worked example 1: the program reads its own version

This console program has `<Version>1.0.1</Version>` in its project file.

```csharp
// VersionDemo: read the version the build stamped into this program.
using System.Reflection;

string? stamp = typeof(Program).Assembly
    .GetCustomAttribute<AssemblyInformationalVersionAttribute>()?
    .InformationalVersion;

Console.WriteLine($"Stamped: {stamp}");
Console.WriteLine($"Shown:   {Shown(stamp)}");
Console.WriteLine($"Shown:   {Shown("1.0.1+3f2a9c1b")}");
Console.WriteLine($"Shown:   {Shown(null)}");

// The part before "+" is the release. After "+" is a commit id.
static string Shown(string? stamp)
{
    if (string.IsNullOrWhiteSpace(stamp))
    {
        return "unknown";
    }

    int plus = stamp.IndexOf('+');
    return plus >= 0 ? stamp[..plus] : stamp;
}
```

Output, built in a folder that is not a Git repository:

```
Stamped: 1.0.1
Shown:   1.0.1
Shown:   1.0.1
Shown:   unknown
```

**Why `Shown` exists.** When you build inside a Git repository, the SDK can add `+` and the commit id to
the stamp. That is useful in a file's properties and too long for an operator's header. The panel shows
the part before `+`.

Your panel does the same thing in its window: read the stamp once at start-up, give the view model the
text, and bind the header to it. The view model never reads the file itself, so tests can hand it any
version string.

---

## Worked example 2: build the release folder

In the folder that holds your panel's solution:

```
dotnet publish Line3.Hmi.Panel -c Release -o ..\release\Line3Panel-1.0.1
```

The last line printed on the build PC:

```
Line3.Hmi.Panel -> ...\release\Line3Panel-1.0.1\
```

The folder it made holds nine files:

```
Line3.Hmi.Core.dll
Line3.Hmi.Core.pdb
Line3.Hmi.Panel.deps.json
Line3.Hmi.Panel.dll
Line3.Hmi.Panel.exe
Line3.Hmi.Panel.pdb
Line3.Hmi.Panel.runtimeconfig.json
thresholds.bench.json
thresholds.json
```

**Every one of those files is part of the release.** The `.exe` is a small launcher. Your code is in the
`.dll` files. The limits are in the two `.json` files.

This is a **framework-dependent** build: the panel PC needs the .NET 8 Desktop Runtime installed. The
`runtimeconfig.json` file says so. A self-contained build would carry the runtime inside the folder,
but making one needs a download the lab build PC does not allow.

The `release` folder is build output. Put it in your `.gitignore`.

---

## Worked example 3: check the stamp before you copy anything

In PowerShell, in the release folder:

```
(Get-Item .\Line3.Hmi.Panel.exe).VersionInfo.ProductVersion
```

Printed on the build PC, where the source sits inside a Git repository:

```
1.0.1+557a56c22322f8a1709ad88c85e68b3a93d9e874
```

Your commit id will differ. **The part before `+` must match your project file.** This one line is the
first verification step of your implementation plan. It proves the folder you are about to carry is the
version your change log says it is.

Then start the program **from the release folder** and read the header:

```
Sensor service http://127.0.0.1:8705 · Version 1.0.1
```

That line was read from the running window on the build PC, with the simulator on port 8705. Your
address will be the one your plan names.

---

## The wrong version, and what it does

It is Friday. The panel PC needs the new build. You copy `Line3.Hmi.Panel.exe` onto a USB drive,
because that is "the program," and double-click it on the panel PC.

**Nothing happens.** No window. No message.

Started from a terminal that shows its errors, the same file prints:

```
The application to execute does not exist: '...\Line3.Hmi.Panel.dll'.
```

and exits with code `0x8000809A`. The launcher looked beside itself for the `.dll` that holds your code,
and it was not there.

The second wrong version is louder, which is better. You copy the whole folder except `thresholds.json`. This time a
box appears, titled **The Line 3 panel cannot start**:

```
Cannot read the thresholds file ...\thresholds.json: Could not find file '...\thresholds.json'.
```

and the program exits with code 2 when the box is closed. That one is the panel doing its job: refusing
to run on limits nobody chose.

**Both belong in your implementation plan's contingency section**, with what you see and what to do.

---

## Why the wrong version is tempting

**The `.exe` looks like the program.** On your own PC, double-clicking the `.exe` in `bin` works, because
everything else is sitting beside it. You never see the files it depends on.

**`dotnet run` hides the build.** It builds, finds everything, and starts the window. It works so well
that "it runs" starts to mean "it ships."

**A version number feels like decoration.** Until two copies of the panel are on two PCs, a bug is
reported, and nobody can say which one has it.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Release** | a built, versioned program with the steps to install it |
| **Release build** | a build made with the Release configuration, for use rather than debugging |
| **`dotnet publish`** | the command that builds a program and gathers everything it needs to run into one folder |
| **Framework-dependent** | a published program that needs the matching .NET runtime already installed on the machine |
| **Version stamp** | the version the build writes into the program file |
| **Informational version** | the stamp your code can read, shown by Windows as "Product version" |
| **Implementation plan** | the document that says how to install a release, prove it worked, and undo it |
| **Rollback** | going back to the previous release, from the folder you kept |

---

## Self-check

**Question 1.** Your project file says `<Version>1.0.1</Version>`. The stamp in your release folder reads
`1.0.0+9ab31c2...`. Give the most likely cause in one sentence, and the command that fixes it.

**Question 2.** A classmate copies your whole release folder to a PC and double-clicks the `.exe`. A
message says .NET must be installed [VERIFY the exact wording on a PC without the runtime]. What kind of build did you make, and what should your plan's
"Before you start" section have checked?

**Question 3.** Why does the panel's view model take the version as text from outside, instead of reading
the program file itself?

---

### Answers

**1.** The release folder was built before the project file changed, so it holds the old program.
Build it again with `dotnet publish Line3.Hmi.Panel -c Release -o <folder>`, then read the stamp again
before copying anything.

**2.** A framework-dependent build, which needs the .NET 8 Desktop Runtime on the target PC. "Before you
start" should have checked for it, for example with `dotnet --list-runtimes`, looking for a line that
starts `Microsoft.WindowsDesktop.App 8.`, and said what to do if it is missing.

**3.** So it can be tested. A test hands the view model `"1.0.1+3f2a9c1"` and checks the header says
`1.0.1`, with no program file involved. The window, which cannot be unit tested, does the one line of
reading.
