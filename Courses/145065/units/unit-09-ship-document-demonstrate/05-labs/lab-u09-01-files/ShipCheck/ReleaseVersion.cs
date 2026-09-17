// ReleaseVersion.cs  .  Lab U09-01  .  ShipCheck
//
// A release number, MAJOR.MINOR.PATCH, held as three integers.
//
// Why a type and not a string: "1.10.0" and "1.9.0" compare the wrong way
// as text. As three integers they compare the right way, and the compiler
// will not let you compare a ReleaseVersion with a string by accident.

using System.Globalization;
using System.Text.RegularExpressions;

namespace ShipCheck;

public readonly record struct ReleaseVersion(int Major, int Minor, int Patch) : IComparable<ReleaseVersion>
{
    // Three groups of digits and nothing else. "1.0" and "v1.0.0" are refused.
    private static readonly Regex Shape = new(@"^(\d+)\.(\d+)\.(\d+)$");

    /// <summary>Reads "1.4.2". Returns false for anything that is not three whole numbers.</summary>
    public static bool TryParse(string? text, out ReleaseVersion version)
    {
        version = default;
        if (text is null)
        {
            return false;
        }

        Match match = Shape.Match(text.Trim());
        if (!match.Success)
        {
            return false;
        }

        version = new ReleaseVersion(
            int.Parse(match.Groups[1].Value, CultureInfo.InvariantCulture),
            int.Parse(match.Groups[2].Value, CultureInfo.InvariantCulture),
            int.Parse(match.Groups[3].Value, CultureInfo.InvariantCulture));
        return true;
    }

    /// <summary>Major first, then minor, then patch. Numbers, never text.</summary>
    public int CompareTo(ReleaseVersion other)
    {
        if (Major != other.Major)
        {
            return Major.CompareTo(other.Major);
        }

        if (Minor != other.Minor)
        {
            return Minor.CompareTo(other.Minor);
        }

        return Patch.CompareTo(other.Patch);
    }

    public override string ToString() =>
        string.Create(CultureInfo.InvariantCulture, $"{Major}.{Minor}.{Patch}");
}
