# Functions Versus Methods
---
## Slide 1: Eight functions, one class, where does each go?
- Your 145060 program is all functions
- Now some of them move into a class
- Move the wrong ones and the class bloats
- Leave the wrong ones out and the data leaks
Speaker notes: Here is the problem you face in the refactor project and in today's lab. You have a program made of functions. Some of them belong inside a class. Some of them do not. Get it wrong one way and your class fills up with code that has nothing to do with it. Get it wrong the other way and loose functions reach into data the class was supposed to guard. By the end of the next fifteen minutes you have a one-sentence rule for every function.
Image: Eight function cards on a table, some sliding into a box labelled Tool, some staying outside.
---
## Slide 2: A method is a function that receives the object
- A method lives inside a class
- Its first parameter, self, is the object
- press.status_text() runs Machine.status_text(press)
- The object before the dot becomes self
Speaker notes: That is the whole difference. A method is a function defined in a class, and Python passes the object in as the first argument. When you write press dot status text, Python runs Machine dot status text with press passed in. Nothing magic happens. It is a function call with one argument filled in for you.
Image: The call press.status_text() with an arrow from press to the self parameter in the def line.
---
## Slide 3: One function, two methods
```python
def celsius_to_fahrenheit(celsius):
    """A function: it needs a number, not a machine."""
    return celsius * 9 / 5 + 32

class Machine:
    def __init__(self, asset_tag, name):
        self.asset_tag = asset_tag
        self.name = name
        self._temperature_c = None

    def record_temperature(self, celsius):
        """A method: it changes THIS machine's data."""
        self._temperature_c = celsius

    def status_text(self):
        """A method: it reads THIS machine's data."""
        if self._temperature_c is None:
            return f"{self.asset_tag} {self.name}: no reading"
        fahrenheit = celsius_to_fahrenheit(self._temperature_c)
        return f"{self.asset_tag} {self.name}: {self._temperature_c:.1f} C ({fahrenheit:.1f} F)"
```
Speaker notes: Read the docstrings. The conversion needs a number, not a machine, so it stays a function. Recording a temperature changes this machine, so it is a method. The status text reads this machine, so it is a method. And notice a method can call a plain function. That is normal and good.
Image: None. This slide is code.
---
## Slide 4: Same call, two spellings
```python
press = Machine("L3-PRS-01", "Press 1")
print(press.status_text())
press.record_temperature(41.5)
print(press.status_text())
print(Machine.status_text(press))
```
```
L3-PRS-01 Press 1: no reading
L3-PRS-01 Press 1: 41.5 C (106.7 F)
L3-PRS-01 Press 1: 41.5 C (106.7 F)
```
Speaker notes: The last two lines of output match because they are the same call. One spelling lets Python pass the object. The other passes it by hand. Also notice the first line says no reading, not zero degrees. A press that has never been read does not have a temperature, and None says that honestly.
Image: None. This slide is code.
---
## Slide 5: The decision rule
- Needs this object's data: make it a method
- Needs no object: keep it a function
- Reaches into underscore data from outside: wrong place
- Never uses self: probably should be a function
Speaker notes: Write this down. If the behavior needs this object's data, it is a method. If it needs no object, it stays a function. Two warning signs. A function outside the class that reads an underscore attribute is a method in the wrong place. A method that never touches self probably did not need to be a method. Next Tuesday adds a third home, static and class methods. Today there are two.
Image: A two-branch decision diagram: does it need this object's data, yes to method, no to function.
---
## Slide 6: A function in the wrong place
```python
def is_hot(machine):
    return machine._temperature_c > 60

new_press = Machine("L3-PRS-02")          # never read
print("function:", is_hot(new_press))
```
```
TypeError: '>' not supported between instances of 'NoneType' and 'int'
```
Speaker notes: This uses the smaller Machine from the notes, built from a tag alone. The function lives outside the class and reads an underscore attribute. It worked on an oven reading seventy-two degrees. It crashed on a press that was never read, because it had to know that the attribute can be None. The method version sits beside the data and already checks for None. When the class changes, the method changes with it. The outside function breaks later, somewhere else.
Image: None. This slide is code.
---
## Slide 7: Watch me call it wrong
```python
print(Machine.status_text(press))
print(Machine.status_text())             # no object handed in
```
```
L3-PRS-01 Press 1
Traceback (most recent call last):
  File "...\status_call.py", line 12, in <module>
    print(Machine.status_text())             # no object handed in
          ~~~~~~~~~~~~~~~~~~~^^
TypeError: Machine.status_text() missing 1 required positional argument: 'self'
```
Speaker notes: I am calling the method on the class with nothing in the parentheses. Read the last line. Missing one required positional argument, self. That error is today's lesson in one line. Self is a real parameter. Through an object, Python fills it. Through the class, you must. The error is really asking a question. Status of which machine?
Image: None. This slide is code.
---
## Slide 8: Some functions should stay functions
- minutes_to_text(95) gives 1 h 35 min
- Works for a press run or your game night
- Needs minutes, not a machine
- Inside a class, it drags in an unused self
Speaker notes: Here is a function that should never move. It turns minutes into readable text. It works for a press run and it works for how long you gamed last night. It needs a number and nothing else. Put it inside Machine and you can no longer use it for anything but machines, and it carries a self it never reads.
Image: A single function card labelled minutes_to_text with arrows to a press icon and a game controller icon.
---
## Slide 9: What you are about to build
- Build 1: Lab U01-02 ToolCrib, Part 2
- Sort 8 procedural functions: method or function
- Write the Tool class with the methods
- Build 2: place every refactor function in your UML
Speaker notes: Build 1 is Lab U01-02, Tool Crib, Part 2. The procedural tool crib has eight functions. For each one, you decide method or function, write one sentence saying why, and then build the Tool class. Build 2 goes back to your refactor project. Every function in your 145060 program gets a home in your draft class diagram, or a note saying it stays a function and why.
Image: A sorting table with two columns, Tool methods and functions, eight cards split between them.
