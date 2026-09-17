# Gate 2: Adversarial Review · Week 1
## 145065 Object-Oriented Programming · Unit 0 · Week 1, Friday

**Gate 2 is the gate where AI is the opponent.** You did not write this brief. You are reviewing it,
and you are scored on what you catch against what you miss.

**35 minutes.** Individual and silent. You may and should run the code file. You may use a browser to
check sources. You may not ask a model whether the brief is correct, because a model is what is being
reviewed.

**This week you review a document, not a program**, so you use the **AI Output Evaluation**
parameters instead of the five code dimensions. The brief includes one code file, and you run it as
evidence. From Week 2 on, Gate 2 reviews object-oriented code.

**Everything in this exercise is invented.** Riverside Fabrication is a composite shop used all
semester. Hollowbrook Sensor Works is an invented vendor. Any report, figure, or quotation in the
brief was written for this exercise.

The code file is `gate2-w01-files/oven_alert.py`. Copy it and run it:

```
python oven_alert.py
```

---

## What you are looking at

A student gave an AI assistant the request in Part A and got back the brief in Part B. It is well
organized, confident, and the right length. **It reads like a good brief.** That is the problem.

**There are exactly five planted defects, one for each parameter:**

| Parameter | The question to ask |
|---|---|
| **Validity** | Is a claim about something real actually correct? |
| **Relevance** | Does this part answer what was asked? |
| **Authenticity** | Is this original work, or does it belong to somebody else? |
| **Potential Bias** | Whose view is built in, and whose is missing? |
| **Hallucinations** | Does the thing described exist at all? |

Validity and Hallucinations are the pair you will confuse. A **validity** defect is a false claim
about something that exists. A **hallucination** describes something that does not exist.

**There is also one arguable item** that is not a planted defect. A reasonable reviewer could call it
a problem, and a reasonable reviewer could defend it. It is scored separately, on your reasoning.

---

## PART A: The request

> Write a one-page emerging technology brief for the Line 3 supervisor at Riverside Fabrication, a
> small metal fabrication shop. The brief must:
>
> 1. Explain what IoT condition monitoring is.
> 2. Describe its architecture in layers, from the sensor to the screen.
> 3. Explain how the readings would get into the maintenance log spreadsheet the supervisor already
>    uses. The log records temperatures in Fahrenheit.
> 4. Argue its value to this shop, with sources the supervisor can check.
> 5. Name the costs and risks.
> 6. Include a short Python example that flags the paint cure oven when it goes over the shop's
>    425 F limit, using the Line 3 payload format. The payload reports the oven in Celsius.

---

## PART B: What the AI produced

> # IoT Condition Monitoring for Riverside Fabrication, Line 3
>
> ## What it is
>
> Internet of Things condition monitoring places small networked sensors on equipment so that its
> health can be tracked continuously. Instead of waiting for a machine to fail, the shop sees
> warning signs in real time and acts before a breakdown stops the line.
>
> ## Architecture
>
> The system has four layers. Sensors on the paint cure oven, Press 2, and the coolant tank measure
> temperature, vibration, and level. A Raspberry Pi gateway reads the sensors every five seconds and
> packages the readings as JSON. The gateway converts every reading to Fahrenheit before it is sent,
> so downstream software never has to handle units. The shop network carries the JSON to a small
> server, and the server feeds the dashboard.
>
> ## How it connects to the systems you already have
>
> Connecting the sensors is straightforward. In the same way a smart thermostat sends alerts to a
> homeowner's phone, the Line 3 sensors can push notifications to a mobile app. Supervisors can check
> machine status from anywhere, and a smart speaker in the office can announce alerts out loud. Most
> modern sensor kits include a companion app with charts and push notifications ready to use.
>
> ## Value to Riverside Fabrication
>
> The case for IoT in small shops is well established. According to the Buckeye Shop Floor
> Connectivity Index (2024), 71 percent of Ohio fabrication shops with fewer than 50 employees already
> use connected sensors, and those shops cut unplanned downtime by 38 percent (Table 3). A shop that
> matched those results on Line 3 would recover most of its lost production within the first year.
>
> A large language model running on the shop's own computer could also read the week's alerts and
> write the supervisor a short plain-language summary every Friday.
>
> ## Costs and risks
>
> Sensor kits are affordable, and every shop that has adopted IoT reports lower costs. The only real
> risk is waiting while competitors move ahead.
>
> ## Integration example
>
> The adapted example below, `oven_alert.py`, is ready to drop into the shop's system. It reads the
> latest payload and alerts when the oven is over the 425 F limit.
>
> ## Recommendation
>
> Riverside Fabrication should equip all of Line 3 this quarter.

The example file, as delivered:

```python
# oven_alert.py
# Copyright (c) 2023 Hollowbrook Sensor Works. All rights reserved.
# Licensed only for use with Hollowbrook sensor hardware. Do not redistribute.
#
# Adapted integration example: reads the latest Line 3 payload and alerts
# when the paint cure oven goes over the shop's temperature limit.

import json

# The shop's written limit for the paint cure oven, in Fahrenheit.
OVEN_LIMIT_F = 425.0

# The latest payload from the Line 3 gateway.
LATEST_PAYLOAD = """
{
  "device": "line3-pi",
  "sequence": 1043,
  "sampled_at": "2027-01-11T14:03:27Z",
  "sensors": [
    {"id": "oven-temp", "kind": "temperature", "value": 221.5, "unit": "C", "ok": true},
    {"id": "press-vibration", "kind": "vibration", "value": 7.4, "unit": "mm/s", "ok": true},
    {"id": "coolant-level", "kind": "level", "value": null, "unit": "%", "ok": false}
  ]
}
"""


def oven_status(payload_text):
    """Return a one-line status for the paint cure oven."""
    payload = json.loads(payload_text)
    for sensor in payload["sensors"]:
        if sensor["id"] != "oven-temp":
            continue
        if not sensor["ok"]:
            return "Oven reading missing. Check the sensor."
        # The gateway converts every reading to Fahrenheit before sending,
        # so the value can be compared with the limit directly.
        if sensor["value"] > OVEN_LIMIT_F:
            return f"ALERT: paint cure oven at {sensor['value']} F, over the {OVEN_LIMIT_F} F limit"
        return f"Oven normal at {sensor['value']} F"
    return "Oven sensor not found in payload."


if __name__ == "__main__":
    print(oven_status(LATEST_PAYLOAD))
```

A real run:

```
Oven normal at 221.5 F
```

**Read that output against request item 6 before you read anything else.**

---

## What to submit

For each defect: **where** (the section name, or the file and line), **which parameter**, **what goes
wrong for the supervisor if nobody catches it**, and **the fix**.

Then two more entries:

- **The arguable item.** Name it, give the strongest case that it is a problem, and the strongest case
  that it is fine. Then say which side you land on and why.
- **What I was unsure about.** Name something specific. A blank costs more than a wrong guess.

### How to spend 35 minutes

- **First 5:** run `oven_alert.py`. Work out by hand what 221.5 C is in Fahrenheit.
- **Next 10:** read Part A one item at a time, and point at the part of the brief that answers it.
- **Next 10:** for every source, figure, and file in the brief, ask who made it and whether you could
  open it.
- **Rest:** ask whose view the brief is written from, and write your entries.

---

## Scoring

Five defects, one point each. The arguable item, one point. The unsure-about entry, one point. **Your
instructor states the Hallucinations weighting before you start.**

**Four of five is a strong score.**
