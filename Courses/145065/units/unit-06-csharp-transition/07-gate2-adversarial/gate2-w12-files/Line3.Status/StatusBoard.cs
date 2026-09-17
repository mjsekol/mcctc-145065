namespace Line3.Status;

/// <summary>
/// The Line 3 status board: one line per reporter, and the most urgent
/// level on the board.
/// </summary>
public sealed class StatusBoard
{
    private readonly List<IStatusReporter> _reporters = new();

    /// <summary>Adds a reporter. Tags must be unique on the board.</summary>
    public void Add(IStatusReporter reporter)
    {
        ArgumentNullException.ThrowIfNull(reporter);
        if (_reporters.Any(existing => existing.Tag == reporter.Tag))
        {
            throw new ArgumentException($"{reporter.Tag} is already on the board", nameof(reporter));
        }
        _reporters.Add(reporter);
    }

    /// <summary>
    /// The reporters on the board, in the order they were added. Returns a
    /// copy, so callers cannot change the board's own list.
    /// </summary>
    public IReadOnlyList<IStatusReporter> Reporters => _reporters.ToList();

    /// <summary>The most urgent level on the board. Normal when the board is empty.</summary>
    public StatusLevel Worst()
    {
        StatusLevel worst = StatusLevel.Normal;
        for (int i = 0; i < Reporters.Count; i++)
        {
            if (Reporters[i].Level > worst)
            {
                worst = Reporters[i].Level;
            }
        }
        return worst;
    }

    /// <summary>
    /// One display line per reporter: tag, level, and a short description.
    /// Works for any IStatusReporter.
    /// </summary>
    public IReadOnlyList<string> Lines()
    {
        var lines = new List<string>();
        for (int i = 0; i < Reporters.Count; i++)
        {
            IStatusReporter reporter = Reporters[i];
            string detail = reporter switch
            {
                TemperatureProbe probe => probe.ReadingC is double t ? $"{t:F1} C" : "no reading",
                GuardSwitch guard => guard.IsClosed switch
                {
                    true => "guard closed",
                    false => "guard OPEN",
                    null => "no signal",
                },
                _ => "unknown device",
            };
            lines.Add($"{reporter.Tag,-12} {reporter.Level,-8} {detail}");
        }
        return lines;
    }

    /// <summary>Returns every reporter to its power-on state, for the start of a shift.</summary>
    public void ResetAll()
    {
        foreach (IStatusReporter reporter in _reporters)
        {
            reporter.Reset();
        }
    }
}
