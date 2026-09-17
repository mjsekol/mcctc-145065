# Lecture Notes: Help Written From the Screen
## 145065 Object-Oriented Programming · Unit 9 · Week 17, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W17_HelpWrittenFromTheScreen.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-09-ship-document-demonstrate/04-slides/MCCTC_145065_Slides_W17_HelpWrittenFromTheScreen.md --export pptx`

If you missed class, you can learn this concept from this file alone.

**Competencies:** 5.6.8, create documentation such as user help. 1.2.5, communicate information for an
intended audience and purpose. 5.2.4, string operations.

---

## Why this exists

Next Monday, a person who has never seen your panel will stand in front of it with your guide in their
hand. You will not be allowed to help. Whatever they do next depends on what the guide says.

In 145060 you wrote user help for a web app, and you learned that every document has one reader. This
reader is harder. They are not technical. They may be wearing gloves. A machine is running behind them.
And the thing in front of them is not asking them to explore; it is telling them something is wrong.

You built the panel from the inside: parser, state rules, view model, window. **The operator meets it
from the outside: a screen, and a situation.** A guide written in the order you built things is written
for you.

---

## The concept in plain language

**User help for an operator is organized by what the operator sees, and it teaches every word on the
screen exactly as the screen shows it.**

Three rules follow from that.

| Rule | Why |
|---|---|
| **One section per situation**, named by what the operator sees: "When a reading alarms", "When the panel loses data" | the operator arrives with a screen in front of them, not a question about code |
| **Every screen word appears in the guide, in capitals, exactly as shown** | the guide is where the operator learns what STALE means before they meet it at 2 a.m. |
| **Every sentence is a claim you can check against the running panel**, with a picture of the real screen | a guide that describes a button the panel does not have is worse than no guide |

A fourth rule you already know: **no programmer words.** An operator should never meet "JSON", "null",
or "PollingLoop".

### The list of screen words

Keep a plain text file, `docs/screen-words.txt`, with one line for every word or phrase the panel can
show. Read your XAML and your view model to build it. For the Line 3 reference panel it has 18 lines,
from LINE 3 SENSOR MONITOR to EVENTS.

That file is the bridge between your code and your guide. When a word changes in code, it changes in
that file, and a check tells you the guide is now out of date.

---

## Worked example 1: which screen words does this guide teach?

```csharp
string[] screenWords = { "NORMAL", "STALE", "NO DATA", "ALARM ENDED, NOT ACKNOWLEDGED" };
string guide = """
    A NORMAL tile is fine. A stale tile is old. NO DATA means no reading.
    If the reading returns first, the banner reads ALARM ENDED, NOT
    ACKNOWLEDGED until someone acknowledges it.
    """;

foreach (string word in screenWords)
{
    bool found = guide.Contains(word, StringComparison.Ordinal);
    Console.WriteLine($"{(found ? "found  " : "MISSING")}  {word}");
}
```

Output:

```
found    NORMAL
MISSING  STALE
found    NO DATA
MISSING  ALARM ENDED, NOT ACKNOWLEDGED
```

Two real problems, found by one comparison each.

- **"stale" is not STALE.** The operator will see the capitals. `StringComparison.Ordinal` refuses to
  pretend they are the same.
- **The long phrase was split across two lines.** A person reading the guide would not notice. The
  check does. So would a search box.

---

## Worked example 2: whole words, not pieces of words

```csharp
using System.Text.RegularExpressions;

string[] jargon = { "API", "thread", "JSON", "null", "HTTP" };
string[] sentences =
{
    "Rapid changes in the threads of a bolt are not a sensor problem.",
    "If the JSON is null, restart the panel.",
    "Ask IT to check the http address.",
};

foreach (string sentence in sentences)
{
    List<string> found = new();
    foreach (string term in jargon)
    {
        // Whole word only: no letter, digit, or underscore on either side.
        Regex whole = new(@"(?<![A-Za-z0-9_])" + Regex.Escape(term) + @"(?![A-Za-z0-9_])", RegexOptions.IgnoreCase);
        if (whole.IsMatch(sentence))
        {
            found.Add(term);
        }
    }

    Console.WriteLine(found.Count == 0 ? "clean" : "jargon: " + string.Join(", ", found));
}
```

Output:

```
clean
jargon: JSON, null
jargon: HTTP
```

"Rapid" contains `api`, and "threads" contains `thread`. With `Contains`, the first sentence would be
flagged for words it does not use. The lookarounds, `(?<!...)` and `(?!...)`, require that no letter,
digit, or underscore touches the term. Jargon ignores case on purpose: "http" is as unreadable as
"HTTP".

---

## Worked example 3: every picture link points at a real file

```csharp
using System.Text.RegularExpressions;

string guide = """
    Picture: [Every sensor normal](screens/panel-normal.png)
    See the [limits table](#the-limits) below.
    ![Oven in alarm](screens/panel-alarm.PNG)
    """;

Regex pictureLink = new(@"\]\(([^)\s]+?\.png)\)", RegexOptions.IgnoreCase);
foreach (Match match in pictureLink.Matches(guide))
{
    Console.WriteLine("docs/" + match.Groups[1].Value);
}
```

Output:

```
docs/screens/panel-normal.png
docs/screens/panel-alarm.PNG
```

The link to `#the-limits` is not a picture, so it is skipped. Each path printed is where a picture must
exist, relative to the guide's own folder. In Lab U09-01 you turn these three examples into ShipCheck's
Part 2.

---

## The wrong version, and what it produces

Here is a guide written in the order the panel was built:

> **How the panel works.** The panel requests readings from the sensor service once a second. If the
> request times out, every sensor is marked missing. The parser rejects a reply with a malformed
> timestamp. Stale data is detected by sampled_at or sequence. Alarms are latched until acknowledged
> and back within limits.

Every sentence is true. An operator cannot use any of it. It never says what the screen shows, and it
never says what to do.

The same mistake hides in careful guides. The course's own Line 3 draft guide is organized well, and
ShipCheck still found this when it was checked against the reference panel's word list:

```
FAIL  screen words in guide  missing from the guide: LINE 3 SENSOR MONITOR, EVENTS
```

The draft writes "Line 3 Sensor Monitor" and "a list of recent events". The screen says
LINE 3 SENSOR MONITOR and EVENTS. A small thing, and exactly the kind an operator trips on.

And one more, from the build of this unit's Gate 2 key: a corrected guide failed the same check because
a line break fell in the middle of ALARM ENDED, NOT ACKNOWLEDGED. The tool is not only for AI output.

---

## Why the wrong version is tempting

**You know the panel from the inside.** The order you built it in feels like the natural order to
explain it in.

**True sentences feel like good sentences.** "Stale data is detected by sampled_at or sequence" is
correct, precise, and useless to the person at the panel.

**You read the screen words so often they stop looking like words.** "Events" and EVENTS look the same
to you. They do not look the same to a person matching a word on paper to a word on a screen.

---

## Vocabulary

| Term | What it means |
|---|---|
| **User help** | documentation for the person who uses the software, in their words |
| **Situation-based guide** | a guide organized by what the reader sees and needs to do, not by how the software is built |
| **Screen word** | a word or phrase the software shows, which the guide must use exactly |
| **Jargon** | a word the reader would have to be a programmer to understand |
| **Ordinal comparison** | comparing text character by character, with capitals counted as different |
| **Whole-word match** | a match that does not count a term found inside a longer word |
| **Lookaround** | a regular expression part that checks what is beside a match without including it |

---

## Self-check

**Question 1.** Your guide says "If the screen shows no connection, call maintenance." The panel's badge
says NO CONNECTION. Will an ordinal check find the screen word? What should the sentence say?

**Question 2.** A classmate's jargon check reports `an operator would have to read: API` for a guide
that never mentions an API. Name the most likely cause.

**Question 3.** Your guide passes every check: all screen words, no jargon, every picture present. Name
one kind of mistake it can still contain, and how you would find it.

---

### Answers

**1.** No. "no connection" in lowercase is not NO CONNECTION. The sentence should use the screen's words
exactly: "If the badge shows NO CONNECTION for more than a minute, call maintenance."

**2.** The check matches pieces of words, so a word like "rapid" or "capital" counts as "API". It needs a
whole-word match.

**3.** A sentence that uses the right words and says something false, such as "a missing reading keeps
its last number." Find it by reading the guide aloud next to the running panel and checking every
sentence against what the screen does, or by watching a person use the panel with only the guide.
