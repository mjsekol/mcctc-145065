// TruthTableChecks.cs  .  Lab U08-03 self-check  .  given to you
//
// Checks your Decide against the course definitions, one definition per
// check, and checks that your own test has all sixteen rows.

using System.Reflection;
using Line3.Hmi.Core;

namespace Rules.SelfCheck;

public class TruthTableChecks
{
    private static readonly bool[] Both = { false, true };

    private static IEnumerable<(bool A, bool K, bool F, bool W)> AllRows()
    {
        foreach (bool a in Both)
        foreach (bool k in Both)
        foreach (bool f in Both)
        foreach (bool w in Both)
        {
            yield return (a, k, f, w);
        }
    }

    [Fact]
    public void T01_NoAnswerMeansMissingWhateverElseIsTrue()
    {
        foreach (var r in AllRows().Where(r => !r.A))
        {
            Assert.True(StateRules.Decide(r.A, r.K, r.F, r.W) == SensorState.Missing, $"row {r}: no answer, so nothing is known");
        }
    }

    [Fact]
    public void T02_ASensorThatIsNotOkIsMissingWhateverElseIsTrue()
    {
        foreach (var r in AllRows().Where(r => !r.K))
        {
            Assert.True(StateRules.Decide(r.A, r.K, r.F, r.W) == SensorState.Missing, $"row {r}: the sensor gave no value");
        }
    }

    [Fact]
    public void T03_AValueThatIsNotFreshIsStaleEvenOutsideItsLimits()
    {
        foreach (var r in AllRows().Where(r => r.A && r.K && !r.F))
        {
            Assert.True(StateRules.Decide(r.A, r.K, r.F, r.W) == SensorState.Stale, $"row {r}: a value that is not live");
        }
    }

    [Fact]
    public void T04_ALiveValueIsAlarmExactlyWhenItIsOutsideItsLimits()
    {
        Assert.Equal(SensorState.Alarm, StateRules.Decide(true, true, true, false));
        Assert.Equal(SensorState.Normal, StateRules.Decide(true, true, true, true));
    }

    [Fact]
    public void T05_YourTestHasAllSixteenRows()
    {
        MethodInfo method = typeof(MyTruthTableTests).GetMethod(nameof(MyTruthTableTests.EveryRow))!;
        HashSet<string> rows = new();
        foreach (InlineDataAttribute row in method.GetCustomAttributes<InlineDataAttribute>())
        {
            object[] values = row.GetData(method).Single();
            rows.Add($"{values[0]} {values[1]} {values[2]} {values[3]}");
        }

        Assert.True(rows.Count == 16, $"MyTruthTableTests.EveryRow has {rows.Count} different rows; it needs all 16");
    }
}
