// LayoutChecks.cs  .  145065 Unit 7  .  Lab U07-01 self-check
//
// Run from the lab folder:   dotnet test
// Every check builds your real MainWindow, lays it out at 900 by 600, and
// looks at it. None of them opens a window on the screen.
//
// A failing check's message says what to fix. Read it before you change code.

using System.Windows;
using System.Windows.Controls;
using Xunit.Abstractions;

namespace ShiftTally.SelfCheck;

public class LayoutChecks
{
    private readonly ITestOutputHelper output;

    public LayoutChecks(ITestOutputHelper output) => this.output = output;

    public static TheoryData<string, string> RequiredControls => new()
    {
        { "HeadingText", "TextBlock" },
        { "StationBox", "TextBox" },
        { "PartBox", "ComboBox" },
        { "GoodButton", "Button" },
        { "ScrapButton", "Button" },
        { "UndoButton", "Button" },
        { "ResetButton", "Button" },
        { "GoodText", "TextBlock" },
        { "ScrapText", "TextBlock" },
        { "TotalText", "TextBlock" },
        { "TargetText", "TextBlock" },
        { "TargetSlider", "Slider" },
        { "ShiftProgress", "ProgressBar" },
        { "ProgressText", "TextBlock" },
        { "ShowRateBox", "CheckBox" },
        { "RateText", "TextBlock" },
        { "PrintButton", "Button" },
        { "StatusText", "TextBlock" },
    };

    private static readonly string[] ButtonNames =
        { "GoodButton", "ScrapButton", "UndoButton", "ResetButton", "PrintButton" };

    [Theory]
    [MemberData(nameof(RequiredControls))]
    public void EveryNamedControlExists(string name, string kind)
    {
        WpfTestHost.Run(window =>
        {
            object? found = window.FindName(name);
            Assert.True(found is not null, $"No control named {name}. Check the x:Name in MainWindow.xaml.");
            Assert.True(found!.GetType().Name == kind,
                $"{name} is a {found.GetType().Name}, but the lab asks for a {kind}.");
        });
    }

    [Fact]
    public void TheButtonsSayWhatTheyDo()
    {
        WpfTestHost.Run(window =>
        {
            Assert.Equal("+1 GOOD", WpfTestHost.Find<Button>(window, "GoodButton").Content);
            Assert.Equal("+1 SCRAP", WpfTestHost.Find<Button>(window, "ScrapButton").Content);
            Assert.Equal("UNDO LAST", WpfTestHost.Find<Button>(window, "UndoButton").Content);
            Assert.Equal("RESET SHIFT", WpfTestHost.Find<Button>(window, "ResetButton").Content);
            Assert.Equal("PRINT SUMMARY", WpfTestHost.Find<Button>(window, "PrintButton").Content);
        });
    }

    [Fact]
    public void UndoStartsDisabledAndTheOthersStartEnabled()
    {
        WpfTestHost.Run(window =>
        {
            Assert.False(WpfTestHost.Find<Button>(window, "UndoButton").IsEnabled,
                "UndoButton should start disabled: there is nothing to undo yet.");
            foreach (string name in new[] { "GoodButton", "ScrapButton", "ResetButton", "PrintButton" })
            {
                Assert.True(WpfTestHost.Find<Button>(window, name).IsEnabled, $"{name} should start enabled.");
            }
        });
    }

    [Fact]
    public void EveryButtonIsTallEnoughForAGlovedFinger()
    {
        WpfTestHost.Run(window =>
        {
            foreach (string name in ButtonNames)
            {
                Button button = WpfTestHost.Find<Button>(window, name);
                Assert.True(button.ActualHeight >= 64,
                    $"{name} is {button.ActualHeight:0} pixels tall. The shop's rule is at least 64.");
            }
        });
    }

    [Fact]
    public void TheCountsStartAtZero()
    {
        WpfTestHost.Run(window =>
        {
            Assert.Equal("Good: 0", WpfTestHost.Find<TextBlock>(window, "GoodText").Text);
            Assert.Equal("Scrap: 0", WpfTestHost.Find<TextBlock>(window, "ScrapText").Text);
            Assert.Equal("Total: 0", WpfTestHost.Find<TextBlock>(window, "TotalText").Text);
        });
    }

    [Fact]
    public void TheSliderFollowsTheShiftRules()
    {
        WpfTestHost.Run(window =>
        {
            Slider slider = WpfTestHost.Find<Slider>(window, "TargetSlider");
            Assert.Equal(50, slider.Minimum);
            Assert.Equal(500, slider.Maximum);
            Assert.Equal(200, slider.Value);
            Assert.Equal(50, slider.TickFrequency);
            Assert.True(slider.IsSnapToTickEnabled, "TargetSlider should snap to its ticks.");
            Assert.Equal("Shift target: 200", WpfTestHost.Find<TextBlock>(window, "TargetText").Text);
        });
    }

    [Fact]
    public void ProgressAndScrapRateStartEmpty()
    {
        WpfTestHost.Run(window =>
        {
            ProgressBar bar = WpfTestHost.Find<ProgressBar>(window, "ShiftProgress");
            Assert.Equal((0.0, 100.0, 0.0), (bar.Minimum, bar.Maximum, bar.Value));
            Assert.Equal("0 of 200 good parts", WpfTestHost.Find<TextBlock>(window, "ProgressText").Text);
            Assert.True(WpfTestHost.Find<CheckBox>(window, "ShowRateBox").IsChecked,
                "ShowRateBox should start checked.");
            Assert.Equal("Scrap rate: no parts yet", WpfTestHost.Find<TextBlock>(window, "RateText").Text);
        });
    }

    [Fact]
    public void TheFourCountingButtonsShareOneRowAtEqualWidths()
    {
        WpfTestHost.Run(window =>
        {
            string[] names = { "GoodButton", "ScrapButton", "UndoButton", "ResetButton" };
            Rect[] boxes = names.Select(n => WpfTestHost.BoundsOf(window, WpfTestHost.Find<Button>(window, n))).ToArray();
            for (int i = 1; i < boxes.Length; i++)
            {
                Assert.True(Math.Abs(boxes[i].Top - boxes[0].Top) < 1,
                    $"{names[i]} is not in the same row as GoodButton.");
                Assert.True(boxes[i].Left > boxes[i - 1].Left,
                    $"{names[i]} should sit to the right of {names[i - 1]}.");
                Assert.True(Math.Abs(boxes[i].Width - boxes[0].Width) < 1,
                    $"{names[i]} is {boxes[i].Width:0} wide and GoodButton is {boxes[0].Width:0}. A UniformGrid makes them equal.");
            }
        });
    }

    [Fact]
    public void TheRowsRunTopToBottomWithoutOverlapping()
    {
        WpfTestHost.Run(window =>
        {
            string[] order = { "StationBox", "GoodButton", "GoodText", "TargetSlider", "ShiftProgress", "RateText", "PrintButton" };
            for (int i = 1; i < order.Length; i++)
            {
                Rect above = WpfTestHost.BoundsOf(window, WpfTestHost.Find<FrameworkElement>(window, order[i - 1]));
                Rect below = WpfTestHost.BoundsOf(window, WpfTestHost.Find<FrameworkElement>(window, order[i]));
                Assert.True(below.Top >= above.Bottom - 0.5,
                    $"{order[i]} starts at y={below.Top:0}, above the bottom of {order[i - 1]} (y={above.Bottom:0}). Check its Grid.Row.");
            }
        });
    }

    [Fact]
    public void NothingFallsOffTheWindow()
    {
        WpfTestHost.Run(window =>
        {
            foreach (object[] row in RequiredControls)
            {
                string name = (string)row[0];
                FrameworkElement element = WpfTestHost.Find<FrameworkElement>(window, name);
                Rect box = WpfTestHost.BoundsOf(window, element);
                Assert.True(box.Width > 0 && box.Height > 0, $"{name} has no size. Is it inside a row that exists?");
                Assert.True(box.Left >= 0 && box.Top >= 0 && box.Right <= WpfTestHost.Width + 0.5
                            && box.Bottom <= WpfTestHost.Height + 0.5,
                    $"{name} runs off the 900 by 600 window: {box}.");
            }
        });
    }

    [Fact]
    public void SavesAPictureOfYourWindow()
    {
        WpfTestHost.Run(window =>
        {
            string path = WpfTestHost.SavePicture(window, "ShiftTally-U07-01.png");
            output.WriteLine($"Picture saved: {path}");
            Assert.True(new System.IO.FileInfo(path).Length > 0);
        });
    }
}
