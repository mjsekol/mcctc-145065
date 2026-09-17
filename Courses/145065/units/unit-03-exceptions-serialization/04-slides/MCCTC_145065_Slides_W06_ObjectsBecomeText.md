# Objects Become Text, and Text Becomes Objects
---
## Slide 1: The power goes out
- Press 1 had 1,250 strokes since service
- Press 2 was locked out by tech-07
- The rack held 640 kg of parts
- The program stops. What survives?
Speaker notes: Every object lives in memory. When the program stops, all of it is gone: the stroke count, the lockout, what is on the rack. Our composite shop needs all three back after a restart, exactly as they were. Today objects become text that outlives the program.
Image: A dark factory floor with a single emergency light.
---
## Slide 2: JSON holds six kinds of value
- Objects and arrays
- Strings and numbers
- true, false, and null
- No Press, no set, no tuple
Speaker notes: JSON can hold objects, which Python calls dictionaries, arrays, which Python calls lists, strings, numbers, true, false, and null. It cannot hold a Press. So each class has to describe itself using only those six.
Image: Six labeled boxes, with a Press icon outside them.
---
## Slide 3: to_dict and from_dict
```python
    def to_dict(self):
        return {"kind": "press", "tag": self.tag, "name": self.name,
                "rated_kw": self.rated_kw, "strokes": self.strokes}

    @classmethod
    def from_dict(cls, data):
        # cls is Press here. Going through the constructor re-checks every rule.
        return cls(data["tag"], data["name"], data["rated_kw"], data["strokes"])
```
Speaker notes: To dict describes the press with plain values. From dict is a class method: it receives the class as cls and builds a new object through the constructor, so every rule the constructor checks is checked for loaded data. Running is deliberately not saved.
Image: None. This slide is code.
---
## Slide 4: There and back
```python
press = Press("L3-PRS-01", "Press 1", 15, strokes=1250)
press.running = True
text = json.dumps(press.to_dict())
print(text)
again = Press.from_dict(json.loads(text))
print(json.dumps(again.to_dict()) == text, again.running)
```
```
{"kind": "press", "tag": "L3-PRS-01", "name": "Press 1", "rated_kw": 15.0, "strokes": 1250}
True False
```
Speaker notes: The text holds five fields. The rebuilt press produces identical text, and it is not running, even though the original was. A machine that ran before a power cut must come back stopped. That is a decision, and you make it in to dict.
Image: None. This slide is code.
---
## Slide 5: Text is bytes
- ASCII: 128 characters, A is 65
- Unicode: a number for every character, Á is 193
- UTF-8: A is one byte, Á is two
- Always open files with encoding="utf-8"
Speaker notes: A file holds bytes. An encoding says which bytes mean which character. ASCII is the old English-only set. Unicode numbers every character in every language. UTF-8 stores those numbers as bytes, one for plain English letters, more for others. On Windows, Python does not assume UTF-8, so always say it.
Image: The letter A beside one byte and the letter Á beside two bytes, navy boxes.
---
## Slide 6: What a name becomes in the file
```
"\u00c1rea de Soldadura"
"Área de Soldadura"
65 b'A'
193 0xc1 b'\xc3\x81'
17 characters, 18 bytes in UTF-8
True
```
Speaker notes: By default, JSON escapes Á as backslash u zero zero c one, six plain characters. With ensure ascii false, it writes the letter. Code point one ninety three, two bytes in UTF-8, so the name is seventeen characters and eighteen bytes. Both spellings load back the same.
Image: None. This slide is code.
---
## Slide 7: The wrong way: handing JSON an object
```python
    def to_dict(self):
        return {"kind": "cell", "name": self.name, "items": self.items}   # forgot .to_dict()


forming = Cell("Forming", [Press("L3-PRS-01", "Press 1", 15)])
print(json.dumps(forming.to_dict()))
```
```
TypeError: Object of type Press is not JSON serializable
```
Speaker notes: The cell put its press objects straight into the list. JSON does not know what a press is. The fix: call to dict on every item. A container's to dict is recursive, like last week.
Image: None. This slide is code.
---
## Slide 8: A round trip that lies
- A tuple goes in
- A list comes back
- No error
- The reloaded data is not equal
Speaker notes: JSON has no tuples. Save a tuple and you get a list back, and the reloaded setup no longer equals the original. Nothing complains. The only defense is a round-trip test that compares what came back with what went in.
Image: A tuple in parentheses entering a box and a list in brackets leaving it.
---
## Slide 9: Decide what is saved
- Saved: ratings, limits, the lockout, the load
- Not saved: running, guard position, live readings
- After a restart, unknown means unsafe
Speaker notes: Save what a restart must remember. Save the lockout, because forgetting it would leave a technician unprotected. Do not save whether a machine was running or where its guard was. After a restart nobody knows, and unknown has to be treated as unsafe.
Image: Two columns, saved and not saved, with a padlock icon in the saved column.
---
## Slide 10: What you are about to build
- Lab U03-02, Part 1
- to_dict and from_dict for three kinds
- dumps, loads, save_line, load_line
- The UTF-8 byte table
- Self-check target: 8 of 17
Speaker notes: Press is the worked example in the lab. You write the same pair for the oven, the conveyor, and the rack, then the four storage functions, then a byte table for a non-English cell name. Build 2 applies it to your own hierarchy with a round-trip test.
Image: A JSON file icon with an arrow back to a class diagram.
