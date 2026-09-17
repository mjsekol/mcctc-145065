// Equipment.cs
// Lab U06-02, Part B. Port the Python Equipment base class to C#.
//
// This file builds right now. Its members throw NotImplementedException.

using System.Text.RegularExpressions;

namespace Line3.Port;

/// <summary>Anything on Line 3 that carries an asset tag. abstract: nobody builds a plain Equipment.</summary>
public abstract class Equipment
{
    // \z, not $: in .NET, $ also matches before a final newline.
    // [0-9], not \d: \d also matches digits from other writing systems.
    private static readonly Regex TagPattern = new("^L3-[A-Z]{3}-[0-9]{2}\\z");

    // protected: only subclasses call this constructor.
    protected Equipment(string assetTag, string name)
    {
        // TODO B1: refuse a tag that fails IsValidAssetTag, and a blank name.
        //          Store both in get-only properties.
        throw new NotImplementedException();
    }

    /// <summary>static: needs no object. This was @staticmethod in Python.</summary>
    public static bool IsValidAssetTag(string? tag) => tag is not null && TagPattern.IsMatch(tag);

    // TODO B2: replace each throw with a get-only property.
    public string AssetTag => throw new NotImplementedException();
    public string Name => throw new NotImplementedException();

    /// <summary>Every concrete kind must say what it is. Python used a class attribute.</summary>
    public abstract string Kind { get; }

    // TODO B3: "L3-RCK-01 Finished Goods Rack (rack)". virtual, so a subclass may extend it.
    public virtual string Describe() => throw new NotImplementedException();
}
