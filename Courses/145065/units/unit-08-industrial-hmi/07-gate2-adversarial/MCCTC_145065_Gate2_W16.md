# Gate 2: Adversarial Review · Week 16
## 145065 Object-Oriented Programming · Unit 8 · Week 16, Friday

**35 minutes.** Individual. You may and should build, test, and run the code against the simulator in
several modes. You may not ask an AI tool whether the code is correct, because an AI tool wrote it.

The code is in `gate2-w16-files/`. Copy the folder. Riverside Fabrication is a composite shop.

---

## What you are looking at

A teammate asked an AI assistant for the fail-safe logic of the Line 3 panel: the part that turns the
Pi's replies into what the operator sees. The assistant put it all in one class, `LinePanel`, and wrote
tests for it. It builds with no warnings, and its five tests pass.

**Five defects, one in each dimension.** They are design defects. The code builds, runs, and reads well.

| Dimension | What to look for |
|---|---|
| **Correctness** | the panel stops telling the operator something it should still be telling them |
| **Security** | the panel does something a monitoring-only program must never be able to do |
| **Readability** | a design that makes the rules hard to find, read, and test |
| **Performance** | work that holds the window's thread when it should not |
| **Requirements Fit** | a requirement in Part A that the display does not meet |

**One defect only shows when the connection drops in the middle of an alarm.** **One defect is
arguable**: some operators would ask for it. Name it and argue both sides.

---

## PART A: The requirements

> Write `LinePanel`, the part of the Line 3 panel that turns the sensor service's replies into what the
> operator sees. The window calls `Tick()` from a once-a-second timer and binds to `Tiles` and
> `ConnectionText`.
>
> 1. Read `GET /api/readings` with a 1.5 s timeout. A slow or silent Pi must never freeze the window.
> 2. Each tile shows one of NORMAL, ALARM HIGH or ALARM LOW, STALE, NO DATA. **Stale:** the sample is
>    older than 5 s, or its sequence has not changed for 5 s. **Missing:** the request failed, the reply
>    was unreadable, or the sensor reported `ok: false`.
> 3. Never show a stale value as live. A stale value may appear only in `LastValueText`, marked not live,
>    never in the big `ValueText`.
> 4. Remember every alarm until a person acknowledges it **and** a live value is back inside limits.
>    Stale or missing data never clears an alarm.
> 5. Monitoring only. The panel sends nothing but `GET /api/readings`. It never changes anything on the
>    Pi.
> 6. Keep the rules (state, freshness, alarm memory) testable without a network or a window.

---

## PART B: What the AI produced

```
gate2-w16-files/
  Line3.FailSafe.sln
  Line3.FailSafe/
    Model.cs             SensorLimit, SensorState, LatchState, TileView
    LinePanel.cs         everything else
  Line3.FailSafe.Demo/   a console stand-in for the window's UI thread
  Line3.FailSafe.Tests/  the AI's own tests (port 8702, and 8704 kept free)
```

From the `gate2-w16-files` folder:

```
dotnet build Line3.FailSafe.sln
dotnet test Line3.FailSafe.Tests
dotnet run --project Line3.FailSafe.Demo -- --url http://127.0.0.1:8700 --seconds 10
```

The demo calls `Tick()` once a second from a loop that stands in for a window's UI thread, and prints the
connection, every tile, and **the longest the loop had to wait for its turn** that second. A window needs
a turn about every 100 ms to repaint.

Start the simulator first, from `05-labs/sensor-service/`, **without** `--quiet`, so it prints every
request it receives:

```
python sensor_service.py --port 8700
```

Useful modes: `drift` (the oven climbs into alarm in about ten seconds), `freeze`, `garbage`, `silent`.
Stopping the service with Ctrl+C is a pulled cable. After any run, check the mode:
`python sim_control.py --port 8700 mode`.

**Keep build output out of your repository:** add `--artifacts-path` with a folder outside it, or delete
`bin` and `obj` before you commit.

---

## What to submit

For each defect: **file and line**, **dimension**, **what goes wrong for the operator**, the **evidence**
(a command and what it printed), and **the fix**. Then:

- **The arguable one:** which defect, the strongest case for the AI's choice, and the strongest case
  against.
- **What I was unsure about:** something specific.

### How to spend 35 minutes

- **First 5:** build, test, run the demo in normal mode. Read the last column.
- **Next 12:** `drift` until the oven alarms, then stop the service while the demo runs. Then `freeze`.
  Then `garbage`, and check the simulator's mode afterward and its request log.
- **Next 8:** read `LinePanel` against the six requirements, one at a time.
- **Rest:** write up. Security first if you found it.

---

## Scoring

Five defects, one point each, plus one point for the arguable entry and the unsure entry together.
**Missing the Security defect costs two points instead of one.**

**Four of five is a strong score.**
