# Help Written From the Screen
---
## Slide 1: Monday, someone you have never met
- They have never seen your panel
- They are holding your guide
- A tile turns red
- You are not allowed to help
Speaker notes: Next Monday, someone who has never seen your panel stands in front of it with your guide in their hand. A tile turns red. You are standing right there, and you are not allowed to say a word. Everything they do next depends on what you write today.
Image: A person in work gloves holding a printed page, looking up at a red tile on a panel.
---
## Slide 2: You know the panel from the inside
- You built parser, rules, view model, window
- The operator meets a screen and a situation
- A guide in build order is written for you
Speaker notes: You built this panel from the inside out. The operator meets it from the outside in. If your guide follows the order you built things, it answers questions only a programmer asks. Today we write from the screen.
Image: An inside-out diagram: code layers on one side, a single screen on the other.
---
## Slide 3: Three rules for operator help
- One section per situation the operator sees
- Every screen word, exactly as the screen shows it
- Every sentence checkable against the running panel
- No programmer words, ever
Speaker notes: One section per situation, named by what the operator sees. Every word the screen can show appears in the guide, in capitals, exactly. Every sentence is a claim you can check against the running panel, with a picture of the real screen. And no word an operator would need to be a programmer to read.
Image: A guide page with a picture of a red tile and the heading When a reading alarms.
---
## Slide 4: Which screen words does this guide teach?
```csharp
foreach (string word in screenWords)
{
    bool found = guide.Contains(word, StringComparison.Ordinal);
    Console.WriteLine($"{(found ? "found  " : "MISSING")}  {word}");
}
```
Speaker notes: This loop takes the list of screen words and checks the guide for each one. Ordinal means capitals count. On the example guide it printed found NORMAL, MISSING STALE, because the guide said stale in lowercase, and MISSING for ALARM ENDED, NOT ACKNOWLEDGED, because a line break split the phrase.
Image: None. This slide is code.
---
## Slide 5: Whole words, not pieces of words
```csharp
Regex whole = new(@"(?<![A-Za-z0-9_])" + Regex.Escape(term)
    + @"(?![A-Za-z0-9_])", RegexOptions.IgnoreCase);
if (whole.IsMatch(sentence))
{
    found.Add(term);
}
```
Speaker notes: For jargon you want whole words. Rapid contains api. Threads contains thread. The lookarounds on each side say no letter, digit, or underscore may touch the term. On three test sentences this printed clean, then JSON and null, then HTTP. Case is ignored on purpose, because lowercase http is equally unreadable.
Image: None. This slide is code.
---
## Slide 6: The wrong way: a guide in build order
- Requests readings once a second
- Parser rejects a malformed timestamp
- Stale detected by sampled_at or sequence
- True, and useless at the panel
Speaker notes: Here is a guide written the way the panel was built. Every sentence is true. Not one of them tells an operator what the screen shows or what to do. The operator reads it, looks back at the red tile, and is exactly as stuck as before.
Image: A paragraph of dense text crossed out beside a red tile.
---
## Slide 7: What the check said about a careful guide
```
FAIL  screen words in guide  missing from the guide: LINE 3 SENSOR MONITOR, EVENTS
```
Speaker notes: This is a real result. The course's own draft guide is well organized, and it still wrote Line 3 Sensor Monitor in mixed case and called the event list a list of recent events. The screen says LINE 3 SENSOR MONITOR and EVENTS. A person matching paper to screen trips on that. The check did not.
Image: None. This slide is code.
---
## Slide 8: Why build order is tempting
- The build order feels like the natural order
- True sentences feel like good sentences
- You stop seeing the screen words as words
Speaker notes: You know the panel from the inside, so that order feels natural. Precise, true sentences feel like quality. And you have read your own screen so many times that Events and EVENTS look the same to you. They do not look the same to someone new.
Image: A developer looking at code while an operator looks at a screen, back to back.
---
## Slide 9: What the checks cannot see
- The right words in a false sentence
- A button the guide invents
- Only a person at the panel finds those
Speaker notes: A guide can use every screen word, contain no jargon, link every picture, and still say something false. It can describe a button that is not there. No string check finds that. Reading the guide aloud beside the running panel finds it. Watching a stranger use it finds it for certain, and that is Monday.
Image: A checklist with all boxes ticked, next to a panel showing something different from the page.
---
## Slide 10: What you are about to build
- Build 1: ShipCheck Part 2, the three guide checks
- Build 2: your screen-words file and your user guide
- Pictures of your real panel, every state
- A partner reads your guide beside your panel
Speaker notes: In Build 1 you finish ShipCheck with the three guide checks from today. In Build 2 you list every word your panel can show, then write your guide by situation, with a picture of each state. Before the commit, a partner reads your guide aloud while your panel runs, and stops at any sentence the screen does not back up.
Image: A guide page next to a panel screenshot, with matching words highlighted in launch blue.
