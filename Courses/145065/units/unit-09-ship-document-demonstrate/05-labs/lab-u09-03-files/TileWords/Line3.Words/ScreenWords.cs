// ScreenWords.cs  .  Lab U09-03  .  Line3.Words  .  version 1.0.0
//
// Every word the practice panel shows an operator, in one place.
//
// Why one place: an operator learns these words from the user guide and
// from training. The words are an interface between the software and a
// person. Change one here, and the guide, the training card, the pictures,
// and the tests all have to change with it. This file is where that
// change starts, and the tests are where you find out what it touched.
//
// Riverside Fabrication and its Line 3 are a composite, an invented shop.

namespace Line3.Words;

/// <summary>What one sensor tile can show.</summary>
public enum TileState
{
    Normal,
    AlarmHigh,
    AlarmLow,
    Stale,
    Missing,
}

/// <summary>What the badge in the top bar can show.</summary>
public enum Connection
{
    Waiting,
    Connected,
    NotUpdating,
    Lost,
}

public static class ScreenWords
{
    /// <summary>The big word on a tile.</summary>
    public static string ForTile(TileState state) => state switch
    {
        TileState.Normal => "NORMAL",
        TileState.AlarmHigh => "ALARM HIGH",
        TileState.AlarmLow => "ALARM LOW",
        TileState.Stale => "STALE",
        TileState.Missing => "NO DATA",
        _ => throw new ArgumentOutOfRangeException(nameof(state), state, "no word for this tile state"),
    };

    /// <summary>The big word on the connection badge.</summary>
    public static string ForConnection(Connection connection) => connection switch
    {
        Connection.Waiting => "WAITING",
        Connection.Connected => "CONNECTED",
        Connection.NotUpdating => "DATA NOT UPDATING",
        Connection.Lost => "NO CONNECTION",
        _ => throw new ArgumentOutOfRangeException(nameof(connection), connection, "no word for this connection state"),
    };

    /// <summary>The sentence under the big word. Never a number.</summary>
    public static string ExplainTile(TileState state) => state switch
    {
        TileState.Normal => "Live. Inside limits.",
        TileState.AlarmHigh => "Live. Above the high limit. Check the machine.",
        TileState.AlarmLow => "Live. Below the low limit. Check the machine.",
        TileState.Stale => "This reading is old, so it is not live. Check it at the machine.",
        TileState.Missing => "The panel has no reading. Check it at the machine.",
        _ => throw new ArgumentOutOfRangeException(nameof(state), state, "no sentence for this tile state"),
    };

    /// <summary>Every word an operator can see, tiles first, then the badge.</summary>
    public static IReadOnlyList<string> All =>
        Enum.GetValues<TileState>().Select(ForTile)
            .Concat(Enum.GetValues<Connection>().Select(ForConnection))
            .ToList();
}
