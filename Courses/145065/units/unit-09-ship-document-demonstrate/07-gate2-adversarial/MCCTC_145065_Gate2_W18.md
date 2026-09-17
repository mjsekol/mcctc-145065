# Gate 2: Adversarial Review · Week 18
## 145065 Object-Oriented Programming · Unit 9 · Week 18, Wednesday, Build 1

**Gate 2 is the gate where AI is the opponent.** This is the last one of the course. You did not write
this release plan. You are reviewing it, and you are scored on what you catch against what you miss.

**35 minutes.** Individual and silent. You may build and run the C# program in the folder. You may not
ask an AI tool whether the plan is correct, because an AI tool wrote it.

**This week you review a release plan with the AI Output Evaluation parameters.** One section of the plan
rests on a C# file, and you run that file as evidence.

**Everything here is invented.** Riverside Fabrication and its Line 3 are a composite. The Line 2 Wash
Monitor team is invented. The commit ids are invented sample data.

The files are in `gate2-w18-files/`:

| File | What it is |
|---|---|
| `RELEASE_PLAN_1.1.0.md` | **what you are reviewing**, written by an AI assistant |
| `WHAT_CHANGED.md` | the team's real commit list since the baseline, and the request they gave the assistant |
| `OPERATOR_TEST_NOTES.md` | the team's notes from Monday's operator test |
| `ReleaseGate/` | the C# install gate the plan describes, `net8.0`, no packages |

---

## What you are looking at

The team asked an AI assistant for a release plan. It produced a tidy document with every section they
asked for and a verification table. **It reads like a finished release plan.** Compare every claim in it
with the other two documents and with what the program actually does.

**There are exactly five planted defects, one for each parameter:**

| Parameter | The question to ask |
|---|---|
| **Validity** | Is a claim about something real actually correct? |
| **Relevance** | Does this part answer what was asked, for the reader it was asked for? |
| **Authenticity** | Is this the team's own work, or does it belong to somebody else? |
| **Potential Bias** | Whose needs are built in, and whose are left out? |
| **Hallucinations** | Does the thing described exist at all? |

**There is also one arguable item**, scored on your reasoning.

---

## Run the install gate

In `gate2-w18-files/`:

```
dotnet run --project ReleaseGate
```

That prints the plan's verification table. The program also takes two versions:

```
dotnet run --project ReleaseGate -- <installed> <candidate>
```

The plan says the check "has been verified for every version this panel will ever ship." **Decide which
versions the table did not try, and try them.** Think about how the numbers will look in a year.

---

## What to submit

For each defect: **where** (the section heading, or the file and line), **which parameter**, **what goes
wrong for the operators or the shift lead if nobody catches it**, and **the fix**. For the defect you
prove by running `ReleaseGate`, include the exact command and what it printed.

Then two more entries:

- **The arguable item.** Name it, argue both sides, and say where you land.
- **What I was unsure about.** Something specific.

### How to spend 35 minutes

- **First 5:** run the table. Then run at least three pairs of your own.
- **Next 10:** go down `WHAT_CHANGED.md` one commit at a time and find it in the plan. Then go down the
  plan one bullet at a time and find it in the commits.
- **Next 10:** compare the plan with `OPERATOR_TEST_NOTES.md`, sentence by sentence.
- **Rest:** read "What changed for operators" and "Rollout" as the shift lead would. Write your entries.

---

## Scoring

Five defects, one point each. The arguable item, one point. The unsure-about entry, one point. **Your
instructor states before you start which defect carries a double penalty.**

**Four of five is a strong score.**
