// StateRules.Freshness.cs  .  HMI PANEL project  .  YOURS: paste your Lab U08-04 CheckFreshness here.
//
// Is a sample fresh? Two independent checks, and a sample is fresh only when
// it passes both. Pure: every time arrives as a parameter, so a test can ask
// about "twelve seconds later" without waiting twelve seconds.
//
//   BY TIMESTAMP   the sample's own sampled_at, against the panel's clock.
//                  Catches a Pi that keeps answering with an old sample.
//
//   BY SEQUENCE    how long ago, by the PANEL's clock, the sequence number
//                  last changed. Catches a Pi that stamps an old reading with
//                  the current time, and still works when the Pi's clock is
//                  wrong.
//
// And one honest limit: a sample stamped further in the FUTURE than the stale
// limit means the two clocks disagree. The panel cannot tell how old that
// value is, so it does not call it live.
//
// Return the FIRST reason that applies, in this order: ClockDisagrees,
// SampleTooOld, SequenceNotAdvancing. Return None only when the sample is
// fresh. A sample exactly at the limit is still fresh.

namespace Line3.Hmi.Core;

public static partial class StateRules
{
    public static StaleReason CheckFreshness(
        DateTimeOffset now,
        DateTimeOffset sampledAt,
        DateTimeOffset sequenceLastAdvancedAt,
        TimeSpan staleAfter)
    {
        // TODO steps 3 to 6.
        //
        // The starter calls every sample fresh. That is the exact bug this lab
        // exists to remove: a panel that shows a frozen number as live.
        return StaleReason.None;
    }
}
