namespace Line3.Reader;

/// <summary>
/// One sensor in one reply. Value is always a number so the display never has to
/// handle null; Ok says whether the sensor actually produced it.
/// </summary>
public sealed record SensorReading(string Id, string Kind, double Value, string Unit, bool Ok);

/// <summary>One complete reply from the Line 3 sensor service.</summary>
public sealed record ReadingBatch(string Device, long Sequence, DateTimeOffset SampledAt, IReadOnlyList<SensorReading> Sensors)
{
    public SensorReading? Find(string id) => Sensors.FirstOrDefault(s => s.Id == id);
}

/// <summary>The outcome of one read: a batch, or the reason there is none.</summary>
public sealed record ReadResult(ReadingBatch? Batch, string? Problem)
{
    public bool Ok => Batch is not null;

    public static ReadResult Success(ReadingBatch batch) => new(batch, null);

    public static ReadResult Failed(string problem) => new(null, problem);
}
