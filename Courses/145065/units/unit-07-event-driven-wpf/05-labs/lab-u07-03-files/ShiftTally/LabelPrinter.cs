// LabelPrinter.cs  .  145065 Unit 7  .  ShiftTally
//
// A SIMULATED label printer. There is no printer and no hardware. Printing a
// real label takes a few seconds, so this class waits for Delay to pass and
// then records the text it "printed".
//
// It offers two ways to print, on purpose:
//   Print       makes the calling thread wait. Call it from a click handler
//               and the whole window stops responding until it finishes.
//   PrintAsync  hands back an unfinished Task at once. Await it from a click
//               handler and the window keeps working while the label prints.
//
// Do not change this file. Lab U07-02 step 12 uses both methods.

namespace ShiftTally;

public sealed class LabelPrinter
{
    /// <summary>How long one label takes. The self-check shortens it.</summary>
    public TimeSpan Delay { get; set; } = TimeSpan.FromSeconds(3);

    /// <summary>For the EXTENDED option: when true, the next print fails after the delay.</summary>
    public bool OutOfLabels { get; set; }

    /// <summary>Every label printed so far, oldest first.</summary>
    public List<string> Printed { get; } = new();

    /// <summary>Prints by making the calling thread wait. Blocks the window if called from a handler.</summary>
    public void Print(string text)
    {
        Thread.Sleep(Delay);
        Finish(text);
    }

    /// <summary>Prints without making anyone wait. Await it.</summary>
    public async Task PrintAsync(string text)
    {
        await Task.Delay(Delay);
        Finish(text);
    }

    private void Finish(string text)
    {
        if (OutOfLabels)
        {
            throw new InvalidOperationException("The label printer is out of labels.");
        }

        Printed.Add(text);
    }
}
