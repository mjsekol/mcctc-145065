# Lecture Notes: Defending the Design
## 145065 Object-Oriented Programming · Unit 9 · Week 18, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W18_DefendingTheDesign.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-09-ship-document-demonstrate/04-slides/MCCTC_145065_Slides_W18_DefendingTheDesign.md --export pptx`

If you missed class, you can learn this concept from this file alone.

**Competencies:** 1.2.2, deliver formal presentations. 1.2.5, communicate for an intended audience and
purpose. 5.6.10 is reinforced: presenting a system to its stakeholders.

---

## Why this exists

In 145060 you demonstrated a deployed app in five minutes. You showed what it did. That was the right
demo for a first program.

This one is different. On Friday you are not showing a feature list. You are **defending decisions**.
The shift lead, your instructor, and your classmates will want to know three things: what it does, why
you built it this way, and what you decided not to do. The third is the one that shows you made
decisions at all.

---

## The concept in plain language

**A defense leads with the claim, shows the evidence, and names the option you rejected, with its
reason and its cost.**

For each decision you present, three parts:

| Part | Example |
|---|---|
| **Claim** | "A missing value shows no number." |
| **Evidence**, on screen | the dark tiles, REQ-03, the test that holds it |
| **Rejected option, reason, cost** | "I rejected keeping the last number, greyed out. An old number on an oven screen is how someone gets hurt. The cost is a screen that sometimes looks empty, so I added a sentence that says what empty means." |

**Five minutes, five parts:** the one sentence, what it does, why it is built this way, what you
rejected, what is next. The Unit 9 project spec has the timings and the score sheet.

**The failure state is the heart of the demo.** Anyone's panel looks fine when everything is normal.
Yours is worth defending because of what it does when the data stops.

---

## Worked example 1: the live part, from a card

Your partner runs the simulator from a written card. On the build PC:

```
python sim_control.py --port 8705 mode drift
```

```
200 {"mode": "drift", "meaning": "oven temperature climbs past its alarm threshold and keeps climbing"}
```

Wait for the red tile. Then:

```
python sim_control.py --port 8705 mode silent
```

```
200 {"mode": "silent", "meaning": "the service accepts connections and never answers (MISSING, by timeout)"}
```

Every tile goes dark, and the alarm banner stays up. That is the moment you point at and say the
sentence your design depends on. In the lab the port is 8660.

---

## Worked example 2: evidence you can run

A claim is stronger when the room sees it proven. On the Unit 9 reference panel, this command runs the
three tests behind "a missing value shows no number" and "acknowledge needs a confirmation":

```
dotnet test Line3.Hmi.Core.Tests --filter "FullyQualifiedName~MissingShowsNoNumberAnywhere|FullyQualifiedName~AFailedRequestIsMissingWithNoNumberAtAll|FullyQualifiedName~TheButtonOnlyOpensTheConfirmation"
```

It reported 6 passed: one test, four cases of another, and one more. On your own panel, use your own test
names. A named test, passing on screen, is evidence nobody has to take on trust.

---

## Worked example 3: the rejected option, written down first

The rejected options you present come from your decision log, where they were written when you made the
choice. From the reference:

```
## Week 18, Monday · The fix for finding F1

- Decision: how to stop operators reading NO DATA as "the machine stopped"
- Chosen: one added sentence on every NO DATA tile, and a bold line in the guide
- Rejected: renaming NO DATA; showing the last value greyed out; changing only the guide
- Why: see CHANGE_IMPACT.md, CR-01. The sentence fixes the misreading without changing a trained word
  or breaking REQ-03.
- Cost: a longer sentence on the tile, which had to be rendered in the worst case to prove it fits.
```

In the demo it becomes two sentences said aloud. The log is what makes them true rather than invented
on the spot.

---

## The wrong version, and what it produces

**The unrehearsed demo.** Your partner types from memory, in front of the room:

```
python sim_control.py --port 8705 mode drfit
```

The output, captured on the build PC:

```
usage: sim_control.py mode [-h] [--sensor SENSOR]
                           [{normal,drift,freeze,drop-sensor,silent,garbage}]
sim_control.py mode: error: argument name: invalid choice: 'drfit' (choose from normal, drift, freeze, drop-sensor, silent, garbage)
```

The panel stays normal. You stand in front of the room describing an alarm nobody can see, and your
five minutes are running. **Rehearse once, timed, and read commands from a card.**

**The feature tour.** "It has three tiles. It has an alarm. It has a confirmation box. It has an event
list." Every sentence is true. None is a decision. Asked "what did you decide not to do?", the presenter
says "nothing, really." That answer scores zero on the row that matters most.

---

## Why the wrong version is tempting

**Features are quick to point at.** Decisions are harder to say out loud, because saying them invites the
question "why?"

**Rejected options feel like admitting weakness.** They are the opposite. They prove you saw more than
one way.

**Rehearsing feels unnecessary for your own project.** You know it best, which is exactly why you
underestimate how fast five minutes goes.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Formal presentation** | a planned, timed talk to an audience, with a structure and evidence |
| **Defense** | a presentation that argues for decisions, and answers challenges to them |
| **Claim** | a statement about your design that you intend to prove |
| **Evidence** | something the audience can see that supports a claim: a test, a requirement, a picture, a record line |
| **Rejected option** | an alternative you considered and did not choose, with the reason |
| **Trade-off** | what your choice cost, stated plainly |

---

## Self-check

**Question 1.** Turn this into a claim, evidence, and a rejected option: "My panel has a confirmation box."

**Question 2.** A classmate asks during your questions, "What happens if the Pi's clock is wrong?" and you
are not sure. What do you say?

**Question 3.** Why does the demo show a failure state, when a normal screen looks better?

---

### Answers

**1.** Claim: "Acknowledging an alarm takes two presses, on purpose." Evidence: the confirmation box on
screen, the requirement that a glove brushing the screen must not acknowledge anything, and the test that
the first button only opens the box. Rejected option: "I rejected a single acknowledge button. It is
faster, but a brushed glove could acknowledge an alarm nobody looked at. The cost is one more press for
every real acknowledgement."

**2.** The truth: "I'm not certain. I believe every tile would show STALE even while readings arrive, and
I would check by reading the tests for the stale rule." A true "I don't know,
and here is how I would find out" earns the point. A confident guess does not.

**3.** Because the failure state is what the design is for. Every panel looks right when the data is
fine. Showing that an alarm survives a disconnect, and that no old number appears, is the evidence that
the panel is safe to hand over.
