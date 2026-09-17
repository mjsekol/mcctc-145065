// Program.cs
// Part of the 1.1.0 release plan for the Line 3 Sensor Monitor.
//
//   dotnet run --project ReleaseGate                        prints the verification table
//   dotnet run --project ReleaseGate -- <installed> <candidate>   prints one decision

namespace ReleaseGate;

public static class Program
{
    // Every upgrade path the Line 3 panel has had, plus the rollback case.
    private static readonly (string Installed, string Candidate)[] Verified =
    {
        ("1.0.0", "1.0.1"),
        ("1.0.1", "1.1.0"),
        ("1.0.0", "1.1.0"),
        ("1.1.0", "1.0.1"),
    };

    public static int Main(string[] args)
    {
        if (args.Length == 2)
        {
            Console.WriteLine($"installed {args[0]}, candidate {args[1]}: {ReleaseCheck.Decision(args[0], args[1])}");
            return 0;
        }

        Console.WriteLine("installed  candidate  decision");
        foreach ((string installed, string candidate) in Verified)
        {
            Console.WriteLine($"{installed,-10} {candidate,-10} {ReleaseCheck.Decision(installed, candidate)}");
        }

        return 0;
    }
}
