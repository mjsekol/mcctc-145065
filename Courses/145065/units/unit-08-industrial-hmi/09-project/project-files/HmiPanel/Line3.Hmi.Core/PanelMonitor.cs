// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/PanelMonitor.cs.
// Given to you. Read it; you do not need to change it.
//
// PanelMonitor.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// The panel's memory. It holds three things and nothing else:
//
//   1. the last poll result, good or bad
//   2. when, by the PANEL's clock, the sequence number last changed
//   3. each sensor's alarm latch
//
// Record(result) stores a poll result. Update(now) turns what is stored into
// one SensorStatus per sensor, moves the alarm latches, and reports what
// changed as PanelEvents. Update is safe to call as often as you like: with
// nothing new recorded, a second call changes nothing and reports nothing,
// except that ages grow and a fresh value can turn stale.
//
// Nothing here reads a clock or a network. Time arrives as a parameter.

using System.Globalization;

namespace Line3.Hmi.Core;

/// <summary>Everything the panel shows for one sensor at one moment.</summary>
public sealed record SensorStatus(
    SensorThreshold Threshold,
    SensorState State,
    double? LiveValue,
    double? LastKnownValue,
    TimeSpan? LastKnownAge,
    AlarmSide Side,
    MissingReason Missing,
    StaleReason Stale,
    AlarmLatchState Latch,
    string Explanation)
{
    public string SensorId => Threshold.Id;
}

public enum ConnectionState
{
    Waiting,
    Connected,
    NotUpdating,
    Lost,
}

public sealed record ConnectionStatus(
    ConnectionState State,
    long? Sequence,
    TimeSpan? SinceLastGoodReply,
    PollFailure LastFailure,
    string Detail);

public sealed record PanelEvent(DateTimeOffset At, string Text);

public sealed record PanelUpdate(
    IReadOnlyList<SensorStatus> Sensors,
    ConnectionStatus Connection,
    IReadOnlyList<PanelEvent> Events);

public sealed class PanelMonitor
{
    private readonly PanelConfig config;
    private readonly Dictionary<string, AlarmLatchState> latches = new(StringComparer.Ordinal);
    private readonly Dictionary<string, (SensorState, MissingReason)> lastStates = new(StringComparer.Ordinal);
    private PollResult? lastResult;
    private DateTimeOffset? lastGoodReceivedAt;
    private string? lastDevice;
    private long? lastSequence;
    private DateTimeOffset sequenceAdvancedAt;
    private ConnectionState lastConnection = ConnectionState.Waiting;

    public PanelMonitor(PanelConfig config)
    {
        this.config = config;
        foreach (SensorThreshold threshold in config.Sensors)
        {
            latches[threshold.Id] = AlarmLatchState.Clear;
            lastStates[threshold.Id] = (SensorState.Missing, MissingReason.WaitingForFirstReply);
        }
    }

    public PanelConfig Config => config;

    public AlarmLatchState LatchOf(string sensorId) => latches[sensorId];

    public void Record(PollResult result)
    {
        lastResult = result;
        if (!result.Ok)
        {
            return;
        }

        ReadingSnapshot snapshot = result.Snapshot!;

        // Any change counts as new, including a lower number: a Pi that
        // restarted begins counting again, and its first sample is new.
        if (lastSequence != snapshot.Sequence || lastDevice != snapshot.Device)
        {
            lastSequence = snapshot.Sequence;
            lastDevice = snapshot.Device;
            sequenceAdvancedAt = result.ReceivedAt;
        }

        lastGoodReceivedAt = result.ReceivedAt;
    }

    /// <summary>A person acknowledged this sensor's alarm. True when that changed anything.</summary>
    public bool Acknowledge(string sensorId, DateTimeOffset now, out PanelEvent? acknowledged)
    {
        acknowledged = null;
        AlarmLatchState before = latches[sensorId];
        AlarmLatchState after = AlarmLatch.Acknowledge(before);
        if (after == before)
        {
            return false;
        }

        latches[sensorId] = after;
        string label = config.Sensors.First(s => s.Id == sensorId).Label;
        acknowledged = new PanelEvent(now, after == AlarmLatchState.Clear
            ? $"{label}: alarm acknowledged and cleared"
            : $"{label}: alarm acknowledged, still active");
        return true;
    }

    public PanelUpdate Update(DateTimeOffset now)
    {
        List<SensorStatus> statuses = new();
        List<PanelEvent> events = new();

        ConnectionStatus connection = EvaluateConnection(now);
        if (connection.State != lastConnection)
        {
            string? text = connection.State switch
            {
                ConnectionState.Lost => "Connection lost: " + connection.Detail,
                ConnectionState.NotUpdating => "Data stopped updating: " + connection.Detail,
                ConnectionState.Connected when lastConnection != ConnectionState.Waiting => "Live data restored",
                ConnectionState.Connected => "Connected to the sensor service",
                _ => null,
            };
            if (text is not null)
            {
                events.Add(new PanelEvent(now, text));
            }

            lastConnection = connection.State;
        }

        foreach (SensorThreshold threshold in config.Sensors)
        {
            SensorStatus evaluated = Evaluate(threshold, lastResult, sequenceAdvancedAt, now, config.StaleAfter);
            AlarmLatchState before = latches[threshold.Id];
            AlarmLatchState after = AlarmLatch.Next(before, evaluated.State);
            latches[threshold.Id] = after;
            SensorStatus status = evaluated with { Latch = after };
            statuses.Add(status);

            if (before != after)
            {
                events.Add(new PanelEvent(now, after switch
                {
                    AlarmLatchState.ActiveUnacked => $"{threshold.Label}: ALARM {status.Side.ToString().ToUpperInvariant()}, {threshold.Format(status.LiveValue!.Value)} {threshold.Unit}",
                    AlarmLatchState.ReturnedUnacked => $"{threshold.Label}: back inside limits, alarm not yet acknowledged",
                    AlarmLatchState.Clear => $"{threshold.Label}: back inside limits, alarm cleared",
                    _ => $"{threshold.Label}: alarm state {after}",
                }));
            }
            else if (lastStates[threshold.Id] != (status.State, status.Missing)
                     && status.State is SensorState.Missing or SensorState.Stale
                     && connection.State == ConnectionState.Connected)
            {
                // Connection-wide losses are already reported once above.
                events.Add(new PanelEvent(now, $"{threshold.Label}: {status.Explanation}"));
            }

            lastStates[threshold.Id] = (status.State, status.Missing);
        }

        return new PanelUpdate(statuses, connection, events);
    }

    /// <summary>
    /// One sensor, from what is stored. Pure: the latch in the result is a
    /// placeholder (Clear) that <see cref="Update"/> replaces.
    /// </summary>
    public static SensorStatus Evaluate(
        SensorThreshold threshold,
        PollResult? lastResult,
        DateTimeOffset sequenceAdvancedAt,
        DateTimeOffset now,
        TimeSpan staleAfter)
    {
        if (lastResult is null)
        {
            return MissingStatus(threshold, MissingReason.WaitingForFirstReply,
                "Waiting for the first reading from the sensor service.");
        }

        if (!lastResult.Ok)
        {
            (MissingReason reason, string what) = lastResult.Failure switch
            {
                PollFailure.ServiceDown => (MissingReason.ServiceDown, "No connection to the sensor service."),
                PollFailure.Timeout => (MissingReason.Timeout, "The sensor service did not answer in time."),
                PollFailure.HttpError => (MissingReason.HttpError, "The sensor service answered with an error."),
                _ => (MissingReason.MalformedReply, "The sensor service sent a reply the panel cannot read."),
            };
            return MissingStatus(threshold, reason, what + " The panel cannot see this value. Check it at the machine.");
        }

        ReadingSnapshot snapshot = lastResult.Snapshot!;
        SensorSample? sample = snapshot.Find(threshold.Id);
        bool haveAnswer = true;

        if (sample is null)
        {
            return MissingStatus(threshold, MissingReason.NotInReply,
                "The sensor service did not report this sensor. Check it at the machine.");
        }

        if (sample.Ok && !string.Equals(sample.Unit, threshold.Unit, StringComparison.Ordinal))
        {
            return MissingStatus(threshold, MissingReason.UnitMismatch,
                $"The sensor reports in {sample.Unit} but the limits are in {threshold.Unit}. The panel will not compare them.");
        }

        StaleReason stale = StateRules.CheckFreshness(now, snapshot.SampledAt, sequenceAdvancedAt, staleAfter);
        bool fresh = stale == StaleReason.None;
        LimitCheck check = sample.Ok ? threshold.Check(sample.Value!.Value) : LimitCheck.Within;

        SensorState state = StateRules.Decide(haveAnswer, sample.Ok, fresh, check == LimitCheck.Within);

        switch (state)
        {
            case SensorState.Missing:
                string why = sample.ContractProblem is null ? string.Empty : $" ({sample.ContractProblem})";
                return MissingStatus(threshold, MissingReason.SensorFailed,
                    $"The sensor did not give a reading{why}. Check it at the machine.");

            case SensorState.Stale:
                TimeSpan byClock = now - snapshot.SampledAt;
                TimeSpan bySequence = now - sequenceAdvancedAt;
                TimeSpan age = stale == StaleReason.ClockDisagrees ? bySequence : Max(byClock, bySequence);
                string explanation = stale == StaleReason.ClockDisagrees
                    ? "The Pi's clock and the panel's clock disagree, so the panel cannot tell how old this value is. It is not live."
                    : $"Not updated for {FormatAge(age)}, so it is not live. It may not match the machine now.";
                return new SensorStatus(threshold, SensorState.Stale, null, sample.Value, age,
                    AlarmSide.None, MissingReason.None, stale, AlarmLatchState.Clear, explanation);

            case SensorState.Alarm:
                AlarmSide side = StateRules.SideOf(check);
                string limit = side == AlarmSide.High
                    ? $"above the high limit of {threshold.Format(threshold.High!.Value)} {threshold.Unit}"
                    : $"below the low limit of {threshold.Format(threshold.Low!.Value)} {threshold.Unit}";
                return new SensorStatus(threshold, SensorState.Alarm, sample.Value, null, null,
                    side, MissingReason.None, StaleReason.None, AlarmLatchState.Clear, $"Live. {Capitalize(limit)}.");

            default:
                return new SensorStatus(threshold, SensorState.Normal, sample.Value, null, null,
                    AlarmSide.None, MissingReason.None, StaleReason.None, AlarmLatchState.Clear, "Live. Inside limits.");
        }
    }

    private ConnectionStatus EvaluateConnection(DateTimeOffset now)
    {
        TimeSpan? sinceGood = lastGoodReceivedAt is DateTimeOffset at ? now - at : null;

        if (lastResult is null)
        {
            return new ConnectionStatus(ConnectionState.Waiting, null, null, PollFailure.None,
                "Waiting for the first reading");
        }

        if (!lastResult.Ok)
        {
            string since = sinceGood is TimeSpan s ? $"last good reading {FormatAge(s)} ago" : "no good reading yet";
            string cause = lastResult.Failure switch
            {
                PollFailure.ServiceDown => "no connection",
                PollFailure.Timeout => "no answer in time",
                PollFailure.HttpError => "the service reported an error",
                _ => "unreadable reply",
            };
            return new ConnectionStatus(ConnectionState.Lost, lastSequence, sinceGood, lastResult.Failure,
                $"{cause}, {since}");
        }

        ReadingSnapshot snapshot = lastResult.Snapshot!;
        StaleReason stale = StateRules.CheckFreshness(now, snapshot.SampledAt, sequenceAdvancedAt, config.StaleAfter);
        if (stale != StaleReason.None)
        {
            string detail = stale == StaleReason.ClockDisagrees
                ? $"sample {snapshot.Sequence} is stamped in the future; check the Pi's clock"
                : $"sample {snapshot.Sequence} has not changed for {FormatAge(now - sequenceAdvancedAt)}";
            return new ConnectionStatus(ConnectionState.NotUpdating, snapshot.Sequence, sinceGood, PollFailure.None, detail);
        }

        return new ConnectionStatus(ConnectionState.Connected, snapshot.Sequence, sinceGood, PollFailure.None,
            $"sample {snapshot.Sequence}, taken {FormatAge(Max(now - snapshot.SampledAt, TimeSpan.Zero))} ago");
    }

    private static SensorStatus MissingStatus(SensorThreshold threshold, MissingReason reason, string explanation) =>
        new(threshold, SensorState.Missing, null, null, null, AlarmSide.None, reason, StaleReason.None,
            AlarmLatchState.Clear, explanation);

    private static TimeSpan Max(TimeSpan a, TimeSpan b) => a > b ? a : b;

    private static string Capitalize(string text) =>
        text.Length == 0 ? text : char.ToUpperInvariant(text[0]) + text[1..];

    /// <summary>"0.4 s", "12 s", "3 min 05 s", "2 h 07 min".</summary>
    public static string FormatAge(TimeSpan age)
    {
        if (age < TimeSpan.Zero)
        {
            age = TimeSpan.Zero;
        }

        if (age < TimeSpan.FromSeconds(10))
        {
            return age.TotalSeconds.ToString("0.0", CultureInfo.InvariantCulture) + " s";
        }

        if (age < TimeSpan.FromMinutes(1))
        {
            return ((int)age.TotalSeconds).ToString(CultureInfo.InvariantCulture) + " s";
        }

        if (age < TimeSpan.FromHours(1))
        {
            return $"{(int)age.TotalMinutes} min {age.Seconds:00} s";
        }

        return $"{(int)age.TotalHours} h {age.Minutes:00} min";
    }
}
