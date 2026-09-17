namespace Line3.Status;

/// <summary>
/// A guard interlock switch. Closed is safe. Open is an alarm. A switch the
/// panel has not heard from yet is Missing, because unknown counts as unsafe.
/// </summary>
public sealed class GuardSwitch : IStatusReporter
{
    private bool? _closed;
    private StatusLevel? _acknowledged;

    public GuardSwitch(string tag)
    {
        if (string.IsNullOrWhiteSpace(tag))
        {
            throw new ArgumentException("a tag is required", nameof(tag));
        }
        Tag = tag;
    }

    public string Tag { get; }

    /// <summary>True when closed, false when open, null before the first signal.</summary>
    public bool? IsClosed => _closed;

    /// <summary>Records the switch position the device reported.</summary>
    public void Update(bool closed) => _closed = closed;

    public StatusLevel Level
    {
        get => _acknowledged ?? _closed switch
        {
            null => StatusLevel.Missing,
            true => StatusLevel.Normal,
            false => StatusLevel.Alarm,
        };
        set => _acknowledged = value;
    }

    /// <summary>
    /// A guard switch reports a physical guard. Software cannot put the guard
    /// back, so this refuses.
    /// </summary>
    public void Reset() =>
        throw new NotSupportedException($"{Tag} is a physical switch and cannot be reset from the panel");
}
