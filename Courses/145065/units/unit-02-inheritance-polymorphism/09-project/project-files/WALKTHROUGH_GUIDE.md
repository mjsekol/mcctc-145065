# Design Walkthrough Guide
## 145065 Object-Oriented Programming · Unit 2 · Week 5, Wednesday

A design walkthrough is a structured review of your design by someone who did not write it. You do
it now, two days before the project is due, because a problem found on Wednesday is a problem you
still have time to fix.

The notes for this lesson are `../../03-lecture-notes/MCCTC_145065_Notes_TheDesignWalkthrough.md`.

---

## Before Build 2: your packet

Commit these before Build 2 starts. Your reviewer reads them first.

1. `DESIGN.md`, updated so the diagram matches your code today.
2. **Three questions** you most want a reviewer to answer, at the bottom of `DESIGN.md`.
3. **One decision you are unsure of**, with both options written out.
4. The output of `python -m unittest`, pasted at the bottom of `DESIGN.md`.

---

## Roles

| | Author | Reviewer |
|---|---|---|
| Job | Walk the reviewer through the design, then listen | Find problems in the design |
| Talks | Less than half the time | Asks, and names findings |
| Writes | Every finding, while it is said | Nothing but notes; the author writes the record |
| Never | Defends a line of code before understanding the finding | Comments on the person |

Your instructor assigns pairs. You will be an author once and a reviewer once.

---

## The timing, per round

| Minutes | What |
|---|---|
| 0-2 | Author shows the diagram and reads the "is a" and "has a" sentences. No code yet. |
| 2-4 | Reviewer reads the three questions and the unsure decision. |
| 4-10 | Reviewer asks questions and names findings. Author runs code to answer, when running settles it. |
| 10-12 | Any disagreement goes through the settling steps below. |
| 12-18 | Author writes `WALKTHROUGH.md` from the record template. Reviewer checks it and signs off by initials. |

Then swap roles and do it again.

---

## Questions that test something

A useful review question tests the design against something. Bring at least three.

- What happens when a new kind is added? Show me which files change.
- Say the sentence test for each `class B(A)` out loud.
- Can this thing have two of that part? Can the part be swapped?
- Which class owns this rule? Where else is it written?
- What happens if outside code changes this collection?
- Where is the base case of this recursive function? What input reaches it?
- What does an override of this method have to keep doing?
- What does a group inside itself do to your walk?

"Looks good" is not a question, and it finds nothing.

---

## Listening, the author's job

Four moves. Use all of them.

1. **Let the reviewer finish.** Do not start answering in the middle of a question.
2. **Say it back.** "So you're saying a line could take a loose machine through `add()`."
3. **Answer a finding with a question first.** "What would that break?" or "Can we test that?" Not "it
   works."
4. **Show you are listening without words.** Face the reviewer. Hands off the keyboard unless you are
   running something to answer a question. Write the finding down while they talk.

---

## Disagreeing, and settling it

Disagreements are expected. A walkthrough with none probably did not look hard.

1. **Each person states the strongest version of their side**, in one or two sentences.
2. **Find what would settle it.** One of:
   - a **test** you can write in two minutes and run now
   - a **requirement** in the project brief or spec that decides it
   - a **reversible choice**: pick one now, and write down what would make you switch
3. **Record it**: the finding, both positions, what settled it, the decision, the option rejected, and
   the next step.

"We agreed to disagree" is allowed only with a next step. "The louder person won" is never a
decision.

---

## After the walkthrough

On Thursday, every finding you accepted becomes a commit, or a decision log entry that says why you
did not act on it. A walkthrough whose findings nobody acts on was a meeting, not a review.
