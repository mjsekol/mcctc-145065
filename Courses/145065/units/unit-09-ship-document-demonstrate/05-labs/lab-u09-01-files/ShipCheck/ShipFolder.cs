// ShipFolder.cs  .  Lab U09-01  .  ShipCheck
//
// The folder you hand off: the panel project, the change log, and the
// documents. This class only knows where things are and how to read them.
// It decides nothing. The checks decide.

namespace ShipCheck;

public sealed class ShipFolder
{
    /// <summary>Every file a ship folder must have, relative to its root.</summary>
    public static readonly IReadOnlyList<string> RequiredFiles = new[]
    {
        "README.md",
        "CHANGELOG.md",
        "docs/IMPLEMENTATION_PLAN.md",
        "docs/USER_GUIDE.md",
        "docs/HANDOFF_LETTER.md",
        "docs/screen-words.txt",
    };

    public ShipFolder(string root)
    {
        Root = Path.GetFullPath(root);
    }

    public string Root { get; }

    /// <summary>"docs/USER_GUIDE.md" becomes a full path on this machine.</summary>
    public string PathTo(string relative) =>
        Path.Combine(Root, relative.Replace('/', Path.DirectorySeparatorChar));

    public bool Has(string relative) => File.Exists(PathTo(relative));

    public string Read(string relative) => File.ReadAllText(PathTo(relative));

    /// <summary>
    /// The WPF project that ships: the first .csproj under the root, in name
    /// order, that says UseWPF is true. Build output folders are skipped.
    /// Returns null when there is none.
    /// </summary>
    public string? FindPanelProject()
    {
        IEnumerable<string> projects = Directory
            .EnumerateFiles(Root, "*.csproj", SearchOption.AllDirectories)
            .Where(path => !IsBuildOutput(path))
            .OrderBy(path => path, StringComparer.OrdinalIgnoreCase);

        foreach (string project in projects)
        {
            string text = File.ReadAllText(project);
            if (text.Contains("<UseWPF>true</UseWPF>", StringComparison.OrdinalIgnoreCase))
            {
                return project;
            }
        }

        return null;
    }

    private bool IsBuildOutput(string path)
    {
        string relative = Path.GetRelativePath(Root, path);
        string[] parts = relative.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        return parts.Any(part => part.Equals("bin", StringComparison.OrdinalIgnoreCase)
                              || part.Equals("obj", StringComparison.OrdinalIgnoreCase));
    }
}
