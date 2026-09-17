// TempShip.cs  .  Lab U09-01  .  ShipCheck.Tests
//
// Builds a small, correct ship folder in the temp directory for one test,
// and deletes it afterward. Each test breaks exactly one thing in it.
// Nothing here touches your repository.

namespace ShipCheck.Tests;

public sealed class TempShip : IDisposable
{
    public const string GoodProject =
        "<Project Sdk=\"Microsoft.NET.Sdk\">\n  <PropertyGroup>\n    <OutputType>WinExe</OutputType>\n"
        + "    <TargetFramework>net8.0-windows</TargetFramework>\n    <UseWPF>true</UseWPF>\n"
        + "    <Version>1.0.1</Version>\n  </PropertyGroup>\n</Project>\n";

    public const string GoodChangelog =
        "# Change log\n\n## 1.0.1 · Week 18 Tue\n- Clearer wording on NO DATA tiles.\n\n## 1.0.0 · Week 17 Wed\n- Baseline.\n";

    public const string GoodPlan = "# Implementation plan\n\nThis plan installs version 1.0.1 on the Line 3 panel PC.\n";

    public const string GoodWords = "# every word the panel can show\nNORMAL\nSTALE\nNO DATA\n";

    public const string GoodGuide =
        "# Line 3 Sensor Monitor\n\nA NORMAL tile is fine. A STALE tile is old. A NO DATA tile has no reading.\n\n"
        + "Picture: [Every sensor normal](screens/normal.png)\n";

    public TempShip()
    {
        Root = Path.Combine(Path.GetTempPath(), "shipcheck-test-" + Guid.NewGuid().ToString("N"));
        Write("README.md", "# Line 3 panel\n");
        Write("CHANGELOG.md", GoodChangelog);
        Write("docs/IMPLEMENTATION_PLAN.md", GoodPlan);
        Write("docs/USER_GUIDE.md", GoodGuide);
        Write("docs/HANDOFF_LETTER.md", "To the Line 3 shift lead,\n");
        Write("docs/screen-words.txt", GoodWords);
        Write("docs/screens/normal.png", "not really a picture, and the check does not open it");
        Write("src/Line3.Hmi.Panel/Line3.Hmi.Panel.csproj", GoodProject);
    }

    public string Root { get; }

    public ShipFolder Folder => new(Root);

    public void Write(string relative, string text)
    {
        string path = Path.Combine(Root, relative.Replace('/', Path.DirectorySeparatorChar));
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, text);
    }

    public void Delete(string relative) =>
        File.Delete(Path.Combine(Root, relative.Replace('/', Path.DirectorySeparatorChar)));

    public void Dispose()
    {
        if (Directory.Exists(Root))
        {
            Directory.Delete(Root, recursive: true);
        }
    }
}
