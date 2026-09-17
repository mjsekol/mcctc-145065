using Line3.Reader;

namespace Line3.Reader.Tests;

public class ReaderTests
{
    private const string Contract = """
        {"device": "line3-pi", "sequence": 1042, "sampled_at": "2027-01-11T14:03:22Z",
         "sensors": [
           {"id": "oven-temp", "kind": "temperature", "value": 212.4, "unit": "C", "ok": true},
           {"id": "press-vibration", "kind": "vibration", "value": 3.1, "unit": "mm/s", "ok": true},
           {"id": "coolant-level", "kind": "level", "value": null, "unit": "%", "ok": false}]}
        """;

    private static readonly SensorLimit Oven = new() { Id = "oven-temp", Low = 190.0, High = 230.0, Reason = "coating cure range" };

    [Fact]
    public void ParsesTheContractExample()
    {
        ReadingBatch? batch = ReadingParser.Parse(Contract, out string? problem);

        Assert.Null(problem);
        Assert.NotNull(batch);
        Assert.Equal(1042, batch.Sequence);
        Assert.Equal(212.4, batch.Find("oven-temp")!.Value);
    }

    [Fact]
    public void AFailedSensorKeepsOkFalse()
    {
        ReadingBatch batch = ReadingParser.Parse(Contract, out _)!;

        Assert.False(batch.Find("coolant-level")!.Ok);
    }

    [Fact]
    public void BrokenJsonIsAProblemNotACrash()
    {
        ReadingBatch? batch = ReadingParser.Parse("{\"device\": \"line3-pi\", \"sequence\": 17, \"sampled_at\": \"2027", out string? problem);

        Assert.Null(batch);
        Assert.NotNull(problem);
    }

    [Theory]
    [InlineData(212.4, AlarmState.Normal)]
    [InlineData(230.0, AlarmState.Normal)]
    [InlineData(190.0, AlarmState.Normal)]
    [InlineData(236.0, AlarmState.AlarmHigh)]
    [InlineData(185.5, AlarmState.AlarmLow)]
    public void LimitsAreInclusive(double value, AlarmState expected)
    {
        SensorReading reading = new("oven-temp", "temperature", value, "C", true);

        Assert.Equal(expected, AlarmRules.Evaluate(reading, Oven));
    }

    [Fact]
    public void TheLimitsFileLoads()
    {
        LimitsFile limits = LimitsFile.Load(Path.Combine(AppContext.BaseDirectory, "limits.json"));

        Assert.Equal(3, limits.Sensors.Count);
        Assert.Equal(TimeSpan.FromMilliseconds(1500), limits.RequestTimeout);
        Assert.Null(limits.Find("press-vibration")!.Low);
    }
}
