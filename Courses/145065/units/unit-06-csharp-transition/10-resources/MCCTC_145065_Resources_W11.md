# Additional Resources · Week 11
## 145065 Object-Oriented Programming · Unit 6 · Week 11
### Topics: compiled and interpreted, static types and arithmetic, loops, classes in C#

Every link is marked **Confident** (the site exists and has been stable for years) or **[VERIFY]**
(the exact page address may have moved; check it before you hand it out). Nothing here needs an
account, and nothing asks you to paste code into an AI tool.

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | Microsoft Learn: the C# documentation home and the tour of C# | Mon to Thu | On-level | 30 min |
| 2 | The C# language reference: built-in types | Tue | On-level | 15 min |
| 3 | The C# language reference: iteration statements | Wed | On-level | 15 min |
| 4 | A short beginner video on C# | Mon | Remediation | under 20 min |
| 5 | Exercism's C# track | Wed to Fri | Remediation or extension | 20 min a day |
| 6 | The .NET command-line tools overview | Mon | Extension | 15 min |
| 7 | An industry read: the .NET Blog | Fri | Extension | 10 min |
| 8 | Side quest SQ-15, Same Program, Two Languages | Fri | Extension | two blocks |

---

## 1. Primary reading: the tour of C#

**Microsoft Learn, C# documentation** · `https://learn.microsoft.com/en-us/dotnet/csharp/` ·
**Confident** for the site. The "tour of C#" section sits under it:
`https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/` **[VERIFY]** the address.

**What it is.** Microsoft's own introduction to the language, free, no account.

**Why this one.** It is the primary source, it is current for .NET 8 and later, and it uses the same
vocabulary as the compiler's messages.

**Assign a question, not the pages:** *what is the difference between a value type and a reference
type, and which one is a `double`?* That is Tuesday's model in the official words.

**Skip for now:** anything about generics, delegates, LINQ, records, or async. None is needed this
unit.

## 2. Built-in types

**C# language reference, built-in types** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/built-in-types`
**[VERIFY]**.

**Why this one.** One table of every type with its range. Tuesday's `int` top of 2,147,483,647 is on it.

**Assign:** find the largest `int` and the largest `long`. Then answer: why does a press stroke counter
in the course anchor use `checked` arithmetic?

## 3. Loops

**C# language reference, iteration statements** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/iteration-statements`
**[VERIFY]**.

**Why this one.** `for`, `foreach`, `while`, and `do`, each with a short example, in one page.

**Assign:** find the sentence that explains when a `do` loop's body runs, and connect it to the
Wednesday demo that printed `do: attempt 1`.

## 4. A short video

**A beginner C# video from Microsoft's own channels**, first episode only, under 20 minutes.
**[VERIFY]**: search Microsoft Learn or the official .NET channel for a current "C# for beginners"
series and check the length and the .NET version before you assign it. Series are renamed and
replaced often, so no address is given here.

**Why this kind.** For the student who missed Monday and needs to see a build happen before reading
about it. Use it as remediation only.

## 5. Practice: Exercism's C# track

`https://exercism.org/tracks/csharp` · **Confident** for the site.

**What it is.** Small exercises with tests you run on your own machine.

**Why this one.** It works the same way Lab U06-02 works: make the tests pass.

**Important.** Exercism has an optional mentoring feature and a sign-up. Students do not need to create
an account to read the exercise descriptions, and **students under 18 must not create an account
without their family's permission and the school's rules.** A student can copy an exercise's
description into a local project and write their own tests. **[VERIFY]** the site's current terms
before you point students at it.

## 6. The `dotnet` command line

**.NET CLI overview** · `https://learn.microsoft.com/en-us/dotnet/core/tools/` **[VERIFY]**.

**Why this one.** Every command this week, `dotnet new`, `build`, `run`, and `test`, with its options.
Look up `--format` under `dotnet new sln`, which is why every solution in this unit is `.sln`.

## 7. An industry read

**The .NET Blog** · `https://devblogs.microsoft.com/dotnet/` · **Confident** for the site.

**How to use it.** Pick one current post about a new .NET release and ask students one question: what
did the release change about warnings, nullable types, or performance? **[VERIFY]** the post you pick
before class. Do not describe a post you have not read.

## 8. Side quest

**SQ-15 Same Program, Two Languages** pairs exactly with this unit. Take a working Python program and
rewrite it in C#, with identical output on the same inputs and a README on what each language made
obvious. Full description in `Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

---

## For the student who is behind

1. Lecture notes for Tuesday and Wednesday, and their self-checks, in that order
2. Gate 1 Reps 05 and 06 again, on paper, then built
3. Lab U06-01 SCAFFOLDED
4. Nothing else. The port project needs types, loops, and classes, and those three notes are the core.

## For the student who is ahead

1. The built-in types page, then write a one-paragraph answer: why does `decimal` exist?
2. Lab U06-02 EXTENDED
3. Start SQ-15 on a small 145060 program
