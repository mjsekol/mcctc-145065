namespace Line3.Status;

/// <summary>A temperature probe with a warning limit and a higher alarm limit.</summary>
public sealed class TemperatureProbe : IStatusReporter
{
    private double? _readingC;
    private StatusLevel? _acknowledged;

    public TemperatureProbe(string tag, double warnAtC, double alarmAtC)
    {
        if (string.IsNullOrWhiteSpace(tag))
        {
            throw new ArgumentException("a tag is required", nameof(tag));
        }
        if (!double.IsFinite(warnAtC) || !double.IsFinite(alarmAtC) || warnAtC >= alarmAtC)
        {
            throw new ArgumentException("the warning limit must be a number below the alarm limit");
        }
        Tag = tag;
        WarnAtC = warnAtC;
        AlarmAtC = alarmAtC;
    }

    public string Tag { get; }

    /// <summary>Readings at or above this limit show Warning.</summary>
    public double WarnAtC { get; }

    /// <summary>Readings at or above this limit show Alarm.</summary>
    public double AlarmAtC { get; }

    /// <summary>The latest reading, or null before the first one arrives.</summary>
    public double? ReadingC => _readingC;

    /// <summary>Records a new reading from the probe.</summary>
    public void Record(double celsius)
    {
        if (!double.IsFinite(celsius))
        {
            throw new ArgumentOutOfRangeException(nameof(celsius), celsius, "a reading must be a finite number");
        }
        _readingC = celsius;
    }

    /// <summary>
    /// Missing until the first reading. After that, the limits decide.
    /// The limits are settings rather than constants, so each arm tests
    /// them with a when clause.
    /// </summary>
    public StatusLevel Level
    {
        get => _acknowledged ?? _readingC switch
        {
            null => StatusLevel.Missing,
            double t when t >= WarnAtC => StatusLevel.Warning,
            double t when t >= AlarmAtC => StatusLevel.Alarm,
            _ => StatusLevel.Normal,
        };
        set => _acknowledged = value;
    }

    /// <summary>Clears the reading and any acknowledgement.</summary>
    public void Reset()
    {
        _readingC = null;
        _acknowledged = null;
    }
}
