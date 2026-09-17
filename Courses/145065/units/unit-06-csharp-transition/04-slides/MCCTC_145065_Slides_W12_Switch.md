# The First Match Wins
---
## Slide 1: 250 degrees is a warning
- The oven reads 250 degrees
- The alarm limit is 240
- The panel shows WARNING
- The build was perfectly clean
Speaker notes: An oven at two hundred fifty degrees. The alarm limit is two hundred forty. The panel shows a warning, not an alarm. Nobody got an error, and the build had zero warnings. By the end of this segment you will spot this bug by reading four lines, and you will know exactly when the compiler can catch it for you.
Image: A panel tile reading "WARNING 250 C" in amber, with an alarm bell sitting unused beside it.
---
## Slide 2: Two kinds of switch
- Statement: run code for the matching case
- Expression: turn one value into one value
- Both replace a long if and else chain
- Python's match is the closest cousin
Speaker notes: C# has two switches. The statement runs a block of code for whichever case matches. The expression produces a value. Both replace a long chain of if and else if when you are comparing one value against a list. Python's match statement is the closest thing you have seen.
Image: A railroad switch sending one train down one of several tracks.
---
## Slide 3: The expression
```csharp
static Level Classify(double? tempC) => tempC switch
{
    null => Level.Missing,
    >= 240 => Level.Alarm,
    >= 215 => Level.Warning,
    _ => Level.Normal,
};
```
Speaker notes: One value in, one value out. The arms are tried top to bottom, and the first arm that matches wins. Null first, because a missing reading is not a number. Then the most urgent test. Greater than or equal to 240 is a relational pattern. The underscore catches everything left.
Image: None. This slide is code.
---
## Slide 4: The statement
```csharp
static string Advice(Level level)
{
    switch (level)
    {
        case Level.Alarm:
            return "call the lead now";
        case Level.Warning:
            return "watch it";
        default:
            return "no action";
    }
}
```
Speaker notes: The statement form. Each case ends with return here, or with break. Level is an enum, a type with a fixed set of names, so a misspelled level does not build. Default handles everything else, including a number that somebody cast into the enum by accident.
Image: None. This slide is code.
---
## Slide 5: Wrong order, constant limits
```csharp
static string Classify(double tempC) => tempC switch
{
    >= 215 => "warning",
    >= 240 => "alarm",
    _ => "normal",
};
```
```
error CS8510: The pattern is unreachable. It has already been handled by a previous arm of the switch expression or it is impossible to match.
```
Speaker notes: Here is the wrong way with the real error. Every value at or above 240 is also at or above 215, so the alarm arm can never win. The limits are constants, so the compiler can prove it, and it refuses with CS8510. Good. Now watch what happens when the limits come from settings.
Image: None. This slide is code.
---
## Slide 6: Wrong order, limits from settings
```csharp
string Classify(double tempC) => tempC switch
{
    var t when t >= warnAtC => "warning",
    var t when t >= alarmAtC => "alarm",
    _ => "normal",
};

Console.WriteLine(Classify(250));   // warning
```
Speaker notes: Same mistake. The limits are variables now, read from a settings file like a real panel would. When clauses test them. It builds with zero warnings and prints warning for 250. The compiler cannot prove the second arm unreachable, because somebody could set the alarm limit below the warning limit. This is slide one.
Image: None. This slide is code.
---
## Slide 7: No falling through
- Code under a case must end on purpose
- break, return, or throw
- Stacked labels with no code are fine
- CS0163 if a case runs into the next
Speaker notes: The statement has one more rule. Code under a case must end on purpose, with break, return, or throw. If it runs into the next case, that is CS0163. Two labels stacked on one block are fine, because the first label has no code of its own. Other languages allow fall through, and forgetting one break there is a classic silent bug.
Image: A staircase with a gate at each landing.
---
## Slide 8: When nothing matches
- An expression with no default arm
- Warning CS8509 at build time
- SwitchExpressionException at run time
- Python's match quietly does nothing
Speaker notes: A switch expression must produce a value, so if no arm matches, it cannot quietly move on. You get warning CS8509 at build time, and an exception at run time. Python's match with no matching case does nothing and moves to the next line. Neither is what a panel wants. Add an underscore arm and decide what an unknown value means.
Image: A sorting machine with an overflow bin labeled "unknown."
---
## Slide 9: The habit that catches slide one
- Most urgent test first
- Read the arms with the extreme value
- Write a test above the highest limit
- 240 and 9999 are both alarms
Speaker notes: The habit. Put the most urgent test first. Read the arms top to bottom with the most extreme value in your hand. And write a test for a value above the highest limit. In the lab, 240 and 9999 must both come back as alarms. If your arm order is wrong, that test is the one that tells you.
Image: A thermometer with test points marked at 240 and 9999.
---
## Slide 10: What you are about to build
- Lab U06-03, Part 3: the classifier
- Classify as a switch expression
- Label as a switch statement
- A made-up level, 42, must be refused
Speaker notes: Build one is Part 3 of the lab. Classify is a switch expression with limits passed in, so the compiler cannot check your order. The tests will. Label is a switch statement with a default that refuses a level that is not a real level, like forty two cast into the enum. In build two, your port gets a switch wherever one value maps to cases.
Image: A test list with 240.0 and 9999.0 both marked Alarm in green.
---
