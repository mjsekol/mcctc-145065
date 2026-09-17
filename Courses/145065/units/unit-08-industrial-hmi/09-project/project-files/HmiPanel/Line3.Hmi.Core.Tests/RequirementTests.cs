// RequirementTests.cs  .  HMI PANEL project  .  acceptance tests, given to you
//
// One test (or a few) per operator requirement, named REQnn after the
// requirement it proves. Adapted from the course's HMI anchor test suite.
// They fail on the starter, and pass once your Lab U08-03, U08-04, and U08-05
// pieces are pasted in and your team's thresholds file is finished.
//
// Every value that depends on a limit is read from YOUR thresholds.json, so
// these tests check your team's numbers, not someone else's.
//
//   dotnet test

using System.Diagnostics;
using Line3.Hmi.Core.ViewModels;
using static Line3.Hmi.Core.Tests.TestData;

namespace Line3.Hmi.Core.Tests;

public class RequirementTests
{
    private readonly ManualClock clock = new(T0);

    private PanelViewModel NewPanel() => new(Config(), clock, TimeZoneInfo.Utc);

    private static SensorTileViewModel Tile(PanelViewModel panel, string id) => panel.Tiles.First(t => t.Id == id);

    private static SensorStatus OvenOf(PanelUpdate update) => update.Sensors.First(s => s.SensorId == "oven-temp");

    // Six degrees past your team's high limit: always an alarm, always a live value.
    private static double OvenTooHot => Oven.High!.Value + 6.0;

    private static SensorThreshold Coolant => ShippedConfig().Sensors.First(s => s.Id == "coolant-level");

    [Fact]
    public void REQ01_EveryStateHasItsOwnWords()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0, oven: OvenTooHot, coolant: Coolant.Low!.Value - 3.0));
        Assert.Equal("NORMAL", Tile(panel, "press-vibration").StateText);
        Assert.Equal("ALARM HIGH", Tile(panel, "oven-temp").StateText);
        Assert.Equal("ALARM LOW", Tile(panel, "coolant-level").StateText);

        clock.Advance(TimeSpan.FromSeconds(8));
        panel.ReceiveResult(Good(1, T0, clock.UtcNow));
        Assert.Equal("STALE", Tile(panel, "press-vibration").StateText);

        panel.ReceiveResult(Bad(PollFailure.ServiceDown, clock.UtcNow));
        Assert.Equal("NO DATA", Tile(panel, "press-vibration").StateText);
    }

    [Fact]
    public void REQ02_StaleNeverShowsTheNumberAsTheValue()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(50, T0, T0, oven: 212.4));
        clock.Advance(TimeSpan.FromSeconds(12));
        panel.ReceiveResult(Good(50, T0, clock.UtcNow, oven: 212.4));

        SensorTileViewModel oven = Tile(panel, "oven-temp");
        Assert.Equal("STALE", oven.StateText);
        Assert.Equal(SensorTileViewModel.NotLiveText, oven.ValueText);
        Assert.DoesNotContain("212", oven.ValueText);
        Assert.False(oven.ValueIsLive);
        Assert.Equal("Last value 212.4 C, 12 s old. Not live.", oven.LastKnownText);
        Assert.Equal("DATA NOT UPDATING", panel.ConnectionTitle);
    }

    [Fact]
    public void REQ02_StaleBySequenceKeepsTheLastValueButNeverAsLive()
    {
        PanelMonitor monitor = new(Config());
        for (int second = 0; second <= 8; second++)
        {
            monitor.Record(Good(50, T0, T0.AddSeconds(second)));
        }

        SensorStatus oven = OvenOf(monitor.Update(T0.AddSeconds(8)));
        Assert.Equal(SensorState.Stale, oven.State);
        Assert.Null(oven.LiveValue);
        Assert.Equal(212.4, oven.LastKnownValue);
        Assert.Equal(TimeSpan.FromSeconds(8), oven.LastKnownAge);
    }

    [Theory]
    [InlineData(PollFailure.ServiceDown, MissingReason.ServiceDown)]
    [InlineData(PollFailure.Timeout, MissingReason.Timeout)]
    [InlineData(PollFailure.HttpError, MissingReason.HttpError)]
    [InlineData(PollFailure.MalformedReply, MissingReason.MalformedReply)]
    public void REQ03_AFailedRequestIsMissingWithNoNumberAtAll(PollFailure failure, MissingReason reason)
    {
        PanelMonitor monitor = new(Config());
        monitor.Record(Good(1, T0, T0));
        monitor.Update(T0);
        monitor.Record(Bad(failure, T0.AddSeconds(2)));
        PanelUpdate update = monitor.Update(T0.AddSeconds(2));

        Assert.All(update.Sensors, s =>
        {
            Assert.Equal(SensorState.Missing, s.State);
            Assert.Equal(reason, s.Missing);
            Assert.Null(s.LiveValue);
            Assert.Null(s.LastKnownValue);
        });
        Assert.Equal(ConnectionState.Lost, update.Connection.State);
    }

    [Fact]
    public void REQ03_MissingShowsNoNumberAnywhereOnTheTiles()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0, oven: 212.4));
        clock.Advance(TimeSpan.FromSeconds(3));
        panel.ReceiveResult(Bad(PollFailure.ServiceDown, clock.UtcNow));

        Assert.Equal("NO CONNECTION", panel.ConnectionTitle);
        Assert.All(panel.Tiles, t =>
        {
            Assert.Equal("NO DATA", t.StateText);
            Assert.Equal(SensorTileViewModel.NoValueText, t.ValueText);
            Assert.DoesNotMatch("[0-9]", t.ValueText + t.LastKnownText + t.Explanation);
        });
    }

    [Fact]
    public void REQ03_ADroppedSensorIsMissingAndTheOthersStayLive()
    {
        PanelMonitor monitor = new(Config());
        monitor.Record(Good(1, T0, T0, vibration: null));
        PanelUpdate update = monitor.Update(T0);

        SensorStatus vibration = update.Sensors.First(s => s.SensorId == "press-vibration");
        Assert.Equal(SensorState.Missing, vibration.State);
        Assert.Equal(MissingReason.SensorFailed, vibration.Missing);
        Assert.Equal(SensorState.Normal, OvenOf(update).State);
        Assert.Equal(ConnectionState.Connected, update.Connection.State);
    }

    [Fact]
    public void REQ04_TheAlarmBannerStaysUpThroughADisconnect()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0, oven: OvenTooHot));
        clock.Advance(TimeSpan.FromSeconds(2));
        panel.ReceiveResult(Bad(PollFailure.Timeout, clock.UtcNow));

        SensorTileViewModel oven = Tile(panel, "oven-temp");
        Assert.Equal("NO DATA", oven.StateText);
        Assert.Equal("UNACKNOWLEDGED ALARM", oven.AlarmBannerText);
        Assert.True(oven.CanAcknowledge);
    }

    [Fact]
    public void REQ04_AnAlarmSurvivesStaleThenMissingThenRecovery()
    {
        PanelMonitor monitor = new(Config());
        monitor.Record(Good(1, T0, T0, oven: OvenTooHot));
        Assert.Equal(AlarmLatchState.ActiveUnacked, OvenOf(monitor.Update(T0)).Latch);

        monitor.Record(Good(1, T0, T0.AddSeconds(10)));
        Assert.Equal(AlarmLatchState.ActiveUnacked, OvenOf(monitor.Update(T0.AddSeconds(10))).Latch);

        monitor.Record(Bad(PollFailure.ServiceDown, T0.AddSeconds(20)));
        Assert.Equal(AlarmLatchState.ActiveUnacked, OvenOf(monitor.Update(T0.AddSeconds(20))).Latch);

        monitor.Record(Good(2, T0.AddSeconds(30), T0.AddSeconds(30), oven: 212.0));
        PanelUpdate back = monitor.Update(T0.AddSeconds(30));
        Assert.Equal(SensorState.Normal, OvenOf(back).State);
        Assert.Equal(AlarmLatchState.ReturnedUnacked, OvenOf(back).Latch);
    }

    [Fact]
    public void REQ04_NoLongRunOfStaleOrMissingEverClearsAnAlarm()
    {
        foreach (AlarmLatchState start in Enum.GetValues<AlarmLatchState>())
        {
            AlarmLatchState state = start;
            for (int i = 0; i < 50; i++)
            {
                state = AlarmLatch.Next(state, i % 2 == 0 ? SensorState.Stale : SensorState.Missing);
            }

            Assert.Equal(start, state);
        }
    }

    [Fact]
    public void REQ05_FreshDataTurnsStaleWithNoNewReplyAtAll()
    {
        PanelMonitor monitor = new(Config());
        monitor.Record(Good(1, T0, T0));
        Assert.Equal(SensorState.Normal, OvenOf(monitor.Update(T0.AddSeconds(5))).State);
        Assert.Equal(SensorState.Stale, OvenOf(monitor.Update(T0.AddSeconds(5.5))).State);
    }

    [Fact]
    public void REQ05_StaleBySequenceEvenWhenThePiStampsEachReplyWithNow()
    {
        PanelMonitor monitor = new(Config());
        for (int second = 0; second <= 7; second++)
        {
            monitor.Record(Good(50, T0.AddSeconds(second), T0.AddSeconds(second)));
        }

        SensorStatus oven = OvenOf(monitor.Update(T0.AddSeconds(7)));
        Assert.Equal(SensorState.Stale, oven.State);
        Assert.Equal(StaleReason.SequenceNotAdvancing, oven.Stale);
    }

    [Fact]
    public void REQ07_TheButtonOnlyOpensTheConfirmation()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0, oven: OvenTooHot));
        SensorTileViewModel oven = Tile(panel, "oven-temp");

        oven.AcknowledgeCommand.Execute(null);

        Assert.True(panel.IsConfirmOpen);
        Assert.Same(oven, panel.PendingAcknowledge);
        Assert.Equal(AlarmLatchState.ActiveUnacked, oven.Latch);
        Assert.Contains("does not change anything on the machine", panel.ConfirmText);
    }

    [Fact]
    public void REQ07_CancelChangesNothing()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0, oven: OvenTooHot));
        SensorTileViewModel oven = Tile(panel, "oven-temp");
        oven.AcknowledgeCommand.Execute(null);

        panel.CancelAcknowledgeCommand.Execute(null);

        Assert.False(panel.IsConfirmOpen);
        Assert.Equal(AlarmLatchState.ActiveUnacked, oven.Latch);
        Assert.False(panel.ConfirmAcknowledgeCommand.CanExecute(null));
    }

    [Fact]
    public void REQ07_ConfirmAcknowledgesButTheAlarmStaysUntilALiveNormalValue()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0, oven: OvenTooHot));
        SensorTileViewModel oven = Tile(panel, "oven-temp");
        oven.AcknowledgeCommand.Execute(null);

        panel.ConfirmAcknowledgeCommand.Execute(null);

        Assert.False(panel.IsConfirmOpen);
        Assert.Equal("ACKNOWLEDGED, NOT CLEARED", oven.AlarmBannerText);
        Assert.Contains("alarm acknowledged, still active", panel.Events[0]);

        clock.Advance(TimeSpan.FromSeconds(1));
        panel.ReceiveResult(Good(2, clock.UtcNow, clock.UtcNow, oven: 212.0));
        Assert.False(oven.HasAlarmBanner);
    }

    [Fact]
    public void REQ07_TheButtonDoesNothingWhenThereIsNothingToAcknowledge()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0));
        panel.RequestAcknowledge(Tile(panel, "oven-temp"));
        Assert.False(panel.IsConfirmOpen);
    }

    [Fact]
    public void REQ08_TheStatusLineNamesWhatThePanelCannotVouchFor()
    {
        PanelViewModel panel = NewPanel();
        panel.ReceiveResult(Good(1, T0, T0, vibration: null));
        Assert.StartsWith("The panel cannot vouch for: Press vibration.", panel.StatusLine);
        Assert.EndsWith("Check it at the machine.", panel.StatusLine);

        panel.ReceiveResult(Good(2, T0, T0));
        Assert.Equal("Every sensor is reporting live data.", panel.StatusLine);
    }

    [Fact]
    public void REQ13_EveryLimitHasAReasonYourTeamWrote()
    {
        PanelConfig config = ShippedConfig();
        Assert.All(config.Sensors, t => Assert.False(
            t.Reason.StartsWith("REPLACE THIS", StringComparison.Ordinal),
            $"{t.Id} still has the placeholder reason in thresholds.json"));
    }

    [Fact]
    public void REQ13_TheSimulatorsNormalRunningIsInsideYourLimits()
    {
        // The simulator's normal mode wanders within these values. Limits that
        // alarm on normal running teach operators to ignore alarms.
        PanelConfig config = ShippedConfig();
        (string Id, double Lowest, double Highest)[] normal =
        {
            ("oven-temp", 211.0, 213.0),
            ("press-vibration", 2.8, 3.4),
            ("coolant-level", 67.6, 68.4),
        };
        foreach ((string id, double lowest, double highest) in normal)
        {
            SensorThreshold t = config.Sensors.Single(s => s.Id == id);
            Assert.Equal(LimitCheck.Within, t.Check(lowest));
            Assert.Equal(LimitCheck.Within, t.Check(highest));
        }
    }

    [Fact]
    public void REQ13_AValueOnALimitIsInsideAndOneStepPastIsOutside()
    {
        foreach (SensorThreshold t in ShippedConfig().Sensors)
        {
            double step = Math.Pow(10, -t.Decimals);
            if (t.Low is double low)
            {
                Assert.Equal(LimitCheck.Within, t.Check(low));
                Assert.Equal(LimitCheck.BelowLow, t.Check(Math.Round(low - step, 6)));
            }

            if (t.High is double high)
            {
                Assert.Equal(LimitCheck.Within, t.Check(high));
                Assert.Equal(LimitCheck.AboveHigh, t.Check(Math.Round(high + step, 6)));
            }
        }
    }

    [Fact]
    public void REQ14_APiRestartWithALowerSequenceCountsAsNew()
    {
        PanelMonitor monitor = new(Config());
        monitor.Record(Good(900, T0, T0));
        monitor.Record(Good(1, T0.AddSeconds(4), T0.AddSeconds(4)));
        Assert.Equal(SensorState.Normal, OvenOf(monitor.Update(T0.AddSeconds(8))).State);
    }

    [Fact]
    public void REQ15_ClockDisagreementIsStaleWithAnHonestExplanation()
    {
        PanelMonitor monitor = new(Config());
        monitor.Record(Good(9, T0.AddMinutes(10), T0));
        PanelUpdate update = monitor.Update(T0);
        Assert.Equal(StaleReason.ClockDisagrees, OvenOf(update).Stale);
        Assert.Contains("clock", OvenOf(update).Explanation);
    }

    [Fact]
    public void REQ16_TheEventLogKeepsOnlyTheNewestEntries()
    {
        PanelViewModel panel = NewPanel();
        for (int i = 0; i < 10; i++)
        {
            clock.Advance(TimeSpan.FromSeconds(1));
            panel.ReceiveResult(i % 2 == 0
                ? Good(i, clock.UtcNow, clock.UtcNow)
                : Bad(PollFailure.ServiceDown, clock.UtcNow));
        }

        Assert.Equal(PanelViewModel.EventLogLength, panel.Events.Count);
        Assert.StartsWith("14:03:32  Connection lost", panel.Events[0]);
    }
}

[Collection("network")]
public class ClientRequirementTests
{
    [Fact]
    public async Task REQ06_ASlowServiceIsATimeoutThatEndsOnTime()
    {
        using FakeSensorService fake = new() { Body = Json(1, T0), Delay = TimeSpan.FromSeconds(5) };
        using SensorClient client = new(fake.BaseUrl, TimeSpan.FromSeconds(0.5), SystemClock.Instance);

        Stopwatch timer = Stopwatch.StartNew();
        PollResult result = await client.PollAsync();

        Assert.Equal(PollFailure.Timeout, result.Failure);
        Assert.InRange(timer.Elapsed.TotalSeconds, 0.4, 2.0);
    }

    [Fact]
    public async Task REQ09_PollAsyncReturnsControlBeforeTheReplyArrives()
    {
        using FakeSensorService fake = new() { Body = Json(1, T0), Delay = TimeSpan.FromMilliseconds(800) };
        using SensorClient client = new(fake.BaseUrl, TimeSpan.FromSeconds(3), SystemClock.Instance);

        Stopwatch timer = Stopwatch.StartNew();
        Task<PollResult> pending = client.PollAsync();
        TimeSpan handedBack = timer.Elapsed;

        Assert.False(pending.IsCompleted);
        Assert.True(handedBack < TimeSpan.FromMilliseconds(300), $"PollAsync held the caller for {handedBack.TotalMilliseconds} ms");
        Assert.True((await pending).Ok);
    }

    [Fact]
    public async Task REQ12_ThePanelOnlyEverSendsGetApiReadings()
    {
        using FakeSensorService fake = new() { Body = Json(1, T0) };
        using SensorClient client = new(fake.BaseUrl, TimeSpan.FromSeconds(2), SystemClock.Instance);

        await client.PollAsync();

        Assert.Equal("/api/readings", fake.LastPath);
        Assert.Equal("GET", fake.LastMethod);
    }
}
