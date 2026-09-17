# Peer Walkthrough Record · [author's port]

Copy this file to your repository as `WALKTHROUGH.md`. Week 12, Thursday, Build 2.

**Roles.** Author, reviewer, recorder, by role only. Do not write anyone's full name in the file.

**The rules.** The author runs the five-minute demo, then stays quiet. The reviewer asks the five
questions from the project spec. The recorder writes every finding. Before the period ends, the
author writes a decision for every finding: **fixed**, **deferred** with a reason, or **kept** with a
reason.

## Static analysis before the walkthrough

| Check | Result, pasted or counted |
|---|---|
| `dotnet build` with `TreatWarningsAsErrors` on the library | |
| The same build with `-p:TreatWarningsAsErrors=false` | warnings: |
| `dotnet test` | |
| `python -m unittest` in `python/` | |
| `python port_check.py .` | |
| Every `!` and `#pragma` in the library, and where the proof is | |

## Demonstration checklist (the recorder scores it)

| # | | Points |
|---|---|---|
| 1 | The brief stated in the controls lead's terms | /1 |
| 2 | Both demos run, and a matching line is pointed at | /2 |
| 3 | A real compiler catch made live, read aloud, and contrasted with Python | /2 |
| 4 | The interface shown with its two implementations | /2 |
| 5 | One thing the compiler did not catch, with its check | /1 |
| 6 | The question, asked by the instructor | /2 |

## Findings

| # | Where (file and line) | Finding | Severity: major, minor, question | Author's decision and reason |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## One thing the reviewer said the port did well
