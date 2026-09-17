// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/ReadingParser.cs.
// Given to you. Read it; you do not need to change it.
//
// ReadingParser.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// Turns the text of a reply into a ReadingSnapshot, or says exactly why it
// could not. It never throws for bad input and never guesses a value.
//
// Two kinds of problem, handled two ways:
//
//   The whole reply is wrong (not JSON, missing sequence, a bad timestamp,
//   two sensors with the same id): the parse FAILS. The panel treats every
//   sensor as MISSING, because nothing in that reply can be trusted.
//
//   One sensor entry breaks the contract (ok true with no value, ok false
//   with a value): the parse SUCCEEDS, and that one sensor is marked not ok
//   with a ContractProblem. The panel shows it MISSING and shows the rest.

using System.Globalization;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace Line3.Hmi.Core;

/// <summary>A parse that worked, or the reason it did not. Never both.</summary>
public sealed record ParseResult(ReadingSnapshot? Snapshot, string? Error)
{
    public bool Ok => Snapshot is not null;

    public static ParseResult Success(ReadingSnapshot snapshot) => new(snapshot, null);

    public static ParseResult Failure(string error) => new(null, error);
}

public static partial class ReadingParser
{
    // A timestamp must say which time zone it is in. "2027-01-11T14:03:22"
    // with no Z could be the Pi's local time or UTC, and a wrong guess makes
    // every value look hours stale, or hours fresh.
    [GeneratedRegex(@"(Z|[+-]\d{2}:\d{2})$")]
    private static partial Regex HasZone();

    public static ParseResult Parse(string? json)
    {
        if (string.IsNullOrWhiteSpace(json))
        {
            return ParseResult.Failure("the reply was empty");
        }

        JsonDocument document;
        try
        {
            document = JsonDocument.Parse(json);
        }
        catch (JsonException problem)
        {
            return ParseResult.Failure($"the reply is not valid JSON ({problem.Message})");
        }

        using (document)
        {
            JsonElement root = document.RootElement;
            if (root.ValueKind != JsonValueKind.Object)
            {
                return ParseResult.Failure("the reply is not a JSON object");
            }

            if (!TryString(root, "device", out string device) || device.Length == 0)
            {
                return ParseResult.Failure("\"device\" is missing or not a string");
            }

            if (!root.TryGetProperty("sequence", out JsonElement sequenceElement)
                || sequenceElement.ValueKind != JsonValueKind.Number
                || !sequenceElement.TryGetInt64(out long sequence)
                || sequence < 0)
            {
                return ParseResult.Failure("\"sequence\" is missing or not a whole number of zero or more");
            }

            if (!TryString(root, "sampled_at", out string stamp)
                || !HasZone().IsMatch(stamp)
                || !DateTimeOffset.TryParse(stamp, CultureInfo.InvariantCulture,
                                            DateTimeStyles.AdjustToUniversal, out DateTimeOffset sampledAt))
            {
                return ParseResult.Failure("\"sampled_at\" is missing, not a time, or has no time zone");
            }

            if (!root.TryGetProperty("sensors", out JsonElement sensorsElement)
                || sensorsElement.ValueKind != JsonValueKind.Array)
            {
                return ParseResult.Failure("\"sensors\" is missing or not a list");
            }

            List<SensorSample> sensors = new();
            HashSet<string> seen = new(StringComparer.Ordinal);
            int index = 0;
            foreach (JsonElement entry in sensorsElement.EnumerateArray())
            {
                string? error = ParseSensor(entry, index, out SensorSample? sample);
                if (error is not null)
                {
                    return ParseResult.Failure(error);
                }

                if (!seen.Add(sample!.Id))
                {
                    return ParseResult.Failure($"sensor \"{sample.Id}\" appears twice");
                }

                sensors.Add(sample);
                index++;
            }

            return ParseResult.Success(new ReadingSnapshot(device, sequence, sampledAt, sensors));
        }
    }

    private static string? ParseSensor(JsonElement entry, int index, out SensorSample? sample)
    {
        sample = null;
        if (entry.ValueKind != JsonValueKind.Object)
        {
            return $"sensors[{index}] is not an object";
        }

        if (!TryString(entry, "id", out string id) || id.Length == 0)
        {
            return $"sensors[{index}] has no \"id\"";
        }

        if (!TryString(entry, "kind", out string kind) || !TryString(entry, "unit", out string unit))
        {
            return $"sensor \"{id}\" is missing \"kind\" or \"unit\"";
        }

        if (!entry.TryGetProperty("ok", out JsonElement okElement)
            || (okElement.ValueKind != JsonValueKind.True && okElement.ValueKind != JsonValueKind.False))
        {
            return $"sensor \"{id}\" has no true or false \"ok\"";
        }

        bool ok = okElement.ValueKind == JsonValueKind.True;

        double? value;
        if (!entry.TryGetProperty("value", out JsonElement valueElement)
            || valueElement.ValueKind == JsonValueKind.Null)
        {
            value = null;
        }
        else if (valueElement.ValueKind == JsonValueKind.Number
                 && valueElement.TryGetDouble(out double number)
                 && double.IsFinite(number))
        {
            value = number;
        }
        else
        {
            return $"sensor \"{id}\" has a \"value\" that is not a number or null";
        }

        // The contract says: ok true has a number, ok false has null. A reply
        // that breaks this for one sensor loses that sensor, not the reply.
        if (ok && value is null)
        {
            sample = new SensorSample(id, kind, null, unit, false)
            {
                ContractProblem = "the service said ok but sent no value",
            };
        }
        else if (!ok && value is not null)
        {
            sample = new SensorSample(id, kind, null, unit, false)
            {
                ContractProblem = "the service sent a value it marked as a failed read",
            };
        }
        else
        {
            sample = new SensorSample(id, kind, value, unit, ok);
        }

        return null;
    }

    private static bool TryString(JsonElement parent, string name, out string text)
    {
        if (parent.TryGetProperty(name, out JsonElement element) && element.ValueKind == JsonValueKind.String)
        {
            text = element.GetString() ?? string.Empty;
            return true;
        }

        text = string.Empty;
        return false;
    }
}
