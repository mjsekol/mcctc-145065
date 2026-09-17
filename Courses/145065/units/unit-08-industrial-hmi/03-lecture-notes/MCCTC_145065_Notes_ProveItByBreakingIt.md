# Lecture Notes: Prove It by Breaking It
## 145065 Object-Oriented Programming · Unit 8 · Week 16, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W16_ProveItByBreakingIt.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-08-industrial-hmi/04-slides/MCCTC_145065_Slides_W16_ProveItByBreakingIt.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK and Python
for the examples.

**Competencies:** 5.6.14 testing: system testing and user acceptance testing · 5.5.4 programs that call
other programs · 5.5.7 read inputs from a device.

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`, or by the course's
simulator.

---

## Why this exists

Your labs proved pieces. The freshness rule works. The latch works. The client gives up on time. Each
has green tests.

None of that proves the sentence your client cares about: **when the cable is pulled during an alarm,
the operator still sees the alarm.** That sentence involves the Pi's service, the network, your client,
your rules, your view model, and a window, all at once. Only a test with every piece running can prove
it.

So tomorrow you pull the plug in front of an audience, on purpose. Today you learn to do it as a test,
not a stunt.

---

## The concept in plain language

**A unit test** checks one piece, alone, with its inputs controlled. Fast, repeatable, and blind to
everything around the piece.

**A system test** checks a requirement with the whole system running. Slower, messier, and the only
kind that sees what the operator sees.

**User acceptance testing** puts the real user at the controls and asks whether the system does the job.
That is Unit 9's operator test.

**A system test has a script.** Five parts, every time:

1. **Put the system in a known state.** Service running, panel connected, values normal.
2. **Break one thing.** Freeze the Pi, stop the service, send garbage.
3. **Observe.** Wait long enough for the rule to act, then read the screen.
4. **Record** what you saw, word for word, next to the requirement it proves.
5. **Restore**, and check the system recovers.

**Break one thing at a time.** If you break two, you cannot tell which one caused what you see.

---

## Worked example 1: a test that starts another program

Your project's `LiveSimulatorTests` does not use a fake. It starts the real simulator as a separate
process, on its own port, switches it through its modes, and checks what the panel's code decides. That
is a program calling another program (5.5.4), reading a device's data (5.5.7), inside a test.

When you stop the simulator with Ctrl+C in its own terminal, it prints one word:

```
Stopped.
```

Its control script switches modes from a second terminal. This is a command you type, not output:

```
python sim_control.py --port 8700 mode freeze
```

In the project, the live test is one of the 29 acceptance tests, and the test run reports it with the
others. If Python is not on the lab PC's path, it cannot start the simulator, and it fails, which is the
honest result: the system could not be tested.

---

## Worked example 2: a scripted system test, in miniature

A system test compares what the system shows with what the requirement expects, step by step. This
program plays a Pi that freezes at step 3 and keeps re-stamping the same reading with the current time.
Two panels watch it: one checks the sequence number, one trusts the timestamp.

```csharp
Console.WriteLine("step  pi sends         expected   both checks   timestamp only");
int lastSequence = -1;
int stepSequenceChanged = 0;
for (int step = 1; step <= 9; step++)
{
    int sequence = step < 3 ? step : 3;          // frozen from step 3
    const int sampleAgeSeconds = 0;              // always stamped "now"
    if (sequence != lastSequence)
    {
        lastSequence = sequence;
        stepSequenceChanged = step;
    }

    int sinceChange = step - stepSequenceChanged;
    string expected = sinceChange > 5 ? "STALE" : "NORMAL";
    string both = sampleAgeSeconds > 5 || sinceChange > 5 ? "STALE" : "NORMAL";
    string timestampOnly = sampleAgeSeconds > 5 ? "STALE" : "NORMAL";
    Console.WriteLine($"{step,4}  seq {sequence}, age {sampleAgeSeconds}  {expected,-10} {Verdict(both, expected),-13} {Verdict(timestampOnly, expected)}");
}

static string Verdict(string shown, string expected) => shown == expected ? shown : shown + " FAIL";
```

```
step  pi sends         expected   both checks   timestamp only
   1  seq 1, age 0  NORMAL     NORMAL        NORMAL
   2  seq 2, age 0  NORMAL     NORMAL        NORMAL
   3  seq 3, age 0  NORMAL     NORMAL        NORMAL
   4  seq 3, age 0  NORMAL     NORMAL        NORMAL
   5  seq 3, age 0  NORMAL     NORMAL        NORMAL
   6  seq 3, age 0  NORMAL     NORMAL        NORMAL
   7  seq 3, age 0  NORMAL     NORMAL        NORMAL
   8  seq 3, age 0  NORMAL     NORMAL        NORMAL
   9  seq 3, age 0  STALE      STALE         NORMAL FAIL
```

One step each second. The sequence stopped changing at step 3, so at step 9 it has stood still for 6
seconds, more than the 5-second limit. Eight rows agree. The ninth is the one that matters, and a test
that stopped at step 8 would have passed both panels.

**The lesson for your demo:** wait long enough for the rule to act. The run-book's "Wait" column exists
for this reason.

---

## Worked example 3: the disconnect demo, as a script

The run-book in `09-project/project-files/DISCONNECT_DEMO_RUNBOOK.md` is a system test written out.
Three of its steps:

| Step | Break | Wait | Expect | Proves |
|---|---|---|---|---|
| Freeze | `mode freeze` | about 6 s | DATA NOT UPDATING, every tile STALE with NOT LIVE, the oven banner still up | stale is never shown as live; alarms survive stale |
| Silent | `mode silent` | about 3 s | NO CONNECTION, every tile NO DATA; drag the window and it still responds | a silent Pi never freezes the window |
| Disconnect, in alarm | Ctrl+C in the service terminal | about 2 s | NO CONNECTION, no numbers, the oven's alarm banner still up | alarms survive a disconnect |

The record you write is not "it worked." It is the words the screen showed, the time you waited, and the
requirement each step proves. A record like this is evidence someone else can check:

| Step | What we did | What the panel showed | Proves |
|---|---|---|---|
| 5 | stopped the service, waited 4 s | `NO CONNECTION`; every tile `NO DATA`; `UNACKNOWLEDGED ALARM` still present | alarms survive a disconnect |

---

## The wrong version: tests that never break anything

In worked example 2, the timestamp-only panel passes every row a short test would check. It fails only
when the Pi misbehaves long enough, and the output shows exactly where:

```
   9  seq 3, age 0  STALE      STALE         NORMAL FAIL
```

A suite built only from healthy replies has the same blind spot. Every test is green, and the first
frozen Pi on the shop floor shows `NORMAL` forever. Green tests are evidence about the cases they try.
They say nothing about the cases they skip.

**The other wrong version is a demo with no record.** "We pulled the cable and it was fine" cannot be
checked by anyone who was not in the room. Write the words the screen showed.

---

## Why the wrong version is tempting

Healthy replies take a minute to write, and every one of them passes. Breaking the system takes a second
terminal, a stopwatch, and patience. It also produces the only evidence your client actually asked for.

---

## Safety, before any real hardware

The run-book's last section is the same demo on the lab Pi, and it opens with the safety brief: ESD
precautions, power off before wiring, no mains voltage ever, and the signed Lab Acceptable Use and Safety
Agreement on file. On the Pi, "break one thing" means pulling the **network** cable, with your
instructor present. It never means touching power or wiring while the Pi is on. The simulator proves
every requirement for grading.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Unit test** | A test of one piece, alone |
| **Integration test** | A test of pieces working together |
| **System test** | A test of a requirement with the whole system running |
| **User acceptance testing** | The real user at the controls, judging whether the system does the job |
| **Fault injection** | Breaking one thing on purpose to see how the system responds |
| **Known state** | A starting point you can describe and repeat |
| **Test record** | What was done, what was seen, and what it proves, written down |

---

## Self-check

**Question 1.** Your partner freezes the simulator, waits 3 seconds, sees NORMAL, and writes "freeze
test failed." What went wrong with the test?

**Question 2.** Why should the demo break one thing at a time?

**Question 3.** Name one requirement a unit test can prove completely, and one that only a system test
can prove.

---

### Answers

**1.** The test did not wait long enough. The stale rule needs more than 5 seconds without a new sample,
so a correct panel still shows NORMAL at 3 seconds. The run-book says to wait about 6. The panel was
never given the chance to fail or pass.

**2.** So that whatever the panel shows can be blamed on one cause. If you freeze the Pi and pull the
cable together, a NO DATA tile does not tell you whether the stale rule worked.

**3.** A unit test can prove that a value exactly on the limit is inside, or that stale data never moves
the latch. Only a system test can prove that the alarm banner is still visible on the real window after
the real service stops, because that involves the process, the network, the client, and the view at
once.
