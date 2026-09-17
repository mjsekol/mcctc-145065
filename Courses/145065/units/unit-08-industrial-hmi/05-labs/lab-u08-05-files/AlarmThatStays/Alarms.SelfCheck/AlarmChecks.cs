// AlarmChecks.cs  .  Lab U08-05 self-check  .  given to you
//
// Your AlarmLatch against the six rules, and your three acknowledge methods
// against the two-step promise.

using Line3.Hmi.Core;
using Line3.Hmi.Core.ViewModels;

namespace Alarms.SelfCheck;

public class LatchChecks
{
    [Theory]
    [InlineData(AlarmLatchState.Clear, SensorState.Normal, AlarmLatchState.Clear)]
    [InlineData(AlarmLatchState.Clear, SensorState.Alarm, AlarmLatchState.ActiveUnacked)]
    [InlineData(AlarmLatchState.ActiveUnacked, SensorState.Alarm, AlarmLatchState.ActiveUnacked)]
    [InlineData(AlarmLatchState.ActiveAcked, SensorState.Alarm, AlarmLatchState.ActiveAcked)]
    [InlineData(AlarmLatchState.ReturnedUnacked, SensorState.Alarm, AlarmLatchState.ActiveUnacked)]
    public void A01_Rule1_ALiveValueOutOfLimitsMakesTheAlarmActive(AlarmLatchState current, SensorState seen, AlarmLatchState expected) =>
        Assert.Equal(expected, AlarmLatch.Next(current, seen));

    [Theory]
    [InlineData(AlarmLatchState.ActiveUnacked, AlarmLatchState.ReturnedUnacked)]
    [InlineData(AlarmLatchState.ActiveAcked, AlarmLatchState.Clear)]
    [InlineData(AlarmLatchState.ReturnedUnacked, AlarmLatchState.ReturnedUnacked)]
    public void A02_Rule2_ALiveValueBackInsideEndsAnActiveAlarm(AlarmLatchState current, AlarmLatchState expected) =>
        Assert.Equal(expected, AlarmLatch.Next(current, SensorState.Normal));

    [Fact]
    public void A03_Rule3_StaleOrMissingChangesNothingFromAnyState()
    {
        foreach (AlarmLatchState start in Enum.GetValues<AlarmLatchState>())
        {
            Assert.Equal(start, AlarmLatch.Next(start, SensorState.Stale));
            Assert.Equal(start, AlarmLatch.Next(start, SensorState.Missing));
        }
    }

    [Fact]
    public void A04_Rule3_NoLongRunOfStaleAndMissingEverClearsAnAlarm()
    {
        AlarmLatchState state = AlarmLatch.Next(AlarmLatchState.Clear, SensorState.Alarm);
        for (int i = 0; i < 50; i++)
        {
            state = AlarmLatch.Next(state, i % 3 == 0 ? SensorState.Stale : SensorState.Missing);
        }

        Assert.Equal(AlarmLatchState.ActiveUnacked, state);
    }

    [Theory]
    [InlineData(AlarmLatchState.ActiveUnacked, AlarmLatchState.ActiveAcked)]
    [InlineData(AlarmLatchState.ReturnedUnacked, AlarmLatchState.Clear)]
    [InlineData(AlarmLatchState.ActiveAcked, AlarmLatchState.ActiveAcked)]
    [InlineData(AlarmLatchState.Clear, AlarmLatchState.Clear)]
    public void A05_Rules4To6_Acknowledge(AlarmLatchState current, AlarmLatchState expected) =>
        Assert.Equal(expected, AlarmLatch.Acknowledge(current));
}

public class AcknowledgeChecks
{
    private static AlarmBoard NewBoard() => new(new[]
    {
        ("oven-temp", "Cure oven temperature"),
        ("coolant-level", "Coolant level"),
    });

    [Fact]
    public void K01_TheButtonOnlyOpensTheQuestion()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Alarm);
        AlarmTile oven = board.TileOf("oven-temp");

        oven.AcknowledgeCommand.Execute(null);

        Assert.True(board.IsConfirmOpen);
        Assert.Same(oven, board.PendingAcknowledge);
        Assert.Equal(AlarmLatchState.ActiveUnacked, board.LatchOf("oven-temp"));
        Assert.Contains("Cure oven temperature", board.ConfirmText);
        Assert.Contains("does not change anything on the machine", board.ConfirmText);
    }

    [Fact]
    public void K02_CancelClosesTheQuestionAndChangesNothing()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Alarm);
        board.TileOf("oven-temp").AcknowledgeCommand.Execute(null);
        int logged = board.Log.Count;

        board.CancelAcknowledgeCommand.Execute(null);

        Assert.False(board.IsConfirmOpen);
        Assert.Equal(AlarmLatchState.ActiveUnacked, board.LatchOf("oven-temp"));
        Assert.Equal("UNACKNOWLEDGED ALARM", board.TileOf("oven-temp").BannerText);
        Assert.Equal(logged, board.Log.Count);
    }

    [Fact]
    public void K03_YesAcknowledgesAndTheAlarmStaysUntilALiveNormalValue()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Alarm);
        board.TileOf("oven-temp").AcknowledgeCommand.Execute(null);

        board.ConfirmAcknowledgeCommand.Execute(null);

        Assert.False(board.IsConfirmOpen);
        Assert.Equal(AlarmLatchState.ActiveAcked, board.LatchOf("oven-temp"));
        Assert.Equal("ACKNOWLEDGED, NOT CLEARED", board.TileOf("oven-temp").BannerText);

        board.Observe("oven-temp", SensorState.Missing);
        Assert.Equal("ACKNOWLEDGED, NOT CLEARED", board.TileOf("oven-temp").BannerText);

        board.Observe("oven-temp", SensorState.Normal);
        Assert.Equal(AlarmLatchState.Clear, board.LatchOf("oven-temp"));
        Assert.Equal(string.Empty, board.TileOf("oven-temp").BannerText);
    }

    [Fact]
    public void K04_AnAlarmThatEndedIsClearedByAcknowledging()
    {
        AlarmBoard board = NewBoard();
        board.Observe("coolant-level", SensorState.Alarm);
        board.Observe("coolant-level", SensorState.Normal);
        Assert.Equal("ALARM ENDED, NOT ACKNOWLEDGED", board.TileOf("coolant-level").BannerText);

        board.TileOf("coolant-level").AcknowledgeCommand.Execute(null);
        Assert.Contains("removes the alarm", board.ConfirmText);
        board.ConfirmAcknowledgeCommand.Execute(null);

        Assert.Equal(AlarmLatchState.Clear, board.LatchOf("coolant-level"));
        Assert.False(board.TileOf("coolant-level").CanAcknowledge);
    }

    [Fact]
    public void K05_TheButtonDoesNothingWhenThereIsNothingToAcknowledge()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Normal);

        board.RequestAcknowledge(board.TileOf("oven-temp"));

        Assert.False(board.IsConfirmOpen);
        Assert.Null(board.PendingAcknowledge);
    }

    [Fact]
    public void K06_YesWithNothingPendingChangesNothing()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Alarm);

        board.ConfirmAcknowledge();

        Assert.Equal(AlarmLatchState.ActiveUnacked, board.LatchOf("oven-temp"));
    }

    [Fact]
    public void K07_AcknowledgingOneSensorLeavesTheOtherAlone()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Alarm);
        board.Observe("coolant-level", SensorState.Alarm);
        board.TileOf("oven-temp").AcknowledgeCommand.Execute(null);
        board.ConfirmAcknowledgeCommand.Execute(null);

        Assert.Equal(AlarmLatchState.ActiveAcked, board.LatchOf("oven-temp"));
        Assert.Equal(AlarmLatchState.ActiveUnacked, board.LatchOf("coolant-level"));
    }

    [Fact]
    public void K08_TheAcknowledgementIsRecordedInTheLog()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Alarm);
        int logged = board.Log.Count;
        board.TileOf("oven-temp").AcknowledgeCommand.Execute(null);
        board.ConfirmAcknowledgeCommand.Execute(null);

        Assert.Equal(logged + 1, board.Log.Count);
        Assert.Contains("Cure oven temperature", board.Log[^1]);
    }

    [Fact]
    public void K09_TheBannerSurvivesADisconnect()
    {
        AlarmBoard board = NewBoard();
        board.Observe("oven-temp", SensorState.Alarm);
        board.Observe("oven-temp", SensorState.Stale);
        board.Observe("oven-temp", SensorState.Missing);

        Assert.Equal(SensorState.Missing, board.TileOf("oven-temp").State);
        Assert.Equal("UNACKNOWLEDGED ALARM", board.TileOf("oven-temp").BannerText);
        Assert.True(board.TileOf("oven-temp").CanAcknowledge);
    }
}
