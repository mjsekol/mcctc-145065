# From Finding to Release
---
## Slide 1: The sheet that hurts to read
- A visitor turned toward the door
- The screen was dark, the oven was not
- You want to open the code right now
Speaker notes: Yesterday someone read your all-dark screen as a stopped line and turned to leave. You have that on paper, with a line number. Your hands want to open the code this second. Today is about the ten minutes between the finding and the fix, and why they matter more than the fix.
Image: A record sheet with one line circled, beside a closed laptop.
---
## Slide 2: Your panel is in maintenance now
- A baseline is tagged
- A shift lead is trained on it
- A guide is on the desk
- Every change reaches people
Speaker notes: After the handoff, your panel is in maintenance, the longest phase any used program has. There is a baseline, a trained owner, and a printed guide. Any change you make lands on all three. So every change is measured against the baseline, on purpose.
Image: A lifecycle strip with the last box, maintenance, highlighted in launch blue.
---
## Slide 3: The path from finding to release
- Decide: code, guide, defer, or no change
- Request, then predict, before any edit
- Change, then hold it with a test
- Measure what really happened
- Release: version, change log, tag
Speaker notes: Seven steps, and the order is the lesson. Decide what kind of fix each finding needs. Write the request and the prediction, and commit the prediction before you touch code. Make the smallest change. Add something that fails if the change is undone. Fill in what actually happened. Then release it with a version chosen by who is affected.
Image: A left-to-right arrow of seven small boxes.
---
## Slide 4: The code change alone
```
Failed Line3.Words.Tests.ScreenWordsTests.TheWordsFileListsExactlyWhatTheCodeCanShow
Failed Line3.Words.Tests.ScreenWordsTests.EachTileStateShowsItsAgreedWord(state: Stale, word: "STALE")
Failed!  - Failed:     2, Passed:    11, Skipped:     0, Total:    13
```
Speaker notes: In the practice library, the change request turns STALE into NOT UPDATING. Change only the code and two tests fail. One says the code and the words file disagree. One says the code and the agreed word disagree. Both are doing their job. Output shortened.
Image: None. This slide is code.
---
## Slide 5: Changing a test is a decision
```csharp
    [InlineData(TileState.Stale, "NOT UPDATING")]
```
Speaker notes: After the words file is fixed, one test still fails, because it records the agreed word. You may change it only because the change request was approved. That is the difference between fixing a test and silencing one. Then all thirteen pass.
Image: None. This slide is code.
---
## Slide 6: The wrong way: green means done
```
Passed!  - Failed:     0, Passed:    13, Skipped:     0, Total:    13
```
Speaker notes: This is the whole output, and the user guide still says STALE, twice. The guide test passed because the top bar says DATA NOT UPDATING, which contains NOT UPDATING. The test found the letters in a different word. Commit now, and the operator's guide teaches a screen that no longer exists.
Image: None. This slide is code.
---
## Slide 7: A test that cannot be fooled that way
```
Failed Line3.Words.Tests.ScreenWordsTests.TheGuideUsesEveryScreenWordOnItsOwn
Collection: ["NOT UPDATING"]
Failed Line3.Words.Tests.ScreenWordsTests.TheGuideNeverUsesARetiredWord
Collection: ["STALE"]
```
Speaker notes: The stronger test removes longer screen words before it searches, and a second one fails if a retired word is still in the guide. Against the unfixed guide, both fail and name the problem. Fix the guide and fifteen of fifteen pass. Output shortened.
Image: None. This slide is code.
---
## Slide 8: Why it is tempting
- Green tests feel like permission
- The finding feels urgent
- Versions feel like bookkeeping
Speaker notes: Green only proves what the tests check. The finding is urgent, which is exactly why the prediction takes five minutes, not an hour. And the version and change log are not bookkeeping: they are the two lines the shift lead reads to decide whether to brief the operators.
Image: A green checkmark with a guide page behind it still showing an old word.
---
## Slide 9: Version by who is affected
- A private rename nobody sees: PATCH
- A clearer sentence on the screen: arguable
- A trained word that changes: MINOR at least
- Something that stops working: MAJOR
Speaker notes: Size does not pick the version. People do. A rename inside the code affects nobody outside it. A word operators were trained on affects every operator. When a change is arguable, and some are, write both sides in your change log, and let the shift lead read your reasoning.
Image: Three people icons of increasing size beside PATCH, MINOR, MAJOR.
---
## Slide 10: What you are about to build
- Build 1: the practice change request, predicted first
- Then: your severity sheet from yesterday's lines
- Build 2: your own change, held by a test
- Version, change log, impact note, tag
Speaker notes: In Build 1 you run the practice change on TileWords, prediction first, and find the check that passes for the wrong reason. Then you turn yesterday's record into decisions with line numbers. In Build 2 you make your own change, hold it with a test, choose the version, write the change log and impact note, and push the tag.
Image: A change log entry above a Git tag, both newly written.
