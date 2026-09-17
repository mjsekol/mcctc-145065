// ScreenWordsTests.cs  .  Lab U09-03  .  Line3.Words.Tests
//
// The screen words, checked three ways:
//   1. the code says the agreed word for every state
//   2. docs/screen-words.txt lists exactly the words the code can show
//   3. docs/USER_GUIDE.md uses every one of them
//
//   dotnet test Line3.Words.Tests

using System.Text.RegularExpressions;
using Line3.Words;

namespace Line3.Words.Tests;

public class ScreenWordsTests
{
    private static string Doc(string name) =>
        File.ReadAllText(Path.Combine(AppContext.BaseDirectory, "docs", name));

    [Theory]
    [InlineData(TileState.Normal, "NORMAL")]
    [InlineData(TileState.AlarmHigh, "ALARM HIGH")]
    [InlineData(TileState.AlarmLow, "ALARM LOW")]
    [InlineData(TileState.Stale, "STALE")]
    [InlineData(TileState.Missing, "NO DATA")]
    public void EachTileStateShowsItsAgreedWord(TileState state, string word)
    {
        Assert.Equal(word, ScreenWords.ForTile(state));
    }

    [Theory]
    [InlineData(Connection.Waiting, "WAITING")]
    [InlineData(Connection.Connected, "CONNECTED")]
    [InlineData(Connection.NotUpdating, "DATA NOT UPDATING")]
    [InlineData(Connection.Lost, "NO CONNECTION")]
    public void EachConnectionStateShowsItsAgreedWord(Connection connection, string word)
    {
        Assert.Equal(word, ScreenWords.ForConnection(connection));
    }

    [Fact]
    public void TheWordsFileListsExactlyWhatTheCodeCanShow()
    {
        List<string> listed = Doc("screen-words.txt")
            .Split('\n')
            .Select(line => line.Trim())
            .Where(line => line.Length > 0 && !line.StartsWith('#'))
            .ToList();
        Assert.Equal(ScreenWords.All, listed);
    }

    [Fact]
    public void TheGuideUsesEveryScreenWord()
    {
        string guide = Doc("USER_GUIDE.md");
        List<string> missing = ScreenWords.All
            .Where(word => !guide.Contains(word, StringComparison.Ordinal))
            .ToList();
        Assert.Empty(missing);
    }

    [Fact]
    public void NoTwoStatesShareAWord()
    {
        Assert.Equal(ScreenWords.All.Count, ScreenWords.All.Distinct().Count());
    }

    [Fact]
    public void NoExplanationEverContainsANumber()
    {
        foreach (TileState state in Enum.GetValues<TileState>())
        {
            Assert.DoesNotMatch(new Regex("[0-9]"), ScreenWords.ExplainTile(state));
        }
    }
}
