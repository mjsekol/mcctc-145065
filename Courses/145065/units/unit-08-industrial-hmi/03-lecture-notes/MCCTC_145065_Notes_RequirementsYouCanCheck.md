# Lecture Notes: Requirements You Can Check
## 145065 Object-Oriented Programming · Unit 8 · Week 15, Monday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W15_RequirementsYouCanCheck.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-08-industrial-hmi/04-slides/MCCTC_145065_Slides_W15_RequirementsYouCanCheck.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK for the
examples.

**Competencies:** 5.6.1 requirements specification · 5.6.2 constraints · 5.6.5 input and output
requirements · 1.3.7 the operator's workplace, at the purpose level · 2.10.2 hardware requirements ·
1.8.2 parts and resource list.

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`.

Riverside Fabrication and its Line 3 are a composite, an invented shop.

---

## Why this exists

For the next two weeks you build a panel an operator trusts with a cure oven. "Trust" is not something
you can test. "The panel never shows a number older than 5 seconds as live" is.

A requirement you cannot check is a wish. Two partners can argue about a wish forever. They can settle a
requirement in a minute, by running the check. By Friday your design review will argue with your
requirements, so write them in a form that can win an argument.

This is also exam material. Requirements and design are 5.6, about 18 percent of the WebXam.

---

## The concept in plain language

**A requirement is a sentence someone can check.** It has three parts:

1. **The need.** What the panel does, stated so it is true or false.
2. **The reason.** Who needs it, and what goes wrong without it.
3. **The check.** A test by name, a measurement with the number that passes, or a person doing a named
   action.

**A constraint is a requirement the environment writes for you.** Gloves, glare, a sensor that samples
once a second, a network cable someone can pull. You do not choose them. You design around them.

**Inputs and outputs are requirements too.** Each one is listed with where it comes from, its format,
and how often it arrives. For this panel the input is one reply from the Pi's service, about once a
second, in JSON. The output is what the operator sees.

**Hardware has requirements.** The Pi needs power, a network, and a sensor it can read. You list each
part, where it comes from, and what it costs the lab in time. That list is the parts and resource list.

---

## Worked example 1: a wish becomes a requirement

A partner writes: "The panel should look clear."

Ask the three questions. Clear to whom? An operator in safety glasses, a few steps away, under shop
lights. Why? A state misread from a distance is a missed alarm. How would anyone check it? With a
number.

| ID | Requirement | Why | Checked by |
|---|---|---|---|
| REQ-11 | State text has a contrast ratio of at least 7:1 with its background | Operators read the panel from a distance under glare | The contrast formula in worked example 3, run on every state color pair |

"Should look clear" had no check. REQ-11 has one, and it can fail.

Two more, from the same draft:

| Wish | Requirement | Checked by |
|---|---|---|
| "It should be fast" | The panel shows NO CONNECTION within 3 s of the service stopping | A stopwatch during the disconnect demo, and the recorded time |
| "Buttons should be big" | Every button is at least 72 px tall at the 1280 by 800 design size | A snapshot of the window, measured |

---

## Worked example 2: a requirement checked by arithmetic

REQ-02 says a value whose sample is more than 5 seconds old is never shown as live. The check is
subtraction:

```csharp
using System.Globalization;

DateTimeOffset now = DateTimeOffset.Parse("2027-01-11T14:03:28Z", CultureInfo.InvariantCulture);
TimeSpan staleAfter = TimeSpan.FromSeconds(5);

foreach (string stamp in new[] { "2027-01-11T14:03:27Z", "2027-01-11T14:03:23Z", "2027-01-11T14:03:22Z" })
{
    DateTimeOffset sampled = DateTimeOffset.Parse(stamp, CultureInfo.InvariantCulture);
    TimeSpan age = now - sampled;
    string verdict = age > staleAfter ? "STALE, may not be shown as live" : "fresh";
    Console.WriteLine(string.Create(CultureInfo.InvariantCulture,
        $"sampled {sampled:HH:mm:ss}  age {age.TotalSeconds:0.0} s  {verdict}"));
}
```

```
sampled 14:03:27  age 1.0 s  fresh
sampled 14:03:23  age 5.0 s  fresh
sampled 14:03:22  age 6.0 s  STALE, may not be shown as live
```

Look at the middle line. Exactly 5.0 seconds is fresh, because the requirement says **more than** 5. A
requirement that says "about 5 seconds" cannot decide that row. Yours has to.

---

## Worked example 3: a requirement checked by a formula

REQ-11 uses the contrast formula from the web accessibility guidelines (WCAG). Each color gets a
relative luminance from 0 (black) to 1 (white). The ratio is the lighter one plus 0.05, divided by the
darker one plus 0.05.

```csharp
using System.Globalization;

foreach ((string what, string text, string back) in new[]
{
    ("alarm tile, white on red", "#FFFFFF", "#B0001D"),
    ("stale tile, ink on yellow", "#111111", "#FFD966"),
    ("grey caption on white", "#8A8A8A", "#FFFFFF"),
})
{
    double ratio = Ratio(text, back);
    string verdict = ratio >= 7.0 ? "meets REQ-11" : "fails REQ-11";
    Console.WriteLine(string.Create(CultureInfo.InvariantCulture, $"{what,-28} {ratio:0.0}:1  {verdict}"));
}

static double Ratio(string text, string background)
{
    double a = Luminance(text);
    double b = Luminance(background);
    return (Math.Max(a, b) + 0.05) / (Math.Min(a, b) + 0.05);
}

static double Luminance(string hex)
{
    double Channel(int start)
    {
        double c = Convert.ToInt32(hex.Substring(start, 2), 16) / 255.0;
        return c <= 0.03928 ? c / 12.92 : Math.Pow((c + 0.055) / 1.055, 2.4);
    }

    return (0.2126 * Channel(1)) + (0.7152 * Channel(3)) + (0.0722 * Channel(5));
}
```

```
alarm tile, white on red     7.3:1  meets REQ-11
stale tile, ink on yellow    13.8:1  meets REQ-11
grey caption on white        3.5:1  fails REQ-11
```

The grey caption looks fine on your monitor at arm's length. The formula says it fails. That is why a
requirement names a check instead of an opinion.

---

## Worked example 4: a requirement the program enforces, and one it cannot

The project's loader refuses a limit with no reason. Its rule is a length: at least 20 characters. The
same rule, by itself:

```csharp
foreach (string reason in new[]
{
    "",
    "seems right",
    "seems right to all of us",
    "Above 230 C the coating discolors, by the process sheet.",
})
{
    string trimmed = reason.Trim();
    string verdict = trimmed.Length < 20 ? "refused" : "accepted";
    Console.WriteLine($"{trimmed.Length,3} characters  {verdict,-8}  \"{trimmed}\"");
}
```

```
  0 characters  refused   ""
 11 characters  refused   "seems right"
 24 characters  accepted  "seems right to all of us"
 56 characters  accepted  "Above 230 C the coating discolors, by the process sheet."
```

Row three is the lesson. A program can count characters. It cannot tell whether a reason is true. So
the requirement "every limit has a reason" has two checks: the loader, and a person reading the reason
at the design review. Write both in the "Checked by" column.

---

## The wrong version: a requirement with no check

```
REQ-04  The panel should handle errors well.
```

Nothing fails. There is no error message to show you, and that is the problem. Every panel "handles
errors well" until someone pulls the cable.

When the check is missing, the project's code finds it for you. Load a thresholds file whose oven reason
is `seems right`, and the lab program prints:

```
thresholds.json was refused: Sensor "oven-temp" has no reason for its limits. Write why these numbers, in a sentence an operator can read.
```

That refusal is a requirement with a check, written into the loader. Your requirements document needs
the same thing for every row.

---

## Why the wrong version is tempting

Vague requirements feel safe. Nobody can say you missed one. They also mean nobody can say you met one,
including your client at the demo. The fix is the third column: if you cannot fill it, rewrite the row.

---

## Constraints for this panel

| Constraint | Where it comes from | What it forces |
|---|---|---|
| Operators wear gloves | The shop's safety rules | Large buttons, far apart |
| Glare and distance | Shop lighting and the screen's position | High contrast, big state words |
| The sensor samples once a second | The Pi's code | A stale limit of several seconds, not one |
| A cable can be pulled | The shop floor | A NO CONNECTION state, and alarms that survive it |
| The panel only watches | The course and the client | No command ever goes to the Pi |

---

## The operator's workplace (1.3.7), at the purpose level

Laws shape who stands at a machine and how a workplace must accommodate them. Two kinds matter to a
panel designer, and you do not need to be a lawyer to respect either.

- **Minor labor laws** limit which tasks and machines workers under 18 may be assigned, and when they
  may work. Their purpose is to keep young workers away from the most dangerous jobs. Federal rules and
  Ohio's rules both apply. Official sources: the U.S. Department of Labor's youth employment pages and
  the Ohio Department of Commerce's minor labor law pages **[VERIFY both addresses in the resources
  file]**.
- **Accessibility laws** require reasonable accommodation for workers with disabilities. Their purpose is
  that a qualified person can do the job. Official source: the Americans with Disabilities Act site
  **[VERIFY]**.

**What this means for your panel.** It never decides who may operate a machine. It is readable without
relying on color alone, and its targets are large. **This is not legal advice.** Questions about a real
workplace go to the employer and the official sources.

---

## Hardware requirements and the parts list (2.10.2, 1.8.2)

| Part | Requirement | Where it comes from |
|---|---|---|
| Raspberry Pi | runs Python 3 and the sensor service | the lab kit [VERIFY the model] |
| Power supply | the one made for that Pi | the lab kit |
| Network | a wired connection on the lab's isolated network | the lab [VERIFY the address] |
| Temperature probe | a DS18B20 on the Pi's one-wire pins | the lab kit [VERIFY] |
| Simulator | runs on your PC with no hardware | `05-labs/sensor-service/` |

**Safety first, every time.** Before anyone touches the Pi, the safety brief is read aloud: ESD
precautions, power off before wiring, no mains voltage ever, and the signed Lab Acceptable Use and Safety
Agreement on file. The simulator proves every requirement for grading.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Requirement** | A statement of need that someone can check |
| **Constraint** | A requirement the environment imposes |
| **Acceptance check** | The test, measurement, or action that proves a requirement is met |
| **Input requirement** | What comes in, from where, in what format, how often |
| **Output requirement** | What the user sees or receives, and how it must look |
| **Contrast ratio** | Lighter luminance plus 0.05, over darker plus 0.05. From 1:1 to 21:1 |
| **Parts and resource list** | Every part, where it comes from, and what it costs |

---

## Self-check

**Question 1.** Rewrite "the alarm should be noticeable" as a requirement with all three parts.

**Question 2.** A sample was taken at 14:03:23 and the panel's clock reads 14:03:28.1. Is it stale under
REQ-02? Show the arithmetic.

**Question 3.** A team's reason for its oven limit is "because our teacher said so, and it works". Does
the loader accept it? Should the design review?

---

### Answers

**1.** One good answer: "An oven alarm shows the word ALARM, a warning shape, and the alarm color, with
a banner that stays up until acknowledged. Why: an operator glancing from across the line must see it,
including one who cannot tell red from green. Checked by: the alarm snapshot, read at arm's length, and
the REQ04 test." Any answer with a checkable statement, a reason, and a named check is correct.

**2.** Stale. The age is 14:03:28.1 minus 14:03:23, which is 5.1 seconds. That is more than 5, so the
value may not be shown as live.

**3.** The loader accepts it: it is more than 20 characters. The review should not. It names no problem
the limit prevents and no evidence. A person has to catch that, which is why the requirement lists a
review as its second check.
