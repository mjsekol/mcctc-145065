// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/Clock.cs.
// Given to you. Read it; you do not need to change it.
//
// Clock.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// Nothing in Core reads DateTimeOffset.UtcNow directly. It asks an IClock.
// That is what makes "stale after five seconds" testable in no seconds at all:
// a test hands the logic a ManualClock and moves it forward by hand.

namespace Line3.Hmi.Core;

public interface IClock
{
    DateTimeOffset UtcNow { get; }
}

/// <summary>The real clock. The panel uses this one.</summary>
public sealed class SystemClock : IClock
{
    public static readonly SystemClock Instance = new();

    public DateTimeOffset UtcNow => DateTimeOffset.UtcNow;
}

/// <summary>A clock that only moves when you move it. Tests and the screenshot harness use it.</summary>
public sealed class ManualClock : IClock
{
    private readonly object gate = new();
    private DateTimeOffset now;

    public ManualClock(DateTimeOffset start)
    {
        now = start;
    }

    public DateTimeOffset UtcNow
    {
        get
        {
            lock (gate)
            {
                return now;
            }
        }
    }

    public void Advance(TimeSpan by)
    {
        lock (gate)
        {
            now += by;
        }
    }

    public void Set(DateTimeOffset to)
    {
        lock (gate)
        {
            now = to;
        }
    }
}
