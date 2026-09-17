# Inheritance or Composition

Copy this file to `unit-02-hierarchy/INHERITANCE_OR_COMPOSITION.md`. Write 250 to 500 words in total. Delete these
instructions when you are done.

This is the written analysis the syllabus asks for: the strengths and weaknesses of two approaches for
your specific problem. Argue it the way you would argue a contested question: the strongest case on
each side, then your decision.

---

## Where I used inheritance

**The relationship:** `<Child>` is a `<Parent>`.

**Why inheritance fits here.** What does the child get from the parent that it would otherwise copy?
Why does the sentence test pass?

**The strongest argument against it.** What would someone who wanted composition say? What does the
child inherit that it does not need, or what could change and break it?

**Why I kept it anyway.**

---

## Where I deliberately did not use inheritance

**The relationship:** `<Owner>` has a `<Part>`.

**What inheritance would have looked like, and what it would have cost.** Be specific: a class count,
a method that would leak in, a thing that could not be swapped.

**What I used instead, and how the owner protects the part.**

**The strongest argument for inheritance here.** What would the other design have made simpler?

**Why composition wins for this problem.**

---

## What would change my mind

One sentence for each choice: the new requirement that would make you switch.
