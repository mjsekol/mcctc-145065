# Lecture Notes: Handing It Over
## 145065 Object-Oriented Programming · Unit 9 · Week 17, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W17_HandingItOver.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-09-ship-document-demonstrate/04-slides/MCCTC_145065_Slides_W17_HandingItOver.md --export pptx`

If you missed class, you can learn this concept from this file alone.

**Competencies:** 5.6.15, train stakeholders. 1.2.11, write professional correspondence. 1.2.5,
communicate for an intended audience and purpose.

---

## Why this exists

A panel nobody else can run is a hobby. Tomorrow your panel becomes somebody else's: the Line 3 shift
lead, who decides when it runs and who uses it, and who will be standing beside it when you are not.

Two things have to cross from you to them. **A skill:** they can use it, and teach an operator to use
it. **A responsibility:** they know what they own, what it does not do, and who to call. The first
crosses by training. The second crosses in writing.

---

## The concept in plain language

**A handoff transfers a skill and a responsibility. You transfer the skill by watching the trainee do
the task, and you transfer the responsibility in a letter.**

### Training: show, do, check

| Step | Who touches the screen | What it proves |
|---|---|---|
| **Tell** what it is for, in one or two sentences | nobody | the trainee knows why |
| **Show** each situation once | you | the trainee has seen it |
| **Do**: the trainee handles each situation while you stay quiet | the trainee | the trainee can do it with you there |
| **Check**: a situation the trainee has not seen, with no hints | the trainee | the trainee can do it without you |

The step people skip is **Check**. A trainee who got through four situations you showed them minutes earlier
has proven they can copy. A trainee who handles a fifth, new situation has proven they understand.

Write the outcomes before you train, each starting with a verb you can watch: "reads any tile and says
its state," not "understands the panel."

### The handoff letter

A short, professional letter from you to the receiver, both named by role. Its job is to leave no
question about ownership.

1. Sender, receiver, date, subject: the product and its version.
2. What is being handed over, and where it is.
3. What it does, and **what it does not do**. For a panel: it only watches.
4. How it was checked.
5. Training given.
6. Known limits.
7. What to do when something goes wrong: point at the implementation plan.
8. What you ask of them: written confirmation that they received it, or what is missing.

In 145060 you wrote documents for a reader. A letter adds something a document does not: **it asks the
reader to act and to answer.**

---

## Worked example 1: set up the training station

Training uses the simulator, on a lab PC. No hardware. **In the lab, use port 8700**, as in Unit 8.
The commands and output below were run on the build PC, which uses port 8705. In the `sensor-service`
folder:

```
python sensor_service.py --port 8705
```

```
Line 3 sensor service on http://127.0.0.1:8705
Backend: simulator, mode normal (all three sensors answer with values inside their thresholds)
GET /api/readings, GET /health. Press Ctrl+C to stop.
```

Start your panel pointed at it, confirm CONNECTED, and keep a second terminal open for the modes.

---

## Worked example 2: the Do situations, in order

Each command switches the simulator while the trainee watches the panel, not you.

```
python sim_control.py --port 8705 mode drift
```

```
200 {"mode": "drift", "meaning": "oven temperature climbs past its alarm threshold and keeps climbing"}
```

```
python sim_control.py --port 8705 mode freeze
```

```
200 {"mode": "freeze", "meaning": "the service answers, but sequence and sampled_at stop advancing (STALE)"}
```

Your record for each situation is what the trainee **did**: "read the triangle, looked toward the oven,
acknowledged through the box." Not "did well."

---

## Worked example 3: the Check situation

The trainee has seen an alarm and has seen lost data. They have not seen both at once. Run `mode drift`,
wait for the alarm, then:

```
python sim_control.py --port 8705 mode silent
```

```
200 {"mode": "silent", "meaning": "the service accepts connections and never answers (MISSING, by timeout)"}
```

In a second window, a read confirms the service now stays quiet:

```
python sim_control.py --port 8705 read
```

```
No answer from http://127.0.0.1:8705: timed out
```

The panel shows NO CONNECTION, every tile dark, and the oven's alarm
banner still up. **A passing answer:** "the oven is still in alarm; the screen cannot see it; check the
oven by hand." A trainee who says "the alarm stopped" has not passed, and you train that situation again.

---

## The wrong version, and what it produces

**The tour.** You drive the screen for twenty minutes, narrating. The trainee nods. You ask, "Make
sense?" They say yes. You write "trained" in your record.

Nothing fails. Nothing is proven. The first time the trainee meets a situation alone, they meet it for
the first time.

There is a smaller wrong version that happens mid-training. You type a mode change from memory:

```
python sim_control.py --port 8705 mode drop-sensor coolant-level
```

```
usage: sim_control.py [-h] --port PORT [--host HOST] [--timeout TIMEOUT]
                      {mode,read} ...
sim_control.py: error: unrecognized arguments: coolant-level
```

The sensor name needs `--sensor`. The panel does not change, the trainee waits, and your five minutes
of Do are now three. **Write your commands on a card before the session**, and read them from it.

**The letter that hands over nothing.** "Here is my panel, let me know if you have questions." It names
no version, no limits, no owner, and asks for no answer. A month later, nobody can say what was handed
over, or whether it was accepted.

---

## Why the wrong version is tempting

**Showing feels like teaching.** You know it well, so a smooth demonstration feels like progress. It is
progress for you.

**Watching someone struggle is uncomfortable.** The urge to take the mouse is strong. Staying quiet is the
skill.

**A letter feels like a formality.** It is the only part of the handoff that still exists after everyone
forgets the training.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Stakeholder** | a person with a stake in the system: here, the shift lead who owns the panel |
| **Handoff** | moving ownership of a system from its builder to the people who will run it |
| **Show, do, check** | a training method: demonstrate, let the trainee do it, then test with something new |
| **Check situation** | a task the trainee has not seen, run with no hints, to prove understanding |
| **Training record** | what the trainee did in each situation, and whether each outcome was met |
| **Professional correspondence** | a letter with sender, receiver, date, subject, a clear purpose, and a request |

---

## Self-check

**Question 1.** Your trainee handled all four Do situations perfectly. Why is that not enough to write
"trained"?

**Question 2.** Name three things a handoff letter for an operator panel must say that a user guide does
not.

**Question 3.** Rewrite this outcome so you can watch it: "The shift lead will understand the alarm
system."

---

### Answers

**1.** They had watched each situation shown once, minutes before, so they may be copying, not understanding. Only a
new situation, with no hints, shows they can do it without you.

**2.** Any three of: who owns the panel from now on; what version and ship folder are handed over; what the
builder remains responsible for, and until when; how it was checked; what training was given; a request
for written confirmation or a reason it is not accepted.

**3.** Any watchable version, for example: "The shift lead acknowledges an alarm through the confirmation
box after looking at the machine, and says what the banner means after acknowledging."
