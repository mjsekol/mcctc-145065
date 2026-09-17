# What actually changed since the baseline

The Line 3 panel team's own record. Riverside Fabrication and its Line 3 are a composite, an invented
shop. The commit ids below are invented sample data.

## The baseline

`v1.0.0`, tagged Week 17, Wednesday. The shift lead was trained on it on Week 17, Thursday.

## Every commit since `v1.0.0`, oldest first

```
a41c9e2 Add "It does not mean the machine stopped." to every NO DATA sentence (F1)
7be0d13 Add six tests that hold the NO DATA sentence in place
c02f5a8 Render the worst-case NO DATA tile with an alarm banner; it fits
e9d3b71 User guide: limits table, and "the red tile stays red" after acknowledging (F2, F3)
5f16a0c Set <Version> to 1.1.0 in Line3.Hmi.Panel.csproj
b88d2f4 Add ReleaseGate, written with an AI assistant, for the install step
```

## Files touched

| File | Commits |
|---|---|
| `Line3.Hmi.Core/PanelMonitor.cs` | a41c9e2 |
| `Line3.Hmi.Core.Tests/ReleaseTests.cs` | 7be0d13 |
| `Line3.Hmi.Snapshots/Program.cs` | c02f5a8 |
| `docs/USER_GUIDE.md` | e9d3b71 |
| `docs/screens/*.png` | c02f5a8 |
| `Line3.Hmi.Panel/Line3.Hmi.Panel.csproj` | 5f16a0c |
| `ReleaseGate/*` | b88d2f4 |

No commit touched `Line3.Hmi.Panel/PanelView.xaml`, `MainWindow.xaml.cs`, `thresholds.json`, or anything
in `sensor-service/`.

## The request the team gave the AI assistant

> Write a release plan for version 1.1.0 of our Line 3 Sensor Monitor, for our shift lead and for us.
> Use our commit list and our operator test notes. Include what changed for operators, a change impact
> section, the install gate, how we roll it out, and how we roll back.
