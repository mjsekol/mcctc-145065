# Documentation Travels With the Code
---
## Slide 1: The instructions that used to be true
- A classmate follows your README exactly
- It fails on the first command
- Your code is fine
- Your README is not
Speaker notes: Picture this. You hand your project to a classmate. They open the README, type the first command exactly as written, and it fails. Your code works perfectly. The instructions stopped being true at some point and nobody noticed, because nothing crashed. Today is about keeping documentation true.
Image: A README page with one line highlighted in launch red, next to a terminal showing an error.
---
## Slide 2: What a commit does not say
- A commit records what changed
- It does not say how to run it
- It does not say why it is built this way
- Documentation carries those two things
Speaker notes: You commit without thinking now, and that is good. But a commit is a record of what changed. A stranger also needs to know how to run the project, and anyone making changes later needs to know why it was built this way. Those two things live in documentation, and documentation lives in the repository.
Image: A commit history list beside a README and a decision log, joined by a bracket.
---
## Slide 3: Three documents, all semester
- README.md: what it is and how to run it
- decision-log.md: why, and what you rejected
- Task board: to do, doing, done
- All three live from Week 1 to Week 18
Speaker notes: This semester you keep three documents. The README says what the project is and how to run it today. The decision log says why you chose what you chose, and in this course every entry names the option you rejected. The task board shows what is coming. You start all three today.
Image: Three document icons in a row labeled README, decision log, task board, navy outlines.
---
## Slide 4: A decision log entry
```
## Week 1, Monday · Project environment
- Decision: how this project gets its Python
- Chosen: uv, with Python 3.14 pinned in .python-version
- Rejected: the machine-wide Python
- Why: the next machine rebuilds the same environment from committed files
- Cost: one more tool to install and learn
```
Speaker notes: Here is the format. Five fields, dated by week and day. Decision, chosen, rejected, why, and cost. Rejected is a syllabus rule for this course. It proves you considered something else. Cost is the one people leave out, because nobody likes admitting a choice costs anything. Every choice does.
Image: None. This slide is code.
---
## Slide 5: A program can check your README
```python
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
for line in readme.splitlines():
    line = line.strip()
    if line.startswith("python ") and line.endswith(".py"):
        script = line.split()[1]
        found = "exists" if Path(script).is_file() else "MISSING"
        print(script, found)
```
Speaker notes: This reads a README, finds every line that looks like a python command, and checks that the file it names exists. On the folder I am about to show you, it prints check dot py MISSING. A program caught what a human reader would skip right past.
Image: None. This slide is code.
---
## Slide 6: Follow the README literally
```
## How to run

python check.py
```
Speaker notes: This is the README. The folder holds env check dot py, because somebody renamed it last week. I am going to do exactly what the README says and nothing more. Watch what happens.
Image: None. This slide is code.
---
## Slide 7: The error, and whose fault it is
```
python.exe: can't open file 'C:\\...\\oop-semester\\check.py': [Errno 2] No such file or directory
```
Speaker notes: Python cannot open a file that is not there. Now the real question. Which commit should have fixed the README? The one that renamed the file. The code change and the documentation change belong in the same commit. That way the history is true at every point, not only at the end.
Image: None. This slide is code.
---
## Slide 8: Why nobody notices
- You already know how to run it
- So you never read your own instructions
- Nothing fails for you
- It fails for the next person
Speaker notes: Stale documentation survives because its author is the one person who never needs it. You know the command by heart. So before every commit, ask one question: does any document name something I changed. And today, a partner follows your README out loud, word for word.
Image: A person reading a README while another person, the author, looks away at a different screen.
---
## Slide 9: The semester task board
- GitHub Projects, board layout, three columns
- Or TASKBOARD.md with the same columns
- One card per course milestone, with week and day
- No personal information on any card
Speaker notes: The task board is a productivity tool, and it is on the exam as one. Use GitHub Projects with the board layout, or a markdown file if that is not available. Put every course milestone on it from the list in the lab, with its week and day. Move cards as the work moves. Milestones and your own tasks only, nobody's personal information.
Image: A three-column kanban board with milestone cards, launch blue headers.
---
## Slide 10: What you are about to build
- Build 1: env_check.py Part 2, four folder checks
- Your repository must pass seven of seven
- Build 2: README, decision log, task board
- A partner runs your project from your README alone
Speaker notes: Build 1 finishes the lab. The checker learns to look at your project folder: required files, the git folder, the gitignore entries, and a real run section in the README. Then you run it on your own repository and fix what it finds. Build 2 writes the three documents. You are done when a partner can run your checker using only your README.
Image: A terminal showing 7 of 7 checks passed beside an open README.
