# Prove It by Breaking It
---
## Slide 1: Every test is green
- The freshness rule passes
- The latch passes
- The client passes
- Does the alarm survive a pulled cable?
Speaker notes: Every lab this unit ended green. The freshness rule passes. The latch passes. The client gives up on time. None of that proves the sentence your client cares about: when the cable is pulled during an alarm, the operator still sees the alarm. That sentence involves every piece at once. Tomorrow you pull the plug in front of an audience. Today you learn to do it as a test, not a stunt.
Image: A wall of green checkmarks with one unplugged cable in front.
---
## Slide 2: Three kinds of test
- Unit test: one piece, alone
- System test: the whole system, one requirement
- User acceptance: the real user at the controls
- Each proves something the others cannot
Speaker notes: A unit test checks one piece, alone, with its inputs controlled. It is fast and blind to everything around it. A system test checks one requirement with the whole system running: service, network, client, rules, window. User acceptance testing puts the real user at the controls, and that is Unit 9's operator test. Each proves something the others cannot.
Image: Three nested boxes labelled piece, system, and person.
---
## Slide 3: A system test has a script
- Put the system in a known state
- Break one thing
- Observe, after waiting long enough
- Record the words, then restore
Speaker notes: A system test is not a stunt, because it has a script. Put the system in a known state: service running, panel connected, values normal. Break exactly one thing. Wait long enough for the rule to act, and read the screen. Record the words the screen showed, next to the requirement they prove. Then restore, and check the system recovers.
Image: A clipboard with five numbered steps.
---
## Slide 4: A scripted test, in miniature
```csharp
int sinceChange = step - stepSequenceChanged;
string expected = sinceChange > 5 ? "STALE" : "NORMAL";
string both = sampleAgeSeconds > 5 || sinceChange > 5 ? "STALE" : "NORMAL";
string timestampOnly = sampleAgeSeconds > 5 ? "STALE" : "NORMAL";
```
```
   8  seq 3, age 0  NORMAL     NORMAL        NORMAL
   9  seq 3, age 0  STALE      STALE         NORMAL FAIL
```
Speaker notes: This program plays a Pi that freezes at step three and keeps re-stamping the same reading. Two panels watch it. One checks the sequence, one trusts the timestamp. Each row compares what the panel shows with what the requirement expects. Eight rows agree. The ninth is the one that matters. A test that stopped at step eight would have passed both panels.
Image: None. This slide is code.
---
## Slide 5: The wrong way: never breaking anything
```
   9  seq 3, age 0  STALE      STALE         NORMAL FAIL
```
Speaker notes: Here is the wrong way. A test suite built only from healthy replies. Every test is green, and the first frozen Pi on the shop floor shows normal forever. The failure only appears when the system is broken long enough, which this row shows. Green tests are evidence about the cases they try. They say nothing about the cases they skip. Wait long enough, every time.
Image: None. This slide is code.
---
## Slide 6: The run-book is a system test
- Freeze: wait about 6 s, expect STALE
- Silent: wait about 3 s, expect NO DATA
- Disconnect in alarm: banner still up
- Every step names what it proves
Speaker notes: The disconnect run-book in your project files is a system test written out. Freeze the simulator, wait about six seconds, expect stale everywhere and the oven banner still up. Make it silent, wait about three seconds, expect no data, and drag the window to prove it still responds. Then the strongest step: stop the service during an alarm, and the banner must still be there.
Image: A printed run-book page with a "Wait" column highlighted.
---
## Slide 7: A record someone else can check
- Not: "it worked"
- The words the screen showed
- How long you waited
- The requirement each step proves
Speaker notes: The record is not it worked. Nobody who was not in the room can check it worked. Write the words the screen showed, like no connection, every tile no data, unacknowledged alarm still present. Write how long you waited. Write which requirement the step proves. That is evidence someone else can check, and it goes in DEMO_RECORD dot md.
Image: A two-column notebook page: what we did, what we saw.
---
## Slide 8: Break one thing at a time
- Two breaks, one screen: which caused what?
- Freeze, observe, restore
- Then stop the service, observe, restore
- Safety brief before any Pi step
Speaker notes: Break one thing at a time. If you freeze the Pi and pull the cable together, a no data tile does not tell you whether the stale rule worked. Freeze, observe, restore. Then stop the service, observe, restore. On the lab Pi, breaking one thing means pulling the network cable with me present, after the safety brief, never touching power or wiring while it is on.
Image: A single hand pulling one network cable from a small board, instructor nearby.
---
## Slide 9: What you are about to build
- Rehearse the run-book, steps 1 to 9
- Fill in DEMO_RECORD.md from what you see
- Five minutes, timed, both partners speaking
- Demonstrations begin in Build 2
Speaker notes: In build one you rehearse the whole run-book with your partner, against the simulator on port 8700, and fill in DEMO_RECORD dot md from what you actually see. Time it: five minutes, and both partners speak. Build two starts the demonstrations, and anyone who missed the post-test takes the make-up at the side table. Tomorrow the rest of the demos run after the quiz and Gate 2.
Image: Two students at a laptop, one holding a stopwatch.
---
