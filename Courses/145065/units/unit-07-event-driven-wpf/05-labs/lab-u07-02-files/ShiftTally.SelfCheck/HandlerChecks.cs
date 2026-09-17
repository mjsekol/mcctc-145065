// HandlerChecks.cs  .  145065 Unit 7  .  Lab U07-02 self-check
//
// Run from the lab folder:   dotnet test
// Every check builds your real MainWindow, presses its buttons the way WPF
// does (by raising their Click event), and reads what the window shows.
// No window appears on the screen, and no dialog appears either: the checks
// replace Confirm with their own answer.

using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using Xunit.Abstractions;

namespace ShiftTally.SelfCheck;

public class HandlerChecks
{
    private readonly ITestOutputHelper output;

    public HandlerChecks(ITestOutputHelper output) => this.output = output;

    private static Button Button(Window w, string name) => WpfTestHost.Find<Button>(w, name);

    private static string Text(Window w, string name) => WpfTestHost.Find<TextBlock>(w, name).Text;

    private static void Press(Window w, string name, int times = 1)
    {
        for (int i = 0; i < times; i++)
        {
            WpfTestHost.Click(Button(w, name));
        }
    }

    [Fact]
    public void GoodAddsOneAndShowsIt()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton");
            Assert.Equal("Good: 1", Text(w, "GoodText"));
            Assert.Equal("Total: 1", Text(w, "TotalText"));
            Assert.Equal("Counted one good part.", Text(w, "StatusText"));
        });
    }

    [Fact]
    public void ScrapAddsOneAndShowsIt()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "ScrapButton");
            Assert.Equal("Scrap: 1", Text(w, "ScrapText"));
            Assert.Equal("Total: 1", Text(w, "TotalText"));
            Assert.StartsWith("Counted one scrap part.", Text(w, "StatusText"));
        });
    }

    [Fact]
    public void EachPressCountsExactlyOnce()
    {
        // A handler attached twice (in the XAML and again with +=) runs twice per press.
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton", 3);
            Press(w, "ScrapButton", 2);
            Assert.Equal(("Good: 3", "Scrap: 2", "Total: 5"),
                (Text(w, "GoodText"), Text(w, "ScrapText"), Text(w, "TotalText")));
        });
    }

    [Fact]
    public void UndoIsEnabledOnlyWhenThereIsSomethingToUndo()
    {
        WpfTestHost.Run(w =>
        {
            Assert.False(Button(w, "UndoButton").IsEnabled, "UNDO LAST should be disabled before any count.");
            Press(w, "GoodButton");
            Assert.True(Button(w, "UndoButton").IsEnabled, "UNDO LAST should be enabled after a count.");
            Press(w, "UndoButton");
            Assert.False(Button(w, "UndoButton").IsEnabled, "UNDO LAST should be disabled again when nothing is left.");
        });
    }

    [Fact]
    public void UndoTakesBackTheLastKindCounted()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton");
            Press(w, "ScrapButton");
            Press(w, "GoodButton");
            Press(w, "UndoButton");
            Assert.Equal(("Good: 1", "Scrap: 1"), (Text(w, "GoodText"), Text(w, "ScrapText")));
            Press(w, "UndoButton");
            Assert.Equal(("Good: 1", "Scrap: 0"), (Text(w, "GoodText"), Text(w, "ScrapText")));
            Assert.Equal("Took back the last count.", Text(w, "StatusText"));
        });
    }

    [Fact]
    public void ResetAsksFirstAndKeepsTheCountsOnNo()
    {
        WpfTestHost.Run(w =>
        {
            string? asked = null;
            w.Confirm = question =>
            {
                asked = question;
                return false;
            };
            Press(w, "GoodButton", 2);
            Press(w, "ScrapButton");
            Press(w, "ResetButton");
            Assert.True(asked is not null, "RESET SHIFT must call Confirm before it resets anything.");
            Assert.Contains("3", asked);
            Assert.Equal("Total: 3", Text(w, "TotalText"));
            Assert.True(Button(w, "UndoButton").IsEnabled, "A cancelled reset keeps the history, so UNDO stays on.");
        });
    }

    [Fact]
    public void ResetClearsEverythingOnYes()
    {
        WpfTestHost.Run(w =>
        {
            w.Confirm = _ => true;
            Press(w, "GoodButton", 2);
            Press(w, "ScrapButton");
            Press(w, "ResetButton");
            Assert.Equal(("Good: 0", "Scrap: 0", "Total: 0"),
                (Text(w, "GoodText"), Text(w, "ScrapText"), Text(w, "TotalText")));
            Assert.Equal("Scrap rate: no parts yet", Text(w, "RateText"));
            Assert.False(Button(w, "UndoButton").IsEnabled, "After a reset there is nothing to undo.");
            Assert.Equal("Counts reset.", Text(w, "StatusText"));
        });
    }

    [Fact]
    public void ScrapRateUsesFloatingPointDivision()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton", 7);
            Press(w, "ScrapButton");
            // 1 of 8 is 12.5 percent. Integer division gives 0.
            Assert.Equal("Scrap rate: 12.5 %", Text(w, "RateText"));
        });
    }

    [Fact]
    public void TheCheckBoxHidesAndShowsTheScrapRate()
    {
        WpfTestHost.Run(w =>
        {
            CheckBox box = WpfTestHost.Find<CheckBox>(w, "ShowRateBox");
            TextBlock rate = WpfTestHost.Find<TextBlock>(w, "RateText");
            box.IsChecked = false;
            Assert.Equal(Visibility.Collapsed, rate.Visibility);
            box.IsChecked = true;
            Assert.Equal(Visibility.Visible, rate.Visibility);
        });
    }

    [Fact]
    public void TheSliderChangesTheTargetAndTheProgress()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton", 25);
            WpfTestHost.Find<Slider>(w, "TargetSlider").Value = 100;
            Assert.Equal("Shift target: 100", Text(w, "TargetText"));
            Assert.Equal("25 of 100 good parts", Text(w, "ProgressText"));
            Assert.Equal(25.0, WpfTestHost.Find<ProgressBar>(w, "ShiftProgress").Value, 3);
        });
    }

    [Fact]
    public void ProgressCountsGoodPartsOnlyAndStopsAtOneHundred()
    {
        WpfTestHost.Run(w =>
        {
            WpfTestHost.Find<Slider>(w, "TargetSlider").Value = 50;
            Press(w, "ScrapButton", 10);
            Assert.Equal(0.0, WpfTestHost.Find<ProgressBar>(w, "ShiftProgress").Value, 3);
            Press(w, "GoodButton", 60);
            Assert.Equal(100.0, WpfTestHost.Find<ProgressBar>(w, "ShiftProgress").Value, 3);
            Assert.Equal("60 of 50 good parts", Text(w, "ProgressText"));
        });
    }

    [Theory]
    [InlineData("Press 4", "Press 4: Hinge bracket")]
    [InlineData("  Press 4  ", "Press 4: Hinge bracket")]
    [InlineData("   ", "(name the station): Hinge bracket")]
    public void TypingAStationNameChangesTheHeading(string typed, string heading)
    {
        WpfTestHost.Run(w =>
        {
            WpfTestHost.Find<TextBox>(w, "StationBox").Text = typed;
            Assert.Equal(heading, Text(w, "HeadingText"));
        });
    }

    [Fact]
    public void PickingAPartChangesTheHeading()
    {
        WpfTestHost.Run(w =>
        {
            WpfTestHost.Find<ComboBox>(w, "PartBox").SelectedIndex = 2;
            Assert.Equal("Press 2: Cover plate", Text(w, "HeadingText"));
        });
    }

    [Fact]
    public void PrintingDoesNotFreezeTheWindow()
    {
        WpfTestHost.Run(w =>
        {
            w.Printer.Delay = TimeSpan.FromSeconds(1);
            Stopwatch clock = Stopwatch.StartNew();
            Press(w, "PrintButton");
            clock.Stop();
            output.WriteLine($"The PRINT handler gave the window back after {clock.ElapsedMilliseconds} ms.");

            Assert.True(clock.ElapsedMilliseconds < 500,
                $"The PRINT handler held the UI thread for {clock.ElapsedMilliseconds} ms. " +
                "While it waits, no button works. Await PrintAsync instead of calling Print.");
            Assert.False(Button(w, "PrintButton").IsEnabled, "Disable PRINT SUMMARY while a label prints.");
            Assert.Equal("Printing the shift summary...", Text(w, "StatusText"));

            // The window still works while the label prints.
            Press(w, "GoodButton");
            Assert.Equal("Good: 1", Text(w, "GoodText"));
        });
    }

    [Fact]
    public void PrintingFinishesAndTurnsTheButtonBackOn()
    {
        WpfTestHost.Run(w =>
        {
            w.Printer.Delay = TimeSpan.FromMilliseconds(300);
            Press(w, "GoodButton", 2);
            Press(w, "PrintButton");
            bool finished = WpfTestHost.PumpUntil(() => Text(w, "StatusText") == "Summary printed.", TimeSpan.FromSeconds(5));
            Assert.True(finished, $"The status never said 'Summary printed.' It says '{Text(w, "StatusText")}'.");
            Assert.True(Button(w, "PrintButton").IsEnabled, "Turn PRINT SUMMARY back on when the label is done.");
            string label = Assert.Single(w.Printer.Printed);
            Assert.Contains("good 2", label);
        });
    }

    [Fact]
    public void SavesAPictureOfYourWindow()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton", 37);
            Press(w, "ScrapButton", 3);
            WpfTestHost.Find<Slider>(w, "TargetSlider").Value = 150;
            string path = WpfTestHost.SavePicture(w, "ShiftTally-U07-02.png");
            output.WriteLine($"Picture saved: {path}");
            Assert.True(new System.IO.FileInfo(path).Length > 0);
        });
    }
}
