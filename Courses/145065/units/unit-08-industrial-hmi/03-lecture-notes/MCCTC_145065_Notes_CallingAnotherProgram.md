# Lecture Notes: Calling Another Program Without Freezing Yours
## 145065 Object-Oriented Programming · Unit 8 · Week 15, Tuesday

**Slides for this lesson:**
[outline](../04-slides/MCCTC_145065_Slides_W15_CallingAnotherProgram.md). There is no exported deck
yet. To generate one, run this from the repository root:
`node tools/gamma.js Courses/145065/units/unit-08-industrial-hmi/04-slides/MCCTC_145065_Slides_W15_CallingAnotherProgram.md --export pptx`

If you missed class, you can learn this concept from this file alone. You need the .NET SDK, and Python
for the simulator.

**Competencies:** 5.5.4 programs that call other programs · 5.5.7 read inputs from a device · 5.3.10
error handling.

Every output below was printed by a real run: .NET SDK 10.0.401, `net8.0`, against the course's sensor
simulator on port 8700. Times can differ by a few hundredths of a second on your machine.

---

## Why this exists

The sensor service on the Pi is a separate program. Your panel does not own it and cannot see inside
it. All it can do is ask, over the network, and wait.

Waiting is the dangerous part. A panel that stops painting while it waits looks exactly like a panel
whose data is fine, until someone touches it. A Pi that never answers must not freeze the operator's
screen, and it must not be reported as a crash. It must become a plain sentence: no answer in time.

You met HTTP and JSON in the Python course. Today you call another program from C#, you give up on
time, and you keep your own program alive while you wait.

---

## The concept in plain language

**One question, one answer.** The panel sends `GET /api/readings`. The service replies with JSON: a
device name, a sequence number, the time the sample was taken, and one entry per sensor.

**`await` hands the thread back while you wait.** `HttpClient.GetAsync` returns a task, a promise of a
reply. `await` says "come back to this line when the reply arrives, and let the thread do other work
until then." In a window, that other work is painting and responding to touches.

**A timeout is a decision you make.** `HttpClient` has its own default of 100 seconds. An operator will
not wait 100 seconds. You set your own limit with a cancellation token that fires after, say, 1.5
seconds.

**Every failure gets a name.** The panel never lets an exception reach the window, and never keeps
showing an old value. Each failed poll becomes one of four results:

| Result | What happened | What a technician checks |
|---|---|---|
| **ServiceDown** | The connection was refused or broke | Is the service running? Is the cable in? |
| **Timeout** | No answer within the limit | Is the Pi overloaded or hung? |
| **HttpError** | An answer, but not 200 | Is the address right? |
| **MalformedReply** | A 200, but the body is not the contract | Is the service the right version? |

To the operator, all four mean the same thing: NO DATA. To the person fixing it, they mean four
different walks across the shop.

---

## Worked example 1: the same poll, three ways the service can behave

You write `PollAsync` yourself in Lab U8-02, so it is not printed here. What it looks like from the
outside is. The lab's console program asks the simulator once a second and counts **heartbeats**: how
many times its own 100 ms loop ran while the poll was waiting. A heartbeat proves the program was not
blocked.

Its first line names the question it asks:

```
LiveReader: polling http://127.0.0.1:8700/api/readings every 1.0 s, 1.5 s timeout
```

The simulator in normal mode:

```
poll  1  OK              seq 2     oven-temp 212.2 C  press-vibration 3.2 mm/s  coolant-level 67.7 %  (0.13 s, heartbeats 1)
```

The simulator in silent mode, where it accepts the connection and never answers:

```
poll  1  TIMEOUT         no answer within 1.5 s  (1.53 s, heartbeats 14)
```

Fourteen heartbeats. For a second and a half the program kept running while it waited.

With the service stopped, the result depends on the timeout, and this surprises people:

| Timeout | Result | Detail | Time |
|---|---|---|---|
| 1.5 s | TIMEOUT | `no answer within 1.5 s` | about 1.5 s |
| 5 s | SERVICEDOWN | `the connection failed: No connection could be made because the target machine actively refused it. (127.0.0.1:8700)` | 2.08 s |

On the course's build PC, Windows took about 2 seconds to refuse a connection to a closed port, so a
1.5-second limit fired first. Both results mean NO DATA to the operator. The detail is for whoever walks
over to the Pi.

---

## Worked example 2: a timeout you control

The same pattern with no network, so you can run it anywhere. The "service" takes 2 seconds. The caller
gives up at 0.3.

```csharp
using System.Diagnostics;

Stopwatch watch = Stopwatch.StartNew();
string result = await AskAsync(TimeSpan.FromSeconds(0.3), CancellationToken.None);
Console.WriteLine($"{result}  after about {watch.Elapsed.TotalSeconds:0.0} s");

static async Task<string> AskAsync(TimeSpan timeout, CancellationToken cancel)
{
    using CancellationTokenSource limit = CancellationTokenSource.CreateLinkedTokenSource(cancel);
    limit.CancelAfter(timeout);
    try
    {
        await SlowServiceAsync(limit.Token);
        return "OK";
    }
    catch (OperationCanceledException)
    {
        return $"TIMEOUT: no answer within {timeout.TotalSeconds:0.0} s";
    }
}

static Task SlowServiceAsync(CancellationToken token) => Task.Delay(TimeSpan.FromSeconds(2), token);
```

```
TIMEOUT: no answer within 0.3 s  after about 0.3 s
```

`CancelAfter` starts the clock. When it fires, the waiting `await` throws `OperationCanceledException`,
and the method turns that into a named result.

---

## Worked example 3: our timeout, or the window closing?

A wait can end early for two reasons. Your own timeout fired, which is news for the operator. Or the
window is closing, which is nobody's problem. The linked token combines both, and a `when` filter tells
them apart.

```csharp
using CancellationTokenSource closing = new();

Console.WriteLine(await AskAsync(TimeSpan.FromSeconds(0.2), closing.Token));

closing.CancelAfter(TimeSpan.FromSeconds(0.1));
try
{
    Console.WriteLine(await AskAsync(TimeSpan.FromSeconds(5), closing.Token));
}
catch (OperationCanceledException)
{
    Console.WriteLine("the window is closing, so the poll stopped quietly");
}

static async Task<string> AskAsync(TimeSpan timeout, CancellationToken cancel)
{
    using CancellationTokenSource limit = CancellationTokenSource.CreateLinkedTokenSource(cancel);
    limit.CancelAfter(timeout);
    try
    {
        await Task.Delay(TimeSpan.FromSeconds(2), limit.Token);
        return "OK";
    }
    catch (OperationCanceledException) when (cancel.IsCancellationRequested)
    {
        throw;
    }
    catch (OperationCanceledException)
    {
        return $"TIMEOUT: no answer within {timeout.TotalSeconds:0.0} s";
    }
}
```

```
TIMEOUT: no answer within 0.2 s
the window is closing, so the poll stopped quietly
```

The first call timed out on its own. In the second, the caller cancelled first, the `when` filter was
true, and the exception went back up to the caller. Order matters: the filtered `catch` comes first.

---

## The wrong version: blocking with `.Result` or `.Wait()`

The same caller, blocking:

```csharp
Console.WriteLine(Ask(TimeSpan.FromSeconds(0.3)));

static string Ask(TimeSpan timeout)
{
    using CancellationTokenSource limit = new();
    limit.CancelAfter(timeout);
    try
    {
        Task.Delay(TimeSpan.FromSeconds(2), limit.Token).Wait();
        return "OK";
    }
    catch (OperationCanceledException)
    {
        return "TIMEOUT";
    }
}
```

```
Unhandled exception. System.AggregateException: One or more errors occurred. (A task was canceled.)
```

Two things went wrong. **The thread was stuck** for the whole wait: in a window, that is a frozen
screen. **The exception changed shape**: `.Wait()` and `.Result` wrap the cancellation inside an
`AggregateException`, so the `catch (OperationCanceledException)` never matched, and the program died.

In the lab, the same mistake in `PollAsync` printed `heartbeats 0` on every line in normal mode, and in
silent mode:

```
Unhandled exception. System.AggregateException: One or more errors occurred. (A task was canceled.)
 ---> System.Threading.Tasks.TaskCanceledException: A task was canceled.
```

---

## Why the wrong version is tempting

`.Result` makes a compiler complaint about `async` go away in one word, and in normal mode the blocked
version looks faster: its time column reads 0.00 s. It only looks worse when the Pi is quiet, which is
the one moment the panel exists for.

---

## Honest cost

C# makes you write this out. Python's `requests` has a `timeout=` argument and no `async` in sight.
Here, every method that awaits must itself be `async`, all the way up to the window. That is more
typing. What it buys is a window that stays alive and a compiler that points at every place that waits.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Task** | A promise of a result that may not be ready yet |
| **`await`** | Wait for a task without blocking the thread |
| **Blocking** | Holding the thread until the work is done: `.Result`, `.Wait()` |
| **`CancellationToken`** | A signal that says "stop waiting" |
| **Linked token source** | One token that fires when any of its sources fires |
| **`when` filter** | A condition on a `catch`; the block runs only if it is true |
| **Timeout** | The longest you will wait before treating silence as a failure |
| **`AggregateException`** | A wrapper that `.Result` and `.Wait()` put around a task's exception |

---

## Self-check

**Question 1.** A poll prints `TIMEOUT` with `heartbeats 0` and `1.50 s`. What does that tell you about
the code?

**Question 2.** Why does `PollAsync` set `HttpClient.Timeout` to infinite instead of using it?

**Question 3.** The service answers with a 200 and the body `<html>Service starting</html>`. Which of the
four results should the panel report, and what does the operator see?

---

### Answers

**1.** The call blocked. It waited the full 1.5 seconds, and the heartbeat loop never ran, so the
thread was held the whole time. Somewhere a `.Result` or `.Wait()` replaced an `await`.

**2.** So the method can tell its own timeout apart from the caller's cancellation. `HttpClient`'s
timeout also arrives as a cancellation, and its default is 100 seconds. With one linked token that the
method controls, the `when` filter can decide whose cancellation it was, and the limit is the panel's
number, not the library's.

**3.** MalformedReply: an answer arrived with a 200, but it is not the contract's JSON. The operator
sees NO DATA, the same as for the other three. The detail is for the technician.
