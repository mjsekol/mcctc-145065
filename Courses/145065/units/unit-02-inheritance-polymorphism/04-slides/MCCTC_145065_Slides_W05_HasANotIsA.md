# Has a, Not Is a
---
## Slide 1: Eight classes for three sensors
- Press with vibration
- Press with coolant
- Press with both
- Add oil temperature: now eight combinations
Speaker notes: Last year someone added sensor readings to the press by inheritance. A press with vibration became one class. A press with coolant became another. A press with both became a third, pasted together. Add one more sensor type and there are eight combinations. When the number of classes doubles every time you add a feature, the relationship is wrong.
Image: A grid of eight press icons, each with a different set of small sensor badges.
---
## Slide 2: A press has sensors
- Is a: inheritance, one chain, fixed when written
- Has a: composition, any number, changeable while running
- Run the sentence test on both
Speaker notes: A press is not a sensor. A press has sensors. Inheritance gives you one parent chain, decided when the class is written. Composition lets an object own any number of parts, of any mix, and change them while the program runs.
Image: A press with two sensor modules plugged into it, labeled has.
---
## Slide 3: The wrong way: a press that is a sensor
```python
class Press(Sensor):                       # "a press is a vibration sensor"
    def __init__(self, asset_tag):
        super().__init__("press-vibration", "mm/s")
        self.asset_tag = asset_tag


press = Press("L3-PRS-01")
press.record(3.1)                          # vibration
press.record(14)                           # coolant level: where does it go?
print(press.sensor_id, press.value, press.unit)
```
```
press-vibration 14 mm/s
```
Speaker notes: This press inherits from Sensor, so it is one sensor with one value. Record vibration, then coolant. The coolant reading overwrote the vibration, and now the press claims fourteen millimeters per second of vibration. No error.
Image: None. This slide is code.
---
## Slide 4: A press that owns its parts
```python
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
```
Speaker notes: The press keeps a dictionary of sensors. Attach sensor is the one door in, so it is the one place that checks for duplicates. Sensors hands out a tuple copy. Inspect asks each sensor and passes the answers on. That is delegation.
Image: None. This slide is code.
---
## Slide 5: Two sensors, one press
```
['press-vibration', 'coolant-level']
['L3-PRS-01: coolant-level reads 14 %']
```
Speaker notes: Two sensors, both kept. Vibration is fine at three point one, so it reports nothing. Coolant is low at fourteen percent, so it reports. The press did not need to know how either sensor judges its reading.
Image: None. This slide is code.
---
## Slide 6: Inheritance brings methods you did not want
- class Squad(list) gets append() and insert()
- Neither one checks the four-player limit
- Six players, no error
- Composition exposes only add()
Speaker notes: A game squad that inherits from list gets every list method, and append and insert never heard of the four-player rule. The composed squad has no append. The only way in is add, and add enforces the limit.
Image: A roster card with six names crammed onto a four-line form.
---
## Slide 7: Composition can leak too
```python
    @property
    def sensors(self):
        return self._sensors                   # the dict itself
```
```
before: ['L3-PRS-01: coolant-level reads 14 %']
after:  []
```
Speaker notes: Composition only protects the parts if the owner keeps them private. This version returns the dictionary itself. One line outside the class calls clear, and the low coolant warning is gone. No error anywhere. Return a copy.
Image: None. This slide is code.
---
## Slide 8: Strengths and weaknesses
- Inheritance: free methods, one fixed parent
- Composition: any mix, more code to write
- Neither is always right
- Weigh them against this problem
Speaker notes: This is the competency this week earns: weigh the strengths and weaknesses of approaches for a specific problem. Inheritance gives you methods for free and locks in one parent. Composition takes more code and lets the parts vary. The Line 3 model uses both, each where it fits.
Image: A balance scale with inheritance on one side and composition on the other.
---
## Slide 9: Your written analysis
- One place you used inheritance, and why
- One place you refused it, and what you used
- The strongest argument against each choice
Speaker notes: Your project's analysis asks for exactly this. Where did you inherit, and why is the sentence test true there. Where did you consider inheritance and refuse it. And for each choice, the best argument someone could make against you.
Image: A two-column notebook page headed used and refused.
---
## Slide 10: What you are about to build
- Lab U02-04, Sensors Are Parts
- Give powered equipment a collection of sensors
- attach_sensor() with three refusals
- Delete the four reading subclasses
- Write your inheritance or composition paragraph
Speaker notes: The lab starts from the eight-class mess. You give powered equipment a sensor collection, write attach sensor with its refusals, make the oven read its own temperature sensor, and delete the four reading subclasses. Step seven breaks it on purpose by leaking the dictionary. Nine of nine.
Image: Four crossed-out subclass boxes beside one press with a sensor rack.
