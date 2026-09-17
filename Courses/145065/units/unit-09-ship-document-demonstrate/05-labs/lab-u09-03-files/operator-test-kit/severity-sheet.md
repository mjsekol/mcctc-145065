# Severity sheet · from sessions to changes

**Fill this in after the last session, from the numbered lines on your record sheets.**
Copy it into your project's `docs/OPERATOR_TEST.md`.

---

## Severity

| Severity | Means |
|---|---|
| **High** | a person could make an unsafe decision, or miss a real alarm |
| **Medium** | a person was confused or slowed, and the screen or the guide recovered them |
| **Low** | a person asked something the screen does not answer, with no effect on what they did |

## The table

| # | Finding, in one sentence | Evidence (line numbers) | Sessions | Severity | Decision |
|---|---|---|---|---|---|
| F1 | | | __ of __ | | |
| F2 | | | __ of __ | | |
| F3 | | | __ of __ | | |

**Decision** is one of:

- **Fix now, in code**, with a change request and a change impact note. Say the version.
- **Fix now, in the guide or the training card only.** Say why the screen does not need to change.
- **Defer**, with the reason and where it is logged.
- **No change**, with the reason. "The design already handled it" is a reason, if a line proves it.

## Rules for a finding

1. **A finding is something a person did or said**, not your opinion of the screen.
2. **Every finding cites at least one numbered line.** No line, no finding.
3. **Say how many sessions it happened in.** One person is a signal. Two or three is a pattern.
4. **A task where you broke a facilitator rule cannot be the only evidence** for a finding.

## What worked

Write at least two things people did right without help, with line numbers. You need them in your
demonstration, and they tell you what not to change.
