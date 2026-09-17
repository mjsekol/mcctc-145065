# Gate 2: Adversarial Review · Week 15
## 145065 Object-Oriented Programming · Unit 8 · Week 15, Friday

**35 minutes.** Individual. You may and should build, test, and run the code, including against the
simulator. You may not ask an AI tool whether the code is correct, because an AI tool wrote it.

The code is in `gate2-w15-files/`. Copy the folder. Riverside Fabrication is a composite shop, and every
reading here is invented.

---

## What you are looking at

A teammate asked an AI assistant for the reading layer of the Line 3 panel, gave it the requirements in
Part A, and got the library in Part B. It builds with no warnings. Its own tests pass, nine of nine. The
comments sound sure of themselves.

**Five defects, one in each dimension of the code review.** In this course the defects are design
defects: they build, they run, and they look reasonable.

| Dimension | What to look for |
|---|---|
| **Correctness** | the panel shows something that is not true |
| **Security** | the code trusts what arrives from the network more than it should |
| **Readability** | a comment, a name, or a type that tells the next reader something false |
| **Performance** | work done more often than it can be useful |
| **Requirements Fit** | a promise in the requirements, or in an interface, that the code does not keep |

**One defect does not show until a sensor fails.** In normal mode the program looks perfect.
**One defect is arguable.** A reasonable person could defend it. Say which one you think it is, and argue
both sides.

---

## PART A: The requirements

> Write `Line3.Reader`, the C# library that reads the Line 3 sensor service for the operator panel.
>
> 1. Read `GET /api/readings` from the service address in `limits.json`.
> 2. The panel depends on an interface, `IReadingSource`, so tests can use a fake source.
> 3. A read gives up after `request_timeout_ms` from `limits.json` (1.5 s) and reports a failure.
>    It never waits longer.
> 4. Poll at `poll_interval_ms` from `limits.json`: once a second, the rate the Pi samples.
> 5. A sensor that reports `ok: false` has no value. It is never judged against a limit.
> 6. A value exactly on a limit is inside.
> 7. Everything from the network is untrusted. The contract reply is a few hundred bytes; do not read an
>    unbounded reply.
> 8. Report every failure as a result. Never throw for a network problem.

---

## PART B: What the AI produced

```
gate2-w15-files/
  Line3.Reader.sln
  Line3.Reader/            the library: 7 files
    SensorReading.cs       SensorReading, ReadingBatch, ReadResult
    IReadingSource.cs      the interface
    HttpReadingSource.cs   reads the service
    ReadingParser.cs       JSON to ReadingBatch
    LimitsFile.cs          SensorLimit, LimitsFile
    AlarmRules.cs          Normal, AlarmLow, AlarmHigh, NoData
    Poller.cs              the polling loop
  Line3.Reader.Demo/       a console program that polls and prints, with limits.json
  Line3.Reader.Tests/      the AI's own tests
```

From the `gate2-w15-files` folder:

```
dotnet build Line3.Reader.sln
dotnet test Line3.Reader.Tests
dotnet run --project Line3.Reader.Demo -- --url http://127.0.0.1:8700 --seconds 5
```

The demo prints one line per read: the time, the sequence, and each sensor with its value and its
`AlarmState`. Start the simulator first, in another terminal, from `05-labs/sensor-service/`:

```
python sensor_service.py --port 8700
```

To see what the service receives, start it **without** `--quiet`: it prints one line per request.

**Keep build output out of your repository:** add `--artifacts-path` with a folder outside it to each
`dotnet` command, or delete `bin` and `obj` before you commit.

---

## What to submit

For each defect: **file and line**, **dimension**, **what goes wrong for the operator or the line**, the
**evidence** (a command and what it printed, or a test), and **the fix**. Then two final entries:

- **The arguable one:** which defect, the strongest case for the AI's choice, and the strongest case
  against.
- **What I was unsure about:** something specific. A blank costs more than a wrong guess.

### How to spend 35 minutes

- **First 5:** build, run the tests, run the demo in normal mode for 5 seconds. Count the lines. Count
  the sequence numbers.
- **Next 10:** switch the simulator's mode while the demo runs:
  `python sim_control.py --port 8700 mode drop-sensor`, then with `--sensor coolant-level`, then
  `mode silent` with a longer `--seconds`. Watch what each line says.
- **Next 10:** read `IReadingSource`, then read how `HttpReadingSource` keeps each promise. Read every
  comment against the code under it.
- **Rest:** write up. Put the security defect first if you found it.

---

## Scoring

Five defects, one point each, plus one point for the arguable entry and the unsure entry together.
**Missing the Security defect costs two points instead of one.** Your instructor states this before you
start.

**Four of five is a strong score.**
