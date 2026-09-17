// Sensor.cs
// Lab U06-02, Part A. Port the Python Sensor class to C#.
// The Python is in python_original/line3_parts.py.
//
// This file builds right now. Every member throws NotImplementedException,
// so every Sensor test fails until you replace the throw lines.

namespace Line3.Port;

/// <summary>A sensor mounted on a piece of equipment. No reading is null, never zero.</summary>
public class Sensor
{
    // TODO A1: private fields. Python kept the reading in self._value.
    //          Pick a C# type that can say "no reading" without using zero.

    public Sensor(string id, string kind, string unit, double low, double high)
    {
        // TODO A2: validate every argument the way the Python __init__ does,
        //          then store each one. Throw ArgumentException for bad values.
        throw new NotImplementedException();
    }

    // TODO A3: replace each throw with a get-only property.
    public string Id => throw new NotImplementedException();
    public string Kind => throw new NotImplementedException();
    public string Unit => throw new NotImplementedException();
    public double Low => throw new NotImplementedException();
    public double High => throw new NotImplementedException();

    // TODO A4: the current reading, or null when there is none.
    public double? Value => throw new NotImplementedException();

    // TODO A5: refuse NaN and infinity with ArgumentOutOfRangeException.
    public void Record(double value) => throw new NotImplementedException();

    public void Clear() => throw new NotImplementedException();

    // TODO A6: "no reading", "low", "high", or "ok", in the same order Python checks them.
    public string Status() => throw new NotImplementedException();
}
