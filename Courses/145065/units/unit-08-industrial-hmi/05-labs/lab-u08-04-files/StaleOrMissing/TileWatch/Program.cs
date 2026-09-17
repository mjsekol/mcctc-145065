// Program.cs  .  Lab U08-04  .  TileWatch  .  given to you
//
//   dotnet run --project TileWatch
//
// Plays four scripted scenes on a clock that only moves when this program
// moves it, and prints what ONE oven tile would show each second. It uses
// YOUR CheckFreshness and YOUR Apply. No service is needed.
//
// The times are invented sample data. Riverside Fabrication is a composite.

using System.Globalization;
using Line3.Hmi.Core;
using Line3.Hmi.Core.ViewModels;

TimeSpan staleAfter = TimeSpan.FromSeconds(5);
SensorThreshold oven = new("oven-temp", "Cure oven temperature", "C", 1, 190.0, 230.0,
    "Line 3 coating cures between 190 and 230 C (composite shop).");
DateTimeOffset t0 = new(2027, 1, 11, 14, 3, 22, TimeSpan.Zero);

Scene("1. The Pi freezes: sample 50, taken at t=0, is sent again and again.",
    second => new Reply(true, 212.4, t0, t0));

Scene("2. The Pi stamps the same sample with the current time every second.",
    second => new Reply(true, 212.4, t0.AddSeconds(second), t0));

Scene("3. The cable is pulled at t=3.",
    second => second < 3
        ? new Reply(true, 212.0 + (second * 0.1), t0.AddSeconds(second), t0.AddSeconds(second))
        : new Reply(false, null, t0, t0));

Scene("4. The Pi's clock is ten minutes ahead of the panel's.",
    second => new Reply(true, 212.4, t0.AddMinutes(10).AddSeconds(second), t0.AddSeconds(second)));

return 0;

void Scene(string title, Func<int, Reply> replyAt)
{
    Console.WriteLine(title);
    SensorTileViewModel tile = new(oven, _ => { });
    for (int second = 0; second <= 7; second++)
    {
        DateTimeOffset now = t0.AddSeconds(second);
        Reply reply = replyAt(second);
        tile.Apply(Evaluate(oven, reply, now, staleAfter));
        string last = tile.HasLastKnown ? "  [" + tile.LastKnownText + "]" : string.Empty;
        Console.WriteLine($"  t={second}  {tile.StateText,-11} {tile.ValueText,-9}{last}".TrimEnd());
    }

    Console.WriteLine($"  explanation at t=7: {tile.Explanation}");
    Console.WriteLine();
}

// A small version of what the panel's PanelMonitor does for one sensor.
static SensorStatus Evaluate(SensorThreshold t, Reply reply, DateTimeOffset now, TimeSpan staleAfter)
{
    if (!reply.HaveAnswer)
    {
        return new SensorStatus(t, SensorState.Missing, null, null, null, AlarmSide.None,
            MissingReason.ServiceDown, StaleReason.None, AlarmLatchState.Clear,
            "No connection to the sensor service. The panel cannot see this value. Check it at the machine.");
    }

    StaleReason stale = StateRules.CheckFreshness(now, reply.SampledAt, reply.SequenceAdvancedAt, staleAfter);
    LimitCheck check = t.Check(reply.Value!.Value);
    SensorState state = StateRules.Decide(true, true, stale == StaleReason.None, check == LimitCheck.Within);

    return state switch
    {
        SensorState.Stale => new SensorStatus(t, state, null, reply.Value, Age(now, reply, stale),
            AlarmSide.None, MissingReason.None, stale, AlarmLatchState.Clear,
            stale == StaleReason.ClockDisagrees
                ? "The Pi's clock and the panel's clock disagree, so the panel cannot tell how old this value is. It is not live."
                : "Not updated for " + PanelMonitor.FormatAge(Age(now, reply, stale)) + ", so it is not live."),
        SensorState.Alarm => new SensorStatus(t, state, reply.Value, null, null, StateRules.SideOf(check),
            MissingReason.None, StaleReason.None, AlarmLatchState.Clear, "Live. Outside limits."),
        _ => new SensorStatus(t, state, reply.Value, null, null, AlarmSide.None,
            MissingReason.None, StaleReason.None, AlarmLatchState.Clear, "Live. Inside limits."),
    };
}

static TimeSpan Age(DateTimeOffset now, Reply reply, StaleReason stale)
{
    TimeSpan bySequence = now - reply.SequenceAdvancedAt;
    TimeSpan byClock = now - reply.SampledAt;
    return stale == StaleReason.ClockDisagrees || bySequence > byClock ? bySequence : byClock;
}

// What the panel knows after one poll: did it get an answer, the oven value,
// when the sample says it was taken, and when the sequence last changed.
internal sealed record Reply(bool HaveAnswer, double? Value, DateTimeOffset SampledAt, DateTimeOffset SequenceAdvancedAt);
