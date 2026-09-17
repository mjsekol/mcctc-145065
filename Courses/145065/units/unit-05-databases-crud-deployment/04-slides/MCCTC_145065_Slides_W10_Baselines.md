# A Baseline Is the Version Every Change Is Measured Against
---
## Slide 1: Did the update install
- A game patch fixes the bug you reported
- The patch notes say it is fixed
- Your game still has the bug
- Which version are you actually running
Speaker notes: You have seen patch notes that promise a fix you still see on your screen. The first question is always which version you are running. Tomorrow a stranger finds a bug in your app, and you ship a fix. Somebody will ask that same question about your app. Today you make sure you can answer it.
Image: A game settings screen showing a version number beside patch notes, launch blue.
---
## Slide 2: The baseline
- The agreed version every later change is measured against
- Yours is v1.0.0, the first deployed release
- Every change after it is maintenance
- A Git tag marks its exact commit
Speaker notes: This is today's idea, and it is competency five point seven point two. The baseline is the version everyone agrees on. When the tester finds a problem, you can say which version they used, what changed since, and whether the fix is live. Five point seven is about five and a half percent of the WebXam, and this is the first time we teach it.
Image: A timeline with a flag labeled v1.0.0 and later points labeled 1.0.1 and 1.1.0.
---
## Slide 3: Three places, one version
- APP_VERSION in app.py, shown in the footer
- The newest row in RELEASE.md
- What /health answers on the live app
- All three must agree
Speaker notes: The version is written in three places. If any one of them disagrees, the next person who reads it is misled. release_check.py reads all three and compares them, so you never have to trust your memory.
Image: Three cards labeled app.py, RELEASE.md, and /health, joined by an equals sign.
---
## Slide 4: release_check.py agrees
```
app.py APP_VERSION       1.0.0
RELEASE.md newest row    1.0.0
GET /health              1.0.0
OK: release 1.0.0 is consistent.
```
Speaker notes: This is the finished lab app with one version row in RELEASE.md. All three say one point oh point oh, and the script exits with zero. The health line does not need a server. The script builds the app with a throwaway database and asks health through the test client.
Image: None. This slide is code.
---
## Slide 5: MAJOR.MINOR.PATCH
```
a typo fixed on the form:   1.0.0 -> 1.0.1
a late-returns column added: 1.0.1 -> 1.1.0
every bookmarked URL moved: 1.1.0 -> 2.0.0
as text,   '1.10.0' > '1.9.0': False
as numbers, 1.10.0 > 1.9.0:  True
```
Speaker notes: PATCH is a fix that changes nothing else. MINOR is a new feature that breaks nothing. MAJOR breaks something people rely on, like every address they bookmarked. The numbers to the right reset to zero. And look at the last two lines. Compared as text, one point ten comes before one point nine. Versions are numbers, not text.
Image: None. This slide is code.
---
## Slide 6: Tag the commit you deployed
```
git tag -a v1.0.0 -m "Baseline: first deployed release of the tool crib app"
git push origin v1.0.0
git show v1.0.0 --stat
```
Speaker notes: These are standard Git commands. They were not run on the machine that built these materials, so run them in your own project repository after the deploy passes its checklist. Dash a makes an annotated tag, which records who tagged it, when, and a message. A plain push does not send tags, so push the tag by name. Then show it and confirm it is the commit you deployed.
Image: None. This slide is code.
---
## Slide 7: Write the note, forget the code
```
| 1.0.1 | The checkout form names the missing field | The outside tester could not tell what was wrong | outside tester |
```
```
app.py APP_VERSION       1.0.0
RELEASE.md newest row    1.0.1
GET /health              1.0.0
MISMATCH: fix every place before you deploy or tag.
```
Speaker notes: I added a one point oh point one row to RELEASE.md and changed nothing else. Mismatch, exit code one. The release notes say the fix shipped. The app says it did not. What would the tester's supervisor believe? They would send the tester back to the same broken form. Change every place in the same commit, and run the check before every deploy and every tag.
Image: None. This slide is code.
---
## Slide 8: How to watch a tester
- Say only: check out, return, find the report
- Ask them to think out loud
- Do not help, point, or explain
- Write every pause, wrong click, and error, with the time
- Invented badge from your seed data, no personal information
Speaker notes: This is the hardest part of the day. Sit beside them and say only the script. If they ask a question, say what would you try, and write the question down, because the question is a finding. The first time you help, the test stops measuring your app. Give them an invented badge, like T-1041. They type nothing real about themselves.
Image: Two people at a laptop, one using it and one writing on a clipboard with hands off the keyboard.
---
## Slide 9: Sort every problem
- Fix now: goes into 1.0.1
- Fix later: recorded with a reason
- Not a problem: recorded with a reason
- Record the tester's role, never their name
Speaker notes: USER_TEST.md records what they were asked to do and every problem, with what they did, what they expected, and what happened. Then you sort. Tomorrow you fix the fix now list, bump to one point oh point one everywhere, run the check, deploy, and show health with the new version. That loop is competency five point six point seventeen.
Image: Three bins labeled fix now, fix later, and not a problem, with cards dropping into each.
---
## Slide 10: What you are about to build
- Lab U05-02, Part 4: steps 19 through 23
- Write RELEASE.md with its version table
- Run release_check.py until it says OK
- Write the tag commands for your baseline
- Target: 101 of 101, due end of Build 1
Speaker notes: Part 4 finishes the lab. RELEASE.md names the release, says why a release gets a name, lists what it contains, names the three places, and has the version table in the exact shape the checker reads. Lab U05-02 is due at the end of Build 1. In Build 2 you tag v1.0.0 in the first five minutes, then your outside tester arrives.
Image: A terminal showing 101 of 101 self-checks passed beside a tag icon labeled v1.0.0.
