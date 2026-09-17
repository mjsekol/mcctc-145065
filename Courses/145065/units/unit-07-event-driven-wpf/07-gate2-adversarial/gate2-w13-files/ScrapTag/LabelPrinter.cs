// LabelPrinter.cs
// Simulated bench label printer. A real tag takes about two seconds to print.

namespace ScrapTag;

public sealed class LabelPrinter
{
    public TimeSpan Delay { get; set; } = TimeSpan.FromSeconds(2);

    public List<string> Printed { get; } = new();

    /// <summary>Prints a tag. Returns when the printer has finished.</summary>
    public void Print(string text)
    {
        Thread.Sleep(Delay);
        Printed.Add(text);
    }

    /// <summary>Prints a tag without holding up the caller.</summary>
    public async Task PrintAsync(string text)
    {
        await Task.Delay(Delay);
        Printed.Add(text);
    }
}
