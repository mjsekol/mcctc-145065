// StateRules.Truth.cs  .  Lab U08-04  .  given to you
//
// Lab U08-03's Decide, written out, so this lab does not depend on whether
// your own copy is finished. If your Lab U08-03 passed its self-check, yours
// does the same thing. Use yours in the HMI PANEL project.

namespace Line3.Hmi.Core;

public static partial class StateRules
{
    /// <summary>The truth table. Four Booleans in, one state out.</summary>
    public static SensorState Decide(bool haveAnswer, bool sensorOk, bool fresh, bool withinLimits)
    {
        if (!haveAnswer || !sensorOk)
        {
            return SensorState.Missing;
        }

        if (!fresh)
        {
            return SensorState.Stale;
        }

        return withinLimits ? SensorState.Normal : SensorState.Alarm;
    }
}
