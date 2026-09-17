# Event flow · <your app's name>

Copy this file to `docs/event-flow.md` in your project and replace every part in angle brackets.
Delete this paragraph and the model rows when you are done.

**Where the model came from.** The model rows below are adapted from the course's HMI anchor project,
the event flow document for the Week 13 ShiftTally app. Your diagram follows the same shape.

---

## 1. What waits, and what calls your code

One or two sentences: which window your app opens, and which events can make your code run. Name the
kinds: presses, typing, selections, timer ticks, the window opening or closing.

```
          +---------------------------------------------+
          |  WPF dispatcher (the UI thread's event loop) |
          |   waits for the next item, runs it to the end |
          +---------------------------------------------+
               ^              ^              ^
               |              |              |
          <your inputs>  <your timer?>  <window opening, closing>
```

---

## 2. Every event your app handles

One row per event. "Handled in" is a method name, or "binding" when a two-way binding writes the value
back with no handler of yours. "What changes" names the view model members and what redraws.

| Event | Raised by | Handled in | What changes |
|---|---|---|---|
| <event> | <control> | <method or binding> | <view model change, then what the screen redraws> |

**Model rows, from ShiftTally (Week 14 version):**

| Event | Raised by | Handled in | What changes |
|---|---|---|---|
| `Click` on +1 GOOD | `GoodButton` | `MainWindow.OnGoodClick` calls `TallyViewModel.AddGood` | `Good` goes up; `Total`, `Progress`, `ProgressText`, `ScrapRateText`, `CanUndo`, and `Status` are announced; their controls redraw |
| `Click` on RESET SHIFT | `ResetButton` | `MainWindow.OnResetClick` | asks a Yes/No question first; resets only on Yes; on No, the status says the counts are kept |
| text typed | `StationBox` | binding, `UpdateSourceTrigger=PropertyChanged` | `Station`, then `Heading` is announced and the heading redraws |
| slider moved | `TargetSlider` | two-way binding | `Target`, then `Progress` and `ProgressText` are announced |
| box checked or cleared | `ShowRateBox` | binding | `ShowScrapRate`; the rate text shows or hides |

---

## 3. The dependency table

For each value that can change, list everything that must be announced with it. This is the table your
notification tests check.

| When this changes | Also announce |
|---|---|
| <value> | <dependent properties> |

---

## 4. The most important action, in order

Draw the sequence for the one action your operator cares about most. Show who calls whom, and where
the screen redraws.

```
operator        <button>          MainWindow            <ViewModel>
   |                |                  |                      |
   |-- press ------>|                  |                      |
   |                |-- Click -------->|                      |
   |                |                  |-- <Method>() ------->|
   |                |                  |                      | <state changes>
   |                |                  |                      | PropertyChanged(<names>)
   |<-- bound controls redraw ---------------------------------|
```

---

## 5. What the operator cannot break

One line per destructive or slow action: what protects the operator. For example: "CLEAR asks first,
with No as the default." or "PRINT is awaited, so the window keeps working."
