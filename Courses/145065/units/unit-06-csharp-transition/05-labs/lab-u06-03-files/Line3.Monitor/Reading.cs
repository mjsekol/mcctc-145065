// Reading.cs
// Lab U06-03, Part 1 (Monday). This class works, and it leaks.
// Anyone holding a Reading can change any of its fields to anything.
// Your job is to lock it down so the compiler refuses that.

namespace Line3.Monitor;

/// <summary>One reading from one sensor. A null Value means the reading is missing.</summary>
public class Reading
{
    public string SensorId;
    public double? Value;
    public int Sequence;

    public Reading(string sensorId, double? value, int sequence)
    {
        SensorId = sensorId;
        Value = value;
        Sequence = sequence;
    }

    public bool IsMissing => Value == null;
}
