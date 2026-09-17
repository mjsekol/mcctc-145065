// RackTests.cs
// Part B. These tests describe what the Python Equipment and StorageRack do.
// Do not edit them. Make them pass by finishing Equipment.cs and StorageRack.cs.

using Line3.Port;

namespace Line3.Port.Tests;

public class RackTests
{
    private static StorageRack Rack() => new("L3-RCK-01", "Finished Goods Rack", 1200);

    [Fact]
    public void B01_a_rack_is_equipment_with_a_kind()
    {
        Equipment item = Rack();
        Assert.Equal("L3-RCK-01", item.AssetTag);
        Assert.Equal("Finished Goods Rack", item.Name);
        Assert.Equal("rack", item.Kind);
        Assert.Equal(1200, Rack().CapacityKg);
    }

    [Theory]
    [InlineData("L3-RCK-01", true)]
    [InlineData("l3-rck-01", false)]
    [InlineData("L3-RCK-1", false)]
    [InlineData("L3-RCK-01\n", false)]
    [InlineData(null, false)]
    public void B02_asset_tags_follow_the_pattern(string? tag, bool expected)
    {
        Assert.Equal(expected, Equipment.IsValidAssetTag(tag));
    }

    [Fact]
    public void B03_a_bad_tag_or_blank_name_is_refused()
    {
        Assert.Throws<ArgumentException>(() => new StorageRack("RACK-1", "Finished Goods Rack", 1200));
        Assert.Throws<ArgumentException>(() => new StorageRack("L3-RCK-01", " ", 1200));
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-50)]
    public void B04_capacity_must_be_above_zero(double capacity)
    {
        Assert.ThrowsAny<ArgumentException>(() => new StorageRack("L3-RCK-01", "Finished Goods Rack", capacity));
    }

    [Fact]
    public void B05_describe_extends_the_base_description()
    {
        StorageRack rack = Rack();
        rack.LoadKg = 1150;
        Assert.Equal("L3-RCK-01 Finished Goods Rack (rack), 96% full", rack.Describe());
    }

    [Fact]
    public void B06_an_overload_is_recorded_not_refused()
    {
        StorageRack rack = Rack();
        rack.LoadKg = 1500;
        Assert.Equal(1500, rack.LoadKg);
        Assert.Equal("L3-RCK-01 Finished Goods Rack (rack), 125% full", rack.Describe());
    }

    [Fact]
    public void B07_a_negative_load_is_refused_and_the_old_load_is_kept()
    {
        StorageRack rack = Rack();
        rack.LoadKg = 300;
        Assert.ThrowsAny<ArgumentException>(() => rack.LoadKg = -5);
        Assert.Equal(300, rack.LoadKg);
    }
}
