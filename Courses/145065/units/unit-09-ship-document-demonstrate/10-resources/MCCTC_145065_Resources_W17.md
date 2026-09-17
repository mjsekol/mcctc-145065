# Additional Resources · Week 17
## 145065 Object-Oriented Programming · Unit 9 · Week 17
### Topic: releases, user help, interfaces and versions, handoff

**About the links.** Every URL is marked with how confident this file is that it exists.

- **Opened** means the page was opened while this file was written and matched the description.
- **Confident** means the resource and address are long established.
- **[VERIFY]** means click it once before assigning it.

Web pages change. Click any link once before you assign it in a later year.

---

## The week at a glance

| # | Resource | Level | Time |
|---|---|---|---|
| 1 | Pro Git, "Git Basics: Tagging" | On-level | 15 min |
| 2 | Microsoft Learn: `dotnet publish` and the publishing overview | On-level | 20 min |
| 3 | Semantic Versioning 2.0.0 | Remediation | 10 min |
| 4 | Keep a Changelog | On-level | 10 min |
| 5 | Write the Docs, software documentation guide | Extension | 20 min |
| 6 | Microsoft Learn: C# records and `init` | Extension | 20 min |
| 7 | Regex tester for Lab U09-01 | On-level | 10 min |
| 8 | Video | deliberately unfilled | |
| 9 | Current article | deliberately unfilled | |
| 10 | Side quests: SQ-24, SQ-17 | Extension | multi-week |

---

## 1. Primary reading

**Pro Git, 2nd edition, section 2.6, "Git Basics: Tagging"** ·
`https://git-scm.com/book/en/v2/Git-Basics-Tagging` · **Opened.**

**What it is.** The free book's section on lightweight and annotated tags, showing tag details with
`git show`, and pushing tags by name or all at once.

**Why this one.** It is the source for Wednesday's baseline commands, and it states plainly the fact
students forget: tags are not pushed unless you push them.

**Time.** 15 minutes. **Level.** On-level.

---

## 2. Official documentation: building a release

**`dotnet publish` command** · `https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish` ·
**Opened.** Lists `-o` and `-c`, says the output includes the `.dll`, `.deps.json`, and
`.runtimeconfig.json`, and notes that with the .NET 8 SDK or later, publishing uses the Release
configuration by default for `net8.0` projects.

**.NET application publishing overview** · `https://learn.microsoft.com/en-us/dotnet/core/deploying/` ·
**Opened.** Explains framework-dependent against self-contained publishing, and the single-file option.

**Give students one question, not the pages:** "Which files in your release folder would be missing if
you copied only the `.exe`, and what does each one do?"

**Time.** 20 minutes. **Level.** On-level.

---

## 3. Version numbers, one more time

**Semantic Versioning 2.0.0** · `https://semver.org/` · **Opened.**

**What it is.** The specification for MAJOR.MINOR.PATCH.

**Why this one.** Students met it in 145060. Assign it only to a student whose Wednesday exit ticket shows
the numbers are fuzzy.

**Time.** 10 minutes, the summary at the top. **Level.** Remediation.

---

## 4. Change logs

**Keep a Changelog, version 1.1.0** · `https://keepachangelog.com/en/1.1.0/` · **Opened.**

**What it is.** A short guide to writing change logs for people: newest first, grouped by kind of
change, one entry per version.

**Why this one.** It matches the course template closely. **One difference to name:** the guide puts a
date on each release. In this course's documents, release headings name the week and day instead, so
the materials can be reused year after year. In your own projects after this course, dated entries are
normal.

**Time.** 10 minutes. **Level.** On-level.

---

## 5. Documentation practice

**Write the Docs, "Software documentation guide"** · `https://www.writethedocs.org/guide/` · **Opened.**

**What it is.** A free community guide to writing documentation, published under a Creative Commons
license.

**Why this one.** For the student whose user guide is already strong and who wants to know how
professional technical writers think about audiences.

**Time.** 20 minutes to skim one section. **Level.** Extension.

---

## 6. Official documentation: the C# behind Wednesday

**Records, C# reference** ·
`https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record` · **Opened.**
Covers positional parameters and init-only properties, which is exactly the Lab U09-02 EXTENDED hint.

**`FileVersionInfo` class** ·
`https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.fileversioninfo` · **Opened.** Lists
`GetVersionInfo` and `ProductVersion`, the Lab U09-01 EXTENDED hint.

**Time.** 20 minutes. **Level.** Extension.

---

## 7. Interactive practice

**regex101** · `https://regex101.com/` · **Opened.** A regular expression tester that explains each part
of a pattern as you type. **[VERIFY]** that a .NET (C#) flavor is selectable before assigning it; the page
opened while this file was written showed the PCRE2 flavor by default, and the flavor list did not load.

**Why this one.** The lookarounds in Lab U09-01 are the hardest pattern students write this year. Seeing
`(?<![A-Za-z0-9_])` explained one piece at a time helps.

**Level.** On-level, Tuesday.

---

## 8. Video, under 20 minutes

**Deliberately unfilled.** No video found for this week could be confirmed as free, under 20 minutes, and
accurate for .NET 8 publishing and versioning at the time this file was written. If you add one, confirm
its length and that it shows framework-dependent publishing, and mark it here.

---

## 9. The current article slot

**Deliberately unfilled.** Pick one current piece about a software update that changed something users
depended on, the week you teach this, and use it Wednesday as a real-world interface change. Find what
changed, who was affected, and whether the version number said so. **[VERIFY]** whatever you choose.

---

## 10. Side quests

**SQ-24 · Ship for a Real Stakeholder** · from `Courses/Misc/MCCTC_Side_Quest_Catalog_2026-2027.md`.
Unlocks in 145010, "or any time with instructor approval." This unit is its rehearsal: scope agreement,
handoff document, and a written answer from the stakeholder.

**SQ-17 · Unit Tests for Something You Already Wrote** · same catalog. For a student whose Unit 8 panel
has thin tests, before Week 18's change needs something to hold it in place.
