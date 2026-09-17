// MainWindow.xaml.cs  .  145065 Unit 7  .  ShiftTally
//
// Lab U07-02 STARTER. The window is built (Lab U07-01) and nothing responds
// yet. You write the event handlers: methods WPF calls when something happens.
// You never call a handler yourself.
//
// This week the shift's state lives in fields on the window. Next week it
// moves into a class of its own, and you will see why.

using System.Windows;

namespace ShiftTally;

public partial class MainWindow : Window
{
    private readonly LabelPrinter printer = new();

    // WPF raises some events WHILE InitializeComponent is still building the
    // window, before every control exists. A handler that touches a control
    // too early throws NullReferenceException and the app never opens.
    // This flag is false until the window is finished.
    private readonly bool windowBuilt;

    // Step 3: add the fields that hold the shift's state here.

    public MainWindow()
    {
        InitializeComponent();
        Confirm = AskYesNo;
        windowBuilt = true;
        ShowCounts();
    }

    /// <summary>
    /// The yes-or-no question the RESET handler asks. The self-check swaps in
    /// its own answer, so no dialog appears while it runs. Call Confirm, not
    /// MessageBox, from your handler.
    /// </summary>
    public Func<string, bool> Confirm { get; set; }

    /// <summary>The simulated printer, so the self-check can shorten its delay.</summary>
    public LabelPrinter Printer => printer;

    // Steps 4 to 12: write your handlers here.

    /// <summary>
    /// Writes every count onto the screen. Every handler that changes a count
    /// calls this as its last step.
    /// </summary>
    private void ShowCounts()
    {
        if (!windowBuilt)
        {
            return;   // still inside InitializeComponent: some controls do not exist yet
        }

        // Steps 4, 8, and 9: write the counts, the target, the progress, and the rate.
    }

    private bool AskYesNo(string question)
    {
        // The last argument makes No the default, so pressing Enter by
        // accident does not wipe a shift's counts.
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
