# Lecture Notes: Objects Become Text, and Text Becomes Objects
## 145065 Object-Oriented Programming · Unit 3 · Week 6, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W06_ObjectsBecomeText.md). There is no exported deck yet.
To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-03-exceptions-serialization/04-slides/MCCTC_145065_Slides_W06_ObjectsBecomeText.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 5.5.6 format output for data files. 2.3.1 identify and explain coding information
and representation of characters (ASCII, Unicode). This is the only place in the course that teaches
character encoding.

**About the setting.** Riverside Fabrication is a **composite**, an invented shop. The player name
in worked example 2 is invented.

---

## Why this exists

When the program stops, every object in memory is gone. The press that had 1,250 strokes since
service, the lockout tech-07 applied, the parts on the rack: all of it. To survive a restart, the
objects have to become something that lives on disk, and then become objects again.

That round trip has to be exact. A shop that reloads its line and gets back slightly different
settings has a problem worse than losing them, because nobody notices.

---

## The concept in plain language

**Serialization** turns objects into a format that can be stored or sent. **Deserialization** turns
it back into objects. This course uses **JSON**, a text format that holds only six kinds of value:
objects (Python dicts), arrays (lists), strings, numbers, `true`/`false`, and `null` (`None`). It
cannot hold a `Press`.

So each class does two jobs:

- **`to_dict()`** describes the object using only those six kinds of value. A parent writes the
  shared fields, and each child adds its own.
- **`from_dict(data)`** is a **class method** (`@classmethod`). It receives the class itself as
  `cls` and returns a new object. It rebuilds the object **through the constructor**, so every rule
  the constructor checks is checked for loaded data too.

Then `json.dumps()` turns the dicts into text, and `json.loads()` turns text back into dicts.

**Decide what is saved.** Configuration and safety state are saved: ratings, limits, the lockout.
Running state is not. A machine that was running before a power cut must come back **stopped**.

**Text is bytes.** A file holds bytes, not letters. An **encoding** says which bytes stand for which
character.

- **ASCII** is the original 128 characters: English letters, digits, punctuation. `A` is 65.
- **Unicode** gives a number, a **code point**, to every character in every writing system. `Á` is 193,
  written `U+00C1`.
- **UTF-8** stores Unicode as bytes. An ASCII character takes one byte, so plain English text is the
  same in ASCII and UTF-8. `Á` takes two bytes.

`json.dumps()` has a choice: with `ensure_ascii=True` (the default) it writes `Á` as the six ASCII
characters `Á`. With `ensure_ascii=False` it writes the letter itself, and the file must then be
written as UTF-8. **Always pass `encoding="utf-8"` when you open a text file.** On Windows, Python
3.13 and 3.14 do not use UTF-8 by default. [VERIFY on the lab's Python 3.14: the default encoding on
Windows lab machines.]

---

## Worked example 1: one press, there and back

```python
# press_round_trip.py
import json


class Press:
    def __init__(self, tag, name, rated_kw, strokes=0):
        if rated_kw <= 0:
            raise ValueError("rated_kw must be above 0")
        self.tag = tag
        self.name = name
        self.rated_kw = float(rated_kw)
        self.strokes = strokes
        self.running = False           # not saved: a restarted press is stopped

    def to_dict(self):
        return {"kind": "press", "tag": self.tag, "name": self.name,
                "rated_kw": self.rated_kw, "strokes": self.strokes}

    @classmethod
    def from_dict(cls, data):
        # cls is Press here. Going through the constructor re-checks every rule.
        return cls(data["tag"], data["name"], data["rated_kw"], data["strokes"])


press = Press("L3-PRS-01", "Press 1", 15, strokes=1250)
press.running = True
text = json.dumps(press.to_dict())
print(text)
again = Press.from_dict(json.loads(text))
print(json.dumps(again.to_dict()) == text, again.running)
```

Output:

```
{"kind": "press", "tag": "L3-PRS-01", "name": "Press 1", "rated_kw": 15.0, "strokes": 1250}
True False
```

The text holds the five saved fields and nothing else. The rebuilt press produces identical text, and
it is **not** running, even though the original was. That is by design.

---

## Worked example 2: a game save

```python
# save_game.py
import json


class SaveGame:
    def __init__(self, player, level, inventory):
        self.player = player
        self.level = level
        self.inventory = inventory          # item name -> count

    def to_dict(self):
        return {"player": self.player, "level": self.level, "inventory": dict(self.inventory)}

    @classmethod
    def from_dict(cls, data):
        return cls(data["player"], data["level"], data["inventory"])


game = SaveGame("Nova", 7, {"potion": 3, "rope": 1})
text = json.dumps(game.to_dict(), indent=2)
print(text)
loaded = SaveGame.from_dict(json.loads(text))
print(loaded.level, loaded.inventory["potion"])
print(json.dumps(loaded.to_dict(), indent=2) == text)
```

Output:

```
{
  "player": "Nova",
  "level": 7,
  "inventory": {
    "potion": 3,
    "rope": 1
  }
}
7 3
True
```

`to_dict()` copies the inventory with `dict(...)`, so the saved description cannot be changed by
changing the live game afterward. The last line is the round-trip test you will write for your own
project: text, to object, to text, and compare.

---

## Worked example 3: what a name becomes in the file

```python
# bytes_of_a_name.py
import json

name = "Área de Soldadura"
print(json.dumps(name))
print(json.dumps(name, ensure_ascii=False))
print(ord("A"), "A".encode("utf-8"))
print(ord("Á"), hex(ord("Á")), "Á".encode("utf-8"))
print(len(name), "characters,", len(name.encode("utf-8")), "bytes in UTF-8")
print(json.loads(json.dumps(name)) == json.loads(json.dumps(name, ensure_ascii=False)))
```

Output:

```
"\u00c1rea de Soldadura"
"Área de Soldadura"
65 b'A'
193 0xc1 b'\xc3\x81'
17 characters, 18 bytes in UTF-8
True
```

Line by line:

1. The default escapes `Á` as `Á`: six ASCII characters. Any old tool can read the file, and no
   person can.
2. `ensure_ascii=False` writes the letter.
3. `A` is 65 in both ASCII and Unicode, and one byte in UTF-8.
4. `Á` is code point 193 (hexadecimal `c1`), and two bytes in UTF-8: `c3 81`.
5. So the name is 17 characters and 18 bytes.
6. Both spellings load back to the same string. The choice changes the file, not the data.

---

## The wrong version, twice

### Handing JSON an object

```python
# cell_not_converted.py
import json


class Press:
    def __init__(self, tag, name, rated_kw, strokes=0):
        if rated_kw <= 0:
            raise ValueError("rated_kw must be above 0")
        self.tag = tag
        self.name = name
        self.rated_kw = float(rated_kw)
        self.strokes = strokes
        self.running = False           # not saved: a restarted press is stopped

    def to_dict(self):
        return {"kind": "press", "tag": self.tag, "name": self.name,
                "rated_kw": self.rated_kw, "strokes": self.strokes}

    @classmethod
    def from_dict(cls, data):
        # cls is Press here. Going through the constructor re-checks every rule.
        return cls(data["tag"], data["name"], data["rated_kw"], data["strokes"])


class Cell:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def to_dict(self):
        return {"kind": "cell", "name": self.name, "items": self.items}   # forgot .to_dict()


forming = Cell("Forming", [Press("L3-PRS-01", "Press 1", 15)])
print(json.dumps(forming.to_dict()))
```

Output:

```
Traceback (most recent call last):
  File "...\cell_not_converted.py", line 35, in <module>
    print(json.dumps(forming.to_dict()))
          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "...\Lib\json\__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "...\Lib\json\encoder.py", line 200, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "...\Lib\json\encoder.py", line 261, in iterencode
    return _iterencode(o, 0)
  File "...\Lib\json\encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    f'is not JSON serializable')
TypeError: Object of type Press is not JSON serializable
```

`Cell.to_dict()` put the `Press` objects themselves into its list. JSON does not know what a `Press`
is. **The fix:** `"items": [item.to_dict() for item in self.items]`. A container's `to_dict()` calls
`to_dict()` on everything it holds, which makes it recursive, like Week 4.

### A round trip that quietly changes the data

```python
# tuple_round_trip.py
import json

setup = {"die": "D-117", "shut_height_mm": 433.5, "shims_mm": (0.5, 0.25)}
text = json.dumps(setup)
back = json.loads(text)
print(text)
print(back["shims_mm"], type(back["shims_mm"]).__name__)
print(back == setup)
```

Output:

```
{"die": "D-117", "shut_height_mm": 433.5, "shims_mm": [0.5, 0.25]}
[0.5, 0.25] list
False
```

**No error.** JSON has arrays and no tuples, so the tuple went in and a list came back, and the
reloaded setup is no longer equal to the original. **The fix:** convert on the way in
(`tuple(data["shims_mm"])` in `from_dict()`), and write the round-trip test that catches it.

---

## Why the wrong version is tempting

`json.dumps(obj.__dict__)` looks like a shortcut that saves every class at once. It fails on the first
nested object, and when it works, it saves private state you meant to leave out, such as `running`.

The tuple problem is tempting because the saved file looks right. You only see it when you compare
what came back with what went in.

The habits that prevent both: **each class writes its own `to_dict()` with exactly the fields a
restart needs**, and **every project has a round-trip test.**

---

## Vocabulary

| Term | What it means |
|---|---|
| **Serialization** | turning objects into a storable format, such as JSON text |
| **Deserialization** | turning stored data back into objects |
| **Round trip** | saving and loading, then checking the result is identical |
| **Class method** | a method that receives the class as `cls`, marked `@classmethod`; used here to build objects |
| **ASCII** | the original 128-character code: English letters, digits, punctuation |
| **Unicode** | the standard that numbers every character in every writing system |
| **Code point** | a character's Unicode number, such as 193 for `Á` |
| **UTF-8** | the encoding that stores Unicode as one to four bytes per character |
| **`ensure_ascii`** | the `json.dumps` option that escapes every non-ASCII character |

---

## Self-check

**Question 1.** Why does `from_dict()` call the constructor instead of setting attributes on an empty
object?

**Question 2.** How many bytes does the word `Área` take in UTF-8? In a JSON file written with
`ensure_ascii=True`, how many characters does it take between the quotes?

**Question 3.** Name one thing your project should deliberately **not** save, and why.

---

### Answers

**1.** So loaded data goes through the same checks as new data. A file with `"rated_kw": -15` is then
refused by the constructor's rule, instead of creating an impossible press.

**2.** Five bytes: `Á` is two, and `r`, `e`, `a` are one each. With `ensure_ascii=True` it is nine
characters: `Á` (six) plus `rea` (three).

**3.** Anything true only while the program runs: whether a machine is running, a guard's position, a
live sensor reading. After a restart those are unknown, and unknown must be treated as unsafe, not
reloaded as if it were still true.
