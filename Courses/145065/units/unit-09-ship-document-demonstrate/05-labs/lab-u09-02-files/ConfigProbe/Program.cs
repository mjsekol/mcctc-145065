// Program.cs  .  Lab U09-02  .  ConfigProbe
//
//   dotnet run --project ConfigProbe -- configs/thresholds.json
//
// Loads one thresholds file with the version 1.0.0 loader (PanelConfig.cs,
// copied unchanged) and prints what a 1.0.0 panel would do with it:
//
//   LOADED   the panel starts, with the limits listed
//   REFUSED  the panel shows its "cannot start" box with this sentence
//
// Then it lists every key in the file that the 1.0.0 loader never reads.
// A 1.0.0 panel says nothing about those keys. ConfigProbe says it for you.
//
// Exit codes: 0 loaded, 1 refused, 2 bad usage.

using System.Globalization;
using System.Text.Json;
using Line3.Hmi.Core;

namespace ConfigProbe;

public static class Program
{
    // Every key the 1.0.0 loader reads. Anything else in a file is ignored.
    private static readonly HashSet<string> TopKeys = new(StringComparer.Ordinal)
    {
        "schema_version", "service_url", "poll_interval_ms", "request_timeout_ms", "stale_after_seconds", "sensors",
    };

    private static readonly HashSet<string> SensorKeys = new(StringComparer.Ordinal)
    {
        "id", "label", "unit", "decimals", "low", "high", "reason",
    };

    // Ignored on purpose: the shipped file uses these to carry notes for people.
    private static readonly HashSet<string> NoteKeys = new(StringComparer.Ordinal) { "setting", "stale_reason" };

    public static int Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.Error.WriteLine("Usage: ConfigProbe <thresholds file>");
            return 2;
        }

        string text;
        try
        {
            text = File.ReadAllText(args[0]);
        }
        catch (IOException problem)
        {
            Console.Error.WriteLine($"Cannot read {args[0]}: {problem.Message}");
            return 2;
        }

        Console.WriteLine($"File: {Path.GetFileName(args[0])}");
        int exit;
        try
        {
            PanelConfig config = PanelConfig.Parse(text);
            Console.WriteLine(string.Create(CultureInfo.InvariantCulture,
                $"LOADED   {config.Sensors.Count} sensors, stale after {config.StaleAfter.TotalSeconds} s"));
            foreach (SensorThreshold sensor in config.Sensors)
            {
                Console.WriteLine($"         {sensor.Id,-16} {sensor.LimitsText}");
            }

            exit = 0;
        }
        catch (PanelConfigException refused)
        {
            Console.WriteLine($"REFUSED  {refused.Message}");
            exit = 1;
        }

        List<string> ignored = IgnoredKeys(text);
        Console.WriteLine(ignored.Count == 0
            ? "Ignored by a 1.0.0 panel: nothing"
            : "Ignored by a 1.0.0 panel: " + string.Join(", ", ignored));
        return exit;
    }

    /// <summary>Keys the 1.0.0 loader never reads, apart from the two note keys.</summary>
    public static List<string> IgnoredKeys(string json)
    {
        List<string> ignored = new();
        try
        {
            using JsonDocument document = JsonDocument.Parse(json);
            if (document.RootElement.ValueKind != JsonValueKind.Object)
            {
                return ignored;
            }

            foreach (JsonProperty top in document.RootElement.EnumerateObject())
            {
                if (!TopKeys.Contains(top.Name) && !NoteKeys.Contains(top.Name))
                {
                    ignored.Add(top.Name);
                }
            }

            if (document.RootElement.TryGetProperty("sensors", out JsonElement sensors)
                && sensors.ValueKind == JsonValueKind.Array)
            {
                foreach (JsonElement sensor in sensors.EnumerateArray())
                {
                    if (sensor.ValueKind != JsonValueKind.Object)
                    {
                        continue;
                    }

                    string id = sensor.TryGetProperty("id", out JsonElement idElement) ? idElement.ToString() : "?";
                    foreach (JsonProperty key in sensor.EnumerateObject())
                    {
                        if (!SensorKeys.Contains(key.Name))
                        {
                            ignored.Add($"{key.Name} ({id})");
                        }
                    }
                }
            }
        }
        catch (JsonException)
        {
            // Not JSON at all. The loader already said so.
        }

        return ignored;
    }
}
