// Program.cs  .  Lab U08-05  .  ShiftReplay  .  given to you
//
//   dotnet run --project ShiftReplay
//
// Plays one scripted stretch of a shift through YOUR AlarmLatch and YOUR
// acknowledge methods, and prints what the oven tile shows after each step.
// Riverside Fabrication is a composite. The shift is invented.

using Line3.Hmi.Core;
using Line3.Hmi.Core.ViewModels;

AlarmBoard board = new(new[] { ("oven-temp", "Cure oven temperature") });
AlarmTile oven = board.TileOf("oven-temp");

Console.WriteLine("step  what happens                              state    latch            banner                          question");
Step(1, "oven reads 212.0, live", () => board.Observe("oven-temp", SensorState.Normal));
Step(2, "oven reads 236.0, live", () => board.Observe("oven-temp", SensorState.Alarm));
Step(3, "the Pi freezes", () => board.Observe("oven-temp", SensorState.Stale));
Step(4, "the cable is pulled", () => board.Observe("oven-temp", SensorState.Missing));
Step(5, "operator presses ACKNOWLEDGE ALARM", () => oven.AcknowledgeCommand.Execute(null));
Step(6, "operator presses CANCEL", () => board.CancelAcknowledgeCommand.Execute(null));
Step(7, "ACKNOWLEDGE ALARM, then YES", () =>
{
    oven.AcknowledgeCommand.Execute(null);
    board.ConfirmAcknowledgeCommand.Execute(null);
});
Step(8, "cable back, oven reads 234.0, live", () => board.Observe("oven-temp", SensorState.Alarm));
Step(9, "oven reads 212.0, live", () => board.Observe("oven-temp", SensorState.Normal));
Step(10, "oven reads 237.0, live", () => board.Observe("oven-temp", SensorState.Alarm));
Step(11, "oven reads 212.0, nobody acknowledged", () => board.Observe("oven-temp", SensorState.Normal));
Step(12, "ACKNOWLEDGE ALARM, then YES", () =>
{
    oven.AcknowledgeCommand.Execute(null);
    board.ConfirmAcknowledgeCommand.Execute(null);
});
Step(13, "operator presses ACKNOWLEDGE ALARM", () => oven.AcknowledgeCommand.Execute(null));

Console.WriteLine();
Console.WriteLine("Log:");
foreach (string line in board.Log)
{
    Console.WriteLine("  " + line);
}

return 0;

void Step(int number, string what, Action act)
{
    act();
    string banner = oven.BannerText.Length == 0 ? "(none)" : oven.BannerText;
    string question = board.IsConfirmOpen ? "OPEN" : "closed";
    Console.WriteLine($"{number,4}  {what,-40}  {oven.State,-7}  {oven.Latch,-15}  {banner,-30}  {question}");
}
