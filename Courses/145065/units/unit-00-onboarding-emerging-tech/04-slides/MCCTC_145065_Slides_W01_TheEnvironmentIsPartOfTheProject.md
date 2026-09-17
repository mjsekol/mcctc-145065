# The Environment Is Part of the Project
---
## Slide 1: It worked yesterday
- Same file, same computer, different result
- The terminal runs it. The Run button fails.
- Nothing in the code changed
- Something around the code did
Speaker notes: Welcome back. Here is a situation most of you have already lived through. A program runs from the terminal and fails from the Run button, or runs on your laptop and fails on the lab machine. You did not change a line. This semester your projects grow, with Flask in Week 7, a database in Week 9, and a second language in Week 11. Every one of those is a chance for this to happen. Today we stop it before it starts.
Image: Two identical laptops side by side, one terminal green with output, one showing a red error, navy and launch blue.
---
## Slide 2: One computer, more than one Python
- A machine can hold several Pythons
- A virtual environment belongs to one project
- It has its own packages and no others
- Installed on the machine is not installed in the project
Speaker notes: Here is the idea for today in one line. A virtual environment is a folder that belongs to one project. It points at one Python and holds that project's packages. So a package can be installed on the computer and still be missing from your project. Both of those are true at the same time, and that is exactly what causes the mystery on slide one.
Image: A computer outline containing three labeled boxes: machine Python, project A environment, project B environment.
---
## Slide 3: Ask the question out loud
```python
# where_am_i.py
import sys

print("Interpreter:", sys.executable)
print("Version:", sys.version_info[:2])
print("Inside a virtual environment:", sys.prefix != sys.base_prefix)
```
Speaker notes: Whenever something behaves strangely, the first question is which Python is running this. This file answers it. sys.executable is the path to the interpreter. version_info is the version as numbers. And the last line is the check the official venv documentation gives: inside an environment, prefix and base prefix are different folders. I am going to run it twice.
Image: None. This slide is code.
---
## Slide 4: Same file, two answers
```
Interpreter: C:\Python313\python.exe
Version: (3, 13)
Inside a virtual environment: False

Interpreter: C:\...\demo-venv\Scripts\python.exe
Version: (3, 13)
Inside a virtual environment: True
```
Speaker notes: First run, the machine-wide Python. Second run, a project environment. The file is identical. The interpreter is not. Notice the version is a tuple of numbers. That matters, and your bell ringer this morning showed why comparing versions as text lies to you.
Image: None. This slide is code.
---
## Slide 5: Watch this break
```python
# needs_flask.py
import flask

print("Flask is available in this environment")
```
Speaker notes: Week 7 needs Flask. This file checks whether it is there. I will run it with the machine Python first, then with the project environment. Predict both results before I press enter. Write them down.
Image: None. This slide is code.
---
## Slide 6: Installed on the machine, missing from the project
```
Flask is available in this environment

Traceback (most recent call last):
  File "...\needs_flask.py", line 3, in <module>
    import flask
ModuleNotFoundError: No module named 'flask'
```
Speaker notes: There it is. The first run worked because the machine has Flask. The second failed because the project does not. Same file, same computer. Now, the tempting fix is to install it on the machine. Do not. Then your project depends on something no file in your repository mentions, and the next machine fails with nobody knowing why.
Image: None. This slide is code.
---
## Slide 7: The project writes its environment down
- .python-version names the Python version
- pyproject.toml lists the packages
- Commit both of those files
- Never commit the .venv folder
- The next machine rebuilds from the two files
Speaker notes: The fix is to make the project describe its own environment. Two small text files do it. They are the recipe. The dot venv folder is the cooked meal, big and specific to one machine, and it never goes in the repository. Anyone can rebuild it from the recipe.
Image: A repository folder tree with two files highlighted in launch blue and the .venv folder crossed out.
---
## Slide 8: Setting it up with uv
```
uv python install 3.14
uv init oop-semester
cd oop-semester
uv python pin 3.14
uv venv
uv run python where_am_i.py
```
Speaker notes: These are the commands we use on the lab machines. Install the Python version, create the project, pin the version, build the environment, and run a file with it. Pin is the one that writes dot python version. Follow the lecture notes during Build 1 and check each step's result before the next.
Image: None. This slide is code.
---
## Slide 9: Tell your editor too
- Command Palette, then Python: Select Interpreter
- Choose the project's .venv
- The status bar shows which one is active
- Make a Gate 1 profile with suggestions off
Speaker notes: The terminal and the editor are two separate programs, and each needs to know which Python to use. Select Interpreter tells VS Code. Then you make a profile called Gate 1, with suggestions and inline completions turned off, and any AI extension absent. You switch to it for every Gate 1 rep. The settings are in the notes.
Image: A VS Code status bar close-up showing a selected .venv interpreter, navy background.
---
## Slide 10: What you are about to build
- Build 1: the semester project environment, pinned
- Terminal and Run button must agree
- Build 2: Lab U00-01, env_check.py Part 1
- A checker that proves your environment is right
Speaker notes: Build 1 sets up oop-semester with uv and points VS Code at it. You are done when where am I prints True from both the terminal and the Run button. Build 2 is the lab. You write a program that checks the Python version as numbers, whether you are inside an environment, and whether git can be found. Then the self-check file tries your functions against machines you do not have.
Image: A terminal showing three PASS lines in launch blue on navy.
