# The Program That Refuses to Start
---
## Slide 1: The alarm that never rang
- An oven alarm branch with a typo in it
- The oven stayed below 240 all month
- Python never read that line
- The first real alarm crashes instead
Speaker notes: Picture a panel on the shop floor. It checks the oven every second. There is an alarm message inside an if statement, and somebody misspelled one name in it. The oven never went above 240 this month, so that line never ran, so Python never noticed. The first time the oven really overheats, the alarm crashes instead of warning anyone. Today is about a language that would have refused to start that program at all.
Image: A dark operator panel with one red alarm light that is not lit, and a small speech bubble reading "never checked."
---
## Slide 2: Python runs, then finds out
```python
print("Checking Line 3")
print("Press 1: running")
print("Oven: " + oven_temp)
```
Speaker notes: Here is a Python program with a typo on the last line. Before I run it, tell me what you expect to see. Watch. Two lines print, and then the NameError. Python read and ran one line at a time. It found the mistake when it got there.
Image: None. This slide is code.
---
## Slide 3: The same program in C#
```csharp
Console.WriteLine("Checking Line 3");
Console.WriteLine("Press 1: running");
Console.WriteLine("Oven: " + ovenTemp);
```
Speaker notes: Same three lines in C#. Console dot WriteLine is print. Every statement ends with a semicolon. I will build it with dotnet build. Predict what prints this time. Not the first line. Not the second. Nothing at all.
Image: None. This slide is code.
---
## Slide 4: What the compiler said
```
Program.cs(3,30): error CS0103: The name 'ovenTemp' does not exist in the current context
```
Speaker notes: This is a compiler error. The compiler read the whole program before running any of it, found a name that does not exist, and refused to produce anything runnable. Let me read it aloud in order. File, Program dot cs. Line three. Column thirty. Error, so the build failed. Code CS0103. Then the message. Every C# error has those same six parts.
Image: None. This slide is code.
---
## Slide 5: Two ways to run a program
- Interpreter: read a line, run it, repeat
- Compiler: check everything, then produce a runnable file
- Python checks names when the line runs
- C# checks names before anything runs
- One mistake anywhere means nothing runs
Speaker notes: Here is the whole difference. Python is interpreted. It checks the grammar first, then checks names and types as each line runs. C# is compiled. The compiler checks every name and every type against everything else, and if anything is inconsistent, you get no program. That one difference explains most of what will feel different this week.
Image: Two conveyor belts: one where each part is inspected as it moves, one where a whole batch is inspected before the belt starts.
---
## Slide 6: The branch that never runs
```csharp
double ovenTempC = 212.0;
if (ovenTempC > 240)
{
    Console.WriteLine("ALARM: " + alarmTxt);
}
Console.WriteLine("Oven normal");
```
Speaker notes: This is the slide from the start of class. The Python version prints Oven normal and nothing else. It never looked inside the if. The C# version does not build. CS0103, line five. The compiler read the alarm line even though it would not run today. That is exactly what you want on a panel that runs all night.
Image: None. This slide is code.
---
## Slide 7: The Python habit, and a confusing message
- You type print with single quotes
- C# says: too many characters in character literal
- Single quotes hold exactly one character in C#
- Fix the first error first, then rebuild
Speaker notes: Your fingers will type print with single quotes. The error you get is CS1012, too many characters in character literal. It does not even mention print. In C#, single quotes are for one character, like the letter B. Text needs double quotes. The compiler got stuck on the quotes before it ever reached print. So fix the first error first and build again.
Image: A keyboard with the single quote key circled and the double quote key highlighted.
---
## Slide 8: What the compiler does not check
- A threshold typed as 420 instead of 240
- A loop that reads past the end
- A formula that is correct Python and wrong here
- Consistent is not the same as right
Speaker notes: Before anyone decides C# is magic, here is what the compiler does not do. A wrong number compiles. A loop that reads one past the end compiles. Tomorrow you will see a formula that is correct in Python, compiles in C#, and gives zero. Write this down. The compiler checks that the program is consistent, not that it is right.
Image: A checklist with "names" and "types" ticked and "values" and "meaning" left blank.
---
## Slide 9: Why C# for this panel, honestly
- C#: mistakes refused before a shift starts
- WPF: a Windows desktop framework C# drives
- Visual Studio: designer, build, tests in one place
- Python is faster to a first version
- The Pi side stays Python for that reason
Speaker notes: So why switch languages for the panel? Because it runs unattended for a whole shift, and a whole class of mistakes gets refused at your desk. WPF is the desktop framework you will use in Unit 7, and Visual Studio is built around both. Now the honest part. Python gets a first version on screen faster, and the Raspberry Pi side of this project is Python for exactly that reason. C# is not better. It is stricter.
Image: A two-column scale, C# on one side labeled "stricter," Python on the other labeled "faster to start," balanced.
---
## Slide 10: What you are about to build
- Lab U06-01, Part 1: your first C# project
- dotnet new console, build, run
- Break it three ways on purpose
- Copy each real error into BUILD_LOG.md
Speaker notes: Build one is the first part of the Shift Summary lab. You create a console project with dotnet new console and the net8.0 flag, build it, and run it. Then you break it on purpose three times, a missing semicolon, a misspelled name, and text where a number belongs, and you copy each real error line into your build log with one sentence saying what it means. Do not invent the errors. Paste what your compiler printed.
Image: A terminal showing a clean build, then a red error line, then a clean build again.
---
