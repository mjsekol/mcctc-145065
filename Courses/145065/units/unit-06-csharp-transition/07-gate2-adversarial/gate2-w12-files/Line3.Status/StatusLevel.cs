namespace Line3.Status;

/// <summary>
/// What the status board shows for one reporter, from least to most urgent.
/// Missing ranks above Warning: a reporter the panel cannot hear from is
/// worse news than one that is running a little warm.
/// </summary>
public enum StatusLevel
{
    Normal,
    Warning,
    Missing,
    Alarm,
}
