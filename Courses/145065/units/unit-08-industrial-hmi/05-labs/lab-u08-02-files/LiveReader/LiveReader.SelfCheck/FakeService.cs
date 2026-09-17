// FakeService.cs  .  Lab U08-02 self-check  .  given to you
//
// A stand-in for the Pi that a test starts and stops, so a test can hand your
// client any reply, including replies the real service never sends. Adapted
// from the HMI anchor's FakeSensorService.
//
// It listens on 127.0.0.1, port 8702 only. If something else holds 8702, the
// test says so instead of quietly using another port.

using System.Net;
using System.Net.Sockets;
using System.Text;

namespace LiveReader.SelfCheck;

[CollectionDefinition("network", DisableParallelization = true)]
public sealed class NetworkCollection
{
}

public sealed class FakeService : IDisposable
{
    public const int Port = 8702;

    private readonly HttpListener listener = new();
    private readonly CancellationTokenSource stopping = new();
    private readonly Task loop;

    public FakeService()
    {
        if (!IsFree(Port))
        {
            throw new InvalidOperationException($"Port {Port} is busy. Stop whatever is using it: netstat -ano | findstr :{Port}");
        }

        BaseUrl = new Uri($"http://127.0.0.1:{Port}/");
        listener.Prefixes.Add(BaseUrl.ToString());
        listener.Start();
        loop = Task.Run(Serve);
    }

    public Uri BaseUrl { get; }

    public int StatusCode { get; set; } = 200;

    public string Body { get; set; } = "{}";

    public TimeSpan Delay { get; set; } = TimeSpan.Zero;

    public string? LastPath { get; private set; }

    public string? LastMethod { get; private set; }

    /// <summary>
    /// True when nothing holds the port. It tries to take the port for a
    /// moment. (Asking by connecting is slower: Windows can take about 2 s to
    /// refuse a connection to a closed port.)
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
            catch (Exception)
            {
                return;
            }

            _ = Task.Run(() => Answer(context));
        }
    }

    private async Task Answer(HttpListenerContext context)
    {
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
