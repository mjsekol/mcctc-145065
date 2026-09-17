// MainWindow.xaml.cs
// ScrapTag: counts rejected parts at the Line 3 scrap bench by reason and
// prints a tag for the bin at the end of the shift.

using System.Windows;

namespace ScrapTag;

public partial class MainWindow : Window
{
    // Shift lead code required to clear the counts.
    private const string LeadCode = "4417";

    private readonly LabelPrinter printer = new();
    private int burr;
    private int bent;
    private int wrongHole;

    public MainWindow()
    {
        InitializeComponent();
        UpdateDisplay();
    }

    public LabelPrinter Printer => printer;

    // +1 BURR
    private void Button_Click(object sender, RoutedEventArgs e)
    {
        burr++;
        UpdateDisplay();
    }

    // +1 WRONG HOLE
    private void Button_Click_1(object sender, RoutedEventArgs e)
    {
        bent++;
        UpdateDisplay();
    }

    // +1 BENT
    private void Button_Click_2(object sender, RoutedEventArgs e)
    {
        wrongHole++;
        UpdateDisplay();
    }

    // Validates the station, prints the tag, and confirms to the operator.
    private void PrintButton_Click(object sender, RoutedEventArgs e)
    {
        if (string.IsNullOrEmpty(StationBox.Text))
        {
            StatusText.Text = "Enter a station name before printing.";
            return;
        }

        StatusText.Text = "Printing tag...";
        printer.Print(BuildTag());
        StatusText.Text = "Tag printed.";
    }

    // Clears the shift's counts once the shift lead's code is confirmed.
    private void ClearButton_Click(object sender, RoutedEventArgs e)
    {
        if (LeadCodeBox.Password != LeadCode)
        {
            StatusText.Text = "Lead code not accepted.";
            LeadCodeBox.Clear();
            return;
        }

        burr = 0;
        bent = 0;
        wrongHole = 0;
        LeadCodeBox.Clear();
        ArmReasonButtons();
        UpdateDisplay();
        StatusText.Text = "Counts cleared for the next shift.";
    }

    // Makes sure each reason button is connected to its handler for the new shift.
    private void ArmReasonButtons()
    {
        BurrButton.Click += Button_Click;
        BentButton.Click += Button_Click_1;
        WrongHoleButton.Click += Button_Click_2;
    }

    private string BuildTag() =>
        $"SCRAP | {StationBox.Text} | burr {burr} | bent {bent} | wrong hole {wrongHole} | total {burr + bent + wrongHole}";

    private void UpdateDisplay()
    {
        BurrText.Text = $"Burr: {burr}";
        BentText.Text = $"Bent: {bent}";
        WrongHoleText.Text = $"Wrong hole: {wrongHole}";
        TotalText.Text = $"Total: {burr + bent + wrongHole}";
    }
}
