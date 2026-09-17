// ExtendedChecks.cs  .  145065 Unit 7  .  Lab U07-02 EXTENDED
//
// These checks are for the EXTENDED option only. Copy this file into your
// ShiftTally.SelfCheck folder, next to HandlerChecks.cs, then run dotnet test.
// While it sits in this "extended" folder, nothing compiles it.
//
// The printer can run out of labels. When it does, PrintAsync throws
// InvalidOperationException after its delay. Your handler must survive that:
// say what went wrong, and turn PRINT SUMMARY back on.

using System.Windows.Controls;

namespace ShiftTally.SelfCheck;

public class ExtendedChecks
{
    private const string FailedMessage =
        "Print failed: The label printer is out of labels. Load labels and press PRINT SUMMARY again.";

    [Fact]
    public void AFailedPrintSaysWhyAndTurnsTheButtonBackOn()
    {
        WpfTestHost.Run(w =>
        {
            w.Printer.Delay = TimeSpan.FromMilliseconds(200);
            w.Printer.OutOfLabels = true;
            WpfTestHost.Click(WpfTestHost.Find<Button>(w, "PrintButton"));

            TextBlock status = WpfTestHost.Find<TextBlock>(w, "StatusText");
            bool done = WpfTestHost.PumpUntil(() => status.Text.StartsWith("Print failed"), TimeSpan.FromSeconds(5));

            Assert.True(done, $"The status never reported the failure. It says '{status.Text}'.");
            Assert.Equal(FailedMessage, status.Text);
            Assert.True(WpfTestHost.Find<Button>(w, "PrintButton").IsEnabled,
                "After a failed print, PRINT SUMMARY must work again.");
            Assert.Empty(w.Printer.Printed);
        });
    }

    [Fact]
    public void TheNextPrintWorksOnceLabelsAreLoaded()
    {
        WpfTestHost.Run(w =>
        {
            w.Printer.Delay = TimeSpan.FromMilliseconds(100);
            w.Printer.OutOfLabels = true;
            Button print = WpfTestHost.Find<Button>(w, "PrintButton");
            TextBlock status = WpfTestHost.Find<TextBlock>(w, "StatusText");

            WpfTestHost.Click(print);
            WpfTestHost.PumpUntil(() => status.Text.StartsWith("Print failed"), TimeSpan.FromSeconds(5));

            w.Printer.OutOfLabels = false;
            WpfTestHost.Click(print);
            bool done = WpfTestHost.PumpUntil(() => status.Text == "Summary printed.", TimeSpan.FromSeconds(5));

            Assert.True(done, $"The second print never finished. The status says '{status.Text}'.");
            Assert.Single(w.Printer.Printed);
        });
    }
}
