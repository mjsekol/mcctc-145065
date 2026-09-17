# Lecture Notes: Four States from Four Booleans
## 145065 Object-Oriented Programming · Unit 8 · Week 15, Wednesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W15_FourStatesFromFourBooleans.md). There is no exported
deck yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-08-industrial-hmi/04-slides/MCCTC_145065_Slides_W15_FourStatesFromFourBooleans.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK for the
examples.

**Competencies:** 5.3.1 Boolean logic · 5.3.2 truth tables · 5.3.3 logical operators · 5.3.4 relational
operators · 5.6.14 testing · 1.2.7 reaching agreement on a threshold.

Every output below was printed by a real build: .NET SDK 10.0.401, `net8.0`.

---

## Why this exists

Every tile on your panel must be in exactly one of four states: NORMAL, ALARM, STALE, or NO DATA. Four
facts decide which. Four true-or-false facts make sixteen combinations, and a panel that gets even one
of them wrong will, some night, show an operator the wrong thing.

You cannot test "it seems right." You can test sixteen rows. That is what a truth table is for.

This is also the heaviest outcome on the WebXam. Programming logic, 5.3, is about 26 percent of the
exam, and Boolean logic and truth tables are the start of it.

---

## The concept in plain language

**The four facts** for one sensor:

| Letter | Fact |
|---|---|
| **A** | The panel got an answer from the service |
| **K** | The sensor reported a value (`ok` was true) |
| **F** | The sample is fresh |
| **W** | The value is within its limits |

**A truth table lists every combination.** With four facts, that is 2 × 2 × 2 × 2 = 16 rows. Count from
0 to 15 in binary with four digits, and each digit is one column. Then write the state for each row by
hand, from the course's definitions, before you write any code.

**The order of the checks is the design.** Some facts only mean something when others are true. A
value you do not have cannot be fresh or stale. A value that is not live cannot be trusted to be inside
or outside its limits. So you ask the questions in the order that makes each answer meaningful.

**A value on a limit is inside.** The course's limits are the last acceptable value. That decides `>`
versus `>=`, and a truth table cannot decide it for you. Your team has to write it down.

**A limit is a decision people make together.** The number in `thresholds.json` needs a reason an
operator can read. Agreeing on it is a skill: state the problem, name the evidence, argue both sides,
then decide and record who agreed.

---

## Worked example 1: De Morgan's law, proved by a table

"Not (A and K)" and "not A, or not K" are the same thing. You do not have to take that on faith. You
can print every row.

```csharp
Console.WriteLine("A      K      !(A && K)  !A || !K");
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

The last two columns match on every row, so the two expressions are equal. When a WebXam item asks
which expression is equivalent, this is the method: build the table, compare the columns.

---

## Worked example 2: a smaller table, where order matters

Your panel's table has sixteen rows, and you build it yourself in Lab U8-03. Here is the same idea with
three facts and a situation you know: what a game console shows on your friend list.

- **C**: the console has a connection.
- **S**: the player is signed in.
- **M**: the player is in a match.

S and M are the last things the server heard. Without a connection, they are old news. So the right
order asks about C first.

```csharp
static string Status(bool connected, bool signedIn, bool inMatch)
{
    if (!connected) return "Offline";
    if (!signedIn) return "Signed out";
    return inMatch ? "In a match" : "Online";
}
```

A program that prints all eight rows, with a count:

```
C      S      M      right order    match checked first
False  False  False  Offline        Offline
False  False  True   Offline        In a match
False  True   False  Offline        Offline
False  True   True   Offline        In a match
True   False  False  Signed out     Signed out
True   False  True   Signed out     In a match
True   True   False  Online         Online
True   True   True   In a match     In a match
8 rows: Offline 4, Signed out 2, Online 1, In a match 1
```

Read the counts. Half the rows are Offline, because once C is false nothing else matters. Your panel's
table has the same shape: the first fact that makes the others meaningless takes the most rows.

The right-hand column is the wrong version, below.

---

## Worked example 3: the boundary, and a limit that may not exist

A posted rule says a ticket is for going **over** 55. At exactly 55 there is no ticket.

```csharp
using System.Globalization;

foreach (double speed in new[] { 54.9, 55.0, 55.1 })
{
    string right = speed > 55.0 ? "ticket" : "no ticket";
    string wrong = speed >= 55.0 ? "ticket" : "no ticket";
    Console.WriteLine(string.Create(CultureInfo.InvariantCulture,
        $"{speed:0.0} mph   with >: {right,-10} with >=: {wrong}"));
}

int? cap = null;
int players = 31;
string verdict = cap is int max && players > max ? "full" : "room to join";
Console.WriteLine($"{players} players, cap {(cap is null ? "none" : cap)}: {verdict}");
```

```
54.9 mph   with >: no ticket  with >=: no ticket
55.0 mph   with >: no ticket  with >=: ticket
55.1 mph   with >: ticket     with >=: ticket
31 players, cap none: room to join
```

Only the boundary row differs. That is why boundary tests exist: test the value on the limit, and one
step each side.

The second half uses `int?`, a number that may be missing. `cap is int max` is true only when `cap`
has a value, and it names that value `max`. A missing cap is never compared. Some of your sensors have
a high limit and no low limit, so you will need exactly this.

---

## The wrong version, part 1: the interesting fact first

```csharp
static string MatchFirst(bool connected, bool signedIn, bool inMatch)
{
    if (inMatch) return "In a match";
    if (!connected) return "Offline";
    return signedIn ? "Online" : "Signed out";
}
```

It compiles with 0 warnings. Look at the right-hand column in example 2: rows 2 and 4 say **In a match**
for a console that is offline. Your friend thinks you are mid-game. You are on a bus with no signal.

On the panel, the same mistake judges a value against its limit before asking whether it is live. The
lab's self-check catches it with this message for the row where A and K are true and F and W are false:

```
Assert.Equal() Failure: Values differ
Expected: Stale
Actual:   Alarm
```

An operator would see an alarm on a number that is not live.

## The wrong version, part 2: forcing a value that is not there

```csharp
int? cap = null;
int players = 31;
Console.WriteLine(players > cap.Value ? "full" : "room to join");
```

The compiler warns:

```
warning CS8629: Nullable value type may be null.
```

and the program throws:

```
Unhandled exception. System.InvalidOperationException: Nullable object must have a value.
```

`.Value` says "I promise there is a number here." When there is not, the program stops. A sensor with
no low limit would crash the panel the first time it was checked.

---

## Why the wrong versions are tempting

The alarm is the most important state, so it feels right to check it first. And `.Value` makes the
compiler's complaint about `int?` go away. Both hide a row you did not think about. The truth table
makes you think about every row.

---

## Agreeing on a limit (1.2.7)

Your oven limit is a number the whole shift lives with. A good agreement follows five steps:

1. **State the problem the limit prevents.** "Parts discolor above 230 C" is a problem. "230 seems
   high" is a preference.
2. **Name the evidence.** What the simulator measured, how fast a drift climbs, what the process sheet
   says.
3. **Argue both sides.** A lower limit catches a drift sooner. It also alarms closer to normal
   running. Say both.
4. **Ask before you argue.** Reviewers ask a question first, and proposers answer the question asked.
5. **Record the decision and who agreed.** If you did not agree, record that, and what would settle it.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Boolean** | A value that is true or false |
| **Truth table** | Every combination of some Booleans, with a result for each |
| **`&&`, `||`, `!`** | And, or, not |
| **De Morgan's law** | `!(a && b)` equals `!a || !b`; `!(a || b)` equals `!a && !b` |
| **Relational operator** | `<`, `<=`, `>`, `>=`, `==`, `!=` |
| **Boundary test** | A test on the limit and one step either side |
| **Nullable value type** | `int?`, `double?`: a number that may be missing |
| **Type pattern** | `x is double d`: true only when `x` holds a value, which is named `d` |
| **Consensus** | A decision the group can support, reached by argument, not by vote alone |

---

## Self-check

**Question 1.** Is `!(inRange || stale)` the same as `!inRange && !stale`? Show a table to prove it.

**Question 2.** In example 2's right-order version, how many rows would say "Signed out" if you added a
fourth fact, "the player is muted", that does not affect the status?

**Question 3.** A sensor's high limit is 6.0 and it has no low limit. List the three values you would put
in its boundary test, and what each should return.

---

### Answers

**1.** Yes, by De Morgan's law.

| inRange | stale | `!(inRange \|\| stale)` | `!inRange && !stale` |
|---|---|---|---|
| false | false | true | true |
| false | true | false | false |
| true | false | false | false |
| true | true | false | false |

The columns match on every row.

**2.** Four. The new fact doubles every row, so the two "Signed out" rows become four.

**3.** 5.9 is inside, 6.0 is inside (on the limit), and 6.1 is above the high limit. Because there is no
low limit, a very small value such as 0.0 is also inside, and it is worth a fourth test.
