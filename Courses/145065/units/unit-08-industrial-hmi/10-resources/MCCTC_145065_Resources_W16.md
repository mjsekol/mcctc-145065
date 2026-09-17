# Additional Resources · Week 16
## 145065 Object-Oriented Programming · Unit 8 · Week 16
### Topics: stale versus missing, alarm memory, system testing, the post-test

Every link is marked **Opened** (opened while this file was written, title matched), **Confident** (a
long-standing official home page), or **[VERIFY]**. Nothing here needs an account, and nothing asks you
to paste code or personal information into an AI tool.

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | Microsoft Learn: the `switch` expression | Wed | On-level | 15 min |
| 2 | Microsoft Learn: asynchronous programming, "Handle asynchronous exceptions" | Mon, Thu | Extension | 10 min |
| 3 | xUnit | Mon to Thu | On-level | 15 min |
| 4 | Alarm management and HMI design standards | Wed | Extension | 10 min |
| 5 | The disconnect run-book | Thu | On-level | 15 min |
| 6 | WebXam, for the post-test | Tue | On-level | 5 min |
| 7 | Your own lecture notes | Mon, Wed, Thu | On-level | 20 min each |

---

## 1. The `switch` expression

**Microsoft Learn, switch expression (C# reference)** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression` ·
**Opened**.

**Why this one.** Wednesday's latch is a `switch` expression. The page's section "Nonexhaustive switch
expressions" names the `SwitchExpressionException` you saw when the discard arm was missing, and its tip
says why a discard arm makes a `switch` exhaustive.

**Assign:** find the sentence about what the compiler does when a lower arm can never be chosen. Then
explain why `_ => current` must be the **last** arm.

## 2. Exceptions in awaited tasks

**Microsoft Learn, Asynchronous programming (C#)**, section "Handle asynchronous exceptions" ·
`https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/` · **Opened**.

**Why this one.** It explains why `await` gives you the original exception and `.Result` gives you an
`AggregateException`. It is the reason Lab U8-02's `.Result` break crashed instead of reporting a
timeout.

## 3. Testing

**xUnit** · `https://xunit.net/` · **Confident** for the site.

**Why this one.** `[Fact]`, `[Theory]`, `[InlineData]`, and `[MemberData]` are all in this unit's
self-checks. **Version note:** the lab uses xunit 2.5.3. Newer documentation may describe a later major
version. If an example does not build, check which version it is written for.

## 4. Where the ideas come from

Industry standards cover HMI design (ISA-101) and alarm management (ISA-18.2) **[VERIFY the names,
current editions, and where your school can read them]**. They are not free to read in full, and this
course does not require them. The ideas you used this week are the ones they are built on: state shown by
more than color, and an alarm that stays until a person deals with it. **Do not quote a standard you have
not read.**

## 5. The run-book

`09-project/project-files/DISCONNECT_DEMO_RUNBOOK.md`, in your project files. Read section 0, the safety
brief, and section 4, "Things that look wrong and are not," before Thursday.

## 6. The post-test

The WebXam post-test is Tuesday. Your instructor confirms the room, the time limit, and the login
**[VERIFY with the testing coordinator]**. The survey at the end asks whether you want college credit for
this course; according to the syllabus, answering it is how that starts. The official WebXam site is
**[VERIFY]**: use the address your instructor gives you, not a search result.

## 7. Your own notes

`03-lecture-notes/`: Stale Is Not Missing, Alarms That Outlive the Data, Prove It by Breaking It. Each
self-check takes about five minutes.

---

## For the student who is behind

1. Monday's note and Lab U8-04 to 20 of 20
2. Wednesday's note and Lab U8-05 to 23 of 23
3. The project's acceptance tests, all passing
4. The run-book, rehearsed once, with a filled-in `DEMO_RECORD.md`

## For the student who is ahead

1. Resource 1 in full, then rewrite your latch as a table lookup and say what the compiler no longer
   checks
2. The project's large scope list
3. Add a scripted system test of your own to `DEMO_RECORD.md`: one failure the run-book does not include
