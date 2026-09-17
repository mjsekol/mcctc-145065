// Program.cs  .  Lab U09-01  .  ShipCheck
//
//   dotnet run --project ShipCheck -- <ship folder>
//
// Exit codes: 0 every check passed, 1 at least one did not, 2 bad usage.
// A script, or your instructor, can read the exit code without reading
// the report.

namespace ShipCheck;

public static class Program
{
    public const string Usage = "Usage: ShipCheck <ship folder>";

    public static int Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.Error.WriteLine(Usage);
            return 2;
        }

        if (!Directory.Exists(args[0]))
        {
            Console.Error.WriteLine($"No folder at {args[0]}. {Usage}");
            return 2;
        }

        ShipFolder ship = new(args[0]);
        Console.WriteLine($"ShipCheck on {ship.Root}");

        IReadOnlyList<CheckResult> results = Checks.RunAll(ship);
        foreach (CheckResult result in results)
        {
            Console.WriteLine(result.ToLine());
        }

        int passed = results.Count(r => r.Outcome == CheckOutcome.Pass);
        Console.WriteLine($"{passed} of {results.Count} checks passed.");
        return passed == results.Count ? 0 : 1;
    }
}
