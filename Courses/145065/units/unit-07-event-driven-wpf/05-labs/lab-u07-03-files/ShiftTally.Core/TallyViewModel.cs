// TallyViewModel.cs  .  145065 Unit 7  .  ShiftTally.Core
//
// Lab U07-03 STARTER. Adapted from the course's HMI anchor
// (anchor-project/hmi/panel/w13_wpf_basics/ShiftTally/TallyViewModel.cs).
//
// A view model holds everything the window shows, as properties, and does
// everything the buttons do, as methods. It knows nothing about windows,
// buttons, or TextBlocks. That is why this project targets plain net8.0 and
// ShiftTally.Core.Tests can test every line without opening a window.
//
// Monday (steps 1 to 6): write the members that throw NotImplementedException.
// Wednesday (steps 13 to 18): make the class announce its changes.
//
// Setting: Riverside Fabrication, Line 3, is a composite. It is not a real shop.

namespace ShiftTally.Core;

public sealed class TallyViewModel
{
    public const int MinimumTarget = 50;
    public const int MaximumTarget = 500;

    private readonly Stack<bool> history = new();   // true = a good part, false = scrap
    private string station = "Press 2";
    private string partType = "Hinge bracket";
    private string status = "Count each part as it leaves the station.";
    private bool showScrapRate = true;

    // Step 2: add the fields for the good count, the scrap count, and the
    // target (which starts at 200).

    public IReadOnlyList<string> PartTypes { get; } = new[] { "Hinge bracket", "Mounting rail", "Cover plate" };

    // ---- Station and part: written for you ------------------------------------

    public string Station
    {
        get => station;
        set => station = value ?? string.Empty;   // stored exactly as typed
    }

    public string StationName => Station.Trim();

    public bool StationIsValid => StationName.Length is > 0 and <= 20;

    public string PartType
    {
        get => partType;
        set => partType = value ?? string.Empty;
    }

    public string Heading => StationIsValid
        ? $"{StationName}: {PartType}"
        : $"(name the station): {PartType}";

    // ---- Counts: step 2 ----------------------------------------------------------

    /// <summary>Good parts this shift. Only AddGood, Undo, and Reset may change it.</summary>
    public int Good => throw new NotImplementedException("Lab U07-03 step 2: Good");

    /// <summary>Scrap parts this shift. Only AddScrap, Undo, and Reset may change it.</summary>
    public int Scrap => throw new NotImplementedException("Lab U07-03 step 2: Scrap");

    public int Total => throw new NotImplementedException("Lab U07-03 step 2: Total");

    public bool CanUndo => history.Count > 0;

    // ---- Target, progress, and rate: step 2 ---------------------------------------

    /// <summary>The slider will bind here. Pull values outside 50 to 500 back into range.</summary>
    public int Target
    {
        get => throw new NotImplementedException("Lab U07-03 step 2: Target get");
        set => throw new NotImplementedException("Lab U07-03 step 2: Target set");
    }

    /// <summary>0 to 100, for the progress bar. Only good parts count toward the target.</summary>
    public double Progress => throw new NotImplementedException("Lab U07-03 step 2: Progress");

    public string ProgressText => throw new NotImplementedException("Lab U07-03 step 2: ProgressText");

    public bool ShowScrapRate
    {
        get => showScrapRate;
        set => showScrapRate = value;
    }

    public string ScrapRateText => throw new NotImplementedException("Lab U07-03 step 2: ScrapRateText");

    // ---- Status line and text for the handlers: step 4 ------------------------------

    public string Status
    {
        get => status;
        set => status = value ?? string.Empty;
    }

    public string ResetQuestion => throw new NotImplementedException("Lab U07-03 step 4: ResetQuestion");

    public string SummaryText => throw new NotImplementedException("Lab U07-03 step 4: SummaryText");

    // ---- What the buttons do: step 3 ---------------------------------------------------

    public void AddGood() => throw new NotImplementedException("Lab U07-03 step 3: AddGood");

    public void AddScrap() => throw new NotImplementedException("Lab U07-03 step 3: AddScrap");

    /// <summary>Takes back the last part counted, whichever kind it was. Does nothing if there is none.</summary>
    public void Undo() => throw new NotImplementedException("Lab U07-03 step 3: Undo");

    public void Reset() => throw new NotImplementedException("Lab U07-03 step 3: Reset");
}
