// StatusDemo: a short run of the status board you can compare against the requirements.
// Invented readings. Riverside Fabrication is a composite: an invented shop.

using Line3.Status;

var oven = new TemperatureProbe("L3-OVN-01", warnAtC: 215, alarmAtC: 240);
var guard1 = new GuardSwitch("L3-PRS-01-G");
var guard2 = new GuardSwitch("L3-PRS-02-G");

var board = new StatusBoard();
board.Add(oven);
board.Add(guard1);
board.Add(guard2);

oven.Record(212.0);
guard1.Update(closed: true);
Print("Start of shift");

oven.Record(250.0);
guard1.Update(closed: false);
Print("Twenty minutes later");

void Print(string title)
{
    Console.WriteLine(title);
    foreach (string line in board.Lines())
    {
        Console.WriteLine("  " + line);
    }
    Console.WriteLine($"  Worst: {board.Worst()}");
}
