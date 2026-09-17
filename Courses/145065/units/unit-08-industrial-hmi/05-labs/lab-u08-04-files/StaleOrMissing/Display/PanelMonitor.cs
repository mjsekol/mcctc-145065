// PanelMonitor.cs  .  Lab U08-04  .  given to you, trimmed
//
// Two pieces of the HMI anchor's PanelMonitor.cs, copied unchanged: the
// SensorStatus record the tile reads, and FormatAge, which turns an age into
// the words an operator reads. The full PanelMonitor ships in the HMI PANEL
// project.

using System.Globalization;

namespace Line3.Hmi.Core;

/// <summary>Everything the panel shows for one sensor at one moment.</summary>
public sealed record SensorStatus(
    SensorThreshold Threshold,
    SensorState State,
    double? LiveValue,
    double? LastKnownValue,
    TimeSpan? LastKnownAge,
    AlarmSide Side,
    MissingReason Missing,
    StaleReason Stale,
    AlarmLatchState Latch,
    string Explanation)
{
    public string SensorId => Threshold.Id;
}

public sealed class PanelMonitor
{
    private PanelMonitor()
    {
    }

    /// <summary>"0.4 s", "12 s", "3 min 05 s", "2 h 07 min".</summary>
    public static string FormatAge(TimeSpan age)
    {
        if (age < TimeSpan.Zero)
        {
            age = TimeSpan.Zero;
        }

        if (age < TimeSpan.FromSeconds(10))
        {
            return age.TotalSeconds.ToString("0.0", CultureInfo.InvariantCulture) + " s";
        }

        if (age < TimeSpan.FromMinutes(1))
        {
            return ((int)age.TotalSeconds).ToString(CultureInfo.InvariantCulture) + " s";
        }

        if (age < TimeSpan.FromHours(1))
        {
            return $"{(int)age.TotalMinutes} min {age.Seconds:00} s";
        }

        return $"{(int)age.TotalHours} h {age.Minutes:00} min";
    }
}
