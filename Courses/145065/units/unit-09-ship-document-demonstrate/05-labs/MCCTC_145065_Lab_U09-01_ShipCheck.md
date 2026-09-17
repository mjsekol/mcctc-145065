# Lab U09-01 · ShipCheck
## 145065 Object-Oriented Programming · Unit 9 · Week 17, Monday and Tuesday

**Files:** `lab-u09-01-files/`
**Time:** Part 1 in Monday Build 1. Part 2 in Tuesday Build 1.
**Due:** Part 1 at the end of Monday Build 1. Part 2 at the end of Tuesday Build 1.
**Competencies:** 5.6.8 (documentation), 5.7.1 (version management), 5.2.4 (string operations),
5.3.6 (repetition), 5.4.5 (test with defined test cases).

**No hardware today.** This lab reads files. It never touches the Pi, a sensor, or the panel PC.

---

## The scenario

On Friday you hand your panel to a shift lead, with a change log, an implementation plan, and a user
guide. Last year a team shipped a folder whose change log said 1.0.0, whose program said 1.0.1, and
whose guide described a button the panel no longer had, and nobody noticed until an operator did.
(That team is a composite. The mistake is common.)

**You will build a C# tool that reads a ship folder and reports, in plain sentences, every place its
documents disagree with each other or with the panel.**

You run it on your own ship folder for the rest of the unit.

---

## What is in the folder

| Path | What it is |
|---|---|
| `ShipCheck/Program.cs` | the command line. Finished. Prints one line per check and sets the exit code. |
| `ShipCheck/ShipFolder.cs` | finds and reads files in a ship folder. Finished. |
| `ShipCheck/ReleaseVersion.cs` | a MAJOR.MINOR.PATCH version held as three numbers. Finished. |
| `ShipCheck/CheckResult.cs` | what one check found: PASS, FAIL, or TODO. Finished. |
| `ShipCheck/Checks.cs` | **the seven checks. One is written. You write six.** |
| `ShipCheck.Tests/` | 27 xunit tests. They are the acceptance criteria. Do not edit them. |
| `sample-ship/` | a ship folder with five planted problems. You run ShipCheck on it. You do not fix it. |

**The ship folder layout ShipCheck expects** is the one the Unit 9 project requires:

```
your-ship-folder/
  README.md
  CHANGELOG.md
  docs/
    IMPLEMENTATION_PLAN.md
    USER_GUIDE.md
    HANDOFF_LETTER.md
    screen-words.txt
    screens/            pictures the guide links to
  ...somewhere below: the panel's .csproj with <UseWPF>true</UseWPF> and <Version>
```

The starter builds and runs. It reports six checks as TODO.

---

# Part 1 · One version everywhere · Monday Build 1 · 35 minutes

**Why first.** A version number is the one fact the program, the change log, and the plan all state.
If they disagree, nobody can say what is installed.

**Step 1.** Copy `lab-u09-01-files/` into your repository as `oop-semester/unit-09-shipcheck/`. Open a
terminal in that folder.
*You should see* two project folders and `sample-ship/`.

**Step 2.** Run the tests.

```
dotnet test ShipCheck.Tests
```

*You should see* a last line with `Failed: 23, Passed: 4, Total: 27`. The four that pass test code
that is already finished.

**Step 3.** Run the tool on the sample.

```
dotnet run --project ShipCheck -- sample-ship
```

*You should see:*

```
PASS  required files         all 6 present
TODO  project version        this check has not been written yet
TODO  changelog version      this check has not been written yet
TODO  plan version           this check has not been written yet
TODO  screen words in guide  this check has not been written yet
TODO  no jargon in guide     this check has not been written yet
TODO  pictures exist         this check has not been written yet
1 of 7 checks passed.
```

(The first line, `ShipCheck on ...`, shows the full path of the folder and is left out here.)

**Step 4.** Read `RequiredFiles` in `Checks.cs`. It is the pattern for every check: find the problems,
then pass or fail with a detail that names exactly what is wrong. Write `ProjectVersion` in the same
shape. The comment above the TODO lists the three failure sentences the tests expect.
*You should see,* after running step 3 again:
`PASS  project version        Line3.Hmi.Panel.csproj says 1.0.1`

**Step 5.** Write `ChangelogVersion`. You need the project version again, so write a private helper,
`TryGetProjectVersion(ShipFolder ship, out ReleaseVersion version)`, and use it here and in step 6.
Compare two `ReleaseVersion` values with `==`, never two strings.
*You should see:*
`FAIL  changelog version      newest entry is 1.0.0, the project says 1.0.1`

**Step 6.** Write `PlanVersion`. The plan must name the version as a whole token: a plan that says
`1.0.10` does not name `1.0.1`.
*You should see:*
`FAIL  plan version           the plan never names 1.0.1`

**Step 7.** Run the tests.
*You should see* `Failed: 11, Passed: 16`. Every test in `Part1OneVersionEverywhere` passes. The 11
failures are Part 2 and the two whole-program tests.

**Step 8.** Read the two FAIL lines on `sample-ship`. In `unit-09-shipcheck/RESULTS.md`, write one
sentence for each: which file is wrong, and which commit should have changed it. Commit.
*You should see* your commit in `git log --oneline`.

### Part 1 acceptance criteria

- [ ] `Part1OneVersionEverywhere`: 14 of 14 pass
- [ ] ShipCheck on `sample-ship` shows the three lines from steps 4, 5, and 6 exactly
- [ ] No check compares versions as strings
- [ ] `RESULTS.md` has two sentences, each naming a file and a commit

---

# Part 2 · A guide written for the screen · Tuesday Build 1 · 35 minutes

**Why.** An operator learns the words on the screen from the guide. A word the guide never uses is a
word the operator meets for the first time in the middle of a problem.

**Step 9.** Open `sample-ship/docs/screen-words.txt`. Count the words that are not comments.
*You should see* 18.

**Step 10.** Write `ScreenWordsInGuide`. Skip blank lines and lines that start with `#`. Match with
`StringComparison.Ordinal`, because the screen says STALE in capitals.
*You should see:*
`FAIL  screen words in guide  missing from the guide: DATA NOT UPDATING, ALARM ENDED, NOT ACKNOWLEDGED`

**Step 11.** Write `NoJargonInGuide`. Each term must match as a **whole word**, ignoring case. Build one
`Regex` per term from `Regex.Escape(term)`, with lookarounds that refuse a letter, digit, or underscore
on either side.
*You should see:*
`FAIL  no jargon in guide     an operator would have to read: JSON`

**Step 12.** Write `PicturesExist`. Links in the guide are relative to `docs/`.
*You should see* the whole report end like this:

```
PASS  required files         all 6 present
PASS  project version        Line3.Hmi.Panel.csproj says 1.0.1
FAIL  changelog version      newest entry is 1.0.0, the project says 1.0.1
FAIL  plan version           the plan never names 1.0.1
FAIL  screen words in guide  missing from the guide: DATA NOT UPDATING, ALARM ENDED, NOT ACKNOWLEDGED
FAIL  no jargon in guide     an operator would have to read: JSON
FAIL  pictures exist         not found: screens/panel-stale.png
2 of 7 checks passed.
```

**Step 13.** Run the tests.
*You should see* `Passed: 27, Total: 27`.

**Step 14.** Run ShipCheck on your own ship folder, the one the Unit 9 project builds.

```
dotnet run --project ShipCheck -- ..\path\to\your\ship-folder
```

Copy the report into `RESULTS.md` under "Tuesday". Commit. It will not pass yet. That is the point: it
is your to-do list for the week.

**Step 15.** Look again at the screen-words FAIL on `sample-ship`. Open its user guide and find the
sentence that should have used ALARM ENDED, NOT ACKNOWLEDGED. Write in `RESULTS.md` what that sentence
gets wrong, and whether ShipCheck could ever catch that kind of mistake.

### Part 2 acceptance criteria

- [ ] `dotnet test ShipCheck.Tests`: 27 of 27
- [ ] ShipCheck on `sample-ship` prints the eight lines in step 12 exactly
- [ ] "threads" and "Rapid" do not count as jargon
- [ ] `RESULTS.md` holds your own folder's first report and the step 15 answer

---

## If it breaks

**1. `error CS0019: Operator '==' cannot be applied to operands of type 'string' and 'ReleaseVersion'`**
You compared the text from the file with a `ReleaseVersion`. The compiler refused to guess. Parse the
text with `ReleaseVersion.TryParse` first, then compare two `ReleaseVersion` values.

**2. `error CS1620: Argument 2 must be passed with the 'out' keyword`**
`TryParse` hands its result back through an `out` parameter. Write
`ReleaseVersion.TryParse(raw, out ReleaseVersion version)`. The `out` goes at the call, not only in the
method.

**3. `Unhandled exception. System.IO.FileNotFoundException: Could not find file '...\CHANGELOG.md'.`**
You called `ship.Read` on a file that is not there. The folder you ran on is missing it, which is a
real finding, but a checker must report it, not crash on it. Check `ship.Has(...)` first and return a
FAIL that names the missing file.

**4. A test fails with `Assert.Equal() Failure: Values differ` and `Expected: Pass` / `Actual: Fail`, in
`JargonMatchesWholeWordsOnly`.**
You used `guide.Contains(term, ...)`. "Rapid" contains "api" and "threads" contains "thread", so your
check reported `an operator would have to read: API, thread` for a sentence about bolts. Match whole
words with the regular expression step 11 describes.

**5. `ScreenWordsMustMatchTheCapitalsOnTheScreen` fails with `Expected: Fail` / `Actual: Pass`.**
You compared with `OrdinalIgnoreCase`. A guide that says "stale" never teaches the word STALE. Use
`StringComparison.Ordinal`.

---

## Stretch goal

Add an eighth check, `changelog order`: every version heading in `CHANGELOG.md` must be **older** than
the one above it. Use `ReleaseVersion.CompareTo`, never a string comparison. Write two tests for it
first: one change log in the right order, and one with `1.0.10` listed below `1.0.9`.

---

## Submission checklist

- [ ] `unit-09-shipcheck/` committed with your six checks
- [ ] 27 of 27 tests pass
- [ ] `RESULTS.md`: Part 1 sentences, Tuesday report, step 15 answer
- [ ] No `bin` or `obj` folders committed
- [ ] You can explain every line of every check you wrote. That is the one way to fail this program.

---

# Extended options

All four assess the same competencies on the same scale: the tests in `ShipCheck.Tests` (or the
version named below) and the report on `sample-ship`.

## SCAFFOLDED

**Same target, smaller steps.** Your instructor gives you a `Checks.cs` in which `TryGetProjectVersion`
is already written and each TODO has its first two lines filled in: the file read and the loop header.

**Checkpoints.** Show your instructor the step 4 output before you start step 5, and the step 10 output
before you start step 11.

**Smaller scope.** Skip step 15 and the stretch goal. You still need 27 of 27.

## STANDARD

The lab as written.

## EXTENDED

Add an eighth check, `release stamp`. After `dotnet publish`, the program file under `release/` carries
a version stamp. The check finds every `<project name>.exe` under `release/` and fails if its stamp does
not match the project version. The part after `+` in the stamp is a commit id; ignore it.

The class that reads a program file's stamp is in `System.Diagnostics`. Its documentation page is the
hint: learn.microsoft.com, search for `FileVersionInfo` and read `GetVersionInfo` and `ProductVersion`
[VERIFY the page before you start]. Write three tests first: a matching stamp, a stamp from an older
build, and no `release/` folder.

**How you know it works.** On a ship folder whose project says 1.0.2 and whose release folder holds a
1.0.1 build, your check prints a FAIL naming the file and the version it found.

## APPLIED

**Same skill, a different folder.** Point the same idea at the thing you use every day: a folder of
game mods, a band's shared setlist folder, or your own `oop-semester` repository. Write a `FolderCheck`
with three checks that matter for that folder, in the same `CheckResult` shape, with a test for each.
For the repository, good choices are "every unit folder has a README", "no file over 5 MB", and "no
`bin` or `obj` folder anywhere".

**Why this version.** The skill is "turn a promise documents make into a check a program can run." It
has nothing to do with operator panels.

---

## Which version, three observable signals

| If you see | Hand them |
|---|---|
| After 15 minutes of Part 1, the student has not got `ProjectVersion` to print anything but TODO, or is comparing strings | **SCAFFOLDED** |
| The student reaches step 7 before Monday's reset | **EXTENDED**, after they finish Part 2 on Tuesday |
| The student asks "why would anyone check a README with code?" | **APPLIED**. The problem is that they cannot see the use yet, and their own repository will show them in five minutes. |
