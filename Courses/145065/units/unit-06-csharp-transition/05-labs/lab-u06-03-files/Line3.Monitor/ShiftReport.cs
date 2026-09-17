// ShiftReport.cs
// Given to you. Do not change it until Part 4 (Thursday) tells you to.
// It builds today, with warnings. Part 4 is about what those warnings mean.

using System.Globalization;
using System.Text;

namespace Line3.Monitor;

/// <summary>A plain-text shift report for the shift lead.</summary>
public class ShiftReport
{
    private readonly List<Reading> _readings = new();

    public ShiftReport(string title)
    {
        if (string.IsNullOrWhiteSpace(title))
        {
            throw new ArgumentException("a report needs a title", nameof(title));
        }
    }

    public string Title { get; }

    /// <summary>An optional note from the lead. Null when there is none.</summary>
    public string? Note { get; set; }

    public void Add(Reading reading) => _readings.Add(reading);

    public string Render()
    {
        var text = new StringBuilder();
        text.AppendLine(Title.ToUpperInvariant());
        text.AppendLine("Note: " + Note.Trim());
        foreach (Reading reading in _readings)
        {
            string value = reading.Value is double v ? v.ToString("F1", CultureInfo.InvariantCulture) : "missing";
            text.AppendLine($"  #{reading.Sequence} {reading.SensorId}: {value}");
        }
        return text.ToString();
    }
}
