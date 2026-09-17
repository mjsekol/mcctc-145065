# New Layers on Old Systems
---
## Slide 1: Where did your steps go
- Your watch counts steps
- Your phone shows them later
- A website shows them after that
- How many stops did that number make
Speaker notes: This morning's bell ringer. Your step count starts on your wrist and ends up on a website that existed long before your watch did. It made several stops on the way. Every emerging technology you will read about works like that. The interesting part is not the watch or the website. It is the stops in between.
Image: A wristwatch, a phone, and a laptop connected by arrows, navy and launch blue.
---
## Slide 2: New technology rarely replaces anything
- A shop still has its maintenance log
- A school still has its records system
- The new thing is a layer on top
- It is useless until it reaches the old system
Speaker notes: Here is today's idea. Articles make emerging technology sound like a replacement for everything. In a real business it almost never is. It is a new layer bolted onto systems that already run. And it is worth nothing until its output reaches one of them. The join is where the work is, and where projects fail.
Image: A stack of blocks with an older base labeled existing systems and a new colored block on top.
---
## Slide 3: Four technologies, one shape
- IoT: sensor, device, gateway, network, application
- Large language model: text in, model server, text out
- Machine learning: past data, training, model, prediction
- Additive manufacturing: design file, slicer, instructions, printer
Speaker notes: The syllabus names four. Each is a pipeline. Something produces data, something processes it, something carries it, something that already existed uses it. A large language model is a kind of machine learning, listed separately because you use it differently. You send text and get text back, like you did with the local model last semester.
Image: Four horizontal pipelines stacked, each with four labeled stages, launch blue arrows.
---
## Slide 4: One reading, four layers
```python
import json

reading = {"id": "oven-temp", "value": 212.4, "unit": "C", "ok": True}
message = json.dumps({"device": "line3-pi", "sensors": [reading]})
received = message
print(type(received).__name__, len(received), "characters")

payload = json.loads(received)
sensor = payload["sensors"][0]
fahrenheit = round(sensor["value"] * 9 / 5 + 32, 1)
print("Paint cure oven,temperature," + str(fahrenheit) + ",F")
```
Speaker notes: Riverside Fabrication is an invented shop we use all semester. Device layer, a reading. Gateway, packaged as JSON text. Transport, only text crosses. Integration, turned back into data and reshaped for the shop's existing log, which has always been in Fahrenheit. The new sensor fits the old log, not the other way round.
Image: None. This slide is code.
---
## Slide 5: The row the supervisor already reads
```
str 97 characters
Paint cure oven,temperature,414.3,F
```
Speaker notes: The first line proves text crossed the boundary. The second line is a row in a spreadsheet the supervisor has opened every morning for years. That second line is the whole value of the sensor. Without it the sensor is a number nobody sees.
Image: None. This slide is code.
---
## Slide 6: Change one field name
```python
reading = {"id": "oven-temp", "reading": 212.4, "unit": "C", "ok": True}
```
Speaker notes: Now the person who writes the device layer decides reading is a better name than value. Seems harmless. Predict what happens, and predict which layer notices.
Image: None. This slide is code.
---
## Slide 7: The far side notices
```
str 99 characters
Traceback (most recent call last):
  File "...\layers.py", line 19, in <module>
    fahrenheit = round(sensor["value"] * 9 / 5 + 32, 1)
                       ~~~~~~^^^^^^^^^
KeyError: 'value'
```
Speaker notes: The change was in layer one. The crash is in layer four. The transport line printed happily, because text is text. The two sides stopped agreeing on the shape of the message. That agreement has a name, a contract, and your Unit 8 operator panel lives or dies by one.
Image: None. This slide is code.
---
## Slide 8: The worse bug does not crash
- Skip the Celsius conversion
- 221.5 lands in a Fahrenheit column
- 221.5 C is 430.7 F, over the limit
- The log says OK
Speaker notes: The key error was the kind bug. It stopped us. Here is the unkind one. Forget the conversion, and the log records an oven at 221.5 degrees Fahrenheit, which looks cool and safe. The real temperature is over the shop's limit. No error anywhere. You will produce this on purpose in the lab.
Image: A log row with OK in green and a thermometer reading far higher, a launch red outline around it.
---
## Slide 9: Where each one joins existing IT
- IoT: rows in the maintenance log
- LLM: an existing program sends and reads text
- Machine learning: a program asks for a prediction
- Printing: the design file joins part records
Speaker notes: For your brief, you must name the join. For IoT, it is the log or database. For a language model, it is a program that already exists and calls the model. For machine learning, a program asks for a prediction and decides what to do with it. For additive manufacturing, the design file becomes a business record with a part number and a version.
Image: Four small icons each connected by one arrow to a shared box labeled existing systems.
---
## Slide 10: What you are about to build
- Lab U00-02: Sensor to Spreadsheet
- Write the integration layer for Line 3
- Convert units, handle a sensor that stays silent
- Then choose your brief's technology
Speaker notes: The lab gives you a working device, gateway, and transport layer. You write the integration layer that lands readings in the shop's existing log. You convert units, you write NO READING when a sensor does not answer, and you break it on purpose to see the silent bug. In the last ten minutes, pick your technology for the brief and log the one you rejected.
Image: A spreadsheet with three new rows, one marked CHECK and one marked NO READING, navy header.
