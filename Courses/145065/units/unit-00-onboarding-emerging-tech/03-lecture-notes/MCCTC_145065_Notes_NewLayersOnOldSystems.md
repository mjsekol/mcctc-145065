# Lecture Notes: New Layers on Old Systems
## 145065 Object-Oriented Programming · Unit 0 · Week 1, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W01_NewLayersOnOldSystems.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-00-onboarding-emerging-tech/04-slides/MCCTC_145065_Slides_W01_NewLayersOnOldSystems.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 2.4.1 identify emerging technologies applicable to the marketplace. 2.4.2 describe
their fundamental architectures and how they integrate into existing IT systems. 2.4.4 describe
emerging technologies, including IoT, large language models, machine learning, and additive
manufacturing. 5.1.1 describe how programs solve problems.

**About the setting.** Riverside Fabrication and its Line 3 are a **composite**: an invented small
metal fabrication shop used all semester. No real company is described.

---

## Why this exists

Every week you will read that some new technology is about to change everything. The articles
describe the technology. They rarely describe the hard part, which is connecting it to what a business
already runs.

A shop that buys sensors still has its maintenance log. A school that adopts a language model still
has its student information system. **An emerging technology is almost never a replacement. It is a
new layer on top of old systems**, and it is useless until its output reaches one of them.

If you can draw the layers and point at the join, you can describe any of these technologies, and you
can see where a project will go wrong before it does.

---

## The concept in plain language

Each technology is a pipeline. Something produces data. Something processes it. Something carries it.
Something that **already existed** uses it.

Between every pair of layers is a boundary. Only an agreed shape crosses it, usually text such as
JSON. Both sides must agree on that shape. The agreement is called a **contract**.

### The four technologies

| Technology | What it is | Layers, input to output | Where it joins existing IT |
|---|---|---|---|
| **Internet of Things (IoT)** | physical devices with sensors that send data over a network | sensor, device, gateway, network, server, application | readings land in a log, spreadsheet, or maintenance database the business already uses |
| **Large language model (LLM)** | a model trained on a very large amount of text to predict the next piece of text | prompt text, model server holding trained weights, generated text | an existing program sends text over HTTP and reads text back |
| **Machine learning (ML)** | programs that learn patterns from past data instead of following hand-written rules | historical data, training, a trained model, predictions on new data | an existing program asks the model for a prediction, then decides what to do |
| **Additive manufacturing** | building a part layer by layer from a digital design, often called 3D printing | 3D design file, slicing software, machine instructions, printer | the design file joins drawings, part numbers, and change control |

A large language model is one kind of machine learning. The syllabus lists it separately because it is
used differently: you send it text and it sends text back.

### Programs that solve problems

Programs come in kinds, and emerging technologies show up in all of them: **desktop** programs on one
computer, **mobile** apps, **enterprise** systems a whole company shares, **AI** services, and
**cloud** services run on someone else's servers. The Line 3 pipeline touches three: a small program
on a device, an enterprise record (the maintenance log), and, if the shop chose it, a cloud service.

---

## Worked example 1: one IoT reading, four layers

```python
# layers.py
# One reading, four layers.
import json

# 1. DEVICE: the sensor on the Pi produces a number.
reading = {"id": "oven-temp", "value": 212.4, "unit": "C", "ok": True}

# 2. GATEWAY: the Pi packages it as text in an agreed shape.
message = json.dumps({"device": "line3-pi", "sensors": [reading]})

# 3. TRANSPORT: only text crosses the network.
received = message
print(type(received).__name__, len(received), "characters")

# 4. INTEGRATION: the receiving side turns text back into data
#    and reshapes it for the system that already exists.
payload = json.loads(received)
sensor = payload["sensors"][0]
fahrenheit = round(sensor["value"] * 9 / 5 + 32, 1)
print("Paint cure oven,temperature," + str(fahrenheit) + ",F")
```

Output:

```
str 97 characters
Paint cure oven,temperature,414.3,F
```

The last line is a row in the shop's **existing** log, which records temperature in Fahrenheit. The
new sensor reports Celsius. The integration layer converts, because the new technology has to fit the
old system, not the other way round.

---

## Worked example 2: an LLM is called like any other service

```python
import json

# The existing program builds a request. Nothing is sent in this example.
request_body = {
    "model": "llama3.2",
    "prompt": "Summarize: Press 2 vibration over limit twice this shift.",
    "stream": False,
}
text = json.dumps(request_body)
print("POST http://127.0.0.1:11434/api/generate")
print(text)
print(type(text).__name__, "crosses the boundary, not a Python dictionary")
```

Output:

```
POST http://127.0.0.1:11434/api/generate
{"model": "llama3.2", "prompt": "Summarize: Press 2 vibration over limit twice this shift.", "stream": false}
str crosses the boundary, not a Python dictionary
```

You sent requests like this to a locally hosted model in 145060 Unit 7. The model server is one
layer. Your program is another. Text crosses between them. In this program, models run on lab
hardware, and no student personal data goes into any AI tool.

---

## Worked example 3: machine learning, in miniature

```python
import statistics

# TRAINING: past vibration readings from normal running (invented data).
history = [2.9, 3.1, 3.0, 3.3, 2.8, 3.2, 3.0, 3.1]
mean = statistics.mean(history)
spread = statistics.stdev(history)
learned_limit = round(mean + 3 * spread, 2)
print("Learned limit:", learned_limit)

# INFERENCE: the existing program asks the "model" about new readings.
for value in [3.2, 3.9, 7.4]:
    verdict = "unusual" if value > learned_limit else "normal"
    print(value, verdict)
```

Output:

```
Learned limit: 3.53
3.2 normal
3.9 unusual
7.4 unusual
```

This is far simpler than real machine learning, and it shows the same shape. Nobody typed the limit.
It came from the data. **If the history contains a bad week, the limit learns the bad week too.** A
model is only as good as the data it learned from.

---

## Worked example 4: additive manufacturing is layers too

```python
import math

# A bracket 18.0 mm tall, printed in 0.2 mm layers (invented part).
part_height_mm = 18.0
layer_height_mm = 0.2
layers = math.ceil(part_height_mm / layer_height_mm)
print("Layers:", layers)
```

Output:

```
Layers: 90
```

Slicing software turns a 3D design into layers and then into machine instructions. The design file
is now part of the business record, like a drawing: it needs a part number, a version, and someone who
approves changes.

---

## The wrong version, and the error it produces

Change the device layer in example 1 so the field is called `"reading"` instead of `"value"`:

```python
reading = {"id": "oven-temp", "reading": 212.4, "unit": "C", "ok": True}
```

Output:

```
str 99 characters
Traceback (most recent call last):
  File "...\layers.py", line 19, in <module>
    fahrenheit = round(sensor["value"] * 9 / 5 + 32, 1)
                       ~~~~~~^^^^^^^^^
KeyError: 'value'
```

The change was in layer 1. The crash is in layer 4. The transport layer printed its line happily,
because text is text. **The contract broke, and only the far side noticed.**

### The worse version, which does not crash

Skip the conversion, and the pipeline writes `221.5` into a column the supervisor reads as
Fahrenheit. An oven at 221.5 C is 430.7 F, over the shop's 425 F limit. The log calls it OK. No error
appears anywhere. You will produce this on purpose in Lab U00-02.

---

## Why the wrong version is tempting

Each layer looks finished on its own. The device reads a number. The gateway sends it. The receiver
reads it. Each person tests their own layer and it passes. Nobody tests the boundary, because nobody
owns it.

The habit that prevents it: write the contract down, test across the boundary, and treat a missing
field or a unit mismatch as the first thing to check.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Architecture** | the layers of a system and what passes between them |
| **Integration** | connecting a new system to the systems a business already runs |
| **Layer** | one stage of a pipeline with one job |
| **Contract** | the agreed shape of data that crosses a boundary |
| **Gateway** | a device or program that collects readings and passes them on |
| **Training** | building a model from past data |
| **Inference** | using a trained model to answer about new data |
| **Slicing** | turning a 3D design into printable layers and machine instructions |

---

## Self-check

**Question 1.** Name the layer where an IoT reading joins the shop's existing maintenance log, and say
what that layer has to do in the Line 3 pipeline.

**Question 2.** Worked example 3 learned its limit from eight readings. Give one way the learned limit
could be wrong, and what it would cause.

**Question 3.** Why is an LLM described as "a layer an existing program calls" rather than "a
program you use"?

---

### Answers

**1.** The integration layer. It turns the JSON text back into data and reshapes it for the existing
log: the equipment names the floor uses, timestamps in the log's format, Celsius converted to
Fahrenheit, and a blank value with a `NO READING` status when a sensor did not answer.

**2.** If the history came from a week when the press was already wearing out, the readings would be
higher and so would the learned limit. The model would call real trouble normal, because it learned
the trouble as normal.

**3.** Because in a business the model's text is rarely the final product. An existing program sends
it text, reads the reply, checks it, and decides what to do with it. The model is one layer in that
program's pipeline.
