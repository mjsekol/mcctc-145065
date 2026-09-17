// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core.Tests/TestData.cs.
//
// TestData.cs  .  145065 HMI anchor  .  Line3.Hmi.Core.Tests
//
// Builders for replies, configs, and times, so each test says only what is
// different about it. The dates here are invented sample data.

using System.Globalization;
using System.Runtime.CompilerServices;

namespace Line3.Hmi.Core.Tests;

internal static class TestData
{
    public static readonly DateTimeOffset T0 = new(2027, 1, 11, 14, 3, 22, TimeSpan.Zero);

    public static readonly Uri ServiceUrl = new("http://127.0.0.1:8660");

    public static PanelConfig ShippedConfig() =>
        PanelConfig.Load(Path.Combine(AppContext.BaseDirectory, "thresholds.json"));

    public static PanelConfig Config(TimeSpan? staleAfter = null)
    {
        PanelConfig shipped = ShippedConfig();
        return new PanelConfig(ServiceUrl, TimeSpan.FromSeconds(1), TimeSpan.FromMilliseconds(1500),
                               staleAfter ?? TimeSpan.FromSeconds(5), shipped.Sensors);
    }

    public static SensorThreshold Oven => ShippedConfig().Sensors.First(s => s.Id == "oven-temp");

    /// <summary>A contract reply as text. Pass null for a failed sensor.</summary>
    public static string Json(long sequence, DateTimeOffset sampledAt,
                              double? oven = 212.4, double? vibration = 3.1, double? coolant = 68.0)
    {
        static string Sensor(string id, string kind, string unit, double? value) =>
            value is double v
                ? $"{{\"id\": \"{id}\", \"kind\": \"{kind}\", \"value\": {v.ToString("R", CultureInfo.InvariantCulture)}, \"unit\": \"{unit}\", \"ok\": true}}"
                : $"{{\"id\": \"{id}\", \"kind\": \"{kind}\", \"value\": null, \"unit\": \"{unit}\", \"ok\": false}}";

        string stamp = sampledAt.UtcDateTime.ToString("yyyy-MM-dd'T'HH:mm:ss'Z'", CultureInfo.InvariantCulture);
        return $$"""
            {
              "device": "line3-pi",
              "sequence": {{sequence}},
              "sampled_at": "{{stamp}}",
              "sensors": [
                {{Sensor("oven-temp", "temperature", "C", oven)}},
                {{Sensor("press-vibration", "vibration", "mm/s", vibration)}},
                {{Sensor("coolant-level", "level", "%", coolant)}}
              ]
            }
            """;
    }

    public static ReadingSnapshot Snapshot(long sequence, DateTimeOffset sampledAt,
                                           double? oven = 212.4, double? vibration = 3.1, double? coolant = 68.0) =>
        ReadingParser.Parse(Json(sequence, sampledAt, oven, vibration, coolant)).Snapshot!;

    public static PollResult Good(long sequence, DateTimeOffset sampledAt, DateTimeOffset receivedAt,
                                  double? oven = 212.4, double? vibration = 3.1, double? coolant = 68.0) =>
        PollResult.Success(Snapshot(sequence, sampledAt, oven, vibration, coolant), receivedAt);

    public static PollResult Bad(PollFailure failure, DateTimeOffset at) =>
        PollResult.Failed(failure, "test failure", at);

    public static string SourceFolder([CallerFilePath] string path = "") => Path.GetDirectoryName(path)!;
}
