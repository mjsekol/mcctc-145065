// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Panel/App.xaml.cs.
// Given to you. Read it; you do not need to change it.
//
// App.xaml.cs  .  145065 HMI anchor  .  Line3.Hmi.Panel
//
// Startup. Read the command line, load the thresholds, open the window.
// If the thresholds file is wrong, say what is wrong and do not open a
// panel. A panel running on limits nobody chose is worse than no panel.

using System.Windows;
using Line3.Hmi.Core;

namespace Line3.Hmi.Panel;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        PanelOptions options;
        PanelConfig config;
        try
        {
            options = PanelOptions.Parse(e.Args, AppContext.BaseDirectory);
            config = options.LoadConfig();
        }
        catch (Exception problem) when (problem is ArgumentException or PanelConfigException)
        {
            MessageBox.Show(problem.Message, "The Line 3 panel cannot start",
                            MessageBoxButton.OK, MessageBoxImage.Error);
            Shutdown(2);
            return;
        }

        MainWindow window = new(config);
        if (options.FullScreen)
        {
            window.WindowStyle = WindowStyle.None;
            window.WindowState = WindowState.Maximized;
        }

        MainWindow = window;
        window.Show();
    }
}
