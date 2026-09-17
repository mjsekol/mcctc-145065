# HMI PANEL project files

Everything you copy into your `hmi-panel` repository for the Unit 8 project. Riverside Fabrication and its
Line 3 are a composite, an invented shop.

| Path | What it is |
|---|---|
| `HmiPanel/` | the starter solution: four projects, builds with 0 warnings |
| `templates/` | starting points for six of your `docs/` files |
| `DISCONNECT_DEMO_RUNBOOK.md` | the script for the disconnect demonstration, with the safety brief |

Also copy `05-labs/sensor-service/` into your repository as `sensor-service/`, next to `HmiPanel/`. The
live acceptance test finds it there.

---

## The starter solution

```
HmiPanel/
  HmiPanel.sln
  Line3.Hmi.Core/            net8.0 library: everything that is not a window
  Line3.Hmi.Core.Tests/      xunit acceptance tests, named for the requirements
  Line3.Hmi.Panel/           net8.0-windows WPF app: the window, your view, your limits
  Line3.Hmi.Snapshots/       renders your view to PNG files without opening a window
```

Most files are copied from the course's HMI anchor, and say so in their first lines. **Five places are
yours**, and each says so in its first lines:

| File | What you put there |
|---|---|
| `Line3.Hmi.Core/StateRules.Truth.cs` | `Decide`, from Lab U8-03 |
| `Line3.Hmi.Core/PanelConfig.cs` | `SensorThreshold.Check`, from Lab U8-03 |
| `Line3.Hmi.Core/StateRules.Freshness.cs` | `CheckFreshness`, from Lab U8-04 |
| `Line3.Hmi.Core/ViewModels/SensorTileViewModel.cs` | the `switch` in `Apply`, from Lab U8-04 |
| `Line3.Hmi.Core/AlarmLatch.cs` and three methods in `ViewModels/PanelViewModel.cs` | from Lab U8-05 |

Plus two files that are yours from the start: **`Line3.Hmi.Panel/PanelView.xaml`**, your screen, and
**`Line3.Hmi.Panel/thresholds.json`**, your limits. The starter's oven reason reads `REPLACE THIS...`,
and a test fails until your team writes its own.

## Build, test, run

From `HmiPanel/`. Use a build folder outside your repository [VERIFY a folder you may write to]:

```
dotnet build HmiPanel.sln --artifacts-path C:\build\hmi
dotnet test Line3.Hmi.Core.Tests --artifacts-path C:\build\hmi
dotnet run --project Line3.Hmi.Panel --artifacts-path C:\build\hmi
dotnet run --project Line3.Hmi.Panel --artifacts-path C:\build\hmi -- --url http://127.0.0.1:8700 --fullscreen
dotnet run --project Line3.Hmi.Snapshots --artifacts-path C:\build\hmi -- ..\docs\screens
```

The panel reads `thresholds.json`, which points at `http://127.0.0.1:8700`. Start the simulator first:
`python sensor_service.py --port 8700` in `sensor-service/`.

**The acceptance tests use ports 8702 and 8703**, and the live test starts the simulator itself on 8703.
Make sure nothing else holds those ports: `netstat -ano | findstr :870`. The live test needs `python` on
your PATH, or the environment variable `HMI_PYTHON` set to your Python. If your `sensor-service` folder
is somewhere else, set `HMI_SERVICE_DIR` to it.

**The starter's state, as delivered:** it builds; the panel opens and shows WAITING, then tiles that all
say NO DATA, because the pieces you write are still stubs; the acceptance tests report 12 passed and
17 failed. Every failing test names the requirement it proves.

## What a person must still check on a lab machine

A PNG proves the XAML lays out. It does not prove a gloved finger can press a button, that the screen
reads under the lab lights, or that Escape closes the confirmation. Try each of those on the lab's touch
screen, and write what you found in `docs/DEMO_RECORD.md` [VERIFY].
