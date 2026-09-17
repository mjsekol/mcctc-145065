# Lecture Notes: Dataflow Diagrams and the Design Review
## 145065 Object-Oriented Programming · Unit 8 · Week 15, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W15_DataflowAndDesignReview.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-08-industrial-hmi/04-slides/MCCTC_145065_Slides_W15_DataflowAndDesignReview.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK for the
examples.

**Competencies:** 5.6.6 design inputs, outputs, and processes · 5.6.7 dataflow diagrams · 5.6.10
preparing and presenting a design review.

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`.

---

## Why this exists

A reading from the oven passes through five places before it reaches an operator's eyes: the sensor,
the Pi's service, the network, your panel's code, and the screen. Each place can fail. When one does,
somebody has to catch it and decide what the operator sees.

If you cannot point at the layer that catches a pulled cable, nobody catches it. A dataflow diagram is
where you point.

Tomorrow you present your design to people who will live with it: an operator and a maintenance lead.
They will not read your code. They will read your diagram and your screens. That is a design review,
and it happens **before** the build is finished, because that is when changes are cheap.

---

## The concept in plain language

**A dataflow diagram shows what moves where.** Each box is a layer. Each arrow is labelled with what
crosses it. The network arrow is labelled with the contract: `GET /api/readings`, JSON, about once a
second.

**Every arrow points toward the operator.** This panel only watches. An arrow back toward a machine is
a write path, and a write path on a monitoring panel is a hazard.

**A good diagram also shows where each failure is caught** and what it becomes. That table is the part
that makes a design reviewable.

**Each layer may assume only what the layer before it guaranteed.** The parser may not assume the reply
is well formed. The rules may assume the parser gave them a number or said there was none. The view may
assume the rules gave it one of four states.

**A design review** presents the requirements, the diagram, and the screens. Reviewers write their
questions before they speak. Every question gets an answer and a decision: change it, or keep it with a
reason.

---

## Worked example 1: one reading, traced through the layers

```csharp
using System.Globalization;
using System.Text.Json;

string wire = "{\"device\": \"line3-pi\", \"sequence\": 1042, \"sampled_at\": \"2027-01-11T14:03:22Z\", "
    + "\"sensors\": [{\"id\": \"oven-temp\", \"kind\": \"temperature\", \"value\": 236.0, \"unit\": \"C\", \"ok\": true}]}";
Console.WriteLine($"1 network  {wire.Length} characters of text arrive");

using JsonDocument reply = JsonDocument.Parse(wire);
JsonElement oven = reply.RootElement.GetProperty("sensors")[0];
double value = oven.GetProperty("value").GetDouble();
bool ok = oven.GetProperty("ok").GetBoolean();
Console.WriteLine(string.Create(CultureInfo.InvariantCulture, $"2 parser   ok={ok} value={value}"));

bool within = value >= 190.0 && value <= 230.0;
string state = !ok ? "MISSING" : within ? "NORMAL" : "ALARM";
Console.WriteLine($"3 rules    within={within} state={state}");

string tile = state == "ALARM" ? "ALARM HIGH" : state;
Console.WriteLine(string.Create(CultureInfo.InvariantCulture, $"4 view     {tile}  {value:0.0} C"));
```

```
1 network  176 characters of text arrive
2 parser   ok=True value=236
3 rules    within=False state=ALARM
4 view     ALARM HIGH  236.0 C
```

Four lines, four boxes. What crosses each arrow changes shape: text, then a number and a flag, then a
state, then words on a screen. Draw it that way:

```
+-----------------+   GET /api/readings, JSON text, about once a second
|  Pi service     | ------------------------------------------------+
+-----------------+                                                 |
                                                                    v
                                                          +-------------------+
                                                          |  parser           |
                                                          +---------+---------+
                                                                    |  number and ok flag, or "none"
                                                                    v
                                                          +-------------------+
                                                          |  rules            |
                                                          +---------+---------+
                                                                    |  one of four states
                                                                    v
                                                          +-------------------+
                                                          |  view             |  words, shape, color
                                                          +-------------------+
```

The example skips freshness to stay short. Your panel's rules layer also decides whether the sample is
live.

---

## Worked example 2: where each failure is caught

The same parser, fed four replies: a good one, a sensor that failed, a reply missing its number, and a
reply cut off in the middle.

```csharp
using System.Globalization;
using System.Text.Json;

string[] replies =
{
    "{\"sensors\": [{\"id\": \"oven-temp\", \"value\": 212.4, \"ok\": true}]}",
    "{\"sensors\": [{\"id\": \"oven-temp\", \"value\": null, \"ok\": false}]}",
    "{\"sensors\": [{\"id\": \"oven-temp\", \"ok\": true}]}",
    "{\"sensors\": [{\"id\": \"oven-te",
};

foreach (string reply in replies)
{
    Console.WriteLine(Read(reply));
}

static string Read(string wire)
{
    try
    {
        using JsonDocument doc = JsonDocument.Parse(wire);
        JsonElement oven = doc.RootElement.GetProperty("sensors")[0];
        if (!oven.GetProperty("ok").GetBoolean())
        {
            return "rules:  MISSING (the sensor said ok:false)";
        }

        if (!oven.TryGetProperty("value", out JsonElement v) || v.ValueKind != JsonValueKind.Number)
        {
            return "parser: MISSING (ok:true but no number)";
        }

        return string.Create(CultureInfo.InvariantCulture, $"view:   {v.GetDouble():0.0} C, live");
    }
    catch (JsonException)
    {
        return "parser: MISSING (the reply is not valid JSON)";
    }
}
```

```
view:   212.4 C, live
rules:  MISSING (the sensor said ok:false)
parser: MISSING (ok:true but no number)
parser: MISSING (the reply is not valid JSON)
```

Every failure became a named result at a named layer. None of them reached the screen as a number.

---

## Worked example 3: a whole failure table, for a different system

Your project's table is yours to write. Here is a finished one for a system you can picture: a weather
station on the school roof that feeds the temperature display in the front hallway.

| Failure | Caught in | Becomes | What the hallway display shows |
|---|---|---|---|
| The thermometer breaks | the station's own code | a reading marked "failed" | "Temperature unavailable" |
| The station loses power | the display's request, which is refused | no data | "Temperature unavailable" |
| The school network is slow | the display's timeout | no data | "Temperature unavailable" |
| The station sends garbled text | the display's parser | no data | "Temperature unavailable" |
| The station keeps sending the same reading | the display's freshness check | old data | "Last reading 41 F, 20 min ago" |
| The station's clock is wrong | the freshness check, by comparing clocks | old data, age unknown | "Last reading 41 F, time unknown" |
| The display's own program hangs | nobody inside the program | nothing | a frozen number, which is why a hang is the worst failure |

The last row is honest: some failures cannot be caught by the layer that failed. That is why your panel
awaits instead of blocking.

---

## The wrong version: a layer that trusts the one before it

```csharp
using System.Text.Json;

string wire = "{\"sensors\": [{\"id\": \"oven-temp\", \"ok\": true}]}";
using JsonDocument doc = JsonDocument.Parse(wire);
double value = doc.RootElement.GetProperty("sensors")[0].GetProperty("value").GetDouble();
Console.WriteLine(value);
```

```
Unhandled exception. System.Collections.Generic.KeyNotFoundException: The given key was not present in the dictionary.
```

`GetProperty` assumes the field is there. The reply broke the contract, and instead of becoming "no
data" at the parser, the failure became a crash. On a panel, that is a window that disappears.

**The other wrong version is drawn, not typed:** an arrow from the panel back to the Pi, labelled
something helpful like "reset the service". It breaks the rule that the panel only watches. In a design
review, the maintenance lead's first question about that arrow should be: "Who said your screen may
touch my machine?"

---

## Why the wrong versions are tempting

The contract says the field is always there, so checking feels like wasted typing. And a reset button
feels helpful. Both are true on a good day. A panel exists for the bad days.

---

## Preparing the design review

**Present, in four minutes:**

1. The brief in one sentence.
2. The three requirements that matter most, and how each is checked.
3. The dataflow diagram, and where a pulled cable is caught.
4. The screen: what the starter's snapshots got wrong, and your sketch.
5. Your oven limit and its reason.

**Expect these kinds of questions:**

| From | Sounds like |
|---|---|
| The operator | "How do I know this number is live?" "What do I press when the alarm goes off, with gloves on?" |
| The maintenance lead | "What happens when my Pi reboots?" "Does your screen ever send anything to my machine?" |

**Record every question**, your answer, and what will change. If you reject a suggestion, write why.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Dataflow diagram** | Boxes for layers, arrows for what moves between them |
| **Layer** | One part of the system with one job |
| **Contract** | What one layer promises to the next: format, fields, rate |
| **Input, output, process** | What comes in, what goes out, what happens between |
| **Write path** | Any flow that changes something outside the program |
| **Design review** | Presenting a design to its users and owners before it is finished |
| **Stakeholder** | Anyone who lives with the result |

---

## Self-check

**Question 1.** The Pi's service restarts, and its sequence number starts over at 1. Which layer notices,
and should the panel treat the reading as live?

**Question 2.** A student's diagram has an arrow from the view back to the rules layer, labelled
"operator acknowledges alarm." Is that a write path to the machine? Explain.

**Question 3.** Write one question an operator might ask at your design review that a unit test could
never answer.

---

### Answers

**1.** The rules layer, which tracks the sequence number on the panel's own clock. Any change in the
sequence is new data, including a jump back to 1, so the reading is live if its timestamp is also recent.
The failure to guard against is the opposite one: a sequence that does not change at all.

**2.** No. The acknowledgement changes what the panel remembers and shows. It never leaves the panel and
never reaches the Pi. An arrow inside the panel is fine. An arrow that crosses to the machine is the
hazard.

**3.** Any question about people and the room. For example: "Can I read that from where I stand at the
oven, with the lights on?" or "Which color means stop in this shop?"
