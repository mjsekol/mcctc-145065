// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Core/PanelOptions.cs.
// Given to you. Read it; you do not need to change it.
//
// PanelOptions.cs  .  145065 HMI anchor  .  Line3.Hmi.Core
//
// The panel's command line, parsed where a test can reach it.
//
//   Line3.Hmi.Panel.exe
//   Line3.Hmi.Panel.exe --config thresholds.bench.json
//   Line3.Hmi.Panel.exe --url http://127.0.0.1:8661
//   Line3.Hmi.Panel.exe --fullscreen
//
// --config   thresholds file. Relative paths are relative to the program's
//            folder. Default: thresholds.json next to the program.
// --url      overrides service_url from the thresholds file.
// --fullscreen  borderless and maximized, for a mounted panel.

namespace Line3.Hmi.Core;

public sealed record PanelOptions(string ConfigPath, Uri? ServiceUrl, bool FullScreen)
{
    public const string DefaultConfigFile = "thresholds.json";

    public const string Usage =
        "Usage: Line3.Hmi.Panel [--config <thresholds.json>] [--url http://host:port] [--fullscreen]";

    /// <summary>Throws ArgumentException with a sentence a person can act on.</summary>
    public static PanelOptions Parse(IReadOnlyList<string> args, string programFolder)
    {
        string config = Path.Combine(programFolder, DefaultConfigFile);
        Uri? url = null;
        bool fullScreen = false;

        for (int i = 0; i < args.Count; i++)
        {
            switch (args[i])
            {
                case "--config":
                    config = Path.GetFullPath(Path.Combine(programFolder, Next(args, ref i, "--config")));
                    break;
                case "--url":
                    string text = Next(args, ref i, "--url");
                    if (!Uri.TryCreate(text, UriKind.Absolute, out url)
                        || (url.Scheme != Uri.UriSchemeHttp && url.Scheme != Uri.UriSchemeHttps))
                    {
                        throw new ArgumentException($"--url \"{text}\" is not an http address. {Usage}");
                    }

                    break;
                case "--fullscreen":
                    fullScreen = true;
                    break;
                default:
                    throw new ArgumentException($"Unknown option \"{args[i]}\". {Usage}");
            }
        }

        return new PanelOptions(config, url, fullScreen);
    }

    private static string Next(IReadOnlyList<string> args, ref int i, string name)
    {
        if (i + 1 >= args.Count || args[i + 1].StartsWith("--", StringComparison.Ordinal))
        {
            throw new ArgumentException($"{name} needs a value. {Usage}");
        }

        i++;
        return args[i];
    }

    /// <summary>Load the thresholds file this command line names, with any URL override applied.</summary>
    public PanelConfig LoadConfig()
    {
        PanelConfig config = PanelConfig.Load(ConfigPath);
        return ServiceUrl is null ? config : config.WithServiceUrl(ServiceUrl);
    }
}
