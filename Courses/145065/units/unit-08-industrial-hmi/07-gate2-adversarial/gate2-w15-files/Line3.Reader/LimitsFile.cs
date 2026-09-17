using System.Text.Json;

namespace Line3.Reader;

/// <summary>One sensor's documented limits. Either limit may be absent.</summary>
public sealed class SensorLimit
{
    public string Id { get; set; } = string.Empty;

    public double? Low { get; set; }

    public double? High { get; set; }

    public string Reason { get; set; } = string.Empty;
}

/// <summary>
/// The limits the panel alarms on, loaded from limits.json. Read-only after Load:
/// limits change only by editing limits.json, so every number on screen has a
/// documented source.
/// </summary>
public sealed class LimitsFile
{
    public Uri ServiceUrl { get; set; } = new("http://127.0.0.1:8700/");

    public TimeSpan RequestTimeout { get; set; } = TimeSpan.FromMilliseconds(1500);

    public TimeSpan PollInterval { get; set; } = TimeSpan.FromSeconds(1);

    public List<SensorLimit> Sensors { get; set; } = new();

    public SensorLimit? Find(string id) => Sensors.FirstOrDefault(s => s.Id == id);

    public static LimitsFile Load(string path)
    {
        using JsonDocument document = JsonDocument.Parse(File.ReadAllText(path));
        JsonElement root = document.RootElement;

        LimitsFile limits = new()
        {
            ServiceUrl = new Uri(root.GetProperty("service_url").GetString()!.TrimEnd('/') + "/"),
            RequestTimeout = TimeSpan.FromMilliseconds(root.GetProperty("request_timeout_ms").GetInt32()),
            PollInterval = TimeSpan.FromMilliseconds(root.GetProperty("poll_interval_ms").GetInt32()),
        };

        foreach (JsonElement entry in root.GetProperty("sensors").EnumerateArray())
        {
            limits.Sensors.Add(new SensorLimit
            {
                Id = entry.GetProperty("id").GetString()!,
                Low = OptionalNumber(entry, "low"),
                High = OptionalNumber(entry, "high"),
                Reason = entry.GetProperty("reason").GetString()!,
            });
        }

        return limits;
    }

    private static double? OptionalNumber(JsonElement entry, string name) =>
        entry.TryGetProperty(name, out JsonElement value) && value.ValueKind == JsonValueKind.Number
            ? value.GetDouble()
            : null;
}
