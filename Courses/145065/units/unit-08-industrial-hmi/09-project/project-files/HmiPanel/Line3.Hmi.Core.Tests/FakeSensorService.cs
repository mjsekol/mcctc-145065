// ADAPTED from the course's HMI anchor, panel/Line3.Hmi.Core.Tests/FakeSensorService.cs:
// one port (8702, the Unit 8 range), and a faster free-port check.
//
// FakeSensorService.cs  .  145065 HMI anchor  .  Line3.Hmi.Core.Tests
//
// A stand-in for the Pi, started and stopped inside a test, so a test can
// hand the client any reply, including replies the real service never sends.
//
// It listens on 127.0.0.1 only, on port 8702. Tests that use it run one at a
// time (the "network" collection), so they never compete for a port.

using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Line3.Hmi.Core.Tests;

[CollectionDefinition("network", DisableParallelization = true)]
public sealed class NetworkCollection
{
}

public sealed class FakeSensorService : IDisposable
{
    public static readonly int[] Ports = { 8702 };

    private readonly HttpListener listener = new();
    private readonly CancellationTokenSource stopping = new();
    private readonly Task loop;
    private int requestCount;

    public FakeSensorService()
    {
        Port = Ports.FirstOrDefault(IsFree);
        if (Port == 0)
        {
            throw new InvalidOperationException("Port 8702 is busy. Stop whatever is using it: netstat -ano | findstr :8702");
        }

        BaseUrl = new Uri($"http://127.0.0.1:{Port}/");
        listener.Prefixes.Add(BaseUrl.ToString());
        listener.Start();
        loop = Task.Run(Serve);
    }

    public int Port { get; }

    public Uri BaseUrl { get; }

    public int StatusCode { get; set; } = 200;

    public string Body { get; set; } = "{}";

    public TimeSpan Delay { get; set; } = TimeSpan.Zero;

    public int RequestCount => Volatile.Read(ref requestCount);

    public string? LastPath { get; private set; }

    public string? LastMethod { get; private set; }

    /// <summary>
    /// True when nothing holds the port. It tries to take the port for a
    /// moment; asking by connecting is slower, because Windows can take about
    /// 2 s to refuse a connection to a closed port.
    /// </summary>
    public static bool IsFree(int port)
    {
        TcpListener probe = new(IPAddress.Loopback, port);
        try
        {
            probe.Start();
            return true;
        }
        catch (SocketException)
        {
            return false;
        }
        finally
        {
            probe.Stop();
        }
    }

    private async Task Serve()
    {
        while (!stopping.IsCancellationRequested)
        {
            HttpListenerContext context;
            try
            {
                context = await listener.GetContextAsync();
            }
            catch (Exception) when (stopping.IsCancellationRequested)
            {
                return;
            }
            catch (HttpListenerException)
            {
                return;
            }
            catch (ObjectDisposedException)
            {
                return;
            }

            _ = Task.Run(() => Answer(context));
        }
    }

    private async Task Answer(HttpListenerContext context)
    {
        Interlocked.Increment(ref requestCount);
        LastPath = context.Request.Url?.AbsolutePath;
        LastMethod = context.Request.HttpMethod;
        try
        {
            if (Delay > TimeSpan.Zero)
            {
                await Task.Delay(Delay, stopping.Token);
            }

            byte[] data = Encoding.UTF8.GetBytes(Body);
            context.Response.StatusCode = StatusCode;
            context.Response.ContentType = "application/json";
            context.Response.ContentLength64 = data.Length;
            await context.Response.OutputStream.WriteAsync(data);
            context.Response.Close();
        }
        catch (Exception)
        {
            // The client gave up or the test ended. Either way, nothing to do.
            try
            {
                context.Response.Abort();
            }
            catch (Exception)
            {
            }
        }
    }

    public void Dispose()
    {
        stopping.Cancel();
        listener.Stop();
        listener.Close();
        try
        {
            loop.Wait(TimeSpan.FromSeconds(5));
        }
        catch (AggregateException)
        {
        }

        stopping.Dispose();
    }
}
