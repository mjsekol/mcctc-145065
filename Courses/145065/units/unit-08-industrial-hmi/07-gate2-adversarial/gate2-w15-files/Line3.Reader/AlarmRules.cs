namespace Line3.Reader;

public enum AlarmState
{
    Normal,
    AlarmLow,
    AlarmHigh,
    NoData,
}

/// <summary>Decides what the panel shows for one sensor.</summary>
public static class AlarmRules
{
    /// <summary>
    /// Compares a reading with its documented limits. Limits are inclusive: a value
    /// exactly on a limit is inside, as limits.json specifies.
    /// </summary>
    public static AlarmState Evaluate(SensorReading reading, SensorLimit? limit)
    {
        // A sensor with no documented limit is not judged.
        if (limit is null)
        {
            return AlarmState.NoData;
        }

        if (limit.Low is double low && reading.Value < low)
        {
            return AlarmState.AlarmLow;
        }

        if (limit.High is double high && reading.Value > high)
        {
            return AlarmState.AlarmHigh;
        }

        return AlarmState.Normal;
    }
}
