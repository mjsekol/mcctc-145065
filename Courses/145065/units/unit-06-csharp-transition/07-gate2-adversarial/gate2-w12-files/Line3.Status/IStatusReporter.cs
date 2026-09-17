namespace Line3.Status;

/// <summary>
/// Anything the Line 3 status board can show. Implemented by
/// <see cref="TemperatureProbe"/> and <see cref="GuardSwitch"/>.
/// </summary>
public interface IStatusReporter
{
    /// <summary>The tag printed on the board, such as L3-OVN-01.</summary>
    string Tag { get; }

    /// <summary>
    /// The current level. Settable so the panel can acknowledge a condition
    /// once an operator has seen it.
    /// </summary>
    StatusLevel Level { get; set; }

    /// <summary>Returns the reporter to its power-on state.</summary>
    void Reset();
}
