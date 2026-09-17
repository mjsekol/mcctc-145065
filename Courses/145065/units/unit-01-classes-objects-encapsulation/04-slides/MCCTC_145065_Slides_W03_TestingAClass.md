# Testing a Class
---
## Slide 1: It worked when you ran it once
- Your class refuses bad ratings. You checked, once.
- Tomorrow someone edits start()
- Nobody reruns your manual check
- The press quietly stops starting
Speaker notes: Every class you wrote this unit makes promises. A locked-out press refuses to start. A zero rating is refused. Right now your proof is that you ran the file once and read the output. That proof expires the moment anyone edits the class, and your refactor project edits working code on purpose. Today you build checks you can rerun in two seconds that say pass or fail without you reading anything.
Image: A sticky note reading tested it, looked fine, peeling off a monitor showing a class file.
---
## Slide 2: Define the cases before the code
- Setup: what exists before the check
- Action: the one thing you do
- Expected: the exact result
- Why: the promise it protects
- Include refusals, not only the happy path
Speaker notes: The hardest part of testing is not the code. It is deciding what to test. So you write a table first, four columns. Setup, action, expected, and why. One row is one test case. And at least one row has to be a refusal, where the class is supposed to say no. A class tested only on the happy path has half its promises unchecked. That is competency 5.4.4, define test cases.
Image: A four-column table with five rows, two rows highlighted as refusal tests.
---
## Slide 3: The case table for Machine
```
#  Setup          Action                      Expected
1  new press      none                        not running
2  new press      start()                     running
3  running press  lock_out, then start()      stopped, then RuntimeError
4  none           build with rating 0 and -5  ValueError each time
5  two presses    start one                   other still stopped
```
Speaker notes: Here is the table for the Machine class. Row one, a new press must never be running. Row two, the basic promise. Row three is a safety rule and a refusal. Row four is the object refusing to be built invalid. Row five checks that two machines never share state. The why column is in your notes. Every one of these becomes one test.
Image: None. This slide is code.
---
## Slide 4: The table, as unittest
```python
import unittest
from machine import Machine

class MachineTests(unittest.TestCase):
    def setUp(self):
        self.press = Machine("L3-PRS-01", 15)   # fresh for every test

    def test_start_runs_the_machine(self):
        self.press.start()
        self.assertTrue(self.press.is_running)

    def test_lockout_stops_and_blocks_start(self):
        self.press.start()
        self.press.lock_out("tech-07")
        self.assertFalse(self.press.is_running)
        with self.assertRaises(RuntimeError):
            self.press.start()

    def test_zero_or_negative_rating_is_refused(self):
        for bad in [0, -5]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Machine("L3-PRS-02", bad)
```
Speaker notes: A test class inherits from unittest TestCase. Unit 2 explains inheritance, so today copy the shape. Set up runs before every single test, so each test gets a brand new press. Every method starting with test is one case. Assert raises checks a refusal. Sub test lets one test try several bad values and still tell you which one failed. The other three tests are in your notes.
Image: None. This slide is code.
---
## Slide 5: Six tests, one command
```
python -m unittest -v

test_lockout_stops_and_blocks_start (...) ... ok
test_new_machine_is_stopped (...) ... ok
test_start_runs_the_machine (...) ... ok
test_that_cannot_fail (...) ... ok
test_two_machines_do_not_share_state (...) ... ok
test_zero_or_negative_rating_is_refused (...) ... ok

Ran 6 tests in 0.008s

OK
```
Speaker notes: Run it from the folder with python dash m unittest dash v. The v prints one line per test. I shortened the names in brackets to fit the slide. Notice the order. Alphabetical, not the order I wrote them. That is one more reason every test builds its own object. And notice the fourth test. Hold that thought.
Image: None. This slide is code.
---
## Slide 6: Now break the class
```
test_start_runs_the_machine (...) ... FAIL
test_that_cannot_fail (...) ... ok

FAIL: test_start_runs_the_machine (test_machine.MachineTests.test_start_runs_the_machine)
Traceback (most recent call last):
  File "...\test_machine.py", line 17, in test_start_runs_the_machine
    self.assertTrue(self.press.is_running)
AssertionError: False is not true

FAILED (failures=1)
```
Speaker notes: I changed one word in start, true to false. The passing lines are trimmed to fit. Read the report from the bottom. One failure. The fail heading names the test, and a good name already tells you which promise broke. Line seventeen is the assertion. False is not true says what it found. The report points at the promise, not at the broken line in machine dot py. Finding that is still your job.
Image: None. This slide is code.
---
## Slide 7: Watch the test that cannot fail
```python
    def test_that_cannot_fail(self):
        self.assertTrue(self.press.start)
```
- No parentheses: start is never called
- A method object always counts as true
- It printed ok on the broken class
Speaker notes: Look back at the last slide. Start was broken, and this test still said ok. No parentheses. It never calls start. It checks the method object, and every method object counts as true. It passes on working code, broken code, and empty code. There is no error message to show you, and that is exactly the problem. A test that cannot fail gives you green and no information.
Image: A green OK light wired to nothing, its cable lying unplugged on the floor.
---
## Slide 8: A test earns trust by failing once
- Break the class on purpose
- Every test that names that behavior must fail
- Still passing means the test is broken
- subTest reports the value: (bad=0)
- Today's lab automates this with mutants
Speaker notes: So here is the habit. Break the class on purpose and watch. Every test about that behavior must go red. If one stays green, the test is broken, not the class. Sub test helps here. When I let a zero rating through, the fail heading ended with bad equals zero, so I knew exactly which value got past. Today's lab plants five broken copies of the class, called mutants, and counts how many your tests catch.
Image: Five small class-file icons with bug stickers, three marked caught and two marked missed.
---
## Slide 9: What you are about to build
- Build 1: Lab U01-04 ScopeAndTests, Part 2
- Case table first, then test_line3.py
- mutant_check.py counts the mutants you catch
- Plus the collection choice: dict versus list
- Build 2: refactor M3, tests and README
Speaker notes: Build 1 is Lab U01-04, Scope and Tests, Part 2. You write your case table first, then test line 3 dot py for Machine and WorkCell. Mutant check tells you how many of five planted mutants your tests catch. The lab also has you time a dictionary against a list for the cell's collection, and write the test that catches a list version that accepts duplicates. Build 2 is refactor milestone 3. A test file per class, at least one refusal test each, and your README. The project is due at tomorrow's commit window.
Image: A terminal showing Mutants caught: 5 of 5 in launch blue on navy.
