// ADAPTED from the course's HMI anchor, panel/Line3.Hmi.Core.Tests/LiveSimulatorTests.cs:
// port 8703 (the Unit 8 range), the sensor service found by searching upward,
// and the alarm checked against YOUR oven limit.
//
// LiveSimulatorTests.cs  .  145065 HMI anchor  .  Line3.Hmi.Core.Tests
//
// The real Python sensor service, started by this test, driven through every
// simulator mode, and read by the real client and monitor. This is the
// disconnect demo as an automated test.
//
// It needs Python 3 on PATH (or the HMI_PYTHON environment variable set to a
// Python executable). It uses port 8703 and stops the service when it ends.
//
// It finds sensor_service.py in a folder named sensor-service next to your
// HmiPanel folder (or in the course's 05-labs folder). Set HMI_SERVICE_DIR to
// the folder if yours is somewhere else.

using System.Diagnostics;
using System.Net.Http;
using System.Text;
using static Line3.Hmi.Core.Tests.TestData;

namespace Line3.Hmi.Core.Tests;

[Collection("network")]
public sealed class LiveSimulatorTests : IDisposable
{
    private const int Port = 8703;
    private readonly Process service;
    private readonly HttpClient control = new() { Timeout = TimeSpan.FromSeconds(3) };
    private readonly Uri baseUrl = new($"http://127.0.0.1:{Port}/");

    public LiveSimulatorTests()
    {
        Assert.True(FakeSensorService.IsFree(Port), $"port {Port} is busy; stop whatever is using it");
        string folder = FindServiceFolder();

        ProcessStartInfo start = new(Environment.GetEnvironmentVariable("HMI_PYTHON") ?? "python")
        {
            WorkingDirectory = folder,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true,
        };
        foreach (string arg in new[] { "sensor_service.py", "--port", Port.ToString(), "--interval", "0.2", "--quiet" })
        {
            start.ArgumentList.Add(arg);
        }

        // Keep Python from writing __pycache__ into the repository.
        start.Environment["PYTHONDONTWRITEBYTECODE"] = "1";
        service = Process.Start(start) ?? throw new InvalidOperationException("could not start Python");
    }

    private static string FindServiceFolder()
    {
        string? chosen = Environment.GetEnvironmentVariable("HMI_SERVICE_DIR");
        if (chosen is not null)
        {
            Assert.True(File.Exists(Path.Combine(chosen, "sensor_service.py")), "HMI_SERVICE_DIR has no sensor_service.py: " + chosen);
            return chosen;
        }

        for (DirectoryInfo? here = new(SourceFolder()); here is not null; here = here.Parent)
        {
            foreach (string candidate in new[] { "sensor-service", Path.Combine("05-labs", "sensor-service") })
            {
                string folder = Path.Combine(here.FullName, candidate);
                if (File.Exists(Path.Combine(folder, "sensor_service.py")))
                {
                    return folder;
                }
            }
        }

        Assert.Fail("No sensor-service folder found above " + SourceFolder() + ". Copy 05-labs/sensor-service next to HmiPanel, or set HMI_SERVICE_DIR.");
        return string.Empty;
    }

    public void Dispose()
    {
        StopService();
        control.Dispose();
        service.Dispose();
    }

    private void StopService()
    {
        if (!service.HasExited)
        {
            service.Kill(entireProcessTree: true);
            service.WaitForExit(10_000);
        }
    }

    private async Task WaitForHealthAsync()
    {
        Stopwatch timer = Stopwatch.StartNew();
        while (timer.Elapsed < TimeSpan.FromSeconds(15))
        {
            try
            {
                using HttpResponseMessage reply = await control.GetAsync(new Uri(baseUrl, "health"));
                if (reply.IsSuccessStatusCode)
                {
                    return;
                }
            }
            catch (HttpRequestException)
            {
            }
            catch (TaskCanceledException)
            {
            }

            Assert.False(service.HasExited, "the service exited: " + await service.StandardError.ReadToEndAsync());
            await Task.Delay(100);
        }

        Assert.Fail("the sensor service did not start within 15 s");
    }

    private async Task SetModeAsync(string mode, string? sensor = null)
    {
        string body = sensor is null ? $"{{\"mode\": \"{mode}\"}}" : $"{{\"mode\": \"{mode}\", \"sensor\": \"{sensor}\"}}";
        using StringContent content = new(body, Encoding.UTF8, "application/json");
        using HttpResponseMessage reply = await control.PostAsync(new Uri(baseUrl, "sim/mode"), content);
        Assert.True(reply.IsSuccessStatusCode, $"POST /sim/mode {mode} answered {(int)reply.StatusCode}");
    }

    private static async Task<PanelUpdate> PollUntilAsync(
        SensorClient client, PanelMonitor monitor, Func<PanelUpdate, bool> done, double seconds, string what)
    {
        Stopwatch timer = Stopwatch.StartNew();
        PanelUpdate update;
        do
        {
            monitor.Record(await client.PollAsync());
            update = monitor.Update(DateTimeOffset.UtcNow);
            if (done(update))
            {
                return update;
            }

            await Task.Delay(150);
        }
        while (timer.Elapsed < TimeSpan.FromSeconds(seconds));

        Assert.Fail($"gave up after {seconds} s waiting for: {what}. Last: "
                    + string.Join("; ", update.Sensors.Select(s => $"{s.SensorId}={s.State}/{s.Missing}"))
                    + $"; connection {update.Connection.State} {update.Connection.Detail}");
        return update;
    }

    private static SensorStatus Of(PanelUpdate update, string id) => update.Sensors.First(s => s.SensorId == id);

    [Fact]
    public async Task EveryModeProducesTheStateTheCourseDefines()
    {
        await WaitForHealthAsync();

        // Stale limit 3 s here, not 5, to keep the test short. The service
        // stamps whole seconds, so a limit under about 1.5 s would flag fresh
        // samples as stale.
        PanelConfig shipped = ShippedConfig();
        PanelConfig config = new(baseUrl, TimeSpan.FromMilliseconds(200), TimeSpan.FromMilliseconds(600),
                                 TimeSpan.FromSeconds(3), shipped.Sensors);
        using SensorClient client = new(baseUrl, config.RequestTimeout, SystemClock.Instance);
        PanelMonitor monitor = new(config);

        // normal: every sensor live and inside limits.
        PanelUpdate update = await PollUntilAsync(client, monitor,
            u => u.Sensors.All(s => s.State == SensorState.Normal), 5, "all normal");
        Assert.Equal(ConnectionState.Connected, update.Connection.State);

        // drift: the oven climbs into alarm, and the latch sets.
        await SetModeAsync("drift");
        update = await PollUntilAsync(client, monitor,
            u => Of(u, "oven-temp").State == SensorState.Alarm, 10, "oven alarm");
        Assert.Equal(AlarmSide.High, Of(update, "oven-temp").Side);
        Assert.True(Of(update, "oven-temp").LiveValue > shipped.Sensors.First(s => s.Id == "oven-temp").High);
        Assert.Equal(AlarmLatchState.ActiveUnacked, monitor.LatchOf("oven-temp"));

        // freeze: answers keep coming, nothing new. Stale, last value kept, alarm kept.
        await SetModeAsync("freeze");
        update = await PollUntilAsync(client, monitor,
            u => Of(u, "oven-temp").State == SensorState.Stale, 8, "oven stale");
        Assert.Null(Of(update, "oven-temp").LiveValue);
        Assert.True(Of(update, "oven-temp").LastKnownValue > shipped.Sensors.First(s => s.Id == "oven-temp").High);
        Assert.Equal(ConnectionState.NotUpdating, update.Connection.State);
        Assert.Equal(AlarmLatchState.ActiveUnacked, monitor.LatchOf("oven-temp"));

        // drop-sensor: one sensor missing, connection live again.
        await SetModeAsync("drop-sensor", "coolant-level");
        update = await PollUntilAsync(client, monitor,
            u => Of(u, "coolant-level").Missing == MissingReason.SensorFailed
                 && u.Connection.State == ConnectionState.Connected, 5, "coolant missing");
        Assert.Null(Of(update, "coolant-level").LiveValue);
        Assert.Equal(SensorState.Normal, Of(update, "press-vibration").State);

        // The oven cools during drop-sensor, so its alarm may have ended. Either
        // way, what happens next must not change the latch.
        AlarmLatchState ovenLatch = monitor.LatchOf("oven-temp");
        Assert.NotEqual(AlarmLatchState.Clear, ovenLatch);

        // garbage: every sensor missing, nothing trusted.
        await SetModeAsync("garbage");
        update = await PollUntilAsync(client, monitor,
            u => u.Connection.LastFailure == PollFailure.MalformedReply, 5, "malformed reply");
        Assert.All(update.Sensors, s => Assert.Equal(MissingReason.MalformedReply, s.Missing));
        Assert.Equal(ovenLatch, monitor.LatchOf("oven-temp"));

        // silent: the request times out on time.
        await SetModeAsync("silent");
        Stopwatch timer = Stopwatch.StartNew();
        PollResult silent = await client.PollAsync();
        Assert.Equal(PollFailure.Timeout, silent.Failure);
        Assert.InRange(timer.Elapsed.TotalSeconds, 0.5, 2.0);
        monitor.Record(silent);
        Assert.All(monitor.Update(DateTimeOffset.UtcNow).Sensors, s => Assert.Equal(MissingReason.Timeout, s.Missing));

        // Back to normal while silent: the control path still answers.
        await SetModeAsync("normal");
        await PollUntilAsync(client, monitor,
            u => u.Connection.State == ConnectionState.Connected, 5, "reconnected");

        // The service stops: the cable-pull. Nothing answers, alarm kept.
        // On Windows a refused connection takes about 2 s to report, longer
        // than this 0.6 s timeout, so it arrives as Timeout. Both are MISSING.
        StopService();
        update = await PollUntilAsync(client, monitor,
            u => u.Connection.LastFailure is PollFailure.ServiceDown or PollFailure.Timeout, 5, "service down");
        Assert.All(update.Sensors, s => Assert.Null(s.LiveValue));
        Assert.NotEqual(AlarmLatchState.Clear, monitor.LatchOf("oven-temp"));
        Assert.True(FakeSensorService.IsFree(Port), "the port should be free once the service stops");
    }
}
