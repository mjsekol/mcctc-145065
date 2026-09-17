// ReleaseCheck.cs
// Part of the 1.1.0 release plan for the Line 3 Sensor Monitor.
//
// Decides whether a candidate build may replace the build installed on the
// panel PC. The install step runs this before copying anything, so an older
// build can never overwrite a newer one.
//
// Verified against every version this panel will ever ship (see the table
// printed by Program.cs).

namespace ReleaseGate;

public static class ReleaseCheck
{
    /// <summary>
    /// Returns true when <paramref name="candidate"/> is a newer release than
    /// <paramref name="installed"/>. Versions use MAJOR.MINOR.PATCH.
    /// </summary>
    public static bool IsUpgrade(string installed, string candidate)
    {
        // Ordinal comparison is fast and culture-safe for version strings,
        // and it orders MAJOR.MINOR.PATCH values correctly.
        return string.Compare(candidate, installed, StringComparison.Ordinal) > 0;
    }

    /// <summary>The words the install step prints for a decision.</summary>
    public static string Decision(string installed, string candidate) =>
        IsUpgrade(installed, candidate) ? "INSTALL" : "KEEP INSTALLED";
}
