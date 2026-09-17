// ReadingClientChecks.cs  .  Lab U08-02 self-check  .  given to you
//
//   dotnet test LiveReader.SelfCheck
//
// Uses port 8702 for the fake service and expects port 8704 to be free.
// Every reply below is invented sample data in the Line 3 contract's shape.

using System.Diagnostics;
using Line3.Hmi.Core;

namespace LiveReader.SelfCheck;

[Collection("network")]
public class ReadingClientChecks
{
    private const string Good = """
        {"device": "line3-pi", "sequence": 1042, "sampled_at": "2027-01-11T14:03:22Z",
         "sensors": [
           {"id": "oven-temp", "kind": "temperature", "value": 212.4, "unit": "C", "ok": true},
           {"id": "press-vibration", "kind": "vibration", "value": 3.1, "unit": "mm/s", "ok": true},
           {"id": "coolant-level", "kind": "level", "value": null, "unit": "%", "ok": false}]}
        """;

    private const string Garbage = "{\"device\": \"line3-pi\", \"sequence\": 17, \"sampled_at\": \"2027-01-11T14:0";

    private static ReadingClient ClientFor(Uri url, double timeoutSeconds = 1.0) =>
        new(url, TimeSpan.FromSeconds(timeoutSeconds));

    [Fact]
    public async Task S01_AGoodReplyIsASnapshot()
    {
        using FakeService fake = new() { Body = Good };
        using ReadingClient client = ClientFor(fake.BaseUrl);

        PollResult result = await client.PollAsync();

        Assert.True(result.Ok, $"expected OK, got {result.Failure}: {result.Detail}");
        Assert.Equal(1042, result.Snapshot!.Sequence);
        Assert.Equal(3, result.Snapshot.Sensors.Count);
        Assert.Null(result.Snapshot.Find("coolant-level")!.Value);
    }

    [Fact]
    public async Task S02_ItAsksForApiReadingsWithAGet()
    {
        using FakeService fake = new() { Body = Good };
        using ReadingClient client = ClientFor(fake.BaseUrl);

        await client.PollAsync();

        Assert.Equal("/api/readings", fake.LastPath);
        Assert.Equal("GET", fake.LastMethod);
    }

    [Fact]
    public async Task S03_ReceivedAtIsNow()
    {
        using FakeService fake = new() { Body = Good };
        using ReadingClient client = ClientFor(fake.BaseUrl);

        PollResult result = await client.PollAsync();

        Assert.True((DateTimeOffset.UtcNow - result.ReceivedAt).Duration() < TimeSpan.FromSeconds(5),
            "ReceivedAt should be the time the reply arrived, by this PC's clock");
    }

    [Theory]
    [InlineData(404)]
    [InlineData(500)]
    [InlineData(503)]
    public async Task S04_AnyStatusOtherThan200IsAnHttpError(int status)
    {
        using FakeService fake = new() { Body = "{\"error\": \"no\"}", StatusCode = status };
        using ReadingClient client = ClientFor(fake.BaseUrl);

        PollResult result = await client.PollAsync();

        Assert.Equal(PollFailure.HttpError, result.Failure);
        Assert.Null(result.Snapshot);
    }

    [Theory]
    [InlineData(Garbage)]
    [InlineData("")]
    [InlineData("[1, 2, 3]")]
    public async Task S05_A200ThatIsNotTheContractIsMalformed(string body)
    {
        using FakeService fake = new() { Body = body };
        using ReadingClient client = ClientFor(fake.BaseUrl);

        PollResult result = await client.PollAsync();

        Assert.Equal(PollFailure.MalformedReply, result.Failure);
        Assert.Null(result.Snapshot);
    }

    [Fact]
    public async Task S06_ASlowServiceIsATimeoutThatEndsOnTime()
    {
        using FakeService fake = new() { Body = Good, Delay = TimeSpan.FromSeconds(4) };
        using ReadingClient client = ClientFor(fake.BaseUrl, timeoutSeconds: 0.5);

        Stopwatch timer = Stopwatch.StartNew();
        PollResult result = await client.PollAsync();

        Assert.Equal(PollFailure.Timeout, result.Failure);
        Assert.InRange(timer.Elapsed.TotalSeconds, 0.4, 2.0);
    }

    [Fact]
    public async Task S07_NothingListeningIsServiceDown()
    {
        const int unused = 8704;
        Assert.True(FakeService.IsFree(unused), "port 8704 must be free for this check");

        // Windows can take about 2 s to report a refused connection. This
        // check allows 5 s so it sees the refusal itself, not a timeout.
        using ReadingClient client = ClientFor(new Uri($"http://127.0.0.1:{unused}"), timeoutSeconds: 5);

        PollResult result = await client.PollAsync();

        Assert.Equal(PollFailure.ServiceDown, result.Failure);
        Assert.Null(result.Snapshot);
    }

    [Fact]
    public async Task S08_PollAsyncHandsBackControlBeforeTheReplyArrives()
    {
        // The "never freeze the window" promise, measured. A PollAsync that
        // blocks holds the caller here for the whole delay.
        using FakeService fake = new() { Body = Good, Delay = TimeSpan.FromMilliseconds(800) };
        using ReadingClient client = ClientFor(fake.BaseUrl, timeoutSeconds: 3);

        Stopwatch timer = Stopwatch.StartNew();
        Task<PollResult> pending = client.PollAsync();
        TimeSpan handedBack = timer.Elapsed;

        Assert.False(pending.IsCompleted, "PollAsync finished before the service answered, so it blocked");
        Assert.True(handedBack < TimeSpan.FromMilliseconds(300), $"PollAsync held the caller for {handedBack.TotalMilliseconds:0} ms");
        Assert.True((await pending).Ok);
    }

    [Fact]
    public async Task S09_CallerCancellationIsNotReportedAsATimeout()
    {
        using FakeService fake = new() { Body = Good, Delay = TimeSpan.FromSeconds(4) };
        using ReadingClient client = ClientFor(fake.BaseUrl, timeoutSeconds: 3);
        using CancellationTokenSource cancel = new(TimeSpan.FromMilliseconds(200));

        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => client.PollAsync(cancel.Token));
    }

    [Fact]
    public async Task S10_AnOversizedReplyIsAFailureNotACrash()
    {
        // 200 KB of spaces, then the good reply. Valid JSON, and far too big.
        using FakeService fake = new() { Body = new string(' ', 200_000) + Good };
        using ReadingClient client = ClientFor(fake.BaseUrl, timeoutSeconds: 3);

        PollResult result = await client.PollAsync();

        Assert.False(result.Ok, "a reply over 64 KB must not be trusted");
        Assert.Null(result.Snapshot);
    }
}
