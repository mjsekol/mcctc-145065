# Lecture Notes: Value Claims and Their Sources
## 145065 Object-Oriented Programming · Unit 0 · Week 1, Thursday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W01_ValueClaimsAndSources.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-00-onboarding-emerging-tech/04-slides/MCCTC_145065_Slides_W01_ValueClaimsAndSources.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need Python.

**Competencies:** 2.4.3 research the value of emerging technologies on the marketplace. 1.2.1
extract relevant, valid information and cite sources. 1.2.12 use technical writing skills to create
reports.

---

## Why this exists

Your brief has to argue that a technology is worth money to someone. That is where most writing about
emerging technology goes wrong. It is full of precise percentages that sound researched and cannot be
traced to anybody who measured anything.

A decision-maker who spends money on a number you cannot trace is trusting you, not the number. This
lesson is how you earn that trust honestly.

---

## The concept in plain language

**Value is value to someone.** "IoT is valuable" means nothing. "Sensors on Line 3 would pay for
themselves within a year if they prevent ten hours of downtime" means something, and somebody can
check it.

**A claim is a claim with an owner.** Before a number goes in your brief, answer two questions:

1. Who measured this, and how?
2. Can I open the source and see it?

If you cannot answer both, the number does not go in. You have three honest options instead:

- find a source you can open,
- state the claim as belonging to whoever made it, labelled, for example "the vendor states",
- or argue the value with your buyer's own numbers, **labelled as assumptions**.

### Kinds of sources, and what each one gains

| Type | Example | What the writer gains | How much to trust it |
|---|---|---|---|
| government | a NIST program page | nothing from your purchase | high for definitions and guidance |
| standards | a standards body's published standard | nothing from your purchase | high for definitions, often paid to read in full |
| academic | a peer-reviewed study | reputation | high, if you can read the method |
| industry-group | a trade association | its members' interests | medium, check who the members are |
| news | an article summarizing a report | your attention | only as good as the report it summarizes. Find the report. |
| vendor | a company selling the product | your purchase | a claim, not evidence. Label it. |
| documentation | the official docs for a tool | adoption of the tool | high for how the tool works |

**A chatbot answer is never a source.** It can be a lead. If it names a report, go and open that
report. If you cannot find it, the report may not exist. Models produce citations that look real and
are not.

### Citing a source in this course

Number your sources and cite them in the text with `[1]`, `[2]`. The source list uses one line each:

```
1. National Institute of Standards and Technology. "Manufacturing Extension Partnership (MEP)." https://www.nist.gov/mep. Type: government. Opened in Week 1. Supports: a federal program supporting small and medium manufacturers.
```

"Opened in Week 1" is the point. You are saying you looked.

### Technical writing rules for the brief

- Lead with the recommendation. A busy reader may read only the summary.
- One idea per paragraph.
- Name the buyer in every value claim.
- Put numbers in a table when there are more than two.
- Write "assumption" next to every number that is yours.

---

## Worked example 1: value to one buyer, with every input labelled

```python
# payback.py
# How long before a sensor kit on Line 3 pays for itself?
# Riverside Fabrication is a composite. Every input below is an ASSUMPTION
# until you replace it with a number you can point at.

kit_cost = 1800.00                # ASSUMPTION: dollars, sensors plus the Pi
install_hours = 16                # ASSUMPTION: hours of maintenance labor
labor_rate = 38.00                # ASSUMPTION: dollars per hour
downtime_hours_avoided = 10       # ASSUMPTION: per year, from the shop's own log
cost_per_downtime_hour = 450.00   # ASSUMPTION: dollars lost per hour the line is down

upfront = kit_cost + install_hours * labor_rate
annual_savings = downtime_hours_avoided * cost_per_downtime_hour
payback_months = upfront / annual_savings * 12

print(f"Upfront cost:    ${upfront:,.2f}")
print(f"Savings a year:  ${annual_savings:,.2f}")
print(f"Payback:         {payback_months:.1f} months")
```

Output:

```
Upfront cost:    $2,408.00
Savings a year:  $4,500.00
Payback:         6.4 months
```

Every number is invented for a composite shop, and the file says so. The result is not "sensors pay
back in 6.4 months." The result is "for this buyer, under these five assumptions, the payback is 6.4
months," and every assumption can be challenged by name.

---

## Worked example 2: which assumption matters most

```python
upfront = 1800.00 + 16 * 38.00          # ASSUMPTIONS, as in payback.py
cost_per_downtime_hour = 450.00         # ASSUMPTION

for hours_avoided in [4, 10, 20]:
    annual_savings = hours_avoided * cost_per_downtime_hour
    months = upfront / annual_savings * 12
    print(f"{hours_avoided:>2} hours avoided a year: payback {months:.1f} months")
```

Output:

```
 4 hours avoided a year: payback 16.1 months
10 hours avoided a year: payback 6.4 months
20 hours avoided a year: payback 3.2 months
```

This is a **sensitivity check**. It shows that the answer depends heavily on one input. That tells
the buyer what to measure first: last year's downtime. A brief that says so is more useful than one
that states a single confident number.

---

## Worked example 3: finding figures with no owner

```python
import re

sentences = [
    "Sensors can warn before a failure [1].",
    "Monitoring cuts downtime by 38 percent.",
    "The kit costs $1,800 (assumption).",
    "Line 3 has three machines.",
]
figure = re.compile(r"\d[\d,.]*\s*(%|percent)|\$\s?\d")
for sentence in sentences:
    has_figure = figure.search(sentence) is not None
    has_owner = "[" in sentence or "(assumption)" in sentence
    if has_figure and not has_owner:
        print("NO OWNER:", sentence)
```

Output:

```
NO OWNER: Monitoring cuts downtime by 38 percent.
```

The second sentence was written for this example and has no source. `brief_check.py` in the project
folder runs the same idea over your whole brief. It can find figures with no owner. **It cannot tell
whether a cited source says what you claim.** Only opening the source can.

---

## The wrong version, and what it produces

Delete `* 12` from the payback line in example 1:

```python
payback_months = upfront / annual_savings
```

Output:

```
Upfront cost:    $2,408.00
Savings a year:  $4,500.00
Payback:         0.5 months
```

No error. A sensor kit that pays for itself in two weeks. `upfront / annual_savings` is measured in
years, and the label says months. The number is off by a factor of twelve, and it looks like good
news.

---

## Why the wrong version is tempting

A fast, confident number feels like a finished answer, and a good-news number is the one nobody
double-checks. The same is true of a precise percentage in an article. It feels like research because
it is precise.

The habits that prevent both: write the unit next to every calculated value, check the result
against common sense ("two weeks, really?"), and for every figure in your writing, point at its owner.

---

## Vocabulary

| Term | What it means |
|---|---|
| **Market value** | what a technology is worth to buyers, in money saved or earned |
| **Payback period** | how long until the savings equal the upfront cost |
| **Assumption** | a number you estimated yourself, labelled as yours |
| **Sensitivity check** | changing one input to see how much the answer moves |
| **Primary source** | the organization that did the measuring or wrote the standard |
| **Citation** | a pointer from a claim to the source that supports it |
| **Hallucinated citation** | a source an AI tool describes that does not exist |

---

## Self-check

**Question 1.** A news article says "a recent report found monitoring cuts downtime by a third." What
do you do before using that claim?

**Question 2.** Your payback prints `0.5 months`. Name two checks that would catch the error.

**Question 3.** Why is a vendor's case study weaker evidence than a government program page, even
when both are accurate?

---

### Answers

**1.** Find and open the report itself. Record who published it and whether you can see how the
figure was measured. If you cannot find or open it, leave the figure out or state it as the article's
claim, labelled, and do not build your value argument on it.

**2.** Check the units: `upfront / annual_savings` is in years, so it needs `* 12` for months. Check
common sense: a kit paying for itself in two weeks is implausible. Recomputing by hand
(2,408 divided by 4,500 is about half a year) also catches it.

**3.** The vendor gains from your purchase, so it chooses which results to publish and how to frame
them. A government program page has no stake in your purchase. Accuracy of one example does not show
the example is typical.
