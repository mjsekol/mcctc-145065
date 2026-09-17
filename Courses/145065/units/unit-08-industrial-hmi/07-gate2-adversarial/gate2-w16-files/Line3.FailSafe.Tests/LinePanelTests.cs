using System.Net;
using System.Text;
using Line3.FailSafe;

namespace Line3.FailSafe.Tests;

[CollectionDefinition("network", DisableParallelization = true)]
public sealed class NetworkCollection
{
}

[Collection("network")]
public class LinePanelTests
{
    private static readonly DateTimeOffset T0 = new(2027, 1, 11, 14, 3, 22, TimeSpan.Zero);

    private static readonly SensorLimit[] Limits =
    {
        new("oven-temp", "Oven", "C", 190.0, 230.0),
        new("press-vibration", "Press", "mm/s", null, 6.0),
        new("coolant-level", "Coolant", "%", 25.0, null),
    };

    private static string Reply(long sequence, DateTimeOffset sampledAt, double oven) =>
        "{\"device\": \"line3-pi\", \"sequence\": " + sequence + ", \"sampled_at\": \""
        + sampledAt.UtcDateTime.ToString("yyyy-MM-dd'T'HH:mm:ss'Z'", System.Globalization.CultureInfo.InvariantCulture) + "\", \"sensors\": ["
        + "{\"id\": \"oven-temp\", \"kind\": \"temperature\", \"value\": " + oven.ToString(System.Globalization.CultureInfo.InvariantCulture) + ", \"unit\": \"C\", \"ok\": true},"
        + "{\"id\": \"press-vibration\", \"kind\": \"vibration\", \"value\": 3.1, \"unit\": \"mm/s\", \"ok\": true},"
        + "{\"id\": \"coolant-level\", \"kind\": \"level\", \"value\": 68.0, \"unit\": \"%\", \"ok\": true}]}";

    [Fact]
    public async Task ANormalReplyShowsNormal()
    {
        using FakeService fake = new() { Body = Reply(1, T0, 212.4) };
        using LinePanel panel = new(fake.BaseUrl, Limits, () => T0);

        panel.Tick();
        await panel.Pending;

        Assert.Equal("CONNECTED", panel.ConnectionText);
        Assert.Equal("NORMAL", panel.Tiles["oven-temp"].StateText);
        Assert.Equal("212.4", panel.Tiles["oven-temp"].ValueText);
    }

    [Fact]
    public async Task AboveTheHighLimitIsAnAlarmWithABanner()
    {
        using FakeService fake = new() { Body = Reply(1, T0, 236.0) };
        using LinePanel panel = new(fake.BaseUrl, Limits, () => T0);

        panel.Tick();
        await panel.Pending;

        Assert.Equal("ALARM HIGH", panel.Tiles["oven-temp"].StateText);
        Assert.Equal("UNACKNOWLEDGED ALARM", panel.Tiles["oven-temp"].BannerText);
    }

    [Fact]
    public async Task AcknowledgingKeepsTheAlarmUntilTheValueIsBack()
    {
        using FakeService fake = new() { Body = Reply(1, T0, 236.0) };
        using LinePanel panel = new(fake.BaseUrl, Limits, () => T0);
        panel.Tick();
        await panel.Pending;

        panel.Acknowledge("oven-temp");

        Assert.Equal("ACKNOWLEDGED, NOT CLEARED", panel.Tiles["oven-temp"].BannerText);
        Assert.Equal(LatchState.Acked, panel.LatchOf("oven-temp"));
    }

    [Fact]
    public async Task NoServiceShowsNoDataAndNoNumber()
    {
        using LinePanel panel = new(new Uri("http://127.0.0.1:8704/"), Limits, () => T0);

        panel.Tick();
        await panel.Pending;

        Assert.Equal("NO CONNECTION", panel.ConnectionText);
        Assert.All(panel.Tiles.Values, t => Assert.Equal("- - -", t.ValueText));
    }

    [Fact]
    public async Task ASequenceThatStopsTurnsStale()
    {
        DateTimeOffset now = T0;
        using FakeService fake = new() { Body = Reply(50, T0, 212.4) };
        using LinePanel panel = new(fake.BaseUrl, Limits, () => now);
        panel.Tick();
        await panel.Pending;

        now = T0.AddSeconds(7);
        panel.Tick();
        await panel.Pending;

        Assert.Equal("DATA NOT UPDATING", panel.ConnectionText);
        Assert.Equal("STALE", panel.Tiles["oven-temp"].StateText);
        Assert.Contains("Not live", panel.Tiles["oven-temp"].LastValueText);
    }
}

/// <summary>A stand-in for the Pi on 127.0.0.1:8702.</summary>
public sealed class FakeService : IDisposable
{
    public const int Port = 8702;

    private readonly HttpListener listener = new();
    private readonly CancellationTokenSource stopping = new();
    private readonly Task loop;

    public FakeService()
    {
        BaseUrl = new Uri($"http://127.0.0.1:{Port}/");
        listener.Prefixes.Add(BaseUrl.ToString());
        listener.Start();
        loop = Task.Run(Serve);
    }

    public Uri BaseUrl { get; }

    public string Body { get; set; } = "{}";

    public int StatusCode { get; set; } = 200;

    public List<string> Requests { get; } = new();

    private async Task Serve()
    {
        while (!stopping.IsCancellationRequested)
        {
            HttpListenerContext context;
            try
            {
                context = await listener.GetContextAsync();
            }
            catch (Exception)
            {
                return;
            }

            lock (Requests)
            {
                Requests.Add($"{context.Request.HttpMethod} {context.Request.Url?.AbsolutePath}");
            }

            try
            {
                byte[] data = Encoding.UTF8.GetBytes(Body);
                context.Response.StatusCode = StatusCode;
                context.Response.ContentType = "application/json";
                context.Response.ContentLength64 = data.Length;
                await context.Response.OutputStream.WriteAsync(data);
                context.Response.Close();
            }
            catch (Exception)
            {
                context.Response.Abort();
            }
        }
    }

    public void Dispose()
    {
        stopping.Cancel();
        listener.Stop();
        listener.Close();
        try
        {
            loop.Wait(TimeSpan.FromSeconds(5));
        }
        catch (AggregateException)
        {
        }

        stopping.Dispose();
    }
}
