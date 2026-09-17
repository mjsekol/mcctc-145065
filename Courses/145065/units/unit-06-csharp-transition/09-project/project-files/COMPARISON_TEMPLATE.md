# What the Compiler Caught · [your hierarchy's name]

Copy this file to your repository as `COMPARISON.md`. Keep the three section headings exactly as
they are: `port_check.py` looks for them.

Every compiler message in this file is pasted from **your own** build. Every Python outcome is
pasted from **your own** run. A retyped message is a claim. A pasted one is evidence.

Built with: `dotnet --version` gives ______. Python: `python --version` gives ______.

## The claim, stated narrowly

One paragraph. What did the switch to C# buy this code, and what did it cost? Do not write that C#
is better. Write what it made stricter.

## What the compiler caught

Five or more entries, each a different compiler message. Use this shape for each.

### 1. [a short name for the mistake]

The C# you wrote, or the mistake you made on purpose:

```csharp
```

What the build printed, pasted:

```
```

**Python:** what the same mistake did in your Python, pasted or described from a real run. Say
whether Python raised nothing, raised something only when that line ran, or caught it only because
you wrote a check by hand. Give Python credit where it earned it.

## What the compiler did not catch

| Still a hand-written check | Why the compiler cannot help | Where your port handles it, and the test that proves it |
|---|---|---|
| | | |

## What is more verbose in C#

At least one real example from your port, the Python and the C# side by side, and a measured count:
lines, or lines that are only braces.

```python
```

```csharp
```

## What this means for the panel

Two or three sentences for the controls lead. Which of your catches would have reached the floor in
Python, and which risks are still yours?
