using System.Diagnostics;
using System.Globalization;
using Line3.FailSafe;

// Usage: dotnet run --project Line3.FailSafe.Demo -- [--url http://127.0.0.1:8700] [--seconds 10]
//
// This loop stands in for a window's UI thread. A real window needs a turn about
// every 100 ms to repaint and answer the mouse. Each line reports the longest
// time the loop waited for its next turn during that second.
Uri url = new("http://127.0.0.1:8700/");
double seconds = 10;
for (int i = 0; i + 1 < args.Length; i += 2)
{
    if (args[i] == "--url")
    {
        url = new Uri(args[i + 1].TrimEnd('/') + "/");
    }
    else if (args[i] == "--seconds")
    {
        seconds = double.Parse(args[i + 1], CultureInfo.InvariantCulture);
    }
}

SensorLimit[] limits =
{
    new("oven-temp", "Oven", "C", 190.0, 230.0),
    new("press-vibration", "Press", "mm/s", null, 6.0),
    new("coolant-level", "Coolant", "%", 25.0, null),
};

using LinePanel panel = new(url, limits);
Stopwatch clock = Stopwatch.StartNew();
TimeSpan nextTick = TimeSpan.Zero;
TimeSpan lastTurn = TimeSpan.Zero;
TimeSpan worstWait = TimeSpan.Zero;
int second = 0;

while (clock.Elapsed.TotalSeconds < seconds)
{
    TimeSpan now = clock.Elapsed;
    if (now - lastTurn > worstWait)
    {
        worstWait = now - lastTurn;
    }

    lastTurn = now;
    if (now >= nextTick)
    {
        panel.Tick();
        nextTick += TimeSpan.FromSeconds(1);
        TimeSpan tickTook = clock.Elapsed - now;
        if (tickTook > worstWait)
        {
            worstWait = tickTook;
        }

        IEnumerable<string> tiles = panel.Tiles.Values.Select(t => t.ToString());
        Console.WriteLine($"t={second,-3} {panel.ConnectionText,-17} {string.Join(" | ", tiles)}   (screen waited up to {worstWait.TotalMilliseconds:0} ms)");
        second++;
        worstWait = TimeSpan.Zero;
        lastTurn = clock.Elapsed;
    }

    Thread.Sleep(100);
}
