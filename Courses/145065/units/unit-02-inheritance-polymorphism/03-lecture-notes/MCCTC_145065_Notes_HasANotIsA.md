# Lecture Notes: Has a, Not Is a
## 145065 Object-Oriented Programming · Unit 2 · Week 5, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W05_HasANotIsA.md). There is no exported deck yet. To
generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-02-inheritance-polymorphism/04-slides/MCCTC_145065_Slides_W05_HasANotIsA.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.1.6 analyze the strengths and weaknesses of different approaches for solving a
specific problem, here inheritance against composition. 5.3.12 write code to create classes,
objects, and methods.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop. Player names in
worked example 3 are invented.

---

## Why this exists

Press 1 has two sensors: vibration and coolant level. Press 2 has one. Next month the shop may add an
oil temperature sensor to either. If you model readings with inheritance, you need a class for every
combination: a press with vibration, a press with coolant, a press with both. Three kinds of sensor
make eight combinations. A fourth makes sixteen.

That is the sign you picked the wrong relationship. A press is not a sensor. **A press has sensors.**

---

## The concept in plain language

**Composition** builds an object out of other objects it owns. The owner keeps its parts in an
attribute, usually a collection, and asks them for help when it needs it. Passing a question on to a
part is called **delegation**.

Compare the two relationships:

| | Inheritance, "is a" | Composition, "has a" |
|---|---|---|
| How many | exactly one parent chain | any number of parts |
| When it is fixed | when the class is written | while the program runs |
| What you get | every method of the parent, wanted or not | only what the owner chooses to expose |
| Main risk | a child inherits methods that break its own rules | the owner leaks its collection |
| Sentence test | "a press is powered equipment" | "a press has a vibration sensor" |

Neither is always right. That is 5.1.6: a strength and a weakness for each, weighed against the
problem in front of you. The Line 3 model uses both: inheritance for the equipment hierarchy,
composition for sensors.

**The owner guards its parts.** One method adds a part and checks it. The collection itself stays
private, and anything handed out is a copy.

---

## Worked example 1: a press that is a sensor

```python
# press_is_a_sensor.py
class Sensor:
    def __init__(self, sensor_id, unit):
        self.sensor_id = sensor_id
        self.unit = unit
        self.value = None

    def record(self, value):
        self.value = value


class Press(Sensor):                       # "a press is a vibration sensor"
    def __init__(self, asset_tag):
        super().__init__("press-vibration", "mm/s")
        self.asset_tag = asset_tag


press = Press("L3-PRS-01")
press.record(3.1)                          # vibration
press.record(14)                           # coolant level: where does it go?
print(press.sensor_id, press.value, press.unit)
```

Output:

```
press-vibration 14 mm/s
```

The press **is** one sensor, so it has one value. Recording the coolant level overwrote the
vibration reading, and the press now claims 14 mm/s of vibration. No error.

---

## Worked example 2: a press that has sensors

```python
# press_has_sensors.py
class Sensor:
    def __init__(self, sensor_id, unit, low, high):
        self.sensor_id = sensor_id
        self.unit = unit
        self.low, self.high = low, high
        self.value = None

    def record(self, value):
        self.value = value

    def inspect(self, owner):
        if self.value is None:
            return [f"{owner}: {self.sensor_id} has no reading"]
        if not self.low <= self.value <= self.high:
            return [f"{owner}: {self.sensor_id} reads {self.value:g} {self.unit}"]
        return []


class Press:
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self._sensors = {}                 # the press HAS sensors

    def attach_sensor(self, sensor):
        if sensor.sensor_id in self._sensors:
            raise ValueError(f"{self.asset_tag} already has {sensor.sensor_id}")
        self._sensors[sensor.sensor_id] = sensor
        return sensor

    def sensor(self, sensor_id):
        return self._sensors[sensor_id]

    @property
    def sensors(self):
        return tuple(self._sensors.values())   # a copy, never the dict

    def inspect(self):
        findings = []
        for sensor in self._sensors.values():  # delegation: ask each part
            findings.extend(sensor.inspect(self.asset_tag))
        return findings


press = Press("L3-PRS-01")
press.attach_sensor(Sensor("press-vibration", "mm/s", 0, 8))
press.attach_sensor(Sensor("coolant-level", "%", 20, 100))
press.sensor("press-vibration").record(3.1)
press.sensor("coolant-level").record(14)
print([s.sensor_id for s in press.sensors])
print(press.inspect())
```

Output:

```
['press-vibration', 'coolant-level']
['L3-PRS-01: coolant-level reads 14 %']
```

`attach_sensor()` is the one way in, so it is the one place to check for duplicates. `sensors` hands
out a tuple copy. `inspect()` delegates: the press does not know how a sensor judges its reading. It
asks, and passes the answers on.

---

## Worked example 3: a squad that is a list, and a squad that has one

A game squad holds at most four players. First, inheritance:

```python
# squad_is_a_list.py
class Squad(list):                         # "a squad is a list of players"
    MAX = 4

    def add(self, player):
        if len(self) >= Squad.MAX:
            raise ValueError(f"squad is full ({Squad.MAX} players)")
        self.append(player)


squad = Squad()
for player in ["Rook", "Sage", "Nova", "Pike"]:
    squad.add(player)
squad.append("Wren")                       # list gave us append() too
squad.insert(0, "Ash")
print(len(squad), squad)
```

Output:

```
6 ['Ash', 'Rook', 'Sage', 'Nova', 'Pike', 'Wren']
```

`Squad` inherited every method a list has, including `append()` and `insert()`, which never heard of
the four-player rule. Six players, no error.

Now composition:

```python
# squad_has_a_list.py
class Squad:                               # a squad HAS a list of players
    MAX = 4

    def __init__(self):
        self._players = []

    def add(self, player):
        if len(self._players) >= Squad.MAX:
            raise ValueError(f"squad is full ({Squad.MAX} players)")
        self._players.append(player)

    @property
    def players(self):
        return tuple(self._players)


squad = Squad()
for player in ["Rook", "Sage", "Nova", "Pike"]:
    squad.add(player)
print(squad.players)
print(hasattr(squad, "append"))
squad.add("Wren")
```

Output:

```
('Rook', 'Sage', 'Nova', 'Pike')
False
Traceback (most recent call last):
  File "...\squad_has_a_list.py", line 23, in <module>
    squad.add("Wren")
    ~~~~~~~~~^^^^^^^^
  File "...\squad_has_a_list.py", line 10, in add
    raise ValueError(f"squad is full ({Squad.MAX} players)")
ValueError: squad is full (4 players)
```

The squad has no `append()` to misuse. The only way in is `add()`, and `add()` enforces the rule.

---

## The wrong version: composition that leaks

Composition protects the parts only if the owner keeps them private. This version hands out the
dictionary itself:

```python
# leaky_sensors.py
class Sensor:
    def __init__(self, sensor_id, unit, low, high):
        self.sensor_id = sensor_id
        self.unit = unit
        self.low, self.high = low, high
        self.value = None

    def record(self, value):
        self.value = value

    def inspect(self, owner):
        if self.value is None:
            return [f"{owner}: {self.sensor_id} has no reading"]
        if not self.low <= self.value <= self.high:
            return [f"{owner}: {self.sensor_id} reads {self.value:g} {self.unit}"]
        return []


class Press:
    def __init__(self, asset_tag):
        self.asset_tag = asset_tag
        self._sensors = {}                 # the press HAS sensors

    def attach_sensor(self, sensor):
        if sensor.sensor_id in self._sensors:
            raise ValueError(f"{self.asset_tag} already has {sensor.sensor_id}")
        self._sensors[sensor.sensor_id] = sensor
        return sensor

    def sensor(self, sensor_id):
        return self._sensors[sensor_id]

    @property
    def sensors(self):
        return self._sensors                   # the dict itself

    def inspect(self):
        findings = []
        for sensor in self._sensors.values():  # delegation: ask each part
            findings.extend(sensor.inspect(self.asset_tag))
        return findings


press = Press("L3-PRS-01")
press.attach_sensor(Sensor("coolant-level", "%", 20, 100))
press.sensor("coolant-level").record(14)
print("before:", press.inspect())
press.sensors.clear()                      # any code, anywhere, can do this
print("after: ", press.inspect())
```

Output:

```
before: ['L3-PRS-01: coolant-level reads 14 %']
after:  []
```

**No error.** One line outside the class deleted every sensor, and the low-coolant warning vanished
with them. **The fix** is the version in worked example 2: `sensors` returns
`tuple(self._sensors.values())`, a copy the caller can read and cannot change the press with.

---

## Why the wrong version is tempting

Inheritance is tempting because it is fast: one word in the class line, and every method arrives.
The methods you did not want arrive too, and nobody notices until someone calls one.

The leak is tempting because returning `self._sensors` is shorter than returning a copy, and it
works in every test that only reads.

The habits that prevent both: **use the sentence test before every `class B(A)`**, and **never
return a private collection, only a copy**.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Composition** | building an object from parts it owns |
| **"has a" relationship** | the relationship composition models: a press has sensors |
| **Delegation** | passing a request on to a part, such as asking each sensor to inspect itself |
| **Part (component)** | an object owned by another object |
| **Leak** | handing out an object's private collection so callers can change it |
| **Class explosion** | needing a new class for every combination of features |

---

## Self-check

**Question 1.** A forklift has a battery, and batteries are swapped between forklifts during a shift.
Which relationship fits, and which fact in that sentence decides it?

**Question 2.** In worked example 3, `Squad(list)` still has its own `add()` that enforces the limit.
Why is that not enough?

**Question 3.** Write the strongest argument **for** `Squad(list)`, then say why it loses for this
program.

---

### Answers

**1.** Composition. "Swapped during a shift" decides it: inheritance is fixed when the class is
written, and a forklift cannot change which battery it **is**. It can change which battery it
**has**.

**2.** Because `add()` is not the only way in. The list methods `append()`, `insert()`, and `extend()`
all add players and none of them checks the limit.

**3.** For: a squad really is an ordered group of players, and inheriting from `list` gives
`len()`, indexing, and looping for free. It loses because the program has a rule about adding, and a
list offers several ways to add that skip the rule. Composition gives up the free methods and keeps
the rule.
