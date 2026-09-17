# Stale Is Not Missing
---
## Slide 1: The calmest number on the screen
- Oven: 212.4 C, NORMAL
- Steady for the last minute
- The Pi stopped measuring a minute ago
- The number never knew
Speaker notes: The oven tile reads two hundred twelve point four, normal. It has been perfectly steady for a minute. That is because the Pi stopped measuring a minute ago, and the number on the screen never knew. This is the hardest idea in the unit and the one the whole panel exists for: the dangerous design is the one that works today.
Image: A calm green gauge with a small unplugged cable in the corner.
---
## Slide 2: Two kinds of not live
- Stale: a value you can no longer vouch for
- Missing: no value at all
- Neither may look live
- Each looks different from the other
Speaker notes: There are two kinds of not live. Stale means the panel has a value, but it cannot vouch for it anymore: it is too old, or it keeps coming back the same. Missing means there is no value at all: the request failed, the reply was unreadable, or the sensor said it could not read. Neither may look like a live value, and they must not look like each other.
Image: Two tiles side by side, one yellow with a hollow diamond, one dark with a boxed X.
---
## Slide 3: One check is not enough
```
fresh update                         update 88  age  1.0 s  live
phone went into a tunnel             update 88  age  9.0 s  OLD, do not show as live
app re-sends update 88, new stamp    update 88  age  0.0 s  live
```
Speaker notes: A delivery app shows your driver's location. This check trusts the timestamp only. The first line is right. The second is right: the phone went into a tunnel and the stamp is nine seconds old. The third is wrong. The app re-sent update eighty eight with a new stamp. The location has not changed, and the timestamp cannot see that. The update number can.
Image: None. This slide is code.
---
## Slide 4: Fresh takes two checks
- Timestamp: sample no more than 5 s old
- Sequence: changed within 5 s, by the panel's clock
- A stamp from the future: clocks disagree
- Any failed check means stale
Speaker notes: Fresh takes two checks, and both must pass. The timestamp must be no more than five seconds old. And the sequence number must have changed within five seconds, measured on the panel's own clock, because the Pi's clock may be the thing that is wrong. In front of both sits a third case: a stamp far in the future means the clocks disagree, and the age is unknown. That is stale too.
Image: Two checkmarks side by side, one labelled clock, one labelled counter.
---
## Slide 5: Four scenes, both checks
```
1. The Pi freezes: sample 50, taken at t=0, is sent again and again.
  t=5  NORMAL      212.4
  t=6  STALE       NOT LIVE   [Last value 212.4 C, 6.0 s old. Not live.]
3. The cable is pulled at t=3.
  t=2  NORMAL      212.2
  t=3  NO DATA     - - -
```
Speaker notes: These lines come from the lab's TileWatch program with both checks written. In scene one the Pi freezes. At five seconds it is still fresh, because the rule says more than five. At six it is stale: the big value says not live, and the old value sits in its own box with its age. In scene three the cable is pulled, and the number disappears at once. A pulled cable means the panel knows nothing.
Image: None. This slide is code.
---
## Slide 6: Three ways to show a value
```
NORMAL   big: 212.4 C   box: (empty)
STALE    big: NOT LIVE   box: Last value 212.4 C, 12 s old. Not live.
NO DATA  big: - - -      box: (empty)
```
Speaker notes: Here is the display rule in three lines. Normal: the live value is the big number. Stale: the big number is the words not live, and the old value appears only in its box, with its age. No data: no number anywhere. The code that printed the third line was handed an old value and threw it away. Format with the invariant culture, so a PC set to another language never shows a comma.
Image: None. This slide is code.
---
## Slide 7: The wrong way: timestamp only
```
  t=6  NORMAL      212.4
  t=7  NORMAL      212.4
  explanation at t=7: Live. Inside limits.
```
Speaker notes: Here is the wrong way. Delete the sequence check and run scene two, the Pi that re-stamps an old reading with the current time. Every second prints normal, two hundred twelve point four, and the explanation says live, inside limits. No error. No crash. The reading is seven seconds old and will never change, and the operator believes the oven is steady.
Image: None. This slide is code.
---
## Slide 8: Why one check is tempting
- The timestamp is in every reply
- It passes every healthy test
- The sequence check must remember
- The failure appears only on bad days
Speaker notes: One check is tempting. The timestamp is right there in every reply, and it passes every test where the Pi behaves. The sequence check needs the panel to remember something between polls, which is more code. And the failure it prevents only shows up when a device misbehaves, which is exactly when an operator is relying on the screen.
Image: A sunny-day checklist with every box ticked, and a storm cloud at the edge.
---
## Slide 9: What you are about to build
- Lab U8-04: the freshness rule, three checks
- The display switch: big value and box
- Twenty self-checks, and TileWatch's four scenes
- Paste both into the project
Speaker notes: In build one you write the freshness rule in Lab U8-04: the future check first, then the timestamp, then the sequence. Then the display switch, which decides the big value and the box for each state. The self-check makes twenty checks, and TileWatch plays four scenes. In build two, after the reteach clinic, you paste both pieces into the project and run its acceptance tests. Tomorrow is the post-test.
Image: A tile on a screen showing NOT LIVE, with a small box beneath it.
---
