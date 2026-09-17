namespace Line3.Readings;

/// <summary>
/// A rolling log of readings from one sensor on Line 3, ported from the
/// Python ReadingLog class. The log keeps the newest readings, up to
/// <see cref="KeepLast"/>, and answers questions about them for the panel.
/// </summary>
/// <remarks>
/// Inheriting from List&lt;double&gt; gives the log Count, indexing, and
/// foreach support for free, so the panel can treat it like any collection.
/// </remarks>
public class ReadingLog : List<double>
{
    /// <summary>The largest log allowed: one reading per second for a full day.</summary>
    public const int MaxKeepLast = 86_400;

    /// <summary>Creates an empty log for one sensor.</summary>
    /// <param name="sensorId">The sensor this log belongs to, such as oven-temp.</param>
    /// <param name="keepLast">How many of the newest readings to keep.</param>
    public ReadingLog(string sensorId, int keepLast = 3_600)
    {
        if (string.IsNullOrWhiteSpace(sensorId))
        {
            throw new ArgumentException("a sensor id is required", nameof(sensorId));
        }
        if (keepLast < 1 || keepLast > MaxKeepLast)
        {
            throw new ArgumentOutOfRangeException(nameof(keepLast), keepLast,
                $"keepLast must be from 1 to {MaxKeepLast}");
        }
        SensorId = sensorId;
        KeepLast = keepLast;
    }

    /// <summary>The sensor this log belongs to.</summary>
    public string SensorId { get; }

    /// <summary>How many of the newest readings this log keeps.</summary>
    public int KeepLast { get; }

    /// <summary>
    /// Records one reading. Refuses NaN and infinity, so every value in the
    /// log is a real measurement. When the log is full, the oldest reading
    /// is dropped.
    /// </summary>
    public void Record(double value)
    {
        if (!double.IsFinite(value))
        {
            throw new ArgumentOutOfRangeException(nameof(value), value,
                "a reading must be a finite number");
        }
        Add(value);
        if (Count > KeepLast)
        {
            RemoveAt(0);
        }
    }

    /// <summary>
    /// The newest reading. Returns NaN when the log is empty, so callers
    /// never need a null check.
    /// </summary>
    public double Latest => Count == 0 ? double.NaN : this[Count - 1];

    /// <summary>
    /// True when the newest reading is too old to show as live. The panel
    /// uses this to grey out the value.
    /// </summary>
    public bool IsStale => Count == 0;

    /// <summary>
    /// The percent of stored readings from low to high, inclusive, rounded
    /// to one decimal place. Returns 0 for an empty log.
    /// </summary>
    public double PercentInRange(double low, double high)
    {
        if (Count == 0)
        {
            return 0;
        }

        int inRange = 0;
        foreach (double reading in this)
        {
            if (reading >= low && reading <= high)
            {
                inRange++;
            }
        }

        double percent = inRange / Count * 100;
        return Math.Round(percent, 1);
    }

    /// <summary>
    /// How many stored readings are above the average of the stored
    /// readings. A rising count is an early sign of drift.
    /// </summary>
    public int CountAboveAverage()
    {
        int above = 0;
        foreach (double reading in this)
        {
            if (reading > this.Average())
            {
                above++;
            }
        }
        return above;
    }
}
