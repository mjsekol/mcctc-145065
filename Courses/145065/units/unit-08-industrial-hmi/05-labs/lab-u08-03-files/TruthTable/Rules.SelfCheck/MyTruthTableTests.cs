// MyTruthTableTests.cs  .  Lab U08-03  .  YOURS TO FINISH (step 5)
//
// One InlineData row per combination of A, K, F, W: sixteen in all. Two
// rows are here to show the shape. Write the other fourteen from your paper
// truth table, not from your code. A test copied from the code it tests
// proves nothing.

using Line3.Hmi.Core;

namespace Rules.SelfCheck;

public class MyTruthTableTests
{
    [Theory]
    [InlineData(false, false, false, false, SensorState.Missing)]
    [InlineData(true, true, true, true, SensorState.Normal)]
    public void EveryRow(bool haveAnswer, bool sensorOk, bool fresh, bool withinLimits, SensorState expected) =>
        Assert.Equal(expected, StateRules.Decide(haveAnswer, sensorOk, fresh, withinLimits));
}
