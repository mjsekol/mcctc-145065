// TallyViewModelTests.cs  .  145065 Unit 7  .  Lab U07-03 self-check, part 1
//
// Adapted from the course's HMI anchor
// (anchor-project/hmi/panel/w13_wpf_basics/ShiftTally.Tests/TallyViewModelTests.cs).
//
// These tests never open a window. That is the point of a view model: the
// logic behind the screen is an ordinary class, so it can be tested like one.
//
// Run from the lab folder:   dotnet test
// The class LogicTests is Monday's work (steps 1 to 6).
// The class NotificationTests is Wednesday's work (steps 13 to 18).

using System.ComponentModel;
using ShiftTally.Core;

namespace ShiftTally.Core.Tests;

public class LogicTests
{
    [Fact]
    public void StartsEmpty()
    {
        TallyViewModel tally = new();
        Assert.Equal((0, 0, 0), (tally.Good, tally.Scrap, tally.Total));
        Assert.Equal("Scrap rate: no parts yet", tally.ScrapRateText);
        Assert.Equal(0.0, tally.Progress);
        Assert.Equal("0 of 200 good parts", tally.ProgressText);
        Assert.False(tally.CanUndo);
        Assert.Equal("Press 2: Hinge bracket", tally.Heading);
    }

    [Fact]
    public void GoodAndScrapEachCountOne()
    {
        TallyViewModel tally = new();
        tally.AddGood();
        tally.AddGood();
        tally.AddScrap();
        Assert.Equal((2, 1, 3), (tally.Good, tally.Scrap, tally.Total));
        Assert.True(tally.CanUndo);
    }

    [Fact]
    public void ScrapRateUsesFloatingPointDivision()
    {
        TallyViewModel tally = new();
        for (int i = 0; i < 7; i++)
        {
            tally.AddGood();
        }

        tally.AddScrap();
        // 1 of 8 is 12.5 percent. Integer division would give 0.
        Assert.Equal("Scrap rate: 12.5 %", tally.ScrapRateText);
    }

    [Fact]
    public void UndoTakesBackTheLastKindCounted()
    {
        TallyViewModel tally = new();
        tally.AddGood();
        tally.AddScrap();
        tally.Undo();
        Assert.Equal((1, 0), (tally.Good, tally.Scrap));
        tally.Undo();
        Assert.Equal((0, 0), (tally.Good, tally.Scrap));
        tally.Undo();   // nothing left: no change, no crash
        Assert.Equal((0, 0), (tally.Good, tally.Scrap));
        Assert.False(tally.CanUndo);
    }

    [Theory]
    [InlineData(10, 50)]
    [InlineData(50, 50)]
    [InlineData(250, 250)]
    [InlineData(9000, 500)]
    public void TheTargetStaysInRange(int asked, int expected)
    {
        TallyViewModel tally = new() { Target = asked };
        Assert.Equal(expected, tally.Target);
    }

    [Fact]
    public void ProgressCountsGoodPartsAndStopsAtOneHundred()
    {
        TallyViewModel tally = new() { Target = 50 };
        for (int i = 0; i < 25; i++)
        {
            tally.AddGood();
            tally.AddScrap();
        }

        Assert.Equal(50.0, tally.Progress);
        Assert.Equal("25 of 50 good parts", tally.ProgressText);
        for (int i = 0; i < 40; i++)
        {
            tally.AddGood();
        }

        Assert.Equal(100.0, tally.Progress);
    }

    [Fact]
    public void ResetClearsCountsAndHistory()
    {
        TallyViewModel tally = new();
        tally.AddGood();
        tally.AddScrap();
        tally.Reset();
        Assert.Equal(0, tally.Total);
        Assert.False(tally.CanUndo);
    }

    [Theory]
    [InlineData("  Press 4  ", "Press 4", true)]
    [InlineData("", "", false)]
    [InlineData("   ", "", false)]
    public void TheStationNameIsTrimmedForDisplayAndChecked(string typed, string shown, bool valid)
    {
        TallyViewModel tally = new() { Station = typed };
        Assert.Equal(typed, tally.Station);
        Assert.Equal(shown, tally.StationName);
        Assert.Equal(valid, tally.StationIsValid);
        Assert.StartsWith(valid ? shown : "(name the station)", tally.Heading);
    }

    [Fact]
    public void TheQuestionAndTheSummarySayWhatIsTrueNow()
    {
        TallyViewModel tally = new() { Station = " Press 4 ", PartType = "Cover plate", Target = 100 };
        tally.AddGood();
        tally.AddGood();
        tally.AddScrap();
        Assert.Equal("Reset 3 counted parts to zero? This cannot be undone.", tally.ResetQuestion);
        Assert.Equal("Press 4 | Cover plate | good 2 | scrap 1 | target 100", tally.SummaryText);
    }

    [Fact]
    public void TheStatusLineSaysWhatJustHappened()
    {
        TallyViewModel tally = new();
        Assert.Equal("Count each part as it leaves the station.", tally.Status);
        tally.AddGood();
        Assert.Equal("Counted one good part.", tally.Status);
        tally.AddScrap();
        Assert.Equal("Counted one scrap part. Tag it before it goes in the bin.", tally.Status);
        tally.Undo();
        Assert.Equal("Took back the last count.", tally.Status);
        tally.Reset();
        Assert.Equal("Counts reset.", tally.Status);
    }
}

public class NotificationTests
{
    /// <summary>Subscribes to PropertyChanged and records every name announced.</summary>
    private static List<string?> Listen(TallyViewModel tally)
    {
        INotifyPropertyChanged? notifier = (object)tally as INotifyPropertyChanged;
        Assert.True(notifier is not null,
            "TallyViewModel does not implement INotifyPropertyChanged yet, so no binding can hear it change (step 13).");
        List<string?> heard = new();
        notifier!.PropertyChanged += (_, e) => heard.Add(e.PropertyName);
        return heard;
    }

    private static void AssertAnnounced(List<string?> heard, params string[] names)
    {
        foreach (string name in names)
        {
            Assert.True(heard.Contains(name),
                $"{name} changed but was never announced. A control bound to it keeps showing the old value. " +
                $"Announced: {string.Join(", ", heard)}");
        }
    }

    [Fact]
    public void ItAnnouncesItsChanges()
    {
        TallyViewModel tally = new();
        List<string?> heard = Listen(tally);
        tally.AddGood();
        Assert.NotEmpty(heard);
    }

    [Fact]
    public void AGoodPartAnnouncesEveryPropertyComputedFromTheCounts()
    {
        TallyViewModel tally = new();
        List<string?> heard = Listen(tally);
        tally.AddGood();
        AssertAnnounced(heard, "Good", "Total", "Progress", "ProgressText", "ScrapRateText", "CanUndo", "Status");
    }

    [Fact]
    public void AScrapPartAnnouncesEveryPropertyComputedFromTheCounts()
    {
        TallyViewModel tally = new();
        List<string?> heard = Listen(tally);
        tally.AddScrap();
        AssertAnnounced(heard, "Scrap", "Total", "Progress", "ProgressText", "ScrapRateText", "CanUndo", "Status");
    }

    [Fact]
    public void UndoAndResetAnnounceTheCountsAndCanUndo()
    {
        TallyViewModel tally = new();
        tally.AddGood();
        tally.AddScrap();
        List<string?> heard = Listen(tally);
        tally.Undo();
        AssertAnnounced(heard, "Scrap", "Total", "CanUndo", "Status");
        heard.Clear();
        tally.Reset();
        AssertAnnounced(heard, "Good", "Total", "CanUndo", "Status");
    }

    [Fact]
    public void TheTargetAnnouncesTheProgress()
    {
        TallyViewModel tally = new();
        List<string?> heard = Listen(tally);
        tally.Target = 300;
        AssertAnnounced(heard, "Target", "Progress", "ProgressText");
    }

    [Fact]
    public void TheStationAndPartAnnounceTheHeading()
    {
        TallyViewModel tally = new();
        List<string?> heard = Listen(tally);
        tally.Station = "Press 4";
        AssertAnnounced(heard, "Station", "StationName", "Heading");
        heard.Clear();
        tally.PartType = "Cover plate";
        AssertAnnounced(heard, "PartType", "Heading");
    }

    [Fact]
    public void TheCheckBoxPropertyAnnouncesItself()
    {
        TallyViewModel tally = new();
        List<string?> heard = Listen(tally);
        tally.ShowScrapRate = false;
        AssertAnnounced(heard, "ShowScrapRate");
    }

    [Fact]
    public void SettingTheSameValueAnnouncesNothing()
    {
        // Announcing a change that did not happen makes every bound control
        // redraw for nothing, and a two-way binding can bounce forever.
        TallyViewModel tally = new();
        List<string?> heard = Listen(tally);
        tally.Target = 200;
        tally.Station = "Press 2";
        tally.ShowScrapRate = true;
        Assert.Empty(heard);
    }
}
