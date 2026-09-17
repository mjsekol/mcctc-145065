// Intruder: code in another project that uses Line3.Monitor the wrong way.
// Lab U06-03, Part 1. This project is not in the solution on purpose.
//
// Build and run it before you lock Reading down, and write down what it prints.
// Build it again after. When Part 1 is done, this project must NOT build.
// The errors it produces are your evidence.

using Line3.Monitor;

var reading = new Reading("oven-temp", 212.4, 7);

reading.Value = double.NaN;
reading.SensorId = "";
reading.Sequence = -1;

Console.WriteLine($"id '{reading.SensorId}', value {reading.Value}, sequence {reading.Sequence}, missing {reading.IsMissing}");
