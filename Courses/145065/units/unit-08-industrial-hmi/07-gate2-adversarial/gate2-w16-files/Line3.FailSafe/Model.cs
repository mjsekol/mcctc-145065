namespace Line3.FailSafe;

/// <summary>One sensor's documented limits. Either limit may be absent.</summary>
public sealed record SensorLimit(string Id, string Label, string Unit, double? Low, double? High);

public enum SensorState
{
    Normal,
    Alarm,
    Stale,
    Missing,
}

public enum LatchState
{
    Clear,
    Unacked,
    Acked,
    Returned,
}

/// <summary>What one tile on the operator panel shows. The window binds to these.</summary>
public sealed class TileView
{
    public TileView(string label)
    {
        Label = label;
    }

    public string Label { get; }

    public SensorState State { get; set; } = SensorState.Missing;

    public string StateText { get; set; } = "NO DATA";

    public string ValueText { get; set; } = "- - -";

    public string LastValueText { get; set; } = string.Empty;

    public string BannerText { get; set; } = string.Empty;

    public override string ToString() =>
        $"{Label}: {StateText} {ValueText} {LastValueText} {BannerText}".TrimEnd();
}
