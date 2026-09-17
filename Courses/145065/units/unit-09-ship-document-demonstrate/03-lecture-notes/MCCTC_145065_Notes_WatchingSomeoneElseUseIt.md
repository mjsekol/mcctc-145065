# Lecture Notes: Watching Someone Else Use It
## 145065 Object-Oriented Programming · Unit 9 · Week 18, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W18_WatchingSomeoneElseUseIt.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-09-ship-document-demonstrate/04-slides/MCCTC_145065_Slides_W18_WatchingSomeoneElseUseIt.md --export pptx`

If you missed class, you can learn this concept from this file alone. You still have to run a session:
see your instructor.

**Competencies:** 5.6.17, collect application feedback. 5.6.14, ensure quality through user acceptance
testing.

---

## Why this exists

In Week 10 someone outside the class used your CRUD app, and you fixed what they broke. That was a web
page, and the person could click around. Today the person is standing in front of a panel beside a
machine, holding your guide, and the question is harder: **can they do the job with what you gave them?**

Your tests prove the panel does what you meant. They cannot prove a stranger understands what you
meant. Only a stranger can.

---

## The concept in plain language

**An operator test is observed, not assisted. You record what the person did and said, not what you
think they meant, and every finding points at a line in that record.**

### Four rules

| Rule | Why |
|---|---|
| **Read the consent line word for word**, and wait for a yes out loud | the person must know nothing is recorded and they can stop at any time |
| **Say nothing that helps**: no button names, no "you can", no "did that work?", no faces | help hides exactly the problem you are there to find |
| **Record actions on the left, their words on the right**, with the task and a time | an action is evidence; your interpretation is not |
| **Name nobody.** Record a role: "a welding program student" | no personal data goes in any record, ever |

When the person asks you a question, say: **"What would you do if I were not here?"** Then stay quiet.

### Tasks, not tours

A task card gives a starting point, a goal, and a reason a real operator would have. It never names a
button or a screen word, and it never says something is wrong.

> Your lead asks whether the oven number on the screen can be trusted right now. Find out and tell me.

Your partner, out of sight, switches the simulator so the screen has something to show.

---

## Worked example 1: the partner's first command

Before a session, the partner starts the simulator. If the last team's simulator is still running, the
port is taken. The build PC, on its own port, printed:

```
python sensor_service.py --port 8705
```

```
Cannot start: port 8705 is already in use on 127.0.0.1; choose another or stop that program
```

The service refuses rather than guess. Stop the old one with Ctrl+C in its terminal, or use another
port and point the panel at it. In the lab, the port is 8660.

---

## Worked example 2: switching modes during the session

The partner switches modes from a second terminal when the facilitator signals. On the build PC:

```
python sim_control.py --port 8705 mode drift
```

```
200 {"mode": "drift", "meaning": "oven temperature climbs past its alarm threshold and keeps climbing"}
```

The published panel, read through Windows UI Automation 11 seconds later, showed the oven tile
`ALARM HIGH` with the banner `UNACKNOWLEDGED ALARM`. After `mode freeze` and 7 seconds, every tile read
`STALE` with `NOT LIVE`, and the badge read `DATA NOT UPDATING`. The cards produce every state the guide
describes in one session.

---

## Worked example 3: the silent mode still takes commands

```
python sim_control.py --port 8705 mode silent
```

```
200 {"mode": "silent", "meaning": "the service accepts connections and never answers (MISSING, by timeout)"}
```

```
python sim_control.py --port 8705 read
```

```
No answer from http://127.0.0.1:8705: timed out
```

Readings stop, but mode commands still work, so the partner can always bring the simulator back:

```
python sim_control.py --port 8705 mode normal
```

```
200 {"mode": "normal", "meaning": "all three sensors answer with values inside their thresholds"}
```

---

## Writing it down

A good record, from the Unit 9 exemplar (a composite):

| Line | Time | What they did | What they said |
|---|---|---|---|
| O1 L5 | T5 0:30 | stood back from the screen, all three tiles dark | "Everything's off. The line stopped." |
| O1 L6 | T5 0:40 | turned toward the door | "So I can go?" |

Two lines. No opinion. They became the most important finding of the whole test: an all-dark screen read
as a stopped machine.

A weak record of the same moment: "Got confused at the end."

---

## The wrong version, and what it produces

**The helpful facilitator.** The visitor pauses at the red tile. You say, "You can press the acknowledge
button." They press it. Your sheet says "T2: done."

The record is now false. It says a stranger handled an alarm. A stranger handled an alarm **after you
told them how**. The Monday after the handoff, nobody will be there to tell them.

What it produces is not an error message. It is a clean sheet, a panel that ships unchanged, and the
first real operator stuck at exactly the place the visitor paused.

**If you slip, write it down.** The sheet has a box for it. A slip you record is still usable evidence.
A slip you hide turns a real finding into a false pass.

---

## Why the wrong version is tempting

**Silence feels rude.** The consent line says the silence is on purpose. Believe it.

**You want the panel to look good.** It is not being graded on this session. Your record is.

**The fix is obvious to you.** That is the point. It was not obvious to them.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Operator test** | a session in which a person who did not build the system uses it for real tasks while the builder watches |
| **User acceptance testing** | testing whether the people who will use a system can do their work with it |
| **Facilitator** | the person running the session, who reads the script and records, and does not help |
| **Consent line** | the fixed words read before a session, including that nothing is recorded and the person can stop |
| **Task card** | a starting point, a goal, and a reason, with no button names and no hint that anything is wrong |
| **Finding** | something a person did or said, cited by line number, that may call for a change |
| **Feedback** | information from the people who use a system, collected so it can be improved |

---

## Self-check

**Question 1.** Your visitor asks, "Is the red one bad?" Write exactly what you say.

**Question 2.** Rewrite this record line so it is evidence: "T3: they didn't really get the stale thing."

**Question 3.** Your record has a first name on it, in the corner. What do you do before committing, and
why does it matter even if the name is only a first name?

---

### Answers

**1.** "What would you do if I were not here?" Then stay quiet.

**2.** Any version that records an action and the person's own words, with a time, for example:
"T3 0:40 · read the number in the oven tile's last-value box aloud as the current temperature ·
'It's two-thirty-four, so it's hot.'"

**3.** Remove it, and record a role instead, such as "an office staff member." A first name, together with
the date, the room, and the program, can identify a real person, and no personal data goes in any record.
