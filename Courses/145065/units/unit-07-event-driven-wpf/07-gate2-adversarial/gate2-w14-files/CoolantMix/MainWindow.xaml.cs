// MainWindow.xaml.cs
// CoolantMix: shows the operator what to add to the CNC sump and logs each
// check to the shared mix log.

using System.Globalization;
using System.IO;
using System.Windows;
using CoolantMix.Core;

namespace CoolantMix;

public partial class MainWindow : Window
{
    private readonly MixViewModel mix;

    public MainWindow()
        : this(DefaultLogPath)
    {
    }

    public MainWindow(string logPath)
    {
        InitializeComponent();
        mix = new MixViewModel(logPath);
        DataContext = mix;
    }

    public static string DefaultLogPath => Path.Combine(AppContext.BaseDirectory, "mix-log.csv");

    public MixViewModel Mix => mix;

    // Appends the current check to the shared mix log.
    private void LogButton_Click(object sender, RoutedEventArgs e)
    {
        string line = string.Join(",",
            DateTime.Now.ToString("yyyy-MM-dd HH:mm", CultureInfo.InvariantCulture),
            mix.Badge,
            mix.VolumeText,
            mix.ReadingText,
            mix.Target.ToString("0.0", CultureInfo.InvariantCulture),
            mix.Instruction,
            mix.Note);

        File.AppendAllText(mix.LogPath, line + Environment.NewLine);
        mix.LogWritten();
        StatusText.Text = "Check logged.";
    }
}
