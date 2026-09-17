# A File Is Untrusted Input
---
## Slide 1: My program wrote it, so I trust it
- Someone edits it in Notepad
- Someone copies it from an older version
- The power cuts it off mid-save
- Someone changes it on purpose
Speaker notes: My program wrote this file, so I can trust it. Every part of that sentence fails on a shop floor. Files get hand-edited, copied from old machines, cut off by power loss, and sometimes changed on purpose. Loading a file is the moment your program trusts outside data. That makes it where security lives.
Image: A file icon passing through four hands.
---
## Slide 2: NaN passes every check
```
nan
overloaded: False
within capacity: False
refused: NaN is not allowed in a plant file
```
Speaker notes: Python reads NaN from JSON even though it is not valid JSON. And NaN is neither greater than the capacity nor less than or equal to it. Any check written as if load is over capacity, warn, stays silent forever. Parse constant lets you refuse it.
Image: None. This slide is code.
---
## Slide 3: Check in layers, cheapest first
- Size, before reading a byte
- Encoding, then JSON syntax, no NaN
- Shape: no missing or extra fields
- Types, then kind from an allowlist
- Values, through the constructor
Speaker notes: A guarded loader checks in layers and stops at the first problem. Ask the operating system for the size first. Then the encoding, the syntax, the shape, the types, the kind, and finally the values, through the same constructor every object goes through. Every refusal says where.
Image: A stack of seven filters, largest at the top.
---
## Slide 4: An allowlist and a where
```python
KINDS = {  # the file may pick one of these, and nothing else
    "press": (Press, {"kind", "tag", "rated_kw"}),
    "rack": (Rack, {"kind", "tag", "capacity_kg"}),
}


def build(data, where):
    entry = KINDS.get(data.get("kind"))
    if entry is None:
        raise LoadError(f"{where}.kind", f"unknown kind {data.get('kind')!r}")
    cls, fields = entry
    if set(data) != fields:
        raise LoadError(where, f"fields must be exactly {sorted(fields)}")
    if cls is Press:
        return Press(data["tag"], number(data["rated_kw"], f"{where}.rated_kw"))
    return Rack(data["tag"], number(data["capacity_kg"], f"{where}.capacity_kg"))
```
Speaker notes: The file may pick press or rack and nothing else. The fields must match exactly. Numbers must be numbers, and true is not a number here, even though Python counts it as one. Every error carries a where.
Image: None. This slide is code.
---
## Slide 5: Three refusals, three places
```
built Press L3-PRS-01
refused items[1].rated_kw: must be a number, not bool
refused items[2].kind: unknown kind 'Line'
refused items[3]: fields must be exactly ['capacity_kg', 'kind', 'tag']
```
Speaker notes: A true where a number belongs. A kind that is not on the list. A misspelled extra field. Each refusal names the exact place, so the person fixing the file knows where to look.
Image: None. This slide is code.
---
## Slide 6: The wrong way: the file chooses
```python
def build(data):
    cls = globals()[data.pop("kind")]          # the file names the class
    item = cls.__new__(cls)                    # skip __init__ and its checks
    item.__dict__.update(data)                 # the file writes any attribute
    return item


press = build(json.loads('{"kind": "Press", "tag": "L3-PRS-01", "rated_kw": -15, "_guard_closed": true}'))
print(press.tag, press.rated_kw, press._guard_closed)
build(json.loads('{"kind": "json", "tag": "x"}'))
```
Speaker notes: This loader looks the class up by the name in the file, skips the constructor, and copies every field onto the object. It is short, and it loads every file your own program writes. Predict what this file does.
Image: None. This slide is code.
---
## Slide 7: What the file did
```
L3-PRS-01 -15 True
Traceback (most recent call last):
  File "...\globals_loader.py", line 22, in <module>
    build(json.loads('{"kind": "json", "tag": "x"}'))
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "...\globals_loader.py", line 15, in build
    item = cls.__new__(cls)                    # skip __init__ and its checks
TypeError: module.__new__(X): X is not a type object (module)
```
Speaker notes: A negative rating the constructor would refuse. A private guard flag set to closed. And a file that named a module crashed the loader with an error nobody planned for. The fix is the allowlist on slide four.
Image: None. This slide is code.
---
## Slide 8: Why this course never uses pickle
```python
class Surprise:
    def __reduce__(self):
        # pickle stores "call print with this text" instead of the object.
        return (print, ("this line ran while the file was being LOADED",))


data = pickle.dumps(Surprise())
print(len(data), "bytes of pickle")
result = pickle.loads(data)
print("loads() returned", result)
```
```
85 bytes of pickle
this line ran while the file was being LOADED
loads() returned None
```
Speaker notes: This demonstration only prints. Pickle can store call this function instead of data, and loads makes the call while loading. The printed line came from reading data. If the stored call were anything else, it would run the same way. JSON can only hold data. That is the whole reason.
Image: None. This slide is code.
---
## Slide 9: The file that passes every check
- lockout_erased.json is well formed
- Every field has the right type
- It has lost a lockout
- Validation cannot prove nobody edited it
Speaker notes: One sample file passes every layer and is still dangerous: someone erased a lockout. Validation proves a file is well formed. It cannot prove it is true. That is why tomorrow is about backups, and why the extended option adds a checksum.
Image: A green checkmark on a document with a missing padlock.
---
## Slide 10: What you are about to build
- Lab U03-02, Part 2
- The allowlist for three more kinds
- A guarded loads() and load_line()
- Twelve sample files to refuse or accept
- Self-check target: 13 of 17
Speaker notes: You fill in the allowlist, guard loads with parse constant and the migrate call, and guard load line with the size check, UTF-8 with the byte order mark, and a missing-file error. Then you run every file in the bad folder. Build 2 is your own guarded loader with three bad-file tests.
Image: A folder of twelve file icons, ten with a launch red X and two with a check.
