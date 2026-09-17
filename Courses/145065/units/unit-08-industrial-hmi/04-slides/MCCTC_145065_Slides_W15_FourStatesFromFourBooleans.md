# Four States from Four Booleans
---
## Slide 1: In a match, on a bus with no signal
- Your friend list says you are mid-game
- You are on a bus with no signal
- The app checked the fun fact first
- Order decided what your friends believe
Speaker notes: Your friend list says you are in a match. You are actually on a bus with no signal. The app looked at the last thing the server heard, in a match, before asking whether it could trust anything at all. The order of the questions decided what your friends believe. On an operator panel, the same mistake decides what an operator believes about an oven.
Image: A phone friend list showing "In a match" next to a bus window with no-signal bars.
---
## Slide 2: Four facts, sixteen rows
- A: the panel got an answer
- K: the sensor reported a value
- F: the sample is fresh
- W: the value is within its limits
Speaker notes: Every tile's state comes from four true-or-false facts. A, did the panel get an answer. K, did the sensor report a value. F, is the sample fresh. W, is the value within its limits. Four facts make two times two times two times two, sixteen combinations. A truth table lists every one, and you fill it in on paper before you write code.
Image: A blank sixteen-row truth table with columns A, K, F, W, and State.
---
## Slide 3: De Morgan, proved by printing
```csharp
foreach (bool a in new[] { false, true })
{
    foreach (bool k in new[] { false, true })
    {
        Console.WriteLine($"{a,-6} {k,-6} {!(a && k),-10} {!a || !k}");
    }
}
```
```
A      K      !(A && K)  !A || !K
False  False  True       True
False  True   True       True
True   False  True       True
True   True   False      False
```
Speaker notes: De Morgan's law says not A and K equals not A or not K. You do not have to believe me. Print every row and compare the last two columns. They match on all four rows, so the expressions are equal. When a WebXam item asks which expression is equivalent, this is your method: build the table, compare the columns.
Image: None. This slide is code.
---
## Slide 4: Order is the design
```csharp
static string Status(bool connected, bool signedIn, bool inMatch)
{
    if (!connected) return "Offline";
    if (!signedIn) return "Signed out";
    return inMatch ? "In a match" : "Online";
}
```
```
8 rows: Offline 4, Signed out 2, Online 1, In a match 1
```
Speaker notes: Here is the friend list done right, with three facts. Connected first, because without a connection the other two are old news. Signed in second. Match last. Print all eight rows and count. Half are offline, because once connected is false nothing else matters. Your panel's table has the same shape, and you write its version in the lab.
Image: None. This slide is code.
---
## Slide 5: The wrong way: the exciting fact first
```
False  False  True   Offline        In a match
False  True   True   Offline        In a match
```
```
Assert.Equal() Failure: Values differ
Expected: Stale
Actual:   Alarm
```
Speaker notes: Check the match first, and two offline rows say in a match. It compiles with zero warnings. On the panel, the same mistake judges a value against its limit before asking whether the value is live. The lab's self-check catches it with this message: expected stale, actual alarm. An operator would see an alarm on a number that is not live.
Image: None. This slide is code.
---
## Slide 6: A value on the limit is inside
- Rule: a ticket for going over 55
- 55.0 with greater-than: no ticket
- 55.0 with greater-or-equal: ticket
- Test the limit, and one step each side
Speaker notes: A posted rule says tickets are for going over fifty five. At exactly fifty five, no ticket. Written with greater than, the code agrees. Written with greater than or equal, it writes a ticket. Only the boundary row differs, which is why boundary tests exist. The course's limits are the last acceptable value, so a value on the limit is inside.
Image: A speedometer needle resting exactly on 55.
---
## Slide 7: A limit that may not exist
- Some sensors have no low limit
- int? and double? may hold nothing
- "cap is int max" is true only with a value
- .Value on nothing throws
Speaker notes: Some of your sensors have a high limit and no low limit. C sharp says that with a nullable number, a question mark after the type. The pattern cap is int max is true only when there is a value, and it names it. If you force it with dot Value instead, the compiler warns CS8629, and the program throws: Nullable object must have a value.
Image: A game lobby screen showing "Player cap: none".
---
## Slide 8: Agreeing on a limit
- State the problem the limit prevents
- Name the evidence
- Argue both sides before deciding
- Record who agreed, or what would settle it
Speaker notes: Your oven limit is a number a whole shift lives with. Agree on it the way a shop does. State the problem it prevents, like parts discoloring. Name the evidence: what the simulator measured, how fast a drift climbs. Argue both sides: a lower limit catches drift sooner and alarms closer to normal. Then record the decision and who agreed. If you did not agree, record that too.
Image: Four people at a table around a single printed chart.
---
## Slide 9: What you are about to build
- Lab U8-03: the paper truth table first
- Decide and the limit check, then 36 checks
- The threshold meeting with another pair
- Your oven reason, in plain words
Speaker notes: Build one is Lab U8-03. Fill in all sixteen rows on paper before any code. Then write Decide and the limit check until the self-check shows thirty six passed. Build two is the threshold meeting. Each pair plays maintenance lead and operator for another pair's oven limit. Then you write your own reason into thresholds dot json and defend it in THRESHOLDS dot md.
Image: A paper truth table beside a laptop showing a passing test run.
---
