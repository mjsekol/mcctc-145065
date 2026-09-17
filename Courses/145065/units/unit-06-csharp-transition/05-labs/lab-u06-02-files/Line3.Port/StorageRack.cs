// StorageRack.cs
// Lab U06-02, Part B. Port the Python StorageRack class to C#.
//
// This file builds right now. Its members throw NotImplementedException.

namespace Line3.Port;

/// <summary>A rack for finished parts. Equipment, with no power.</summary>
public class StorageRack : Equipment
{
    // TODO B4: a private field for the load. Python kept it in self._load_kg.

    // The ": base(assetTag, name)" line runs the Equipment constructor first.
    // Python did the same thing with super().__init__(asset_tag, name).
    public StorageRack(string assetTag, string name, double capacityKg)
        : base(assetTag, name)
    {
        // TODO B5: refuse a capacity that is not above zero, then store it.
        throw new NotImplementedException();
    }

    // TODO B6: "rack".
    public override string Kind => throw new NotImplementedException();

    public double CapacityKg => throw new NotImplementedException();

    // TODO B7: a property with a get and a set. The set refuses a negative
    //          load, and records an overload instead of refusing it.
    public double LoadKg
    {
        get => throw new NotImplementedException();
        set => throw new NotImplementedException();
    }

    // TODO B8: the base description plus ", 96% full". Use Math.Round.
    public override string Describe() => throw new NotImplementedException();
}
