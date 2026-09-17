# Calling Another Program Without Freezing Yours
---
## Slide 1: The panel that looked fine
- The Pi went quiet
- The panel kept its last numbers
- Nobody noticed until someone touched the screen
- It had been frozen the whole time
Speaker notes: Picture this. The Pi stops answering. The panel is waiting for it, and while it waits, it stops painting. The numbers on the screen stay exactly where they were, calm and steady. Nobody notices anything is wrong until someone touches the screen and nothing happens. Today is about asking another program for data without letting the wait freeze yours.
Image: A control screen with a spinning cursor and steady green numbers.
---
## Slide 2: One question, one answer
- The panel sends GET /api/readings
- The Pi's service replies with JSON
- Device, sequence, sample time, one entry per sensor
- The panel never sends anything else
Speaker notes: The sensor service is a separate program. Your panel cannot see inside it. It asks one question, get slash api slash readings, and gets back JSON: the device name, a sequence number, the time the sample was taken, and one entry per sensor. That is the contract. The panel only ever asks. It never tells the Pi to do anything.
Image: Two boxes, panel and Pi, with a single arrow labelled GET and a reply arrow labelled JSON.
---
## Slide 3: await hands the thread back
- GetAsync returns a task, a promise
- await: come back when the reply arrives
- Meanwhile the window paints and responds
- Blocking holds the thread hostage
Speaker notes: HttpClient's GetAsync returns a task, a promise of a reply. The await keyword says: come back to this line when the reply arrives, and let the thread do other work until then. In a window, that other work is painting and responding to touches. The alternative, blocking, holds the thread until the reply comes, and the window cannot do anything at all.
Image: A relay runner handing off a baton instead of standing still holding it.
---
## Slide 4: A timeout you control
```csharp
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
```
```
TIMEOUT: no answer within 0.3 s  after about 0.3 s
```
Speaker notes: HttpClient's own default timeout is a hundred seconds. No operator waits that long. So we make our own. A linked cancellation token source starts from the caller's token, and CancelAfter starts a clock. When the clock fires, the waiting await throws an operation cancelled exception, and we turn it into a named result. The service here takes two seconds and we gave up at point three.
Image: None. This slide is code.
---
## Slide 5: Whose cancel was it?
```csharp
catch (OperationCanceledException) when (cancel.IsCancellationRequested)
{
    throw;
}
catch (OperationCanceledException)
{
    return $"TIMEOUT: no answer within {timeout.TotalSeconds:0.0} s";
}
```
```
TIMEOUT: no answer within 0.2 s
the window is closing, so the poll stopped quietly
```
Speaker notes: A wait can end early for two reasons. Our own timeout, which is news for the operator. Or the window is closing, which is nobody's problem. The when filter checks the caller's token. If the caller cancelled, we rethrow and let it go. Otherwise it was our timeout. The filtered catch has to come first. The output shows one of each.
Image: None. This slide is code.
---
## Slide 6: Four names for failure
- ServiceDown: refused or broken connection
- Timeout: no answer within the limit
- HttpError: an answer, but not 200
- MalformedReply: a 200 that breaks the contract
Speaker notes: Every failed poll becomes one of four results. Service down, when the connection is refused or breaks. Timeout, when nothing comes back in time. HTTP error, when the service answers with something other than two hundred. Malformed reply, when the body is not the contract. To the operator, all four mean no data. To the technician, they mean four different walks across the shop.
Image: Four labelled doors, each leading to a different part of a factory.
---
## Slide 7: The wrong way: .Result
```csharp
Task.Delay(TimeSpan.FromSeconds(2), limit.Token).Wait();
```
```
Unhandled exception. System.AggregateException: One or more errors occurred. (A task was canceled.)
```
Speaker notes: Here is the wrong way. Block with dot Wait, or dot Result. Two things break. The thread is stuck for the whole wait, which in a window is a frozen screen. And the exception changes shape. Blocking wraps the cancellation inside an aggregate exception, so our catch for operation cancelled never matches, and the program dies. In the lab, the same mistake printed heartbeats zero in normal mode and crashed in silent mode.
Image: None. This slide is code.
---
## Slide 8: Heartbeats prove it
- Normal mode: OK, 0.13 s, heartbeats 1
- Silent mode: TIMEOUT, 1.53 s, heartbeats 14
- Blocked version: heartbeats 0 every time
- A heartbeat means your program kept living
Speaker notes: The lab program counts heartbeats, a small loop that ticks every hundred milliseconds while a poll is out. In normal mode the reply came in point one three seconds with one heartbeat. In silent mode it gave up at one point five three seconds, with fourteen heartbeats. The program was alive the whole time. The blocked version shows zero, every time.
Image: A heart monitor line next to a poll timer.
---
## Slide 9: A stopped service surprised us
- Timeout 1.5 s: TIMEOUT
- Timeout 5 s: SERVICEDOWN after 2.08 s
- Windows took about 2 s to refuse
- Both mean NO DATA to the operator
Speaker notes: When we stopped the service, the result depended on the timeout. With one and a half seconds, the panel said timeout. With five seconds, it said service down, after two point zero eight seconds. On the course's build PC, Windows took about two seconds to refuse a connection to a closed port, so the shorter limit fired first. Both mean no data to the operator.
Image: A stopwatch beside a closed door.
---
## Slide 10: What you are about to build
- Lab U8-02: write PollAsync, step by step
- Fourteen self-checks, against a fake service
- A mode table from the real simulator
- A README section: why not .Result
Speaker notes: In both builds today you write PollAsync in Lab U8-02. The self-check runs a fake service on port 8702 and makes fourteen checks. Then you run the real simulator through its modes and fill in a table, including the heartbeat column. Last, you break it on purpose with dot Result, copy the crash into your README, and explain in one sentence why the panel never blocks.
Image: A terminal window showing a table of poll results with a heartbeat column.
---
