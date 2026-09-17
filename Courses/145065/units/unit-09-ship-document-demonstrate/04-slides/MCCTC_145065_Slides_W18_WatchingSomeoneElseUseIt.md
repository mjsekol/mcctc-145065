# Watching Someone Else Use It
---
## Slide 1: They paused at the red tile
- A stranger stands at your panel
- A tile turns red
- They look at you
- Everything in you wants to help
Speaker notes: In an hour, a person who has never seen your panel will stand in front of it. A tile turns red. They look at you. Every part of you will want to say, press that button. Today you learn why you do not, and what you write down instead.
Image: A visitor glancing sideways at a student standing quietly beside a panel with one red tile.
---
## Slide 2: Your tests cannot answer this
- Tests prove it does what you meant
- They cannot prove a stranger understands it
- Only a stranger can
Speaker notes: You have a hundred-odd tests. They prove the panel does what you meant it to do. Not one of them can tell you whether a person who did not build it can do the job with it. Only watching that person can.
Image: A green test report on one side, a puzzled person at a panel on the other.
---
## Slide 3: Four rules for the session
- Read the consent line word for word
- Say nothing that helps
- Record actions and their exact words
- Name nobody: record a role
Speaker notes: One. Read the consent line exactly, and wait for a yes out loud. Two. No button names, no you can, no did that work, no faces. Three. Left column, what they did, with a time. Right column, their words, in quotes. Four. No names, anywhere. A role, like a welding program student.
Image: A clipboard with two columns, did and said, and no name line.
---
## Slide 4: The one sentence you are allowed
- "What would you do if I were not here?"
- Then stay quiet
- Stuck three minutes: "Let's move on."
Speaker notes: When they ask you anything, you say this sentence and then you stop talking. If they are stuck for three minutes, you say let's move on and you record the task as not done. That is not a failure. That is the finding.
Image: A speech bubble with the sentence, in navy.
---
## Slide 5: Your partner drives the simulator
```
python sim_control.py --port 8705 mode drift
200 {"mode": "drift", "meaning": "oven temperature climbs past its alarm threshold and keeps climbing"}
```
Speaker notes: Behind the divider, your partner switches modes when you signal. This is from the build PC, which uses port 8705; in the lab it is 8660. Read through the real panel 11 seconds later, the oven tile said ALARM HIGH with an unacknowledged alarm banner. The five task cards produce every state in one session.
Image: None. This slide is code.
---
## Slide 6: The wrong way: last session's simulator is still running
```
python sensor_service.py --port 8705
Cannot start: port 8705 is already in use on 127.0.0.1; choose another or stop that program
```
Speaker notes: This is the error that eats the first five minutes of a rotation. The last team's simulator is still running, so yours refuses to start rather than guess. Real output from the build PC. Stop the old one with Control C in its terminal before the visitor sits down. That is why the dry run comes first.
Image: None. This slide is code.
---
## Slide 7: Silent mode still takes commands
```
python sim_control.py --port 8705 read
No answer from http://127.0.0.1:8705: timed out

python sim_control.py --port 8705 mode normal
200 {"mode": "normal", "meaning": "all three sensors answer with values inside their thresholds"}
```
Speaker notes: In silent mode the readings stop, and that is what T5 needs. But mode commands still work, so your partner can always bring the simulator back to normal before the next visitor sits down.
Image: None. This slide is code.
---
## Slide 8: The wrong way: the helpful facilitator
- "You can press the acknowledge button."
- They press it
- Your sheet says "T2: done"
- The record is now false
Speaker notes: This is the mistake everyone wants to make. You help, they succeed, and your sheet says a stranger handled an alarm. They did not. They followed your instruction. On the Monday after the handoff, nobody will be standing there to give it.
Image: A student pointing at a button while a visitor presses it.
---
## Slide 9: What a real record looks like
```
O1 L5 | T5 0:30 | stood back, all three tiles dark | "Everything's off. The line stopped."
O1 L6 | T5 0:40 | turned toward the door            | "So I can go?"
```
Speaker notes: Two lines from the exemplar record, which is a composite. No opinion in either one. Together they became the most important finding of the whole test: a person read an all-dark screen as a stopped machine and started to leave. Compare that to got confused at the end.
Image: None. This slide is code.
---
## Slide 10: Why helping is tempting
- Silence feels rude
- You want the panel to look good
- The fix seems plain to you
Speaker notes: Silence feels rude, and the consent line tells them it is on purpose. The panel is not what is graded today; your record is. And the answer seems plain to you precisely because you built it. That is the whole reason this test exists.
Image: A student with a hand over their own mouth, smiling.
---
## Slide 11: What you are about to build
- Dry run with your partner first
- Run a session: consent, T1 to T5, closing question
- Swap roles for your partner's panel
- Type your record with numbered lines
Speaker notes: Set up your station, then do a five-minute dry run so no command fails in front of a visitor. Run your session by the script, ask the closing question, and walk them out. Swap roles. Then type your record into your project with every line numbered, because tomorrow every finding has to point at a line.
Image: Two stations with a divider, a visitor at one, a partner at a laptop behind the other.
