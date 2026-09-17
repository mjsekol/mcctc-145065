// AlarmBoard.cs  .  Lab U08-05  .  STARTER. You write three methods.
//
// The alarm half of an operator panel, as data. A window would bind to this.
// It holds one AlarmTile per sensor, remembers each sensor's latch, and runs
// the two-step acknowledge:
//
//   RequestAcknowledge(tile)   the tile's button. It only OPENS the confirmation.
//   ConfirmAcknowledge()       the YES button. Now the latch moves.
//   CancelAcknowledge()        the CANCEL button, or Escape. Nothing changes.
//
// Why two steps: a gloved hand that brushes the screen opens a question. It
// does not acknowledge an alarm.
//
// MONITORING ONLY. Acknowledging changes what this panel shows and records.
// It never sends anything to the Pi or to a machine.
//
// The HMI PANEL project's PanelViewModel has the same three methods with the
// same names. What you write here moves there.

using System.Collections.ObjectModel;

namespace Line3.Hmi.Core.ViewModels;

/// <summary>One sensor's alarm, as the window shows it. Given to you.</summary>
public sealed class AlarmTile : ObservableObject
{
    private SensorState state = SensorState.Missing;
    private AlarmLatchState latch = AlarmLatchState.Clear;

    public AlarmTile(string id, string label, Action<AlarmTile> requestAcknowledge)
    {
        Id = id;
        Label = label;
        AcknowledgeCommand = new RelayCommand(() => requestAcknowledge(this), () => CanAcknowledge);
    }

    public string Id { get; }

    public string Label { get; }

    public RelayCommand AcknowledgeCommand { get; }

    public SensorState State
    {
        get => state;
        private set => SetProperty(ref state, value);
    }

    public AlarmLatchState Latch
    {
        get => latch;
        private set
        {
            if (SetProperty(ref latch, value))
            {
                OnPropertyChanged(nameof(BannerText));
                OnPropertyChanged(nameof(CanAcknowledge));
                AcknowledgeCommand.RaiseCanExecuteChanged();
            }
        }
    }

    /// <summary>The banner follows the latch, not the value, so it survives a disconnect.</summary>
    public string BannerText => Latch switch
    {
        AlarmLatchState.ActiveUnacked => "UNACKNOWLEDGED ALARM",
        AlarmLatchState.ActiveAcked => "ACKNOWLEDGED, NOT CLEARED",
        AlarmLatchState.ReturnedUnacked => "ALARM ENDED, NOT ACKNOWLEDGED",
        _ => string.Empty,
    };

    public bool CanAcknowledge => AlarmLatch.NeedsAcknowledge(Latch);

    internal void Show(SensorState newState, AlarmLatchState newLatch)
    {
        State = newState;
        Latch = newLatch;
    }
}

public sealed class AlarmBoard : ObservableObject
{
    private readonly Dictionary<string, AlarmLatchState> latches = new(StringComparer.Ordinal);
    private AlarmTile? pendingAcknowledge;
    private string confirmText = string.Empty;

    public AlarmBoard(IEnumerable<(string Id, string Label)> sensors)
    {
        Tiles = new ObservableCollection<AlarmTile>();
        foreach ((string id, string label) in sensors)
        {
            latches[id] = AlarmLatchState.Clear;
            Tiles.Add(new AlarmTile(id, label, RequestAcknowledge));
        }

        ConfirmAcknowledgeCommand = new RelayCommand(ConfirmAcknowledge, () => IsConfirmOpen);
        CancelAcknowledgeCommand = new RelayCommand(CancelAcknowledge, () => IsConfirmOpen);
    }

    public ObservableCollection<AlarmTile> Tiles { get; }

    /// <summary>What happened, oldest first. The panel shows the newest few.</summary>
    public ObservableCollection<string> Log { get; } = new();

    public RelayCommand ConfirmAcknowledgeCommand { get; }

    public RelayCommand CancelAcknowledgeCommand { get; }

    /// <summary>The tile whose acknowledge is waiting for YES or CANCEL, or null.</summary>
    public AlarmTile? PendingAcknowledge
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

    public string ConfirmText
    {
        get => confirmText;
        private set => SetProperty(ref confirmText, value);
    }

    public AlarmLatchState LatchOf(string id) => latches[id];

    public AlarmTile TileOf(string id) => Tiles.First(t => t.Id == id);

    /// <summary>Given to you. The panel evaluated a sensor: move its latch with YOUR AlarmLatch.Next.</summary>
    public void Observe(string id, SensorState state)
    {
        AlarmLatchState before = latches[id];
        AlarmLatchState after = AlarmLatch.Next(before, state);
        latches[id] = after;
        AlarmTile tile = TileOf(id);
        tile.Show(state, after);
        if (before != after)
        {
            Log.Add($"{tile.Label}: {before} -> {after}");
        }

        if (PendingAcknowledge is not null)
        {
            ComposeConfirmation(PendingAcknowledge);
        }
    }

    /// <summary>The tile's ACKNOWLEDGE ALARM button.</summary>
    public void RequestAcknowledge(AlarmTile tile)
    {
        // TODO step 7. Only when the tile can be acknowledged: compose the
        // question, then open it by setting PendingAcknowledge. Change no latch.
    }

    /// <summary>The YES, ACKNOWLEDGE button.</summary>
    public void ConfirmAcknowledge()
    {
        // TODO step 8. Close the question first. If nothing was pending, stop.
        // Otherwise move that sensor's latch with YOUR AlarmLatch.Acknowledge,
        // update the tile (tile.Show), and add a line to Log.
    }

    /// <summary>The CANCEL button, or Escape.</summary>
    public void CancelAcknowledge()
    {
        // TODO step 9. Close the question. Nothing else.
    }

    /// <summary>Given to you. The sentence the confirmation shows.</summary>
    private void ComposeConfirmation(AlarmTile tile)
    {
        string now = tile.State switch
        {
            SensorState.Alarm => "Right now the value is out of limits.",
            SensorState.Normal => "Right now the value is back inside limits.",
            SensorState.Stale => "Right now the panel does not have a live value.",
            _ => "Right now the panel cannot see this sensor.",
        };
        string effect = tile.Latch == AlarmLatchState.ReturnedUnacked
            ? "Acknowledging removes the alarm from this panel."
            : "Acknowledging records that you saw it. The alarm stays until a live value is back inside limits.";
        ConfirmText = $"Acknowledge the alarm on {tile.Label}? {now} {effect} It does not change anything on the machine.";
    }
}
