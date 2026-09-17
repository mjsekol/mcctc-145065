// CheckResult.cs  .  Lab U09-01  .  ShipCheck
//
// What one check found. NotWritten exists so the starter program runs and
// tells you honestly which checks are still empty.

namespace ShipCheck;

public enum CheckOutcome
{
    Pass,
    Fail,
    NotWritten,
}

public sealed record CheckResult(string Name, CheckOutcome Outcome, string Detail)
{
    public static CheckResult Pass(string name, string detail) => new(name, CheckOutcome.Pass, detail);

    public static CheckResult Fail(string name, string detail) => new(name, CheckOutcome.Fail, detail);

    public static CheckResult NotWritten(string name) =>
        new(name, CheckOutcome.NotWritten, "this check has not been written yet");

    /// <summary>One line of the report, for example "PASS  required files  all 6 present".</summary>
    public string ToLine()
    {
        string label = Outcome switch
        {
            CheckOutcome.Pass => "PASS",
            CheckOutcome.Fail => "FAIL",
            _ => "TODO",
        };
        return $"{label,-5} {Name,-22} {Detail}";
    }
}
