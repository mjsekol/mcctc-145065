// StaleOrMissingChecks.cs  .  Lab U08-04 self-check  .  given to you
//
// Your CheckFreshness against the freshness rule, and your Apply against the
// display rules: a stale number is never shown as live, and a missing value
// shows no number at all. The times are invented sample data.

using System.ComponentModel;
using Line3.Hmi.Core;
using Line3.Hmi.Core.ViewModels;

namespace Display.SelfCheck;

public class FreshnessChecks
{
    private static readonly DateTimeOffset T0 = new(2027, 1, 11, 14, 3, 22, TimeSpan.Zero);
    private static readonly TimeSpan Limit = TimeSpan.FromSeconds(5);

    [Theory]
    [InlineData(0, 0, StaleReason.None)]
    [InlineData(5, 5, StaleReason.None)]
    [InlineData(5.001, 0, StaleReason.SampleTooOld)]
    [InlineData(0, 5.001, StaleReason.SequenceNotAdvancing)]
    [InlineData(60, 60, StaleReason.SampleTooOld)]
    [InlineData(-5, 0, StaleReason.None)]
    [InlineData(-5.001, 0, StaleReason.ClockDisagrees)]
    [InlineData(-600, 30, StaleReason.ClockDisagrees)]
    public void F01_TwoIndependentChecksAndOneHonestLimit(double sampleAgeSeconds, double sinceSequenceSeconds, StaleReason expected)
    {
        StaleReason actual = StateRules.CheckFreshness(
            T0,
            T0 - TimeSpan.FromSeconds(sampleAgeSeconds),
            T0 - TimeSpan.FromSeconds(sinceSequenceSeconds),
            Limit);
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void F02_APiThatRestampsAnOldSampleIsCaughtBySequence()
    {
        // sampled_at says "just now", but sequence has not changed for 7 s.
        Assert.Equal(StaleReason.SequenceNotAdvancing,
            StateRules.CheckFreshness(T0.AddSeconds(7), T0.AddSeconds(7), T0, Limit));
    }

    [Fact]
    public void F03_APiWithASlowClockIsNeverTrustedAsLive()
    {
        // The Pi thinks it is an hour earlier. Every sample looks old. That is
        // the safe mistake to make.
        Assert.Equal(StaleReason.SampleTooOld, StateRules.CheckFreshness(T0, T0.AddHours(-1), T0, Limit));
    }
}

public class DisplayChecks
{
    private static readonly SensorThreshold Oven = new("oven-temp", "Cure oven temperature", "C", 1, 190.0, 230.0,
        "a reason of twenty characters or more");

    private static readonly SensorThreshold Coolant = new("coolant-level", "Coolant level", "%", 0, 25.0, null,
        "a reason of twenty characters or more");

    private static SensorTileViewModel NewTile(SensorThreshold t) => new(t, _ => { });

    private static SensorStatus Normal(SensorThreshold t, double value) =>
        new(t, SensorState.Normal, value, null, null, AlarmSide.None, MissingReason.None, StaleReason.None, AlarmLatchState.Clear, "Live. Inside limits.");

    private static SensorStatus Alarm(SensorThreshold t, double value, AlarmSide side, AlarmLatchState latch = AlarmLatchState.ActiveUnacked) =>
        new(t, SensorState.Alarm, value, null, null, side, MissingReason.None, StaleReason.None, latch, "Live. Outside limits.");

    private static SensorStatus Stale(SensorThreshold t, double? last, double ageSeconds, AlarmLatchState latch = AlarmLatchState.Clear) =>
        new(t, SensorState.Stale, null, last, TimeSpan.FromSeconds(ageSeconds), AlarmSide.None, MissingReason.None,
            StaleReason.SampleTooOld, latch, "Not updated, so it is not live.");

    private static SensorStatus Missing(SensorThreshold t, AlarmLatchState latch = AlarmLatchState.Clear) =>
        new(t, SensorState.Missing, null, null, null, AlarmSide.None, MissingReason.ServiceDown, StaleReason.None, latch,
            "No connection to the sensor service. Check it at the machine.");

    [Fact]
    public void D01_NormalShowsTheLiveValueFormatted()
    {
        SensorTileViewModel tile = NewTile(Oven);
        tile.Apply(Normal(Oven, 212.44));
        Assert.Equal("NORMAL", tile.StateText);
        Assert.Equal("212.4", tile.ValueText);
        Assert.True(tile.ValueIsLive);
        Assert.Equal(string.Empty, tile.LastKnownText);
    }

    [Fact]
    public void D02_ZeroDecimalsShowsNoDecimalPoint()
    {
        SensorTileViewModel tile = NewTile(Coolant);
        tile.Apply(Normal(Coolant, 67.6));
        Assert.Equal("68", tile.ValueText);
    }

    [Theory]
    [InlineData(236.0, AlarmSide.High, "ALARM HIGH", "236.0")]
    [InlineData(185.5, AlarmSide.Low, "ALARM LOW", "185.5")]
    public void D03_AnAlarmShowsItsSideAndTheLiveValue(double value, AlarmSide side, string words, string shown)
    {
        SensorTileViewModel tile = NewTile(Oven);
        tile.Apply(Alarm(Oven, value, side));
        Assert.Equal(words, tile.StateText);
        Assert.Equal(shown, tile.ValueText);
        Assert.True(tile.ValueIsLive);
    }

    [Fact]
    public void D04_StaleNeverPutsTheNumberInTheBigValue()
    {
        SensorTileViewModel tile = NewTile(Oven);
        tile.Apply(Stale(Oven, 212.4, 12));
        Assert.Equal("STALE", tile.StateText);
        Assert.Equal(SensorTileViewModel.NotLiveText, tile.ValueText);
        Assert.DoesNotContain("212", tile.ValueText);
        Assert.False(tile.ValueIsLive);
    }

    [Fact]
    public void D05_StaleShowsTheLastValueWithItsAgeAndTheWordsNotLive()
    {
        SensorTileViewModel tile = NewTile(Oven);
        tile.Apply(Stale(Oven, 212.4, 12));
        Assert.Equal("Last value 212.4 C, 12 s old. Not live.", tile.LastKnownText);
        Assert.True(tile.HasLastKnown);
    }

    [Fact]
    public void D06_MissingShowsNoNumberAnywhere()
    {
        SensorTileViewModel tile = NewTile(Oven);
        tile.Apply(Normal(Oven, 212.4));
        tile.Apply(Missing(Oven));
        Assert.Equal("NO DATA", tile.StateText);
        Assert.Equal(SensorTileViewModel.NoValueText, tile.ValueText);
        Assert.Equal(string.Empty, tile.LastKnownText);
        Assert.False(tile.ValueIsLive);
        Assert.DoesNotMatch("[0-9]", tile.ValueText + tile.LastKnownText);
    }

    [Fact]
    public void D07_GoingFromStaleBackToNormalRemovesTheNotLiveBox()
    {
        SensorTileViewModel tile = NewTile(Oven);
        tile.Apply(Stale(Oven, 212.4, 8));
        tile.Apply(Normal(Oven, 212.9));
        Assert.Equal("212.9", tile.ValueText);
        Assert.False(tile.HasLastKnown);
    }

    [Fact]
    public void D08_AnAlarmBannerStaysUpWhenTheDataGoesStaleOrMissing()
    {
        SensorTileViewModel tile = NewTile(Oven);
        tile.Apply(Alarm(Oven, 236.0, AlarmSide.High));
        tile.Apply(Stale(Oven, 236.0, 9, AlarmLatchState.ActiveUnacked));
        Assert.Equal("UNACKNOWLEDGED ALARM", tile.AlarmBannerText);
        Assert.Equal(SensorTileViewModel.NotLiveText, tile.ValueText);
        tile.Apply(Missing(Oven, AlarmLatchState.ActiveUnacked));
        Assert.Equal("UNACKNOWLEDGED ALARM", tile.AlarmBannerText);
        Assert.Equal("NO DATA", tile.StateText);
    }

    [Fact]
    public void D09_TheWindowHearsAboutEveryChange()
    {
        SensorTileViewModel tile = NewTile(Oven);
        List<string?> heard = new();
        ((INotifyPropertyChanged)tile).PropertyChanged += (_, e) => heard.Add(e.PropertyName);
        tile.Apply(Stale(Oven, 212.4, 6));
        Assert.Contains(nameof(SensorTileViewModel.StateText), heard);
        Assert.Contains(nameof(SensorTileViewModel.ValueText), heard);
        Assert.Contains(nameof(SensorTileViewModel.LastKnownText), heard);
        Assert.Contains(nameof(SensorTileViewModel.HasLastKnown), heard);
    }
}
