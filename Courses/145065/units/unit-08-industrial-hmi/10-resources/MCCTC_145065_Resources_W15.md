# Additional Resources · Week 15
## 145065 Object-Oriented Programming · Unit 8 · Week 15
### Topics: requirements, calling another program, truth tables, dataflow, the operator's workplace

Every link is marked one of three ways. **Opened** means the page was opened while this file was
written, and its title matched. **Confident** means the address is a long-standing official home page.
**[VERIFY]** means check the address before you rely on it. Nothing here needs an account, and nothing
asks you to paste code or personal information into an AI tool.

| # | Resource | For | Level | Time |
|---|---|---|---|---|
| 1 | WCAG 2.1, Contrast (Enhanced) | Mon | On-level | 10 min |
| 2 | U.S. Department of Labor, YouthRules | Mon | On-level | 15 min |
| 3 | Ohio's minor labor law pages | Mon | On-level | 10 min |
| 4 | ADA.gov | Mon | On-level | 10 min |
| 5 | OSHA, young workers | Mon | Extension | 10 min |
| 6 | Raspberry Pi documentation | Mon | Extension | 20 min |
| 7 | Microsoft Learn: asynchronous programming | Tue | On-level | 25 min |
| 8 | `HttpClient` and `CancelAfter` reference pages | Tue | Extension | 15 min |
| 9 | Microsoft Learn: JSON in .NET | Thu | On-level | 10 min |
| 10 | Your own lecture notes | Mon to Thu | On-level | 20 min each |

---

## 1. Contrast you can measure

**WCAG 2.1, Understanding Success Criterion 1.4.6: Contrast (Enhanced)** ·
`https://www.w3.org/WAI/WCAG21/Understanding/contrast-enhanced.html` · **Opened**.

**Why this one.** Monday's REQ-11 uses the 7:1 ratio. This page is where that number comes from: it is
the enhanced level (AAA) for normal text, with 4.5:1 allowed for large text.

**Assign a question:** *which people is the 7:1 level meant to help?* Then say why a shop floor under
glare is a good place to aim for it.

## 2. Young workers, federal

**YouthRules, U.S. Department of Labor, Wage and Hour Division** ·
`https://www.dol.gov/agencies/whd/youthrules` · **Opened**.

**Why this one.** The official federal site about labor rules for workers under 18. Read it at the
purpose level: why the rules exist, and what kinds of work they limit. **This course gives no legal
advice.** Questions about a real job go to the employer and these official sources.

## 3. Young workers, Ohio

**Ohio's minor labor law pages**, published by the Ohio Department of Commerce **[VERIFY the address
and the agency before sharing]**. State rules apply alongside federal ones. Search the state's official
site, not a summary written by someone else.

## 4. Accessibility at work

**ADA.gov, U.S. Department of Justice, Civil Rights Division** · `https://www.ada.gov/` · **Opened**.

**Why this one.** The official site for the Americans with Disabilities Act. Read the purpose, not the
fine print: a qualified person gets reasonable accommodation to do the job. Your panel supports that by
never relying on color alone.

## 5. Young worker safety

**OSHA, young workers** · `https://www.osha.gov/young-workers` **[VERIFY]**. The page refused an automated
request when this file was written, so the address is unconfirmed.

## 6. The Pi

**Raspberry Pi Documentation, Raspberry Pi Ltd** · `https://www.raspberrypi.com/documentation/` ·
**Opened**.

**Why this one.** The official source for the Pi's operating system, configuration, and pins. The lab's
Pi steps are marked [VERIFY]; this is where to check them. **Read it. Do not wire anything from it**
without the safety brief, your signed agreement, and your instructor present.

## 7. `async` and `await`

**Microsoft Learn, Asynchronous programming (C#)** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/` · **Opened**.

**Why this one.** The breakfast example explains "don't block, await instead" in the same terms as
Tuesday. It also explains why a faulted task holds an `AggregateException`, which is the wrapper you saw
when `.Result` crashed.

**Honest caution.** The page's examples use `Console` programs and `Task.Delay`. Your panel waits on the
network. The idea is the same.

## 8. The exact APIs

**`HttpClient` class** · `https://learn.microsoft.com/en-us/dotnet/api/system.net.http.httpclient` ·
**Opened**. **`CancellationTokenSource.CancelAfter`** ·
`https://learn.microsoft.com/en-us/dotnet/api/system.threading.cancellationtokensource.cancelafter` ·
**Opened**.

**Assign:** in the `CancelAfter` page, find what happens if you call it twice. Could that matter to a
panel that polls every second?

## 9. JSON in .NET

**Microsoft Learn, Serialize and deserialize JSON using C#** ·
`https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview` · **Opened**.

**Why this one.** It names `JsonDocument`, the read-only view the parser in Thursday's example uses.

## 10. Your own notes

The four lecture notes in `03-lecture-notes/` are written so you can learn each day's concept from the
file alone. Their self-checks are the fastest review before the practice test.

---

## BPA and side quests

**BPA 330 C# Programming.** The review bank's section A is event practice. Confirm this year's event
guidelines on the official BPA site **[VERIFY]**.

**SQ-15 Same Program, Two Languages** fits this week: port `bench_check.py` to a C# console app. See
`Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.

## For the student who is behind

1. The lecture notes' self-checks, Monday through Thursday
2. Lab U8-02 to 14 of 14, because Week 16 builds on it
3. Resource 7, the first two sections only
4. Nothing else this week

## For the student who is ahead

1. Resources 1 and 7 in full
2. The EXTENDED option of each lab
3. Resource 6's configuration pages, then write the questions you would ask before wiring the probe
