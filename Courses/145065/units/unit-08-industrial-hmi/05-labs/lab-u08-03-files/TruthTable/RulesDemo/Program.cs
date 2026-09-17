// Program.cs  .  Lab U08-03  .  given to you
//
//   dotnet run --project RulesDemo
//
// Prints the truth table YOUR Decide produces, then your team's limits from
// thresholds.json with the values on each side of every limit, checked by
// YOUR SensorThreshold.Check.

using System.Globalization;
using Line3.Hmi.Core;

Console.WriteLine("Truth table from your StateRules.Decide");
Console.WriteLine("  A      K      F      W      state");
Dictionary<SensorState, int> counts = new();
bool[] both = { false, true };
foreach (bool a in both)
foreach (bool k in both)
foreach (bool f in both)
foreach (bool w in both)
{
    SensorState state = StateRules.Decide(a, k, f, w);
    counts[state] = counts.GetValueOrDefault(state) + 1;
    Console.WriteLine($"  {Word(a),-6} {Word(k),-6} {Word(f),-6} {Word(w),-6} {state}");
}

Console.WriteLine("16 rows: " + string.Join(", ",
    Enum.GetValues<SensorState>().Select(s => $"{s} {counts.GetValueOrDefault(s)}")));
Console.WriteLine();

string path = Path.Combine(AppContext.BaseDirectory, "thresholds.json");
PanelConfig config;
try
{
    config = PanelConfig.Load(path);
}
catch (PanelConfigException problem)
{
    Console.WriteLine("thresholds.json was refused: " + problem.Message);
    return 1;
}

Console.WriteLine("Limits from thresholds.json");
foreach (SensorThreshold t in config.Sensors)
{
    Console.WriteLine($"  {t.Label}: {t.LimitsText}");
    if (t.Reason.StartsWith("REPLACE THIS", StringComparison.Ordinal))
    {
        Console.WriteLine("    reason: STILL THE PLACEHOLDER. Your team writes this one (step 11).");
    }

    // One display step either side of each limit: 0.1 for one decimal, 1 for none.
    double step = Math.Pow(10, -t.Decimals);
    List<string> checks = new();
    if (t.Low is double low)
    {
        checks.Add(Show(t, low - step));
        checks.Add(Show(t, low));
    }

    if (t.High is double high)
    {
        checks.Add(Show(t, high));
        checks.Add(Show(t, high + step));
    }

    Console.WriteLine("    " + string.Join("   ", checks));
}

return 0;

static string Word(bool value) => value ? "true" : "false";

static string Show(SensorThreshold t, double value) =>
    string.Create(CultureInfo.InvariantCulture, $"{t.Format(value)} -> {t.Check(Math.Round(value, 6))}");
