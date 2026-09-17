// StateRules.cs  .  HMI PANEL project  .  given to you (the same file as Lab U08-03)
//
// The names the whole course uses for what a panel knows about one sensor.
// The same file ships in the HMI PANEL project, so your Decide pastes
// straight in.
//
// The four states (build brief definitions, used all course):
//
//   MISSING  there is no current value: the request failed or timed out,
//            the reply was unreadable, or the sensor reported ok: false
//   STALE    the panel has a value, but the sample is older than the stale
//            limit, so it is not live
//   ALARM    a LIVE value outside its documented limits
//   NORMAL   a LIVE value inside its documented limits
//
// Riverside Fabrication, Line 3, is a composite. It is not a real shop.

namespace Line3.Hmi.Core;

public enum SensorState
{
    Normal,
    Alarm,
    Stale,
    Missing,
}

/// <summary>Why the panel has no current value for a sensor.</summary>
public enum MissingReason
{
    None,
    WaitingForFirstReply,
    ServiceDown,
    Timeout,
    HttpError,
    MalformedReply,
    NotInReply,
    SensorFailed,
    UnitMismatch,
}

/// <summary>Why a value the panel has is not live.</summary>
public enum StaleReason
{
    None,
    SampleTooOld,
    SequenceNotAdvancing,
    ClockDisagrees,
}

public enum AlarmSide
{
    None,
    Low,
    High,
}

public static partial class StateRules
{
    /// <summary>Which side of its limits a value fell on.</summary>
    public static AlarmSide SideOf(LimitCheck check) => check switch
    {
        LimitCheck.BelowLow => AlarmSide.Low,
        LimitCheck.AboveHigh => AlarmSide.High,
        _ => AlarmSide.None,
    };
}
