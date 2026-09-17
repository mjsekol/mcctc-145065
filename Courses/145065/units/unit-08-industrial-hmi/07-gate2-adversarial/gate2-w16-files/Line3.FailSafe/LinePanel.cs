using System.Globalization;
using System.Net.Http;
using System.Text;
using System.Text.Json;

namespace Line3.FailSafe;

/// <summary>
/// The Line 3 fail-safe panel logic. The window creates one LinePanel, calls Tick()
/// from its once-a-second timer, and binds to Tiles and ConnectionText.
/// Everything the panel decides lives here, so there is one place to look.
/// </summary>
public sealed class LinePanel : IDisposable
{
    public static readonly TimeSpan StaleAfter = TimeSpan.FromSeconds(5);
    public static readonly TimeSpan RequestTimeout = TimeSpan.FromMilliseconds(1500);

    private readonly HttpClient http = new() { Timeout = RequestTimeout };
    private readonly Uri baseUrl;
    private readonly Func<DateTimeOffset> clock;
    private readonly Dictionary<string, SensorLimit> limits = new();
    private readonly Dictionary<string, TileView> tiles = new();
    private readonly Dictionary<string, LatchState> latches = new();
    private readonly Dictionary<string, double> lastValues = new();

    private long? lastSequence;
    private DateTimeOffset sequenceChangedAt;
    private DateTimeOffset lastSampledAt;

    public LinePanel(Uri baseUrl, IEnumerable<SensorLimit> sensorLimits, Func<DateTimeOffset>? clock = null)
    {
        this.baseUrl = baseUrl;
        this.clock = clock ?? (() => DateTimeOffset.UtcNow);
        foreach (SensorLimit limit in sensorLimits)
        {
            limits[limit.Id] = limit;
            tiles[limit.Id] = new TileView(limit.Label);
            latches[limit.Id] = LatchState.Clear;
        }
    }

    public IReadOnlyDictionary<string, TileView> Tiles => tiles;

    public string ConnectionText { get; private set; } = "WAITING";

    /// <summary>The poll in flight, for tests. Tick finishes its work before it returns.</summary>
    public Task Pending => Task.CompletedTask;

    public LatchState LatchOf(string id) => latches[id];

    /// <summary>Called by the window's timer once a second.</summary>
    public void Tick()
    {
        DateTimeOffset now = clock();
        Dictionary<string, JsonElement>? sensors = null;

        try
        {
            using HttpResponseMessage response = http.GetAsync(new Uri(baseUrl, "api/readings")).Result;
            string body = response.Content.ReadAsStringAsync().Result;
            if (response.IsSuccessStatusCode)
            {
                sensors = ReadReply(body, now);
                if (sensors is null)
                {
                    RecoverDevice();
                }
            }
        }
        catch (AggregateException)
        {
            // Timed out or refused. Shown below as missing data.
        }

        ConnectionText = sensors is null ? "NO CONNECTION" : IsFresh(now) ? "CONNECTED" : "DATA NOT UPDATING";

        foreach (SensorLimit limit in limits.Values)
        {
            SensorState state;
            if (sensors is null
                || !sensors.TryGetValue(limit.Id, out JsonElement entry)
                || !entry.GetProperty("ok").GetBoolean())
            {
                state = SensorState.Missing;
            }
            else
            {
                double value = entry.GetProperty("value").GetDouble();
                lastValues[limit.Id] = value;
                state = !IsFresh(now) ? SensorState.Stale
                    : Within(limit, value) ? SensorState.Normal
                    : SensorState.Alarm;
            }

            latches[limit.Id] = NextLatch(latches[limit.Id], state);
            Show(limit, state, now);
        }
    }

    /// <summary>The operator acknowledged this sensor's alarm.</summary>
    public void Acknowledge(string id)
    {
        latches[id] = latches[id] switch
        {
            LatchState.Unacked => LatchState.Acked,
            LatchState.Returned => LatchState.Clear,
            _ => latches[id],
        };
        Show(limits[id], tiles[id].State, clock());
    }

    public void Dispose() => http.Dispose();

    private Dictionary<string, JsonElement>? ReadReply(string body, DateTimeOffset now)
    {
        try
        {
            using JsonDocument document = JsonDocument.Parse(body);
            JsonElement root = document.RootElement;
            long sequence = root.GetProperty("sequence").GetInt64();
            DateTimeOffset sampledAt = DateTimeOffset.Parse(root.GetProperty("sampled_at").GetString()!,
                CultureInfo.InvariantCulture, DateTimeStyles.AssumeUniversal | DateTimeStyles.AdjustToUniversal);

            Dictionary<string, JsonElement> sensors = new();
            foreach (JsonElement s in root.GetProperty("sensors").EnumerateArray())
            {
                // The contract: ok is true with a number, or false with null.
                bool ok = s.GetProperty("ok").GetBoolean();
                JsonValueKind value = s.GetProperty("value").ValueKind;
                if (ok != (value == JsonValueKind.Number) || (!ok && value != JsonValueKind.Null))
                {
                    return null;
                }

                sensors[s.GetProperty("id").GetString()!] = s.Clone();
            }

            if (sequence != lastSequence)
            {
                lastSequence = sequence;
                sequenceChangedAt = now;
            }

            lastSampledAt = sampledAt;
            return sensors;
        }
        catch (Exception ex) when (ex is JsonException or KeyNotFoundException or InvalidOperationException or FormatException)
        {
            return null;
        }
    }

    // A garbled reply usually means the simulator was left in a test mode.
    // Put it back to normal so the operator gets readings again.
    private void RecoverDevice()
    {
        try
        {
            using StringContent body = new("{\"mode\": \"normal\"}", Encoding.UTF8, "application/json");
            http.PostAsync(new Uri(baseUrl, "sim/mode"), body).Result.Dispose();
        }
        catch (AggregateException)
        {
            // Nothing more to try.
        }
    }

    private bool IsFresh(DateTimeOffset now) =>
        now - lastSampledAt <= StaleAfter && now - sequenceChangedAt <= StaleAfter;

    private static bool Within(SensorLimit limit, double value) =>
        (limit.Low is not double low || value >= low) && (limit.High is not double high || value <= high);

    private static LatchState NextLatch(LatchState current, SensorState state) => state switch
    {
        SensorState.Alarm => current == LatchState.Acked ? LatchState.Acked : LatchState.Unacked,
        SensorState.Normal => current switch
        {
            LatchState.Unacked => LatchState.Returned,
            LatchState.Acked => LatchState.Clear,
            _ => current,
        },

        // A sensor we can no longer see cannot be in alarm. Reset its latch so an
        // old alarm does not linger on a dark tile.
        SensorState.Missing => LatchState.Clear,
        _ => current,
    };

    private void Show(SensorLimit limit, SensorState state, DateTimeOffset now)
    {
        TileView tile = tiles[limit.Id];
        string Format(double v) => v.ToString("0.0", CultureInfo.InvariantCulture);

        switch (state)
        {
            case SensorState.Normal:
                tile.StateText = "NORMAL";
                tile.ValueText = Format(lastValues[limit.Id]);
                tile.LastValueText = string.Empty;
                break;
            case SensorState.Alarm:
                tile.StateText = limit.Low is double low && lastValues[limit.Id] < low ? "ALARM LOW" : "ALARM HIGH";
                tile.ValueText = Format(lastValues[limit.Id]);
                tile.LastValueText = string.Empty;
                break;
            case SensorState.Stale:
                // Keep the last number in the big text so the operator is not left
                // staring at a blank. The STALE word and the yellow tile already say
                // it is not live.
                TimeSpan age = now - lastSampledAt > now - sequenceChangedAt ? now - lastSampledAt : now - sequenceChangedAt;
                tile.StateText = "STALE";
                tile.ValueText = Format(lastValues[limit.Id]);
                tile.LastValueText = $"Last value {Format(lastValues[limit.Id])} {limit.Unit}, {age.TotalSeconds:0} s old. Not live.";
                break;
            default:
                tile.StateText = "NO DATA";
                tile.ValueText = "- - -";
                tile.LastValueText = string.Empty;
                break;
        }

        tile.State = state;
        tile.BannerText = latches[limit.Id] switch
        {
            LatchState.Unacked => "UNACKNOWLEDGED ALARM",
            LatchState.Acked => "ACKNOWLEDGED, NOT CLEARED",
            LatchState.Returned => "ALARM ENDED, NOT ACKNOWLEDGED",
            _ => string.Empty,
        };
    }
}
