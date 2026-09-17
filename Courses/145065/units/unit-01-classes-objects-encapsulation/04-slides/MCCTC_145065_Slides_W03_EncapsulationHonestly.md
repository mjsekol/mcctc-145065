# Encapsulation, Honestly
---
## Slide 1: You were told it was private
- Tutorials call _name private
- They call __name really private
- One line of code changes both from outside
- Believing the myth makes you stop guarding data
Speaker notes: Last week I promised you an honest answer about the underscore. Here it is. Python does not stop anyone. A lot of tutorials call one underscore private and two underscores really private. Both claims are wrong in a way that matters, because if you think the language is protecting your data, you stop protecting it yourself. Today you see the truth, and then you learn the tool Python does give you.
Image: A padlock drawn on a whiteboard next to an open door, navy and launch blue.
---
## Slide 2: What the underscores really do
- One underscore: a team convention, nothing more
- Two underscores: Python renames it, called name mangling
- __locked_by becomes _Machine__locked_by
- Renamed is not hidden
- C# private in Unit 6 is a compiler error
Speaker notes: One underscore is a convention. It means internal, and Python allows anyone to read or write it. Two underscores inside a class trigger name mangling. Python renames the attribute to underscore Machine double underscore locked by. Its real job is to stop a subclass from clobbering the name by accident. It does not hide anything. In Unit 6, C# private is enforced by the compiler. That strictness is something C# buys you. Python trusts you instead.
Image: A name tag being relabelled from __locked_by to _Machine__locked_by, with nothing covering it.
---
## Slide 3: Proof
```python
press._running = True
print("running after press._running = True:", press.is_running)
press.lock_out("tech-07")
try:
    print(press.__locked_by)
except AttributeError as error:
    print("Hidden?", error)
press._Machine__locked_by = "anyone"
print("lock holder now:", press.locked_out_by)
print(list(vars(press)))
```
```
running after press._running = True: True
Hidden? 'Machine' object has no attribute '__locked_by'
lock holder now: anyone
['_asset_tag', '_rated_kw', '_running', '_Machine__locked_by']
```
Speaker notes: Read the output line by line. One underscore stopped nothing. The second line looks like protection, but it is only a name that does not exist. The third line is a lockout holder replaced from outside the class. And the last line shows the renamed attribute sitting in plain view. So what protects the machine? Your team, and code review.
Image: None. This slide is code.
---
## Slide 4: The tool Python does give you
- A property looks like an attribute outside
- Reading it runs the getter
- Writing it runs the setter, which can refuse
- No setter means read-only
- The value lives in the underscore name
Speaker notes: A property looks like a plain attribute from the outside and runs a method on the inside. Reading press dot rated kw runs the getter. Writing it runs the setter, and the setter can check the value and refuse. Leave out the setter and the property is read-only. The value itself lives in an underscore attribute, and the property is the guard in front of it. Last week you wrote is running with parentheses. From today it is a property with none. That was the plan.
Image: A guard booth labelled rated_kw in front of a storage box labelled _rated_kw.
---
## Slide 5: A validated property
```python
    def __init__(self, asset_tag, rated_kw):
        self._asset_tag = asset_tag
        self.rated_kw = rated_kw          # no underscore: this runs the setter

    @property
    def asset_tag(self):
        return self._asset_tag            # a getter and no setter: read-only

    @property
    def rated_kw(self):
        return self._rated_kw

    @rated_kw.setter
    def rated_kw(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"rated_kw must be a number, not {type(value).__name__}")
        if not math.isfinite(value) or not 0 < value <= Machine.MAX_RATED_KW:
            raise ValueError(f"rated_kw must be above 0 and at most {Machine.MAX_RATED_KW:g}")
        self._rated_kw = float(value)
```
Speaker notes: Two rules make this work. Inside the setter, store in the underscore name. Everywhere else, including init, go through the property name. Look at the init line. No underscore, so construction runs the same checks as every later change. And look at the two traps in the setter. Bool is checked first because True is a number in Python. And math is finite catches NaN, which slips past every ordinary comparison.
Image: None. This slide is code.
---
## Slide 6: It reads like an attribute and still refuses
```
L3-PRS-01 18.5 False
Refused: rated_kw must be above 0 and at most 500
Refused: rated_kw must be above 0 and at most 500
Refused: rated_kw must be a number, not str
Refused: property 'asset_tag' of 'Machine' object has no setter
Refused at construction: rated_kw must be above 0 and at most 500
```
Speaker notes: Setting the rating to eighteen and a half worked. Negative five, NaN, and the word fast were all refused. The asset tag refused a new value because it has no setter. And the last line proves init runs the setter, because a zero rating cannot even be built.
Image: None. This slide is code.
---
## Slide 7: Watch the setter call itself
```python
    @rated_kw.setter
    def rated_kw(self, value):
        if value <= 0:
            raise ValueError("rated_kw must be above 0")
        self.rated_kw = value         # no underscore
```
```
  File "...\recursive_setter.py", line 13, in rated_kw
    self.rated_kw = value         # the deliberate mistake: no underscore
    ^^^^^^^^^^^^^
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```
Speaker notes: I dropped the underscore inside the setter. Assigning to self dot rated kw runs the setter, which assigns to self dot rated kw, which runs the setter. Python gives up after about a thousand calls. This one is loud, which makes it the friendly mistake. The fix is the underscore.
Image: None. This slide is code.
---
## Slide 8: The quiet one is worse
```python
    def __init__(self, rated_kw):
        self._rated_kw = rated_kw     # skips the setter

press = Machine(-5)
print("Built a press rated at", press.rated_kw, "kW")
```
```
Built a press rated at -5 kW
```
Speaker notes: Now the opposite mistake. The setter is perfect, but init writes the underscore name directly, so the setter never runs during construction. No error. A press rated at negative five kilowatts exists. It is dangerous because it looks like good style. The setter stores in the underscore. Everyone else, init included, goes through the property.
Image: None. This slide is code.
---
## Slide 9: Two traps inside a check that looks fine
- if value <= 0 accepts True, stored as 1
- bool is a kind of int in Python
- Every comparison with NaN is False
- So NaN passes value <= 0 too
- Check bool first; use not math.isfinite(value)
Speaker notes: A setter with only if value less than or equal to zero looks like validation. It accepts True, because bool is a kind of int and True is one. It also accepts NaN, because every comparison with NaN is false, even NaN equals NaN. A NaN setpoint then poisons every calculation it touches. Check for bool first, and use not math is finite, which catches NaN and infinity.
Image: A security checkpoint where a card labelled True and a card labelled NaN walk through a gate marked value <= 0.
---
## Slide 10: What you are about to build
- Build 1: Lab U01-03 GuardTheState, Part 1
- An Oven with public attributes a rogue script abuses
- Underscores, validated properties, read-only state
- Prove what the underscore does not stop
- Build 2: finish Part 1, then refactor Improve
Speaker notes: Build 1 is Lab U01-03, Guard the State, Part 1. You get an Oven class with public attributes and a rogue script that abuses them. You underscore the state, add validated properties, make the right things read-only, and then write proof of what the underscore still does not stop. Build 2 gives you twenty more minutes on the lab, then twenty on your refactor project.
Image: An industrial oven control label with a setpoint field and a lock icon, navy and launch blue.
