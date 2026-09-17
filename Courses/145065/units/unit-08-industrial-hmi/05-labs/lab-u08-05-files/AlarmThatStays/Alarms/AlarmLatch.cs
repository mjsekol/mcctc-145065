// AlarmLatch.cs  .  Lab U08-05  .  STARTER. You write Next and Acknowledge.
//
// An alarm is not the same thing as a red number. The number goes away the
// moment the data stops. The alarm must not.
//
// The latch remembers that an alarm happened. It has four states:
//
//   Clear            nothing to report
//   ActiveUnacked    the value is out of limits, and nobody has acknowledged
//   ActiveAcked      the value is out of limits, and a person acknowledged it
//   ReturnedUnacked  the value came back inside limits, and nobody has
//                    acknowledged the alarm that happened
//
// THE RULES (build your table from these in step 2, before any code):
//
//   1. A live value out of limits makes the alarm active. If a person
//      already acknowledged it, it stays acknowledged.
//   2. A live value back inside limits ends an active alarm. An
//      acknowledged alarm then clears. An unacknowledged one becomes
//      ReturnedUnacked, because someone still needs to see that it happened.
//   3. Stale or missing data changes NOTHING. The panel does not know, so it
//      does not guess. This is the fail-safe rule.
//   4. Acknowledging an active alarm marks it acknowledged. It does not clear
//      it: only a live value inside limits does that.
//   5. Acknowledging a returned alarm clears it.
//   6. Acknowledging when there is nothing to acknowledge changes nothing.
//
// Alarm management standards describe a fuller version of this idea. This is
// the smallest version that keeps the fail-safe promise.

namespace Line3.Hmi.Core;

public enum AlarmLatchState
{
    Clear,
    ActiveUnacked,
    ActiveAcked,
    ReturnedUnacked,
}

public static class AlarmLatch
{
    /// <summary>The next latch state after the panel evaluates a sensor.</summary>
    public static AlarmLatchState Next(AlarmLatchState current, SensorState evaluated)
    {
        // TODO step 4 (rules 1 to 3). The starter never moves the latch, so
        // no alarm is ever remembered. That is the bug this lab removes.
        return current;
    }

    /// <summary>The latch state after a person acknowledges.</summary>
    public static AlarmLatchState Acknowledge(AlarmLatchState current)
    {
        // TODO step 5 (rules 4 to 6).
        return current;
    }

    /// <summary>Given to you. True when a person still needs to acknowledge.</summary>
    public static bool NeedsAcknowledge(AlarmLatchState state) =>
        state is AlarmLatchState.ActiveUnacked or AlarmLatchState.ReturnedUnacked;
}
