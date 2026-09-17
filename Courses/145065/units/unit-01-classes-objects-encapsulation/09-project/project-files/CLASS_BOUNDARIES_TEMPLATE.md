# Class Boundaries

The Refactor, Unit 1. Copy this file to `unit-01-refactor/CLASS_BOUNDARIES.md`.

**Sections 1 to 4 are due at M2, Week 2, Friday, committed before any class code.** Section 5 is
finished with the code. Replace every line in angle brackets. Delete these instructions when you
submit.

---

## 1. The program I refactored

- Program: <name, and the 145060 unit it came from>
- Where the original lives: <repository and folder>
- Why it is procedural: <two sentences. Where does its data live, and how do its functions get it?>
- How I record its behavior: <the exact golden_check.py record command you ran>

## 2. Inventory

Fill this from the code, not from memory. Every function in the program gets a row.

### Functions

| Function | Reads | Changes | Called by |
|---|---|---|---|
| <name> | <the data it looks at> | <the data it changes, or nothing> | <which functions call it> |

### Data

Every piece of data the program keeps: module-level constants and variables, and any list or
dictionary that is passed from function to function.

| Name | What it holds | Level now | Passed through which functions |
|---|---|---|---|
| <name> | <description> | <module, or local to which function> | <list, or none> |

**The state that travels.** Name any value that is created in one function and handed through
three or more others. That is the strongest sign of a missing object.

## 3. Where every function goes

One row for every function in the inventory.

| Old function | Becomes | Reason: the data it needs |
|---|---|---|
| <name> | <Class.method, a static or class method, or "stays a function"> | <one sentence> |

## 4. One section per class

Copy this block for each class in your diagram.

### <ClassName>

- **Owns:** <the data this class keeps, and which of it is internal>
- **Enforces:** <the rules it refuses to break, and the exception each refusal raises>
- **Why this is its own class:** <why this data and these rules belong together, and not inside
  another class>
- **What I considered and rejected:** <merging it with, or splitting it into, which other class, and
  why not>
- **The collection it keeps, and why:** <list, dict, set, tuple, or none, and the question it answers
  fastest>
- **Properties:** <which are read-only, which are validated, and what each setter checks>
- **Static and class methods:** <each one, and why it needs the class or needs nothing>

## 5. Known differences from the old program

A refactor changes organization, not behavior. `golden_check.py compare` should report every line
as `MATCH`. If anything differs, list it here with the reason, and list every `--ignore` pattern you
used.

| Difference | Why it is acceptable |
|---|---|
| <none, or the difference> | <reason> |
