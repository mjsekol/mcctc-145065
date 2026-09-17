# Gate 2: Adversarial Review · Week 17
## 145065 Object-Oriented Programming · Unit 9 · Week 17, Friday

**Gate 2 is the gate where AI is the opponent.** You did not write this user guide. You are reviewing
it, and you are scored on what you catch against what you miss.

**35 minutes.** Individual and silent. You may open the pictures, the requirements excerpt, and your
own panel. You may run your ShipCheck from Lab U09-01. You may not ask an AI tool whether the guide is
correct, because an AI tool is what is being reviewed.

**This week you review a document, so you use the AI Output Evaluation parameters**, not the five code
dimensions. It is the same kind of review as Week 1's brief, applied to the document an operator will
hold in their hand next Monday.

**Everything here is invented.** Riverside Fabrication and its Line 3 are a composite. Northgate
Controls and its ProView 8 handbook are invented. The pictures were rendered from the real version
1.0.0 Line 3 panel.

The files are in `gate2-w17-files/ship/`, laid out as a ship folder:

| File | What it is |
|---|---|
| `docs/USER_GUIDE.md` | **what you are reviewing**, written by an AI assistant |
| `docs/screens/*.png` | the real panel, version 1.0.0, in five states |
| `docs/REQUIREMENTS_EXCERPT.md` | nine of the panel's operator requirements, and where the limits come from |
| `docs/screen-words.txt` | every word the panel can show |
| everything else | the rest of a ship folder, so ShipCheck can run on it |

---

## What you are looking at

A student gave an AI assistant the request in Part A. The assistant wrote the guide in Part B. It is
organized, confident, friendly, and the right length. It uses every word on the screen. **It reads like
a good guide.** That is the problem.

**There are exactly five planted defects, one for each parameter:**

| Parameter | The question to ask |
|---|---|
| **Validity** | Is a claim about something real actually correct? |
| **Relevance** | Does this part answer what was asked, for the reader it was asked for? |
| **Authenticity** | Is this original work, or does it belong to somebody else? |
| **Potential Bias** | Whose needs are built in, and whose are left out? |
| **Hallucinations** | Does the thing described exist at all? |

Validity and Hallucinations are the pair you will confuse. A **validity** defect is a false claim about
something that exists. A **hallucination** describes something that does not exist.

**There is also one arguable item.** It is not a planted defect. A careful reviewer could call it a
problem, and a careful reviewer could defend it. It is scored on your reasoning.

---

## PART A: The request

> Write a user guide for the Line 3 Sensor Monitor, version 1.0.0, for an operator who is not
> technical and who uses a touch screen with work gloves on. Use the screenshots in `docs/screens`.
> The panel only monitors. Explain every word the screen can show, what to do when an alarm happens,
> and what to do when data stops. Use only what the panel, its requirements, and its limits actually
> do. Leave out anything the operator cannot do at this screen.

---

## PART B: What the AI produced

Open `gate2-w17-files/ship/docs/USER_GUIDE.md`. Read it the way an operator would, from the top, then
read it again the way a reviewer does, one sentence at a time.

**Then open every picture it links, and look at what the picture actually shows.**

---

## One command you should run

From the folder that holds your Lab U09-01 `ShipCheck` project:

```
dotnet run --project ShipCheck -- <path to>\gate2-w17-files\ship
```

Read the report. It finds one of the five defects. **Ask yourself why it finds only one.**

---

## What to submit

For each defect: **where** (the section heading), **which parameter**, **what goes wrong for an
operator if nobody catches it**, and **the fix**.

Then two more entries:

- **The arguable item.** Name it, give the strongest case that it is a problem and the strongest case
  that it is fine, then say which side you land on and why.
- **What I was unsure about.** Name something specific. A blank costs more than a wrong guess.

### How to spend 35 minutes

- **First 5:** run ShipCheck. Open all five pictures.
- **Next 10:** read Part A one sentence at a time. For each, point at the part of the guide that
  answers it.
- **Next 10:** for every claim the guide makes about the screen, find the picture or the requirement
  that proves or disproves it. For every control the guide tells the operator to press, find it in a
  picture.
- **Rest:** ask who would struggle to use this guide, and whose words these are. Write your entries.

---

## Scoring

Five defects, one point each. The arguable item, one point. The unsure-about entry, one point. **Your
instructor states before you start which defect carries a double penalty if you miss it.**

**Four of five is a strong score.**
