// Program.cs  .  145065 Unit 7  .  TallyConsole
//
// The Line 3 shift tally written as a procedural program.
// Riverside Fabrication, Line 3, is a composite shop invented for this course.
//
// Read the loop before you run it. This program decides what happens next,
// every time, in order. It waits in exactly one place: Console.ReadLine.
// Nothing else can happen while it waits there.
//
// Run it:   dotnet run --project TallyConsole
// Type g for a good part, s for scrap, q to quit.

int good = 0;
int scrap = 0;

Console.WriteLine("Shift tally for Press 2.");
Console.WriteLine("Type g for a good part, s for scrap, q to quit.");

while (true)
{
    Console.Write("> ");
    string? input = Console.ReadLine();   // the program waits here, and only here

    if (input is null || input == "q")
    {
        break;
    }

    if (input == "g")
    {
        good++;
    }
    else if (input == "s")
    {
        scrap++;
    }
    else
    {
        Console.WriteLine("Unknown key. Type g, s, or q.");
        continue;
    }

    Console.WriteLine($"Good: {good}  Scrap: {scrap}  Total: {good + scrap}");
}

Console.WriteLine($"Shift over. {good + scrap} parts counted.");
