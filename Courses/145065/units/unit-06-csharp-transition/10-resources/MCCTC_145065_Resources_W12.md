# Additional Resources · Week 12
## 145065 Object-Oriented Programming · Unit 6 · Week 12
### Topics: access modifiers, interfaces, switch, warnings and the impact of change

Every link is marked **Confident** or **[VERIFY]**, as in Week 11. Nothing here needs an account, and
nothing asks you to paste code into an AI tool.

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | Microsoft Learn: access modifiers | Mon | On-level | 15 min |
| 2 | Microsoft Learn: interfaces | Tue | On-level | 20 min |
| 3 | C# language reference: the switch expression and patterns | Wed | On-level | 20 min |
| 4 | Microsoft Learn: nullable reference types | Thu | Extension | 25 min |
| 5 | C# compiler messages reference | Thu and Fri | On-level | 10 min |
| 6 | xUnit and `dotnet test` | Mon to Wed | On-level | 15 min |
| 7 | Python's `typing.Protocol`, for comparison | Tue | Extension | 15 min |
| 8 | Side quests SQ-16 and SQ-17 | Fri | Extension | one block each |

---

## 1. Access modifiers

**Microsoft Learn, access modifiers** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers`
**[VERIFY]** the address. The C# documentation has moved this page between the language reference and
the programming guide before.

**Why this one.** It has the table of which modifier allows which caller, including `protected
internal` and `private protected`, which this unit does not teach.

**Assign a question:** *what is the default access for a class member when you write no modifier?*
Then say why this unit writes it anyway.

## 2. Interfaces

**Microsoft Learn, interfaces** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces` **[VERIFY]**.

**Why this one.** A short page with one example of a class implementing an interface.

**Warning worth passing on:** the page mentions default interface members. They exist, they change
what "adding a member breaks everything" means, and this course does not use them. A student who asks
gets that sentence and the page.

## 3. The switch expression and patterns

**C# language reference, switch expression** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression`
**[VERIFY]**, and **patterns** on the same site under `language-reference/operators/patterns`
**[VERIFY]**.

**Why this one.** The relational patterns (`>= 240`), `or`, `when` clauses, and the discard `_` from
Wednesday are all documented here with examples.

**Assign:** find what happens at run time when no arm matches. Match it with the
`SwitchExpressionException` from Wednesday's notes.

## 4. Nullable reference types

**Microsoft Learn, nullable reference types** · `https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references`
**[VERIFY]**.

**Why this one.** Thursday's CS8602 and CS8618 come from this feature. The page explains the `?` on a
reference type and the `!` operator.

**Assign:** find the sentence that says what the null-forgiving operator does at run time. Then write
Thursday's review comment again, in your own words.

## 5. Compiler messages

**C# compiler errors and warnings reference** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/` **[VERIFY]**.

**Why this one.** Search for any `CS` code you met this unit. Some codes have a long page with fixes.
Some do not. When a code is not documented, the message and your own code are the documentation.

**Honest caution.** A page's suggested fix is not always the right fix for a panel. CS0266 suggests a
cast. This unit showed why that is often wrong.

## 6. Testing

**xUnit** · `https://xunit.net/` · **Confident** for the site. The .NET testing overview on Microsoft
Learn, `https://learn.microsoft.com/en-us/dotnet/core/testing/` **[VERIFY]**.

**Why these.** `[Fact]`, `[Theory]`, `[InlineData]`, and `[MemberData]` are all in Lab U06-03. The
xUnit site explains each one.

**Version note.** The lab machines use xunit 2.5.3, the version `dotnet new xunit -f net8.0` selects.
Newer xUnit documentation may describe a later major version. If an example does not build, check
which version it is written for.

## 7. Python's version of an interface

**Python documentation, `typing.Protocol`** ·
`https://docs.python.org/3/library/typing.html#typing.Protocol` · **Confident** for the page.

**Why this one.** For the student who asks whether Python has interfaces. It does, in a sense, and
the check happens in a separate type checker, not when the program runs. Read the first example and
compare it with Tuesday's `IReadingSource`.

## 8. Side quests

**SQ-16 The Class That Should Not Be a Class** and **SQ-17 Unit Tests for Something You Already
Wrote**, both unlocked in 145065. SQ-17 on the Python half of the port is the natural Friday flex. Full
descriptions in `Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

**BPA 330 C# Programming.** Nationals usually falls in Week 14. Confirm this year's dates and the
event's current guidelines on the official BPA site **[VERIFY]**. Gate 1 Reps 15 to 20, timed, are
this week's practice.

---

## For the student who is behind

1. Monday's and Tuesday's lecture notes and self-checks
2. Lab U06-03 SCAFFOLDED
3. The port: small scope, finished, with five honest catches
4. Nothing else this week

## For the student who is ahead

1. The nullable reference types page, then find every `?` in your port and justify each one
2. Lab U06-03 EXTENDED
3. The large port scope, and a second interface experiment with a narrower interface
