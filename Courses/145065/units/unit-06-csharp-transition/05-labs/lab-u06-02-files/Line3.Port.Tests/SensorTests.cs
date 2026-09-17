// SensorTests.cs
// Part A. These tests describe what the Python Sensor does. Do not edit them.
// Make them pass by finishing Line3.Port/Sensor.cs.

using Line3.Port;

namespace Line3.Port.Tests;

public class SensorTests
{
    private static Sensor OvenTemp() => new("oven-temp", "temperature", "C", 0, 240);

    [Fact]
    public void A01_constructor_stores_every_value()
    {
        Sensor s = OvenTemp();
        Assert.Equal("oven-temp", s.Id);
        Assert.Equal("temperature", s.Kind);
        Assert.Equal("C", s.Unit);
        Assert.Equal(0, s.Low);
        Assert.Equal(240, s.High);
    }

    [Fact]
    public void A02_a_new_sensor_has_no_reading_not_zero()
    {
        Sensor s = OvenTemp();
        Assert.Null(s.Value);
        Assert.Equal("no reading", s.Status());
    }

    [Theory]
    [InlineData(212.4, "ok")]
    [InlineData(-3, "low")]
    [InlineData(251, "high")]
    [InlineData(240, "ok")]
    public void A03_status_follows_the_limits(double reading, string expected)
    {
        Sensor s = OvenTemp();
        s.Record(reading);
        Assert.Equal(reading, s.Value);
        Assert.Equal(expected, s.Status());
    }

    [Fact]
    public void A04_clear_means_missing_again()
    {
        Sensor s = OvenTemp();
        s.Record(212.4);
        s.Clear();
        Assert.Null(s.Value);
        Assert.Equal("no reading", s.Status());
    }

    [Theory]
    [InlineData(double.NaN)]
    [InlineData(double.PositiveInfinity)]
    public void A05_record_refuses_values_that_are_not_measurements(double bad)
    {
        Sensor s = OvenTemp();
        Assert.Throws<ArgumentOutOfRangeException>(() => s.Record(bad));
        Assert.Null(s.Value);
    }

    [Theory]
    [InlineData("Oven-Temp")]
    [InlineData("oven temp")]
    [InlineData("")]
    public void A06_bad_ids_are_refused(string id)
    {
        Assert.Throws<ArgumentException>(() => new Sensor(id, "temperature", "C", 0, 240));
    }

    [Fact]
    public void A07_blank_kind_or_unit_is_refused()
    {
        Assert.Throws<ArgumentException>(() => new Sensor("oven-temp", "  ", "C", 0, 240));
        Assert.Throws<ArgumentException>(() => new Sensor("oven-temp", "temperature", "", 0, 240));
    }

    [Fact]
    public void A08_low_must_be_below_high()
    {
        Assert.Throws<ArgumentException>(() => new Sensor("oven-temp", "temperature", "C", 240, 240));
    }
}
