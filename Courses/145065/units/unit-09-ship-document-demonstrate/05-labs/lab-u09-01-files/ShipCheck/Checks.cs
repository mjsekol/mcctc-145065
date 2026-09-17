// Checks.cs  .  Lab U09-01  .  ShipCheck  .  STARTER
//
// Seven checks on a ship folder. Each one answers a single question and
// says why when the answer is no. None of them changes a file.
//
//   Monday (Part 1): the release has ONE version, and every document agrees.
//     1 required files     (written for you, as the pattern to copy)
//     2 project version    3 changelog version    4 plan version
//   Tuesday (Part 2): the user guide is written for the operator's screen.
//     5 screen words in guide   6 no jargon in guide   7 pictures exist
//
// Every TODO check returns CheckResult.NotWritten until you write it.
// The tests in ShipCheck.Tests say exactly what each check must do.

using System.Text.RegularExpressions;

namespace ShipCheck;

public static class Checks
{
    public const string RequiredFilesName = "required files";
    public const string ProjectVersionName = "project version";
    public const string ChangelogVersionName = "changelog version";
    public const string PlanVersionName = "plan version";
    public const string ScreenWordsName = "screen words in guide";
    public const string JargonName = "no jargon in guide";
    public const string PicturesName = "pictures exist";

    /// <summary>
    /// Words an operator should never have to read. Match them as whole
    /// words, ignoring case.
    /// </summary>
    public static readonly IReadOnlyList<string> Jargon = new[]
    {
        "JSON", "HTTP", "API", "exception", "null", "thread",
        "ViewModel", "PollingLoop", "localhost", "127.0.0.1", "csproj", "dotnet",
    };

    // Patterns you will want. They are here so you spend the time on the
    // logic, not on regular expression syntax.
    //
    // A version number standing on its own: not part of 1.0.10 or 11.0.1.
    private static readonly Regex AnyVersion = new(@"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])");

    // The text between <Version> and </Version>, trimmed.
    private static readonly Regex ProjectVersionElement = new(@"<Version>\s*([^<]*?)\s*</Version>");

    // A Markdown link or image whose target ends in .png: [text](screens/x.png)
    private static readonly Regex PictureLink = new(@"\]\(([^)\s]+?\.png)\)", RegexOptions.IgnoreCase);

    public static IReadOnlyList<CheckResult> RunAll(ShipFolder ship) => new[]
    {
        RequiredFiles(ship),
        ProjectVersion(ship),
        ChangelogVersion(ship),
        PlanVersion(ship),
        ScreenWordsInGuide(ship),
        NoJargonInGuide(ship),
        PicturesExist(ship),
    };

    // ---- Part 1 · one version everywhere ---------------------------------

    // Written for you. Copy its shape: find the problems, then pass or fail
    // with a detail that names exactly what is wrong.
    public static CheckResult RequiredFiles(ShipFolder ship)
    {
        List<string> missing = ShipFolder.RequiredFiles.Where(file => !ship.Has(file)).ToList();
        return missing.Count == 0
            ? CheckResult.Pass(RequiredFilesName, $"all {ShipFolder.RequiredFiles.Count} present")
            : CheckResult.Fail(RequiredFilesName, "missing: " + string.Join(", ", missing));
    }

    public static CheckResult ProjectVersion(ShipFolder ship)
    {
        // TODO step 3. Use ship.FindPanelProject(). Read the file and match
        // ProjectVersionElement. Then ReleaseVersion.TryParse the text.
        // Pass detail:  "<file name> says 1.0.1"
        // Fail details: "no .csproj with <UseWPF>true</UseWPF> under this folder"
        //               "<file name> has no <Version> element"
        //               "<file name> says \"1.0\", which is not MAJOR.MINOR.PATCH"
        return CheckResult.NotWritten(ProjectVersionName);
    }

    public static CheckResult ChangelogVersion(ShipFolder ship)
    {
        // TODO step 5. The newest entry is the FIRST line that starts with
        // "## " and contains a version (AnyVersion). Compare it with the
        // project version as ReleaseVersion values, not as strings.
        // Pass detail:  "newest entry is 1.0.1"
        // Fail details: "newest entry is 1.0.0, the project says 1.0.1"
        //               "CHANGELOG.md has no \"## \" heading with a version number"
        //               "the project version could not be read; fix that check first"
        return CheckResult.NotWritten(ChangelogVersionName);
    }

    public static CheckResult PlanVersion(ShipFolder ship)
    {
        // TODO step 6. docs/IMPLEMENTATION_PLAN.md must name the project
        // version as a whole token. "1.0.10" must NOT count as "1.0.1".
        // Hint: build a Regex from Regex.Escape(version.ToString()) with the
        // same lookarounds AnyVersion uses.
        // Pass detail:  "the plan names 1.0.1"
        // Fail details: "the plan never names 1.0.1"
        //               "the project version could not be read; fix that check first"
        return CheckResult.NotWritten(PlanVersionName);
    }

    // ---- Part 2 · a guide written for the operator's screen ------------------

    public static CheckResult ScreenWordsInGuide(ShipFolder ship)
    {
        // TODO step 10. Every line of docs/screen-words.txt that is not blank
        // and does not start with # must appear in docs/USER_GUIDE.md,
        // with the same capitals (StringComparison.Ordinal).
        // Pass detail:  "all 14 screen words appear"
        // Fail details: "missing from the guide: STALE, NO DATA"
        //               "screen-words.txt lists no words"
        return CheckResult.NotWritten(ScreenWordsName);
    }

    public static CheckResult NoJargonInGuide(ShipFolder ship)
    {
        // TODO step 11. Report every term in Jargon found in the guide as a
        // whole word, ignoring case. "threads" is not "thread".
        // Pass detail:  "none of the listed terms appear"
        // Fail detail:  "an operator would have to read: JSON, null"
        return CheckResult.NotWritten(JargonName);
    }

    public static CheckResult PicturesExist(ShipFolder ship)
    {
        // TODO step 12. Every PictureLink target must exist. Targets are
        // relative to the guide's folder, so check "docs/" + target.
        // Pass detail:  "all 6 pictures found"
        // Fail details: "not found: screens/alarm.png"
        //               "the guide links no .png pictures of the screen"
        return CheckResult.NotWritten(PicturesName);
    }
}
