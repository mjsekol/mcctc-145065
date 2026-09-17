using System.Globalization;
using System.Text.Json;

namespace Line3.Reader;

/// <summary>Turns the service's JSON into a ReadingBatch, or explains why it cannot.</summary>
public static class ReadingParser
{
    public static ReadingBatch? Parse(string json, out string? problem)
    {
        problem = null;
        try
        {
            using JsonDocument document = JsonDocument.Parse(json);
            JsonElement root = document.RootElement;

            string device = root.GetProperty("device").GetString() ?? string.Empty;
            long sequence = root.GetProperty("sequence").GetInt64();
            string stamp = root.GetProperty("sampled_at").GetString() ?? string.Empty;
            DateTimeOffset sampledAt = DateTimeOffset.Parse(stamp, CultureInfo.InvariantCulture, DateTimeStyles.AssumeUniversal | DateTimeStyles.AdjustToUniversal);

            List<SensorReading> sensors = new();
            foreach (JsonElement entry in root.GetProperty("sensors").EnumerateArray())
            {
                bool ok = entry.GetProperty("ok").GetBoolean();
                JsonElement value = entry.GetProperty("value");

                // A failed sensor sends null. Store 0.0 and keep Ok false, so the
                // record never holds a null and the display always has a number.
                sensors.Add(new SensorReading(
                    entry.GetProperty("id").GetString() ?? string.Empty,
                    entry.GetProperty("kind").GetString() ?? string.Empty,
                    value.ValueKind == JsonValueKind.Null ? 0.0 : value.GetDouble(),
                    entry.GetProperty("unit").GetString() ?? string.Empty,
                    ok));
            }

            return new ReadingBatch(device, sequence, sampledAt, sensors);
        }
        catch (Exception ex) when (ex is JsonException or KeyNotFoundException or InvalidOperationException or FormatException)
        {
            problem = "the reply is not a valid Line 3 reading: " + ex.Message;
            return null;
        }
    }
}
