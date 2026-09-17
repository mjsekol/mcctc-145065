namespace Line3.Reader;

/// <summary>Reads from a source on a schedule and reports every result.</summary>
public sealed class Poller
{
    // Poll four times a second. The Pi samples once a second, but polling faster
    // means a pulled cable shows up on the panel sooner.
    public static readonly TimeSpan FastPollInterval = TimeSpan.FromMilliseconds(250);

    private readonly IReadingSource source;
    private readonly Action<ReadResult> onResult;

    public Poller(IReadingSource source, Action<ReadResult> onResult)
    {
        this.source = source;
        this.onResult = onResult;
    }

    public int Completed { get; private set; }

    /// <summary>Runs until cancelled. Ends without throwing.</summary>
    public async Task RunAsync(CancellationToken cancel)
    {
        while (!cancel.IsCancellationRequested)
        {
            ReadResult result;
            try
            {
                result = await source.ReadAsync(cancel);
            }
            catch (OperationCanceledException)
            {
                return;
            }

            Completed++;
            onResult(result);

            try
            {
                await Task.Delay(FastPollInterval, cancel);
            }
            catch (OperationCanceledException)
            {
                return;
            }
        }
    }
}
