// ChecksTests.cs  .  Lab U09-01  .  ShipCheck.Tests
//
// Your acceptance criteria, as code. Run them with:
//
//   dotnet test ShipCheck.Tests
//
// Part 1 tests go green on Monday. Part 2 tests go green on Tuesday.
// TheProgram tests go green when all seven checks are written.
// Every test starts from a correct ship folder and breaks one thing.

namespace ShipCheck.Tests;

public class Part1OneVersionEverywhere
{
    [Fact]
    public void RequiredFilesNamesEveryMissingFile()
    {
        using TempShip ship = new();
        ship.Delete("CHANGELOG.md");
        ship.Delete("docs/HANDOFF_LETTER.md");
        CheckResult result = Checks.RequiredFiles(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("CHANGELOG.md", result.Detail);
        Assert.Contains("docs/HANDOFF_LETTER.md", result.Detail);
    }

    [Fact]
    public void ProjectVersionReadsTheWpfProject()
    {
        using TempShip ship = new();
        CheckResult result = Checks.ProjectVersion(ship.Folder);
        Assert.Equal(CheckOutcome.Pass, result.Outcome);
        Assert.Contains("1.0.1", result.Detail);
    }

    [Fact]
    public void ProjectVersionIgnoresALibraryThatIsNotTheWindow()
    {
        using TempShip ship = new();
        ship.Write("src/Aaa.Core/Aaa.Core.csproj",
            "<Project><PropertyGroup><TargetFramework>net8.0</TargetFramework><Version>9.9.9</Version></PropertyGroup></Project>");
        Assert.Contains("1.0.1", Checks.ProjectVersion(ship.Folder).Detail);
    }

    [Fact]
    public void ProjectVersionFailsWithNoVersionElement()
    {
        using TempShip ship = new();
        ship.Write("src/Line3.Hmi.Panel/Line3.Hmi.Panel.csproj", TempShip.GoodProject.Replace("    <Version>1.0.1</Version>\n", ""));
        CheckResult result = Checks.ProjectVersion(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("no <Version>", result.Detail);
    }

    [Theory]
    [InlineData("1.0")]
    [InlineData("v1.0.1")]
    [InlineData("1.0.1-beta")]
    public void ProjectVersionRefusesAnythingButThreeNumbers(string bad)
    {
        using TempShip ship = new();
        ship.Write("src/Line3.Hmi.Panel/Line3.Hmi.Panel.csproj", TempShip.GoodProject.Replace("1.0.1", bad));
        CheckResult result = Checks.ProjectVersion(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("MAJOR.MINOR.PATCH", result.Detail);
    }

    [Fact]
    public void ChangelogVersionUsesTheNewestEntryOnly()
    {
        using TempShip ship = new();
        ship.Write("CHANGELOG.md", "# Change log\n\n## 1.0.0 · Week 17 Wed\n- Baseline.\n\n## 1.0.1 · Week 18 Tue\n- Added later, but written below.\n");
        CheckResult result = Checks.ChangelogVersion(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("newest entry is 1.0.0", result.Detail);
        Assert.Contains("the project says 1.0.1", result.Detail);
    }

    [Fact]
    public void ChangelogVersionSkipsHeadingsWithNoVersion()
    {
        using TempShip ship = new();
        ship.Write("CHANGELOG.md", "# Change log\n\n## Unreleased\n- nothing yet\n\n## 1.0.1 · Week 18 Tue\n- fix\n");
        Assert.Equal(CheckOutcome.Pass, Checks.ChangelogVersion(ship.Folder).Outcome);
    }

    [Fact]
    public void ChangelogVersionFailsWhenNoHeadingHasAVersion()
    {
        using TempShip ship = new();
        ship.Write("CHANGELOG.md", "# Change log\n\nVersion 1.0.1 fixed some things.\n");
        CheckResult result = Checks.ChangelogVersion(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("no \"## \" heading", result.Detail);
    }

    [Fact]
    public void PlanVersionFindsTheExactVersion()
    {
        using TempShip ship = new();
        Assert.Equal(CheckOutcome.Pass, Checks.PlanVersion(ship.Folder).Outcome);
    }

    [Fact]
    public void PlanVersionIsNotFooledByALongerNumber()
    {
        using TempShip ship = new();
        ship.Write("docs/IMPLEMENTATION_PLAN.md", "# Implementation plan\n\nThis plan installs version 1.0.10.\n");
        CheckResult result = Checks.PlanVersion(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("never names 1.0.1", result.Detail);
    }

    [Fact]
    public void VersionChecksSayWhenTheProjectVersionIsTheRealProblem()
    {
        using TempShip ship = new();
        ship.Delete("src/Line3.Hmi.Panel/Line3.Hmi.Panel.csproj");
        Assert.Contains("fix that check first", Checks.ChangelogVersion(ship.Folder).Detail);
        Assert.Contains("fix that check first", Checks.PlanVersion(ship.Folder).Detail);
    }

    [Fact]
    public void ReleaseVersionsCompareAsNumbersNotText()
    {
        Assert.True(ReleaseVersion.TryParse("1.10.0", out ReleaseVersion ten));
        Assert.True(ReleaseVersion.TryParse("1.9.0", out ReleaseVersion nine));
        Assert.True(ten.CompareTo(nine) > 0);
        Assert.True(string.CompareOrdinal("1.10.0", "1.9.0") < 0);
    }
}

public class Part2AGuideForTheScreen
{
    [Fact]
    public void ScreenWordsNamesEveryWordTheGuideLeftOut()
    {
        using TempShip ship = new();
        ship.Write("docs/USER_GUIDE.md", "A NORMAL tile is fine.\n\n[pic](screens/normal.png)\n");
        CheckResult result = Checks.ScreenWordsInGuide(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("STALE", result.Detail);
        Assert.Contains("NO DATA", result.Detail);
        Assert.DoesNotContain("NORMAL", result.Detail);
    }

    [Fact]
    public void ScreenWordsMustMatchTheCapitalsOnTheScreen()
    {
        using TempShip ship = new();
        ship.Write("docs/USER_GUIDE.md", TempShip.GoodGuide.Replace("A STALE tile", "A stale tile"));
        Assert.Equal(CheckOutcome.Fail, Checks.ScreenWordsInGuide(ship.Folder).Outcome);
    }

    [Fact]
    public void ScreenWordsIgnoresCommentsAndBlankLines()
    {
        using TempShip ship = new();
        ship.Write("docs/screen-words.txt", "# comment\n\nNORMAL\n   \n# STALE is not listed here\n");
        CheckResult result = Checks.ScreenWordsInGuide(ship.Folder);
        Assert.Equal(CheckOutcome.Pass, result.Outcome);
        Assert.Contains("all 1 screen words", result.Detail);
    }

    [Fact]
    public void ScreenWordsFailsOnAnEmptyList()
    {
        using TempShip ship = new();
        ship.Write("docs/screen-words.txt", "# nothing yet\n");
        Assert.Equal(CheckOutcome.Fail, Checks.ScreenWordsInGuide(ship.Folder).Outcome);
    }

    [Fact]
    public void JargonNamesEveryTermFound()
    {
        using TempShip ship = new();
        ship.Write("docs/USER_GUIDE.md", TempShip.GoodGuide + "\nIf the JSON is null, restart the PollingLoop.\n");
        CheckResult result = Checks.NoJargonInGuide(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("JSON", result.Detail);
        Assert.Contains("null", result.Detail);
        Assert.Contains("PollingLoop", result.Detail);
    }

    [Fact]
    public void JargonMatchesWholeWordsOnly()
    {
        using TempShip ship = new();
        ship.Write("docs/USER_GUIDE.md", TempShip.GoodGuide + "\nRapid changes in the threads of a bolt are not a sensor problem.\n");
        Assert.Equal(CheckOutcome.Pass, Checks.NoJargonInGuide(ship.Folder).Outcome);
    }

    [Fact]
    public void JargonIgnoresCase()
    {
        using TempShip ship = new();
        ship.Write("docs/USER_GUIDE.md", TempShip.GoodGuide + "\nAsk IT to check the http address.\n");
        Assert.Contains("HTTP", Checks.NoJargonInGuide(ship.Folder).Detail);
    }

    [Fact]
    public void PicturesNamesEveryBrokenLink()
    {
        using TempShip ship = new();
        ship.Write("docs/USER_GUIDE.md", TempShip.GoodGuide + "\n[alarm](screens/alarm.png)\n![stale](screens/stale.PNG)\n");
        CheckResult result = Checks.PicturesExist(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("screens/alarm.png", result.Detail);
        Assert.Contains("screens/stale.PNG", result.Detail);
        Assert.DoesNotContain("normal.png", result.Detail);
    }

    [Fact]
    public void PicturesFailsWhenTheGuideHasNone()
    {
        using TempShip ship = new();
        ship.Write("docs/USER_GUIDE.md", "NORMAL STALE NO DATA\n");
        CheckResult result = Checks.PicturesExist(ship.Folder);
        Assert.Equal(CheckOutcome.Fail, result.Outcome);
        Assert.Contains("no .png", result.Detail);
    }
}

public class TheProgram
{
    [Fact]
    public void AGoodShipFolderPassesEveryCheck()
    {
        using TempShip ship = new();
        Assert.All(Checks.RunAll(ship.Folder), r => Assert.Equal(CheckOutcome.Pass, r.Outcome));
    }

    [Fact]
    public void ExitsZeroWhenEverythingPasses()
    {
        using TempShip ship = new();
        Assert.Equal(0, Program.Main(new[] { ship.Root }));
    }

    [Fact]
    public void ExitsOneWhenAnyCheckFails()
    {
        using TempShip ship = new();
        ship.Delete("docs/HANDOFF_LETTER.md");
        Assert.Equal(1, Program.Main(new[] { ship.Root }));
    }

    [Fact]
    public void ExitsTwoOnBadUsage()
    {
        Assert.Equal(2, Program.Main(Array.Empty<string>()));
        Assert.Equal(2, Program.Main(new[] { Path.Combine(Path.GetTempPath(), "no-such-ship-" + Guid.NewGuid().ToString("N")) }));
    }
}
