// MixViewModel.cs
// View model for the CoolantMix panel. Holds the operator's inputs, works out
// what to add to the sump, and exposes the recent log for the window.

using System.ComponentModel;
using System.Globalization;
using System.Runtime.CompilerServices;

namespace CoolantMix.Core;

public sealed class MixViewModel : INotifyPropertyChanged
{
    /// <summary>A reading this close to the target needs nothing added.</summary>
    public const double OnTargetBand = 0.2;

    private readonly string logPath;
    private string volumeText = string.Empty;
    private string readingText = string.Empty;
    private double target = 6.0;
    private string badge = string.Empty;
    private string note = string.Empty;

    public MixViewModel(string logPath)
    {
        this.logPath = logPath;
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public string LogPath => logPath;

    /// <summary>Sump volume in litres, as typed.</summary>
    public string VolumeText
    {
        get => volumeText;
        set
        {
            if (Set(ref volumeText, value ?? string.Empty))
            {
                Recalculate();
            }
        }
    }

    /// <summary>Refractometer reading in percent, as typed.</summary>
    public string ReadingText
    {
        get => readingText;
        set
        {
            if (Set(ref readingText, value ?? string.Empty))
            {
                Recalculate();
            }
        }
    }

    /// <summary>Target concentration in percent. The slider binds here.</summary>
    public double Target
    {
        get => target;
        set => Set(ref target, value);
    }

    /// <summary>The operator's four-digit badge number.</summary>
    public string Badge
    {
        get => badge;
        set
        {
            if (Set(ref badge, value ?? string.Empty))
            {
                Recalculate();
            }
        }
    }

    /// <summary>Free-text note that goes in the log with the check.</summary>
    public string Note
    {
        get => note;
        set => Set(ref note, value ?? string.Empty);
    }

    /// <summary>What the operator should add, in words.</summary>
    public string Instruction
    {
        get
        {
            if (!TryVolume(out double volume) || !TryReading(out double reading))
            {
                return "Enter the sump volume and the reading.";
            }

            // Rounded first: 6.2 - 6.0 is 0.20000000000000018 in floating point.
            if (Math.Round(Math.Abs(reading - Target), 3) <= OnTargetBand)
            {
                return "Mix is on target. Add nothing.";
            }

            return reading < Target
                ? string.Format(CultureInfo.InvariantCulture, "Add {0:0.0} L of concentrate.", ConcentrateToAdd(volume, reading, Target))
                : string.Format(CultureInfo.InvariantCulture, "Add {0:0.0} L of water.", WaterToAdd(volume, reading, Target));
        }
    }

    /// <summary>True when the check has everything the log needs.</summary>
    public bool CanLog => TryVolume(out _) && TryReading(out _);

    /// <summary>The five most recent log lines, newest first.</summary>
    public IReadOnlyList<string> RecentLines =>
        File.Exists(logPath)
            ? File.ReadAllLines(logPath).Reverse().Take(5).ToList()
            : Array.Empty<string>();

    /// <summary>Litres of concentrate that raise the mix from reading to target.</summary>
    public static double ConcentrateToAdd(double volume, double reading, double target) =>
        volume * (target - reading) / (100.0 - target);

    /// <summary>Litres of water that lower the mix from reading to target.</summary>
    public static double WaterToAdd(double volume, double reading, double target) =>
        volume * (reading - target) / target;

    /// <summary>Call after a check has been written to the log.</summary>
    public void LogWritten()
    {
        Note = string.Empty;
        OnPropertyChanged(nameof(RecentLines));
    }

    private bool TryVolume(out double volume) =>
        double.TryParse(VolumeText, NumberStyles.Float, CultureInfo.InvariantCulture, out volume)
        && volume > 0 && volume <= 5000;

    private bool TryReading(out double reading) =>
        double.TryParse(ReadingText, NumberStyles.Float, CultureInfo.InvariantCulture, out reading)
        && reading >= 0 && reading < 100;

    // Refresh everything that depends on the inputs.
    private void Recalculate()
    {
        OnPropertyChanged(nameof(Instruction));
        OnPropertyChanged(nameof(CanLog));
        OnPropertyChanged(nameof(RecentLines));
    }

    private bool Set<T>(ref T field, T value, [CallerMemberName] string? name = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value))
        {
            return false;
        }

        field = value;
        OnPropertyChanged(name);
        return true;
    }

    private void OnPropertyChanged(string? name) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
