// COPIED from the course's HMI anchor, panel/Line3.Hmi.Core/ViewModels/SensorTileViewModel.cs.
// HMI PANEL project. Given to you, with ONE change: the body of the switch in
// Apply is removed. Paste the switch you wrote in Lab U08-04 here.
//
// SensorTileViewModel.cs  .  145065 HMI anchor  .  Line3.Hmi.Core.ViewModels
//
// One sensor's tile, as text the window binds to. Every rule about what may
// appear on screen is enforced here, where a test can check it:
//
//   - ValueText holds a number ONLY when the value is live (normal or alarm).
//   - A stale value appears only in LastKnownText, labelled not live.
//   - A missing value appears nowhere.
//   - The alarm banner follows the latch, not the current value, so it stays
//     up through stale and missing data.

using System.Globalization;

namespace Line3.Hmi.Core.ViewModels;

public sealed class SensorTileViewModel : ObservableObject
{
    public const string NoValueText = "- - -";
    public const string NotLiveText = "NOT LIVE";

    private SensorState state = SensorState.Missing;
    private string stateText = "NO DATA";
    private string valueText = NoValueText;
    private bool valueIsLive;
    private string lastKnownText = string.Empty;
    private string explanation = "Waiting for the first reading from the sensor service.";
    private AlarmLatchState latch = AlarmLatchState.Clear;
    private string alarmBannerText = string.Empty;
    private string lastUpdateKey = string.Empty;

    public SensorTileViewModel(SensorThreshold threshold, Action<SensorTileViewModel> requestAcknowledge)
    {
        Threshold = threshold;
        AcknowledgeCommand = new RelayCommand(() => requestAcknowledge(this), () => CanAcknowledge);
    }

    public SensorThreshold Threshold { get; }

    public string Id => Threshold.Id;

    public string Label => Threshold.Label;

    public string Unit => Threshold.Unit;

    public string LimitsText => Threshold.LimitsText;

    public string Reason => Threshold.Reason;

    public RelayCommand AcknowledgeCommand { get; }

    public SensorState State
    {
        get => state;
        private set => SetProperty(ref state, value);
    }

    /// <summary>The state in words: NORMAL, ALARM HIGH, ALARM LOW, STALE, NO DATA.</summary>
    public string StateText
    {
        get => stateText;
        private set => SetProperty(ref stateText, value);
    }

    /// <summary>The big number. A live value, NOT LIVE, or the no-value dashes. Never a stale number.</summary>
    public string ValueText
    {
        get => valueText;
        private set => SetProperty(ref valueText, value);
    }

    public bool ValueIsLive
    {
        get => valueIsLive;
        private set => SetProperty(ref valueIsLive, value);
    }

    /// <summary>For stale data only: the last value, its age, and the words "not live".</summary>
    public string LastKnownText
    {
        get => lastKnownText;
        private set
        {
            if (SetProperty(ref lastKnownText, value))
            {
                OnPropertyChanged(nameof(HasLastKnown));
            }
        }
    }

    public bool HasLastKnown => LastKnownText.Length > 0;

    /// <summary>A sentence for the operator: what the panel knows, or what it does not.</summary>
    public string Explanation
    {
        get => explanation;
        private set => SetProperty(ref explanation, value);
    }

    public AlarmLatchState Latch
    {
        get => latch;
        private set
        {
            if (SetProperty(ref latch, value))
            {
                OnPropertyChanged(nameof(CanAcknowledge));
                AcknowledgeCommand.RaiseCanExecuteChanged();
            }
        }
    }

    public string AlarmBannerText
    {
        get => alarmBannerText;
        private set
        {
            if (SetProperty(ref alarmBannerText, value))
            {
                OnPropertyChanged(nameof(HasAlarmBanner));
            }
        }
    }

    public bool HasAlarmBanner => AlarmBannerText.Length > 0;

    public bool CanAcknowledge => AlarmLatch.NeedsAcknowledge(Latch);

    /// <summary>A plain summary for confirmation dialogs and the event log.</summary>
    public string Summary => State switch
    {
        SensorState.Normal or SensorState.Alarm => $"{Label}: {StateText}, {ValueText} {Unit}",
        _ => $"{Label}: {StateText}",
    };

    /// <summary>
    /// What a screen reader announces for the tile. Without this, UI
    /// Automation reads out the class name.
    /// </summary>
    public override string ToString() => Summary;

    public void Apply(SensorStatus status)
    {
        SensorThreshold t = status.Threshold;
        // TODO Lab U08-04, steps 7 to 10. One case per state. Each case sets
        // StateText, ValueText, ValueIsLive, and LastKnownText.
        //
        // The starter sets nothing, so every tile keeps saying NO DATA with
        // dashes. That is never dangerous and never useful.
        switch (status.State)
        {
            default:
                break;
        }

        State = status.State;
        Explanation = status.Explanation;
        Latch = status.Latch;
        AlarmBannerText = status.Latch switch
        {
            AlarmLatchState.ActiveUnacked => "UNACKNOWLEDGED ALARM",
            AlarmLatchState.ActiveAcked => "ACKNOWLEDGED, NOT CLEARED",
            AlarmLatchState.ReturnedUnacked => "ALARM ENDED, NOT ACKNOWLEDGED",
            _ => string.Empty,
        };

        string key = $"{State}|{ValueText}|{Latch}";
        if (key != lastUpdateKey)
        {
            lastUpdateKey = key;
            OnPropertyChanged(nameof(Summary));
        }
    }
}
