# Lab U01-02: The Tool Crib
## 145065 Object-Oriented Programming · Unit 1 · Week 2, Tuesday to Thursday

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** three Build 1 blocks.
Part 1 on Tuesday (the diagram), Part 2 on Wednesday (`Tool` and the functions that stay functions),
Part 3 on Thursday (`ToolCrib`, the object that holds the tools).
**Competencies:** 5.1.3 and 5.6.7 (model and document a design with UML), 5.3.9 (write code that
creates and calls functions), 5.3.12 (write code to create classes, objects, and methods), 5.5.1
(data validation), 5.5.5 (naming conventions and comments).

Files: `lab-u01-02-files/tool_crib_procedural.py` (the program as it runs today),
`lab-u01-02-files/crib_diagram_template.md`, `lab-u01-02-files/tool_crib.py` (your starter), and
`lab-u01-02-files/selfcheck_crib.py`.

**Riverside Fabrication is a composite**, an invented small metal fabrication shop. Every tag, badge,
and time here is invented.

---

## The scenario

Line 3 keeps its torque wrenches, calipers, and gauges in a locked tool crib, and technicians check
them out with their badge. The crib program is one dictionary and eight loose functions, and last
month it let someone add a spare wrench over the record of a wrench that was still out, so the crib
lost track of it. The attendant needs a version where the rules live with the tools, designed on
paper first so the shift supervisor can review it before anyone writes code.

## What you will build

A class diagram for a `Tool` and a `ToolCrib`, then the two classes built to match it.

---

## The spec

Times are whole minutes since the shift started. Minute 90 is 1 h 30 min into the shift.

**The eight rules.**

1. A tool's tag is `TC-` followed by exactly three digits, such as `TC-014`. Its name is not blank.
2. A tool is either in the crib, or out to exactly one badge since a known minute.
3. A tool that is out cannot be checked out again.
4. A tool that is in cannot be checked in.
5. Minutes are whole numbers, 0 or more. A check-in cannot be earlier than its checkout.
6. A tool out for more than 240 minutes is overdue. Exactly 240 is not.
7. The crib holds only tools, and never two tools with the same tag.
8. The crib lists tools in the order they were added, and nothing adds or removes a tool except the
   crib itself.

**Operations on one tool.**

| Operation | Returns |
|---|---|
| build a tool: `Tool(tag, name)` | the tool |
| `check_out(badge, minute)` | nothing |
| `check_in(minute)` | the whole minutes it was out |
| `is_out()` | `True` or `False` |
| `holder()` | the badge, or `None` |
| `minutes_out(now)` | minutes out as of `now`, or `None` if it is in |
| `is_overdue(now)` | `True` or `False` |
| `status_text(now)` | one line, below |
| `repr(tool)` | `Tool(tag='TC-014', name='Torque wrench')` |

**Operations on the whole crib.**

| Operation | Returns |
|---|---|
| build a crib: `ToolCrib(name)` | the crib |
| `add(tool)` | the tool added |
| `get(tag)` | the tool, or `None` |
| `check_out(tag, badge, minute)` | nothing |
| `check_in(tag, minute)` | the whole minutes it was out |
| `tools()` | every tool, in the order added, as a tuple |
| `out_tools()` | a list of the tools that are out |
| `overdue(now)` | a list of the overdue tools |
| `report(now)` | a list of every tool's status line |
| `len(crib)`, `tag in crib`, `for tool in crib` | what you would expect |
| `repr(crib)` | `ToolCrib(name='Line 3 crib', tools=3)` |

**Two functions** turn minutes into what a person reads: `minutes_between(start, end)` and
`format_duration(minutes)`, which gives `1 h 05 min` for 65.

**Status lines.**

```
TC-022 Digital caliper: in the crib
TC-014 Torque wrench: out to tech-07 for 1 h 05 min
TC-014 Torque wrench: out to tech-07 for 4 h 30 min OVERDUE
```

**Refusals** follow the same table as Lab U01-01: `TypeError` for the wrong type of thing (adding a
string to the crib), `ValueError` for a bad value, `RuntimeError` for a call that is not allowed now.
An unknown tag in a crib operation raises `KeyError`.

---

## Part 1: Tuesday Build 1, steps 1 through 6 · the diagram

**No class code today.** The diagram is the design, and the supervisor reviews it before anything is
built.

### Step 1. Run the program the crib uses today

```
python tool_crib_procedural.py
```

**Observable result:** a report, then these two lines at the end, then a traceback ending:

```
After the spare was added, is TC-014 out? False
...
TypeError: unsupported operand type(s) for -: 'int' and 'NoneType'
```

In your lab README, under `## What the functions allowed`, explain both in one sentence each. For the
traceback, name the line where it crashed and the line that was actually wrong. They are not the same
line.

### Step 2. Start the diagram

Copy `crib_diagram_template.md` to `crib_diagram.md`. Read the spec above once more.

**Observable result:** `crib_diagram.md` exists and is committed.

### Step 3. The `Tool` box: attributes

List every piece of data one tool keeps. Mark each `+` if outside code may read it directly, or `-` if
only the tool's methods touch it. Give each a type after a colon: `str`, `int`, or `str or None`.

**Observable result:** at least four attributes, each with a mark and a type.

### Step 4. The `Tool` box: methods

Add every operation on one tool, with its parameters and what it returns, for example
`+check_in(minute) int`.

**Observable result:** eight methods including `__repr__`.

### Step 5. The `ToolCrib` box and the line between the boxes

Fill the crib's attributes and methods. Then the line: how many tools can one crib hold, and what
does the line mean? Fill `"TODO"` on the `o--` line with a multiplicity such as `0..*`, and a label.
Then answer "The collection the crib keeps" in the template.

**Observable result:** both boxes complete, a multiplicity, a label, and a collection named with the
question it answers fastest.

### Step 6. What a diagram cannot say, and a review

Fill "Two things the diagram does not show" with two of the eight rules that no box or line can
express. Then trade with a partner. Your partner checks your diagram against all eight rules and
writes `Reviewed by <first name>: <one thing to change>` at the bottom.

**Observable result:** the review line is in your file. Commit.

---

## Part 2: Wednesday Build 1, steps 7 through 12 · `Tool`, and what stays a function

### Step 7. Decide where each old function goes

Fill "Where each procedural function goes" in `crib_diagram.md`. For each of the eight functions in
`tool_crib_procedural.py`, write where it goes: a method of `Tool`, a method of `ToolCrib`, or a plain
function. The reason is the data it needs. **If it needs no tool and no crib, it stays a function.**

**Observable result:** eight rows, each with a reason. If a row disagrees with your Tuesday diagram,
fix the diagram in the same commit.

### Step 8. The two functions

In `tool_crib.py`, under the "functions that stay functions" heading, write `minutes_between` and
`format_duration`. Use `divmod` for hours and minutes, and `:02d` to pad the minutes.

```
python selfcheck_crib.py part2
```

**Observable result:** P2-1 passes.

### Step 9. Build a valid tool

In `Tool.__init__`, raise `ValueError` for a tag that does not fully match `TAG_PATTERN` or a name
that is blank. Use `TAG_PATTERN.fullmatch(tag)`, which checks the whole string. Store the trimmed
name. Add `__repr__`.

**Observable result:** P2-2 and P2-3 pass.

### Step 10. Check out

`check_out(badge, minute)` refuses a blank badge and a minute that is not a whole number 0 or more
(`ValueError`), and a tool that is already out (`RuntimeError`). Then it records the holder and the
minute. Add `is_out()` and `holder()`.

**Observable result:** P2-4 and P2-5 pass.

### Step 11. Check in

`check_in(minute)` refuses a tool that is in (`RuntimeError`) and a minute before the checkout
(`ValueError`). It returns the minutes out, using `minutes_between`, and clears the holder and minute.

**Observable result:** P2-6 passes.

### Step 12. Time out, overdue, and the status line

`minutes_out(now)`, `is_overdue(now)`, and `status_text(now)`. The status line calls
`format_duration`. Do not copy its arithmetic.

**Observable result:** `9 of 9 self-checks passed` on `part2`. Commit.

---

## Part 3: Thursday Build 1, steps 13 through 19 · `ToolCrib`

### Step 13. Build a crib

`ToolCrib(name)` refuses a blank name and stores the trimmed name and an empty collection, the one
your diagram named. Add `__repr__`.

```
python selfcheck_crib.py part3
```

**Observable result:** P3-1 passes.

### Step 14. Add and find

`add(tool)` raises `TypeError` for anything that is not a `Tool` and `ValueError` for a tag already in
the crib, then stores the tool and returns it. Add `get(tag)`, `__len__`, and `__contains__(tag)`.

**Observable result:** P3-2, P3-3, and P3-9 pass.

### Step 15. Hand out a copy, never the collection

`tools()` returns a tuple of the tools in the order they were added.

**Observable result:** P3-4 passes.

### Step 16. The crib finds, the tool decides

`check_out(tag, badge, minute)` and `check_in(tag, minute)` find the tool, raising `KeyError(tag)` if
it is not in the crib, and then call the tool's own method. **Do not copy the tool's rules into the
crib.** The tool already enforces them.

**Observable result:** P3-5 passes.

### Step 17. Questions about the whole crib

`out_tools()`, `overdue(now)`, and `report(now)`, each built by asking every tool.

**Observable result:** P3-6 and P3-7 pass.

### Step 18. Looping over the crib

`__iter__` returns an iterator over a **copy**, so a loop that adds a tool does not break itself.

**Observable result:** `18 of 18 self-checks passed`.

### Step 19. Replay the shift

Replace `main()` in `tool_crib.py` with the shift from `tool_crib_procedural.py`, using a `ToolCrib`.
Catch each refusal and print it. Keep the two lines the old program could not stop: adding the spare
`TC-014`, and checking in `TC-031`.

**Observable result:** the crib report at minute 300 matches the old program's three lines, the spare
wrench is refused, `TC-014` is still out after it, and the `TC-031` check-in is refused instead of
crashing. Check your diagram against your code one last time. Commit and push.

### Acceptance criteria, full lab

- [ ] `crib_diagram.md` has both boxes, marks and types on every member, a multiplicity, the collection,
      the two rules, the placement table, and a partner's review line
- [ ] The diagram matches the code, or was changed in the same commit as the code
- [ ] `python selfcheck_crib.py` prints `18 of 18 self-checks passed`
- [ ] `minutes_between` and `format_duration` are plain functions, not methods
- [ ] The crib never repeats a rule the tool already enforces
- [ ] `python tool_crib.py` refuses both things the old program allowed
- [ ] The README has `What the functions allowed`
- [ ] Committed and pushed at the end of each Build 1

---

## If it breaks

### 1. A method called with nothing to describe

```
TypeError: Tool.status_text() missing 1 required positional argument: 'now'
```

**Cause:** `status_text` needs the current minute to work out how long a tool has been out. Pass it:
`tool.status_text(300)`.

### 2. The crash from the old program, back again

```
TypeError: '<' not supported between instances of 'int' and 'NoneType'
```

**Cause:** `check_in` compared the minute with a checkout time of `None`, because the tool was never
out. Check `self._holder is None` first and raise `RuntimeError`. The order of the checks is the fix.

### 3. The crib changed while you looped over it

P3-8 fails with `crashed with RuntimeError: dictionary changed size during iteration`.

**Cause:** `__iter__` returns `iter(self._tools.values())`, which walks the live dictionary. Adding a
tool mid-loop breaks it. Iterate over `self.tools()`, the tuple copy.

### 4. A tag that almost matches

P2-3 fails with `tag 'TC-0140' was accepted, expected ValueError`.

**Cause:** `TAG_PATTERN.match(tag)` checks only the start of the string. `fullmatch` checks all of it.

### 5. A function moved into the class

P2-1 fails with `minutes_between is inside Tool; it needs no tool, so it stays a function`.

**Cause:** the function uses no tool data. Inside the class it would need `self` it never uses, or a
decorator you meet in Week 3. Leave it at module level, and say why in the placement table.

---

## Stretch goal

Give `Tool` a `__str__` that returns `TC-014 Torque wrench`, and keep `__repr__` as it is. Then write,
in the README, when a program shows each one: `print(tool)` and `print([tool])` behave differently.
Find out how.

---

## Submission checklist

- [ ] Self-check 18 of 18
- [ ] `crib_diagram.md` complete, reviewed, and matching the code
- [ ] README section written
- [ ] AI usage log updated if you used a model
- [ ] Committed and pushed at the end of Tuesday, Wednesday, and Thursday Build 1

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| On Tuesday, the diagram has boxes but no types or marks after 20 minutes, or on Wednesday the student is writing the crib's rules into `Tool` | SCAFFOLDED |
| Steady progress, a real argument with the partner about a mark or a multiplicity | STANDARD |
| `9 of 9` on `part2` before Wednesday's Build 1 is half over | EXTENDED |
| The student says nobody uses tool cribs | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Part 1:** the student receives the `Tool` box with the attributes already listed, unmarked, and
  marks them, types them, and adds the methods. The `ToolCrib` box is theirs to draw.
- **Part 2:** step 10 skips the badge and minute validation, so P2-5 is not required. Step 11 keeps
  its checks.
- **Part 3:** step 18 comes with its one line written, `return iter(self.tools())`. The student
  explains at a checkpoint why the copy matters.
- **Checkpoints:** show the instructor the diagram after step 5, `part2` after step 11, and `part3`
  after step 16.

**Acceptance criteria:** the diagram with marks, types, and a multiplicity; 17 of 18 (P2-5 excepted);
step 19 done.

**Grading:** same 100-point scale. Requirements Fit is judged against this version's list. Full
completion earns the same grade as full completion of STANDARD.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a concept the lab has not taught.

**Added requirement.** The attendant wants a history of every completed checkout: tag, badge,
checkout minute, and check-in minute. Add `history()` to `ToolCrib`, returning every completed
checkout in order. **A record must be impossible to edit after it is written**, and each record
should report its own minutes.

**Hint, not the answer.** Python's standard library can generate a small class for you from a list of
typed fields, including one whose fields cannot be reassigned. Read the `dataclasses` documentation,
`https://docs.python.org/3/library/dataclasses.html`, especially the `frozen` parameter. Update your
diagram with the new class and its line to `ToolCrib`.

**Acceptance criteria:** all STANDARD criteria still pass; two checkouts of one tool give two records;
assigning to a record's field raises an error; the diagram shows the new class with a multiplicity.

**Grading:** same scale.

---

## APPLIED

**For the student who says nobody uses tool cribs.** The same design, somewhere else.

**Changed scenario.** Your school's robotics club lends out batteries, chargers, and controllers from a
parts bin. Items are tagged `RB-` and three digits, and are checked out to a team number (invent them;
no student names) at a minute of the build session. Anything out longer than 90 minutes must be
returned before the next team's slot.

**What you build.** The diagram first, with a partner review. Then `Part` and `PartsBin` with the same
shape as the spec, your own two plain functions, and a self-check of at least twelve checks, including
one for each of the eight rules rewritten for your domain.

**Acceptance criteria:** your diagram matches your code; your self-check passes; the README explains
where each old-style function would have gone.

**Grading:** same scale. Requirements Fit is judged on whether every rule is enforced by the class that
owns the data it needs.
