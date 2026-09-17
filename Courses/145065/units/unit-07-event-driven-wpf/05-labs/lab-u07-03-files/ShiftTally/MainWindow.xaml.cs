// MainWindow.xaml.cs  .  145065 Unit 7  .  ShiftTally
//
// Lab U07-03 STARTER. This is the Lab U07-02 solution with one addition:
// the window now owns a TallyViewModel, in the Tally property below.
//
// Monday (step 5): the handlers stop counting in fields and call Tally.
// Tuesday (steps 7 to 12): bindings replace ShowCounts and ShowHeading.
// By Wednesday this file is about a third of its current length.

using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using ShiftTally.Core;

namespace ShiftTally;

public partial class MainWindow : Window
{
    private readonly LabelPrinter printer = new();

    // WPF raises ValueChanged, TextChanged, SelectionChanged, and Checked while
    // InitializeComponent is still building the window. This flag stops those
    // early calls from touching controls that do not exist yet.
    private readonly bool windowBuilt;

    // The shift's state. It lives on the window this week. Week 14 moves it
    // into a view model, because a window is hard to test and easy to tangle.
    private readonly Stack<bool> history = new();   // true = a good part, false = scrap
    private int good;
    private int scrap;
    private int target = 200;

    public MainWindow()
    {
        InitializeComponent();
        Confirm = AskYesNo;
        windowBuilt = true;
        ShowCounts();
        ShowHeading();
    }

    /// <summary>
    /// Everything the window shows, once the lab is done. The self-check reads
    /// it. Step 5 moves the counting into it.
    /// </summary>
    public TallyViewModel Tally { get; } = new();

    /// <summary>The yes-or-no question RESET asks. Tests replace it.</summary>
    public Func<string, bool> Confirm { get; set; }

    /// <summary>The simulated printer, so the self-check can shorten its delay.</summary>
    public LabelPrinter Printer => printer;

    // ---- Click handlers ----------------------------------------------------

    private void OnGoodClick(object sender, RoutedEventArgs e)
    {
        good++;
        history.Push(true);
        ShowCounts();
        StatusText.Text = "Counted one good part.";
    }

    private void OnScrapClick(object sender, RoutedEventArgs e)
    {
        scrap++;
        history.Push(false);
        ShowCounts();
        StatusText.Text = "Counted one scrap part. Tag it before it goes in the bin.";
    }

    private void OnUndoClick(object sender, RoutedEventArgs e)
    {
        // The button is disabled when history is empty, but a handler should
        // not trust the screen. TryPop does nothing on an empty stack.
        if (!history.TryPop(out bool wasGood))
        {
            return;
        }

        if (wasGood)
        {
            good--;
        }
        else
        {
            scrap--;
        }

        ShowCounts();
        StatusText.Text = "Took back the last count.";
    }

    private void OnResetClick(object sender, RoutedEventArgs e)
    {
        // Destructive, so ask first. Confirm is AskYesNo in the running app.
        int total = good + scrap;
        if (!Confirm($"Reset {total} counted parts to zero? This cannot be undone."))
        {
            StatusText.Text = "Reset cancelled. The counts are kept.";
            return;
        }

        good = 0;
        scrap = 0;
        history.Clear();
        ShowCounts();
        StatusText.Text = "Counts reset.";
    }

    private async void OnPrintClick(object sender, RoutedEventArgs e)
    {
        // async void is allowed for event handlers and nowhere else.
        // The await hands the UI thread back to WPF while the label prints,
        // so the other buttons keep working. The button is disabled so one
        // press prints one label.
        PrintButton.IsEnabled = false;
        StatusText.Text = "Printing the shift summary...";
        await printer.PrintAsync(SummaryText());
        StatusText.Text = "Summary printed.";
        PrintButton.IsEnabled = true;
    }

    // ---- Change handlers ---------------------------------------------------

    private void OnTargetChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
    {
        // Slider values are double. The slider snaps to ticks of 50, so the
        // cast to int loses nothing.
        target = (int)e.NewValue;
        ShowCounts();
    }

    private void OnStationChanged(object sender, TextChangedEventArgs e) => ShowHeading();

    private void OnPartChanged(object sender, SelectionChangedEventArgs e) => ShowHeading();

    // One handler for both Checked and Unchecked. ShowCounts reads IsChecked.
    private void OnShowRateChanged(object sender, RoutedEventArgs e) => ShowCounts();

    // ---- Helpers -----------------------------------------------------------

    private void ShowCounts()
    {
        if (!windowBuilt)
        {
            return;
        }

        int total = good + scrap;
        GoodText.Text = $"Good: {good}";
        ScrapText.Text = $"Scrap: {scrap}";
        TotalText.Text = $"Total: {total}";
        TargetText.Text = $"Shift target: {target}";

        // 100.0 comes first so the arithmetic is floating-point. With whole
        // numbers, good / target is 0 until the target is reached.
        ShiftProgress.Value = Math.Min(100.0, 100.0 * good / target);
        ProgressText.Text = $"{good} of {target} good parts";

        RateText.Text = total == 0
            ? "Scrap rate: no parts yet"
            : string.Format(CultureInfo.InvariantCulture, "Scrap rate: {0:0.0} %", 100.0 * scrap / total);
        RateText.Visibility = ShowRateBox.IsChecked == true ? Visibility.Visible : Visibility.Collapsed;

        UndoButton.IsEnabled = history.Count > 0;
    }

    private void ShowHeading()
    {
        if (!windowBuilt)
        {
            return;
        }

        string station = StationBox.Text.Trim();
        HeadingText.Text = station.Length > 0
            ? $"{station}: {PartName()}"
            : $"(name the station): {PartName()}";
    }

    private string PartName() =>
        PartBox.SelectedItem is ComboBoxItem item ? item.Content as string ?? "" : "";

    private string SummaryText() =>
        $"{StationBox.Text.Trim()} | {PartName()} | good {good} | scrap {scrap} | target {target}";

    private bool AskYesNo(string question)
    {
        MessageBoxResult answer = MessageBox.Show(
            this,
            question,
            "Reset shift",
            MessageBoxButton.YesNo,
            MessageBoxImage.Warning,
            MessageBoxResult.No);
        return answer == MessageBoxResult.Yes;
    }
}
