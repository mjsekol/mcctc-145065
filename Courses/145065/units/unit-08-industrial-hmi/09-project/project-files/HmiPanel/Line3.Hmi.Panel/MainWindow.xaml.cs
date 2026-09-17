// COPIED UNCHANGED from the course's HMI anchor, panel/Line3.Hmi.Panel/MainWindow.xaml.cs.
// Given to you. Read it; you do not need to change it.
//
// MainWindow.xaml.cs  .  145065 HMI anchor  .  Line3.Hmi.Panel
//
// The event flow, in one file:
//
//   Loaded         start the refresh timer and the polling loop
//   (loop)         each finished poll -> PanelViewModel.ReceiveResult
//   timer Tick     every 500 ms -> PanelViewModel.Refresh (ages grow,
//                  fresh data turns stale even if a poll is stuck)
//   button Click   bound commands in the view model, no handlers here
//   Closed         cancel the loop, stop the timer, release the client
//
// The loop is started from the UI thread and awaits without
// ConfigureAwait(false), so every ReceiveResult call lands back on the UI
// thread. The HTTP wait itself holds no thread. The window never freezes.

using System.Windows;
using System.Windows.Threading;
using Line3.Hmi.Core;
using Line3.Hmi.Core.ViewModels;

namespace Line3.Hmi.Panel;

public partial class MainWindow : Window
{
    private readonly PanelConfig config;
    private readonly PanelViewModel viewModel;
    private readonly SensorClient client;
    private readonly CancellationTokenSource stopping = new();
    private readonly DispatcherTimer refreshTimer;

    public MainWindow(PanelConfig config)
    {
        InitializeComponent();
        this.config = config;
        viewModel = new PanelViewModel(config, SystemClock.Instance);
        client = new SensorClient(config.ServiceUrl, config.RequestTimeout, SystemClock.Instance);
        DataContext = viewModel;

        refreshTimer = new DispatcherTimer(DispatcherPriority.Normal)
        {
            Interval = TimeSpan.FromMilliseconds(500),
        };
        refreshTimer.Tick += OnRefreshTick;

        Loaded += OnLoaded;
        Closed += OnClosed;
    }

    private void OnLoaded(object sender, RoutedEventArgs e)
    {
        refreshTimer.Start();
        PollingLoop loop = new(client.PollAsync, config.PollInterval, viewModel.ReceiveResult);

        // Not awaited on purpose: the loop runs for the life of the window.
        // It ends without throwing when the window closes.
        _ = loop.RunAsync(stopping.Token);
    }

    private void OnRefreshTick(object? sender, EventArgs e) => viewModel.Refresh();

    private void OnClosed(object? sender, EventArgs e)
    {
        stopping.Cancel();
        refreshTimer.Stop();
        client.Dispose();
    }
}
