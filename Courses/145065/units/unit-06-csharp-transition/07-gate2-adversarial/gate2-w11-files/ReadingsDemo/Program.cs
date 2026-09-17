// ReadingsDemo: a short run of ReadingLog you can compare against the requirements.
// Invented readings. Riverside Fabrication is a composite: an invented shop.

using Line3.Readings;

var log = new ReadingLog("oven-temp", keepLast: 5);
foreach (double reading in new[] { 201.0, 205.0, 210.0, 230.0 })
{
    log.Record(reading);
}

Console.WriteLine($"{log.SensorId}: {log.Count} readings, keeps the last {log.KeepLast}");
Console.WriteLine($"Latest: {log.Latest}");
Console.WriteLine($"In range 200 to 215: {log.PercentInRange(200, 215)}%");
Console.WriteLine($"Above average: {log.CountAboveAverage()}");
Console.WriteLine($"Stale: {log.IsStale}");

foreach (double reading in new[] { 199.0, 198.0 })
{
    log.Record(reading);
}
Console.WriteLine($"After two more: {string.Join(", ", log)}");

var empty = new ReadingLog("coolant-level");
Console.WriteLine($"{empty.SensorId}: latest {empty.Latest}, stale {empty.IsStale}");

try
{
    log.Record(double.NaN);
}
catch (ArgumentOutOfRangeException error)
{
    Console.WriteLine($"Refused: {error.Message.Split(" (")[0]}");
}
