// AlarmLatch.cs  .  Lab U08-04  .  given to you, trimmed
//
// Only the part of the HMI anchor's AlarmLatch.cs that the tile needs: the
// four latch states and "does this need a person?". The rules that move the
// latch are Lab U08-05's work.

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
    public static bool NeedsAcknowledge(AlarmLatchState state) =>
        state is AlarmLatchState.ActiveUnacked or AlarmLatchState.ReturnedUnacked;
}
