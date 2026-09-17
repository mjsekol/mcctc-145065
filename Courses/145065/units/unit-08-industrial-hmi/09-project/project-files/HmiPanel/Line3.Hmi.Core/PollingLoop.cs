// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/PollingLoop.cs.
// Given to you. Read it; you do not need to change it.
//
// PollingLoop.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// Ask, report, wait, repeat, until cancelled.
//
// Start RunAsync from the UI thread and do not call ConfigureAwait(false)
// here. Each await then resumes on the UI thread, so onResult runs where it
// is allowed to touch the view model, and the waiting in between happens on
// no thread at all. The HTTP work inside SensorClient does use
// ConfigureAwait(false), because nothing there touches the window.

namespace Line3.Hmi.Core;

public sealed class PollingLoop
{
    private readonly Func<CancellationToken, Task<PollResult>> poll;
    private readonly Action<PollResult> onResult;

    public PollingLoop(Func<CancellationToken, Task<PollResult>> poll, TimeSpan interval, Action<PollResult> onResult)
    {
        if (interval <= TimeSpan.Zero)
        {
            throw new ArgumentOutOfRangeException(nameof(interval), "interval must be positive");
        }

        this.poll = poll;
        this.onResult = onResult;
        Interval = interval;
    }

    public TimeSpan Interval { get; }

    /// <summary>How many polls have finished. For tests and the status bar.</summary>
    public int Completed { get; private set; }

    /// <summary>Runs until <paramref name="cancel"/> is cancelled. Completes without throwing.</summary>
    public async Task RunAsync(CancellationToken cancel)
    {
        System.Diagnostics.Stopwatch timer = new();
        while (!cancel.IsCancellationRequested)
        {
            timer.Restart();
            PollResult result;
            try
            {
                result = await poll(cancel);
            }
            catch (OperationCanceledException) when (cancel.IsCancellationRequested)
            {
                return;
            }

            Completed++;
            onResult(result);

            // Start to start, not end to start: a slow reply shortens the wait
            // instead of stretching the whole cycle.
            TimeSpan wait = Interval - timer.Elapsed;
            if (wait > TimeSpan.Zero)
            {
                try
                {
                    await Task.Delay(wait, cancel);
                }
                catch (OperationCanceledException)
                {
                    return;
                }
            }
        }
    }
}
