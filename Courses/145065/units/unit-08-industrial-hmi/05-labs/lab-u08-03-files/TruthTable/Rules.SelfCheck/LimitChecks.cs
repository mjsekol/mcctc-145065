// LimitChecks.cs  .  Lab U08-03 self-check  .  given to you
//
// Checks your SensorThreshold.Check, including the values on the limits,
// then your team's thresholds file. The limits in the first three checks are
// the Line 3 file's. Riverside Fabrication is a composite.

using Line3.Hmi.Core;

namespace Rules.SelfCheck;

public class LimitChecks
{
    private static readonly SensorThreshold Oven = new("oven-temp", "Cure oven temperature", "C", 1, 190.0, 230.0, "a reason of twenty characters or more");
    private static readonly SensorThreshold Press = new("press-vibration", "Press vibration", "mm/s", 1, null, 6.0, "a reason of twenty characters or more");
    private static readonly SensorThreshold Coolant = new("coolant-level", "Coolant level", "%", 0, 25.0, null, "a reason of twenty characters or more");

    [Theory]
    [InlineData(212.4, LimitCheck.Within)]
    [InlineData(190.0, LimitCheck.Within)]
    [InlineData(230.0, LimitCheck.Within)]
    [InlineData(189.9, LimitCheck.BelowLow)]
    [InlineData(230.1, LimitCheck.AboveHigh)]
    [InlineData(-40.0, LimitCheck.BelowLow)]
    public void L01_TheOvenHasTwoLimitsAndAValueOnALimitIsInside(double value, LimitCheck expected) =>
        Assert.Equal(expected, Oven.Check(value));

    [Theory]
    [InlineData(0.0, LimitCheck.Within)]
    [InlineData(6.0, LimitCheck.Within)]
    [InlineData(6.1, LimitCheck.AboveHigh)]
    public void L02_ThePressHasOnlyAHighLimit(double value, LimitCheck expected) =>
        Assert.Equal(expected, Press.Check(value));

    [Theory]
    [InlineData(1000.0, LimitCheck.Within)]
    [InlineData(25.0, LimitCheck.Within)]
    [InlineData(24.0, LimitCheck.BelowLow)]
    public void L03_TheCoolantHasOnlyALowLimit(double value, LimitCheck expected) =>
        Assert.Equal(expected, Coolant.Check(value));

    [Fact]
    public void L04_SideOfNamesTheSide()
    {
        Assert.Equal(AlarmSide.High, StateRules.SideOf(Oven.Check(236.0)));
        Assert.Equal(AlarmSide.Low, StateRules.SideOf(Oven.Check(185.5)));
        Assert.Equal(AlarmSide.None, StateRules.SideOf(Oven.Check(212.0)));
    }

    [Fact]
    public void L05_YourTeamsThresholdsFileLoadsAndEveryReasonIsYours()
    {
        PanelConfig config = PanelConfig.Load(Path.Combine(AppContext.BaseDirectory, "thresholds.json"));
        Assert.Equal(3, config.Sensors.Count);
        foreach (SensorThreshold t in config.Sensors)
        {
            Assert.False(t.Reason.StartsWith("REPLACE THIS", StringComparison.Ordinal),
                $"{t.Id} still has the placeholder reason. Write the reason your team agreed on (step 11).");
        }
    }

    [Fact]
    public void L06_TheSimulatorsNormalOvenStaysInsideYourLimits()
    {
        // The simulator's normal oven wanders from 211.0 to 213.0 C. Limits
        // that alarm on normal running teach operators to ignore alarms.
        PanelConfig config = PanelConfig.Load(Path.Combine(AppContext.BaseDirectory, "thresholds.json"));
        SensorThreshold oven = config.Sensors.Single(s => s.Id == "oven-temp");
        Assert.Equal(LimitCheck.Within, oven.Check(211.0));
        Assert.Equal(LimitCheck.Within, oven.Check(213.0));
    }
}
