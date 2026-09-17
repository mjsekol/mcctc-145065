// COPIED from the course's HMI anchor, panel/Line3.Hmi.Core/PanelConfig.cs.
// Given to you, with ONE change: the body of SensorThreshold.Check is removed
// for Lab U08-03, step 7. Paste your Lab U08-03 Check here. Everything else is
// the anchor code.
//
// PanelConfig.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// Loads thresholds.json: where the service is, how often to ask, how long to
// wait, when data counts as stale, and every sensor's limits WITH A REASON.
//
// A limit with no reason is refused. "Documented threshold you can defend"
// is a requirement of the Unit 8 project, and the loader enforces it, so a
// panel cannot start with a number nobody can explain.
//
// A bad file stops the panel with a sentence saying what is wrong. The panel
// never falls back to built-in limits: an operator watching limits that are
// not the ones on the process sheet is worse than no panel.

using System.Globalization;
using System.Text.Json;

namespace Line3.Hmi.Core;

public enum LimitCheck
{
    Within,
    BelowLow,
    AboveHigh,
}

/// <summary>One sensor's documented limits. Either limit may be absent, not both.</summary>
public sealed record SensorThreshold(
    string Id,
    string Label,
    string Unit,
    int Decimals,
    double? Low,
    double? High,
    string Reason)
{
    /// <summary>
    /// Inside means low &lt;= value &lt;= high. A value exactly on a limit is
    /// inside. The limit is the last acceptable value, not the first bad one.
    /// </summary>
    public LimitCheck Check(double value)
    {
        // TODO Lab U08-03, step 7. Low and High are double? (nullable): either
        // one may be missing. A value exactly on a limit is Within.
        return LimitCheck.Within;
    }

    public string Format(double value) =>
        value.ToString("F" + Decimals.ToString(CultureInfo.InvariantCulture), CultureInfo.InvariantCulture);

    public string LimitsText
    {
        get
        {
            if (Low is double low && High is double high)
            {
                return $"Limits {Format(low)} to {Format(high)} {Unit}";
            }

            return Low is double onlyLow
                ? $"Low limit {Format(onlyLow)} {Unit}"
                : $"High limit {Format(High!.Value)} {Unit}";
        }
    }
}

/// <summary>Thrown when thresholds.json cannot be trusted. The message is for a person.</summary>
public sealed class PanelConfigException : Exception
{
    public PanelConfigException(string message)
        : base(message)
    {
    }
}

public sealed class PanelConfig
{
    public const int SupportedSchemaVersion = 1;

    public PanelConfig(Uri serviceUrl, TimeSpan pollInterval, TimeSpan requestTimeout,
                       TimeSpan staleAfter, IReadOnlyList<SensorThreshold> sensors)
    {
        ServiceUrl = serviceUrl;
        PollInterval = pollInterval;
        RequestTimeout = requestTimeout;
        StaleAfter = staleAfter;
        Sensors = sensors;
    }

    public Uri ServiceUrl { get; }

    public TimeSpan PollInterval { get; }

    public TimeSpan RequestTimeout { get; }

    public TimeSpan StaleAfter { get; }

    public IReadOnlyList<SensorThreshold> Sensors { get; }

    /// <summary>The same limits, pointed at a different service.</summary>
    public PanelConfig WithServiceUrl(Uri serviceUrl) =>
        new(ValidateUrl(serviceUrl.ToString()), PollInterval, RequestTimeout, StaleAfter, Sensors);

    public static PanelConfig Load(string path)
    {
        string text;
        try
        {
            text = File.ReadAllText(path);
        }
        catch (Exception problem) when (problem is IOException or UnauthorizedAccessException)
        {
            throw new PanelConfigException($"Cannot read the thresholds file {path}: {problem.Message}");
        }

        return Parse(text);
    }

    public static PanelConfig Parse(string json)
    {
        JsonDocument document;
        try
        {
            document = JsonDocument.Parse(json);
        }
        catch (JsonException problem)
        {
            throw new PanelConfigException($"The thresholds file is not valid JSON: {problem.Message}");
        }

        using (document)
        {
            JsonElement root = document.RootElement;
            if (root.ValueKind != JsonValueKind.Object)
            {
                throw new PanelConfigException("The thresholds file must be one JSON object.");
            }

            int version = RequireInt(root, "schema_version");
            if (version != SupportedSchemaVersion)
            {
                throw new PanelConfigException(
                    $"schema_version is {version}; this panel reads version {SupportedSchemaVersion}.");
            }

            Uri url = ValidateUrl(RequireString(root, "service_url"));
            TimeSpan poll = TimeSpan.FromMilliseconds(RequireInt(root, "poll_interval_ms"));
            TimeSpan timeout = TimeSpan.FromMilliseconds(RequireInt(root, "request_timeout_ms"));
            TimeSpan stale = TimeSpan.FromSeconds(RequireDouble(root, "stale_after_seconds"));

            if (poll < TimeSpan.FromMilliseconds(100))
            {
                throw new PanelConfigException("poll_interval_ms must be at least 100.");
            }

            if (timeout < TimeSpan.FromMilliseconds(100))
            {
                throw new PanelConfigException("request_timeout_ms must be at least 100.");
            }

            // If a request may take longer than the stale limit, a slow reply
            // could arrive already stale every time, and the panel would never
            // show a live value. Refuse that combination.
            if (timeout >= stale)
            {
                throw new PanelConfigException("request_timeout_ms must be shorter than stale_after_seconds.");
            }

            if (poll >= stale)
            {
                throw new PanelConfigException("poll_interval_ms must be shorter than stale_after_seconds.");
            }

            if (!root.TryGetProperty("sensors", out JsonElement list)
                || list.ValueKind != JsonValueKind.Array
                || list.GetArrayLength() == 0)
            {
                throw new PanelConfigException("\"sensors\" must be a list with at least one sensor.");
            }

            List<SensorThreshold> sensors = new();
            HashSet<string> ids = new(StringComparer.Ordinal);
            foreach (JsonElement entry in list.EnumerateArray())
            {
                SensorThreshold threshold = ParseSensor(entry);
                if (!ids.Add(threshold.Id))
                {
                    throw new PanelConfigException($"Sensor \"{threshold.Id}\" is listed twice.");
                }

                sensors.Add(threshold);
            }

            return new PanelConfig(url, poll, timeout, stale, sensors);
        }
    }

    private static SensorThreshold ParseSensor(JsonElement entry)
    {
        if (entry.ValueKind != JsonValueKind.Object)
        {
            throw new PanelConfigException("Every entry in \"sensors\" must be an object.");
        }

        string id = RequireString(entry, "id");
        string label = RequireString(entry, "label");
        string unit = RequireString(entry, "unit");
        int decimals = RequireInt(entry, "decimals");
        double? low = OptionalDouble(entry, "low", id);
        double? high = OptionalDouble(entry, "high", id);
        string reason = entry.TryGetProperty("reason", out JsonElement r) && r.ValueKind == JsonValueKind.String
            ? r.GetString()!.Trim()
            : string.Empty;

        if (decimals is < 0 or > 3)
        {
            throw new PanelConfigException($"Sensor \"{id}\": decimals must be 0 to 3.");
        }

        if (low is null && high is null)
        {
            throw new PanelConfigException($"Sensor \"{id}\" has no low and no high limit. Give it at least one.");
        }

        if (low is double l && high is double h && l >= h)
        {
            throw new PanelConfigException($"Sensor \"{id}\": low ({l}) must be less than high ({h}).");
        }

        if (reason.Length < 20)
        {
            throw new PanelConfigException(
                $"Sensor \"{id}\" has no reason for its limits. Write why these numbers, in a sentence an operator can read.");
        }

        return new SensorThreshold(id, label, unit, decimals, low, high, reason);
    }

    private static Uri ValidateUrl(string text)
    {
        if (!Uri.TryCreate(text, UriKind.Absolute, out Uri? url)
            || (url.Scheme != Uri.UriSchemeHttp && url.Scheme != Uri.UriSchemeHttps))
        {
            throw new PanelConfigException($"service_url \"{text}\" is not an http address.");
        }

        return url;
    }

    private static string RequireString(JsonElement parent, string name)
    {
        if (parent.TryGetProperty(name, out JsonElement element)
            && element.ValueKind == JsonValueKind.String
            && !string.IsNullOrWhiteSpace(element.GetString()))
        {
            return element.GetString()!;
        }

        throw new PanelConfigException($"\"{name}\" is missing or empty.");
    }

    private static int RequireInt(JsonElement parent, string name)
    {
        if (parent.TryGetProperty(name, out JsonElement element)
            && element.ValueKind == JsonValueKind.Number
            && element.TryGetInt32(out int value))
        {
            return value;
        }

        throw new PanelConfigException($"\"{name}\" is missing or not a whole number.");
    }

    private static double RequireDouble(JsonElement parent, string name)
    {
        if (parent.TryGetProperty(name, out JsonElement element)
            && element.ValueKind == JsonValueKind.Number
            && element.TryGetDouble(out double value)
            && value > 0)
        {
            return value;
        }

        throw new PanelConfigException($"\"{name}\" is missing or not a number above zero.");
    }

    private static double? OptionalDouble(JsonElement parent, string name, string id)
    {
        if (!parent.TryGetProperty(name, out JsonElement element) || element.ValueKind == JsonValueKind.Null)
        {
            return null;
        }

        if (element.ValueKind == JsonValueKind.Number && element.TryGetDouble(out double value))
        {
            return value;
        }

        throw new PanelConfigException($"Sensor \"{id}\": \"{name}\" must be a number or null.");
    }
}
