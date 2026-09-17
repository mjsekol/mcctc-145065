# TileWords · Lab U09-03 practice library

The screen words for a small practice panel, the user guide that explains them, and the tests that
hold the two together. Riverside Fabrication and its Line 3 are a composite, an invented shop.

This is not your panel. It is a small copy of the same problem, so you can practice a change request
where every result is known, before you change your own panel.

## Run the tests

From this folder:

```
dotnet test Line3.Words.Tests
```

Version 1.0.0 passes 13 tests.

## What is here

| Path | What it is |
|---|---|
| `Line3.Words/ScreenWords.cs` | every word the practice panel can show |
| `Line3.Words/Line3.Words.csproj` | the project, with the release `<Version>` |
| `Line3.Words.Tests/ScreenWordsTests.cs` | the words, the words file, and the guide, checked together |
| `docs/screen-words.txt` | the words, one per line, for people and for ShipCheck |
| `docs/USER_GUIDE.md` | the operator's guide to those words |
| `CHANGELOG.md` | what changed in each version, newest first |
