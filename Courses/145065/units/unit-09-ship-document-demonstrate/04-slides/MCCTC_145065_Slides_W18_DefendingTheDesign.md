# Defending the Design
---
## Slide 1: "What did you decide not to do?"
- Friday, five minutes, a full room
- Someone asks the question above
- "Nothing, really" scores zero
Speaker notes: On Friday, after your five minutes, someone will ask what you decided not to do. If the answer is nothing, really, then as far as anyone can tell you never made a decision. Today you learn to answer that question before anyone asks it.
Image: A presenter at a panel with a raised hand in the audience.
---
## Slide 2: This is a defense, not a tour
- A tour lists what it has
- A defense argues why it is this way
- Decisions need evidence and alternatives
Speaker notes: In 145060 you showed what your app did. That was the right demo then. This time you defend decisions. A tour says it has three tiles. A defense says why a missing value shows no number, shows the proof, and names what you chose not to do.
Image: A feature checklist crossed out, replaced by a claim with an arrow to evidence.
---
## Slide 3: Claim, evidence, rejected option
- Claim: what your design does, in one sentence
- Evidence: something the room can see
- Rejected: the other option, reason, and cost
Speaker notes: Every decision you present has three parts. The claim. The evidence on screen: a requirement, a test, a picture, or a line from your operator test. And the option you rejected, why, and what your choice cost you. That last part is the one that proves you thought.
Image: Three stacked cards labeled claim, evidence, rejected.
---
## Slide 4: Five minutes, five parts
- The one sentence, including "it only watches"
- What it does, including a failure state
- Why it is built this way
- What you rejected
- What is next
Speaker notes: Here is the shape. Thirty seconds for the one sentence. Ninety for what it does, and that must include the alarm surviving a disconnect. Ninety for three decisions with evidence. A minute for two rejected options. Thirty seconds for one known limit. The score sheet follows the same five parts.
Image: A horizontal timeline from 0:00 to 5:00 with five segments.
---
## Slide 5: The live part, from a card
```
python sim_control.py --port 8705 mode drift
200 {"mode": "drift", "meaning": "oven temperature climbs past its alarm threshold and keeps climbing"}

python sim_control.py --port 8705 mode silent
200 {"mode": "silent", "meaning": "the service accepts connections and never answers (MISSING, by timeout)"}
```
Speaker notes: Your partner runs these from a card while you talk. On the build PC the port was 8705; in the lab it is 8700. Drift, wait for red, then silent. Every tile goes dark and the alarm banner stays. That is the moment your whole design exists for. Point at it.
Image: None. This slide is code.
---
## Slide 6: The wrong way: from memory, in front of everyone
```
python sim_control.py --port 8705 mode drfit
usage: sim_control.py mode [-h] [--sensor SENSOR]
                           [{normal,drift,freeze,drop-sensor,silent,garbage}]
sim_control.py mode: error: argument name: invalid choice: 'drfit' (choose from normal, drift, freeze, drop-sensor, silent, garbage)
```
Speaker notes: One typo, typed in a hurry, and the panel stays normal while you describe an alarm nobody can see. The clock keeps running. This is real output. Read commands from a card, and rehearse once, timed, today.
Image: None. This slide is code.
---
## Slide 7: A rejected option, said aloud
- "I rejected keeping the last number, greyed out."
- "An old oven number can hurt someone."
- "It costs a screen that can look empty."
- "So the screen says what empty means."
Speaker notes: This is what the rejected-option part sounds like. The option. The reason. The cost of the choice you made. And what you did about that cost. Four sentences. They come from your decision log, where you wrote them when you made the choice, so they are true, not invented on the spot.
Image: A decision log entry with the Rejected line highlighted in launch blue.
---
## Slide 8: Why presenters skip this
- Features are quick to point at
- Rejections feel like admitting weakness
- Rehearsal feels unnecessary for your own work
Speaker notes: It is natural to point at features, because decisions invite the question why. Rejected options feel like confessing, but they prove you saw more than one way. And you know your project best, which is exactly why you underestimate how fast five minutes goes.
Image: A stopwatch past five minutes beside a presenter still on slide one.
---
## Slide 9: Answering the question you cannot answer
- Say what you know
- Say what you do not know
- Say how you would find out
Speaker notes: One question will stump you. A true I don't know, followed by how you would find out, earns full credit on the score sheet. A confident guess that turns out wrong does not. Nobody on a shop floor trusts a person who guesses about a machine.
Image: A presenter with an open hand and a notebook, calm.
---
## Slide 10: What you are about to build
- Build 1: Gate 2 W18, the release plan review
- Build 2: your demo script and command card
- One timed rehearsal with a partner
- Score each other with the real sheet
Speaker notes: Build 1 is the last Gate 2 of the course, an AI-written release plan. In Build 2 you write your demo script from your decision log, make your command card, and rehearse once with a partner holding a stopwatch and the real score sheet. Tomorrow is the exam and the ship deadline. Friday you defend.
Image: Two students, one presenting, one timing with a score sheet.
