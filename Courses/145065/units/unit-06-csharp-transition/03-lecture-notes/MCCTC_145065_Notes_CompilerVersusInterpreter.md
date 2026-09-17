# Lecture Notes: A Compiler Reads the Whole Program First
## 145065 Object-Oriented Programming · Unit 6 · Week 11, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W11_CompilerVersusInterpreter.md). There is no exported
deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-06-csharp-transition/04-slides/MCCTC_145065_Slides_W11_CompilerVersusInterpreter.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK and a
terminal.

**Competencies:** 5.1.7 compare compilers and interpreters · 5.4.3 compile a working program ·
5.4.6 correct syntax errors · 5.6.4 identify a language, framework, and IDE.

Every output and error below was printed by a real build: .NET SDK 10.0.401, compiling for
`net8.0`. Python outputs are from Python 3.13.7.

---

## Why this exists

For a year, Python has run your programs one line at a time. When a line is wrong, you find out when
that line runs. Most days that is fine, because you run the program and watch it.

Units 7 and 8 build an operator panel that runs for a whole shift with nobody watching the code. A
mistake in a branch that runs once a month is a mistake nobody sees until the month it matters. C#
checks the whole program before any of it runs. That is the reason this course switches languages
for the panel, and it is the only reason you need today.

**C# is not a better language than Python. It is a stricter one.** This unit shows you what the
strictness buys and what it costs.

---

## The concept in plain language

**An interpreter** reads your program and runs it as it goes. Python checks the spelling of the
language before it starts, so a missing colon stops everything. It does not check whether a name
exists or whether two values can be added until the line with them runs.

**A compiler** reads the whole program first. The C# compiler checks every name, every type, and
every call against everything else in the program. If all of it is consistent, it writes a file
the computer can run. If anything is wrong, it writes nothing, and nothing runs.

That is why C# has a build step and Python does not seem to. `dotnet build` is the compiler.
`dotnet run` builds first, then runs.

### Side by side

| You already write, in Python | In C# | What changed, beyond spelling |
|---|---|---|
| `python check.py` | `dotnet build`, then `dotnet run` | Checking and running are two separate steps |
| A `NameError` when the line runs | error CS0103 before anything runs | The mistake is found even if the line never runs |
| `print("text")` | `Console.WriteLine("text");` | Statements end with `;` and text uses double quotes |
| One `.py` file is the program | A project folder with a `.csproj` file | The project file tells the compiler what to build and for which .NET |

---

## Worked example 1: the same mistake, two languages

Python, `typo_at_the_end.py`:

```python
print("Checking Line 3")
print("Press 1: running")
print("Oven: " + oven_temp)
```

Output:

```
Checking Line 3
Press 1: running
NameError: name 'oven_temp' is not defined
```

C#, in a new console project:

```
dotnet new console -n LineCheck -f net8.0
cd LineCheck
```

`Program.cs`:

```csharp
Console.WriteLine("Checking Line 3");
Console.WriteLine("Press 1: running");
Console.WriteLine("Oven: " + ovenTemp);
```

`dotnet build` prints:

```
w11mon_a_typo_on_last_line.cs(4,30): error CS0103: The name 'ovenTemp' does not exist in the current context
```

Nothing printed. Not even the first line. (The error names the file that was compiled. The recorded
file has one comment line at the top. In a `Program.cs` holding only these three lines, the same
build prints `Program.cs(3,30): error CS0103: ...`, which was also checked.)

---

## Worked example 2: the typo that never runs

This is the one that matters on a panel.

Python:

```python
oven_temp_c = 212.0
if oven_temp_c > 240:
    print("ALARM: " + alarm_txt)
print("Oven normal")
```

Output:

```
Oven normal
```

No error. The alarm branch did not run today, so Python never looked at `alarm_txt`. The first time
the oven goes above 240, the alarm crashes instead of printing.

C#:

```csharp
double ovenTempC = 212.0;
if (ovenTempC > 240)
{
    Console.WriteLine("ALARM: " + alarmTxt);
}
Console.WriteLine("Oven normal");
```

```
w11mon_b_typo_in_rare_branch.cs(5,35): error CS0103: The name 'alarmTxt' does not exist in the current context
```

The compiler read the branch anyway. Fix the name to `alarmText`, declare it, and the program
builds and prints `Oven normal`.

---

## Worked example 3: reading an error line

Every C# error line has the same six parts. Read them in this order.

```
w11mon_b_typo_in_rare_branch.cs(5,35): error CS0103: The name 'alarmTxt' does not exist in the current context
```

| Part | Here | What it tells you |
|---|---|---|
| File | `w11mon_b_typo_in_rare_branch.cs` | Which file to open |
| Line | `5` | Which line |
| Column | `35` | Which character on that line, counting from 1 |
| Severity | `error` | The build failed. A `warning` means it did not |
| Code | `CS0103` | A number you can search for. Same mistake, same code, every time |
| Message | `The name 'alarmTxt' does not exist...` | What the compiler could not make consistent |

Count 35 characters into line 5 and you land on the `a` of `alarmTxt`.

---

## The wrong version, and the error it produces

The Python habit: `print` and single quotes.

```csharp
print('Checking Line 3');
```

```
w11mon_d_python_print.cs(2,7): error CS1012: Too many characters in character literal
```

The message does not mention `print` at all. In C#, single quotes hold exactly one character, such
as `'B'`, and text needs double quotes. The compiler stopped at the quotes before it ever reached
the question of whether `print` exists. **Fix the first error first.** Later errors often vanish,
and new ones sometimes appear, because the compiler could not read past the first mistake.

Fixed: `Console.WriteLine("Checking Line 3");`

---

## Why the wrong version is tempting

You have typed `print(` thousands of times. Your fingers do it before you think. Single quotes and
double quotes mean the same thing in Python, so you never had a reason to notice which you used.

The habit that prevents it: build after every few lines, not after every hundred. A compiler error
from a line you wrote ten seconds ago takes ten seconds to fix.

---

## What the compiler does not do

It does not check whether your program is right. It checks whether it is consistent. A wrong
threshold, a wrong formula, and a loop that reads past the end of its data all build without a word.
You will meet each of those this week. Write this down:

> The compiler checks that the program is consistent, not that it is right.

---

## Why C# for this panel, and the honest counterpoint (5.6.4)

| Choice | Why here |
|---|---|
| Language: C# | The panel runs all shift. Mistakes the compiler refuses never reach the floor. |
| Framework: WPF | A Windows desktop framework that C# drives directly. Unit 7 teaches it. |
| IDE: Visual Studio 2026 | Built around C# and WPF: designer, build, tests, and debugger in one place. |

**The counterpoint.** Python gets a first working version on screen faster, and the Raspberry Pi
side of the panel is written in Python for exactly that reason. The right language depends on the
job.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Compiler** | A program that checks a whole program and translates it into a runnable file before anything runs |
| **Interpreter** | A program that reads and runs code as it goes |
| **Build** | Running the compiler on a project. `dotnet build` |
| **Compile-time** | When the compiler is checking. Errors here stop the build |
| **Run-time** | When the program is running. Errors here are exceptions |
| **Project file** | The `.csproj` file that tells the compiler what to build and which .NET to target |
| **Error code** | The `CSxxxx` number on every compiler message |
| **Warning** | A compiler message that does not stop the build |

---

## Self-check

**Question 1.** A Python program and a C# program each have a misspelled name inside an `if` whose
condition is false today. What happens when each one is started?

**Question 2.** Read this line and name the file, the line, the column, and the error code. Then
say in one sentence what the compiler could not make consistent.

```
Program.cs(12,9): error CS0103: The name 'shiftTotal' does not exist in the current context
```

**Question 3.** A classmate says, "My C# program built, so it works." Give one example from this
lesson that proves the claim can be false.

---

### Answers

**1.** Python starts, skips the branch, and runs to the end with no error. The mistake waits for
the day the condition is true. C# never starts: the build fails with CS0103, because the compiler
checks every line whether or not it will run.

**2.** File `Program.cs`, line 12, column 9, code CS0103. The compiler found the name `shiftTotal`
used where no variable, method, or type of that name exists, often a typo or a variable declared
somewhere it cannot be seen.

**3.** Any program that is consistent and wrong. For example, a loop that reads one element past
the end of an array builds and then crashes, and an alarm threshold typed as 420 instead of 240
builds and never alarms. The compiler checks consistency, not correctness.
