# Lecture Notes: From Finding to Release
## 145065 Object-Oriented Programming · Unit 9 · Week 18, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W18_FromFindingToRelease.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-09-ship-document-demonstrate/04-slides/MCCTC_145065_Slides_W18_FromFindingToRelease.md --export pptx`

If you missed class, you can learn this concept from this file alone.

**Competencies:** 5.6.17, collect application feedback and maintain the application. 5.7.3, analyze the
impact of changes. 5.7.2, baseline. 5.4.5, test using defined test cases.

---

## Why this exists

Yesterday you watched a stranger use your panel. You have a sheet of numbered lines. Some of them hurt
to read.

The tempting move is to open the code and start fixing. That is how a panel with a baseline, a trained
shift lead, and a guide on the desk turns into a panel nobody can describe. **After the handoff, your
panel is in maintenance**, the longest phase of any program people use. In maintenance, every change is
measured against the baseline, and every change reaches people.

---

## The concept in plain language

**Every finding becomes a decision. Every code decision becomes a change request with a prediction,
then a change, then something that holds it in place, then a new version that says what changed and
why.**

The path, in order:

| Step | What you produce |
|---|---|
| 1. **Decide** | for each finding: fix in code, fix in the guide or card, defer, or no change, each with a reason |
| 2. **Request** | a change request that names the finding and the line numbers |
| 3. **Predict** | a table of everything the change touches, **committed before any edit** |
| 4. **Change** | the smallest change that answers the finding |
| 5. **Hold** | a test or a check that fails if the change is undone |
| 6. **Measure** | the Actual column: what really broke, what did not, what you missed |
| 7. **Release** | a version number chosen by who is affected, a change log entry, a tag |

**The version is chosen by who is affected, not by how many lines changed.** A one-word change that
operators were trained on can be MINOR. A hundred-line refactor nobody can see can be PATCH.

---

## Worked example 1: the code change alone

Lab U09-03's practice library holds the panel's screen words. The change request: the tile word STALE
becomes NOT UPDATING. Change only the code, and run the tests:

```
dotnet test Line3.Words.Tests
```

```
Failed Line3.Words.Tests.ScreenWordsTests.TheWordsFileListsExactlyWhatTheCodeCanShow
Failed Line3.Words.Tests.ScreenWordsTests.EachTileStateShowsItsAgreedWord(state: Stale, word: "STALE")
Failed!  - Failed:     2, Passed:    11, Skipped:     0, Total:    13
```

(Shortened: test names without their timing, and every summary line in this file without its
duration and file name.)
The first failure says the code and the words file now disagree. The second says the code and the agreed
word disagree. Both are the tests doing their job.

---

## Worked example 2: the words file, then the test

Update `docs/screen-words.txt`:

```
Failed!  - Failed:     1, Passed:    12, Skipped:     0, Total:    13
```

The last failure is the test that records the agreed word. **Changing a test is a decision**, and the
approved change request is what allows it. Change the expected word:

```csharp
    [InlineData(TileState.Stale, "NOT UPDATING")]
```

```
Passed!  - Failed:     0, Passed:    13, Skipped:     0, Total:    13
```

Green. And the user guide still says STALE, twice.

---

## Worked example 3: the check that passed for the wrong reason

Why did `TheGuideUsesEveryScreenWord` pass when the guide never mentions the new tile word? Because the
guide's top-bar table says **DATA NOT UPDATING**, and "NOT UPDATING" is inside it. The test found the
letters, in a different screen word.

A stronger test removes every longer screen word before it searches, and a second test fails if a
retired word is still in the guide. Against the unfixed guide:

```
Failed Line3.Words.Tests.ScreenWordsTests.TheGuideUsesEveryScreenWordOnItsOwn
Assert.Empty() Failure: Collection was not empty
Collection: ["NOT UPDATING"]
Failed Line3.Words.Tests.ScreenWordsTests.TheGuideNeverUsesARetiredWord
Assert.Empty() Failure: Collection was not empty
Collection: ["STALE"]
```

Fix the guide, and 15 of 15 pass. Then the release:

```xml
<Version>1.1.0</Version>
```

```
## 1.1.0 · Week 18 Tue

- Changed for operators: a tile whose reading is too old now says NOT UPDATING instead of the old word.
  The meaning is the same. The guide's tile table and warning sentence changed with it.
```

and, in your own repository, the tag:

```
git tag -a v1.1.0 -m "CR-18-01: NOT UPDATING replaces the old tile word"
git push origin v1.1.0
```

---

## The wrong version, and what it produces

**Fix first, think later.** You change the word, run the tests until they are green, and commit.

```
Passed!  - Failed:     0, Passed:    13, Skipped:     0, Total:    13
```

That is the whole output. No error. The release goes on the panel, and the guide on the desk still
teaches STALE, a word the screen no longer shows. The next operator test finds it, if there is one.

**A prediction would have caught it.** Anyone who wrote "Documents: the guide's tile table" before
touching the code would have opened the guide.

---

## Why the wrong version is tempting

**Green tests feel like permission.** They only prove what they check.

**The finding feels urgent.** It is, which is why the prediction takes five minutes and not an hour.

**Versions feel like bookkeeping.** The shift lead decides whether to brief operators from your version
number and your change log. Those two lines are the part of the release a person reads.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Maintenance** | the lifecycle phase after deployment: fixing, improving, and responding to feedback |
| **Change request** | a written request for one change, naming its reason and evidence |
| **Prediction table** | the change impact analysis, written and committed before the change |
| **Regression test** | a test that fails if a fixed problem comes back |
| **Retired word** | a screen word the software no longer shows, which documents must stop using |
| **Release tag** | a Git tag naming the commit that was released, such as `v1.0.1` |
| **Change log** | the file that lists every release, newest first, with what changed and why |

---

## Self-check

**Question 1.** Your operator test found that a visitor expected the red tile to turn normal after
acknowledging. The confirmation box already says it stays red. Which of the four decisions fits, and
why?

**Question 2.** You change one explanation sentence on the panel. No existing test fails. Why is that not
good news by itself, and what do you add?

**Question 3.** Two changes: A renames a private method with no visible effect. B changes a word on the
screen that operators were trained on. Which gets the larger version bump, and why?

---

### Answers

**1.** Fix in the guide only. The screen already says it, so the gap is in what the operator read before
the moment, not in the panel. Add a sentence to the guide's acknowledge section, and record the decision
with the line number.

**2.** It means no test was checking that sentence, so a later change could delete it and nothing would
fail. Add a test that fails if the new sentence is missing.

**3.** B. Nobody outside the code is affected by A, so it is at most a PATCH. B changes something people
depend on, their trained vocabulary, so it is at least MINOR, and the shift lead must brief operators
before it ships.
