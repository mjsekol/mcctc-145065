// COPIED from the course's HMI anchor, panel/Line3.Hmi.Core/ViewModels/PanelViewModel.cs.
// HMI PANEL project. Given to you, with ONE change: the bodies of
// RequestAcknowledge, ConfirmAcknowledge, and CancelAcknowledge are removed.
// Write them the way you wrote the same three methods in Lab U08-05.
//
// PanelViewModel.cs  .  145065 HMI anchor  .  Line3.Hmi.Core.ViewModels
//
// The whole operator panel, as data. The window binds to this and does
// nothing else. The window's code-behind starts the polling loop and a
// refresh timer, and forwards both here.
//
//   ReceiveResult(result)   a poll finished (good or bad)
//   Refresh()               time passed; ages grow, fresh data can go stale
//
// Acknowledging is two steps on purpose. The tile's button only OPENS the
// confirmation. Nothing changes until the operator presses the confirm
// button. A gloved hand that brushes the screen opens a dialog; it does not
// acknowledge an alarm.
//
// MONITORING ONLY. Nothing here sends anything to the Pi or to a machine.
// Acknowledge changes what this panel displays and nothing else.

using System.Collections.ObjectModel;
using System.Globalization;

namespace Line3.Hmi.Core.ViewModels;

public sealed class PanelViewModel : ObservableObject
{
    public const int EventLogLength = 4;

    private readonly PanelMonitor monitor;
    private readonly IClock clock;
    private readonly TimeZoneInfo displayZone;
    private ConnectionState connectionState = ConnectionState.Waiting;
    private string connectionTitle = "WAITING";
    private string connectionDetail = "Waiting for the first reading";
    private string unknownsText = string.Empty;
    private SensorTileViewModel? pendingAcknowledge;
    private string confirmTitle = string.Empty;
    private string confirmText = string.Empty;

    public PanelViewModel(PanelConfig config, IClock clock, TimeZoneInfo? displayZone = null)
    {
        monitor = new PanelMonitor(config);
        this.clock = clock;
        this.displayZone = displayZone ?? TimeZoneInfo.Local;
        Tiles = new ObservableCollection<SensorTileViewModel>(
            config.Sensors.Select(t => new SensorTileViewModel(t, RequestAcknowledge)));
        ConfirmAcknowledgeCommand = new RelayCommand(ConfirmAcknowledge, () => IsConfirmOpen);
        CancelAcknowledgeCommand = new RelayCommand(CancelAcknowledge, () => IsConfirmOpen);
        Refresh();
    }

    public string Title => "LINE 3 SENSOR MONITOR";

    public string MonitoringNotice => "Monitoring only. This panel does not control any equipment.";

    public string ServiceText => monitor.Config.ServiceUrl.GetLeftPart(UriPartial.Authority);

    public ObservableCollection<SensorTileViewModel> Tiles { get; }

    /// <summary>Newest first, at most <see cref="EventLogLength"/>.</summary>
    public ObservableCollection<string> Events { get; } = new();

    public RelayCommand ConfirmAcknowledgeCommand { get; }

    public RelayCommand CancelAcknowledgeCommand { get; }

    public ConnectionState ConnectionState
    {
        get => connectionState;
        private set => SetProperty(ref connectionState, value);
    }

    /// <summary>CONNECTED, DATA NOT UPDATING, NO CONNECTION, or WAITING.</summary>
    public string ConnectionTitle
    {
        get => connectionTitle;
        private set => SetProperty(ref connectionTitle, value);
    }

    public string ConnectionDetail
    {
        get => connectionDetail;
        private set => SetProperty(ref connectionDetail, value);
    }

    /// <summary>Every sensor the panel cannot currently vouch for, in one sentence.</summary>
    public string UnknownsText
    {
        get => unknownsText;
        private set
        {
            if (SetProperty(ref unknownsText, value))
            {
                OnPropertyChanged(nameof(HasUnknowns));
                OnPropertyChanged(nameof(StatusLine));
            }
        }
    }

    public bool HasUnknowns => UnknownsText.Length > 0;

    /// <summary>The line under the header: what the panel cannot vouch for, or that it can vouch for everything.</summary>
    public string StatusLine => HasUnknowns ? UnknownsText : "Every sensor is reporting live data.";

    public SensorTileViewModel? PendingAcknowledge
    {
        get => pendingAcknowledge;
        private set
        {
            if (SetProperty(ref pendingAcknowledge, value))
            {
                OnPropertyChanged(nameof(IsConfirmOpen));
                ConfirmAcknowledgeCommand.RaiseCanExecuteChanged();
                CancelAcknowledgeCommand.RaiseCanExecuteChanged();
            }
        }
    }

    public bool IsConfirmOpen => PendingAcknowledge is not null;

    public string ConfirmTitle
    {
        get => confirmTitle;
        private set => SetProperty(ref confirmTitle, value);
    }

    public string ConfirmText
    {
        get => confirmText;
        private set => SetProperty(ref confirmText, value);
    }

    public PanelMonitor Monitor => monitor;

    public void ReceiveResult(PollResult result)
    {
        monitor.Record(result);
        Refresh();
    }

    public void Refresh()
    {
        PanelUpdate update = monitor.Update(clock.UtcNow);

        foreach (SensorStatus status in update.Sensors)
        {
            Tiles.First(t => t.Id == status.SensorId).Apply(status);
        }

        ConnectionState = update.Connection.State;
        ConnectionTitle = update.Connection.State switch
        {
            ConnectionState.Connected => "CONNECTED",
            ConnectionState.NotUpdating => "DATA NOT UPDATING",
            ConnectionState.Lost => "NO CONNECTION",
            _ => "WAITING",
        };
        ConnectionDetail = update.Connection.Detail;

        List<string> unknown = Tiles
            .Where(t => t.State is SensorState.Stale or SensorState.Missing)
            .Select(t => t.Label)
            .ToList();
        UnknownsText = unknown.Count == 0
            ? string.Empty
            : $"The panel cannot vouch for: {string.Join(", ", unknown)}. Check {(unknown.Count == 1 ? "it" : "them")} at the machine.";

        foreach (PanelEvent happened in update.Events)
        {
            Log(happened);
        }

        if (PendingAcknowledge is not null)
        {
            ComposeConfirmation(PendingAcknowledge);
        }
    }

    public void RequestAcknowledge(SensorTileViewModel tile)
    {
        // TODO (Lab U08-05, step 7). Only when the tile can be acknowledged:
        // ComposeConfirmation(tile), then open the question by setting
        // PendingAcknowledge. Change no latch.
    }

    public void ConfirmAcknowledge()
    {
        // TODO (Lab U08-05, step 8). Close the question first. If nothing was
        // pending, stop. Otherwise ask monitor.Acknowledge(tile.Id, clock.UtcNow,
        // out PanelEvent? acknowledged). When it returns true, Log the event.
        // Then Refresh() so every tile shows the new latch.
    }

    public void CancelAcknowledge()
    {
        // TODO (Lab U08-05, step 9). Close the question. Nothing else.
    }

    private void ComposeConfirmation(SensorTileViewModel tile)
    {
        ConfirmTitle = $"Acknowledge the alarm on {tile.Label}?";
        string now = tile.State switch
        {
            SensorState.Normal or SensorState.Alarm => $"Right now: {tile.StateText}, {tile.ValueText} {tile.Unit}.",
            SensorState.Stale => "Right now: STALE. The panel does not have a live value.",
            _ => "Right now: NO DATA. The panel cannot see this sensor.",
        };
        string effect = tile.Latch == AlarmLatchState.ReturnedUnacked
            ? "The value came back inside limits. Acknowledging removes the alarm from this panel."
            : "Acknowledging records that you have seen this alarm. The alarm stays on screen until a live value is back inside limits.";
        ConfirmText = $"{now} {effect} It does not change anything on the machine.";
    }

    private void Log(PanelEvent happened)
    {
        string time = TimeZoneInfo.ConvertTime(happened.At, displayZone)
            .ToString("HH:mm:ss", CultureInfo.InvariantCulture);
        Events.Insert(0, $"{time}  {happened.Text}");
        while (Events.Count > EventLogLength)
        {
            Events.RemoveAt(Events.Count - 1);
        }
    }
}
