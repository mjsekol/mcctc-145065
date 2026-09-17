// StateRules.Truth.cs  .  HMI PANEL project  .  YOURS: paste your Lab U08-03 Decide here.
//
// Four Booleans in, one state out. A pure function: no clock, no network,
// no memory. The same inputs always give the same answer, so a test can
// check every one of the 16 combinations.
//
//   haveAnswer    A   the request worked and the reply parsed
//   sensorOk      K   this sensor reported ok, with a value
//   fresh         F   the sample is not older than the stale limit
//   withinLimits  W   the value is inside its documented limits
//
// Step 3: write your Boolean expression for each state in the comment block
// below BEFORE you write any code. Step 4: write Decide from them.
//
//   MISSING =
//   STALE   =
//   ALARM   =
//   NORMAL  =

namespace Line3.Hmi.Core;

public static partial class StateRules
{
    /// <summary>The truth table. Four Booleans in, one state out.</summary>
    public static SensorState Decide(bool haveAnswer, bool sensorOk, bool fresh, bool withinLimits)
    {
        // TODO step 4. The starter says Missing for everything, which is the
        // one answer that is never dangerous and never useful.
        return SensorState.Missing;
    }
}
