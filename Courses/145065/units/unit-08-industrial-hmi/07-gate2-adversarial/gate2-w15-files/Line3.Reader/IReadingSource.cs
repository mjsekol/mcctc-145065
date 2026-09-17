namespace Line3.Reader;

/// <summary>
/// Anything that can produce Line 3 readings. The panel depends on this interface,
/// not on HTTP, so tests can swap in a fake source.
/// </summary>
public interface IReadingSource
{
    /// <summary>How long a single read may take before it is abandoned.</summary>
    TimeSpan Timeout { get; }

    /// <summary>Reads the latest batch. Never throws for network problems.</summary>
    Task<ReadResult> ReadAsync(CancellationToken cancel = default);
}
