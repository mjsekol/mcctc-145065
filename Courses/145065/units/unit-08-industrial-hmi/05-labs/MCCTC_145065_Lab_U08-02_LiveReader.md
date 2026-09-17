# Lab U8-02: Live Reader
## 145065 Object-Oriented Programming · Unit 8 · Week 15, Tuesday

**Gate:** 3 (open tooling, AI allowed and logged). **Duration:** Tuesday Build 1 and Build 2.
**Competencies:** 5.5.4 (programs that call other programs), 5.5.7 (read inputs from a device),
5.3.10 (error handling), 5.1.4 (event-driven and asynchronous code).

Files: `lab-u08-02-files/LiveReader/`, a solution with three projects, and the simulator in
`sensor-service/`. `Contract.cs` and `ReadingParser.cs` are copied unchanged from the course's HMI
anchor; `PollResult.cs` is copied from the anchor's client. You write one method.

**Riverside Fabrication is a composite**, an invented shop. This lab touches no hardware: it reads the
simulator. The client you write sends only `GET` requests and never changes anything on the service.

---

## The scenario

The Line 3 panel is one program and the Pi's sensor service is another, on the other end of a cable
that a forklift can snag. When the Pi is slow, dead, or confused, the panel must say so within a second
and a half, and its window must keep answering the operator the whole time. A panel that freezes while
it waits looks exactly like a calm line.

## What you will build

`ReadingClient.PollAsync`: one request to the sensor service that awaits the reply, gives up on time, and
turns every way it can go wrong into one of four named results.

---

## The four results

| Result | Means | A technician checks |
|---|---|---|
| `ServiceDown` | nothing answered, or the connection broke | is the Pi on, is the service running, is the cable in |
| `Timeout` | something is listening and did not answer in time | is the service hung, is the network overloaded |
| `HttpError` | it answered with a status other than 200 | the service's own log |
| `MalformedReply` | it answered 200 with text that is not the contract | what the service is sending |

All four show the operator the same thing: NO DATA. They are separate so the person who fixes it knows
where to look.

---

## Starter code

```
LiveReader/
  LiveReader.sln
  LiveReader.Core/          the library
    Contract.cs             SensorSample, ReadingSnapshot (given)
    ReadingParser.cs        text to snapshot, or a reason (given)
    PollResult.cs           PollResult, PollFailure (given)
    ReadingClient.cs        YOU WRITE PollAsync
  LiveReader/               a console program that polls and prints (given)
  LiveReader.SelfCheck/     14 checks against a fake service on port 8702 (given)
```

The constructor in `ReadingClient.cs` is written for you. Read its comments: it keeps **one**
`HttpClient` for the life of the object, switches off `HttpClient`'s own timeout so yours can be told
apart from a caller's cancel, and refuses to buffer a reply over 64 KB. `PollAsync` throws
`NotImplementedException` until you write it, and the console program catches that and says so.

**Keep build output out of your repository.** Give every `dotnet` command an artifacts folder outside
it, for example `--artifacts-path C:\build\lab02` [VERIFY a folder students may write to], or delete
`bin` and `obj` before you commit.

---

## Part 1: Build 1, steps 1 through 6

### Step 1. Build, run, and check the starter

From `LiveReader/`:

```
dotnet build LiveReader.sln --artifacts-path C:\build\lab02
dotnet run --project LiveReader --artifacts-path C:\build\lab02 -- --polls 3
dotnet test LiveReader.SelfCheck --artifacts-path C:\build\lab02
```

**Observable result:** the build reports 0 warnings and 0 errors. The program prints
`poll  1  PollAsync is not written yet. Start at step 3.` The self-check reports 14 failed.

### Step 2. Start the simulator

In another terminal, in `sensor-service/`, check the port is free, then start it:

```
netstat -ano | findstr :8700
python sensor_service.py --port 8700
```

**Observable result:** `Line 3 sensor service on http://127.0.0.1:8700` and the simulator's banner.

### Step 3. Ask, and await the answer

Delete the `throw` line. Add `async` to the method's first line. Send the request with
`await http.GetAsync(ReadingsUrl, cancel)` and keep the response in a `using` variable.

**Observable result:** the project builds. If it does not, read "If it breaks" 1 and 2.

### Step 4. Anything but 200 is an error

If `response.StatusCode` is not `HttpStatusCode.OK`, return
`Failed(PollFailure.HttpError, ...)` with a detail that includes the status number.

**Observable result:** the project builds.

### Step 5. Read the body and parse it

Read the body with `await response.Content.ReadAsStringAsync(cancel)` and give it to
`ReadingParser.Parse`. A parse that worked is `PollResult.Success(parsed.Snapshot!, DateTimeOffset.UtcNow)`.
A parse that failed is `Failed(PollFailure.MalformedReply, parsed.Error!)`. Run the program:

```
dotnet run --project LiveReader --artifacts-path C:\build\lab02 -- --polls 3
```

**Observable result:** three `OK` lines with a sequence number that goes up, three sensors with values,
and `heartbeats 1` on each line. The self-check reports **11 passed, 3 failed**: S06, S07, and S10 still
fail.

### Step 6. A connection that fails is ServiceDown

Wrap the work in `try`. Catch `HttpRequestException` and return `Failed(PollFailure.ServiceDown, ...)`
with the exception's message in the detail.

**Observable result:** the self-check reports **13 passed, 1 failed**. S07 (nothing listening) and S10
(a reply over 64 KB) now pass, because both arrive as `HttpRequestException`. Only S06 fails. Commit.

---

## Part 2: Build 2, steps 7 through 12

### Step 7. Give up on time

Before the `try`, create one token that fires on the caller's cancel **or** on your timeout:

```csharp
using CancellationTokenSource limit = CancellationTokenSource.CreateLinkedTokenSource(cancel);
limit.CancelAfter(Timeout);
```

Pass `limit.Token` (not `cancel`) to both awaits. Catch `OperationCanceledException` and return
`Failed(PollFailure.Timeout, $"no answer within {Timeout.TotalSeconds:0.0} s")`.

**Observable result:** S06 passes. **S09 now fails.** Read its message before step 8.

### Step 8. The caller's cancel is not a timeout

When the window closes, the caller cancels, and that is not something to report as a Pi problem. Add a
second `catch` for `OperationCanceledException` **above** the one from step 7, with a filter,
`when (cancel.IsCancellationRequested)`, and `throw;` inside it.

**Observable result:** `dotnet test LiveReader.SelfCheck` reports **14 passed**.

### Step 9. Watch the heartbeats

The program counts 100 ms heartbeats while each poll is out. Switch the simulator to silent and poll:

```
python sim_control.py --port 8700 mode silent
dotnet run --project LiveReader --artifacts-path C:\build\lab02 -- --polls 3
```

**Observable result:** three `TIMEOUT` lines, each about 1.5 s, each with about 14 or 15 heartbeats. The
program kept counting while it waited. That is the window staying alive.

### Step 10. Fill the mode table

For each row, switch the simulator's mode, run `--polls 3`, and copy what you saw. For the last two rows,
stop the service with Ctrl+C first.

| Simulator | Result on each line | Detail | Seconds per poll | Heartbeats |
|---|---|---|---|---|
| normal | | | | |
| drift | | | | |
| freeze | | | | |
| drop-sensor | | | | |
| garbage | | | | |
| silent | | | | |
| stopped | | | | |
| stopped, with `--timeout 5` | | | | |

Under the table, answer: **in freeze mode every line says OK. What in the output tells you the data is
not new?** And: **why does a stopped service show TIMEOUT at 1.5 s but SERVICEDOWN with a 5 s
timeout?**

**Observable result:** eight rows from real runs, and two answers.

### Step 11. Break it on purpose

Restart the simulator in normal mode. In `PollAsync`, change

```csharp
using HttpResponseMessage response = await http.GetAsync(ReadingsUrl, limit.Token);
```

to

```csharp
using HttpResponseMessage response = http.GetAsync(ReadingsUrl, limit.Token).Result;
```

It builds with no warning. Run `--polls 2` in normal mode, then in silent mode, then run the self-check.

**Observable result:** in normal mode every line says `heartbeats 0`. In silent mode the program dies:

```
Unhandled exception. System.AggregateException: One or more errors occurred. (A task was canceled.)
```

The self-check reports **5 failed**. Copy the silent-mode line into your README under a heading
`## Why not .Result`, and write two sentences: what an operator would see, and why your
`catch (OperationCanceledException)` did not catch it. Then put `await` back and confirm 14 passed.

### Step 12. Stop, clean, commit

Ctrl+C the service and confirm `netstat -ano | findstr :8700` prints nothing. Make sure no `bin` or
`obj` folder is in your repository. Commit and push.

**Observable result:** the port is free and `git status` is clean.

---

## Acceptance criteria

- [ ] `dotnet test LiveReader.SelfCheck` reports 14 passed
- [ ] `PollAsync` awaits every call and never uses `.Result` or `.Wait()`
- [ ] The program shows heartbeats while a slow poll is out
- [ ] The mode table has eight rows from real runs and both answers
- [ ] The README has the `## Why not .Result` section
- [ ] The only request sent is `GET /api/readings`
- [ ] The service is stopped, the port is free, and no `bin` or `obj` is committed

---

## If it breaks

### 1. `await` in a method that is not async

```
ReadingClient.cs(73,50): error CS4032: The 'await' operator can only be used within an async method. Consider marking this method with the 'async' modifier and changing its return type to 'Task<Task<PollResult>>'.
ReadingClient.cs(78,24): error CS0029: Cannot implicitly convert type 'Line3.Hmi.Core.PollResult' to 'System.Threading.Tasks.Task<Line3.Hmi.Core.PollResult>'
```

**Cause:** you wrote `await` without adding `async` to the method's first line. Do not follow the first
message's suggestion literally: the return type is already `Task<PollResult>`. Add only `async`. Your
line numbers will differ.

### 2. `async` in the wrong place

```
ReadingClient.cs(63,29): error CS1983: The return type of an async method must be void, Task, Task<T>, a task-like type, IAsyncEnumerable<T>, or IAsyncEnumerator<T>
```

**Cause:** the return type was changed to `PollResult`. An async method returns `Task<PollResult>`; the
`return` statements inside still return a `PollResult`.

### 3. The catch blocks are in the wrong order

```
ReadingClient.cs(92,16): error CS0160: A previous catch clause already catches all exceptions of this or of a super type ('OperationCanceledException')
```

**Cause:** the plain `catch (OperationCanceledException)` is above the filtered one. The filtered catch
goes first.

### 4. S09 fails after step 7

```
Assert.ThrowsAny() Failure: No exception was thrown
Expected: typeof(System.OperationCanceledException)
```

**Cause:** your one `catch (OperationCanceledException)` turns the caller's cancel into a Timeout
result. Step 8 fixes it.

### 5. S06 fails with Expected: Timeout, Actual: None

```
Assert.Equal() Failure: Values differ
Expected: Timeout
Actual:   None
```

**Cause:** no timeout is applied, so the read waited for the slow fake service and succeeded after 4 s.
`HttpClient`'s own timeout is switched off in the constructor on purpose. Step 7 applies yours.

### Not an error: a stopped service shows TIMEOUT

On the build machine, Windows took about 2 seconds to refuse a connection to a port with nothing
listening, longer than the 1.5 s timeout, so a stopped service showed `TIMEOUT` at 1.5 s. With
`--timeout 5` the refusal arrived first, at about 2.1 s, as `SERVICEDOWN`. Both are MISSING to the
operator. How fast the lab Pi refuses across the network is something to measure [VERIFY].

### Not an error: every poll takes about 0.11 s and 1 heartbeat

The program looks at the poll once every 100 ms. A reply that took a few milliseconds is noticed at the
first heartbeat. The column shows the heartbeat's resolution, not the network's speed.

---

## Stretch goal

Add a detail to every `ServiceDown` result that names the address it tried, and to every `Timeout`
result that names how long it waited. Then run the mode table's last two rows again and compare the
details a technician would read.

---

## Submission checklist

- [ ] Self-check 14 of 14
- [ ] Mode table and answers, and `## Why not .Result`, in the lab README
- [ ] `await` restored after step 11
- [ ] Port free, no `bin` or `obj` committed
- [ ] AI usage log updated if you used a model
- [ ] Pushed

---

# Extended Lab Options

All four versions assess the same competencies and grade on the same 100-point five-dimension scale.

## Which version to hand a student

| What you observe | Hand them |
|---|---|
| No build by 15 minutes into Build 1, or the student has added `.Result` to make an error go away | SCAFFOLDED |
| Steady progress through the self-check counts | STANDARD |
| 14 of 14 before Build 2 is half over | EXTENDED |
| "Why would I ever need this outside a factory?" | APPLIED |

---

## SCAFFOLDED

**Changed sections:**

- **Starter code:** `PollAsync` arrives with the `try` and all three `catch` blocks in the right order,
  each with an empty body and a comment naming the result it returns. The student writes the request,
  the status check, the parse, and the four `return` lines.
- **Steps:** steps 3-8 become "fill each block, then run the self-check". Step 10 needs four rows:
  normal, garbage, silent, stopped.
- **Checkpoints:** show the self-check count to the instructor after the request and after the catches.
- **Keep step 11.** The frozen heartbeat is the lesson.

**Acceptance criteria:** 14 of 14, the four-row table, the `## Why not .Result` section.

**Grading:** same scale. Requirements Fit is judged against this version's list.

---

## STANDARD

The base lab above, unchanged.

---

## EXTENDED

Everything in STANDARD, plus a way to poll that the program reads with `await foreach`.

**Added requirement.** Write `WatchAsync(TimeSpan interval, CancellationToken cancel)`, an extension
method on `ReadingClient` that returns `IAsyncEnumerable<PollResult>`: it polls, hands back each
result, waits out the rest of the interval (start to start, so a slow poll shortens the wait), and ends
quietly when cancelled. Add a check that runs it against the fake service for 1.1 s at a 200 ms interval
and gets between four and seven results, all OK.

**Hint, not the answer.** Look up "asynchronous streams" and `IAsyncEnumerable<T>` in the C# language
documentation on learn.microsoft.com [VERIFY the exact page], and read about the `yield return`
statement and the `[EnumeratorCancellation]` attribute.

**Acceptance criteria:** all STANDARD criteria; your new check passes; the program still passes 14 of 14.

**Grading:** same scale.

---

## APPLIED

**For the student who asks where else this matters.** The same skill, somewhere else.

**Changed scenario.** A school's bus-arrival screen in the front lobby asks the district's bus-tracking
service, every few seconds, how far away each bus is. When the service is slow or down, families
standing in the lobby must see "arrival time unknown", never a stale "2 minutes", and the screen must
keep scrolling announcements. Build a fake bus service with Python's `http.server` on port 8703 that can
answer normally, slowly, with an error, or with garbage (invented bus numbers only, no student or
family information), and a C# client with the same four results.

**What you build.** A `BusClient.PollAsync` with the same rules as `ReadingClient`, and a console
program that shows heartbeats while it waits.

**Acceptance criteria:** your client returns each of the four results against your fake service, with
the heartbeat count showing it never blocked; your README has a mode table and the
`## Why not .Result` section for your domain.

**Grading:** same scale. Requirements Fit is judged on whether "unknown" is shown for every failure.
