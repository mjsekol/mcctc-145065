// BindingChecks.cs  .  145065 Unit 7  .  Lab U07-03 self-check, part 2
//
// Run from the lab folder:   dotnet test
// These checks open your real MainWindow on a test thread.
// The class BindingChecks is Tuesday's work (steps 7 to 12).
// The class LiveScreenChecks is Wednesday's work (steps 13 to 18).

using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using ShiftTally.Core;
using Xunit.Abstractions;

namespace ShiftTally.SelfCheck;

public class BindingChecks
{
    public static TheoryData<string, string> BoundProperties => new()
    {
        { "HeadingText", "Text" },
        { "StationBox", "Text" },
        { "PartBox", "SelectedItem" },
        { "UndoButton", "IsEnabled" },
        { "GoodText", "Text" },
        { "ScrapText", "Text" },
        { "TotalText", "Text" },
        { "TargetText", "Text" },
        { "TargetSlider", "Value" },
        { "ShiftProgress", "Value" },
        { "ProgressText", "Text" },
        { "ShowRateBox", "IsChecked" },
        { "RateText", "Text" },
        { "RateText", "Visibility" },
        { "StatusText", "Text" },
    };

    private static DependencyProperty PropertyOf(FrameworkElement element, string name) => name switch
    {
        "Text" when element is TextBlock => TextBlock.TextProperty,
        "Text" when element is TextBox => TextBox.TextProperty,
        "SelectedItem" => Selector.SelectedItemProperty,
        "IsEnabled" => UIElement.IsEnabledProperty,
        "Value" => RangeBase.ValueProperty,
        "IsChecked" => ToggleButton.IsCheckedProperty,
        "Visibility" => UIElement.VisibilityProperty,
        _ => throw new ArgumentException($"The check does not know {element.GetType().Name}.{name}."),
    };

    [Fact]
    public void TheWindowShowsItsOwnViewModel()
    {
        WpfTestHost.Run(w =>
        {
            Assert.True(w.DataContext is TallyViewModel,
                "The window's DataContext is not a TallyViewModel. Set DataContext = Tally after InitializeComponent.");
            Assert.Same(w.Tally, w.DataContext);
        });
    }

    [Theory]
    [MemberData(nameof(BoundProperties))]
    public void EveryDisplayedValueIsBound(string name, string property)
    {
        WpfTestHost.Run(w =>
        {
            FrameworkElement element = WpfTestHost.Find<FrameworkElement>(w, name);
            bool bound = BindingOperations.IsDataBound(element, PropertyOf(element, property));

            // EXTENDED option: a button bound to a command is enabled by the
            // command's CanExecute, which counts as bound.
            if (!bound && element is Button && property == "IsEnabled")
            {
                bound = BindingOperations.IsDataBound(element, ButtonBase.CommandProperty);
            }

            Assert.True(bound,
                $"{name}.{property} is not bound. Give it a {{Binding}} to a TallyViewModel property.");
        });
    }

    [Fact]
    public void NoBindingPathIsMisspelled()
    {
        // A misspelled path does not stop the build. WPF writes an error to
        // the debug output and shows nothing. This check listens for it.
        List<string> errors = new();
        TraceListener listener = new CollectingListener(errors);
        PresentationTraceSources.Refresh();
        PresentationTraceSources.DataBindingSource.Listeners.Add(listener);
        PresentationTraceSources.DataBindingSource.Switch.Level = SourceLevels.Warning;
        try
        {
            WpfTestHost.Run(w => WpfTestHost.LayOut(w));
        }
        finally
        {
            PresentationTraceSources.DataBindingSource.Listeners.Remove(listener);
        }

        Assert.True(errors.Count == 0, "WPF reported binding errors:\n" + string.Join("\n", errors));
    }

    [Fact]
    public void TheScreenStartsWithTheViewModelsValues()
    {
        WpfTestHost.Run(w =>
        {
            Assert.Equal("Press 2: Hinge bracket", WpfTestHost.Find<TextBlock>(w, "HeadingText").Text);
            Assert.Equal("Press 2", WpfTestHost.Find<TextBox>(w, "StationBox").Text);
            Assert.Equal("Hinge bracket", WpfTestHost.Find<ComboBox>(w, "PartBox").SelectedItem);
            Assert.Equal("Good: 0", WpfTestHost.Find<TextBlock>(w, "GoodText").Text);
            Assert.Equal("Total: 0", WpfTestHost.Find<TextBlock>(w, "TotalText").Text);
            Assert.Equal("Shift target: 200", WpfTestHost.Find<TextBlock>(w, "TargetText").Text);
            Assert.Equal(200, WpfTestHost.Find<Slider>(w, "TargetSlider").Value);
            Assert.Equal("0 of 200 good parts", WpfTestHost.Find<TextBlock>(w, "ProgressText").Text);
            Assert.Equal("Scrap rate: no parts yet", WpfTestHost.Find<TextBlock>(w, "RateText").Text);
            Assert.False(WpfTestHost.Find<Button>(w, "UndoButton").IsEnabled);
        });
    }

    [Fact]
    public void TheSliderWritesBackToTheViewModel()
    {
        WpfTestHost.Run(w =>
        {
            WpfTestHost.Find<Slider>(w, "TargetSlider").Value = 300;
            Assert.Equal(300, w.Tally.Target);
        });
    }

    [Fact]
    public void TypingWritesBackOnEveryKeystroke()
    {
        WpfTestHost.Run(w =>
        {
            // Without UpdateSourceTrigger=PropertyChanged, a TextBox writes
            // back only when it loses focus, and the heading lags behind.
            WpfTestHost.Find<TextBox>(w, "StationBox").Text = "Press 4";
            Assert.Equal("Press 4", w.Tally.Station);
        });
    }

    [Fact]
    public void ThePartListComesFromTheViewModel()
    {
        WpfTestHost.Run(w =>
        {
            ComboBox parts = WpfTestHost.Find<ComboBox>(w, "PartBox");
            Assert.Same(w.Tally.PartTypes, parts.ItemsSource);
            parts.SelectedIndex = 2;
            Assert.Equal("Cover plate", w.Tally.PartType);
        });
    }

    private sealed class CollectingListener : TraceListener
    {
        private readonly List<string> lines;

        public CollectingListener(List<string> lines) => this.lines = lines;

        public override void Write(string? message)
        {
        }

        public override void WriteLine(string? message)
        {
            if (message is not null)
            {
                lines.Add(message);
            }
        }
    }
}

public class LiveScreenChecks
{
    private readonly ITestOutputHelper output;

    public LiveScreenChecks(ITestOutputHelper output) => this.output = output;

    private static string Text(Window w, string name) => WpfTestHost.Find<TextBlock>(w, name).Text;

    private static void Press(Window w, string name, int times = 1)
    {
        for (int i = 0; i < times; i++)
        {
            WpfTestHost.Click(WpfTestHost.Find<Button>(w, name));
        }
    }

    [Fact]
    public void PressingAButtonUpdatesTheScreen()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton", 2);
            Press(w, "ScrapButton");
            Assert.Equal(("Good: 2", "Scrap: 1", "Total: 3"),
                (Text(w, "GoodText"), Text(w, "ScrapText"), Text(w, "TotalText")));
            Assert.Equal("Scrap rate: 33.3 %", Text(w, "RateText"));
            Assert.Equal("Counted one scrap part. Tag it before it goes in the bin.", Text(w, "StatusText"));
            Assert.True(WpfTestHost.Find<Button>(w, "UndoButton").IsEnabled,
                "UNDO LAST stayed disabled. Is CanUndo announced when a count changes?");
        });
    }

    [Fact]
    public void EachPressCountsExactlyOnce()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "GoodButton");
            Assert.Equal(1, w.Tally.Good);
        });
    }

    [Fact]
    public void UndoUpdatesTheScreenAndTurnsItselfOff()
    {
        WpfTestHost.Run(w =>
        {
            Press(w, "ScrapButton");
            Press(w, "UndoButton");
            Assert.Equal("Scrap: 0", Text(w, "ScrapText"));
            Assert.False(WpfTestHost.Find<Button>(w, "UndoButton").IsEnabled);
        });
    }

    [Fact]
    public void TheHeadingFollowsTheStationBox()
    {
        WpfTestHost.Run(w =>
        {
            WpfTestHost.Find<TextBox>(w, "StationBox").Text = "Press 4";
            Assert.Equal("Press 4: Hinge bracket", Text(w, "HeadingText"));
            WpfTestHost.Find<TextBox>(w, "StationBox").Text = "   ";
            Assert.Equal("(name the station): Hinge bracket", Text(w, "HeadingText"));
        });
    }

    [Fact]
    public void ProgressFollowsTheSlider()
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
    public void TheCheckBoxHidesTheScrapRate()
    {
        WpfTestHost.Run(w =>
        {
            WpfTestHost.Find<CheckBox>(w, "ShowRateBox").IsChecked = false;
            Assert.Equal(Visibility.Collapsed, WpfTestHost.Find<TextBlock>(w, "RateText").Visibility);
        });
    }

    [Fact]
    public void ResetStillAsksFirst()
    {
        WpfTestHost.Run(w =>
        {
            string? asked = null;
            w.Confirm = q =>
            {
                asked = q;
                return false;
            };
            Press(w, "GoodButton", 3);
            Press(w, "ResetButton");
            Assert.Equal("Reset 3 counted parts to zero? This cannot be undone.", asked);
            Assert.Equal("Total: 3", Text(w, "TotalText"));

            w.Confirm = _ => true;
            Press(w, "ResetButton");
            Assert.Equal("Total: 0", Text(w, "TotalText"));
            Assert.Equal("Counts reset.", Text(w, "StatusText"));
        });
    }

    [Fact]
    public void PrintingStillKeepsTheWindowWorking()
    {
        WpfTestHost.Run(w =>
        {
            w.Printer.Delay = TimeSpan.FromMilliseconds(300);
            Stopwatch clock = Stopwatch.StartNew();
            Press(w, "PrintButton");
            clock.Stop();
            Assert.True(clock.ElapsedMilliseconds < 200,
                $"The PRINT handler held the UI thread for {clock.ElapsedMilliseconds} ms.");
            bool done = WpfTestHost.PumpUntil(() => Text(w, "StatusText") == "Summary printed.", TimeSpan.FromSeconds(5));
            Assert.True(done, $"The status says '{Text(w, "StatusText")}'.");
            Assert.True(WpfTestHost.Find<Button>(w, "PrintButton").IsEnabled);
        });
    }

    [Fact]
    public void SavesAPictureOfYourWindow()
    {
        WpfTestHost.Run(w =>
        {
            for (int i = 0; i < 37; i++)
            {
                w.Tally.AddGood();
            }

            for (int i = 0; i < 3; i++)
            {
                w.Tally.AddScrap();
            }

            w.Tally.Target = 150;
            string path = WpfTestHost.SavePicture(w, "ShiftTally-U07-03.png");
            output.WriteLine($"Picture saved: {path}");
            Assert.True(new System.IO.FileInfo(path).Length > 0);
        });
    }
}
