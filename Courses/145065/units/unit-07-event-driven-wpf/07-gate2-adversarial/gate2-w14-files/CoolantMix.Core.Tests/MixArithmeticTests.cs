// MixArithmeticTests.cs
// Tests for the mix arithmetic, as the shop requires for anything that tells
// an operator how much to add.

using CoolantMix.Core;

namespace CoolantMix.Core.Tests;

public class MixArithmeticTests
{
    [Theory]
    [InlineData(400, 5.0, 7.0, 8.602)]
    [InlineData(400, 5.0, 6.0, 4.255)]
    [InlineData(1000, 4.0, 8.0, 43.478)]
    public void ConcentrateRaisesTheMixToTarget(double volume, double reading, double target, double expected)
    {
        Assert.Equal(expected, MixViewModel.ConcentrateToAdd(volume, reading, target), 3);
    }

    [Theory]
    [InlineData(400, 9.0, 6.0, 200.0)]
    [InlineData(1000, 8.0, 7.5, 66.667)]
    public void WaterLowersTheMixToTarget(double volume, double reading, double target, double expected)
    {
        Assert.Equal(expected, MixViewModel.WaterToAdd(volume, reading, target), 3);
    }

    [Fact]
    public void AWeakMixAsksForConcentrate()
    {
        MixViewModel mix = new("unused.csv") { VolumeText = "400", ReadingText = "5.0" };
        Assert.Equal("Add 4.3 L of concentrate.", mix.Instruction);
    }

    [Fact]
    public void AStrongMixAsksForWater()
    {
        MixViewModel mix = new("unused.csv") { VolumeText = "400", ReadingText = "9.0" };
        Assert.Equal("Add 200.0 L of water.", mix.Instruction);
    }

    [Theory]
    [InlineData("6.2")]
    [InlineData("5.8")]
    public void AReadingWithinTheBandNeedsNothing(string reading)
    {
        MixViewModel mix = new("unused.csv") { VolumeText = "400", ReadingText = reading };
        Assert.Equal("Mix is on target. Add nothing.", mix.Instruction);
    }

    [Theory]
    [InlineData("", "5.0")]
    [InlineData("400", "")]
    [InlineData("-50", "5.0")]
    [InlineData("four hundred", "5.0")]
    public void BadInputsGiveNoAmount(string volume, string reading)
    {
        MixViewModel mix = new("unused.csv") { VolumeText = volume, ReadingText = reading };
        Assert.Equal("Enter the sump volume and the reading.", mix.Instruction);
        Assert.False(mix.CanLog);
    }
}
