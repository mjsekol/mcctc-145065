// Program.cs  .  Lab U08-02  .  given to you
//
// Polls the Line 3 sensor service and prints one line per poll.
//
//   dotnet run --project LiveReader
//   dotnet run --project LiveReader -- --url http://127.0.0.1:8700 --polls 5 --timeout 1.5
//
// THE HEARTBEAT COLUMN. While a poll is out, this program counts 100 ms
// heartbeats. It can only count them if PollAsync handed control back while
// it waited. A PollAsync that blocks returns a finished task, so the count is
// 0 no matter how long the poll took. On a panel, a blocked thread is a
// frozen window.
//
// THE TIME COLUMN is when this program noticed the reply. It looks once every
// 100 ms, so a reply that took 5 ms shows as about 0.11 s and 1 heartbeat.
// That is the heartbeat's resolution, not the network.

using System.Diagnostics;
using System.Globalization;
using Line3.Hmi.Core;

Uri url = new("http://127.0.0.1:8700");
int polls = 10;
double timeoutSeconds = 1.5;

for (int i = 0; i < args.Length - 1; i += 2)
{
    switch (args[i])
    {
        case "--url":
            url = new Uri(args[i + 1]);
            break;
        case "--polls":
            polls = int.Parse(args[i + 1], CultureInfo.InvariantCulture);
            break;
        case "--timeout":
            timeoutSeconds = double.Parse(args[i + 1], CultureInfo.InvariantCulture);
            break;
        default:
            Console.Error.WriteLine($"Unknown option {args[i]}. Use --url, --polls, --timeout.");
            return 2;
    }
}

using ReadingClient client = new(url, TimeSpan.FromSeconds(timeoutSeconds));
Console.WriteLine(string.Create(CultureInfo.InvariantCulture,
    $"LiveReader: polling {client.ReadingsUrl} every 1.0 s, {timeoutSeconds:0.0} s timeout"));

for (int poll = 1; poll <= polls; poll++)
{
    Stopwatch timer = Stopwatch.StartNew();
    Task<PollResult> pending;
    try
    {
        pending = client.PollAsync();
    }
    catch (NotImplementedException problem)
    {
        Console.WriteLine($"poll {poll,2}  {problem.Message}");
        return 0;
    }

    // Count heartbeats until the poll finishes.
    int heartbeats = 0;
    while (!pending.IsCompleted)
    {
        await Task.Delay(100);
        heartbeats++;
    }

    PollResult result = await pending;
    string took = string.Create(CultureInfo.InvariantCulture, $"{timer.Elapsed.TotalSeconds:0.00} s");
    Console.WriteLine($"poll {poll,2}  {Describe(result)}  ({took}, heartbeats {heartbeats})");

    // Start to start: a slow poll shortens the wait.
    TimeSpan rest = TimeSpan.FromSeconds(1) - timer.Elapsed;
    if (rest > TimeSpan.Zero && poll < polls)
    {
        await Task.Delay(rest);
    }
}

return 0;

static string Describe(PollResult result)
{
    if (!result.Ok)
    {
        return $"{result.Failure.ToString().ToUpperInvariant(),-15} {result.Detail}";
    }

    ReadingSnapshot snapshot = result.Snapshot!;
    IEnumerable<string> sensors = snapshot.Sensors.Select(s => s.Ok
        ? string.Create(CultureInfo.InvariantCulture, $"{s.Id} {s.Value:0.0} {s.Unit}")
        : $"{s.Id} NO READING");
    return $"{"OK",-15} seq {snapshot.Sequence,-5} {string.Join("  ", sensors)}";
}
