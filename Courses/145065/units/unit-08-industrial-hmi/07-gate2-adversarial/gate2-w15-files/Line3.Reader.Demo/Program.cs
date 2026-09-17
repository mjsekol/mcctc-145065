using System.Globalization;
using Line3.Reader;

// Usage: dotnet run --project Line3.Reader.Demo -- [--url http://127.0.0.1:8700] [--seconds 5]
LimitsFile limits = LimitsFile.Load(Path.Combine(AppContext.BaseDirectory, "limits.json"));
double seconds = 5;
for (int i = 0; i + 1 < args.Length; i += 2)
{
    if (args[i] == "--url")
    {
        limits.ServiceUrl = new Uri(args[i + 1].TrimEnd('/') + "/");
    }
    else if (args[i] == "--seconds")
    {
        seconds = double.Parse(args[i + 1], CultureInfo.InvariantCulture);
    }
}

using HttpReadingSource source = new(limits);
DateTime started = DateTime.Now;
Poller poller = new(source, result =>
{
    string at = (DateTime.Now - started).TotalSeconds.ToString("0.00", CultureInfo.InvariantCulture);
    if (!result.Ok)
    {
        Console.WriteLine($"{at,6} s  FAILED  {result.Problem}");
        return;
    }

    IEnumerable<string> shown = result.Batch!.Sensors.Select(s =>
        string.Create(CultureInfo.InvariantCulture, $"{s.Id} {s.Value:0.0} {s.Unit} {AlarmRules.Evaluate(s, limits.Find(s.Id))}"));
    Console.WriteLine($"{at,6} s  seq {result.Batch.Sequence,-4}  {string.Join("  ", shown)}");
});

using CancellationTokenSource stop = new(TimeSpan.FromSeconds(seconds));
await poller.RunAsync(stop.Token);
Console.WriteLine($"{poller.Completed} reads in {seconds} s");
